/* Scene 04: Improving through children.

The Gödel Machine's blueprint fades, unbuilt. A team of researchers gathers
at a screen, and a machine appears on it: the Darwin Gödel Machine. Pip does
not change in place; it writes a changed copy of its code, and the copy
becomes its child. The child solves problems and gets a score. Parents are
picked, mostly the ones with high scores, and a family grows generation by
generation. An old program from early on becomes a parent again.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, hold, alpha, every } = kit;
  const radians = (deg) => deg * Math.PI / 180;

  const [SHEET_W, SHEET_H] = [6.4, 4.6];
  const SCREEN_AT = [1.2, 0.6];
  const PIP_AT = [-4.4, 0.2];
  const CODE_AT = [-0.6, 0.3];
  const CHILD_AT = [3.8, 0.2];
  const SIZE = 0.45;

  // The family: id, parent, place, score. Higher scores have more children.
  const TREE = [
    ['n0', null, [-6.5, -0.2], 20],
    ['n1', 'n0', [-4.4, 0.9], 23],
    ['n2', 'n0', [-4.4, -1.4], 18],
    ['n3', 'n1', [-2.3, 1.8], 27],
    ['n4', 'n1', [-2.3, 0.3], 25],
    ['n5', 'n3', [-0.2, 2.6], 31],
    ['n6', 'n3', [-0.2, 1.4], 29],
    ['n7', 'n4', [-0.2, 0.0], 24],
    ['n8', 'n5', [1.9, 3.1], 36],
    ['n9', 'n5', [1.9, 2.0], 33],
    ['n10', 'n6', [1.9, 0.9], 30],
    ['n11', 'n8', [4.0, 3.4], 41],
    ['n12', 'n8', [4.0, 2.4], 38],
    ['n13', 'n9', [4.0, 1.4], 35],
    ['n14', 'n11', [6.1, 3.2], 47],
    ['n15', 'n11', [6.1, 2.2], 44],
    ['n16', 'n2', [-2.3, -1.9], 26],
    ['n17', 'n7', [1.9, -0.4], 32],
  ];

  kit.state.zstep = 0.0005;
  const cues = [];
  const end = sec(kit.frames());
  const tDim = T.at(0, 0.1);
  const t2025 = T.at(0, 0.22);
  const tTeam = T.at(0, 0.28);
  const tBuilt = T.at(0, 0.47);
  const tName = T.at(0, 0.78);
  const tOut0 = T.start(1) - 0.4;
  const tPip = T.start(1) + 0.05;
  const tPlace = T.at(1, 0.08);
  const tCode = T.at(1, 0.38);
  const tCopy = T.at(1, 0.5);
  const tChange = T.at(1, 0.64);
  const tChild = T.at(1, 0.82);
  const tTests = T.start(2) + 0.2;
  const tScore = T.at(2, 0.4);
  const tMove = T.at(2, 0.55);
  const tAgain = T.at(2, 0.86);
  const [tGrow0, tGrow1] = [T.at(3, 0.04), T.at(3, 0.92)];
  const tOld = T.at(4, 0.3);

  kit.backdrop(41, kit.MINT_DEEP);
  kit.motes(undefined, 42, kit.MINT);
  const lines = kit.layer('lines', 0.9);
  const stage = kit.layer('stage', 1.0);

  // ------------------------------------------------------------ the blueprint, never built
  const sheet = kit.empty('sheet', stage, [0, 0.3, kit.nextZ(stage)]);
  const paper = kit.shape('sheet-paper', kit.rrectPts(SHEET_W, SHEET_H, 0.15), kit.material('#1d3f8f', '#16307a'), sheet);
  const gridMat = kit.material(kit.SKY, null, 0.18, { over: kit.laid('#1d3f8f', 0.5, '#16307a') });
  const drawn = [paper];
  for (let i = 1; i < 12; i++) {
    drawn.push(kit.shape(`grid-v${i}`, kit.rrectPts(0.025, SHEET_H - 0.3, 0), gridMat, sheet, [-SHEET_W / 2 + i * SHEET_W / 12, 0]));
  }
  for (let i = 1; i < 9; i++) {
    drawn.push(kit.shape(`grid-h${i}`, kit.rrectPts(SHEET_W - 0.3, 0.025, 0), gridMat, sheet, [0, -SHEET_H / 2 + i * SHEET_H / 9]));
  }
  parts.machineOutline().forEach(([x, y], k) => {
    drawn.push(kit.shape(`dash${k}`, kit.circlePts(0.04, null, null, 10), kit.material('#cfe9ff'), sheet, [x * 1.4, y * 1.4 - 0.1]));
  });
  for (const ob of drawn) {
    alpha(ob, 1, 1.0);
    alpha(ob, fr(tDim), 1.0);
    alpha(ob, fr(tDim + 0.8), 0.35);
  }
  const zs = sheet.z;
  for (const f of every(1, 1, fr(tTeam + 0.4))) {
    const t = sec(f);
    const q = span(t, t2025 - 0.2, tTeam + 0.4);
    key(sheet, 'loc', f, [mix(0.0, -10.5, q), 0.3 - 0.4 * q, zs]);
    key(sheet, 'rot', f, 0.02 * Math.sin(t * 0.7) + 0.25 * q);
  }
  cues.push({ t: t2025 - 0.2, type: 'whoosh', gain: 0.5 });

  // ------------------------------------------------------------ the team and their screen
  const floor = kit.shape('floor', kit.rrectPts(30, 0.06, 0), kit.material(kit.MIST, null, 0.2), stage, [0, -2.35]);
  kit.appear(floor, tTeam, tOut0, 0.5);
  const screen = kit.screenStand('screen', stage, SCREEN_AT);
  kit.pop(screen.root, tTeam, 1.0, 0.5, tOut0);
  cues.push({ t: tTeam, type: 'pop', pitch: 0.8 });

  const team = [  // where they stand, where they come from, facing, scale, coat, coat shade, hair
    [[-3.4, 0.9], -10.5, 1, 0.72, '#d9604f', '#a8413a', '#2b1d1a'],
    [[5.4, 1.0], 10.5, -1, 0.75, '#3f8f6f', '#2b6b52', '#5a3a22'],
    [[6.9, 0.6], 11.5, -1, 0.66, kit.AMBER_DEEP, '#b86c12', '#141414'],
  ];
  team.forEach(([at, startX, facing, s, coat, coatDeep, hair], k) => {
    const who = kit.person(`researcher${k}`, stage, at, s, { coat, coatDeep, hair, facing });
    const z = who.root.z;
    const tIn = tTeam + 0.15 + 0.3 * k;
    for (const f of every(1)) {
      const t = sec(f);
      let x = mix(startX, at[0], span(t, tIn, tIn + 1.0, kit.easeOut));
      x = mix(x, startX, span(t, tOut0 - 0.3, tOut0 + 0.5));
      const walk = span(t, tIn, tIn + 1.0) < 1 || span(t, tOut0 - 0.3, tOut0 + 0.5) > 0;
      const bob = walk ? 0.06 * Math.abs(Math.sin(t * 9)) : 0.0;
      key(who.root, 'loc', f, [x, at[1] + bob, z]);
      const point = span(t, tBuilt - 0.3 + 0.2 * k, tBuilt + 0.1 + 0.2 * k) * (1 - span(t, tName + 1.0, tName + 1.5));
      const deg = mix(8, k === 0 ? 75 : 50, point) + 3 * Math.sin(t * 1.3 + k);
      key(who.arm, 'rot', f, facing * radians(deg));
      key(who.head, 'rot', f, 0.04 * Math.sin(t * 0.9 + k * 2));
    }
  });

  const year = kit.text('year', '2025', 0.62, kit.material(kit.PAPER), stage, [-6.9, 3.85], { align: 'LEFT' });
  kit.appear(year, t2025, tOut0, 0.4);
  const m = parts.pip('machine', stage, [SCREEN_AT[0], SCREEN_AT[1] + 0.05], 1.0);
  kit.pop(m.root, tBuilt, 1.0, undefined, tOut0 - 0.1);
  parts.pipIdle(m);
  parts.pipBlink(m, [tBuilt + 1.5, tName + 0.8]);
  cues.push({ t: tBuilt, type: 'pop', pitch: 1.2 });
  const title = kit.text('title', 'Darwin Gödel Machine', 0.55, kit.material(kit.PAPER), stage, [SCREEN_AT[0], 3.25]);
  kit.appear(title, tName, tOut0 - 0.2, 0.5);
  cues.push({ t: tName, type: 'chime', gain: 0.6 });

  // ------------------------------------------------------------ Pip writes a changed copy: its child
  const n0 = parts.pip('n0', stage, PIP_AT, 1.3);
  parts.pipIdle(n0);
  parts.pipBlink(n0, [tPip + 1.2, tCopy + 1.0, tTests + 2.0, tMove + 3.0, tGrow1 + 1.0]);
  alpha(n0.halo, 1, 0.6);
  cues.push({ t: tPip, type: 'pop' });

  // not in place: a loop around Pip shows up and fades, and Pip shakes its eyes no
  const loop = kit.shape('in-place', kit.arcPts(1.6, 0.1, 110, 410, 48), kit.material(kit.MIST, null, 0.7), stage, PIP_AT, { lift: 0.05 });
  kit.appear(loop, tPlace, tPlace + 1.4, 0.3);
  for (const f of every(1, fr(tPlace), fr(tPlace + 1.8))) key(loop, 'rot', f, -(sec(f) - tPlace) * 2.5);
  [0.1, -0.1, 0.1, 0.0].forEach((dx, k) => parts.pipLook(n0, tPlace + 0.5 + 0.22 * k, dx, 0.0, 0.18));

  const code = parts.program('code', stage, CODE_AT, { rows: 6, w: 3.0, h: 3.6, seed: 44, tabIcon: true, scale: 0.8 });
  kit.pop(code.root, tCode, 0.8, undefined, tChild - 0.1);
  cues.push({ t: tCode, type: 'pop', pitch: 0.9 });
  const copy = parts.program('copy', stage, CODE_AT, { rows: 6, w: 3.0, h: 3.6, seed: 44, tabIcon: true, scale: 0.8 });
  const zc = copy.root.z;
  for (const f of every(1, 1, fr(tChild + 0.4))) {
    const t = sec(f);
    const q = span(t, tCopy, tCopy + 0.8, kit.easeOut);
    key(copy.root, 'loc', f, [mix(CODE_AT[0], CHILD_AT[0], q), mix(CODE_AT[1], CHILD_AT[1] + 0.1, q) + 0.3 * Math.sin(Math.PI * q), zc]);
    key(copy.root, 'scale', f, 0.8 * (t >= tCopy ? 1.0 : 0.001) * (1 - span(t, tChild, tChild + 0.25)) + 0.001);
  }
  cues.push({ t: tCopy, type: 'whoosh', gain: 0.5 });
  parts.pipLook(n0, tCopy - 0.3, 0.13, 0.0);
  const row = 2;
  const y = copy.rows[row][0].y;
  const hl = kit.shape('changed-row', kit.rrectPts(2.8, 0.36, 0.18), kit.material(kit.AMBER, null, 0.4, { over: kit.laid(kit.INK700, 0.5, kit.INK800) }),
    copy.root, [0, y], { lift: -0.0015 });
  alpha(hl, 1, 0.0);
  for (const [f, a] of [[fr(tChange), 0.0], [fr(tChange) + 3, 1.0], [fr(tChild - 0.2), 1.0], [fr(tChild), 0.0]]) alpha(hl, f, a);
  for (const ob of copy.rows[row]) {
    hold(ob, 'scale', fr(tChange));
    key(ob, 'scale', fr(tChange) + 4, [0.001, 1, 1]);
    key(ob, 'scale', fr(tChange) + 10, [1.25, 1, 1]);
  }
  cues.push({ t: tChange, type: 'tick', pitch: 1.3, gain: 0.7 });

  const child = parts.pip('n1', stage, CHILD_AT, 1.0, ...parts.scoreColour(23));
  kit.pop(child.root, tChild, 1.0);
  parts.pipIdle(child, undefined, undefined, 1.3, 2);
  parts.pipBlink(child, [tChild + 1.0, tScore + 0.6, tMove + 2.4]);
  alpha(child.halo, 1, 0.6);
  cues.push({ t: tChild, type: 'pop', pitch: 1.3 });
  const firstLine = kit.branch('first-line', lines, PIP_AT, CHILD_AT, kit.MIST);
  kit.grow(firstLine, tChild - 0.1, 0.4, tMove - 0.2);
  parts.pipLook(n0, tChild + 0.3, 0.14, 0.0);

  // ------------------------------------------------------------ the child is tested and gets a score
  parts.pipLook(child, tTests - 0.2, 0.12, -0.05);
  for (let k = 0; k < 4; k++) {
    const t0 = tTests + 0.55 * k;
    const job = parts.program(`task${k}`, stage, [9.5, -2.6], { rows: 3, w: 2.0, h: 1.4, seed: 50 + k, mistake: 1, scale: 0.6 });
    const zj = job.root.z;
    const tHit = t0 + 0.55;
    for (const f of every(1, fr(t0 - 0.1), fr(t0 + 1.7))) {
      const t = sec(f);
      let x = mix(9.5, CHILD_AT[0] + 0.3, span(t, t0, tHit, kit.easeOut));
      x = mix(x, -9.5, span(t, tHit + 0.2, t0 + 1.7, (v) => v * v));
      key(job.root, 'loc', f, [x, -2.4 + 0.15 * Math.sin(Math.PI * span(t, t0, tHit)), zj]);
    }
    if (k !== 2) {                          // one problem stays unsolved
      for (const ob of job.bad.bars) {
        alpha(ob, fr(tHit), 1.0);
        alpha(ob, fr(tHit + 0.1), 0.0);
      }
      for (const ob of job.good) {
        alpha(ob, fr(tHit), 0.0);
        alpha(ob, fr(tHit + 0.1), 1.0);
      }
      cues.push({ t: tHit, type: 'blip', pitch: 1.1 + 0.05 * k, gain: 0.5 });
    } else {
      cues.push({ t: tHit, type: 'tick', pitch: 0.7, gain: 0.5 });
    }
  }
  const big = kit.tag('n1-big-tag', stage, [CHILD_AT[0], CHILD_AT[1] + 2.05], '23', undefined, 0.42);
  kit.pop(big.root, tScore, 1.0, undefined, tMove - 0.3);
  cues.push({ t: tScore, type: 'chime', gain: 0.5, pitch: 1.2 });

  // ------------------------------------------------------------ parents are picked, and the family grows
  for (const [p, at, s0, dest] of [[n0, PIP_AT, 1.3, TREE[0][2]], [child, CHILD_AT, 1.0, TREE[1][2]]]) {
    const z = p.root.z;
    for (const f of every(1, fr(tMove - 0.05), fr(tMove + 1.0))) {
      const q = span(sec(f), tMove, tMove + 1.0);
      key(p.root, 'loc', f, [mix(at[0], dest[0], q), mix(at[1], dest[1], q), z]);
      key(p.root, 'scale', f, mix(s0, SIZE, q));
    }
    alpha(p.halo, fr(tMove), 0.6);
    alpha(p.halo, fr(tMove + 1.0), 0.35);
  }
  cues.push({ t: tMove, type: 'whoosh', gain: 0.4 });
  const n1Line = kit.branch('n1-line', lines, TREE[0][2], TREE[1][2]);
  kit.grow(n1Line, tMove + 0.9, 0.3);

  // when each node pops in, and who was picked to be its parent just before
  const tTree = { n2: tMove + 1.5, n3: tAgain + 0.4 };
  const later = TREE.slice(4, 16).map(([n]) => n);
  later.forEach((n, k) => { tTree[n] = mix(tGrow0, tGrow1, k / (later.length - 1)); });
  tTree.n16 = tOld + 0.45;
  tTree.n17 = tOld + 1.6;
  const nodes = TREE.slice(2).map(([n, pa, at, sc]) => ({ id: n, parent: pa, at, score: sc, t: tTree[n] }));
  const places = Object.fromEntries(TREE.map(([n, , at]) => [n, at]));
  const fam = parts.family('fam', stage, lines, nodes, { size: SIZE, known: places });
  for (const [n, pa, , sc] of TREE.slice(2)) {
    const r = kit.ring(`${n}-pick`, stage, places[pa], 0.62, kit.AMBER, undefined, 0.02);
    kit.flash(r, tTree[n] - 0.45, 0.6);
    kit.pop(fam[n].tag.root, tTree[n] + 0.25, 1.0, 0.3);
    cues.push({ t: tTree[n], type: 'pop', pitch: 0.9 + sc / 60, gain: 0.45 });
  }
  for (const [n, s] of [['n0', 20], ['n1', 23]]) {
    const tg = kit.tag(`${n}-tag`, stage, [places[n][0] + 0.8, places[n][1] + 0.3], String(s));
    kit.pop(tg.root, tMove + 1.0, 1.0, 0.3);
  }
  cues.push({ t: tGrow0, type: 'rise', dur: tGrow1 - tGrow0, pitch: 0.9, gain: 0.35 });

  // the old ones stay, and an early program becomes a parent again
  const old = kit.ring('old-glow', stage, places.n2, 0.75, kit.MINT, 0.12, 0.02);
  for (const [f, a] of [[fr(tOld - 0.3), 0.0], [fr(tOld), 1.0], [fr(tOld + 1.2), 1.0], [fr(tOld + 1.8), 0.0]]) alpha(old, f, a);
  cues.push({ t: tOld, type: 'chime', gain: 0.45, pitch: 0.9 });

  // ------------------------------------------------------------ camera
  const path = (t) => {
    const q = kit.smooth(t / end);
    let [x, y, h] = [0.1 * q, 0.05 * q, kit.H0 - 0.4 * q];
    const tree = span(t, tMove, tMove + 1.4);
    [x, y, h] = [mix(x, -4.2, tree), mix(y, 0.1, tree), mix(h, 15.0, tree)];
    const wide = span(t, tGrow0 - 0.5, tGrow0 + 3.0);
    [x, y, h] = [mix(x, 0.0, wide), mix(y, 0.6, wide), mix(h, kit.H0 + 1.0, wide)];
    const back = span(t, T.start(4) - 0.2, T.start(4) + 1.6);
    return [mix(x, -2.6, back), mix(y, -0.6, back), mix(h, 16.5, back)];
  };

  kit.camera(path, 1.0);
  return cues;
}
