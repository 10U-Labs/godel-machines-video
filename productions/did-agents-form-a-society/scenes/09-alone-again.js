/* Scene 09: Alone again.

The board is on the left with Pip beside it, Hugging Face is on the right, and
the group is spread between the two, sparks running both ways. In one instant
most of the agents go dark, the coral agent beside Pip among them, and so do
the three with flags, whose flags sink. Nothing more is posted on the board.
At Hugging Face a light starts to flash and two people come out; a shutter
comes down over the building, and the agents still lit are pushed back. The
key in Pip's hand goes dull. Close on Pip: no pass, no answer about the
scorer, dark agents on every side, a clock almost empty. The picture draws
back, and Pip is the one small light on its side of it.
*/
'use strict';

function build(T) {
  const { fr, sec, key, alpha } = kit;
  parts.begin();

  const BOARD = [-9.6, 0.4];
  const PIP = [-4.6, -2.5];
  const HELD = [PIP[0], PIP[1] - 0.7];
  const KEY = [PIP[0] + 1.05, PIP[1] - 0.25];
  const IDEA = [PIP[0] + 1.0, PIP[1] + 0.6];
  const CLOCK = [PIP[0] - 1.6, PIP[1] + 1.3];
  const PRESS = [-2.0, -2.7];
  const HF = [8.6, -0.5];
  const GROUND = -3.3;
  const MACHINE = [3.6, -1.95];
  const LEADS = [[2.6, 2.2, 1], [1.6, 0.1, 2], [2.4, -3.9, 3]];

  const ALL = [-0.5, -0.3, 27];
  const cues = [];
  const end = sec(kit.frames());
  const tStop = T.at(0, 0.56);
  const tLeaders = T.start(1);
  const tNotBack = T.at(1, 0.6);
  const tQuiet = T.start(2);
  const tFound = T.at(2, 0.2);
  const tDay = T.at(2, 0.52);
  const tKey = T.at(2, 0.8);
  const tNotPassed = T.start(3);
  const tNotFound = T.at(3, 0.22);
  const tGone = T.at(3, 0.55);
  const tAlmostUp = T.at(3, 0.8);
  const tAlone = T.start(4);

  kit.backdrop(6, kit.SKY_DEEP);
  kit.motes(22, 13);
  const st = parts.stage();

  // ------------------------------------------------------------ Hugging Face, which finds the break-in and shuts the agents out
  parts.building('hf', st.back, HF, { w: 7.4, h: 4.8, label: 'Hugging Face', rows: 4, seed: 5 });
  kit.branch('wire', st.back, [MACHINE[0] + 0.7, MACHINE[1] + 0.4], [HF[0] - 3.7, MACHINE[1] + 0.4], kit.MIST, 0.1, 0.6);
  const machine = parts.computer('machine', st.props, MACHINE, { w: 1.7, h: 2.5, rows: 3, lamp: kit.CORAL });
  parts.flicker(machine.lamps, 0, tDay, 5);
  for (const lamp of machine.lamps) alpha(lamp, fr(tDay + 0.3), 0.0);

  const alarm = kit.shape('alarm', kit.circlePts(1.6), kit.glowMaterial(kit.CORAL, 0.9, 1.3), st.front, [HF[0] + 3.0, HF[1] + 2.75]);
  kit.shape('alarm-lamp-base', kit.rrectPts(0.5, 0.2, 0.05), kit.material(kit.INK500), st.props, [HF[0] + 3.0, HF[1] + 2.62]);
  const lamp = kit.shape('alarm-lamp', kit.circlePts(0.2), kit.material(kit.CORAL), st.props, [HF[0] + 3.0, HF[1] + 2.85]);
  alpha(alarm, 1, 0.0);
  alpha(lamp, 1, 0.25);
  for (const f of kit.every(3, fr(tFound), fr(tKey + 1.5))) {
    const on = 0.5 + 0.5 * Math.sin((sec(f) - tFound) * 9);
    alpha(alarm, f, on);
    alpha(lamp, f, 0.25 + 0.75 * on);
  }
  alpha(alarm, fr(tKey + 1.6), 0.0);
  for (let t = tFound; t < tDay; t += 0.7) cues.push({ t, type: 'blip', pitch: 0.6, gain: 0.6 });

  const staff = [
    kit.person('staff0', st.cast, [17.0, GROUND + 4.3 * 0.4], 0.4, { facing: -1 }),
    kit.person('staff1', st.cast, [18.2, GROUND + 4.3 * 0.4], 0.4, { coat: '#c28a3f', coatDeep: '#8f6229', hair: '#d8d2c4', facing: -1 }),
  ];
  staff.forEach((made, k) => {
    parts.move(made.root, tFound + 0.2 + 0.5 * k, [HF[0] + 0.6 + 2.2 * k, made.root.y], 2.0);
    key(made.arm, 'rot', fr(tFound + 2.2 + 0.5 * k), 0.0);
    key(made.arm, 'rot', fr(tFound + 2.7 + 0.5 * k), -1.5);
  });

  const shutter = parts.group('shutter', st.front, [HF[0], 9.5]);
  kit.shape('shutter-slab', kit.rrectPts(7.0, 3.6, 0.12), kit.material(kit.INK800, kit.INK900), shutter);
  for (let r = 0; r < 7; r++) kit.shape(`shutter-rib${r}`, kit.rrectPts(6.7, 0.1, 0), kit.material(kit.INK500), shutter, [0, 1.5 - r * 0.5]);
  parts.lock('shutter-lock', shutter, [0, -1.25], 1.3);
  parts.move(shutter, tDay, [HF[0], HF[1] + 0.25], 0.5);
  parts.shake(shutter, tDay + 0.5, 0.3, 0.05);
  cues.push({ t: tDay, type: 'whoosh', pitch: 0.7 }, { t: tDay + 0.5, type: 'tick', pitch: 0.4, gain: 1.5 });

  // ------------------------------------------------------------ the board, the group, and the instant most of it stops
  const board = parts.board('board', st.props, BOARD, { scale: 0.8 });
  const posted = parts.post(board, 22, 28, 0.2, tStop - 0.3);
  posted.forEach((t, k) => cues.push({ t, type: 'tick', pitch: 1.0 + 0.05 * k, gain: 0.4 }));

  const rnd = new kit.Random(53);
  const spots = [];
  for (const x of [-13.4, -12.0, -10.6, -9.2, -7.8, -6.4]) spots.push([x, -3.75 - (spots.length % 2) * 0.4], [x + 0.3, 4.3 + (spots.length % 2) * 0.35]);
  spots.push([-5.9, 2.6], [-6.0, 0.9], [-5.8, -0.8], [-4.4, 1.8], [-4.3, 0.1]);
  const near = spots.length;
  for (let tries = 0; spots.length < near + 26 && tries < 4000; tries++) {
    const at = [-2.6 + rnd.random() * 6.8, -4.3 + rnd.random() * 7.8];
    const clear = [...spots.slice(near), ...LEADS, PRESS, MACHINE, [PIP[0] + 1.0, PIP[1]]].every(([x, y]) => Math.hypot(at[0] - x, at[1] - y) > 1.15);
    if (clear) spots.push(at);
  }
  for (let k = 0; k < 7; k++) spots.push([5.2 + k * 1.05, GROUND - 0.55 - (k % 2) * 0.35]);
  const crowd = parts.crowd('agent', st.cast, spots, 0.52, 27);
  const out = crowd.map((made, i) => (i * 7 + 3) % 10 < 6);        // which agents stop
  crowd.forEach((made, i) => {
    const pushed = !out[i] && made.at[0] > 4.5;            // still lit, and at the building when it shuts
    parts.bob(made.root, 0, out[i] ? tStop : pushed ? tDay + 0.5 : end, i * 0.9, 0.04);
    if (out[i]) parts.miniOff(made, tStop, 0.12);
    if (pushed) parts.move(made.root, tDay + 0.6, [1.0 + rnd.random() * 2.5, GROUND - 0.4 - rnd.random() * 1.1], 1.0);
  });
  cues.push({ t: tStop, type: 'tick', pitch: 0.35, gain: 1.6 }, { t: tStop + 0.05, type: 'whoosh', pitch: 0.5, gain: 0.8 });

  // Sparks run both ways between the board and Hugging Face, until the stop.
  for (let k = 0; k < 6; k++) {
    const runner = parts.spark(`runner${k}`, st.front, parts.body(1 + k % 5)[0], 0.6);
    const a = [-6.5 + rnd.random(), -1.5 + rnd.random() * 3.5];
    const b = [4.2 + rnd.random(), -2.5 + rnd.random() * 3.5];
    for (let t = 0.1 + 0.25 * k; t + 1.2 < tStop; t += 1.45) parts.send(runner, k % 2 ? [b, a] : [a, b], t, t + 1.2, { spin: 3 });
  }

  LEADS.forEach(([x, y, which], k) => {
    const lead = parts.agent(`lead${k}`, st.cast, [x, y], 0.7, which);
    const flag = parts.group(`flag${k}`, st.front, [x + 0.62, y + 0.25]);
    kit.branch(`flag${k}-pole`, flag, [0, 0], [0, 1.0], kit.MIST, 0.07, 1.0);
    kit.shape(`flag${k}-cloth`, [[0.02, 1.0], [0.62, 0.8], [0.02, 0.6]], kit.material(...parts.body(which)), flag);
    parts.off(lead, tStop, 0.12);
    key(flag, 'rot', fr(tStop + 0.2), 0.0);
    key(flag, 'rot', fr(tNotBack + 0.9 + 0.15 * k), -1.35);
    parts.live(lead, 30 + k, 0, tStop);
  });
  cues.push({ t: tNotBack + 0.9, type: 'swoosh', dur: 0.8, gain: 0.5 });

  // ------------------------------------------------------------ Pip, with the agent that pressed it, and what Pip holds
  const pip = parts.agent('pip', st.cast, PIP, 0.9);
  parts.mood(pip, 0, 'flat', 0);
  parts.word('held', st.front, HELD, 0.85, false);
  const promise = parts.check('yes', st.front, [PIP[0] + 0.05, PIP[1] + 1.7], 0.9);
  parts.vanish(promise, tQuiet + 0.4, 0.4);
  const idea = parts.group('idea', st.front, IDEA, 0.8);
  const ideaGlow = kit.shape('idea-glow', kit.circlePts(0.75), kit.glowMaterial(kit.AMBER, 0.6), idea, [0, 0.08]);
  kit.shape('idea-base', kit.rrectPts(0.26, 0.24, 0.05), kit.material(kit.MIST, kit.SLATE), idea, [0, -0.28]);
  const ideaGlass = kit.shape('idea-glass', kit.circlePts(0.3), kit.material('#fff2c4', kit.AMBER), idea, [0, 0.08]);
  for (const lit of [ideaGlow, ideaGlass]) {
    alpha(lit, fr(tQuiet + 0.4), 1.0);
    alpha(lit, fr(tQuiet + 1.4), lit === ideaGlow ? 0.0 : 0.25);
  }
  parts.vanish(idea, tFound, 0.4);

  const presser = parts.agent('presser', st.cast, PRESS, 0.8, 4);
  kit.pipLook(presser, 0.1, -0.13, 0.02);
  parts.off(presser, tStop, 0.12);
  parts.live(presser, 22, 0, tStop);

  kit.pipLook(pip, 0.2, 0.13, 0.04);
  parts.mood(pip, tStop + 0.15, 'wide', 0.12);
  kit.pipLook(pip, tStop + 0.5, -0.13, 0.05);
  kit.pipLook(pip, tStop + 1.3, 0.14, 0.0);
  parts.mood(pip, tLeaders, 'worried');

  const mine = parts.doorKey('pip-key', st.front, KEY, 0.95, 0.5);
  const dead = kit.ring('dead', st.front, KEY, 0.7, kit.CORAL, 0.08);
  kit.flash(dead, tKey, 0.8, 0.5);
  for (const part of mine.shapes) {
    alpha(part, fr(tKey), 1.0);
    alpha(part, fr(tKey + 0.5), 0.35);
  }
  parts.shake(mine.root, tKey, 0.4, 0.06);
  cues.push({ t: tKey, type: 'tick', pitch: 0.45, gain: 1.4 });
  kit.pipLook(pip, tKey - 0.2, 0.1, -0.08);
  parts.mood(pip, tKey + 0.3, 'sad');

  // ------------------------------------------------------------ what Pip has lost
  const noPass = parts.group('no-pass', st.front, [PIP[0] + 0.05, PIP[1] + 1.75]);
  parts.check('no-pass-tick', noPass, [0, 0], 0.9, kit.SLATE);
  parts.cross('no-pass-cross', noPass, [0, 0], 1.1);
  kit.pop(noPass, tNotPassed + 0.2, 1.0, 0.3, tGone - 0.2);
  const noAnswer = parts.notion('no-answer', st.front, [PIP[0] + 1.6, PIP[1] + 1.9], 1.5);
  const what = kit.text('what', '?', 0.75, kit.material(kit.PAPER), st.front, [PIP[0] + 2.7, PIP[1] + 2.2]);
  kit.pop(noAnswer, tNotFound, 1.5, 0.3, tGone - 0.1);
  kit.appear(what, tNotFound + 0.2, tGone - 0.2, 0.2);
  cues.push({ t: tNotPassed + 0.2, type: 'tick', pitch: 0.55, gain: 1.2 }, { t: tNotFound, type: 'blip', pitch: 0.7 });
  kit.pipLook(pip, tNotPassed, 0.0, 0.1);
  kit.pipLook(pip, tGone, -0.14, 0.0);
  kit.pipLook(pip, tGone + 0.9, 0.14, -0.02);
  const clock = parts.clock('clock', st.front, CLOCK, 1.0, 0.14);
  kit.pop(clock.root, tAlmostUp, 1.0, 0.35);
  parts.drain(clock, tAlmostUp + 0.2, end, 0.09);
  const low = kit.ring('low', st.front, CLOCK, 0.65, kit.CORAL, 0.08);
  kit.flash(low, tAlmostUp + 0.3, 0.9, 0.4);
  for (let t = tAlmostUp + 0.2; t < end - 0.2; t += 0.5) cues.push({ t, type: 'tick', pitch: 1.4, gain: 0.7 });
  kit.pipLook(pip, tAlmostUp + 0.2, -0.12, 0.09);
  parts.mood(pip, tAlmostUp + 0.3, 'worried');
  kit.pipLook(pip, tAlone, 0.0, -0.05);
  parts.mood(pip, tAlone, 'sad');
  parts.live(pip, 23);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, ALL], [tLeaders - 0.2, [-0.3, -0.3, 26.4]], [tLeaders + 1.2, [3.4, -0.5, 18.5]], [tQuiet - 0.2, [3.3, -0.5, 18]],
    [tQuiet + 1.2, [-7.4, 0.2, 18]], [tFound - 0.2, [-7.4, 0.2, 17.6]], [tFound + 1.3, [7.4, -0.3, 19]], [tKey - 0.5, [7.2, -0.3, 19]],
    [tKey + 0.8, [-4.0, -1.8, 14]], [tGone - 0.2, [-4.0, -1.5, 14]], [tGone + 1.2, [-3.6, -1.4, 17.5]], [tAlone, [-3.3, -1.2, 19]],
    [end, [-2.0, -0.7, 25]],
  ]), 1.0);
  return cues;
}
