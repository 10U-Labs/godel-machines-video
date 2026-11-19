/* Scene 03: Improving itself.

A computer scientist sketches a machine as a blueprint, and it is named the
Gödel Machine. The blueprint becomes one working machine, tied to its own
code: it does its job while it rewrites that code, changes any part of
itself, and even changes the part that makes the changes. Then the machine
becomes Pip: only one Pip, changing itself again and again.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, hold, alpha, every } = kit;
  const radians = (deg) => deg * Math.PI / 180;

  const SHEET_AT = [1.3, 0.3];
  const [SHEET_W, SHEET_H] = [8.0, 5.8];
  const BOT_S = 1.7;
  const MACHINE_AT = [-3.4, 0.3];
  const CODE_AT = [3.6, 0.4];

  const cues = [];
  const end = sec(kit.frames());
  const tYear = T.start(0);
  const [tDraw0, tDraw1] = [T.at(0, 0.25), T.at(0, 0.7)];
  const tName = T.at(0, 0.8);
  const tOne = T.start(1);
  const tJob = T.at(1, 0.42);
  const tRewrite = T.at(1, 0.68);
  const tAny = T.start(2);
  const tChanger = T.at(2, 0.52);
  const tPip = T.start(3);
  const tOnly = T.at(3, 0.42);
  const tAgain = T.at(3, 0.66);

  kit.backdrop(31, kit.SKY_DEEP);
  kit.motes(undefined, 32, kit.SKY);
  const stage = kit.layer('stage', 1.0);

  // ------------------------------------------------------------ the scientist and the blueprint
  const sheet = kit.empty('sheet', stage, [SHEET_AT[0], SHEET_AT[1], kit.nextZ(stage)]);
  kit.shape('sheet-paper', kit.rrectPts(SHEET_W, SHEET_H, 0.15), kit.material('#1d3f8f', '#16307a'), sheet);
  const gridMat = kit.material(kit.SKY, null, 0.18, { over: kit.laid('#1d3f8f', 0.5, '#16307a') });
  for (let i = 1; i < 16; i++) {
    kit.shape(`grid-v${i}`, kit.rrectPts(0.025, SHEET_H - 0.3, 0), gridMat, sheet, [-SHEET_W / 2 + i * SHEET_W / 16, 0]);
  }
  for (let i = 1; i < 12; i++) {
    kit.shape(`grid-h${i}`, kit.rrectPts(SHEET_W - 0.3, 0.025, 0), gridMat, sheet, [0, -SHEET_H / 2 + i * SHEET_H / 12]);
  }
  // The blueprint's lines: dots around the machine's body, screen, eyes, and antenna.
  const dashes = parts.machineOutline().map(([x, y], k) => (
    kit.shape(`dash${k}`, kit.circlePts(0.045, null, null, 10), kit.material('#cfe9ff'), sheet, [x * BOT_S, y * BOT_S + 0.3])));
  const n = dashes.length;
  dashes.forEach((d, k) => {
    const t0 = mix(tDraw0, tDraw1, k / n);
    alpha(d, 1, 0.0);
    alpha(d, fr(t0), 0.0);
    alpha(d, fr(t0) + 2, 1.0);
    alpha(d, fr(tOne + 0.1), 1.0);
    alpha(d, fr(tOne + 0.4), 0.0);
  });
  for (let k = 0; k < 10; k++) {
    cues.push({ t: tDraw0 + (tDraw1 - tDraw0) * k / 10, type: 'tick', pitch: 0.8 + 0.04 * (k % 4), gain: 0.35 });
  }
  for (const f of every(1)) {
    const t = sec(f);
    const s = Math.max(0.001, kit.backOut((t - tYear - 0.2) / 0.5)) * (1 - span(t, tOne + 0.2, tOne + 0.6));
    key(sheet, 'scale', f, [Math.max(0.001, s), Math.max(0.001, s), 1]);
  }
  cues.push({ t: tYear + 0.2, type: 'pop', pitch: 0.8 });

  const who = kit.person('scientist', stage, [-4.6, 1.2], 0.78, { coat: '#8a5a3c', coatDeep: '#5e3b28', hair: '#c9c2b8' });
  const zw = who.root.z;
  for (const f of every(1)) {
    const t = sec(f);
    let x = mix(-9.5, -4.6, span(t, tYear, tYear + 0.9, kit.easeOut));
    x = mix(x, -10.5, span(t, tOne, tOne + 0.8));
    key(who.root, 'loc', f, [x, 1.2, zw]);
    const drawing = tDraw0 <= t && t <= tDraw1 ? 1.0 : 0.0;
    const reach = 58 + span(t, tDraw0 - 0.4, tDraw0) * 12 * (1 - span(t, tDraw1, tDraw1 + 0.4));
    key(who.arm, 'rot', f, radians(reach + drawing * 4 * Math.sin(t * 9)));
    key(who.head, 'rot', f, -0.06 * drawing + 0.03 * Math.sin(t * 0.8));
  }

  const year = kit.text('year', '2003', 0.62, kit.material(kit.PAPER), stage, [-6.9, 3.85], { align: 'LEFT' });
  const name = kit.text('name', 'Jürgen Schmidhuber', 0.3, kit.material(kit.MIST), stage, [-6.9, 3.3], { align: 'LEFT' });
  kit.fade(year, tYear + 0.3, tOne, 0.4);
  kit.fade(name, tYear + 0.8, tOne, 0.4);
  const title = kit.text('title', 'Gödel Machine', 0.6, kit.material(kit.PAPER), stage, [SHEET_AT[0], -3.25]);
  kit.fade(title, tName, tAny - 0.5, 0.5);
  cues.push({ t: tName, type: 'chime', gain: 0.6 });

  // ------------------------------------------------------------ the machine and its own code
  const m = parts.pip('machine', stage, MACHINE_AT, BOT_S, kit.SKY, kit.SKY_DEEP);
  const p = parts.pip('pip', stage, [0, 0.2], 1.6);
  const zm = m.root.z;
  for (const f of every(1)) {
    const t = sec(f);
    let x = mix(SHEET_AT[0], MACHINE_AT[0], span(t, tOne + 0.5, tOne + 1.3));
    x = mix(x, 0.0, span(t, tPip, tPip + 0.7));
    const grown = Math.max(0.001, kit.backOut((t - tOne - 0.2) / 0.45)) * (1 - span(t, tPip + 0.7, tPip + 0.95));
    key(m.root, 'loc', f, [x, mix(SHEET_AT[1] + 0.5, MACHINE_AT[1], span(t, tOne + 0.5, tOne + 1.3)), zm]);
    key(m.root, 'scale', f, BOT_S * Math.max(0.001, grown));
  }
  parts.pipIdle(m, undefined, undefined, 0.5);
  parts.pipBlink(m, [tOne + 2.5, tRewrite + 1.4, tAny + 2.3]);
  cues.push({ t: tOne + 0.2, type: 'pop' });

  const code = parts.program('code', stage, CODE_AT, { rows: 7, w: 3.4, h: 4.4, seed: 31 });
  const zc = code.root.z;
  for (const f of every(1)) {
    const t = sec(f);
    const s = Math.max(0.001, kit.backOut((t - tOne - 1.0) / 0.45)) * (1 - span(t, tPip, tPip + 0.4));
    key(code.root, 'scale', f, [Math.max(0.001, s), Math.max(0.001, s), 1]);
    key(code.root, 'loc', f, [CODE_AT[0], CODE_AT[1], zc]);
  }
  for (let k = 0; k < 12; k++) {
    const x = mix(MACHINE_AT[0] + 1.7, CODE_AT[0] - 1.8, k / 11);
    const d = kit.shape(`tether${k}`, kit.circlePts(0.06, null, null, 10), kit.material(kit.SKY, null, 0.8), stage, [x, MACHINE_AT[1] + 0.1 * Math.sin(k)]);
    alpha(d, 1, 0.0);
    alpha(d, fr(tOne + 1.2 + 0.04 * k), 0.0);
    alpha(d, fr(tOne + 1.3 + 0.04 * k), 1.0);
    alpha(d, fr(tPip), 1.0);
    alpha(d, fr(tPip + 0.3), 0.0);
  }

  // the machine does its job: small programs come along, and each leaves fixed
  for (let k = 0; k < 5; k++) {
    const t0 = tJob + 0.75 * k;
    const job = parts.program(`task${k}`, stage, [-9, -3.0], { rows: 3, w: 2.0, h: 1.4, seed: 40 + k, mistake: 1, scale: 0.68 });
    const zj = job.root.z;
    const tMid = t0 + 0.7;
    for (const f of every(1, fr(t0 - 0.1), fr(t0 + 1.6))) {
      const t = sec(f);
      let x = mix(-9.5, MACHINE_AT[0], span(t, t0, tMid, kit.easeOut));
      x = mix(x, 9.5, span(t, tMid + 0.15, t0 + 1.6, (v) => v * v));
      key(job.root, 'loc', f, [x, -3.0, zj]);
    }
    for (const ob of job.bad.bars) {
      alpha(ob, fr(tMid), 1.0);
      alpha(ob, fr(tMid + 0.1), 0.0);
    }
    for (const ob of job.good) {
      alpha(ob, fr(tMid), 0.0);
      alpha(ob, fr(tMid + 0.1), 1.0);
    }
    cues.push({ t: tMid, type: 'blip', pitch: 1.1 + 0.05 * k, gain: 0.5 });
  }
  parts.pipLook(m, tJob, -0.05, -0.12);

  // ... and while it works, it rewrites its own code
  parts.pipLook(m, tRewrite - 0.3, 0.13, 0.0);
  const onPage = { over: kit.laid(kit.INK700, 0.5, kit.INK800) };
  const lit = [];
  for (const r of [1, 3, 5]) {
    const y = code.rows[r][0].y;
    const hl = kit.shape(`row${r}-flash`, kit.rrectPts(3.2, 0.36, 0.18), kit.material(kit.AMBER, null, 0.35, onPage), code.root, [0, y], { lift: -0.003 });
    alpha(hl, 1, 0.0);
    lit.push([r, hl]);
  }
  const rnd = new kit.Random(3);
  lit.forEach(([r, hl], k) => {
    const t0 = tRewrite + 0.45 * k;
    for (const [f, a] of [[fr(t0), 0.0], [fr(t0) + 3, 1.0], [fr(t0 + 0.6), 0.0]]) alpha(hl, f, a);
    for (const ob of code.rows[r]) {
      hold(ob, 'scale', fr(t0));
      key(ob, 'scale', fr(t0) + 4, [0.001, 1, 1]);
      key(ob, 'scale', fr(t0) + 9, [0.6 + 0.7 * rnd.random(), 1, 1]);
    }
    cues.push({ t: t0, type: 'tick', pitch: 1.3, gain: 0.6 });
  });
  parts.pipArm(m, 'right', tRewrite - 0.3, 80, 0.25);
  parts.pipArm(m, 'right', tRewrite + 1.4, 18, 0.3);

  // ------------------------------------------------------------ any part, even the part that changes
  const spots = [[0, 1.15], [-0.95, -0.6], [0.95, -0.6], [0, 0.15]];       // antenna, hands, face (in machine units)
  spots.forEach(([dx, dy], k) => {
    const t0 = tAny + 0.35 + 0.45 * k;
    const ring = kit.shape(`part-ring${k}`, kit.circlePts(0.5), kit.glowMaterial(kit.AMBER, 0.9, 0.7), stage, [0, 0], { lift: 0.2 });
    const zr = ring.z;
    for (const f of every(1, fr(t0 - 0.1), fr(t0 + 0.6))) {
      const t = sec(f);
      const q = span(t, t0, t0 + 0.5, (v) => v);
      key(ring, 'loc', f, [MACHINE_AT[0] + dx * BOT_S, MACHINE_AT[1] + dy * BOT_S, zr]);
      key(ring, 'scale', f, [0.6 + 1.6 * q, 0.6 + 1.6 * q, 1]);
      alpha(ring, f, Math.sin(Math.PI * q));
    }
    alpha(ring, 1, 0.0);
    cues.push({ t: t0, type: 'pop', pitch: 1.0 + 0.1 * k, gain: 0.6 });
  });
  parts.pipEyes(m, tAny + 1.65, 1.25, 1.25, 0.15);
  parts.pipEyes(m, tAny + 2.1, 1.0, 1.0, 0.2);

  // the part that makes the changes: a pencil beside one line of the code, which rewrites itself
  const row = 6;
  const y = code.rows[row][0].y;
  const pencil = kit.empty('pencil', code.root, [-3.4 / 2 - 0.35, y, kit.nextZ(code.root)]);
  kit.shape('pencil-glow', kit.circlePts(0.6), kit.glowMaterial(kit.AMBER, 0.7), pencil);
  kit.shape('pencil-body', [[-0.07, 0.24], [0.07, 0.24], [0.07, -0.12], [0, -0.26], [-0.07, -0.12]], kit.material(kit.AMBER, kit.AMBER_DEEP), pencil);
  kit.shape('pencil-tip', [[-0.035, -0.19], [0.035, -0.19], [0, -0.26]], kit.material(kit.INK900), pencil);
  pencil.rot = -0.6;
  pencil.sx = pencil.sy = pencil.sz = 0.001;
  hold(pencil, 'scale', 1);
  hold(pencil, 'scale', fr(tOne + 1.2));
  key(pencil, 'scale', fr(tOne + 1.5), [1, 1, 1]);
  const ring = kit.shape('changer-ring', kit.rrectPts(3.9, 0.5, 0.25), kit.material(kit.AMBER, null, 0.4, onPage), code.root, [-0.25, y], { lift: -0.003 });
  alpha(ring, 1, 0.0);
  for (const f of every(1, fr(tChanger - 0.1), fr(tPip))) {
    const t = sec(f);
    alpha(ring, f, span(t, tChanger, tChanger + 0.3) * (1 - span(t, tPip - 0.6, tPip - 0.2)) * (0.75 + 0.25 * Math.sin((t - tChanger) * 8)));
    const spin = span(t, tChanger + 0.5, tChanger + 1.1);
    const pulse = 1 + 0.5 * Math.sin(Math.PI * spin);
    key(pencil, 'rot', f, -0.6 - 2 * Math.PI * spin);
    key(pencil, 'scale', f, [pulse, pulse, 1]);
  }
  for (const ob of code.rows[row]) {
    hold(ob, 'scale', fr(tChanger + 0.6));
    key(ob, 'scale', fr(tChanger + 0.75), [0.001, 1, 1]);
    key(ob, 'scale', fr(tChanger + 1.0), [1.3, 1, 1]);
  }
  cues.push({ t: tChanger, type: 'tick', pitch: 0.9 });
  cues.push({ t: tChanger + 0.5, type: 'rise', dur: 0.6, pitch: 1.2, gain: 0.6 });

  // ------------------------------------------------------------ if Pip were a Gödel Machine
  for (const f of every(1)) {
    const t = sec(f);
    key(p.root, 'scale', f, 1.6 * Math.max(0.001, kit.backOut((t - tPip - 0.8) / 0.45)));
  }
  parts.pipIdle(p);
  cues.push({ t: tPip + 0.75, type: 'pop', pitch: 1.1 });
  const spot = kit.shape('spotlight', kit.circlePts(4.0), kit.glowMaterial(kit.PAPER, 0.18, 1.0), stage, [0, 0.2], { lift: -0.01 });
  alpha(spot, 1, 0.0);
  kit.fade(spot, tOnly, null, 0.6);

  // one Pip, changing itself: each change ripples out from Pip, and Pip itself is a little different after it
  const changes = [tAgain, tAgain + 0.75, tAgain + 1.5];
  changes.forEach((t0, k) => {
    const ripple = kit.shape(`ripple${k}`, kit.arcPts(1.6, 0.12, 0, 360, 48), kit.material(kit.MINT, null, 0.8), stage, [0, 0.2], { lift: 0.2 });
    alpha(ripple, 1, 0.0);
    for (const f of every(1, fr(t0 - 0.05), fr(t0 + 0.8))) {
      const q = span(sec(f), t0, t0 + 0.7, (v) => v);
      key(ripple, 'scale', f, [1 + 1.4 * q, 1 + 1.4 * q, 1]);
      alpha(ripple, f, 1 - q);
    }
    cues.push({ t: t0, type: 'rise', dur: 0.4, pitch: 1.0 + 0.15 * k, gain: 0.6 });
  });
  const a = p.antenna;
  hold(a, 'scale', fr(changes[0]));
  key(a, 'scale', fr(changes[0]) + 5, [1.15, 1.45, 1]);
  for (const e of p.eyeList) {
    hold(e, 'scale', fr(changes[1]));
    key(e, 'scale', fr(changes[1]) + 5, [1.25, 1.25, 1]);
  }
  for (const side of ['left', 'right']) {
    const sh = p.arms[side];
    hold(sh, 'scale', fr(changes[2]));
    key(sh, 'scale', fr(changes[2]) + 5, [1.2, 1.3, 1]);
  }
  parts.pipArm(p, 'right', changes[2] + 0.3, 140, 0.25);
  parts.pipArm(p, 'left', changes[2] + 0.3, 140, 0.25);

  // ------------------------------------------------------------ camera
  const path = (t) => {
    const q = kit.smooth(t / end);
    const close = span(t, tPip, tPip + 1.5);
    return [mix(0.1 * q, 0.0, close), 0.05 * q, kit.H0 - 0.7 * q - 3.0 * close];
  };

  kit.camera(path, 1.0);
  return cues;
}
