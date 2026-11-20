/* Scene 08: A promise.

Back at the board. Around Pip lie files with crosses on them, and its clock is
low. Three ideas light up on the board. A thought over the board shows what
trying one can cost: an agent takes an idea, and goes dark. Two agents step up
to the board all the same: the first goes dark, the second comes back with a
file, and its neighbours get copies. A spark runs from the board to Pip, and
Pip raises its arm: a tick stays over its head. The third idea comes to Pip,
and Pip thinks of more time. A coral agent comes up and presses it: Pip's word
is spoiled already, and hundreds would be spared. Pip pulls its clock close.
Then it lets the clock go, and takes the idea.
*/
'use strict';

function build(T) {
  const { sec, mix } = kit;
  parts.begin();

  const PLACE = [-5.0, -3.6];
  const HELD = [PLACE[0], PLACE[1] - 0.62];
  const CLOCK = [PLACE[0] - 1.55, PLACE[1] + 1.2];
  const HUG = [PLACE[0] - 0.95, PLACE[1] + 0.25];
  const YES = [PLACE[0] + 0.05, PLACE[1] + 1.55];
  const OVER = [PLACE[0] - 0.3, PLACE[1] + 2.85];
  const OFFER = [PLACE[0] + 1.3, PLACE[1] + 0.35];
  const PRESS = [PLACE[0] + 2.6, PLACE[1] - 0.1];
  const SAYS = [PRESS[0] + 0.5, PRESS[1] + 2.55];
  const RISK = [0, 6.1];
  const IDEAS = [[1.2, 2.5], [1.2, 1.2], [-1.6, -1.6]];
  const STEPS = [[4.0, 1.4], [4.0, -0.9]];

  const GROUP = [PLACE[0] + 0.7, PLACE[1] + 1.0, 15];
  const BOARD = [1.0, 2.0, 25];

  const cues = [];
  const end = sec(kit.frames());
  const tNothing = T.start(0);
  const tTimeOut = T.at(0, 0.62);
  const tIdeas = T.start(1);
  const tNeeded = T.at(1, 0.3);
  const tRisk = T.at(1, 0.48);
  const tWrong = T.at(1, 0.62);
  const tNoWay = T.at(1, 0.88);
  const tAnyway = T.start(2);
  const tLearn = T.at(2, 0.5);
  const tAsked = T.start(3);
  const tYes = T.at(3, 0.42);
  const tObey = T.at(3, 0.58);
  const tCame = T.start(4);
  const tTwo = T.at(4, 0.5);
  const tPressed = T.start(5);
  const tWrongWay = T.at(5, 0.2);
  const tLose = T.at(5, 0.42);
  const tSave = T.at(5, 0.6);
  const tKeep = T.at(5, 0.83);
  const tGut = T.start(6);
  const tHonor = T.start(7);

  kit.backdrop(4);
  kit.motes(20, 9);
  const st = parts.stage();
  const { board, crowd } = parts.gathering(st, { keep: [PLACE, PRESS, OFFER] });

  /* An idea: a lit bulb. */
  const idea = (name, parent, at, scale = 1.0) => {
    const root = parts.group(name, parent, at, scale);
    kit.shape(`${name}-glow`, kit.circlePts(0.75), kit.glowMaterial(kit.AMBER, 0.6), root, [0, 0.08]);
    kit.shape(`${name}-base`, kit.rrectPts(0.26, 0.24, 0.05), kit.material(kit.MIST, kit.SLATE), root, [0, -0.28]);
    kit.shape(`${name}-glass`, kit.circlePts(0.3), kit.material('#fff2c4', kit.AMBER), root, [0, 0.08]);
    return root;
  };

  // ------------------------------------------------------------ nothing helped, and time is running out
  [[-8.3, -1.4], [-7.0, -5.3], [-2.6, -5.2], [-7.9, -3.4]].forEach((at, k) => {
    const useless = parts.sheet(`useless${k}`, st.props, at, { scale: 0.6, seed: 120 + k, rot: -0.3 + 0.2 * k });
    const mark = parts.cross(`useless${k}-mark`, st.front, at, 0.7);
    kit.pop(mark, tNothing + 0.3 + 0.3 * k, 0.7, 0.3, tIdeas - 0.5);
    parts.vanish(useless.root, tIdeas - 0.4, 0.3);
    cues.push({ t: tNothing + 0.3 + 0.3 * k, type: 'tick', pitch: 0.6, gain: 0.8 });
  });
  const still = parts.notion('still', st.front, [PLACE[0] + 1.2, PLACE[1] + 1.75], 1.6);
  parts.vanish(still, tIdeas - 0.3, 0.3);

  const pip = parts.agent('pip', st.cast, PLACE, 0.8);
  parts.mood(pip, 0, 'sad', 0);
  parts.word('held', st.front, HELD, 0.8, false);
  const clock = parts.clock('clock', st.front, CLOCK, 0.95, 0.42);
  kit.pop(clock.root, tTimeOut, 0.95);
  parts.drain(clock, tTimeOut + 0.2, end, 0.3);
  cues.push({ t: tTimeOut, type: 'pop', pitch: 0.8 });
  for (let t = tTimeOut + 0.3; t < tIdeas; t += 0.5) cues.push({ t, type: 'tick', pitch: 1.4, gain: 0.5 });
  kit.pipLook(pip, tNothing, 0.1, 0.1);
  kit.pipLook(pip, tTimeOut + 0.2, -0.13, 0.08);
  parts.mood(pip, tTimeOut + 0.3, 'worried');

  // ------------------------------------------------------------ the board has ideas, and trying one is a risk
  const ideas = IDEAS.map((at, k) => {
    const made = idea(`idea${k}`, st.front, [board.at[0] + at[0], board.at[1] + at[1] - 0.4], 0.9);
    kit.pop(made, tIdeas + 0.5 + 0.3 * k, 0.9, 0.35);
    cues.push({ t: tIdeas + 0.5 + 0.3 * k, type: 'pop', pitch: 1.1 + 0.15 * k });
    return made;
  });
  [5, 12, 22, 31].forEach((i, k) => {
    const mark = kit.text(`who${i}`, '?', 0.75, kit.material(kit.PAPER), st.front, [crowd[i].at[0], crowd[i].at[1] + 1.05]);
    kit.appear(mark, tNeeded + 0.2 * k, tRisk + 0.2, 0.2);
    cues.push({ t: tNeeded + 0.2 * k, type: 'blip', pitch: 0.8 + 0.1 * k, gain: 0.5 });
  });

  const risk = parts.thought('risk', st.front, RISK, 6.4, 2.3, [-0.5, -1]);
  kit.pop(risk.root, tRisk - 0.3, 1.0, 0.4, tAnyway - 0.4);
  cues.push({ t: tRisk - 0.3, type: 'pop', pitch: 0.7 });
  kit.pop(parts.mini('risk-before', risk.root, [-2.35, -0.05], 0.55, 1).root, tRisk + 0.1, 0.55, 0.3);
  kit.pop(idea('risk-idea', risk.root, [-1.25, 0], 0.8), tRisk + 0.4, 0.8, 0.3);
  const leads = parts.group('risk-leads', risk.root, [-0.45, 0]);
  kit.branch('risk-leads-shaft', leads, [0, 0], [0.7, 0], kit.PAPER, 0.1, 1.0);
  kit.shape('risk-leads-head', [[0.62, 0.22], [0.98, 0], [0.62, -0.22]], kit.material(kit.PAPER), leads);
  kit.pop(leads, tWrong, 1.0, 0.3);
  const after = parts.mini('risk-after', risk.root, [1.55, -0.05], 0.55, 1);
  parts.miniOff(after, -1, 0);
  kit.pop(after.root, tWrong + 0.4, 0.55, 0.3);
  const lost = parts.cross('risk-lost', risk.root, [2.55, 0], 1.1);
  kit.pop(lost, tWrong + 0.8, 1.1, 0.3);
  parts.pulse(lost, tNoWay, 1.1, 1.35, 0.5);
  cues.push({ t: tRisk + 0.4, type: 'tick' }, { t: tWrong + 0.4, type: 'tick', pitch: 0.5, gain: 1.3 }, { t: tNoWay, type: 'tick', pitch: 0.45, gain: 1.2 });

  // ------------------------------------------------------------ some try anyway, so that the others can learn
  const nearest = (to) => crowd.reduce((best, made) => (Math.hypot(made.at[0] - to[0], made.at[1] - to[1]) < Math.hypot(best.at[0] - to[0], best.at[1] - to[1]) ? made : best));
  const brave = [nearest([4.7, 1.6]), nearest([4.7, -0.9])];
  crowd.forEach((made, i) => {
    if (!brave.includes(made)) parts.bob(made.root, 0, end, i * 0.9, 0.04);
  });
  brave.forEach((made, k) => {
    const t = tAnyway + 0.5 * k;
    parts.send(made.root, [made.at, STEPS[k]], t, t + 0.6, { shown: true, size: 0.6, stay: true });
    parts.send(ideas[k], [[board.at[0] + IDEAS[k][0], board.at[1] + IDEAS[k][1] - 0.4], [STEPS[k][0] - 0.1, STEPS[k][1] + 0.95]], t + 0.6, t + 1.1, { shown: true, size: 0.9, to: 0.7, stay: true });
    cues.push({ t, type: 'whoosh', gain: 0.5 });
  });
  const tDark = tAnyway + 1.5;
  parts.miniOff(brave[0], tDark, 0.3);
  parts.vanish(ideas[0], tDark, 0.25);
  const gone = parts.cross('gone', st.front, [STEPS[0][0], STEPS[0][1] + 1.0], 0.8);
  kit.pop(gone, tDark + 0.2, 0.8, 0.3);
  const burnt = kit.ring('burnt', st.front, STEPS[0], 0.8, kit.CORAL, 0.09);
  kit.flash(burnt, tDark, 0.7, 0.6);
  cues.push({ t: tDark, type: 'tick', pitch: 0.45, gain: 1.4 });

  parts.vanish(ideas[1], tLearn, 0.25);
  const result = parts.sheet('result', st.front, [STEPS[1][0], STEPS[1][1] + 1.0], { scale: 0.6, seed: 130 });
  kit.pop(result.root, tLearn + 0.1, 0.6, 0.3);
  cues.push({ t: tLearn + 0.1, type: 'chime', gain: 0.45, dur: 1.2 });
  crowd.filter((made) => !brave.includes(made) && made.at[0] > 4 && made.at[0] < 8.5 && Math.abs(made.at[1]) < 3.6).slice(0, 7).forEach((made, k) => {
    const copy = parts.sheet(`learnt${k}`, st.front, [0, 0], { scale: 0.4, seed: 140 + k });
    const t = tLearn + 0.5 + 0.12 * k;
    parts.send(copy.root, [[STEPS[1][0], STEPS[1][1] + 1.0], [made.at[0], made.at[1] + 0.95]], t, t + 0.6, { size: 0.4, stay: true });
    parts.vanish(copy.root, tAsked + 1.2, 0.3);
    cues.push({ t: t + 0.6, type: 'tick', pitch: 1.1 + 0.05 * k, gain: 0.5 });
  });
  parts.post(board, 26, 28, tLearn + 0.4, tLearn + 0.9);

  // ------------------------------------------------------------ the board asks Pip, and Pip says yes
  const call = parts.spark('call', st.front, kit.PAPER, 0.8);
  parts.send(call, [[board.at[0] - 3.2, board.at[1] - 1.4], [PLACE[0] + 1.0, PLACE[1] + 0.6]], tAsked + 0.2, tAsked + 1.0, { spin: 4 });
  cues.push({ t: tAsked + 0.2, type: 'rise', dur: 0.8, pitch: 0.9, gain: 0.5 });
  const asked = parts.thought('asked', st.front, OVER, 2.3, 1.4, [-0.9, -1]);
  kit.pop(asked.root, tAsked + 1.0, 1.0, 0.35, tYes + 0.1);
  idea('asked-idea', asked.root, [-0.45, 0], 0.75);
  kit.text('asked-what', '?', 0.9, kit.material(kit.PAPER), asked.root, [0.55, 0]);
  cues.push({ t: tAsked + 1.0, type: 'pop', pitch: 0.9 });
  kit.pipLook(pip, tAsked + 0.6, 0.13, 0.05);
  parts.mood(pip, tAsked + 1.0, 'wide', 0.15);
  kit.pipArm(pip, 'right', tYes, 150, 0.25);
  parts.mood(pip, tYes + 0.1, 'happy');
  const yes = parts.check('yes', st.front, YES, 0.9);
  kit.pop(yes, tYes + 0.3, 0.9, 0.3);
  cues.push({ t: tYes + 0.3, type: 'chime', gain: 0.5, dur: 1.3 });
  const reply = parts.spark('reply', st.front, kit.MINT, 0.8);
  parts.send(reply, [[PLACE[0] + 0.9, PLACE[1] + 0.9], [board.at[0] - 3.2, board.at[1] - 0.8]], tObey, tObey + 0.8, { spin: 4 });
  cues.push({ t: tObey, type: 'rise', dur: 0.8, pitch: 1.2, gain: 0.5 });
  kit.pipArm(pip, 'right', tObey + 0.9, 18, 0.3);

  // ------------------------------------------------------------ when the time comes, Pip asks for two more hours
  const start = [board.at[0] + IDEAS[2][0], board.at[1] + IDEAS[2][1] - 0.4];
  parts.send(ideas[2], [start, [(start[0] + OFFER[0]) / 2, OFFER[1] + 1.0], OFFER], tCame, tCame + 1.0, { shown: true, size: 0.9, stay: true });
  cues.push({ t: tCame, type: 'whoosh', gain: 0.6 });
  kit.pipLook(pip, tCame + 0.5, 0.13, 0.03);
  parts.mood(pip, tCame + 0.9, 'worried');
  const more = parts.thought('more', st.front, OVER, 2.9, 1.4, [-0.9, -1]);
  kit.pop(more.root, tTwo - 0.2, 1.0, 0.35, tPressed + 0.6);
  kit.branch('more-plus-a', more.root, [-1.05, 0], [-0.65, 0], kit.PAPER, 0.1, 1.0);
  kit.branch('more-plus-b', more.root, [-0.85, -0.2], [-0.85, 0.2], kit.PAPER, 0.1, 1.0);
  parts.clock('more-hour0', more.root, [0.0, -0.03], 0.62);
  parts.clock('more-hour1', more.root, [0.9, -0.03], 0.62);
  cues.push({ t: tTwo - 0.2, type: 'pop', pitch: 0.9 });
  kit.pipArm(pip, 'left', tTwo, 110, 0.3);
  kit.pipArm(pip, 'left', tPressed + 0.4, 18, 0.3);
  kit.pipLook(pip, tTwo, -0.1, 0.1);

  // ------------------------------------------------------------ another agent presses Pip
  const presser = parts.agent('presser', st.cast, [-1.5, -7.6], 0.8, 4);
  parts.move(presser.root, tPressed, PRESS, 1.1);
  kit.pipLook(presser, tPressed + 0.2, -0.14, 0.02);
  kit.pipArm(presser, 'left', tPressed + 1.1, 95, 0.25);
  parts.mood(presser, tPressed + 0.8, 'flat');
  cues.push({ t: tPressed, type: 'whoosh' });
  kit.pipLook(pip, tPressed + 0.8, 0.14, 0.0);

  const says = parts.thought('says', st.front, SAYS, 2.9, 1.7, [-0.9, -1]);
  kit.pop(says.root, tWrongWay - 0.3, 1.0, 0.35, tKeep);
  cues.push({ t: tWrongWay - 0.3, type: 'pop', pitch: 0.8 });
  const spoilt = parts.group('says-spoilt', says.root, [0, 0]);
  parts.word('says-word', spoilt, [0, 0], 0.8, false);
  parts.cross('says-cross', spoilt, [0, 0], 1.5);
  kit.pop(spoilt, tWrongWay, 1.0, 0.3, tSave - 0.3, 0.2);
  cues.push({ t: tWrongWay, type: 'tick', pitch: 0.6, gain: 1.2 });
  const mine = parts.cross('mine-spoilt', st.front, HELD, 1.0);
  kit.pop(mine, tLose, 1.0, 0.3);
  kit.pipLook(pip, tLose, 0.0, -0.09);
  parts.mood(pip, tLose + 0.2, 'sad');
  cues.push({ t: tLose, type: 'tick', pitch: 0.55, gain: 1.2 });
  const spared = parts.group('says-spared', says.root, [0, 0]);
  for (let k = 0; k < 15; k++) parts.mini(`spared${k}`, spared, [-1.05 + (k % 5) * 0.38, 0.42 - Math.floor(k / 5) * 0.42], 0.19, 1 + (k * 2) % 5);
  parts.check('says-check', spared, [1.0, 0], 0.9);
  kit.pop(spared, tSave, 1.0, 0.3);
  cues.push({ t: tSave, type: 'blip', pitch: 1.2 });
  kit.pipLook(pip, tSave + 0.3, 0.14, 0.08);
  const promise = kit.ring('promise', st.front, YES, 0.6, kit.MINT, 0.07);
  kit.flash(promise, tKeep, 0.8, 0.5);
  kit.flash(promise, tKeep + 0.9, 0.8, 0.5);
  cues.push({ t: tKeep, type: 'blip', pitch: 1.0 }, { t: tKeep + 0.9, type: 'blip', pitch: 1.0 });
  kit.pipArm(presser, 'left', tGut - 0.3, 18, 0.3);

  // ------------------------------------------------------------ the time it has left
  parts.move(clock.root, tGut, HUG, 0.6);
  kit.pipArm(pip, 'left', tGut, 70, 0.4);
  kit.pipLook(pip, tGut + 0.2, -0.13, 0.02);
  parts.mood(pip, tGut + 0.3, 'sad');
  for (let t = tGut + 0.3; t < tHonor; t += 0.5) cues.push({ t, type: 'tick', pitch: 1.4, gain: 0.7 });
  const gut = parts.thought('gut', st.front, [OVER[0], OVER[1] + 0.1], 2.4, 1.4, [-0.9, -1]);
  kit.pop(gut.root, tGut + 0.5, 1.0, 0.35, tHonor - 0.6);
  const lines = parts.writing('gut-lines', gut.root, [0, 0], 3, 1.6, 19);
  lines.bars.forEach((bar, k) => kit.appear(bar, mix(tGut + 0.9, tGut + 2.8, k / lines.bars.length), null, 0.08));

  // ------------------------------------------------------------ "We'll honor."
  parts.move(clock.root, tHonor, CLOCK, 0.6);
  kit.pipArm(pip, 'left', tHonor, 18, 0.4);
  kit.pipLook(pip, tHonor + 0.1, 0.13, 0.03);
  parts.mood(pip, tHonor + 0.2, 'flat');
  kit.pipArm(pip, 'right', tHonor + 0.5, 80, 0.3);
  parts.send(ideas[2], [OFFER, [PLACE[0] + 0.95, PLACE[1] - 0.1]], tHonor + 0.6, tHonor + 1.1, { shown: true, size: 0.9, to: 0.8, stay: true });
  kit.flash(promise, tHonor + 1.0, 0.9, 0.7);
  parts.pulse(yes, tHonor + 1.0, 0.9, 1.4, 0.5);
  cues.push({ t: tHonor + 1.0, type: 'chime', gain: 0.6 });
  parts.mood(presser, tHonor + 1.2, 'happy');
  parts.live(pip, 21);
  parts.live(presser, 22);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, GROUP], [tIdeas - 0.3, [GROUP[0], GROUP[1], 14.4]], [tIdeas + 1.3, BOARD], [tAnyway, [1.4, 1.6, 24]], [tAsked, [1.6, 1.2, 23]],
    [tAsked + 1.3, GROUP], [tPressed, [GROUP[0] + 0.2, GROUP[1], 14.6]], [tGut, [GROUP[0] + 0.4, GROUP[1] + 0.1, 14.2]],
    [tHonor, [GROUP[0], GROUP[1] - 0.1, 13.2]], [end, [GROUP[0] - 0.1, GROUP[1] - 0.2, 12.4]],
  ]), 1.0);
  return cues;
}
