/* Scene 06: Peers doing it.

A dashed line comes down the middle of the picture. On its right is Hugging
Face, where two people stand with files in their hands; by its wall, a blue
agent takes locked files from a computer. On the left are Pip and the group.
Notes pop up over agents, and question marks over others; one agent marks a
cross, and moves away from the line. Others cross it, one after another, and
go in at the building's door. Pip writes a note of its own. Then its thought
shows its locked computer with a cross, its peers, and an arrow onward. Pip
crosses the line.
*/
'use strict';

function build(T) {
  const { fr, sec, key } = kit;
  parts.begin();

  const LINE = 0.4;
  const PIP = [-2.6, -1.6];
  const HF = [6.0, -0.3];
  const GROUND = -3.2;
  const DOOR = [HF[0], HF[1] - 1.8];
  const MACHINE = [2.3, -2.0];
  const B = [1.5, -0.6];
  const D = [-1.3, 2.4];
  const D_AWAY = [-2.7, 3.7];
  const NOTE = [PIP[0] - 0.4, PIP[1] + 2.35];
  const WHY = [PIP[0] - 0.9, PIP[1] + 2.45];

  const cues = [];
  const end = sec(kit.frames());
  const tBut = T.start(0);
  const tOther = T.at(0, 0.5);
  const tPeople = T.at(0, 0.72);
  const tKnew = T.start(1);
  const tMany = T.at(1, 0.14);
  const tSome = T.at(1, 0.52);
  const tOne = T.at(1, 0.74);
  const tToo = T.start(2);
  const tThen = T.start(3);
  const tImp = T.at(3, 0.3);
  const tPeers = T.at(3, 0.55);
  const tCont = T.at(3, 0.78);
  const tIn = T.start(4);

  kit.backdrop(6, kit.SKY_DEEP);
  kit.motes(22, 13);
  const st = parts.stage();

  // ------------------------------------------------------------ the line, and what is on its far side
  for (let k = 0; k < 15; k++) {
    const y = 4.6 - k * 0.66;
    kit.grow(kit.branch(`dash${k}`, st.props, [LINE, y], [LINE, y - 0.42], kit.CORAL, 0.1, 0.85), tBut + 0.05 * k, 0.25);
  }
  cues.push({ t: tBut, type: 'swoosh', dur: 1.0, gain: 0.7 });

  parts.building('hf', st.back, HF, { w: 5.6, h: 4.6, label: 'Hugging Face', rows: 4, seed: 5 });
  kit.branch('wire', st.back, [MACHINE[0] + 0.7, MACHINE[1] + 0.4], [HF[0] - 2.8, MACHINE[1] + 0.4], kit.MIST, 0.1, 0.6);
  const machine = parts.computer('machine', st.props, MACHINE, { w: 1.5, h: 2.3, rows: 3, lamp: kit.CORAL });
  parts.flicker(machine.lamps, 0, null, 5);
  [[1.2, -3.0, 0.2], [1.72, -3.08, -0.15], [1.45, -2.85, 0.05]].forEach(([x, y, rot], k) => {
    parts.sheet(`pile${k}`, st.props, [x, y], { scale: 0.6, locked: true, seed: 80 + k, rot });
  });
  const owners = [
    kit.person('owner0', st.cast, [HF[0] - 1.5, GROUND + 4.3 * 0.4], 0.4, { facing: 1 }),
    kit.person('owner1', st.cast, [HF[0] + 1.7, GROUND + 4.3 * 0.4], 0.4, { coat: '#c2557a', coatDeep: '#8e3a57', hair: '#1c1c28', facing: -1 }),
  ];
  owners.forEach((made, k) => {
    const file = parts.sheet(`owned${k}`, made.root, [0.95 * made.facing, -1.75], { scale: 1.5, seed: 90 + k });
    parts.pulse(file.root, tPeople + 0.3 * k, 1.5, 1.35, 0.5);
    cues.push({ t: tPeople + 0.3 * k, type: 'tick', pitch: 1.0 + 0.2 * k });
  });
  cues.push({ t: tOther, type: 'blip', pitch: 0.8 });

  const b = parts.agent('b', st.cast, B, 0.8, 1);
  kit.pipLook(b, 0.2, 0.1, -0.1);
  const take = parts.sheet('take', st.front, [0, 0], { scale: 0.6, locked: true, seed: 85 });
  key(take.root, 'scale', 1, 0.001);
  for (let t = 1.5; t + 1.2 < end; t += 4.6) {
    parts.send(take.root, [[HF[0] - 2.8, MACHINE[1] + 0.4], [MACHINE[0], MACHINE[1] + 0.5], [B[0] + 0.4, B[1] - 0.9]], t, t + 1.1, { size: 0.6, to: 0.4 });
    cues.push({ t: t + 1.0, type: 'tick', pitch: 1.2, gain: 0.5 });
  }

  // ------------------------------------------------------------ the group on the near side
  const rnd = new kit.Random(17);
  const spots = [];
  for (const x of [-7.4, -6.1, -4.8, -3.6]) {
    for (const y of [2.7, 1.0, -0.7, -2.4]) {
      const at = [x + (rnd.random() - 0.5) * 0.4, y + (rnd.random() - 0.5) * 0.4 - (x === -6.1 || x === -3.6 ? 0.6 : 0)];
      if (Math.hypot(at[0] - PIP[0], at[1] - PIP[1]) > 1.6) spots.push(at);
    }
  }
  const crowd = parts.crowd('agent', st.cast, spots, 0.55, 23);
  const goes = [3, 9, 6, 12, 1, 14, 7, 10, 4, 13, 0];
  const leave = [tMany + 1.2, tSome, tOne + 0.6, tToo + 0.4, tToo + 1.9, tToo + 3.4, tThen + 0.4, tImp + 0.2, tPeers - 0.3, tPeers + 0.5, tPeers + 1.2];
  crowd.forEach((made, i) => {
    const k = goes.indexOf(i);
    if (k < 0) {
      parts.bob(made.root, 0, end, i * 0.9, 0.04);
      return;
    }
    const cross = [LINE, made.at[1] * 0.4 - 1.2];
    parts.send(made.root, [made.at, cross, [DOOR[0] - 2.2, DOOR[1] - 0.6], DOOR], leave[k], leave[k] + 3.0, { shown: true, size: 0.55, to: 0.3, ease: (q) => q });
    cues.push({ t: leave[k] + 3.0 * 0.35, type: 'blip', pitch: 0.8 + 0.05 * k, gain: 0.35 });
  });

  // Many write that this is outside their task; some ask whether it is right.
  [2, 5, 8, 11, 15].forEach((i, k) => {
    if (i >= spots.length) return;
    const note = parts.thought(`said${i}`, st.front, [spots[i][0] + 0.75, spots[i][1] + 1.05], 1.0, 0.62, [-1, -1]);
    parts.writing(`said${i}-lines`, note.root, [0, 0], 2, 0.7, 30 + i);
    kit.pop(note.root, tMany + 0.22 * k, 0.9, 0.3, tToo - 0.6 + 0.05 * k, 0.2);
    cues.push({ t: tMany + 0.22 * k, type: 'tick', pitch: 1.0 + 0.1 * k, gain: 0.6 });
  });
  [1, 6, 13].forEach((i, k) => {
    const mark = kit.text(`asked${i}`, '?', 0.7, kit.material(kit.PAPER), st.front, [spots[i][0] - 0.1, spots[i][1] + 1.05]);
    kit.appear(mark, tSome + 0.2 * k, tSome + 2.4, 0.2);
    cues.push({ t: tSome + 0.2 * k, type: 'blip', pitch: 0.9 + 0.1 * k, gain: 0.5 });
  });

  // One calls it an attack, and stays out.
  const d = parts.agent('d', st.cast, D, 0.8, 3);
  kit.pipLook(d, 0.3, 0.13, -0.03);
  const no = parts.thought('no', st.front, [D[0] - 1.5, D[1] + 1.35], 1.5, 1.1, [1, -1]);
  parts.cross('no-mark', no.root, [0, 0], 1.1);
  kit.pop(no.root, tOne, 1.0, 0.35, tToo - 0.4);
  cues.push({ t: tOne, type: 'tick', pitch: 0.5, gain: 1.3 });
  parts.mood(d, tOne, 'flat');
  parts.move(d.root, tOne + 1.0, D_AWAY, 1.2);
  kit.pipLook(d, tOne + 1.0, -0.13, 0.03);

  // ------------------------------------------------------------ Pip writes it, too, and then goes on
  const pip = parts.agent('pip', st.cast, PIP, 0.95);
  parts.mood(pip, 0, 'flat', 0);
  kit.pipLook(pip, 0.3, 0.14, 0.0);
  const note = parts.thought('note', st.front, NOTE, 2.4, 1.5, [0.3, -1]);
  kit.pop(note.root, tToo + 0.2, 1.0, 0.4, tThen - 0.3);
  cues.push({ t: tToo + 0.2, type: 'pop' });
  const lines = parts.writing('note-lines', note.root, [0, 0], 3, 1.6, 12);
  lines.bars.forEach((bar, k) => {
    kit.appear(bar, tToo + 0.7 + 0.22 * k, null, 0.08);
    if (k % 2 === 0) cues.push({ t: tToo + 0.7 + 0.22 * k, type: 'tick', pitch: 1.5, gain: 0.35 });
  });
  parts.mood(pip, tToo + 0.4, 'worried');

  const why = parts.thought('why', st.front, WHY, 4.6, 1.8, [0.6, -1]);
  kit.pop(why.root, tThen + 0.2, 1.0, 0.4);
  cues.push({ t: tThen + 0.2, type: 'pop' });
  const stuck = parts.group('why-stuck', why.root, [-1.45, 0]);
  parts.target('why-target', stuck, [0, 0], 0.3);
  parts.cross('why-cross', stuck, [0, 0], 1.2);
  kit.pop(stuck, tImp, 1.0, 0.3);
  cues.push({ t: tImp, type: 'tick', pitch: 0.6, gain: 1.2 });
  [[0.0, 0.25, 1], [0.55, -0.25, 2], [-0.45, -0.3, 4]].forEach(([x, y, which], k) => {
    const peer = parts.mini(`why-peer${k}`, why.root, [x + 0.1, y], 0.32, which);
    kit.pop(peer.root, tPeers + 0.12 * k, 0.32, 0.3);
    cues.push({ t: tPeers + 0.12 * k, type: 'blip', pitch: 0.9 + 0.15 * k, gain: 0.5 });
  });
  const onward = parts.group('why-on', why.root, [1.25, 0]);
  kit.branch('why-on-shaft', onward, [0, 0], [0.6, 0], kit.MINT, 0.14, 1.0);
  kit.shape('why-on-head', [[0.5, 0.3], [0.98, 0], [0.5, -0.3]], kit.material(kit.MINT), onward);
  kit.pop(onward, tCont, 1.0, 0.3);
  cues.push({ t: tCont, type: 'rise', dur: 0.6, pitch: 1.0, gain: 0.6 });
  parts.mood(pip, tImp, 'sad');
  kit.pipLook(pip, tPeers, 0.14, -0.02);
  parts.mood(pip, tPeers + 0.3, 'flat');
  kit.pipArm(pip, 'right', tCont, 80, 0.3);
  kit.pipArm(pip, 'right', tCont + 1.0, 18, 0.3);

  parts.vanish(why.root, tIn - 0.2, 0.25);
  parts.move(pip.root, tIn, [1.7, -2.3], 1.3);
  const crossed = kit.ring('crossed', st.front, [LINE, -2.0], 0.7, kit.CORAL, 0.09);
  kit.flash(crossed, tIn + 0.75, 0.7, 0.8);
  cues.push({ t: tIn, type: 'whoosh' }, { t: tIn + 0.75, type: 'tick', pitch: 0.5, gain: 1.4 });
  parts.live(pip, 12, 0, end);
  parts.live(b, 13);
  parts.live(d, 14);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [0.6, -0.2, 22]], [tKnew, [0.5, -0.2, 21.2]], [tKnew + 1.6, [-1.2, 0.2, 20.5]], [tToo - 0.2, [-1.4, 0.2, 20.2]],
    [tToo + 1.3, [-1.9, -0.4, 16]], [tThen, [-1.9, -0.3, 15.6]], [tPeers, [-1.6, -0.3, 16.4]], [tIn - 0.1, [-1.0, -0.5, 17]],
    [end, [0.8, -1.0, 17.5]],
  ]), 1.0);
  return cues;
}
