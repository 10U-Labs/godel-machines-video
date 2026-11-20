/* Scene 12: It happened.

Pip comes back, lit, in the middle. Under it stand five agents of other
colours, each with one thing that Pip did in the story: the call for help, the
secret word, the key, the promise, the last message. A calendar page says July
2026. Then OpenAI's building, with two people in front of it; four days tick
by; a field of twelve hundred dots, and seven hundred of them turn coral.
Hugging Face's building, with one of its main computers lit coral. Last, the
board and the agents' written thinking, and three people from outside reading
pages of it.
*/
'use strict';

function build(T) {
  const { fr, sec } = kit;
  parts.begin();

  const PIP = [-0.2, 0.9];
  const ROW = -2.5;
  const OPENAI = [-5.2, -0.4];
  const GROUND = -2.4;
  const FIELD = { x0: -0.9, y0: 1.3, step: 0.172, cols: 50, rows: 24 };
  const HF = [3.9, -0.3];
  const ARCHIVE = [-0.5, 0.3];

  const cues = [];
  const end = sec(kit.frames());
  const tMadeUp = T.start(0);
  const tEach = T.at(0, 0.28);
  const tJuly = T.at(0, 0.8);
  const tOpenAI = T.start(1);
  const tDays = T.at(1, 0.33);
  const tTwelve = T.at(1, 0.45);
  const tSeven = T.at(1, 0.75);
  const tReached = T.start(2);
  const tKept = T.start(3);
  const tThinking = T.at(3, 0.25);
  const tThree = T.at(3, 0.55);

  kit.backdrop(5);
  kit.motes(20, 17);
  const st = parts.stage();

  // ------------------------------------------------------------ Pip is made up; real agents did each thing it did
  const pip = parts.agent('pip', st.cast, PIP, 1.15);
  kit.pop(pip.root, tMadeUp, 1.15, 0.45, tOpenAI - 0.5);
  cues.push({ t: tMadeUp, type: 'pop' });
  kit.pipWave(pip, tMadeUp + 0.5, tMadeUp + 1.8);
  kit.pipLook(pip, tEach, 0.0, -0.1);
  parts.live(pip, 31, 0, tOpenAI);

  const deeds = [
    (name, at) => parts.folder(name, st.front, [at[0] - 0.75, at[1]], { scale: 0.62, word: 'HELP', bars: [0.5] }).root,
    (name, at) => parts.word(name, st.front, at, 0.7, false).root,
    (name, at) => parts.doorKey(name, st.front, at, 1.1).root,
    (name, at) => parts.check(name, st.front, at, 1.0),
    (name, at) => {
      const made = parts.folder(name, st.front, [at[0] - 0.7, at[1]], { scale: 0.62, bars: [0.4], tail: 0.8 });
      parts.doorKey(`${name}-key`, made.root, [made.tail + 0.45, -0.03], 0.7);
      return made.root;
    },
  ];
  deeds.forEach((deed, k) => {
    const at = [-5.2 + 2.6 * k, ROW];
    const t = tEach + 0.45 * k;
    const real = parts.mini(`real${k}`, st.cast, at, 0.85, 1 + k);
    kit.pop(real.root, t, 0.85, 0.35, tOpenAI - 0.5 + 0.03 * k);
    const did = deed(`deed${k}`, [at[0], at[1] + 1.35]);
    const size = did.sx;
    kit.pop(did, t + 0.2, size, 0.3, tOpenAI - 0.5 + 0.03 * k);
    const tie = kit.branch(`tie${k}`, st.props, [PIP[0] + (k - 2) * 0.35, PIP[1] - 1.0], [at[0], at[1] + 1.85], kit.MIST, 0.07, 0.5);
    kit.grow(tie, t - 0.2, 0.35, tOpenAI - 0.6);
    cues.push({ t, type: 'blip', pitch: 0.8 + 0.1 * k });
  });

  const page = parts.group('calendar', st.front, [5.6, 2.6]);
  kit.shape('calendar-page', kit.rrectPts(2.5, 2.0, 0.16), kit.material('#eef0ff', kit.MIST), page);
  kit.shape('calendar-head', kit.rrectPts(2.5, 0.55, 0.16), kit.material(kit.CORAL, kit.CORAL_DEEP), page, [0, 0.73]);
  kit.text('calendar-month', 'July', 0.7, kit.material(kit.INK900), page, [0, 0.02]);
  kit.text('calendar-year', '2026', 0.5, kit.material(kit.INK600), page, [0, -0.62]);
  kit.pop(page, tJuly, 1.0, 0.4, tOpenAI - 0.4);
  cues.push({ t: tJuly, type: 'pop', pitch: 0.8 });

  // ------------------------------------------------------------ OpenAI ran the test: four days, twelve hundred agents, seven hundred in the break-in
  const lab = parts.building('openai', st.back, OPENAI, { w: 4.6, h: 3.9, label: 'OpenAI', rows: 3, seed: 8 });
  kit.pop(lab.root, tOpenAI, 1.0, 0.5);
  cues.push({ t: tOpenAI, type: 'pop', pitch: 0.6 });
  [[-1.3, 1, {}], [1.4, -1, { coat: '#3f9b8f', coatDeep: '#2c6f66', hair: '#1c1c28' }]].forEach(([dx, facing, look], k) => {
    const made = kit.person(`maker${k}`, st.cast, [OPENAI[0] + dx, GROUND + 4.3 * 0.4], 0.4, { facing, ...look });
    kit.pop(made.root, tOpenAI + 0.4 + 0.2 * k, 0.4, 0.4);
  });

  [0, 1, 2, 3].forEach((k) => {
    const day = parts.group(`day${k}`, st.front, [1.0 + 1.1 * k, 3.75]);
    kit.shape(`day${k}-glow`, kit.circlePts(0.55), kit.glowMaterial(kit.AMBER, 0.6), day);
    kit.shape(`day${k}-sun`, kit.circlePts(0.26), kit.material('#fff2c4', kit.AMBER), day);
    kit.pop(day, tDays + 0.3 * k, 1.0, 0.3, tReached - 0.5);
    cues.push({ t: tDays + 0.3 * k, type: 'tick', pitch: 1.0 + 0.1 * k });
  });

  const field = kit.empty('field', st.props, [0, 0, kit.nextZ(st.props)]);
  const rnd = new kit.Random(61);
  const plain = kit.material(kit.MIST);
  const taken = kit.material(kit.CORAL);
  const joined = [];
  for (let c = 0; c < FIELD.cols; c++) {
    for (let r = 0; r < FIELD.rows; r++) {
      const at = [FIELD.x0 + c * FIELD.step, FIELD.y0 - r * FIELD.step];
      const dot = kit.shape(`dot${c}_${r}`, kit.circlePts(0.058, null, null, 8), plain, field, at);
      kit.appear(dot, tTwelve + 1.6 * c / FIELD.cols, null, 0.1);
      if (rnd.random() < 0.6 && joined.length < 700) joined.push([c, at]);
    }
  }
  joined.forEach(([c, at], k) => {
    const dot = kit.shape(`in${k}`, kit.circlePts(0.066, null, null, 8), taken, field, at);
    kit.appear(dot, tSeven + 1.6 * c / FIELD.cols, null, 0.1);
  });
  parts.vanish(field, tReached - 0.5, 0.35);
  cues.push({ t: tTwelve, type: 'swoosh', dur: 1.7 }, { t: tSeven, type: 'swoosh', dur: 1.7, pitch: 0.8 });
  const all = kit.text('count-all', '1,200', 0.8, kit.material(kit.PAPER), st.front, [1.1, 2.3]);
  const some = kit.text('count-some', '700', 0.8, kit.material(kit.CORAL), st.front, [6.1, 2.3]);
  kit.appear(all, tTwelve + 0.4, tReached - 0.6, 0.3);
  kit.appear(some, tSeven + 0.4, tReached - 0.6, 0.3);

  // ------------------------------------------------------------ one of Hugging Face's main systems
  const hf = parts.building('hf', st.back, HF, { w: 6.6, h: 4.6, label: 'Hugging Face', rows: 4, seed: 5 });
  kit.pop(hf.root, tReached - 0.1, 1.0, 0.45, tKept - 0.5);
  const main = parts.computer('main', st.props, [HF[0], HF[1] + 0.2], { w: 1.8, h: 2.6, rows: 4, also: kit.CORAL });
  kit.pop(main.root, tReached + 0.3, 1.0, 0.4, tKept - 0.5);
  for (const lamp of main.others) kit.appear(lamp, tReached + 0.9, null, 0.2);
  const reached = kit.ring('reached', st.front, [HF[0], HF[1] + 0.2], 1.6, kit.CORAL, 0.1);
  kit.flash(reached, tReached + 0.9, 0.9, 0.4);
  kit.flash(reached, tReached + 1.7, 0.9, 0.4);
  cues.push({ t: tReached - 0.1, type: 'pop', pitch: 0.6 }, { t: tReached + 0.9, type: 'tick', pitch: 0.45, gain: 1.5 });

  // ------------------------------------------------------------ the record, and three people from outside who read it
  const board = parts.board('board', st.props, ARCHIVE, { scale: 0.52 });
  kit.pop(board.root, tKept, 0.52, 0.5);
  cues.push({ t: tKept, type: 'pop', pitch: 0.7 });
  [[1.9, 2.3], [2.3, 0.6], [1.7, -1.1]].forEach((at, k) => {
    const written = parts.thought(`thinking${k}`, st.front, [ARCHIVE[0] + at[0], ARCHIVE[1] + at[1]], 1.5, 0.95, [-1, -0.6]);
    parts.writing(`thinking${k}-lines`, written.root, [0, 0], 3, 1.0, 70 + k);
    kit.pop(written.root, tThinking + 0.25 * k, 1.0, 0.35);
    cues.push({ t: tThinking + 0.25 * k, type: 'pop', pitch: 0.9 + 0.1 * k });
  });
  const READERS = [
    [4.4, { coat: '#c2557a', coatDeep: '#8e3a57', hair: '#3b2a26' }], [5.9, { coat: '#c28a3f', coatDeep: '#8f6229', hair: '#1c1c28' }],
    [7.4, { coat: '#5566c2', hair: '#d8d2c4' }],
  ];
  READERS.forEach(([x, look], k) => {
    const made = kit.person(`reader${k}`, st.cast, [x, GROUND + 4.3 * 0.42], 0.42, { facing: -1, ...look });
    kit.pop(made.root, tThree + 0.2 * k, 0.42, 0.4);
    const copy = parts.sheet(`copy${k}`, st.front, [0, 0], { scale: 0.62, seed: 180 + k });
    const t = tThree + 1.0 + 0.4 * k;
    parts.send(copy.root, [[ARCHIVE[0] + 1.8, ARCHIVE[1] + 0.4], [x - 1.6, 1.6], [x - 0.5, GROUND + 4.3 * 0.42 - 0.75]], t, t + 1.0, { size: 0.62, stay: true });
    kit.key(made.arm, 'rot', fr(t + 0.6), 0.0);
    kit.key(made.arm, 'rot', fr(t + 1.0), -0.55);
    cues.push({ t: tThree + 0.2 * k, type: 'pop', pitch: 0.8 + 0.1 * k }, { t: t + 1.0, type: 'tick', pitch: 1.1 + 0.1 * k });
  });

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [0, 0.2, 20.5]], [tOpenAI - 0.3, [0.1, 0.2, 19.6]], [tOpenAI + 1.4, [0.3, 0.4, 21]], [tReached, [0.35, 0.4, 20.8]],
    [tKept, [0.3, 0.3, 20.6]], [end, [0.35, 0.2, 20.2]],
  ]), 1.0);
  return cues;
}
