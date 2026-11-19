/* The cast and props of the Gödel machines film that its first scene needs,
   built from the trial's kit as productions/godel-machines/parts.py builds them
   from the Blender kit: Pip and how it moves, and a program drawn as a page of code. */
'use strict';

const parts = (() => {
  const {
    AMBER, CORAL, INK600, INK700, INK800, INK900, MINT, MINT_DEEP, MIST, PAPER, SKY, VIOLET,
    Random, Track, arcPts, barPts, capsulePts, circlePts, empty, every, fr, frames, glowMaterial,
    material, nextZ, rrectPts, sec, shape, within,
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
      shoulder.turn = new Track(shoulder.rot);
      arms[side < 0 ? 'left' : 'right'] = shoulder;
    }
    const antenna = empty(`${name}-antenna`, rig, [0, 0.72, nextZ(rig)]);
    shape(`${name}-stem`, capsulePts(0.34, 0.07), material(bodyDeep), antenna, [0, 0.34]);
    const bulbGlow = shape(`${name}-bulb-glow`, circlePts(0.45), glowMaterial(AMBER, 0.55), antenna, [0, 0.38]);
    shape(`${name}-bulb`, circlePts(0.11), material('#fff2c4', AMBER), antenna, [0, 0.38]);
    shape(`${name}-body`, rrectPts(1.7, 1.5, 0.62), material(body, bodyDeep), rig);
    shape(`${name}-shine`, circlePts(0.2, null, 0.1), material(PAPER, null, 0.45, body), rig, [-0.48, 0.5], { rot: 0.5 });
    shape(`${name}-screen`, rrectPts(1.28, 0.86, 0.34), material(INK800, INK900), rig, [0, 0.06]);
    const face = empty(`${name}-face`, rig, [0, 0.06, nextZ(rig)]);
    const eyes = empty(`${name}-eyes`, face, [0, 0.08, nextZ(face)]);
    const eyeList = [];
    for (const side of [-1, 1]) {
      const e = empty(`${name}-eye${side}`, eyes, [side * 0.27, 0, nextZ(face)]);
      shape(`${name}-eyeglow${side}`, circlePts(0.3), glowMaterial(body, 0.4), e);
      shape(`${name}-eyeball${side}`, circlePts(0.12, null, 0.16), material('#d9fff5', body), e);
      shape(`${name}-spark${side}`, circlePts(0.035), material(PAPER), e, [0.04, 0.06]);
      eyeList.push(e);
    }
    const mouth = shape(`${name}-mouth`, arcPts(0.13, 0.05, 200, 340), material(body), face, [0, -0.1]);
    // The curves that Blender keys on a few frames: where the eyes look, and how wide they are.
    const gaze = new Track([0, 0.08]);
    const lids = new Track([1, 1, 1]);
    return { root, rig, halo, arms, eyes, eyeList, mouth, antenna, bulbGlow, face, gaze, lids };
  }

  /* Bob gently, with a slight squash, and let the antenna sway. */
  function pipIdle(p, t0 = 0.0, t1 = null, phase = 0.0) {
    const f0 = fr(t0);
    const f1 = fr(t1 === null ? sec(frames()) : t1);
    const at = (t) => within(t, f0, f1) + phase;
    p.rig.move.loc = (t) => [0, 0.08 * Math.sin(at(t) * 2.2)];
    p.rig.move.scale = (t) => {
      const b = Math.sin(at(t) * 2.2);
      return [1 - 0.015 * b, 1 + 0.015 * b, 1];
    };
    p.antenna.move.rot = (t) => 0.12 * Math.sin(at(t) * 2.2 - 0.9);
    p.bulbGlow.move.alpha = (t) => 0.8 + 0.2 * Math.sin(at(t) * 3.1);
  }

  function pipBlink(p, times) {
    for (const t of times) {
      const f = fr(t);
      for (const [df, s] of [[-3, 1.0], [0, 0.08], [3, 1.0]]) p.lids.keyFrame(f + df, [1, s, 1]);
    }
    for (const e of p.eyeList) e.move.scale = p.lids;
  }

  /* Glance: the eyes slide across the screen within dur seconds, ending at time t + dur. */
  function pipLook(p, t, dx, dy = 0.0, dur = 0.25) {
    p.gaze.insert(t).key(t + dur, [dx, 0.08 + dy]);
    p.eyes.move.loc = p.gaze;
  }

  /* Swing an arm to deg (0 hangs down, 90 points sideways, 160 straight up) by t + dur. */
  function pipArm(p, side, t, deg, dur = 0.3) {
    const shoulder = p.arms[side];
    shoulder.turn.insert(t).key(t + dur, (side === 'right' ? 1 : -1) * radians(deg));
    shoulder.move.rot = shoulder.turn;
  }

  function pipWave(p, t0, t1, rate = 7.0) {
    const shoulder = p.arms.right;
    shoulder.turn.insert(t0);
    for (const f of every(2, fr(t0) + 4, fr(t1))) {
      shoulder.turn.keyFrame(f, radians(135 + 22 * Math.sin((sec(f) - t0) * rate)));
    }
    shoulder.turn.key(t1 + 0.35, radians(18));
    shoulder.move.rot = shoulder.turn;
  }

  /* Widen (above 1) or narrow (below 1) both eyes by time t + dur. */
  function pipEyes(p, t, sx, sy, dur = 0.2) {
    p.lids.insert(t).key(t + dur, [sx, sy, 1]);
    for (const e of p.eyeList) e.move.scale = p.lids;
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

  /* A program shown as a page of code: a window with a title bar and rows of coloured bars.

     Returns the root, the list of row bars, and, if mistake is a row number,
     the red bars on that row and the fixed bars that replace them. */
  function program(name, parent, loc = [0, 0], options = {}) {
    const { rows = 8, w = 3.6, h = 4.2, seed = 1, mistake = null, scale = 1.0, tabIcon = false } = options;
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
        const col = r === mistake ? (rnd.randrange(CODE.length), CORAL) : CODE[rnd.randrange(CODE.length)];
        row.push(shape(`${name}-r${r}w${j}`, barPts(ln, 0.14), material(col), root, [x, y]));
        if (r === mistake) {
          const fix = shape(`${name}-r${r}w${j}-fixed`, barPts(ln, 0.14), material(MINT), root, [x, y]);
          fix.alpha = 0.0;
          fix.shown = new Track(0.0).keyFrame(1, 0.0);
          good = (good || []).concat([fix]);
        }
        x += ln + 0.15;
      });
      if (r === mistake) {
        const spanW = x - 0.15 - x0;
        const ring = shape(`${name}-ring`, rrectPts(spanW + 0.3, 0.42, 0.21), material(CORAL, null, 0.25, INK700), root,
          [x0 + spanW / 2, y], { lift: -0.0015 });
        ring.alpha = 0.0;
        bad = { bars: row, ring, y, x: x0 + spanW / 2 };
      }
      bars.push(row);
    }
    return { root, rows: bars, bad, good, icon };
  }

  return { pip, pipIdle, pipBlink, pipLook, pipArm, pipWave, pipEyes, badge, program };
})();

if (typeof module !== 'undefined') module.exports = parts;
