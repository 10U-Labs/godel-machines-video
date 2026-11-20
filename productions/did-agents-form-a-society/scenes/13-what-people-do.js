/* Scene 13: What people do.

A cluster of agents, with a question mark over it. Four suns for its four
days. Then the cluster moves to the right, and a group of people around a
fire appears on the left. They give way to six small pictures of what the
agents did, each with its name under it: one thought over three agents, and
the same thought crossed out; four agents joined around a word, and a dark
agent beside two that hold what it found; an agent following two across a
line, and an agent with a tick, a clock at its side, tied to its group.
*/
'use strict';

function build(T) {
  const { sec } = kit;
  parts.begin();

  const COLS = [-5.3, 0.0, 5.3];
  const ROWS = [2.15, -1.75];
  const cues = [];
  const end = sec(kit.frames());
  const tDid = T.at(0, 0.6);
  const tLasted = T.start(1);
  const tShort = T.at(1, 0.28);
  const tBut = T.at(1, 0.5);
  const tPeople = T.at(1, 0.66);
  const tBelieve = T.start(2);
  const tWrong = T.at(2, 0.3);
  const tWorked = T.start(3);
  const tRisked = T.at(3, 0.25);
  const tPeers = T.start(4);
  const tStood = T.at(4, 0.3);
  const NAMED = [T.at(2, 0.55), T.at(2, 0.8), T.at(3, 0.68), T.at(3, 0.87), T.at(4, 0.72), T.at(4, 0.86)];

  kit.backdrop(5);
  kit.motes(20, 17);
  const st = parts.stage();

  // ------------------------------------------------------------ the group, its four days, and the question
  const cluster = parts.group('cluster', st.cast, [0, -0.5]);
  const rnd = new kit.Random(71);
  const places = [];
  for (let tries = 0; places.length < 24 && tries < 3000; tries++) {
    const a = rnd.random() * 2 * Math.PI;
    const far = Math.sqrt(rnd.random());
    const at = [3.0 * far * Math.cos(a), 1.75 * far * Math.sin(a)];
    if (places.every(([x, y]) => Math.hypot(at[0] - x, at[1] - y) > 0.78)) places.push(at);
  }
  places.sort((p, q) => q[1] - p[1]).forEach((at, i) => {
    const made = parts.mini(`member${i}`, cluster, at, 0.5, i === 7 ? 0 : 1 + rnd.randrange(5));
    kit.pop(made.root, 0.2 + 0.03 * i, 0.5, 0.3);
  });
  cues.push({ t: 0.2, type: 'swoosh', dur: 1.0, gain: 0.6 });
  const asked = kit.text('asked', '?', 2.2, kit.material(kit.PAPER), st.front, [0, 2.7]);
  kit.appear(asked, tDid, tLasted + 0.2, 0.3);
  cues.push({ t: tDid, type: 'blip', pitch: 0.8 });
  [0, 1, 2, 3].forEach((k) => {
    const day = parts.group(`day${k}`, st.front, [-1.35 + 0.9 * k, 2.75]);
    kit.shape(`day${k}-glow`, kit.circlePts(0.55), kit.glowMaterial(kit.AMBER, 0.6), day);
    kit.shape(`day${k}-sun`, kit.circlePts(0.26), kit.material('#fff2c4', kit.AMBER), day);
    kit.pop(day, tLasted + 0.5 + 0.3 * k, 1.0, 0.3, tShort + 1.0 + 0.12 * k);
    cues.push({ t: tLasted + 0.5 + 0.3 * k, type: 'tick', pitch: 1.0 + 0.1 * k });
  });
  parts.move(cluster, tBut, [3.9, -0.5], 1.2);
  cues.push({ t: tBut, type: 'whoosh', gain: 0.6 });

  // ------------------------------------------------------------ what people do when they live together
  const town = parts.group('town', st.front, [-3.9, -0.5]);
  parts.fire('fire', town, [0, -1.55]);
  kit.pop(town, tPeople, 1.0, 0.5, tBelieve - 0.5);
  [[-2.3, 1], [-1.2, 1], [1.2, -1], [2.3, -1], [0, 1]].forEach(([x, facing], k) => {
    const made = parts.human(`villager${k}`, st.cast, [-3.9 + x, -2.3 + (k === 4 ? 0.9 : 0)], 0.4, k, facing);
    kit.pop(made.root, tPeople + 0.1 + 0.12 * k, 0.4, 0.4, tBelieve - 0.5 + 0.03 * k);
    cues.push({ t: tPeople + 0.1 + 0.12 * k, type: 'pop', pitch: 0.7 + 0.08 * k, gain: 0.6 });
  });
  parts.vanish(cluster, tBelieve - 0.5, 0.35);

  // ------------------------------------------------------------ six things the agents did, and their names
  const NAMES = ['shared belief', 'collective mistake', 'cooperation', 'altruism', 'peer influence', 'loyalty to a group'];
  const scene = (k, t) => {
    const at = [COLS[Math.floor(k / 2)], ROWS[k % 2]];
    const root = parts.group(`did${k}`, st.props, at, 1.2);
    kit.pop(root, t, 1.2, 0.4);
    cues.push({ t, type: 'pop', pitch: 0.8 + 0.08 * k });
    const label = kit.text(`name${k}`, NAMES[k], 0.42, kit.material(kit.PAPER), st.front, [at[0], at[1] - 1.72]);
    kit.appear(label, NAMED[k], null, 0.3);
    cues.push({ t: NAMED[k], type: 'chime', gain: 0.35, pitch: 0.9 + 0.06 * k, dur: 1.0 });
    return root;
  };
  const trio = (name, root, colours = [1, 2, 4]) => colours.map((which, i) => parts.mini(`${name}-m${i}`, root, [-1.0 + i, -0.62], 0.55, which));
  const thinks = (name, root) => {
    const cloud = parts.thought(name, root, [0, 0.88], 2.3, 1.0, [0, -1]);
    parts.scorer(`${name}-scorer`, cloud.root, [-0.55, 0.0], 0.32, false);
    parts.sheet(`${name}-read`, cloud.root, [0.45, 0.02], { scale: 0.55, seed: 7 });
    return cloud;
  };

  const one = scene(0, tBelieve);
  trio('one', one);
  thinks('one-thought', one);

  const two = scene(1, tWrong);
  trio('two', two);
  thinks('two-thought', two);
  const mistaken = parts.cross('two-wrong', two, [0, 0.88], 2.0);
  kit.pop(mistaken, tWrong + 0.7, 2.0, 0.3);
  cues.push({ t: tWrong + 0.7, type: 'tick', pitch: 0.5, gain: 1.2 });

  const three = scene(2, tWorked);
  [[-1.25, 0.55, 1], [1.25, 0.55, 3], [-1.25, -0.6, 2], [1.25, -0.6, 5]].forEach(([x, y, which], i) => {
    kit.grow(kit.branch(`three-tie${i}`, three, [x * 0.62, y * 0.6], [0, 0], kit.MIST, 0.07, 0.7), tWorked + 0.5 + 0.1 * i, 0.3);
    parts.mini(`three-m${i}`, three, [x, y], 0.5, which);
  });
  kit.pop(parts.word('three-word', three, [0, 0], 0.6, false).root, tWorked + 1.0, 0.6, 0.3);

  const four = scene(3, tRisked);
  const giver = parts.mini('four-giver', four, [-1.2, -0.3], 0.55, 3);
  parts.miniOff(giver, tRisked + 1.0, 0.3);
  kit.branch('four-gives', four, [-0.55, -0.3], [0.15, -0.3], kit.PAPER, 0.08, 1.0);
  kit.shape('four-gives-head', [[0.1, -0.1], [0.42, -0.3], [0.1, -0.5]], kit.material(kit.PAPER), four);
  [[0.95, 0.15, 1], [1.5, -0.7, 4]].forEach(([x, y, which], i) => {
    parts.mini(`four-m${i}`, four, [x, y], 0.5, which);
    kit.pop(parts.sheet(`four-got${i}`, four, [x + 0.05, y + 0.72], { scale: 0.42, seed: 9 + i }).root, tRisked + 1.3 + 0.2 * i, 0.42, 0.3);
  });
  cues.push({ t: tRisked + 1.0, type: 'tick', pitch: 0.5, gain: 1.1 });

  const five = scene(4, tPeers);
  for (let d = 0; d < 6; d++) kit.branch(`five-dash${d}`, five, [0.1, 0.95 - d * 0.36], [0.1, 0.75 - d * 0.36], kit.CORAL, 0.08, 0.85);
  parts.mini('five-m0', five, [1.1, 0.35], 0.5, 1);
  parts.mini('five-m1', five, [1.6, -0.5], 0.5, 2);
  const follower = parts.mini('five-follower', five, [-1.3, -0.1], 0.5, 0);
  parts.send(follower.root, [[-1.3, -0.1], [0.75, -0.75]], tPeers + 1.3, tPeers + 2.2, { shown: true, size: 0.5, stay: true });
  cues.push({ t: tPeers + 1.3, type: 'whoosh', gain: 0.5 });

  const six = scene(5, tStood);
  [[0.8, 0.35, 1], [1.5, -0.1, 4], [0.9, -0.75, 2]].forEach(([x, y, which], i) => parts.mini(`six-m${i}`, six, [x, y], 0.5, which));
  kit.grow(kit.branch('six-bond', six, [-0.75, -0.2], [0.45, -0.2], kit.MINT, 0.09, 0.9), tStood + 0.6, 0.4);
  parts.mini('six-loyal', six, [-1.2, -0.2], 0.55, 0);
  kit.pop(parts.check('six-word', six, [-1.2, 0.6], 0.7), tStood + 1.0, 0.7, 0.3);
  const cost = parts.clock('six-clock', six, [-2.0, -0.35], 0.45, 0.3);
  parts.drain(cost, tStood + 1.2, end, 0.15);
  cues.push({ t: tStood + 1.0, type: 'blip', pitch: 1.1 });

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [0, 0.4, 18.5]], [tBut, [0, 0.3, 19.5]], [tBelieve - 0.4, [0, 0.1, 20]], [tBelieve + 1.0, [-1.6, 0.0, 19]], [tWorked - 0.3, [-1.5, 0.0, 18.8]],
    [tWorked + 1.0, [0.0, 0.0, 19]], [tPeers - 0.3, [0.2, 0.0, 18.8]], [tPeers + 1.0, [1.6, 0.0, 19]], [NAMED[4], [1.5, 0.0, 19.2]], [NAMED[5], [0, 0.05, 20.4]], [end, [0, 0.05, 20.1]],
  ]), 1.0);
  return cues;
}
