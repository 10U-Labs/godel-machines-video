/* The shared kit of src/blender/kit.py, drawn as SVG in a browser page.

A trial: it holds what the first scene of the Gödel machines film needs, so
that the scene can be rendered by Hyperframes and set beside its Blender clip.

Every scene is built from flat 2D shapes set out in depth, as in Blender. The
kit works out where the camera sees each shape and writes that as the shape's
SVG transform, so a moving camera gives the same parallax. What is near or far
is blurred by as much as the Blender camera's depth of field blurs it.

Design units are screen units at depth z = 0, seen from the camera's start
height H0: the frame spans x from -8 to 8 and y from -4.5 to 4.5.

A scene is drawn for a time and for nothing else: render(t) gives the same
picture whatever was drawn before it.
*/
'use strict';

const kit = (() => {
  const H0 = 20.0;
  const WIDTH = 1920;
  const HEIGHT = 1080;
  const UNIT = WIDTH / 16;                 // pixels to a design unit at the camera's start height
  const LENS = 0.036 * H0 / 16;            // the Blender camera's lens and sensor, in metres
  const SENSOR = 0.036;
  const SVG = 'http://www.w3.org/2000/svg';

  // Colours (sRGB hex), one palette for every scene.
  const palette = {
    INK900: '#0b1030', INK800: '#121a47', INK700: '#1b2660', INK600: '#27347d', INK500: '#3a4aa3',
    MINT: '#4fe3c1', MINT_DEEP: '#1fae93', AMBER: '#ffc24b', AMBER_DEEP: '#f09a1f',
    CORAL: '#ff6b6b', CORAL_DEEP: '#d9434f', VIOLET: '#a78bfa', VIOLET_DEEP: '#7357e0',
    SKY: '#5cc8ff', SKY_DEEP: '#2b93e0', PAPER: '#f4f1ff', MIST: '#b9c0ea', SLATE: '#7c86c2',
  };

  const state = { fps: 30, frames: 1, zstep: 0.002 };
  let nodes = [];
  let materials = new Map();
  let view = null;
  let drawn = null;

  function setup(options) {
    state.fps = options.fps;
    state.frames = options.frames;
    nodes = [];
    materials = new Map();
    view = null;
    drawn = null;
  }

  // ---------------------------------------------------------------- Python's random numbers

  /* The Mersenne Twister as Python's random module runs it, so that a seed
     lays out specks and lines of code here just as it does in Blender. */
  class Random {
    constructor(seed) {
      this.mt = new Uint32Array(624);
      this.seedArray([seed >>> 0]);
    }

    seedArray(key) {
      const mt = this.mt;
      mt[0] = 19650218;
      for (let i = 1; i < 624; i++) {
        mt[i] = (Math.imul(1812433253, mt[i - 1] ^ (mt[i - 1] >>> 30)) + i) >>> 0;
      }
      let i = 1;
      let j = 0;
      for (let k = Math.max(624, key.length); k; k--) {
        mt[i] = ((mt[i] ^ Math.imul(mt[i - 1] ^ (mt[i - 1] >>> 30), 1664525)) + key[j] + j) >>> 0;
        i++;
        j++;
        if (i >= 624) { mt[0] = mt[623]; i = 1; }
        if (j >= key.length) j = 0;
      }
      for (let k = 623; k; k--) {
        mt[i] = ((mt[i] ^ Math.imul(mt[i - 1] ^ (mt[i - 1] >>> 30), 1566083941)) - i) >>> 0;
        i++;
        if (i >= 624) { mt[0] = mt[623]; i = 1; }
      }
      mt[0] = 0x80000000;
      this.at = 624;
    }

    bits() {
      const mt = this.mt;
      if (this.at >= 624) {
        const twist = (y, far) => far ^ (y >>> 1) ^ ((y & 1) ? 0x9908b0df : 0);
        for (let k = 0; k < 624; k++) {
          const y = (mt[k] & 0x80000000) | (mt[(k + 1) % 624] & 0x7fffffff);
          mt[k] = twist(y, mt[(k + 397) % 624]);
        }
        this.at = 0;
      }
      let y = mt[this.at++];
      y ^= y >>> 11;
      y ^= (y << 7) & 0x9d2c5680;
      y ^= (y << 15) & 0xefc60000;
      y ^= y >>> 18;
      return y >>> 0;
    }

    random() {
      const a = this.bits() >>> 5;
      const b = this.bits() >>> 6;
      return (a * 67108864 + b) / 9007199254740992;
    }

    randrange(n) {
      const shift = Math.clz32(n);
      let r = this.bits() >>> shift;
      while (r >= n) r = this.bits() >>> shift;
      return r;
    }
  }

  // ---------------------------------------------------------------- timing

  /* Narration timings for one scene, in seconds. */
  class Timing {
    constructor(entry) {
      this.duration = entry.duration;
      this.lines = entry.lines.map((line) => [line.start, line.end]);
    }

    start(i) { return this.lines[i][0]; }

    end(i) { return this.lines[i][1]; }

    /* A moment part way through line i (share 0 is its start, 1 its end). */
    at(i, share) {
      const [s, e] = this.lines[i];
      return s + share * (e - s);
    }
  }

  /* Python's round: a half goes to the even neighbour. */
  function round(x) {
    const low = Math.floor(x);
    const part = x - low;
    if (part < 0.5) return low;
    if (part > 0.5) return low + 1;
    return low % 2 === 0 ? low : low + 1;
  }

  const frames = () => state.frames;

  /* The frame shown at a time in seconds (frames count from 1, as in Blender). */
  const fr = (seconds) => Math.max(1, Math.min(state.frames, round(seconds * state.fps) + 1));

  const sec = (frame) => (frame - 1) / state.fps;

  function every(step = 1, f0 = 1, f1 = null) {
    const last = f1 === null ? state.frames : f1;
    const out = [];
    for (let f = Math.max(1, f0); f <= last; f += step) out.push(f);
    if (out.length && out[out.length - 1] !== last) out.push(last);
    return out;
  }

  /* Holds a time inside the frames from f0 to f1, as a curve keyed only there holds its end values. */
  const within = (t, f0, f1) => Math.min(sec(f1), Math.max(sec(f0), t));

  // ---------------------------------------------------------------- motion

  const clamp = (p) => Math.min(1.0, Math.max(0.0, p));

  function smooth(p) {
    p = clamp(p);
    return p * p * (3 - 2 * p);
  }

  function easeOut(p) {
    p = clamp(p);
    return 1 - (1 - p) ** 3;
  }

  /* Overshoots a little and settles: for things that pop in. */
  function backOut(p, s = 1.9) {
    p = clamp(p) - 1;
    return 1 + (s + 1) * p ** 3 + s * p ** 2;
  }

  /* Progress from 0 to 1 as time t (seconds) goes from t0 to t1. */
  function span(t, t0, t1, ease = smooth) {
    if (t1 <= t0) return t >= t1 ? 1.0 : 0.0;
    return ease(clamp((t - t0) / (t1 - t0)));
  }

  const mix = (a, b, p) => a + (b - a) * p;

  /* A value keyed on a few frames, as a Blender curve is: it eases from each
     key to the next, and holds the first and last. */
  class Track {
    constructor(value) {
      this.now = value;
      this.keys = new Map();
      this.curve = null;
    }

    /* Key the value as it stands, at a time: Blender's keyframe_insert. */
    insert(t) { return this.keyFrame(fr(t), this.now); }

    key(t, value) { return this.keyFrame(fr(t), value); }

    keyFrame(frame, value) {
      this.now = value;
      this.keys.set(frame, value);
      this.curve = null;
      return this;
    }

    build() {
      const fs = [...this.keys.keys()].sort((a, b) => a - b);
      const rows = fs.map((f) => [].concat(this.keys.get(f)));
      const slopes = rows.map(() => rows[0].map(() => 0));
      for (let c = 0; c < rows[0].length; c++) {
        for (let i = 1; i < fs.length - 1; i++) {
          const h0 = fs[i] - fs[i - 1];
          const h1 = fs[i + 1] - fs[i];
          const d0 = (rows[i][c] - rows[i - 1][c]) / h0;
          const d1 = (rows[i + 1][c] - rows[i][c]) / h1;
          if (d0 * d1 > 0) {
            const w0 = 2 * h1 + h0;
            const w1 = h1 + 2 * h0;
            slopes[i][c] = (w0 + w1) / (w0 / d0 + w1 / d1);
          }
        }
      }
      this.curve = { fs, rows, slopes, single: !Array.isArray(this.now) };
    }

    at(t) {
      if (!this.keys.size) return this.now;
      if (!this.curve) this.build();
      const { fs, rows, slopes, single } = this.curve;
      const f = t * state.fps + 1;
      let out;
      if (f <= fs[0]) {
        out = rows[0];
      } else if (f >= fs[fs.length - 1]) {
        out = rows[rows.length - 1];
      } else {
        let i = 0;
        while (fs[i + 1] <= f) i++;
        const h = fs[i + 1] - fs[i];
        const s = (f - fs[i]) / h;
        const s2 = s * s;
        const s3 = s2 * s;
        out = rows[i].map((v0, c) => (2 * s3 - 3 * s2 + 1) * v0 + (s3 - 2 * s2 + s) * h * slopes[i][c]
          + (3 * s2 - 2 * s3) * rows[i + 1][c] + (s3 - s2) * h * slopes[i + 1][c]);
      }
      return single ? out[0] : out;
    }
  }

  // ---------------------------------------------------------------- materials

  function linear(hex) {
    const out = [];
    for (const i of [1, 3, 5]) {
      const c = parseInt(hex.slice(i, i + 2), 16) / 255;
      out.push(c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
    }
    return out;
  }

  const encode = (c) => (c <= 0.0031308 ? c * 12.92 : 1.055 * c ** (1 / 2.4) - 0.055);

  const hex = (encoded) => '#' + encoded.map((c) => Math.round(255 * clamp(c)).toString(16).padStart(2, '0')).join('');

  /* The colour that a see-through colour gives over another, mixed as light, which is how Blender mixes them. */
  function laid(colour, alpha, over) {
    const back = linear(over);
    const front = linear(colour);
    return hex(back.map((b, c) => encode(b * (1 - alpha) + front[c] * alpha)));
  }

  // What see-through shapes mostly lie over: the middle of the backdrop's sky, bare and with its glow.
  const DEEP_BEHIND = laid(palette.INK800, 0.5, palette.INK900);
  const SKY_BEHIND = laid(palette.VIOLET_DEEP, 0.35 * 0.6 ** 1.2, DEEP_BEHIND);

  /* A flat colour, or a gradient from bottom to top of the shape, with alpha.
     over is the colour a see-through shape mostly lies over; the sky if none is given. */
  function material(top, bottom = null, alpha = 1.0, over = null) {
    const id = ['flat', top, bottom, alpha, over].join('|');
    if (!materials.has(id)) materials.set(id, { kind: bottom === null ? 'flat' : 'linear', top, bottom, alpha, over: over || SKY_BEHIND });
    return materials.get(id);
  }

  /* A soft round glow: bright in the middle, fading toward the edge. */
  function glowMaterial(colour, alpha = 0.5, power = 1.6, over = null) {
    const id = ['glow', colour, alpha, power, over].join('|');
    if (!materials.has(id)) materials.set(id, { kind: 'radial', top: colour, alpha, power, over: over || SKY_BEHIND });
    return materials.get(id);
  }

  /* The colour and alpha to draw so that a see-through shape looks as it does in Blender.

     Blender lays a see-through colour over what is behind it by mixing the two
     as light. A browser mixes the two colours' sRGB numbers, which leaves a
     light colour over a dark one much darker. So the mix is worked out here as
     light, over the colour the shape mostly lies over, and the browser is given
     the colour and alpha that bring it to that result. */
  function seeThrough(colour, alpha, over) {
    if (alpha >= 1) return [colour, 1];
    if (alpha <= 0) return [colour, 0];
    const back = linear(over);
    const front = linear(colour);
    const behind = back.map(encode);
    const wanted = back.map((b, c) => encode(b * (1 - alpha) + front[c] * alpha));
    let drawn = alpha;
    wanted.forEach((w, c) => {
      drawn = Math.max(drawn, w >= behind[c] ? (w - behind[c]) / (1 - behind[c]) : (behind[c] - w) / behind[c]);
    });
    return [hex(wanted.map((w, c) => behind[c] + (w - behind[c]) / drawn)), drawn];
  }

  // ---------------------------------------------------------------- shapes

  /* Later shapes sit a hair closer to the camera, so they draw on top. */
  function nextZ(parent, lift = 0.0) {
    if (!parent) return 0.0;
    let root = parent;
    while (root.parent) root = root.parent;
    root.order += 1;
    return lift + root.order * state.zstep;
  }

  function node(kind, name, parent, loc, scale, rot) {
    const made = {
      kind, name, parent, order: 0, index: nodes.length,
      x: loc[0], y: loc[1], z: loc[2], sx: scale, sy: scale, sz: scale, rot, alpha: 1.0,
      move: {},           // loc, scale, rot, alpha: each a function of time, or a Track
      world: null,
    };
    nodes.push(made);
    return made;
  }

  function empty(name, parent = null, loc = [0, 0, 0], scale = 1.0, rot = 0.0) {
    const z = loc.length === 3 ? loc[2] : nextZ(parent);
    return node('empty', name, parent, [loc[0], loc[1], z], scale, rot);
  }

  /* A depth layer. Its children use screen units at the camera's start position. */
  function layer(name, z, options = {}) {
    const made = empty(name, null, [0, 0, z], (H0 - z) / H0);
    made.sharp = options.sharp === true;
    return made;
  }

  /* A filled 2D shape from points given relative to its own origin at loc.

     options.inside names another shape, and this one is then drawn only where that one is.
     It is for a see-through shape that lies over two colours and shows over one of them alone:
     the page works a see-through colour out over a single colour behind it (see seeThrough). */
  function shape(name, pts, mat, parent, loc = [0, 0], options = {}) {
    const made = node('shape', name, parent, [loc[0], loc[1], nextZ(parent, options.lift || 0.0)], 1.0, options.rot || 0.0);
    made.pts = pts;
    made.mat = mat;
    made.inside = options.inside || null;
    return made;
  }

  function circlePts(r, rx = null, ry = null, n = 40) {
    const out = [];
    for (let i = 0; i < n; i++) {
      out.push([(rx || r) * Math.cos(2 * Math.PI * i / n), (ry || r) * Math.sin(2 * Math.PI * i / n)]);
    }
    return out;
  }

  function rrectPts(w, h, r, n = 6) {
    r = Math.min(r, w / 2, h / 2);
    if (r <= 0) return [[w / 2, h / 2], [-w / 2, h / 2], [-w / 2, -h / 2], [w / 2, -h / 2]];
    const out = [];
    const corners = [[w / 2 - r, h / 2 - r, 0], [-w / 2 + r, h / 2 - r, 90], [-w / 2 + r, -h / 2 + r, 180], [w / 2 - r, -h / 2 + r, 270]];
    for (const [cx, cy, a0] of corners) {
      for (let i = 0; i <= n; i++) {
        const a = (a0 + 90 * i / n) * Math.PI / 180;
        out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
      }
    }
    return out;
  }

  /* A rounded bar whose left end sits at the origin, so scaling x grows it rightward. */
  const barPts = (w, h) => rrectPts(w, h, h / 2).map(([x, y]) => [x + w / 2, y]);

  /* A rounded bar hanging down from its origin: from (0, 0) to (0, -length). */
  function capsulePts(length, w, n = 10) {
    const r = w / 2;
    const out = [];
    for (let i = 0; i <= n; i++) out.push([r * Math.cos(Math.PI * i / n), r * Math.sin(Math.PI * i / n)]);
    for (let i = 0; i <= n; i++) {
      out.push([r * Math.cos(Math.PI + Math.PI * i / n), -length + r * Math.sin(Math.PI + Math.PI * i / n)]);
    }
    return out;
  }

  /* A curved band, such as a smile: radius r, width w, from angle a0 to a1 in degrees. */
  function arcPts(r, w, a0, a1, n = 16) {
    const at = (radius, angle) => [radius * Math.cos(angle * Math.PI / 180), radius * Math.sin(angle * Math.PI / 180)];
    const out = [];
    for (let i = 0; i <= n; i++) out.push(at(r + w / 2, a0 + (a1 - a0) * i / n));
    for (let i = 0; i <= n; i++) out.push(at(r - w / 2, a1 - (a1 - a0) * i / n));
    return out;
  }

  function starPts(rOut, rIn, points = 4) {
    const out = [];
    for (let i = 0; i < points * 2; i++) {
      const r = i % 2 === 0 ? rOut : rIn;
      out.push([r * Math.cos(Math.PI * i / points + Math.PI / 2), r * Math.sin(Math.PI * i / points + Math.PI / 2)]);
    }
    return out;
  }

  /* Blender draws a font at its own size and weight, and the page follows it. It scales a font so
     that the box around all its glyphs is one unit tall, where a browser makes the em one unit:
     scale is the em over that box. It puts the middle of that box on the text's origin, which
     leaves the baseline drop ems below it. And it draws a font of many weights at the weight the
     file names as its default. The numbers are read from the files in src/fonts/. */
  const FACES = {
    Figtree: { family: 'Figtree', scale: 1000 / 1132, drop: 0.346, weight: 300 },
    JetBrainsMono: { family: 'JetBrains Mono', scale: 1000 / 1320, drop: 0.36, weight: 400 },
  };

  function text(name, body, size, mat, parent, loc, face = 'Figtree') {
    const made = node('text', name, parent, [loc[0], loc[1], nextZ(parent)], 1.0, 0.0);
    made.body = body;
    made.size = size;
    made.mat = mat;
    made.face = FACES[face];
    return made;
  }

  /* Fade a shape in at tIn and out at tOut (seconds); either may be null. */
  function fade(made, tIn = null, tOut = null, dur = 0.4) {
    made.move.alpha = (t) => {
      let v = 1.0;
      if (tIn !== null) v *= span(t, tIn, tIn + dur);
      if (tOut !== null) v *= 1 - span(t, tOut, tOut + dur);
      return v;
    };
  }

  // ---------------------------------------------------------------- the stage

  /* A deep blue field with a soft glow and faint specks at a few depths. */
  function backdrop(seed = 3, glow = palette.VIOLET_DEEP) {
    const rnd = new Random(seed);
    const back = layer('back', -6.0, { sharp: true });
    shape('sky', rrectPts(28, 16, 0), material(palette.INK800, palette.INK900), back);
    shape('sky-glow', circlePts(9.0, null, 6.5), glowMaterial(glow, 0.35, 1.2, DEEP_BEHIND), back, [0, 0.5]);
    for (let i = 0; i < 70; i++) {
      const z = -5.0 + rnd.random() * 5.5;
      const s = (H0 - z) / H0;
      const x = (-9 + rnd.random() * 18) * 1.3;
      const y = (-5 + rnd.random() * 10) * 1.3;
      const r = 0.03 + rnd.random() * 0.04;
      const speck = shape(`speck${i}`, circlePts(r, null, null, 12), material(palette.MIST, null, 0.25 + rnd.random() * 0.4), null);
      const phase = rnd.random() * 2 * Math.PI;
      [speck.x, speck.y, speck.z] = [x * s, y * s, z];
      speck.move.alpha = (t) => 0.6 + 0.4 * Math.sin(t * 1.3 + phase);
    }
    return back;
  }

  /* Out-of-focus specks close to the camera, drifting slowly upward. */
  function motes(n = 30, seed = 5, colour = palette.MINT) {
    const rnd = new Random(seed);
    for (let i = 0; i < n; i++) {
      const z = 3.0 + rnd.random() * 9.0;
      const s = (H0 - z) / H0;
      const x = -9 + rnd.random() * 18;
      const y = -5 + rnd.random() * 10;
      const r = 0.03 + rnd.random() * 0.05;
      const mote = shape(`mote${i}`, circlePts(r, null, null, 12), material(colour, null, 0.25 + rnd.random() * 0.35), null);
      const phase = rnd.random() * 2 * Math.PI;
      const speed = 0.05 + rnd.random() * 0.1;
      mote.z = z;
      mote.move.loc = (t) => [(x + 0.2 * Math.sin(t * 0.5 + phase)) * s, (y + speed * t) * s];
    }
  }

  /* A camera that looks straight down the z axis.
     path(t) returns [x, y, height] at time t in seconds; focus stays on depth focusZ. */
  function camera(path, focusZ = 1.0, fstop = 0.3) {
    view = { path, focusZ, fstop };
  }

  // ---------------------------------------------------------------- drawing

  const read = (source, t) => (typeof source === 'function' ? source(t) : source.at(t));

  /* Where a node is at a time: a 2D matrix for x and y, and its depth. */
  function place(made, t) {
    const move = made.move;
    let { x, y, z, sx, sy, sz, rot, alpha } = made;
    if (move.loc) {
      const v = read(move.loc, t);
      x = v[0];
      y = v[1];
      if (v.length > 2) z = v[2];
    }
    if (move.scale) {
      const v = read(move.scale, t);
      if (typeof v === 'number') {
        sx = sy = sz = v;
      } else {
        sx = v[0];
        sy = v[1];
        sz = v.length > 2 ? v[2] : 1.0;
      }
    }
    if (move.rot) rot = read(move.rot, t);
    if (move.alpha) alpha = read(move.alpha, t);
    const cos = Math.cos(rot);
    const sin = Math.sin(rot);
    const local = [sx * cos, sx * sin, -sy * sin, sy * cos, x, y];
    const up = made.parent ? made.parent.world : { m: [1, 0, 0, 1, 0, 0], z: 0, sz: 1 };
    const p = up.m;
    made.world = {
      m: [
        p[0] * local[0] + p[2] * local[1], p[1] * local[0] + p[3] * local[1],
        p[0] * local[2] + p[2] * local[3], p[1] * local[2] + p[3] * local[3],
        p[0] * local[4] + p[2] * local[5] + p[4], p[1] * local[4] + p[3] * local[5] + p[5],
      ],
      z: up.z + up.sz * z,
      sz: up.sz * sz,
      alpha,
    };
  }

  function element(tag, attributes, parent) {
    const made = document.createElementNS(SVG, tag);
    for (const [name, value] of Object.entries(attributes)) made.setAttribute(name, value);
    if (parent) parent.appendChild(made);
    return made;
  }

  /* A shape's fill, and the alpha to draw the whole shape with.

     Blender runs a gradient across a box that is one unit larger on every side
     than the shape's points. So a shape shows only the middle of its gradient:
     a small glow is nearly even and ends in a hard edge, and a thin bar is
     nearly one colour. The gradients here are laid over the same box. */
  function paint(made, defs, ids) {
    const mat = made.mat;
    if (mat.kind === 'flat') {
      const [colour, alpha] = seeThrough(mat.top, mat.alpha, mat.over);
      return { fill: colour, alpha };
    }
    const xs = made.pts.map((pt) => pt[0]);
    const ys = made.pts.map((pt) => pt[1]);
    const mid = [(Math.min(...xs) + Math.max(...xs)) / 2, (Math.min(...ys) + Math.max(...ys)) / 2];
    const half = [(Math.max(...xs) - Math.min(...xs)) / 2 + 1, (Math.max(...ys) - Math.min(...ys)) / 2 + 1];
    const key = [mat.kind, mat.top, mat.bottom, mat.alpha, mat.power, mat.over, ...mid, ...half].join('|');
    if (!ids.has(key)) {
      const id = `paint${ids.size}`;
      const units = { id, gradientUnits: 'userSpaceOnUse' };
      let gradient;
      const stops = [];
      if (mat.kind === 'radial') {
        gradient = element('radialGradient', {
          ...units, cx: 0, cy: 0, r: 1, gradientTransform: `translate(${mid[0]} ${mid[1]}) scale(${half[0]} ${half[1]})`,
        }, defs);
        for (let i = 0; i <= 48; i++) stops.push([i / 48, ...seeThrough(mat.top, mat.alpha * (1 - i / 48) ** mat.power, mat.over)]);
      } else {
        gradient = element('linearGradient', { ...units, x1: 0, y1: mid[1] - half[1], x2: 0, y2: mid[1] + half[1] }, defs);
        const low = linear(mat.bottom);
        const high = linear(mat.top);
        for (let i = 0; i <= 12; i++) {
          const colour = hex(low.map((v, c) => encode(mix(v, high[c], i / 12))));
          stops.push([i / 12, ...seeThrough(colour, mat.alpha, mat.over)]);
        }
      }
      for (const [offset, colour, opacity] of stops) {
        element('stop', { offset: offset.toFixed(4), 'stop-color': colour, 'stop-opacity': opacity.toFixed(4) }, gradient);
      }
      ids.set(key, id);
    }
    return { fill: `url(#${ids.get(key)})`, alpha: 1 };
  }

  /* Build the page's SVG once: a group for each depth layer, far to near,
     and in each group its shapes from back to front. */
  function mount(svg) {
    const defs = element('defs', {}, svg);
    const ids = new Map();
    for (const made of nodes) place(made, 0);
    const groups = new Map();
    for (const made of nodes) {
      if (made.kind === 'empty') continue;
      let root = made;
      while (root.parent) root = root.parent;
      if (!groups.has(root)) groups.set(root, []);
      groups.get(root).push(made);
    }
    const rest = (made) => {             // depth with every scale as it was made, not as a pop-in leaves it at time 0
      let z = made.z;
      let nest = 0;
      for (let up = made.parent; up; up = up.parent) {
        z = up.z + up.sz * z;
        nest += 1;
      }
      return [z, nest];
    };
    // Two shapes can come out at one depth, and then Blender's rounding says which is in front. In
    // this scene that is Pip's right arm and its body, and the arm, which is nested deeper, is in front.
    const behind = (a, b) => (Math.abs(a[0][0] - b[0][0]) > 1e-9 ? a[0][0] - b[0][0] : a[0][1] - b[0][1] || a[1].index - b[1].index);
    drawn = [];
    const roots = [...groups.keys()].sort((a, b) => a.z - b.z || a.index - b.index);
    for (const root of roots) {
      const group = element('g', {}, svg);
      const members = groups.get(root).map((made) => [rest(made), made]).sort(behind);
      const shapes = members.map(([, made]) => {
        const { fill, alpha } = made.kind === 'text' ? { fill: made.mat.top, alpha: made.mat.alpha } : paint(made, defs, ids);
        made.drawnAlpha = alpha;
        let el;
        if (made.kind === 'text') {
          el = element('text', {
            fill, 'font-family': made.face.family, 'font-weight': made.face.weight, 'font-size': 100, 'text-anchor': 'middle',
            y: 100 * made.face.drop,
          }, group);
          el.textContent = made.body;
        } else {
          let holder = group;
          if (made.inside) {
            const id = `inside${made.index}`;
            made.window = { made: made.inside, el: element('polygon', { points: points(made.inside) }, element('clipPath', { id }, defs)), was: {} };
            holder = element('g', { 'clip-path': `url(#${id})` }, group);
          }
          el = element('polygon', { fill, points: points(made) }, holder);
        }
        return { made, el, was: {} };
      });
      drawn.push({ root, group, shapes, blur: '' });
    }
  }

  const points = (made) => made.pts.map(([x, y]) => `${x.toFixed(4)},${y.toFixed(4)}`).join(' ');

  /* Where the camera at [cx, cy, cz] sees a shape, as an SVG transform. */
  function seen(made, cx, cy, cz) {
    const w = made.world;
    const k = UNIT * H0 / (cz - w.z);
    const grow = made.kind === 'text' ? made.size * made.face.scale / 100 : 1;
    const flip = made.kind === 'text' ? -grow : 1;
    const m = [k * w.m[0] * grow, -k * w.m[1] * grow, k * w.m[2] * flip, -k * w.m[3] * flip,
      WIDTH / 2 + k * (w.m[4] - cx), HEIGHT / 2 - k * (w.m[5] - cy)];
    return `matrix(${m.map((v) => v.toFixed(4)).join(' ')})`;
  }

  function set(shown, name, value) {
    if (shown.was[name] === value) return;
    shown.was[name] = value;
    shown.el.setAttribute(name, value);
  }

  /* Draw the scene as it is at time t. */
  function render(t) {
    const [cx, cy, cz] = view.path(t);
    for (const made of nodes) place(made, t);
    const focus = cz - view.focusZ;
    const spread = LENS * LENS / (view.fstop * (focus - LENS)) / SENSOR * WIDTH;
    for (const entry of drawn) {
      // The camera blurs a point into a disc; a Gaussian blur a quarter as wide spreads light as far.
      const far = cz - entry.root.world.z;
      const sigma = entry.root.sharp ? 0 : spread * Math.abs(far - focus) / far / 4;
      const filter = sigma >= 0.3 ? `blur(${sigma.toFixed(2)}px)` : '';
      if (filter !== entry.blur) {
        entry.group.style.filter = filter;
        entry.blur = filter;
      }
      for (const shown of entry.shapes) {
        const w = shown.made.world;
        const alpha = clamp(w.alpha) * shown.made.drawnAlpha;
        const k = UNIT * H0 / (cz - w.z);
        const size = Math.hypot(w.m[0], w.m[1]) * k;
        if (alpha <= 0.002 || size < 0.5) {     // faded out, or shrunk to less than a pixel
          set(shown, 'display', 'none');
          continue;
        }
        set(shown, 'display', 'inline');
        set(shown, 'opacity', alpha.toFixed(3));
        set(shown, 'transform', seen(shown.made, cx, cy, cz));
        if (shown.made.window) set(shown.made.window, 'transform', seen(shown.made.inside, cx, cy, cz));
      }
    }
  }

  return {
    ...palette, DEEP_BEHIND, SKY_BEHIND, H0, Random, Timing, Track, setup, state, laid,
    frames, fr, sec, every, within, clamp, smooth, easeOut, backOut, span, mix,
    material, glowMaterial, nextZ, empty, layer, shape, text, fade,
    circlePts, rrectPts, barPts, capsulePts, arcPts, starPts,
    backdrop, motes, camera, mount, render,
  };
})();

if (typeof module !== 'undefined') module.exports = kit;
