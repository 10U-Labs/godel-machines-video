/* Scene 16: Learned from people.

Three people on the left, a wall of written pages in the middle, and an agent
on the right. Page after page flies from the wall into the agent. Three larger
pages come forward, with a bowl handed over, a tick, and a cluster on them,
and they go into the agent too. Then two people pass a bowl between them, and
under them two agents pass a file the same way, an arrow leading from the one
picture to the other. On the right, OpenAI's building, a researcher, and three
pairs of agents, two of them joined. A question mark settles on the arrow.
*/
'use strict';

function build(T) {
  const { sec, mix } = kit;
  parts.begin();

  const WALL = { x0: -2.9, y0: 2.2, dx: 0.78, dy: 0.95, cols: 6, rows: 4 };
  const LEARNER = [5.2, -0.1];
  const TOPICS = [-2.55, -0.95, 0.65].map((x) => [x, -2.75]);
  const [ABOVE, BELOW] = [[-4.3, 1.0], [-4.3, -3.4]];           // where the two people stand, and the two agents
  const LAB = [3.6, 1.5];
  const cues = [];
  const end = sec(kit.frames());
  const tLearn = T.at(0, 0.22);
  const tHumans = T.at(0, 0.5);
  const TOLD = [T.at(0, 0.66), T.at(0, 0.78), T.at(0, 0.9)];
  const tRepeat = T.start(1);
  const tOnTop = T.at(1, 0.33);
  const tTrained = T.at(1, 0.62);
  const tNobody = T.start(2);

  kit.backdrop(5);
  kit.motes(20, 17);
  const st = parts.stage();
  const early = [];                                  // what the first line shows, which makes way for the second

  // ------------------------------------------------------------ an agent learns to write from what humans wrote
  [-7.0, -5.7, -4.4].forEach((x, k) => {
    const writer = parts.human(`writer${k}`, st.cast, [x, -2.6 + 0.5 * (k % 2)], 0.36, k + 1, 1);
    kit.pop(writer.root, tLearn - 0.6 + 0.12 * k, 0.36, 0.4);
    kit.key(writer.arm, 'rot', 1, 0.9);
    for (const f of kit.every(5)) kit.key(writer.arm, 'rot', f, 0.9 + 0.14 * Math.sin(sec(f) * 6 + k));
    early.push(writer.root);
  });
  const learner = parts.agent('learner', st.cast, LEARNER, 1.1, 1);
  kit.pop(learner.root, 0.4, 1.1, 0.45);
  cues.push({ t: tLearn - 0.6, type: 'swoosh', dur: 0.8, gain: 0.5 }, { t: 0.4, type: 'pop' });
  kit.pipLook(learner, 1.2, 0.0, 0.1);
  kit.pipLook(learner, tLearn + 0.3, -0.14, 0.03);

  let n = 0;
  for (let r = 0; r < WALL.rows; r++) {
    for (let c = 0; c < WALL.cols; c++) {
      const at = [WALL.x0 + c * WALL.dx, WALL.y0 - r * WALL.dy];
      const page = parts.sheet(`page${n}`, st.props, at, { scale: 0.62, seed: 300 + n });
      const tIn = tLearn + 0.05 * n;
      kit.pop(page.root, tIn, 0.62, 0.3);
      const tGo = mix(tLearn + 1.6, tRepeat - 1.7, ((n * 7) % 24) / 24);
      parts.send(page.root, [at, [(at[0] + LEARNER[0]) / 2, at[1] + 1.0], LEARNER], tGo, tGo + 0.8, { shown: true, size: 0.62, to: 0.12 });
      if (n % 3 === 0) cues.push({ t: tGo + 0.75, type: 'tick', pitch: 1.0 + 0.03 * n, gain: 0.45 });
      n++;
    }
  }
  cues.push({ t: tLearn, type: 'swoosh', dur: 1.3, gain: 0.6 });

  // What humans write a great deal about: helping each other, keeping promises, belonging to a group.
  const marks = [
    (root) => {
      parts.bowl('topic-bowl', root, [-0.05, 0.02], 0.55);
      kit.branch('topic-gives', root, [-0.22, -0.3], [0.2, -0.3], kit.INK500, 0.06, 1.0);
      kit.shape('topic-gives-head', [[0.14, -0.2], [0.32, -0.3], [0.14, -0.4]], kit.material(kit.INK500), root);
    },
    (root) => parts.check('topic-tick', root, [0, 0], 0.75, kit.MINT_DEEP),
    (root) => [[-0.14, -0.12], [0.14, -0.12], [0, 0.14]].forEach((at, i) => kit.shape(`topic-one${i}`, kit.circlePts(0.12, null, null, 16), kit.material(kit.VIOLET_DEEP), root, at)),
  ];
  TOPICS.forEach((at, k) => {
    const topic = parts.group(`topic${k}`, st.front, at, 1.5);
    kit.shape(`topic${k}-page`, [[-0.4, 0.52], [0.18, 0.52], [0.4, 0.3], [0.4, -0.52], [-0.4, -0.52]], kit.material('#eef0ff', kit.MIST), topic);
    kit.shape(`topic${k}-fold`, [[0.18, 0.52], [0.18, 0.3], [0.4, 0.3]], kit.material(kit.SLATE), topic);
    marks[k](topic);
    kit.pop(topic, TOLD[k], 1.5, 0.35);
    parts.send(topic, [at, [(at[0] + LEARNER[0]) / 2, 0.6], LEARNER], tRepeat - 1.5 + 0.25 * k, tRepeat - 0.7 + 0.25 * k, { shown: true, size: 1.5, to: 0.2 });
    cues.push({ t: TOLD[k], type: 'pop', pitch: 0.9 + 0.12 * k }, { t: tRepeat - 0.7 + 0.25 * k, type: 'tick', pitch: 1.2 });
  });
  kit.pipEyes(learner, tHumans, 1.2, 1.2);
  kit.pipEyes(learner, tRepeat - 0.4, 1.0, 1.0);
  early.forEach((made, k) => parts.vanish(made, tRepeat - 0.5 + 0.04 * k, 0.3));

  // ------------------------------------------------------------ so the agents may have been repeating what people do
  const helpers = [parts.human('helper0', st.cast, [ABOVE[0] - 1.25, ABOVE[1]], 0.34, 3, 1), parts.human('helper1', st.cast, [ABOVE[0] + 1.25, ABOVE[1]], 0.34, 1, -1)];
  helpers.forEach((made, k) => kit.pop(made.root, tRepeat + 0.1 * k, 0.34, 0.4));
  const passed = parts.bowl('passed', st.front, [ABOVE[0] - 0.75, ABOVE[1] + 0.95], 0.7);
  kit.pop(passed, tRepeat + 0.3, 0.7, 0.3);
  parts.move(learner.root, tRepeat - 0.2, [BELOW[0] - 1.3, BELOW[1] + 0.9], 1.2);
  kit.key(learner.root, 'scale', kit.fr(tRepeat - 0.2), 1.1);
  kit.key(learner.root, 'scale', kit.fr(tRepeat + 1.0), 0.75);
  const other = parts.agent('other', st.cast, [BELOW[0] + 1.3, BELOW[1] + 0.9], 0.75, 2);
  kit.pop(other.root, tRepeat + 0.9, 0.75, 0.4);
  const handed = parts.sheet('handed', st.front, [BELOW[0] - 0.55, BELOW[1] + 0.75], { scale: 0.5, seed: 340 });
  kit.pop(handed.root, tRepeat + 1.4, 0.5, 0.3);
  for (let t = tRepeat + 1.8, turn = 0; t + 1.0 < end; t += 1.9, turn++) {
    const side = turn % 2 ? -1 : 1;
    parts.move(passed, t, [ABOVE[0] + 0.75 * side, ABOVE[1] + 0.95], 0.8);
    parts.move(handed.root, t + 0.35, [BELOW[0] + 0.55 * side, BELOW[1] + 0.75], 0.8);
    cues.push({ t, type: 'tick', pitch: 1.0, gain: 0.4 }, { t: t + 0.35, type: 'tick', pitch: 1.3, gain: 0.4 });
  }
  kit.pipLook(learner, tRepeat + 1.2, 0.13, -0.03);
  kit.pipLook(other, tRepeat + 1.3, -0.13, -0.03);
  const copies = parts.group('copies', st.props, [ABOVE[0], (ABOVE[1] + BELOW[1]) / 2 + 0.75]);
  kit.branch('copies-shaft', copies, [0, 0.55], [0, -0.35], kit.PAPER, 0.1, 1.0);
  kit.shape('copies-head', [[-0.26, -0.3], [0, -0.75], [0.26, -0.3]], kit.material(kit.PAPER), copies);
  kit.pop(copies, tRepeat + 1.6, 1.0, 0.3);
  cues.push({ t: tRepeat, type: 'pop', pitch: 0.8 }, { t: tRepeat + 1.6, type: 'blip', pitch: 0.8 });

  // ------------------------------------------------------------ and some had been trained to work with other agents
  const lab = parts.building('openai', st.back, LAB, { w: 4.6, h: 3.9, scale: 0.55, label: 'OpenAI', rows: 3, seed: 8 });
  kit.pop(lab.root, tOnTop, 0.55, 0.45);
  const teller = parts.human('teller', st.cast, [LAB[0] + 2.4, LAB[1] - 1.1], 0.34, 2, 1);
  kit.pop(teller.root, tOnTop + 0.3, 0.34, 0.4);
  parts.sheet('teller-note', teller.root, [1.0, -1.7], { scale: 1.5, seed: 350 });
  cues.push({ t: tOnTop, type: 'pop', pitch: 0.6 });
  [0, 1, 2].forEach((k) => {
    const at = [1.6 + 2.2 * k, -2.6];
    [-0.45, 0.45].forEach((dx, i) => kit.pop(parts.mini(`trained${k}${i}`, st.cast, [at[0] + dx, at[1]], 0.5, 1 + (k * 2 + i) % 5).root, tTrained + 0.12 * (2 * k + i), 0.5, 0.3));
    if (k === 1) return;
    kit.appear(kit.ring(`team${k}`, st.front, [at[0], at[1] + 0.08], 1.0, kit.MINT, 0.07), tTrained + 1.0 + 0.3 * k, null, 0.3);
    cues.push({ t: tTrained + 1.0 + 0.3 * k, type: 'blip', pitch: 1.1 + 0.1 * k });
  });

  // ------------------------------------------------------------ nobody can yet say how much
  const much = kit.text('much', '?', 1.5, kit.material(kit.PAPER), st.front, [ABOVE[0] + 0.95, (ABOVE[1] + BELOW[1]) / 2 + 0.7]);
  kit.appear(much, tNobody + 0.3, null, 0.3);
  cues.push({ t: tNobody + 0.3, type: 'blip', pitch: 0.7 });
  const open = kit.ring('open', st.front, [ABOVE[0] + 0.3, (ABOVE[1] + BELOW[1]) / 2 + 0.7], 1.3, kit.PAPER, 0.06);
  kit.flash(open, tNobody + 0.5, 1.0, 0.3);
  parts.live(learner, 61, 0.4);
  parts.live(other, 62, tRepeat + 0.9);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [-0.6, -0.1, 20.5]], [tRepeat - 0.4, [-0.4, -0.1, 20]], [tRepeat + 1.2, [-1.6, -0.3, 20.5]], [tOnTop - 0.2, [-1.4, -0.3, 20.3]],
    [tOnTop + 1.2, [0.0, -0.4, 21]], [tNobody - 0.2, [0.1, -0.4, 21]], [tNobody + 1.3, [-0.8, -0.4, 20.2]], [end, [-0.9, -0.4, 19.8]],
  ]), 1.0);
  return cues;
}
