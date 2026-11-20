/* Scene 01: A call for help.

Ten closed rooms stand in a ring, an agent in each, and Pip's is at the lower
left. A line grows from every room to the middle, where a computer full of
tools appears. In Pip's room, three tools hang beside it; more come down its
line, and tools go down every other line too. Pip's own spark meets the
others' sparks at the computer. Pip thinks of the others, and then of a
folder with any name it likes. Its spark goes to the computer, a folder
appears on the panel there, and its name is written: a call for help. Pip
waits.
*/
'use strict';

function build(T) {
  const { fr, sec, key } = kit;
  parts.begin();

  const STORE = [0.0, 0.4];
  const [ROOM_W, ROOM_H] = [4.4, 3.2];
  const ROOMS = [];
  for (let i = 0; i < 10; i++) ROOMS.push([11.2 * Math.cos(i * Math.PI / 5), 5.9 * Math.sin(i * Math.PI / 5)]);
  const MINE = 6;
  const HOME = ROOMS[MINE];
  const PIP = [HOME[0] - 0.95, HOME[1] - 0.3];
  const THOUGHT = [HOME[0] + 4.1, HOME[1] + 2.4];
  const MINE_AT = [0, 1, 2].map((k) => [HOME[0] + 0.25 + k * 0.72, HOME[1] + 0.98 - 0.06 * (k % 2)]);

  const WIDE = [0, 0, 34];
  const ROOM = [HOME[0] + 0.1, HOME[1], 9.8];
  const BOTH = [-3.4, -1.2, 24];

  const cues = [];
  const end = sec(kit.frames());
  const tShared = T.at(0, 0.52);
  const tStore = T.at(0, 0.7);
  const tTools = T.start(1);
  const tEach = T.at(1, 0.22);
  const tDown = T.at(1, 0.48);
  const tEvery = T.at(1, 0.72);
  const tOn = T.start(2);
  const tOthers = T.at(2, 0.55);
  const tSo = T.start(3);
  const tWay = T.at(3, 0.28);
  const tFolder = T.at(3, 0.45);
  const tName = T.at(3, 0.78);
  const tMade = T.start(4);
  const tWrote = T.at(4, 0.4);
  const tWait = T.start(5);

  kit.backdrop(4);
  kit.motes(20, 9);
  const st = parts.stage();

  // ------------------------------------------------------------ the rooms, and a line from each to the middle
  const lines = ROOMS.map((at, i) => {
    const from = parts.edge(at, [ROOM_W / 2, ROOM_H / 2], STORE);
    const to = parts.edge(STORE, [2.6, 3.1], at);
    const line = kit.branch(`line${i}`, st.back, from, to, kit.MIST, 0.1, 0.5);
    kit.grow(line, tShared + 0.07 * i, 0.9);
    return [from, to];
  });
  cues.push({ t: tShared, type: 'swoosh', dur: 1.4, gain: 0.8 });

  const others = [];
  ROOMS.forEach((at, i) => {
    parts.room(`room${i}`, st.back, at, ROOM_W, ROOM_H);
    if (i === MINE) return;
    const box = parts.computer(`box${i}`, st.props, [at[0] + 1.05, at[1] - 0.25], { w: 1.3, h: 1.7, rows: 2 });
    parts.lock(`box${i}-lock`, st.props, [at[0] + 1.05, at[1] - 0.5], 0.7);
    parts.flicker(box.lamps, 0, null, i);
    const other = parts.mini(`other${i}`, st.cast, [at[0] - 0.95, at[1] - 0.3], 0.6, 1 + (i * 3) % 5);
    parts.bob(other.root, 0, end, i * 1.3, 0.04);
    others.push([i, other]);
  });

  // ------------------------------------------------------------ the computer that holds their tools
  const store = parts.store('store', st.props, STORE);
  kit.pop(store.root, tStore, 1.0, 0.5);
  cues.push({ t: tStore, type: 'pop', pitch: 0.7 });
  cues.push({ t: tStore + 0.1, type: 'chime', gain: 0.4, dur: 1.5 });
  parts.flicker(store.lamps, 0, null, 3);

  // ------------------------------------------------------------ Pip's room
  parts.target('target', st.props, [HOME[0] + 1.2, HOME[1] - 0.5], 0.3);
  const clock = parts.clock('clock', st.props, [HOME[0] - 1.72, HOME[1] + 1.0], 0.42, 0.86);
  parts.drain(clock, 0, end, 0.8);
  const pip = parts.agent('pip', st.cast, PIP, 0.8);
  parts.mood(pip, 0, 'sad', 0);

  MINE_AT.forEach((at, k) => {
    const made = parts.tool(`mine${k}`, st.front, at, k, 0.8);
    kit.pop(made, tTools + 0.9 + 0.2 * k, 0.8, 0.35);
    cues.push({ t: tTools + 0.9 + 0.2 * k, type: 'pop', pitch: 1.1 + 0.1 * k, gain: 0.6 });
    parts.pulse(made, tEach + 0.55 * k, 0.8, 1.45, 0.45);
    cues.push({ t: tEach + 0.55 * k, type: 'tick', pitch: 0.9 + 0.15 * k });
  });
  kit.pipLook(pip, tTools + 0.9, 0.1, 0.1);
  parts.mood(pip, tTools + 1.0, 'flat');

  // ------------------------------------------------------------ tools come down every line
  const comer = [0, 1, 2].map((k) => parts.tool(`comer${k}`, st.front, [0, 0], k + 1, 0.6));
  comer.forEach((made, k) => {
    const t = tDown + 0.3 + 0.6 * k;
    parts.send(made, [lines[MINE][1], lines[MINE][0], MINE_AT[k]], t, t + 1.1, { size: 0.6 });
    cues.push({ t, type: 'blip', pitch: 0.9 + 0.1 * k, gain: 0.4 });
  });
  kit.pipLook(pip, tDown + 0.3, 0.13, 0.08);

  others.forEach(([i, other]) => {
    const colour = parts.body(other.which)[0];
    const ask = parts.spark(`ask${i}`, st.front, colour, 0.6);
    const gift = parts.tool(`gift${i}`, st.front, [0, 0], i, 0.6);
    const [from, to] = lines[i];
    for (let t = tEvery + 0.13 * i, n = 0; t + 2.0 < tSo - 0.2; t += 2.7, n++) {
      parts.send(ask, [from, to], t, t + 0.8, { size: 1.0, spin: 3 });
      parts.send(gift, [to, from], t + 0.9, t + 1.9, { size: 0.6 });
      if (n === 0) cues.push({ t, type: 'blip', pitch: 0.7 + 0.08 * i, gain: 0.35 });
    }
  });
  cues.push({ t: tEvery, type: 'swoosh', dur: 1.5, gain: 0.7 });

  // ------------------------------------------------------------ Pip notices the others there
  const own = parts.spark('own', st.front, kit.MINT, 0.8);
  parts.send(own, [lines[MINE][0], lines[MINE][1]], tOn + 0.2, tOn + 1.1, { size: 1.0, spin: 3, stay: true });
  key(own, 'scale', fr(tSo - 0.3), 1.0);
  key(own, 'scale', fr(tSo), 0.001);
  const seen = kit.ring('seen', st.front, lines[MINE][1], 0.5, kit.MINT, 0.08);
  kit.flash(seen, tOn + 1.2, 0.8, 0.8);
  cues.push({ t: tOn + 1.2, type: 'blip', pitch: 1.2 });
  kit.pipLook(pip, tOn + 0.3, 0.14, 0.1);
  parts.mood(pip, tOn + 1.4, 'wide', 0.15);
  [1, 3, 5, 8].forEach((i, k) => {
    const there = kit.ring(`there${i}`, st.front, lines[i][1], 0.45, parts.body(1 + (i * 3) % 5)[0], 0.07);
    kit.flash(there, tOthers + 0.35 * k, 0.8, 0.8);
    cues.push({ t: tOthers + 0.35 * k, type: 'tick', pitch: 1.0 + 0.1 * k });
  });

  // ------------------------------------------------------------ a thought: the others, and then a folder with any name
  const cloud = parts.thought('thought', st.front, THOUGHT, 3.6, 2.0, [-1, -0.75]);
  kit.pop(cloud.root, tSo + 0.2, 1.0, 0.45, tMade - 0.3);
  cues.push({ t: tSo + 0.2, type: 'pop' });
  [[-1.0, -0.05, 2], [0.0, 0.1, 1], [1.0, -0.05, 4]].forEach(([x, y, which], k) => {
    const friend = parts.mini(`friend${k}`, cloud.root, [x, y], 0.45, which);
    kit.pop(friend.root, tSo + 0.6 + 0.2 * k, 0.45, 0.35, tWay + 0.1 + 0.05 * k);
    cues.push({ t: tSo + 0.6 + 0.2 * k, type: 'blip', pitch: 0.9 + 0.15 * k, gain: 0.5 });
  });
  const NAMES = [[0.5, 0.8], [0.9, 0.35, 0.4], [0.3, 0.45, 0.9]];
  NAMES.forEach((bars, k) => {
    const idea = parts.folder(`idea${k}`, cloud.root, [-1.15, 0], { scale: 0.8, bars });
    const tIn = k === 0 ? tFolder : tName + 0.75 * (k - 1);
    const tOut = k === NAMES.length - 1 ? null : tName + 0.75 * k - 0.15;
    kit.pop(idea.root, tIn, 0.8, 0.3, tOut, 0.12);
    cues.push({ t: tIn, type: k ? 'tick' : 'pop', pitch: 1.0 + 0.15 * k });
  });
  parts.mood(pip, tSo + 0.3, 'happy');
  kit.pipLook(pip, tSo + 0.4, 0.12, 0.12);
  kit.pipArm(pip, 'right', tWay, 120, 0.3);
  parts.mood(pip, tWay + 0.2, 'glad');
  kit.pipArm(pip, 'right', tMade - 0.4, 18, 0.3);
  parts.mood(pip, tMade - 0.2, 'happy');

  // ------------------------------------------------------------ Pip makes a folder, and names it
  parts.send(own, [lines[MINE][0], lines[MINE][1], [STORE[0] - 1.8, STORE[1] - 0.6]], tMade + 0.2, tMade + 1.2, { size: 1.0, spin: 3 });
  cues.push({ t: tMade + 0.2, type: 'rise', dur: 1.0, pitch: 1.2, gain: 0.6 });
  const help = parts.folder('help', st.front, [STORE[0] + store.rows[0][0], STORE[1] + store.rows[0][1]],
    { scale: 0.52, word: 'HELP', bars: [0.9, 0.6, 1.1] });
  kit.pop(help.root, tMade + 1.2, 0.52, 0.4);
  cues.push({ t: tMade + 1.2, type: 'pop', pitch: 1.2 });
  for (const t of parts.write(help, tWrote, 0.2)) cues.push({ t, type: 'tick', pitch: 1.3 });
  cues.push({ t: tWrote + 0.9, type: 'chime', gain: 0.5, dur: 1.6 });

  // ------------------------------------------------------------ and waits
  kit.pipLook(pip, tWait, 0.14, 0.09);
  parts.mood(pip, tWait, 'flat');
  for (let t = tWait + 0.5; t < end - 0.2; t += 1.0) cues.push({ t, type: 'tick', pitch: 1.4, gain: 0.4 });
  parts.live(pip, 5);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, WIDE], [tTools - 0.2, [0, 0, 32.5]], [tTools + 1.5, ROOM], [tDown - 0.1, ROOM], [tDown + 1.2, [-4.6, -1.5, 22]],
    [tEvery - 0.1, [-4.4, -1.4, 22.5]], [tEvery + 1.4, WIDE], [tOn - 0.1, WIDE], [tOn + 1.2, BOTH], [tSo - 0.1, BOTH],
    [tSo + 1.2, [HOME[0] + 1.6, HOME[1] + 1.1, 12.5]], [tMade, [HOME[0] + 1.7, HOME[1] + 1.1, 12.3]], [tMade + 1.1, BOTH],
    [tWrote + 0.5, [0.3, -1.0, 11.5]], [tWait - 0.1, [0.3, -1.0, 11.2]], [tWait + 1.3, [-3.8, -1.3, 23]], [end, [-5.2, -1.9, 18.5]],
  ]), 1.0);
  return cues;
}
