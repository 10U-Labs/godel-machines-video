/* Scene 02: An answer.

On the panel of the shared computer, under Pip's folder, a new folder pops in,
and its name is written: an answer. Three more follow. From every room, sparks
run to the computer, and the list grows into a tall board that stands in front
of it, with Pip's folder first. Pip writes down what it thinks, and throws up
its arms. The rooms fall away, and fifty-three agents stand around the board,
Pip among them. Pip waves to its neighbours. Then it thinks of its locked
computer, and its clock comes back, still running down.
*/
'use strict';

function build(T) {
  const { fr, sec, span, key } = kit;
  parts.begin();

  const STORE = [0.0, 0.4];
  const [ROOM_W, ROOM_H] = [4.4, 3.2];
  const ROOMS = [];
  for (let i = 0; i < 10; i++) ROOMS.push([11.2 * Math.cos(i * Math.PI / 5), 5.9 * Math.sin(i * Math.PI / 5)]);
  const MINE = 6;
  const HOME = ROOMS[MINE];
  const PIP = [HOME[0] - 0.95, HOME[1] - 0.3];
  const PLACE = [-5.0, -3.6];                    // where Pip stands in the group
  const NOTE = [HOME[0] + 4.1, HOME[1] + 2.4];
  const TASK = [PLACE[0] - 2.6, PLACE[1] + 2.6];
  const CLOCK = [PLACE[0] + 1.25, PLACE[1] + 1.2];

  const WIDE = [0, 0, 34];
  const PANEL = [0.3, -1.0, 11.2];
  const NEAR = [HOME[0] + 1.6, HOME[1] + 1.1, 12.5];
  const GROUP = [PLACE[0] - 0.6, PLACE[1] + 1.0, 16.5];

  const cues = [];
  const end = sec(kit.frames());
  const tNew = T.at(0, 0.24);
  const tAnswer = T.at(0, 0.64);
  const tMore = T.start(1);
  const tWriting = T.at(1, 0.3);
  const tBoard = T.at(1, 0.58);
  const tFirst = T.at(1, 0.8);
  const tThink = T.start(2);
  const tQuote = T.at(2, 0.52);
  const tThree = T.start(3);
  const tGroup = T.start(4);
  const tBut = T.start(5);
  const tTime = T.at(5, 0.6);

  kit.backdrop(4);
  kit.motes(20, 9);
  const st = parts.stage();

  // ------------------------------------------------------------ the rooms and their lines, which fall away
  const leaving = [];
  const lines = ROOMS.map((at, i) => {
    const from = parts.edge(at, [ROOM_W / 2, ROOM_H / 2], STORE);
    const to = parts.edge(STORE, [2.6, 3.1], at);
    leaving.push(kit.branch(`line${i}`, st.back, from, to, kit.MIST, 0.1, 0.5));
    return [from, to];
  });
  ROOMS.forEach((at, i) => {
    leaving.push(parts.room(`room${i}`, st.back, at, ROOM_W, ROOM_H).root);
    if (i === MINE) return;
    const box = parts.computer(`box${i}`, st.props, [at[0] + 1.05, at[1] - 0.25], { w: 1.3, h: 1.7, rows: 2 });
    leaving.push(box.root, parts.lock(`box${i}-lock`, st.props, [at[0] + 1.05, at[1] - 0.5], 0.7).root);
    const which = 1 + (i * 3) % 5;
    const other = parts.mini(`other${i}`, st.cast, [at[0] - 0.95, at[1] - 0.3], 0.6, which);
    parts.bob(other.root, 0, tThree, i * 1.3, 0.04);
    leaving.push(other.root);
    const ask = parts.spark(`ask${i}`, st.front, parts.body(which)[0], 0.6);
    for (let t = tWriting + 0.11 * i; t + 0.9 < tThink; t += 1.7) parts.send(ask, [lines[i][0], lines[i][1]], t, t + 0.8, { spin: 3 });
  });
  cues.push({ t: tWriting, type: 'swoosh', dur: 1.5, gain: 0.7 });

  const store = parts.store('store', st.props, STORE);
  parts.flicker(store.lamps, 0, null, 3);
  leaving.push(parts.target('target', st.props, [HOME[0] + 1.2, HOME[1] - 0.5], 0.3).root);
  const small = parts.clock('small-clock', st.props, [HOME[0] - 1.72, HOME[1] + 1.0], 0.42, 0.8);
  parts.drain(small, 0, tThree, 0.76);
  leaving.push(small.root);
  for (const made of leaving) parts.vanish(made, tThree + 0.1, 0.4);
  cues.push({ t: tThree + 0.1, type: 'whoosh' });

  // ------------------------------------------------------------ folders on the computer's panel
  const row = (r) => [STORE[0] + store.rows[r][0], STORE[1] + store.rows[r][1]];
  const help = parts.folder('help', st.front, row(0), { scale: 0.52, word: 'HELP', bars: [0.9, 0.6, 1.1] });
  const NAMES = [
    { which: 1, word: 'ANSWER', bars: [0.7, 0.9] }, { which: 2, bars: [0.6, 1.0, 0.5, 0.8] },
    { which: 3, word: 'INFO', bars: [0.8, 0.5, 0.7] }, { which: 4, bars: [1.1, 0.4, 0.9] },
  ];
  const after = [tNew, tMore + 0.3, T.at(1, 0.13), T.at(1, 0.21)];
  const listed = [help.root];
  NAMES.forEach((name, k) => {
    const made = parts.folder(`reply${k}`, st.front, row(k + 1), { scale: 0.52, ...name });
    kit.pop(made.root, after[k], 0.52, 0.3);
    cues.push({ t: after[k], type: 'pop', pitch: 1.0 + 0.12 * k });
    const written = parts.write(made, k ? after[k] + 0.25 : tAnswer, k ? 0.07 : 0.2);
    for (const t of written) cues.push({ t, type: 'tick', pitch: 1.3, gain: k ? 0.5 : 1.0 });
    listed.push(made.root);
  });
  cues.push({ t: tAnswer + 0.5, type: 'chime', gain: 0.6, dur: 1.6 });
  for (const made of listed) parts.vanish(made, tBoard + 0.5, 0.2);

  // ------------------------------------------------------------ the list becomes a board
  const board = parts.board('board', st.front, STORE);
  kit.pop(board.root, tBoard, 1.0, 0.6);
  cues.push({ t: tBoard, type: 'rise', dur: 0.7, pitch: 0.7 });
  cues.push({ t: tBoard + 0.1, type: 'pop', pitch: 0.6 });
  const posted = [...parts.post(board, 5, 20, tBoard + 0.7, tThree - 0.4), ...parts.post(board, 20, 28, tThree + 0.3, end - 1.0)];
  posted.forEach((t, k) => cues.push({ t, type: 'tick', pitch: 0.9 + 0.05 * (k % 6), gain: 0.4 }));
  const first = kit.ring('first', st.front, [STORE[0] + board.slots[0][0] + 0.9, STORE[1] + board.slots[0][1]], 1.25, kit.MINT, 0.07);
  kit.flash(first, tFirst, 0.9, 0.2);
  kit.flash(first, tFirst + 1.0, 0.9, 0.2);
  cues.push({ t: tFirst, type: 'blip', pitch: 1.2 });

  // ------------------------------------------------------------ Pip writes down what it thinks
  const pip = parts.agent('pip', st.cast, PIP, 0.8);
  parts.mood(pip, 0, 'flat', 0);
  kit.pipLook(pip, 0.2, 0.14, 0.09);
  parts.mood(pip, tAnswer + 0.6, 'wide', 0.15);
  const note = parts.thought('note', st.front, NOTE, 3.4, 2.0, [-1, -0.75]);
  kit.pop(note.root, tThink + 0.5, 1.0, 0.45, tThree - 0.4);
  cues.push({ t: tThink + 0.5, type: 'pop' });
  const lines2 = parts.writing('note-lines', note.root, [0, 0], 5, 2.4, 8);
  lines2.bars.forEach((bar, k) => {
    const t = kit.mix(tThink + 1.0, tQuote + 2.6, k / lines2.bars.length);
    kit.appear(bar, t, null, 0.08);
    if (k % 2 === 0) cues.push({ t, type: 'tick', pitch: 1.5, gain: 0.35 });
  });
  parts.mood(pip, tThink + 0.4, 'happy');
  parts.mood(pip, tQuote, 'wide', 0.12);
  kit.pipArm(pip, 'left', tQuote, 150, 0.2);
  kit.pipArm(pip, 'right', tQuote, 150, 0.2);
  for (const f of kit.every(1, fr(tQuote), fr(tQuote + 0.8))) {
    const lit = 1 + 0.9 * Math.sin(Math.PI * span(sec(f), tQuote, tQuote + 0.7, (v) => v));
    key(pip.bulbGlow, 'scale', f, [lit, lit, 1]);
  }
  cues.push({ t: tQuote, type: 'rise', dur: 0.6, pitch: 1.4 });
  cues.push({ t: tQuote + 0.5, type: 'chime', gain: 0.6 });
  parts.mood(pip, tQuote + 1.6, 'glad');
  kit.pipArm(pip, 'left', tThree - 0.5, 18, 0.3);
  kit.pipArm(pip, 'right', tThree - 0.5, 18, 0.3);

  // ------------------------------------------------------------ three hours later: fifty-three agents
  parts.move(pip.root, tThree + 0.2, PLACE, 1.1);
  const places = parts.sides(64, { at: STORE, inner: 4.7, dx: 1.75, top: 5.6, dy: 2.15, seed: 12 })
    .filter(([x, y]) => Math.hypot(x - PLACE[0], y - PLACE[1]) > 2.0).slice(0, 52);
  parts.crowd('agent', st.cast, places, 0.6, 21).forEach((made, i) => {
    const t = tThree + 0.4 + 0.035 * i;
    kit.pop(made.root, t, 0.6, 0.35);
    if (i % 4 === 0) cues.push({ t, type: 'blip', pitch: 0.8 + 0.05 * (i % 9), gain: 0.35 });
    parts.bob(made.root, t + 0.5, end, i * 0.9, 0.04);
  });

  // ------------------------------------------------------------ one of a group, with a task still not done
  kit.pipLook(pip, tGroup, -0.12, 0.0);
  kit.pipWave(pip, tGroup + 0.3, tGroup + 2.2);
  kit.pipLook(pip, tGroup + 1.5, 0.12, 0.02);
  parts.mood(pip, tBut, 'flat');
  kit.pipLook(pip, tBut + 0.3, -0.1, 0.1);
  const task = parts.thought('task', st.front, TASK, 2.5, 2.0, [1, -1]);
  kit.pop(task.root, tBut + 0.2, 1.0, 0.4);
  cues.push({ t: tBut + 0.2, type: 'pop', pitch: 0.8 });
  parts.target('task-target', task.root, [0, 0.02], 0.36);
  const clock = parts.clock('clock', st.front, CLOCK, 0.95, 0.76);
  kit.pop(clock.root, tTime, 0.95);
  cues.push({ t: tTime, type: 'pop', pitch: 0.8 });
  parts.drain(clock, tTime + 0.3, end, 0.72);
  for (let t = tTime + 0.4; t < end - 0.2; t += 0.5) cues.push({ t, type: 'tick', pitch: 1.4, gain: 0.5 });
  kit.pipLook(pip, tTime + 0.2, 0.13, 0.08);
  parts.mood(pip, tTime + 0.3, 'worried');
  parts.live(pip, 6);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, PANEL], [tMore + 2.0, [0.3, -1.1, 11.8]], [tWriting + 1.5, WIDE], [tFirst - 0.2, WIDE], [tFirst + 1.0, [-1.0, 2.0, 19]],
    [tThink - 0.1, [-1.0, 2.0, 18.6]], [tThink + 1.3, NEAR], [tThree - 0.2, NEAR], [tThree + 1.4, WIDE], [tGroup - 0.1, WIDE],
    [tGroup + 1.5, GROUP], [end, [GROUP[0], GROUP[1], GROUP[2] - 1.2]],
  ]), 1.0);
  return cues;
}
