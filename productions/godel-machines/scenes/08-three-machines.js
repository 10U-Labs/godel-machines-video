/* Scene 08: Three machines.

Three small pictures stand side by side, one for each machine, and the camera
visits each in turn: one program rewriting itself; a family growing child by
child; a family hanging down from one program, where the best branch grows.
Then a line of Pips climbs a stair, each new version a little better than the
last, and the trail goes on up into the dark.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, hold, alpha, every } = kit;

  const [LEFT, MID, RIGHT] = [[-5.4, 0.2], [0.0, 0.2], [5.4, 0.2]];
  const SIZE = 0.34;

  const DARWIN = [  // id, parent, place (relative to the middle picture), score
    ['d0', null, [-1.6, -1.7], 20],
    ['d1', 'd0', [-0.3, -0.9], 25],
    ['d2', 'd0', [-1.7, -0.3], 19],
    ['d3', 'd1', [0.9, -0.2], 30],
    ['d4', 'd1', [-0.4, 0.5], 27],
    ['d5', 'd3', [1.6, 0.9], 36],
    ['d6', 'd2', [-1.6, 1.1], 24],
    ['d7', 'd5', [0.6, 1.8], 41],
  ];

  const HUXLEY = [  // id, parent, place (relative to the right picture), score
    ['h0', null, [0.0, 1.8], 22],
    ['h1', 'h0', [-1.2, 0.6], 30],
    ['h2', 'h0', [1.2, 0.6], 34],
    ['h3', 'h1', [-1.8, -0.6], 33],
    ['h4', 'h1', [-0.6, -0.6], 35],
    ['h5', 'h2', [1.2, -0.6], 24],
    ['h6', 'h3', [-1.8, -1.8], 40],      // the best branch grows
    ['h7', 'h4', [-0.6, -1.8], 42],
  ];

  const STAIR = [[-5.6, -2.7, 0.6, 20], [-3.0, -1.75, 0.7, 26], [-0.4, -0.8, 0.8, 33], [2.2, 0.15, 0.9, 40], [4.8, 1.1, 1.0, 47]];

  kit.state.zstep = 0.0005;
  const cues = [];
  const end = sec(kit.frames());
  const tShow = [T.at(0, 0.3), T.at(0, 0.5), T.at(0, 0.7)];
  const [tG, tD, tH] = [T.start(1), T.start(2), T.start(3)];
  const tAway = T.start(4) - 0.4;
  const [tStair0, tStair1] = [T.at(4, 0.05), T.at(4, 0.8)];
  const tFar = T.start(5);

  kit.backdrop(81, kit.VIOLET_DEEP);
  kit.motes(undefined, 82, kit.MINT);
  const lines = kit.layer('lines', 0.9);
  const stage = kit.layer('stage', 1.0);

  const picture = (name, at, tIn, k) => {
    const root = kit.empty(name, stage, [at[0], at[1], kit.nextZ(stage)]);
    const lineRoot = kit.empty(`${name}-lines`, lines, [at[0], at[1], 0.0]);
    for (const ob of [root, lineRoot]) kit.pop(ob, tIn, 1.0, 0.5, tAway + 0.12 * k);
    return [root, lineRoot];
  };

  const names = ['Gödel Machine', 'Darwin Gödel Machine', 'Huxley-Gödel Machine'];
  [[LEFT, tG], [MID, tD], [RIGHT, tH]].forEach(([at, tLine], k) => {
    const lab = kit.text(`name${k}`, names[k], 0.3, kit.material(kit.PAPER), stage, [at[0], -3.35]);
    alpha(lab, 1, 0.0);
    for (const [f, a] of [[fr(tShow[k] + 0.2), 0.0], [fr(tShow[k] + 0.6), 0.5], [fr(tLine), 0.5], [fr(tLine + 0.4), 1.0],
      [fr(tLine + 0.4) + 1, 1.0], [fr(tAway), 1.0], [fr(tAway + 0.3), 0.0]]) {
      alpha(lab, f, a);
    }
    cues.push({ t: tShow[k], type: 'pop', pitch: 0.9 + 0.15 * k, gain: 0.6 });
  });

  // ------------------------------------------------------------ the Gödel Machine: one program rewriting itself
  const [gRoot] = picture('godel', LEFT, tShow[0], 0);
  const g = kit.pip('godel-pip', gRoot, [0, 0], 1.0, kit.SKY, kit.SKY_DEEP);
  kit.pipIdle(g);
  kit.pipBlink(g, [3.0, tG + 2.6, 14.0, 21.0]);
  const loop = kit.empty('godel-loop', gRoot, [0, 0, kit.nextZ(gRoot)]);
  kit.shape('godel-arc', kit.arcPts(1.65, 0.09, 120, 400, 48), kit.material(kit.SKY, null, 0.75), loop);
  const tipA = 400 * Math.PI / 180;
  const tip = [1.65 * Math.cos(tipA), 1.65 * Math.sin(tipA)];
  const [c, s] = [Math.cos(tipA + Math.PI / 2), Math.sin(tipA + Math.PI / 2)];
  kit.shape('godel-head', [[0.2, 0], [-0.14, 0.17], [-0.14, -0.17]].map(([x, y]) => [tip[0] + x * c - y * s, tip[1] + x * s + y * c]),
    kit.material(kit.SKY, null, 0.75), loop);
  let angle = 0.0;
  for (const f of every(1)) {
    const t = sec(f);
    const speed = 0.6 + 2.4 * span(t, tG, tG + 0.6) * (1 - span(t, tD - 0.5, tD + 0.5));
    angle += speed / kit.state.fps;
    key(loop, 'rot', f, angle);
  }
  const changes = [T.at(1, 0.3), T.at(1, 0.55), T.at(1, 0.8)];
  changes.forEach((t0, k) => {
    const ripple = kit.ring(`godel-ripple${k}`, gRoot, [0, 0], 1.2, kit.SKY, 0.1, 0.02);
    kit.flash(ripple, t0, 0.7, 1.2);
    cues.push({ t: t0, type: 'rise', dur: 0.4, pitch: 1.0 + 0.15 * k, gain: 0.5 });
  });
  const a = g.antenna;
  hold(a, 'scale', fr(changes[0]));
  key(a, 'scale', fr(changes[0]) + 5, [1.15, 1.45, 1]);
  for (const e of g.eyeList) {
    hold(e, 'scale', fr(changes[1]));
    key(e, 'scale', fr(changes[1]) + 5, [1.25, 1.25, 1]);
  }
  for (const side of ['left', 'right']) {
    const sh = g.arms[side];
    hold(sh, 'scale', fr(changes[2]));
    key(sh, 'scale', fr(changes[2]) + 5, [1.2, 1.3, 1]);
  }

  // ------------------------------------------------------------ the Darwin Gödel Machine: improving through children
  const [dRoot, dLines] = picture('darwin', MID, tShow[1], 1);
  const tDNode = { d0: tShow[1] + 0.1, d1: tShow[1] + 0.5 };
  const later = DARWIN.slice(2).map(([n]) => n);
  later.forEach((n, k) => { tDNode[n] = mix(T.at(2, 0.12), T.at(2, 0.9), k / (later.length - 1)); });
  const dfam = parts.family('darwin-fam', dRoot, dLines,
    DARWIN.map(([n, pa, at, sc]) => ({ id: n, parent: pa, at, score: sc, t: tDNode[n] })), { size: SIZE });
  for (const [n, pa, , sc] of DARWIN.slice(2)) {
    const r = kit.ring(`${n}-pick`, dRoot, dfam[pa].at, 0.5, kit.AMBER, undefined, 0.02);
    kit.flash(r, tDNode[n] - 0.4, 0.55);
    cues.push({ t: tDNode[n], type: 'pop', pitch: 0.9 + sc / 60, gain: 0.45 });
  }

  // ------------------------------------------------------------ the Huxley-Gödel Machine: improving through families
  const [hRoot, hLines] = picture('huxley', RIGHT, tShow[2], 2);
  const tHNode = {};
  HUXLEY.slice(0, 6).forEach(([n], k) => { tHNode[n] = tShow[2] + 0.1 + 0.1 * k; });
  [tHNode.h6, tHNode.h7] = [T.at(3, 0.62), T.at(3, 0.78)];
  const hfam = parts.family('huxley-fam', hRoot, hLines,
    HUXLEY.map(([n, pa, at, sc]) => ({ id: n, parent: pa, at, score: sc, t: tHNode[n] })), { size: SIZE });
  for (const [name, centre, w, h, colour, tIn] of [['best', [-1.2, -0.6], 2.7, 3.7, kit.MINT, T.at(3, 0.3)],
    ['weak', [1.2, 0.0], 1.4, 2.4, kit.CORAL, T.at(3, 0.38)]]) {
    const hull = kit.shape(`huxley-${name}`, kit.rrectPts(w, h, 0.6), kit.material(colour, null, 0.18), hLines, centre);
    kit.appear(hull, tIn, null, 0.5);
    cues.push({ t: tIn, type: 'swoosh', gain: 0.35 });
  }
  for (const n of ['h6', 'h7']) {
    const pa = HUXLEY.find(([i]) => i === n)[1];
    const r = kit.ring(`${n}-pick`, hRoot, hfam[pa].at, 0.5, kit.AMBER, undefined, 0.02);
    kit.flash(r, tHNode[n] - 0.4, 0.55);
    cues.push({ t: tHNode[n], type: 'pop', pitch: 1.2, gain: 0.5 });
  }
  cues.push({ t: tAway, type: 'whoosh', gain: 0.5 });

  // ------------------------------------------------------------ today: each new version better than the last
  const pips = [];
  STAIR.forEach(([x, y, size, score], k) => {
    const t0 = mix(tStair0, tStair1, k / (STAIR.length - 1));
    const step = kit.shape(`stair${k}`, kit.rrectPts(2.0, 0.16, 0.08), kit.material(kit.INK500), stage, [x, y - 1.05 * size]);
    kit.appear(step, t0 - 0.3, null, 0.3);
    const p = kit.pip(`version${k}`, stage, [x, y], size, ...parts.scoreColour(score));
    kit.pop(p.root, t0, size);
    kit.pipIdle(p, t0, undefined, k * 1.3, 2);
    alpha(p.halo, 1, 0.4 + 0.15 * k);
    pips.push([p, t0]);
    cues.push({ t: t0, type: 'pop', pitch: 0.9 + 0.12 * k, gain: 0.55 });
  });
  for (let k = 1; k < pips.length; k++) {
    const [prev, t0] = [pips[k - 1][0], pips[k][1]];
    kit.pipLook(prev, t0 - 0.5, 0.12, 0.06);
    const spark = kit.shape(`spark${k}`, kit.starPts(0.22, 0.07), kit.material('#fff3cf'), stage, [0, 0], { lift: 0.3 });
    const sg = kit.shape(`spark${k}-glow`, kit.circlePts(0.6), kit.glowMaterial(kit.AMBER, 0.8), stage, [0, 0], { lift: 0.29 });
    const [[x0, y0], [x1, y1]] = [STAIR[k - 1], STAIR[k]];
    for (const ob of [spark, sg]) {
      const z = ob.z;
      alpha(ob, 1, 0.0);
      for (const f of every(1, fr(t0 - 0.5), fr(t0 + 0.05))) {
        const q = span(sec(f), t0 - 0.45, t0, (v) => v);
        key(ob, 'loc', f, [mix(x0, x1, q), mix(y0, y1, q) + 0.8 * Math.sin(Math.PI * q), z]);
        alpha(ob, f, q > 0 && q < 1 ? 1.0 : 0.0);
      }
    }
  }
  const last = pips[pips.length - 1][0];
  kit.pipLook(last, tFar, 0.06, 0.12, 0.4);
  kit.pipArm(last, 'right', tFar + 0.3, 110, 0.4);

  // the trail goes on up, into the dark
  const [lx, ly] = STAIR[STAIR.length - 1];
  for (let k = 0; k < 18; k++) {
    const q = k / 17;
    const dot = kit.shape(`trail${k}`, kit.circlePts(0.08 - 0.03 * q, null, null, 12), kit.material(kit.AMBER, null, 1 - 0.8 * q), stage,
      [lx + 1.2 + 2.4 * q, ly + 1.6 + 5.0 * q ** 0.9]);
    kit.appear(dot, tFar + 0.1 + 0.08 * k, null, 0.3);
  }
  cues.push({ t: tFar + 0.1, type: 'rise', dur: 1.6, pitch: 1.1, gain: 0.45 });

  kit.veil(end - 1.0, 0.9);

  // ------------------------------------------------------------ camera
  const path = (t) => {
    let [x, y, h] = [0.0, 0.0, kit.H0 + 0.6];
    for (const [t0, [px, py]] of [[tG - 0.4, LEFT], [tD - 0.4, MID], [tH - 0.4, RIGHT]]) {
      const q = span(t, t0, t0 + 1.1);
      [x, y, h] = [mix(x, px, q), mix(y, py, q), mix(h, 13.5, q)];
    }
    let q = span(t, tAway - 0.2, tAway + 1.2);
    [x, y, h] = [mix(x, 0.0, q), mix(y, 0.0, q), mix(h, kit.H0, q)];
    q = span(t, tFar - 0.3, end);
    return [mix(x, 1.6, q), mix(y, 2.4, q), mix(h, kit.H0 + 0.8, q)];
  };

  kit.camera(path, 1.0);
  return cues;
}
