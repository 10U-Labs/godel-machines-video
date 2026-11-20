/* Scene 07: Improving through families.

A family of programs hangs down from one program at the top. One program,
then its children, then theirs, light up, and a soft boundary closes around
them all: a clade. Each clade is rated as a whole, and the best clade gets
more children. The best single program sits in a weak clade; the program
that starts the best family is picked instead. Last, the two machines stand
on columns as tall as their scores, beside clocks of the computer time they
used.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, alpha, every } = kit;

  const SIZE = 0.42;

  const TREE = [  // id, parent, place, score
    ['r', null, [0.0, 3.3], 22],
    ['a', 'r', [-5.0, 1.7], 26],
    ['b', 'r', [0.0, 1.7], 29],
    ['c', 'r', [5.0, 1.7], 44],
    ['a1', 'a', [-6.3, 0.1], 28],
    ['a2', 'a', [-3.7, 0.1], 25],
    ['b1', 'b', [-1.3, 0.1], 33],
    ['b2', 'b', [1.3, 0.1], 31],
    ['c1', 'c', [5.0, 0.1], 23],
    ['a3', 'a1', [-6.3, -1.5], 27],
    ['a4', 'a2', [-3.7, -1.5], 24],
    ['b3', 'b1', [-1.9, -1.5], 37],
    ['b4', 'b1', [-0.6, -1.5], 35],
    ['b5', 'b2', [0.7, -1.5], 36],
    ['b6', 'b2', [1.9, -1.5], 38],
    ['c2', 'c1', [5.0, -1.5], 21],
    ['b7', 'b3', [-1.9, -3.0], 40],
    ['b8', 'b6', [1.9, -3.0], 39],
    ['b9', 'b4', [-0.6, -3.0], 42],       // the best clade's new children
    ['b10', 'b5', [0.7, -3.0], 41],
  ];

  const CLADES = [  // name, centre, width, height, colour, rating (share of the meter)
    ['a', [-5.0, -0.1], 4.0, 4.4, kit.SKY, 0.45],
    ['b', [0.0, -0.55], 5.0, 5.3, kit.MINT, 0.9],
    ['c', [5.0, -0.1], 2.6, 4.4, kit.CORAL, 0.22],
  ];

  /* A clock face whose rim lights segment by segment from t0, one segment every rate seconds. */
  const clock = (name, parent, loc, lit, t0, rate, colour) => {
    const root = kit.empty(name, parent, [loc[0], loc[1], kit.nextZ(parent)]);
    kit.shape(`${name}-face`, kit.circlePts(0.72), kit.material(kit.INK700, kit.INK800), root);
    for (let i = 0; i < 24; i++) {
      const a = Math.PI / 2 - 2 * Math.PI * (i + 0.5) / 24;
      const at = [0.6 * Math.cos(a), 0.6 * Math.sin(a)];
      kit.shape(`${name}-slot${i}`, kit.rrectPts(0.07, 0.17, 0.03), kit.material(kit.INK500), root, at, { rot: a - Math.PI / 2 });
      if (i < lit) {
        const on = kit.shape(`${name}-seg${i}`, kit.rrectPts(0.08, 0.19, 0.03), kit.material(colour), root, at, { rot: a - Math.PI / 2 });
        const t = t0 + rate * i;
        alpha(on, 1, 0.0);
        alpha(on, fr(t), 0.0);
        alpha(on, fr(t) + 1, 1.0);
      }
    }
    const hand = kit.shape(`${name}-hand`, [[-0.03, 0], [0.03, 0], [0.02, 0.45], [-0.02, 0.45]], kit.material(kit.PAPER), root);
    kit.shape(`${name}-hub`, kit.circlePts(0.06), kit.material(kit.PAPER), root);
    for (const f of every(1, fr(t0), fr(t0 + rate * lit) + 1)) {
      const q = Math.min(lit, (sec(f) - t0) / rate) / 24;
      key(hand, 'rot', f, -2 * Math.PI * q);
    }
    return root;
  };

  kit.state.zstep = 0.0005;
  const cues = [];
  const end = sec(kit.frames());
  const tTree0 = 0.15;
  const tOne = T.at(1, 0.04);
  const tKids = T.at(1, 0.19);
  const tGrand = T.at(1, 0.31);
  const tDown = T.at(1, 0.43);
  const tClade = T.at(1, 0.56);
  const tName = T.at(1, 0.76);
  const tRate = T.start(2) + 0.2;
  const tMeters = T.at(2, 0.25);
  const tMore = T.at(2, 0.62);
  const tBest = T.start(3) + 0.3;
  const tStarts = T.at(3, 0.52);
  const tClear = T.start(4) - 0.35;
  const tCols = T.at(4, 0.08);
  const tClocks = T.at(4, 0.6);

  kit.backdrop(71, kit.VIOLET_DEEP);
  kit.motes(undefined, 72, kit.VIOLET);
  const lines = kit.layer('lines', 0.9);
  const hulls = kit.layer('hulls', 0.8);
  const stage = kit.layer('stage', 1.0);

  // ------------------------------------------------------------ the family, built quickly from the top
  const tNode = {};
  TREE.slice(0, 18).forEach(([n], k) => { tNode[n] = tTree0 + 0.12 * k; });
  [tNode.b9, tNode.b10] = [tMore + 0.45, tMore + 1.2];
  const nodes = TREE.map(([n, pa, at, sc], i) => ({ id: n, parent: pa, at, score: sc, t: tNode[n], tOut: tClear + 0.02 * i }));
  const fam = parts.family('fam', stage, lines, nodes, { size: SIZE });
  const places = Object.fromEntries(TREE.map(([n, , at]) => [n, at]));
  cues.push({ t: tTree0, type: 'rise', dur: 2.0, pitch: 0.9, gain: 0.4 });
  for (const n of ['r', 'a', 'b', 'c']) cues.push({ t: tNode[n], type: 'pop', pitch: 0.9 + 0.05 * cues.length, gain: 0.4 });

  // ------------------------------------------------------------ a program, its children, theirs, and so on down
  const lights = [[tOne, ['b']], [tKids, ['b1', 'b2']], [tGrand, ['b3', 'b4', 'b5', 'b6']], [tDown, ['b7', 'b8']]];
  lights.forEach(([t, ids], k) => {
    for (const n of ids) {
      const r = kit.ring(`${n}-light`, stage, places[n], 0.58, kit.MINT, 0.09, 0.02);
      for (const [f, a] of [[fr(t), 0.0], [fr(t + 0.2), 1.0], [fr(tClade + 0.3), 1.0], [fr(tClade + 0.9), 0.0]]) alpha(r, f, a);
    }
    cues.push({ t, type: 'blip', pitch: 1.0 + 0.12 * k, gain: 0.55 });
  });

  for (const [c, centre, w, h, colour] of CLADES) {
    const ob = kit.shape(`${c}-hull`, kit.rrectPts(w, h, 0.9), kit.material(colour, null, 0.16), hulls, centre);
    const tIn = c === 'b' ? tClade : tRate;
    alpha(ob, 1, 0.0);
    alpha(ob, fr(tIn), 0.0);
    alpha(ob, fr(tIn + 0.5), 1.0);
    alpha(ob, fr(tClear), 1.0);
    alpha(ob, fr(tClear + 0.4), 0.0);
    if (c === 'b') {                             // the best family lights up brighter
      const bright = kit.shape('b-hull-bright', kit.rrectPts(w, h, 0.9), kit.material(colour, null, 0.2), hulls, centre);
      kit.appear(bright, tStarts, tClear, 0.4);
    }
  }
  const best = CLADES[1][1];
  const word = kit.text('clade-word', 'clade', 0.4, kit.material(kit.MINT), stage, [best[0] + 1.9, best[1] + 2.95]);
  kit.appear(word, tClade + 0.2, tRate, 0.4);
  cues.push({ t: tClade, type: 'swoosh', gain: 0.5 });
  const title = kit.text('title', 'Huxley-Gödel Machine', 0.55, kit.material(kit.PAPER), stage, [0, -4.05]);
  kit.appear(title, tName, tRate - 0.3, 0.5);
  cues.push({ t: tName, type: 'chime', gain: 0.6 });

  // ------------------------------------------------------------ each clade gets a rating; the best grows
  CLADES.forEach(([c, centre, , , colour, share], k) => {
    const at = [centre[0] - 1.6, -4.15];
    const rail = kit.shape(`${c}-track`, kit.barPts(3.2, 0.22), kit.material(kit.INK600), stage, at);
    const fill = kit.shape(`${c}-fill`, kit.barPts(3.2, 0.22), kit.material(colour), stage, at);
    kit.appear(rail, tRate, tClear, 0.4);
    const t0 = tMeters + 0.25 * k;
    key(fill, 'scale', 1, [0.001, 1, 1]);
    key(fill, 'scale', fr(t0), [0.001, 1, 1]);
    key(fill, 'scale', fr(t0 + 0.9), [share, 1, 1]);
    kit.appear(fill, tRate, tClear, 0.4);
    cues.push({ t: t0, type: 'rise', dur: 0.9, pitch: 0.8 + share * 0.6, gain: 0.4 });
  });
  for (const n of ['b9', 'b10']) {
    const pa = TREE.find(([i]) => i === n)[1];
    const r = kit.ring(`${n}-pick`, stage, places[pa], 0.6, kit.AMBER, undefined, 0.02);
    kit.flash(r, tNode[n] - 0.45, 0.6);
    cues.push({ t: tNode[n], type: 'pop', pitch: 1.2, gain: 0.5 });
  }

  // ------------------------------------------------------------ not the best Pip, the Pip that starts the best family
  kit.pop(fam.c.tag.root, tBest, 1.3, 0.35, tStarts);
  const cRing = kit.ring('c-best', stage, places.c, 0.62, kit.AMBER, 0.1, 0.02);
  for (const [f, a] of [[fr(tBest), 0.0], [fr(tBest + 0.25), 1.0], [fr(tStarts - 0.2), 1.0], [fr(tStarts + 0.2), 0.0]]) alpha(cRing, f, a);
  cues.push({ t: tBest, type: 'pop', pitch: 1.3, gain: 0.6 });
  kit.pop(fam.b.tag.root, tStarts, 1.3, 0.35, tClear);
  const bRing = kit.ring('b-best', stage, places.b, 0.62, kit.MINT, 0.12, 0.02);
  for (const [f, a] of [[fr(tStarts), 0.0], [fr(tStarts + 0.25), 1.0], [fr(tClear - 0.1), 1.0], [fr(tClear + 0.2), 0.0]]) alpha(bRing, f, a);
  cues.push({ t: tStarts, type: 'chime', gain: 0.6 });
  for (const n of ['b', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10']) {
    kit.pipEyes(fam[n].pip, tStarts + 0.1, 1.12, 0.7);
  }
  kit.pipLook(fam.c.pip, tStarts, -0.1, -0.05);

  // ------------------------------------------------------------ the two machines: score and computer time
  cues.push({ t: tClear, type: 'whoosh', gain: 0.5 });
  const base = -3.0;
  const machines = [
    ['dgm', -3.4, 2.4, [kit.VIOLET, kit.VIOLET_DEEP], 'Darwin Gödel Machine', 24],
    ['hgm', 3.4, 3.4, [kit.MINT, kit.MINT_DEEP], 'Huxley-Gödel Machine', 10],
  ];
  machines.forEach(([name, x, height, [body, deep], label, lit], k) => {
    const col = kit.shape(`${name}-column`, [[0.75, 0], [0.75, 1], [-0.75, 1], [-0.75, 0]], kit.material(body, deep), stage, [x, base]);
    const p = kit.pip(`${name}-pip`, stage, [x, base + 0.95], 0.9, body, deep);
    kit.pipIdle(p, undefined, undefined, k * 1.7, 2);
    kit.pipBlink(p, [tCols + 2.0 + k * 0.6]);
    const z = p.root.z;
    const t0 = tCols + 0.35 * k;
    for (const f of every(1)) {
      const t = sec(f);
      const q = span(t, t0, t0 + 1.4, kit.easeOut);
      const h = 0.001 + height * q;
      key(col, 'scale', f, [1, h, 1]);
      key(p.root, 'loc', f, [x, base + h + 0.95, z]);
    }
    kit.pop(p.root, t0, 0.9);
    kit.appear(col, t0, null, 0.2);
    const lab = kit.text(`${name}-label`, label, 0.32, kit.material(kit.PAPER), stage, [x, base - 0.45]);
    kit.appear(lab, t0 + 0.2, null, 0.4);
    cues.push({ t: t0, type: 'rise', dur: 1.4, pitch: 0.8 + 0.25 * k, gain: 0.45 });
    clock(`${name}-clock`, stage, [x + 2.0, base + height * 0.5 + 0.3], lit, tClocks, 0.11, body);
  });
  for (let k = 0; k < 24; k += 3) cues.push({ t: tClocks + 0.11 * k, type: 'tick', pitch: 1.0, gain: 0.3 });
  cues.push({ t: tClocks + 0.11 * 10, type: 'chime', gain: 0.5, pitch: 1.2 });

  // ------------------------------------------------------------ camera
  const path = (t) => {
    let [x, y, h] = [0.0, 2.4, 13.5];
    const wide = span(t, 0.6, T.end(0));
    [x, y, h] = [mix(x, 0.0, wide), mix(y, -0.3, wide), mix(h, kit.H0 + 1.4, wide)];
    const near = span(t, tOne - 0.3, tOne + 1.2) * (1 - span(t, tRate - 0.6, tRate + 0.6));
    [x, y, h] = [mix(x, 0.0, near), mix(y, -0.4, near), mix(h, 17.0, near)];
    const last = span(t, tClear, tClear + 1.2);
    return [mix(x, 0.0, last), mix(y, 0.3, last), mix(h, kit.H0 - 0.5, last) - 0.3 * span(t, tClear, end)];
  };

  kit.camera(path, 1.0);
  return cues;
}
