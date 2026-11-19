/* Scene 06: The wrong parents.

Two programs wait to be picked as parents. The one with the higher score is
picked. Then two other researchers walk up and look further down: the
picked program's children and grandchildren come out weak, while the
lower-scored program's family comes out strong.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, alpha, every } = kit;
  const radians = (deg) => deg * Math.PI / 180;

  const SIZE = 0.5;
  const A_AT = [-5.4, 1.7];     // higher score, weak family
  const B_AT = [-5.4, -1.6];    // lower score, strong family

  const FAMILY = [  // id, parent, place, score
    ['a1', 'a', [-3.1, 2.6], 30],
    ['a2', 'a', [-3.1, 1.0], 27],
    ['a3', 'a1', [-0.8, 3.0], 26],
    ['a4', 'a2', [-0.8, 1.4], 24],
    ['b1', 'b', [-3.1, -0.9], 38],
    ['b2', 'b', [-3.1, -2.4], 42],
    ['b3', 'b1', [-0.8, -0.3], 46],
    ['b4', 'b2', [-0.8, -1.7], 49],
    ['b5', 'b2', [-0.8, -3.0], 45],
  ];

  kit.state.zstep = 0.0005;
  const cues = [];
  const end = sec(kit.frames());
  const tPick = T.at(0, 0.5);
  const tGroup = T.start(1);
  const tKids = T.at(1, 0.6);
  const tGrand = T.at(1, 0.78);
  const tVerdict = T.end(1) - 0.4;

  kit.backdrop(61, kit.VIOLET_DEEP);
  kit.motes(undefined, 62, kit.MIST);
  const lines = kit.layer('lines', 0.9);
  const stage = kit.layer('stage', 1.0);

  // ------------------------------------------------------------ two would-be parents and their scores
  const parents = parts.family('par', stage, lines, [
    { id: 'a', parent: null, at: A_AT, score: 41, t: 0.15 },
    { id: 'b', parent: null, at: B_AT, score: 33, t: 0.3 },
  ], { size: SIZE, idleStep: 2 });
  for (const n of ['a', 'b']) kit.pop(parents[n].tag.root, 0.45, 1.0, 0.3);
  cues.push({ t: 0.15, type: 'pop' });
  const pick = kit.ring('pick', stage, A_AT, 0.75, kit.AMBER, 0.1, 0.02);
  for (const [f, a] of [[fr(tPick), 0.0], [fr(tPick + 0.25), 1.0], [fr(tGrand), 1.0], [fr(tGrand + 0.5), 0.35]]) alpha(pick, f, a);
  for (const f of every(1, fr(tPick), fr(tPick + 0.5))) {
    const s = Math.max(0.001, kit.backOut((sec(f) - tPick) / 0.5));
    key(pick, 'scale', f, [s, s, 1]);
  }
  cues.push({ t: tPick, type: 'chime', gain: 0.5 });
  const aPip = parents.a.pip;
  parts.pipEyes(aPip, tPick + 0.1, 1.15, 0.65);          // pleased
  parts.pipEyes(aPip, tGrand + 0.4, 1.0, 1.0);
  const bPip = parents.b.pip;
  parts.pipLook(bPip, tPick, 0.0, 0.1);

  // ------------------------------------------------------------ a second group looks further down the family
  const group = [
    [[5.6, 1.0], 10.5, 0.74, '#4a6fd1', '#33509e', '#d8c7a0'],
    [[7.1, 0.7], 11.5, 0.68, '#c25a9b', '#8f3f72', '#2b1d1a'],
  ];
  group.forEach(([at, startX, s, coat, coatDeep, hair], k) => {
    const who = kit.person(`group${k}`, stage, at, s, { coat, coatDeep, hair, facing: -1 });
    const z = who.root.z;
    const tIn = tGroup + 0.25 * k;
    for (const f of every(1)) {
      const t = sec(f);
      const q = span(t, tIn, tIn + 1.1, kit.easeOut);
      const bob = q > 0 && q < 1 ? 0.06 * Math.abs(Math.sin(t * 9)) : 0.0;
      key(who.root, 'loc', f, [mix(startX, at[0], q), at[1] + bob, z]);
      const point = span(t, tKids - 0.4 + 0.3 * k, tKids + 0.2 * k);
      key(who.arm, 'rot', f, -radians(mix(8, 65 - 15 * k, point) + 3 * Math.sin(t * 1.4 + k)));
      key(who.head, 'rot', f, 0.05 * Math.sin(t * 0.8 + k) - 0.08 * point);
    }
  });
  const floor = kit.shape('floor', kit.rrectPts(10, 0.06, 0), kit.material(kit.MIST, null, 0.2), stage, [8.0, -2.35]);
  kit.appear(floor, tGroup, null, 0.6);
  cues.push({ t: tGroup, type: 'whoosh', gain: 0.4 });

  const nodes = FAMILY.map(([n, pa, at, sc]) => {
    const gen2 = pa === 'a' || pa === 'b';
    const t = (gen2 ? tKids : tGrand) + (n.startsWith('b') ? 0.12 : 0.0) + 0.05 * Number(n[1]);
    return { id: n, parent: pa, at, score: sc, t };
  });
  const fam = parts.family('fam', stage, lines, nodes, { size: SIZE * 0.9, known: { a: A_AT, b: B_AT } });
  for (const d of nodes) kit.pop(fam[d.id].tag.root, d.t + 0.2, 1.0, 0.3);
  cues.push({ t: tKids, type: 'pop', pitch: 0.9, gain: 0.6 });
  cues.push({ t: tGrand, type: 'pop', pitch: 1.1, gain: 0.6 });

  // the strong family glows; the picked parent's family stays dim
  const glow = kit.shape('b-glow', kit.rrectPts(7.0, 4.4, 1.6), kit.glowMaterial(kit.AMBER, 0.45, 0.9), stage, [-2.9, -1.6], { lift: -0.2 });
  kit.appear(glow, tVerdict - 0.8, null, 0.8);
  cues.push({ t: tVerdict - 0.8, type: 'rise', dur: 0.8, pitch: 1.1, gain: 0.5 });
  parts.pipLook(bPip, tGrand + 0.3, 0.12, -0.04);

  const path = (t) => {
    const q = kit.smooth(t / end);
    const look = span(t, tGroup - 0.3, tGroup + 1.5);
    return [mix(-3.2, 0.0, look) + 0.2 * q, 0.1, mix(15.5, kit.H0, look) - 0.3 * q];
  };

  kit.camera(path, 1.0);
  return cues;
}
