/* The cast and props of the Gödel machines film, built from the shared kit.

Pip, the film's made-up program, and how it moves; a program drawn as a file
and as a page of code; a family of programs drawn as small Pips joined by
branches; and Pip's shape as a blueprint drawing.
*/
'use strict';

const parts = (() => {
  const {
    AMBER, AMBER_DEEP, CORAL, DEEP_BEHIND, INK500, INK600, INK700, INK800, INK900, MINT, MINT_DEEP, MIST, PAPER, SKY,
    SKY_BEHIND, VIOLET, Random, alpha, arcPts, barPts, branch, capsulePts, circlePts, empty, every, fr, frames,
    glowMaterial, grow, hold, key, laid, material, nextZ, pop, rrectPts, sec, shape, tag, text,
  } = kit;

  const radians = (deg) => deg * Math.PI / 180;

  // ---------------------------------------------------------------- Pip

  /* Pip: a small round program with a screen for a face, two arms, and an antenna.

     The origin is the middle of the body. Arms hang down at angle 0 and rotate
     about the shoulder; positive angles swing the right arm outward and up. */
  function pip(name, parent, loc = [0, 0], scale = 1.0, body = MINT, bodyDeep = MINT_DEEP) {
    const root = empty(name, parent, [loc[0], loc[1], nextZ(parent)], scale);
    const rig = empty(`${name}-rig`, root, [0, 0, 0]);          // bobbing and squash live here
    const halo = shape(`${name}-halo`, circlePts(2.0), glowMaterial(body, 0.3, 2.2), rig, [0, 0.1]);
    const arms = {};
    for (const side of [-1, 1]) {
      const shoulder = empty(`${name}-shoulder${side}`, rig, [side * 0.8, -0.18, nextZ(rig)]);
      shape(`${name}-arm${side}`, capsulePts(0.5, 0.22), material(body, bodyDeep), shoulder);
      shape(`${name}-hand${side}`, circlePts(0.15), material(body, bodyDeep), shoulder, [0, -0.52]);
      shoulder.rot = side * radians(18);
      arms[side < 0 ? 'left' : 'right'] = shoulder;
    }
    const antenna = empty(`${name}-antenna`, rig, [0, 0.72, nextZ(rig)]);
    shape(`${name}-stem`, capsulePts(0.34, 0.07), material(bodyDeep), antenna, [0, 0.34]);
    // The bulb's glow lies over the halo, a third of the way out from the halo's middle.
    const haloBehind = laid(body, 0.3 * (2 / 3) ** 2.2, kit.state.over || SKY_BEHIND);
    const bulbGlow = shape(`${name}-bulb-glow`, circlePts(0.45), glowMaterial(AMBER, 0.55, 1.6, haloBehind), antenna, [0, 0.38]);
    shape(`${name}-bulb`, circlePts(0.11), material('#fff2c4', AMBER), antenna, [0, 0.38]);
    shape(`${name}-body`, rrectPts(1.7, 1.5, 0.62), material(body, bodyDeep), rig);
    shape(`${name}-shine`, circlePts(0.2, null, 0.1), material(PAPER, null, 0.45, { over: body }), rig, [-0.48, 0.5], { rot: 0.5 });
    const screen = shape(`${name}-screen`, rrectPts(1.28, 0.86, 0.34), material(INK800, INK900), rig, [0, 0.06]);
    const face = empty(`${name}-face`, rig, [0, 0.06, nextZ(rig)]);
    const eyes = empty(`${name}-eyes`, face, [0, 0.08, nextZ(face)]);
    const eyeList = [];
    for (const side of [-1, 1]) {
      const e = empty(`${name}-eye${side}`, eyes, [side * 0.27, 0, nextZ(face)]);
      // The glow has the body's colour, so it shows on the dark screen and not on the body around it.
      shape(`${name}-eyeglow${side}`, circlePts(0.3), glowMaterial(body, 0.4, 1.6, DEEP_BEHIND), e, [0, 0], { inside: screen });
      shape(`${name}-eyeball${side}`, circlePts(0.12, null, 0.16), material('#d9fff5', body), e);
      shape(`${name}-spark${side}`, circlePts(0.035), material(PAPER), e, [0.04, 0.06]);
      eyeList.push(e);
    }
    const mouth = shape(`${name}-mouth`, arcPts(0.13, 0.05, 200, 340), material(body), face, [0, -0.1]);
    return { root, rig, halo, arms, eyes, eyeList, mouth, antenna, bulbGlow, face };
  }

  /* Bob gently, with a slight squash, and let the antenna sway. */
  function pipIdle(p, t0 = 0.0, t1 = null, phase = 0.0, step = 2) {
    const last = t1 === null ? sec(frames()) : t1;
    for (const f of every(step, fr(t0), fr(last))) {
      const t = sec(f) + phase;
      const b = Math.sin(t * 2.2);
      key(p.rig, 'loc', f, [0, 0.08 * b, 0]);
      key(p.rig, 'scale', f, [1 - 0.015 * b, 1 + 0.015 * b, 1]);
      key(p.antenna, 'rot', f, 0.12 * Math.sin(t * 2.2 - 0.9));
      alpha(p.bulbGlow, f, 0.8 + 0.2 * Math.sin(t * 3.1));
    }
  }

  function pipBlink(p, times) {
    for (const t of times) {
      const f = fr(t);
      for (const [df, s] of [[-3, 1.0], [0, 0.08], [3, 1.0]]) {
        for (const e of p.eyeList) key(e, 'scale', f + df, [1, s, 1]);
      }
    }
  }

  /* Glance: the eyes slide across the screen within dur seconds, ending at time t + dur. */
  function pipLook(p, t, dx, dy = 0.0, dur = 0.25) {
    const eyes = p.eyes;
    const z = eyes.z;
    hold(eyes, 'loc', fr(t));
    key(eyes, 'loc', fr(t + dur), [dx, 0.08 + dy, z]);
  }

  /* Swing an arm to deg (0 hangs down, 90 points sideways, 160 straight up) by t + dur. */
  function pipArm(p, side, t, deg, dur = 0.3) {
    const shoulder = p.arms[side];
    const s = side === 'right' ? 1 : -1;
    hold(shoulder, 'rot', fr(t));
    key(shoulder, 'rot', fr(t + dur), s * radians(deg));
  }

  function pipWave(p, t0, t1, rate = 7.0) {
    const shoulder = p.arms.right;
    hold(shoulder, 'rot', fr(t0));
    for (const f of every(2, fr(t0) + 4, fr(t1))) {
      key(shoulder, 'rot', f, radians(135 + 22 * Math.sin((sec(f) - t0) * rate)));
    }
    key(shoulder, 'rot', fr(t1 + 0.35), radians(18));
  }

  /* Widen (above 1) or narrow (below 1) both eyes by time t + dur. */
  function pipEyes(p, t, sx, sy, dur = 0.2) {
    for (const e of p.eyeList) {
      hold(e, 'scale', fr(t));
      key(e, 'scale', fr(t + dur), [sx, sy, 1]);
    }
  }

  // ---------------------------------------------------------------- programs

  const CODE = [MINT, VIOLET, SKY, AMBER, MIST];

  /* Pip's face in miniature, marking something as Pip's own. */
  function badge(name, parent, loc = [0, 0], scale = 1.0) {
    const icon = empty(name, parent, [loc[0], loc[1], nextZ(parent)], scale);
    shape(`${name}-glow`, circlePts(0.7), glowMaterial(MINT, 0.6), icon);
    shape(`${name}-body`, rrectPts(0.42, 0.36, 0.14), material(MINT, MINT_DEEP), icon);
    shape(`${name}-screen`, rrectPts(0.3, 0.2, 0.08), material(INK900), icon, [0, 0.01]);
    for (const side of [-1, 1]) {
      shape(`${name}-eye${side}`, circlePts(0.03, null, 0.04), material('#d9fff5'), icon, [side * 0.06, 0.02]);
    }
    return icon;
  }

  /* A file: a page with a folded corner and a few lines of text on it. */
  function fileIcon(name, parent, loc = [0, 0], scale = 1.0, mine = false, seed = 0) {
    const rnd = new Random(seed);
    const root = empty(name, parent, [loc[0], loc[1], nextZ(parent)], scale);
    const glow = shape(`${name}-glow`, rrectPts(1.9, 2.2, 0.8), glowMaterial(mine ? MINT : SKY, 0.5, 1.0), root);
    alpha(glow, 1, 0.0);
    shape(`${name}-page`, [[-0.5, 0.65], [0.22, 0.65], [0.5, 0.37], [0.5, -0.65], [-0.5, -0.65]], material(INK600, INK700), root);
    shape(`${name}-fold`, [[0.22, 0.65], [0.22, 0.37], [0.5, 0.37]], material(INK500), root);
    const page = laid(INK600, 0.5, INK700);
    for (let r = 0; r < 5; r++) {
      const ln = r ? 0.3 + rnd.random() * 0.4 : 0.35;
      shape(`${name}-line${r}`, barPts(ln, 0.07), material(MIST, null, 0.8, { over: page }), root, [-0.34, 0.38 - r * 0.2 - (r ? 0.08 : 0)]);
    }
    const icon = mine ? badge(`${name}-badge`, root, [0.12, -0.42], 0.9) : null;
    return { root, glow, badge: icon };
  }

  /* A program shown as a page of code: a window with a title bar and rows of coloured bars.

     Returns the root, the list of row bars, and, if mistake is a row number,
     the red bars on that row and the fixed bars that replace them. */
  function program(name, parent, loc = [0, 0], options = {}) {
    const { rows = 8, w = 3.6, h = 4.2, seed = 1, mistake = null, label = null, scale = 1.0, tabIcon = false } = options;
    const rnd = new Random(seed);
    const root = empty(name, parent, [loc[0], loc[1], nextZ(parent)], scale);
    shape(`${name}-shadow`, rrectPts(w + 0.5, h + 0.5, 0.5), glowMaterial(INK900, 0.7, 0.8), root, [0.15, -0.2]);
    shape(`${name}-page`, rrectPts(w, h, 0.22), material(INK700, INK800), root);
    shape(`${name}-bar`, rrectPts(w, 0.6, 0.22).map(([x, y]) => [x, y + h / 2 - 0.3]), material(INK600), root);
    shape(`${name}-bar-fill`, rrectPts(w, 0.3, 0).map(([x, y]) => [x, y + h / 2 - 0.45]), material(INK600), root);
    [CORAL, AMBER, MINT].forEach((c, i) => {
      shape(`${name}-dot${i}`, circlePts(0.08), material(c), root, [-w / 2 + 0.3 + i * 0.25, h / 2 - 0.3]);
    });
    const icon = tabIcon ? badge(`${name}-icon`, root, [w / 2 - 0.45, h / 2 - 0.3]) : null;
    if (label) text(`${name}-label`, label, 0.2, material(MIST), root, [0, h / 2 - 0.3], { face: 'JetBrainsMono' });
    const bars = [];
    let bad = null;
    let good = null;
    const top = h / 2 - 0.95;
    const gap = (h - 1.4) / rows;
    for (let r = 0; r < rows; r++) {
      const indent = r ? [0, 1, 1, 2, 2, 1, 0][rnd.randrange(7)] : 0;
      const x0 = -w / 2 + 0.35 + indent * 0.35;
      let x = x0;
      const y = top - r * gap;
      let left = w - 0.7 - indent * 0.35;
      const words = [];
      while (left > 0.35) {
        const ln = Math.min(left, 0.35 + rnd.random() * 1.0);
        words.push(ln);
        left -= ln + 0.15;
        if (rnd.random() < 0.3) break;
      }
      const row = [];
      words.forEach((ln, j) => {
        let col = CODE[rnd.randrange(CODE.length)];
        if (r === mistake) col = CORAL;
        row.push(shape(`${name}-r${r}w${j}`, barPts(ln, 0.14), material(col), root, [x, y]));
        if (r === mistake) {
          const fix = shape(`${name}-r${r}w${j}-fixed`, barPts(ln, 0.14), material(MINT), root, [x, y]);
          alpha(fix, 1, 0.0);
          good = (good || []).concat([fix]);
        }
        x += ln + 0.15;
      });
      if (r === mistake) {
        const spanW = x - 0.15 - x0;
        const ring = shape(`${name}-ring`, rrectPts(spanW + 0.3, 0.42, 0.21), material(CORAL, null, 0.25, { over: INK700 }), root,
          [x0 + spanW / 2, y], { lift: -0.0015 });
        alpha(ring, 1, 0.0);
        bad = { bars: row, ring, y, x: x0 + spanW / 2 };
      }
      bars.push(row);
    }
    return { root, rows: bars, bad, good, icon };
  }

  // ---------------------------------------------------------------- families of programs

  const SCORE_COLOURS = [[18, ['#5aa59b', '#3c7a73']], [24, [MINT, MINT_DEEP]], [32, ['#9af7d8', MINT]], [40, [AMBER, AMBER_DEEP]]];

  /* Pip's colours for a program with a score: dull for low scores, warm for high ones. */
  function scoreColour(score) {
    let out = SCORE_COLOURS[0][1];
    for (const [floor, c] of SCORE_COLOURS) {
      if (score >= floor) out = c;
    }
    return out;
  }

  /* A family of programs drawn as small Pips joined by branches.

     nodes is a list of objects with id, parent (an id, or null), at ([x, y]), t
     (when it pops in), and optionally score, colour ([body, deep]), and
     tOut. Branches go in the lines layer, which sits just behind the stage.
     options.known maps ids of parents drawn elsewhere to their places.
     Returns id -> { pip, line, at, tag }. */
  function family(name, stage, lines, nodes, options = {}) {
    const { size = 0.45, lineColour = MIST, idleStep = 3, known = null } = options;
    const rnd = new Random(nodes.length);
    const out = {};
    for (const n of nodes) {
      const at = n.at;
      const tOut = n.tOut === undefined ? null : n.tOut;
      const [body, deep] = n.colour || scoreColour(n.score === undefined ? 24 : n.score);
      let line = null;
      if (n.parent !== null && n.parent !== undefined) {
        const pa = n.parent in out ? out[n.parent].at : known[n.parent];
        line = branch(`${name}-${n.id}-line`, lines, pa, at, lineColour);
        grow(line, n.t - 0.3, 0.3, tOut);
      }
      const p = pip(`${name}-${n.id}`, stage, at, size, body, deep);
      alpha(p.halo, 1, 0.35);
      pop(p.root, n.t, size, undefined, tOut);
      pipIdle(p, undefined, undefined, rnd.random() * 6, idleStep);
      let tg = null;
      if (n.score !== undefined) {
        tg = tag(`${name}-${n.id}-tag`, stage, [at[0] + 0.8 * size / 0.45, at[1] + 0.3 * size / 0.45], String(n.score),
          n.score >= 40 ? AMBER : PAPER);
      }
      out[n.id] = { pip: p, line, at, tag: tg };
    }
    return out;
  }

  /* Points along the lines of Pip's shape (body, screen, eyes, antenna, arms), for a blueprint drawing. */
  function machineOutline(step = 0.16) {
    const sample = (pts, closed = true) => {
      const out = [];
      const loop = closed ? pts.concat([pts[0]]) : pts;
      for (let i = 0; i + 1 < loop.length; i++) {
        const [x0, y0] = loop[i];
        const [x1, y1] = loop[i + 1];
        const n = Math.max(1, Math.trunc(Math.hypot(x1 - x0, y1 - y0) / step));
        for (let j = 0; j < n; j++) out.push([x0 + (x1 - x0) * j / n, y0 + (y1 - y0) * j / n]);
      }
      return out;
    };
    const body = sample(rrectPts(1.7, 1.5, 0.62));
    const screen = sample(rrectPts(1.28, 0.86, 0.34)).map(([x, y]) => [x, y + 0.06]);
    const eyes = [-0.27, 0.27].flatMap((dx) => sample(circlePts(0.14, null, 0.17, 24)).map(([x, y]) => [x + dx, y + 0.14]));
    const antenna = sample([[0, 0.75], [0, 1.1]], false).concat(sample(circlePts(0.11, null, null, 16)).map(([x, y]) => [x, y + 1.13]));
    const arms = [-1, 1].flatMap((s) => [0, 1, 2, 3, 4, 5, 6].map((i) => [s * 0.85 + s * 0.15 * i / 6, -0.2 - 0.5 * i / 6]));
    return [...body, ...screen, ...eyes, ...antenna, ...arms];
  }

  return {
    pip, pipIdle, pipBlink, pipLook, pipArm, pipWave, pipEyes,
    badge, fileIcon, program, scoreColour, family, machineOutline,
  };
})();

if (typeof module !== 'undefined') module.exports = parts;
