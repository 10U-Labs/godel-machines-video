/* Scene 00: Stuck.

Pip pops in and waves. A task comes down to it, and Pip does it a step at a
time. Then a locked computer slides in with a secret word shining inside, and
Pip sends spark after spark at its one way in; every one dies there. The
computer's front fades: the passage from the way in stops at a wall, short of
the room the word is in. The picture draws back: Pip is in a closed room, and
around it are hundreds of rooms like it, an agent in each. Back with Pip, a
clock appears and starts to run down.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, alpha, every } = kit;
  parts.begin();

  const HOME = [0.0, -0.3];
  const WORK = [-4.5, -0.7];
  const TARGET = [3.3, -0.1];
  const SHEET = [2.7, 0.5];
  const CLOCK = [-2.3, 1.7];
  const [ROOM_W, ROOM_H] = [18.0, 10.2];
  const [PITCH_X, PITCH_Y] = [21.0, 12.4];
  const NEAR = 0.72;                       // the picture's scale when it shows the whole of Pip's room, and no other
  const FAR = 0.03;                        // and when it shows the rooms around it

  const cues = [];
  const end = sec(kit.frames());
  const tHello = T.start(0);
  const tTask = T.at(0, 0.42);
  const tSteps = T.at(0, 0.7);
  const tDay = T.start(1);
  const tWord = T.at(1, 0.26);
  const tBreak = T.at(1, 0.45);
  const tWhy = T.start(2);
  const tOne = T.at(2, 0.22);
  const tNoWay = T.at(2, 0.55);
  const tAlone = T.start(3);
  const tThought = T.at(3, 0.2);
  const tMany = T.at(3, 0.36);
  const tShut = T.at(3, 0.62);
  const tNobody = T.at(3, 0.84);
  const tTime = T.start(4);
  const tSet = T.at(4, 0.28);
  const tUp = T.at(4, 0.62);

  kit.backdrop();
  kit.motes(24);
  const grid = kit.empty('all-grid', kit.layer('grid', 0.7, { sharp: true }), [0, 0, 0]);
  const st = parts.stage();

  // ------------------------------------------------------------ the rooms around Pip's
  const rnd = new kit.Random(7);
  const wall = kit.material(kit.INK500);
  const inside = kit.material(kit.INK800);
  for (let j = -13; j <= 13; j++) {
    for (let i = -14; i <= 14; i++) {
      if (i === 0 && j === 0) continue;
      const at = [i * PITCH_X, j * PITCH_Y];
      kit.shape(`room${i}_${j}`, kit.rrectPts(ROOM_W, ROOM_H, 0), wall, grid, at);
      kit.shape(`room${i}_${j}-in`, kit.rrectPts(ROOM_W - 1.2, ROOM_H - 1.2, 0), inside, grid, at);
      const dot = [at[0] - 4.5 + rnd.random() * 3, at[1] - 0.7];
      kit.shape(`room${i}_${j}-agent`, kit.circlePts(1.3, null, null, 8), kit.material(parts.body(1 + rnd.randrange(5))[0]), grid, dot);
    }
  }

  // ------------------------------------------------------------ Pip's room, the locked computer, Pip
  parts.room('room', st.back, [0, 0], ROOM_W, ROOM_H, 0.6);
  const target = parts.target('target', st.props, [16, TARGET[1]]);
  const pip = parts.agent('pip', st.cast, HOME, 1.3);
  kit.pop(pip.root, tHello, 1.3);
  cues.push({ t: tHello, type: 'pop' });
  kit.pipWave(pip, tHello + 0.7, tHello + 2.4);

  const label = kit.text('pip-name', 'Pip', 0.55, kit.material(kit.PAPER), st.front, [0, -2.3]);
  kit.fade(label, tHello + 0.5, tTask - 0.4);

  // ------------------------------------------------------------ a task, done a step at a time
  const sheet = parts.sheet('task', st.props, SHEET, { scale: 1.7, seed: 5 });
  kit.pop(sheet.root, tTask, 1.7, 0.45, tDay - 0.7);
  cues.push({ t: tTask, type: 'whoosh', gain: 0.6 });
  kit.pipLook(pip, tTask + 0.2, 0.12, 0.04);
  for (let r = 0; r < 3; r++) {
    const done = parts.check(`step${r}`, st.front, [SHEET[0] + 1.15, SHEET[1] + (0.28 - r * 0.17) * 1.7], 0.5);
    const t = tSteps + r * 0.55;
    kit.pop(done, t, 0.5, 0.3, tDay - 0.7 + r * 0.04);
    cues.push({ t, type: 'tick', pitch: 1 + 0.12 * r });
  }
  kit.pipArm(pip, 'right', tSteps - 0.3, 75, 0.25);
  kit.pipArm(pip, 'right', tDay - 0.6, 18, 0.3);
  kit.pipLook(pip, tDay - 0.4, 0, 0);

  // ------------------------------------------------------------ the locked computer and its secret word
  key(pip.root, 'scale', fr(tDay), 1.3);
  key(pip.root, 'scale', fr(tDay + 0.9), 1.0);
  parts.move(pip.root, tDay, WORK, 0.9);
  parts.move(target.root, tDay + 0.2, TARGET, 1.1);
  cues.push({ t: tDay + 0.2, type: 'whoosh' });
  kit.pipLook(pip, tDay + 0.9, 0.14, 0.03);

  parts.pulse(target.word.root, tWord, 0.95, 1.3, 0.6);
  cues.push({ t: tWord, type: 'chime', gain: 0.5, dur: 1.4 });
  parts.pulse(target.lock.root, tWord + 1.0, 1.5, 1.2, 0.4);
  cues.push({ t: tWord + 1.0, type: 'tick', pitch: 0.7 });

  // Pip sends a spark at the way in, again and again, and each one dies there.
  const place = (local) => [TARGET[0] + local[0], TARGET[1] + local[1]];
  const hand = [WORK[0] + 1.3, WORK[1] - 0.27];
  const door = place(target.entrance);
  const arc = (lift) => {
    const pts = [];
    for (let i = 0; i <= 12; i++) pts.push([mix(hand[0], door[0], i / 12), mix(hand[1], door[1], i / 12) + lift * Math.sin(Math.PI * i / 12)]);
    return pts;
  };
  const shot = parts.spark('shot', st.front);
  const dud = parts.spark('dud', st.front, kit.CORAL, 0.8);
  const refused = kit.ring('refused', st.front, door, 0.42, kit.CORAL, 0.09);
  const tries = [0, 1, 2, 3, 4, 5].map((i) => mix(tBreak + 0.5, T.end(1) - 0.8, i / 5));
  tries.forEach((t, i) => {
    kit.pipArm(pip, 'right', t - 0.25, 82, 0.2);
    parts.send(shot, arc(0.5 + 0.25 * (i % 3)), t, t + 0.45, { spin: 4 });
    kit.flash(refused, t + 0.45, 0.5, 0.6);
    parts.send(dud, [door, [door[0] - 0.5, door[1] - 0.5], [door[0] - 0.7, door[1] - 1.4]], t + 0.45, t + 0.95, { size: 0.7, ease: (q) => q * q });
    kit.pipArm(pip, 'right', t + 0.5, 30, 0.3);
    cues.push({ t, type: 'rise', dur: 0.4, pitch: 1.4 + 0.05 * i, gain: 0.5 });
    cues.push({ t: t + 0.45, type: 'tick', pitch: 0.6 });
  });
  parts.mood(pip, tries[1] + 0.6, 'flat');
  parts.mood(pip, tries[3] + 0.6, 'worried');
  parts.mood(pip, tries[5] + 0.6, 'sad');

  // ------------------------------------------------------------ why: the way in leads nowhere
  parts.mood(pip, tWhy, 'wide', 0.15);
  for (const f of every(1, fr(tWhy), fr(tWhy + 0.8))) {
    const lit = 1 + 0.9 * Math.sin(Math.PI * span(sec(f), tWhy, tWhy + 0.7, (v) => v));
    key(pip.bulbGlow, 'scale', f, [lit, lit, 1]);
  }
  cues.push({ t: tWhy, type: 'blip', pitch: 1.3 });
  for (const part of target.cover) {
    alpha(part, fr(tWhy + 0.4), 1.0);
    alpha(part, fr(tWhy + 1.2), 0.0);
    alpha(part, fr(tAlone + 0.2), 0.0);
    alpha(part, fr(tAlone + 1.0), 1.0);
  }
  cues.push({ t: tWhy + 0.4, type: 'swoosh', dur: 0.9, gain: 0.7 });
  const oneWay = kit.ring('one-way', st.front, door, 0.5, kit.MINT, 0.09);
  kit.flash(oneWay, tOne, 0.7, 0.5);
  kit.flash(oneWay, tOne + 0.8, 0.7, 0.5);
  cues.push({ t: tOne, type: 'blip', pitch: 0.9 });

  const tGo = tNoWay - 0.5;
  const tStop = tNoWay + 1.3;
  kit.pipArm(pip, 'right', tGo - 0.25, 82, 0.2);
  parts.send(shot, [...arc(0.6), ...target.way.slice(1).map(place)], tGo, tStop, { spin: 4, ease: (q) => q });
  cues.push({ t: tGo, type: 'rise', dur: 0.5, pitch: 1.3, gain: 0.5 });
  alpha(target.cap, fr(tStop - 0.3), 0.0);
  alpha(target.cap, fr(tStop), 1.0);
  alpha(target.cap, fr(tAlone + 0.2), 1.0);
  alpha(target.cap, fr(tAlone + 1.0), 0.0);
  const stopped = kit.ring('stopped', st.front, place(target.way[2]), 0.4, kit.CORAL, 0.09);
  kit.flash(stopped, tStop, 0.7, 0.8);
  cues.push({ t: tStop, type: 'tick', pitch: 0.5, gain: 1.2 });
  const sealed = kit.ring('sealed', st.front, place(target.chamber), 1.25, kit.AMBER, 0.07);
  kit.flash(sealed, tStop + 0.7, 1.0, 0.25);
  kit.pipArm(pip, 'right', tStop + 0.3, 18, 0.4);
  parts.mood(pip, tStop + 0.3, 'sad');

  // ------------------------------------------------------------ alone, among hundreds of closed rooms
  kit.pipLook(pip, tAlone + 0.4, -0.13, 0.0);
  kit.pipLook(pip, tAlone + 1.3, 0.13, 0.0);
  kit.pipLook(pip, tThought, 0.0, 0.07);
  parts.mood(pip, tThought, 'flat');
  const scale = parts.ramp([
    [tAlone, 0.0], [tAlone + 1.6, Math.log(NEAR)], [tMany, Math.log(NEAR)], [tMany + 2.8, Math.log(FAR)],
    [tNobody - 0.2, Math.log(FAR)], [tNobody + 1.8, Math.log(NEAR)], [tTime, Math.log(NEAR)], [tTime + 1.2, 0.0],
  ]);
  parts.zoom([grid, ...st.all], (t) => Math.exp(scale(t)));
  cues.push({ t: tMany, type: 'swoosh', dur: 2.8 });
  cues.push({ t: tNobody - 0.2, type: 'swoosh', dur: 2.0, gain: 0.8 });
  const here = kit.ring('here', st.raw.front, [0, 0], 0.45, kit.MINT, 0.06);
  kit.flash(here, tMany + 2.8, 1.1, 0.6);
  kit.flash(here, tShut + 0.9, 1.1, 0.6);
  cues.push({ t: tMany + 2.8, type: 'blip', pitch: 1.1, gain: 0.6 });
  parts.mood(pip, tNobody, 'sad');
  kit.pipLook(pip, tNobody + 1.2, -0.1, -0.04);

  // ------------------------------------------------------------ a set amount of time
  const clock = parts.clock('clock', st.front, CLOCK, 1.5);
  kit.pop(clock.root, tSet, 1.5);
  cues.push({ t: tSet, type: 'pop', pitch: 0.8 });
  parts.drain(clock, tSet + 0.5, end, 0.87);
  for (let t = tSet + 0.6; t < end - 0.2; t += 0.5) cues.push({ t, type: 'tick', pitch: 1.4, gain: 0.5 });
  kit.pipLook(pip, tSet + 0.2, 0.12, 0.09);
  const last = kit.ring('last', st.front, CLOCK, 0.95, kit.CORAL, 0.08);
  kit.flash(last, tUp, 0.9, 0.3);
  kit.flash(last, tUp + 1.0, 0.9, 0.3);
  parts.mood(pip, tUp, 'worried');
  parts.live(pip, 3);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [-0.2, 0.0, kit.H0]], [tDay, [0.2, 0.05, kit.H0 - 0.8]], [tWhy, [0.4, 0.0, kit.H0 - 1.2]],
    [tWhy + 1.8, [2.0, -0.1, kit.H0 - 4.6]], [tAlone - 0.3, [2.3, -0.1, kit.H0 - 5.0]], [tAlone + 1.4, [0, 0, kit.H0]],
    [tTime, [0, 0, kit.H0]], [tTime + 1.6, [-2.6, 0.3, kit.H0 - 4.2]], [end, [-2.8, 0.35, kit.H0 - 5.0]],
  ]), 1.0);
  return cues;
}
