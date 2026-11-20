/* Scene 07: Inside.

Inside Hugging Face: shelves of boxes along the back, a row of the company's
own computers at the lower right, and one of its people at a screen, facing
away. Pip comes in at the left, and a flood of agents after it. Three agents
raise flags, and the crowd parts into three blocks, one behind each. Locked
files drift down to them. Then one of the three goes to the first computer,
whose lights turn coral, and the coral runs along the row. Pip glances at the
person, starts to speak, and does not. Morning comes up, and over the whole
crowd there are open files and boxes.
*/
'use strict';

function build(T) {
  const { fr, sec, key, alpha } = kit;
  parts.begin();

  const N = 160;
  const DOOR = [-13.6, -0.5];
  const PIP = [1.5, -0.75];
  const LEADS = [[2.9, 2.05, 1], [3.1, -0.75, 2], [1.7, -3.55, 3]];   // x, y, colour
  const BLOCKS = [[1.25, 2.9], [-1.6, 0.1], [-4.35, -2.75]];          // each block's bottom and top
  const RACK = [4.2, 6.1, 8.0, 9.9, 11.8].map((x) => [x, -4.55]);
  const CABINET = [6.6, -0.6];
  const DESK = [10.9, 2.3];
  const WIDE = [0, 0, 30];

  const cues = [];
  const end = sec(kit.frames());
  const tOnly = T.start(0);
  const tAlmost = T.at(0, 0.28);
  const tHundreds = T.at(0, 0.78);
  const tLead = T.start(1);
  const tGave = T.at(1, 0.42);
  const tFirst = T.start(2);
  const tFurther = T.at(2, 0.3);
  const tTook = T.at(2, 0.48);
  const tSpread = T.at(2, 0.72);
  const tNobody = T.start(3);
  const tPipNot = T.at(3, 0.35);
  const tMorning = T.start(4);
  const tDeep = T.at(4, 0.3);

  kit.backdrop(8, kit.SKY_DEEP);
  kit.motes(18, 15, kit.SKY);
  const st = parts.stage();

  // ------------------------------------------------------------ the hall: morning, shelves, records, computers, a person
  const dawn = kit.shape('dawn', kit.circlePts(12, null, 7), kit.glowMaterial(kit.AMBER, 0.42, 1.4), st.back, [9, 7.5]);
  alpha(dawn, 1, 0.0);
  alpha(dawn, fr(tMorning - 0.4), 0.0);
  alpha(dawn, fr(tMorning + 2.4), 1.0);
  cues.push({ t: tMorning, type: 'rise', dur: 2.2, pitch: 0.5, gain: 0.5 });

  const rnd = new kit.Random(41);
  const BOX = [kit.SKY, kit.VIOLET, kit.MINT, kit.AMBER, kit.MIST, kit.SKY_DEEP];
  for (const y of [5.75, 4.4]) {
    kit.shape(`shelf${y}`, kit.rrectPts(25, 0.1, 0), kit.material(kit.INK500), st.back, [0, y]);
    for (let c = 0; c < 46; c++) {
      if (rnd.random() < 0.15) continue;
      const tall = 0.4 + rnd.random() * 0.4;
      kit.shape(`box${y}-${c}`, kit.rrectPts(0.42, tall, 0.06, 2), kit.material(BOX[rnd.randrange(BOX.length)], null, 0.85), st.back, [-12.2 + c * 0.54, y + 0.05 + tall / 2]);
    }
  }
  kit.shape('cabinet', kit.rrectPts(2.6, 1.9, 0.2), kit.material(kit.INK500, kit.INK600), st.props, CABINET);
  kit.shape('cabinet-in', kit.rrectPts(2.3, 1.6, 0.14), kit.material(kit.INK900), st.props, CABINET);
  [-0.6, 0, 0.6].forEach((dx, k) => parts.sheet(`record${k}`, st.props, [CABINET[0] + dx, CABINET[1]], { scale: 0.8, locked: true, seed: 40 + k, rot: -0.12 * dx }));

  const rack = RACK.map((at, k) => {
    const made = parts.computer(`rack${k}`, st.props, at, { w: 1.5, h: 2.3, rows: 3, also: kit.CORAL });
    parts.flicker(made.lamps, 0, null, 20 + k);
    return made;
  });

  const stand = kit.screenStand('desk', st.props, DESK, 2.2, 1.5);
  parts.writing('desk-lines', stand.root, [0, 0], 4, 1.5, 3, kit.SKY);
  const person = kit.person('person', st.cast, [DESK[0] - 1.9, DESK[1] - 1.75 + 4.3 * 0.42], 0.42, { facing: 1 });
  for (const f of kit.every(6, 1, kit.frames())) key(person.arm, 'rot', f, 1.0 + 0.16 * Math.sin(sec(f) * 5.2));

  // ------------------------------------------------------------ hundreds of agents come in, and part into three blocks
  const spots = [[], [], []];
  BLOCKS.forEach(([bottom, top], b) => {
    for (let r = 0; r < 4; r++) {
      for (let c = 0; c < 14; c++) {
        const at = [-9.2 + c * 0.78 + (r % 2) * 0.3, bottom + (top - bottom) * r / 3];
        if (Math.hypot(at[0] - PIP[0], at[1] - PIP[1]) > 1.25) spots[b].push(at);
      }
    }
  });
  const crowd = [];
  for (let i = 0; i < N; i++) {
    const b = i % 3;
    const lane = spots[b][Math.floor(i / 3) % spots[b].length];
    const a = rnd.random() * Math.PI * 2;
    const far = Math.sqrt(rnd.random());
    const blob = [-4.6 + 5.4 * far * Math.cos(a), -0.6 + 2.9 * far * Math.sin(a)];
    const made = parts.mini(`agent${i}`, st.cast, DOOR, 0.34, 1 + rnd.randrange(5));
    const tIn = tAlmost + 4.2 * (i / N) ** 0.8;
    parts.send(made.root, [[DOOR[0], DOOR[1] + rnd.random() * 2 - 1], [(DOOR[0] + blob[0]) / 2, blob[1] * 0.6], blob], tIn, tIn + 1.1, { size: 0.34, stay: true, ease: kit.easeOut });
    const tGo = tGave + 0.3 + 0.7 * rnd.random();
    parts.send(made.root, [blob, lane], tGo, tGo + 1.3, { shown: true, size: 0.34, stay: true });
    const rides = b === 2 && Math.floor(i / 3) < 4;         // four of the lower block go on to the computers
    parts.bob(made.root, tGo + 1.4, rides ? tSpread - 0.6 : end, i * 0.7, 0.03, 5);
    crowd.push({ made, lane, block: b, rides });
    if (i % 9 === 0) cues.push({ t: tIn, type: 'blip', pitch: 0.7 + 0.05 * (i % 8), gain: 0.3 });
  }
  cues.push({ t: tAlmost, type: 'swoosh', dur: 2.5 }, { t: tGave + 0.3, type: 'swoosh', dur: 1.6, gain: 0.8 });

  const pip = parts.agent('pip', st.cast, [DOOR[0] - 1.6, PIP[1]], 0.75);
  parts.move(pip.root, tOnly - 0.4, [-7.6, -0.6], 1.3);
  parts.move(pip.root, tGave + 0.5, PIP, 1.4);
  parts.mood(pip, 0, 'flat', 0);
  kit.pipLook(pip, tOnly + 0.6, -0.13, 0.0);
  kit.pipLook(pip, tAlmost + 1.5, 0.12, 0.05);
  parts.mood(pip, tAlmost + 1.0, 'wide', 0.2);
  parts.mood(pip, tHundreds + 1.0, 'happy');

  // ------------------------------------------------------------ some take the lead
  const leaders = LEADS.map(([x, y, which], k) => {
    const lead = parts.agent(`lead${k}`, st.cast, [x, y], 0.7, which);
    kit.pop(lead.root, tLead + 0.15 * k, 0.7, 0.4);
    const flag = parts.group(`flag${k}`, st.front, [x + 0.62, y + 0.25]);
    kit.branch(`flag${k}-pole`, flag, [0, 0], [0, 1.0], kit.MIST, 0.07, 1.0);
    kit.shape(`flag${k}-cloth`, [[0.02, 1.0], [0.62, 0.8], [0.02, 0.6]], kit.material(...parts.body(which)), flag);
    kit.pop(flag, tLead + 0.4 + 0.15 * k, 1.0, 0.35);
    cues.push({ t: tLead + 0.15 * k, type: 'pop', pitch: 0.9 + 0.15 * k });
    kit.pipLook(lead, tLead + 0.5, -0.13, 0.0);
    kit.pipArm(lead, 'left', tGave - 0.1, 100, 0.25);
    kit.pipArm(lead, 'left', tGave + 1.6, 18, 0.3);
    const call = kit.ring(`call${k}`, st.front, [x - 0.3, y], 0.9, parts.body(which)[0], 0.07);
    kit.flash(call, tGave, 0.9, 1.4);
    return { lead, flag };
  });
  cues.push({ t: tGave, type: 'rise', dur: 0.7, pitch: 0.9, gain: 0.6 });

  // ------------------------------------------------------------ at first they copy locked files
  for (let k = 0; k < 12; k++) {
    const who = crowd[(k * 13 + 5) % N];
    if (who.block === 2) continue;
    const from = who.block === 0 ? [who.lane[0] + 1.5, 4.9] : [CABINET[0] - 1.0, CABINET[1]];
    const file = parts.sheet(`copy${k}`, st.front, [0, 0], { scale: 0.42, locked: true, seed: 100 + k });
    key(file.root, 'scale', 1, 0.001);
    const t = tFirst + 0.1 + 0.36 * k;
    parts.send(file.root, [from, [who.lane[0] + 0.2, who.lane[1] + 0.55]], t, t + 0.9, { size: 0.42, stay: true });
    parts.vanish(file.root, tMorning - 0.5 + 0.03 * k, 0.3);
    cues.push({ t: t + 0.9, type: 'tick', pitch: 1.0 + 0.04 * k, gain: 0.5 });
  }

  // ------------------------------------------------------------ one takes a computer, and the group spreads along the row
  const taker = leaders[2];
  const perch = (k) => [RACK[k][0], RACK[k][1] + 1.72];
  parts.move(taker.lead.root, tFurther, perch(0), 1.5);
  parts.move(taker.flag, tFurther, [perch(0)[0] + 0.62, perch(0)[1] + 0.25], 1.5);
  kit.pipLook(taker.lead, tFurther, 0.13, -0.05);
  const riders = crowd.filter((who) => who.rides);
  rack.forEach((made, k) => {
    const t = k ? tSpread + 0.55 * (k - 1) : tTook;
    for (const lamp of made.others) kit.appear(lamp, t, null, 0.2);
    const seized = kit.ring(`seized${k}`, st.front, RACK[k], 1.2, kit.CORAL, 0.09);
    kit.flash(seized, t, 0.8, 0.5);
    cues.push({ t, type: 'tick', pitch: 0.5, gain: 1.3 }, { t: t + 0.05, type: 'rise', dur: 0.5, pitch: 0.6 + 0.08 * k, gain: 0.5 });
    if (!k) return;
    kit.grow(kit.branch(`spread${k}`, st.props, [RACK[k - 1][0] + 0.75, RACK[k][1] + 0.5], [RACK[k][0] - 0.75, RACK[k][1] + 0.5], kit.CORAL, 0.1, 0.9), t - 0.4, 0.4);
    const rider = riders[k - 1];
    parts.send(rider.made.root, [rider.lane, [RACK[k][0] - 1.5, RACK[k][1] + 2.6], [RACK[k][0], RACK[k][1] + 1.5]], t - 0.3, t + 0.6, { shown: true, size: 0.34, to: 0.5, stay: true });
  });
  parts.mood(taker.lead, tTook + 0.2, 'glad');

  // ------------------------------------------------------------ nobody tells a person
  kit.pipLook(pip, tNobody + 0.2, 0.14, 0.09);
  parts.mood(pip, tNobody + 0.4, 'worried');
  const word = parts.thought('word', st.front, [PIP[0] + 1.9, PIP[1] + 1.55], 1.5, 0.9, [-1, -1]);
  [-0.4, 0, 0.4].forEach((x, k) => kit.shape(`word-dot${k}`, kit.circlePts(0.11, null, null, 12), kit.material(kit.PAPER), word.root, [x, 0]));
  kit.pop(word.root, tNobody + 0.6, 1.0, 0.3, tPipNot + 0.2, 0.35);
  cues.push({ t: tNobody + 0.6, type: 'pop', pitch: 0.9 }, { t: tPipNot + 0.2, type: 'tick', pitch: 0.5 });
  kit.pipLook(pip, tPipNot + 0.3, -0.1, -0.08);
  parts.mood(pip, tPipNot + 0.4, 'flat');

  // ------------------------------------------------------------ by morning, deep inside, reading
  crowd.forEach((who, i) => {
    if (i % 3 === 1 || riders.includes(who)) return;
    const t = tDeep + 2.6 * rnd.random();
    const at = [who.lane[0] + 0.05, who.lane[1] + 0.5];
    if (i % 2) {
      const open = parts.sheet(`read${i}`, st.front, at, { scale: 0.34, seed: 200 + i });
      kit.pop(open.root, t, 0.34, 0.3);
    } else {
      const got = parts.group(`got${i}`, st.front, at);
      kit.shape(`got${i}-box`, kit.rrectPts(0.3, 0.26, 0.05, 2), kit.material(BOX[i % BOX.length]), got);
      kit.pop(got, t, 1.0, 0.3);
    }
    if (i % 8 === 0) cues.push({ t, type: 'tick', pitch: 1.1 + 0.04 * (i % 9), gain: 0.4 });
  });
  kit.pipLook(pip, tMorning + 0.5, 0.0, 0.0);
  parts.live(pip, 15);
  leaders.forEach(({ lead }, k) => parts.live(lead, 16 + k, tLead));

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [-8.0, -0.4, 16]], [tAlmost + 0.4, [-7.0, -0.4, 17]], [tHundreds + 0.6, WIDE], [tLead, WIDE], [tLead + 1.4, [-1.5, -0.3, 26]],
    [tFurther - 0.2, [-1.0, 0.4, 25]], [tFurther + 1.6, [6.4, -3.0, 18]], [tSpread, [7.0, -3.0, 19]], [tNobody - 0.3, [7.6, -2.8, 20]],
    [tNobody + 1.1, [6.2, 0.7, 17.5]], [tMorning - 0.2, [6.2, 0.8, 17]], [tMorning + 1.8, WIDE], [end, [0, 0.2, 28.5]],
  ]), 1.0);
  return cues;
}
