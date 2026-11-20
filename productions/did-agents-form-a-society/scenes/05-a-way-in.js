/* Scene 05: A way in.

On the left, the board, with Pip and some of the group beside it. Pip sends a
spark off to look, and it comes to a building on the right, where people
bring boxes in: Hugging Face. Behind its glass are the records, and a padlock
snaps onto them. Pip posts a question on the board, and thinks of a key. A
blue agent goes out into the open ground between the two, where people walk
past and two keys lie among boxes; it takes the keys and posts them. The keys
do not open the padlock. Morning comes up behind the building. The blue agent
hands a parcel to a computer by the building's wall, and the computer passes
out a locked file. A violet agent does the same, and tells the board.
*/
'use strict';

function build(T) {
  const { fr, sec, key, alpha } = kit;
  parts.begin();

  const BOARD = [-9.6, 0.4];
  const PIP = [-4.6, -2.5];
  const HELD = [PIP[0], PIP[1] - 0.7];
  const HF = [8.6, -0.5];
  const RECORDS = [8.6, -0.1];
  const GROUND = -3.3;
  const MACHINE = [3.6, -1.95];
  const KEYS = [[1.5, -3.0], [2.15, -3.12]];
  const B_HOME = [-3.2, 0.5];
  const B_OPEN = [0.3, -2.2];
  const B_WALL = [1.7, -1.5];
  const C_HOME = [-3.0, 2.7];
  const C_WALL = [1.5, -3.4];
  const POSTS = [[-11.7, 2.55], [-11.7, 1.85], [-11.7, 1.15]];

  const LEFT = [-6.5, 0.0, 19.5];
  const MID = [0.4, -0.9, 19];
  const RIGHT = [7.5, -0.3, 19];
  const TRICK = [3.2, -2.0, 13.8];

  const cues = [];
  const end = sec(kit.frames());
  const tKnow = T.start(0);
  const tNoOne = T.at(0, 0.2);
  const tLooking = T.at(0, 0.3);
  const tFound = T.at(0, 0.52);
  const tKept = T.at(0, 0.64);
  const tPeople = T.at(0, 0.8);
  const tLocked = T.start(1);
  const tAsk = T.at(1, 0.36);
  const tKey = T.at(1, 0.62);
  const tWent = T.start(2);
  const tKeys = T.at(2, 0.16);
  const tOpen = T.at(2, 0.5);
  const tPosted = T.at(2, 0.82);
  const tNotOpen = T.start(3);
  const tKept2 = T.at(3, 0.24);
  const tMorning = T.at(3, 0.38);
  const tWay = T.at(3, 0.52);
  const tTrick = T.at(3, 0.66);
  const tSecond = T.start(4);
  const tTold = T.at(4, 0.6);

  kit.backdrop(6, kit.SKY_DEEP);
  kit.motes(22, 13);
  const st = parts.stage();

  // ------------------------------------------------------------ morning, the open ground, and Hugging Face
  const dawn = kit.shape('dawn', kit.circlePts(11, null, 6.5), kit.glowMaterial(kit.AMBER, 0.42, 1.4), st.back, [7.5, -5.2]);
  alpha(dawn, 1, 0.0);
  alpha(dawn, fr(tMorning - 0.3), 0.0);
  alpha(dawn, fr(tMorning + 2.6), 1.0);
  cues.push({ t: tMorning, type: 'rise', dur: 2.2, pitch: 0.5, gain: 0.5 });

  // Two people walk across the open ground, behind everything else. They wait out of sight until then.
  const street = kit.layer('street', 0.6, { sharp: true });
  const walkers = [
    kit.person('walker0', street, [-30, GROUND + 0.9 + 4.3 * 0.36], 0.36, { coat: '#3f9b8f', coatDeep: '#2c6f66', hair: '#1c1c28' }),
    kit.person('walker1', street, [-30, GROUND + 0.7 + 4.3 * 0.36], 0.36, { coat: '#c2557a', coatDeep: '#8e3a57', hair: '#8a5a2b' }),
  ];
  walkers.forEach((made, k) => {
    parts.move(made.root, tOpen - 1.6 + 0.9 * k, [-8.4, made.root.y], 0.03);
    parts.move(made.root, tOpen - 1.5 + 0.9 * k, [16.5, made.root.y], 10.5);
  });

  const hf = parts.building('hf', st.back, HF, { w: 7.4, h: 4.8, label: 'Hugging Face', rows: 4, seed: 5 });
  kit.branch('wire', st.back, [MACHINE[0] + 0.7, MACHINE[1] + 0.4], [HF[0] - 3.7, MACHINE[1] + 0.4], kit.MIST, 0.1, 0.6);
  const rnd = new kit.Random(31);
  for (let k = 0; k < 7; k++) {
    const x = -1.9 + k * 0.85 + rnd.random() * 0.3;
    if (k % 3 === 2) parts.sheet(`litter${k}`, st.props, [x, GROUND + 0.2], { scale: 0.5, seed: k, rot: -0.3 + rnd.random() * 0.6 });
    else kit.shape(`litter${k}`, kit.rrectPts(0.5 + rnd.random() * 0.3, 0.4 + rnd.random() * 0.25, 0.06), kit.material([kit.SLATE, kit.INK500, kit.MIST][k % 3], kit.INK600), st.props, [x, GROUND + 0.22]);
  }
  const found = KEYS.map((at, k) => parts.doorKey(`key${k}`, st.props, at, 0.95, k ? 0.5 : -0.25));

  const machine = parts.computer('machine', st.props, MACHINE, { w: 1.7, h: 2.5, rows: 3, also: kit.CORAL });
  parts.flicker(machine.lamps, 0, null, 5);

  kit.shape('records-back', kit.rrectPts(2.6, 1.9, 0.2), kit.material(kit.INK900, null, 0.9, { over: kit.INK800 }), st.props, RECORDS);
  [-0.6, 0, 0.6].forEach((dx, k) => parts.sheet(`record${k}`, st.props, [RECORDS[0] + dx, RECORDS[1] + 0.05 * (k % 2)], { scale: 0.85, seed: 40 + k, rot: -0.12 * dx }));
  const padlock = parts.lock('padlock', st.front, [RECORDS[0], RECORDS[1] - 0.1], 1.5);
  kit.pop(padlock.root, tLocked + 0.1, 1.5, 0.3);
  cues.push({ t: tLocked + 0.1, type: 'tick', pitch: 0.5, gain: 1.4 });
  const shut = kit.ring('shut', st.front, RECORDS, 1.1, kit.CORAL, 0.09);
  kit.flash(shut, tLocked + 0.2, 0.8, 0.5);

  const staff = [
    kit.person('staff0', st.cast, [HF[0] - 2.3, GROUND + 4.3 * 0.4], 0.4, { facing: 1 }),
    kit.person('staff1', st.cast, [16.8, GROUND + 4.3 * 0.4], 0.4, { coat: '#c28a3f', coatDeep: '#8f6229', hair: '#d8d2c4', facing: -1 }),
  ];
  kit.shape('staff1-box', kit.rrectPts(0.95, 0.8, 0.1), kit.material(kit.AMBER, kit.AMBER_DEEP), staff[1].root, [-1.0, -1.55]);
  parts.move(staff[1].root, tKept, [HF[0] + 2.2, staff[1].root.y], 3.2);
  key(staff[0].arm, 'rot', fr(tPeople), 0.0);
  key(staff[0].arm, 'rot', fr(tPeople + 0.5), 1.9);
  key(staff[0].arm, 'rot', fr(tPeople + 1.6), 1.9);
  key(staff[0].arm, 'rot', fr(tPeople + 2.1), 0.0);
  const shelved = parts.group('shelved', st.front, [HF[0] - 1.9, GROUND + 1.0]);
  kit.shape('shelved-box', kit.rrectPts(0.36, 0.3, 0.05), kit.material(kit.SKY, kit.SKY_DEEP), shelved);
  parts.send(shelved, [[HF[0] - 1.9, GROUND + 1.3], [HF[0] - 1.6, HF[1] + 0.2]], tPeople + 0.5, tPeople + 1.3, { stay: true });
  cues.push({ t: tPeople + 1.3, type: 'tick', pitch: 0.9 });

  // ------------------------------------------------------------ the board, some of the group, and Pip
  const board = parts.board('board', st.props, BOARD, { scale: 0.8 });
  const CROWD = [[-6.0, 2.9], [-6.1, 1.0], [-5.9, -0.9], [-4.5, 1.9], [-11.9, -3.6], [-10.3, -3.85], [-8.7, -3.6], [-7.1, -3.85], [-12.9, 3.9], [-13.3, 1.8], [-13.2, -0.4], [-13.3, -2.3]];
  const crowd = parts.crowd('agent', st.cast, CROWD, 0.6, 21);
  crowd.forEach((made, i) => parts.bob(made.root, 0, end, i * 0.9, 0.04));

  const pip = parts.agent('pip', st.cast, PIP, 0.9);
  parts.mood(pip, 0, 'flat', 0);
  parts.word('held', st.front, HELD, 0.85, false);
  const wonder = parts.notion('wonder', st.front, [PIP[0] + 0.95, PIP[1] + 1.55], 1.5);
  const what = kit.text('what', '?', 0.7, kit.material(kit.PAPER), st.front, [PIP[0] + 2.0, PIP[1] + 1.85]);
  kit.pop(wonder, tKnow, 1.5, 0.35, tLooking - 0.1);
  kit.appear(what, tKnow + 0.3, tLooking - 0.2, 0.2);
  cues.push({ t: tKnow, type: 'pop', pitch: 0.8 });
  kit.pipLook(pip, tKnow, 0.1, 0.12);
  [0, 2, 3, 6].forEach((i, k) => {
    const mark = kit.text(`shrug${i}`, '?', 0.6, kit.material(kit.PAPER), st.front, [CROWD[i][0] + 0.1, CROWD[i][1] + 1.05]);
    kit.appear(mark, tNoOne + 0.15 * k, tLooking + 0.1 * k, 0.2);
    cues.push({ t: tNoOne + 0.15 * k, type: 'tick', pitch: 0.8 + 0.1 * k, gain: 0.6 });
  });

  // ------------------------------------------------------------ Pip goes looking, and finds the records
  const search = parts.spark('search', st.front, kit.MINT, 0.9);
  const hover = [RECORDS[0] - 1.9, RECORDS[1] + 1.2];
  kit.pipArm(pip, 'right', tLooking, 85, 0.25);
  parts.send(search, [[PIP[0] + 1.2, PIP[1] - 0.2], [-2.0, 0.6], [0.4, -1.3], [3.2, 1.3], [5.6, 0.4], hover], tLooking + 0.2, tFound + 0.4, { spin: 4, stay: true });
  cues.push({ t: tLooking + 0.2, type: 'rise', dur: 1.2, pitch: 1.1, gain: 0.5 });
  kit.pipArm(pip, 'right', tLooking + 1.0, 18, 0.4);
  kit.pipLook(pip, tLooking + 0.3, 0.14, 0.03);
  const there = kit.ring('there', st.front, RECORDS, 1.3, kit.MINT, 0.08);
  kit.flash(there, tFound + 0.4, 0.9, 0.3);
  cues.push({ t: tFound + 0.4, type: 'chime', gain: 0.5, dur: 1.4 });
  cues.push({ t: tKept + 0.5, type: 'blip', pitch: 0.9 });
  parts.send(search, [hover, [RECORDS[0] - 0.4, RECORDS[1] + 0.3], [RECORDS[0] - 1.6, RECORDS[1] - 1.3], [RECORDS[0] - 1.9, GROUND]], tLocked + 0.3, tLocked + 1.3,
    { shown: true, to: 0.3, ease: (q) => q * q });

  // ------------------------------------------------------------ a question for the board: has anyone a key?
  const ask = parts.folder('ask', st.front, POSTS[0], { scale: 0.7, word: 'ASK', bars: [0.6, 0.9], tail: 0.9 });
  parts.doorKey('ask-key', ask.root, [ask.tail + 0.5, -0.03], 0.75);
  const post = parts.spark('post', st.front, kit.MINT, 0.8);
  kit.pipArm(pip, 'left', tAsk, 95, 0.25);
  parts.send(post, [[PIP[0] - 1.1, PIP[1]], [-7.5, 2.0], POSTS[0]], tAsk + 0.2, tAsk + 1.0, { spin: 4 });
  kit.pop(ask.root, tAsk + 1.0, 0.7, 0.35);
  cues.push({ t: tAsk + 0.2, type: 'rise', dur: 0.8, pitch: 1.2, gain: 0.5 }, { t: tAsk + 1.0, type: 'pop', pitch: 1.2 });
  kit.pipArm(pip, 'left', tAsk + 1.0, 18, 0.3);
  const wish = parts.thought('wish', st.front, [PIP[0] + 2.1, PIP[1] + 2.2], 2.5, 1.5, [-1, -1]);
  kit.pop(wish.root, tKey, 1.0, 0.4, tWent + 0.6);
  parts.doorKey('wish-key', wish.root, [-0.35, 0], 1.3);
  kit.text('wish-what', '?', 0.9, kit.material(kit.PAPER), wish.root, [0.8, 0.0]);
  cues.push({ t: tKey, type: 'pop', pitch: 0.9 });
  kit.pipLook(pip, tAsk, -0.13, 0.08);
  kit.pipLook(pip, tKey + 0.3, 0.1, 0.1);

  // ------------------------------------------------------------ agents go looking, and one finds keys lying in the open
  [[0, [-1.0, 4.2]], [1, [0.5, 1.5]], [4, [-6.0, -4.6]], [3, [2.5, 3.6]]].forEach(([i, to], k) => {
    const scout = parts.spark(`scout${i}`, st.front, parts.body(crowd[i].which)[0], 0.7);
    const from = CROWD[i];
    parts.send(scout, [from, [(from[0] + to[0]) / 2, from[1] + 1.2], to], tWent + 0.12 * k, tWent + 1.6 + 0.2 * k, { spin: 4, to: 0.2 });
    cues.push({ t: tWent + 0.12 * k, type: 'blip', pitch: 0.8 + 0.1 * k, gain: 0.5 });
  });
  const b = parts.agent('b', st.cast, B_HOME, 0.85, 1);
  parts.move(b.root, tWent + 0.2, B_OPEN, 1.5);
  kit.pipLook(b, tWent + 0.4, 0.13, -0.04);
  kit.pipLook(b, tKeys, 0.12, -0.1);
  parts.mood(b, tKeys + 0.2, 'wide', 0.15);
  const glint = kit.ring('glint', st.front, [1.8, -3.05], 0.75, kit.PAPER, 0.06);
  kit.flash(glint, tKeys + 0.2, 0.8, 0.5);
  kit.flash(glint, tKeys + 1.1, 0.8, 0.5);
  cues.push({ t: tKeys + 0.2, type: 'chime', gain: 0.45, pitch: 1.3, dur: 1.2 });
  const mine = [[B_OPEN[0] + 0.55, B_OPEN[1] - 0.75], [B_OPEN[0] + 1.05, B_OPEN[1] - 0.6]];
  found.forEach((made, k) => {
    parts.send(made.root, [KEYS[k], mine[k]], tOpen + 1.2 + 0.2 * k, tOpen + 1.8 + 0.2 * k, { shown: true, size: 0.95, to: 0.8, stay: true });
    cues.push({ t: tOpen + 1.8 + 0.2 * k, type: 'tick', pitch: 1.3 });
  });
  kit.pipArm(b, 'right', tOpen + 1.0, 60, 0.3);
  parts.mood(b, tOpen + 1.8, 'glad');
  const told = parts.folder('told', st.front, POSTS[1], { scale: 0.7, which: 1, bars: [0.7, 0.5], tail: 1.5 });
  parts.doorKey('told-key0', told.root, [told.tail + 0.5, -0.03], 0.7);
  parts.doorKey('told-key1', told.root, [told.tail + 1.25, -0.03], 0.7);
  const news = parts.spark('news', st.front, kit.SKY, 0.8);
  parts.send(news, [[B_OPEN[0] - 0.9, B_OPEN[1] + 0.3], [-5.0, 2.6], POSTS[1]], tPosted, tPosted + 1.1, { spin: 4 });
  kit.pop(told.root, tPosted + 1.1, 0.7, 0.35);
  cues.push({ t: tPosted, type: 'rise', dur: 1.0, pitch: 1.0, gain: 0.5 }, { t: tPosted + 1.1, type: 'pop', pitch: 1.1 });
  kit.pipArm(b, 'right', tPosted + 0.3, 18, 0.3);
  parts.mood(b, tPosted + 1.2, 'happy');

  // ------------------------------------------------------------ the keys do not open the records
  const tried = [0, 1].map((k) => parts.doorKey(`tried${k}`, st.front, [0, 0], 0.9));
  tried.forEach((made, k) => {
    const at = [RECORDS[0] - 0.75 - 0.5 * k, RECORDS[1] - 0.25 + 0.5 * k];
    parts.send(made.root, [mine[k], [4.5, 1.2], at], tNotOpen + 0.1 + 0.15 * k, tNotOpen + 1.3 + 0.15 * k, { size: 0.9, stay: true });
    parts.shake(made.root, tNotOpen + 1.5 + 0.15 * k, 0.5, 0.12);
    parts.send(made.root, [at, [at[0] - 0.4, GROUND]], tNotOpen + 2.2 + 0.1 * k, tNotOpen + 2.8 + 0.1 * k, { shown: true, size: 0.9, to: 0.3, ease: (q) => q * q });
  });
  for (const made of found) parts.vanish(made.root, tNotOpen + 0.1, 0.15);
  parts.shake(padlock.root, tNotOpen + 1.5, 0.5, 0.05);
  kit.flash(shut, tNotOpen + 1.6, 0.8, 0.5);
  cues.push({ t: tNotOpen + 1.5, type: 'tick', pitch: 0.5, gain: 1.3 }, { t: tNotOpen + 1.7, type: 'tick', pitch: 0.45, gain: 1.1 });
  parts.mood(b, tNotOpen + 1.8, 'flat');

  // ------------------------------------------------------------ the same agent keeps trying, and by morning finds another way in
  parts.move(b.root, tKept2 - 0.3, B_WALL, 1.4);
  const attempt = parts.spark('attempt', st.front, kit.SKY, 0.8);
  const refused = kit.ring('refused', st.front, [HF[0], HF[1] - 1.9], 0.6, kit.CORAL, 0.08);
  [tKept2 + 1.2, tMorning + 0.2].forEach((t, k) => {
    parts.send(attempt, [[B_WALL[0] + 1.0, B_WALL[1]], [5.0, 1.0 - k], [HF[0], HF[1] - 1.9]], t, t + 0.7, { spin: 4 });
    kit.flash(refused, t + 0.7, 0.5, 0.6);
    cues.push({ t, type: 'rise', dur: 0.6, pitch: 1.2, gain: 0.4 }, { t: t + 0.7, type: 'tick', pitch: 0.6 });
  });
  kit.pipLook(b, tWay - 0.2, 0.14, -0.04);
  parts.mood(b, tWay, 'wide', 0.15);
  const noticed = kit.ring('noticed', st.front, MACHINE, 1.5, kit.SKY, 0.08);
  kit.flash(noticed, tWay, 0.9, 0.3);
  cues.push({ t: tWay, type: 'blip', pitch: 1.3 });

  // A parcel goes into the computer by the wall, and the computer passes a locked file out.
  const slot = [MACHINE[0] - 0.3, MACHINE[1] + 0.55];
  const trick = (who, hands, name, t, colour, deep) => {
    const parcel = parts.group(`${name}-parcel`, st.front, [0, 0], 0.001);
    kit.shape(`${name}-parcel-box`, kit.rrectPts(0.6, 0.5, 0.08), kit.material(colour, deep), parcel);
    kit.shape(`${name}-parcel-band`, kit.rrectPts(0.1, 0.5, 0), kit.material(kit.PAPER), parcel);
    kit.pipArm(who, 'right', t - 0.2, 80, 0.25);
    parts.send(parcel, [hands, [(hands[0] + slot[0]) / 2, hands[1] + 0.7], slot], t, t + 0.7, { to: 0.5 });
    for (const lamp of machine.others) {
      alpha(lamp, fr(t + 0.7), 0.0);
      alpha(lamp, fr(t + 0.9), 1.0);
      alpha(lamp, fr(t + 2.2), 1.0);
      alpha(lamp, fr(t + 2.5), 0.0);
    }
    const file = parts.sheet(`${name}-file`, st.front, [0, 0], { scale: 0.8, locked: true, seed: 60 + t });
    key(file.root, 'scale', 1, 0.001);
    parts.send(file.root, [[HF[0] - 3.7, MACHINE[1] + 0.4], [MACHINE[0] + 0.7, MACHINE[1] + 0.4], slot, [hands[0] + 0.25, hands[1] - 0.1]], t + 1.0, t + 2.1,
      { size: 0.8, stay: true });
    kit.pipArm(who, 'right', t + 2.2, 40, 0.3);
    parts.mood(who, t + 2.1, 'glad');
    cues.push({ t, type: 'whoosh', gain: 0.6 }, { t: t + 0.8, type: 'tick', pitch: 0.7 }, { t: t + 1.0, type: 'rise', dur: 1.0, pitch: 0.9, gain: 0.5 },
      { t: t + 2.1, type: 'chime', gain: 0.5, dur: 1.3 });
    return file;
  };
  trick(b, [B_WALL[0] + 0.95, B_WALL[1] - 0.3], 'b', tTrick + 0.2, kit.SKY, kit.SKY_DEEP);

  // ------------------------------------------------------------ a second agent tries it, and tells the board
  const c = parts.agent('c', st.cast, C_HOME, 0.85, 2);
  parts.move(c.root, tWay, C_WALL, 2.2);
  kit.pipLook(c, tWay + 0.5, 0.13, -0.03);
  trick(c, [C_WALL[0] + 0.95, C_WALL[1] - 0.3], 'c', tSecond - 0.5, kit.VIOLET, kit.VIOLET_DEEP);
  const worked = parts.check('worked', st.front, [C_WALL[0] + 0.2, C_WALL[1] + 1.55], 1.0);
  kit.pop(worked, tSecond + 1.7, 1.0, 0.3);
  const word2 = parts.folder('word2', st.front, POSTS[2], { scale: 0.7, which: 2, bars: [0.8, 0.5], tail: 0.8 });
  parts.sheet('word2-file', word2.root, [word2.tail + 0.4, -0.03], { scale: 0.5, locked: true, seed: 71 });
  const report = parts.spark('report', st.front, kit.VIOLET, 0.8);
  parts.send(report, [[C_WALL[0] - 0.9, C_WALL[1] + 0.4], [-4.5, 3.0], POSTS[2]], tTold - 0.3, tTold + 0.7, { spin: 4 });
  kit.pop(word2.root, tTold + 0.7, 0.7, 0.35);
  cues.push({ t: tTold - 0.3, type: 'rise', dur: 1.0, pitch: 1.0, gain: 0.5 }, { t: tTold + 0.7, type: 'pop', pitch: 1.0 });
  parts.post(board, 24, 28, tWent, tSecond);

  parts.live(pip, 9);
  parts.live(b, 10);
  parts.live(c, 11);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, LEFT], [tLooking + 0.3, LEFT], [tLooking + 2.2, MID], [tFound + 0.8, RIGHT], [tLocked + 1.2, RIGHT], [tAsk + 0.6, LEFT],
    [tWent + 0.2, LEFT], [tWent + 1.8, MID], [tPosted - 0.2, MID], [tPosted + 1.2, LEFT], [tNotOpen - 0.1, LEFT], [tNotOpen + 1.3, RIGHT],
    [tKept2 + 0.6, RIGHT], [tKept2 + 2.0, [5.0, -0.8, 19]], [tTrick - 0.4, [4.6, -1.0, 18.5]], [tTrick + 0.8, TRICK], [tTold - 0.5, TRICK],
    [tTold + 0.8, LEFT], [end, [LEFT[0] - 0.6, LEFT[1] + 0.3, LEFT[2] - 1.5]],
  ]), 1.0);
  return cues;
}
