/* Scene 00: A program that fixes programs.

Pip pops in and waves. A program with a red mistake slides in; Pip spots the
mistake and fixes it. Other programs like Pip appear all around, then go. A
new program drops in, and its title bar shows Pip's own face.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, hold, alpha, every } = kit;

  const HOME = [0.0, -0.3];
  const WORK = [-3.7, -0.3];
  const CARD = [2.9, 0.15];
  const PIP_SCALE = 1.35;

  const CROWD = [  // x, y, depth, scale, colour, deep colour
    [-6.3, 2.6, -2.5, 0.55, kit.SKY, kit.SKY_DEEP],
    [-3.1, 3.2, -4.0, 0.45, kit.VIOLET, kit.VIOLET_DEEP],
    [3.4, 3.1, -3.2, 0.5, kit.AMBER, kit.AMBER_DEEP],
    [6.4, 2.2, -1.5, 0.6, kit.CORAL, kit.CORAL_DEEP],
    [-6.8, -1.0, -1.0, 0.65, kit.VIOLET, kit.VIOLET_DEEP],
    [6.7, -1.4, -3.6, 0.5, kit.SKY, kit.SKY_DEEP],
    [-4.6, -3.3, 0.3, 0.6, kit.AMBER, kit.AMBER_DEEP],
    [4.4, -3.4, -0.6, 0.62, kit.MIST, kit.SLATE],
    [-0.6, 3.6, -5.0, 0.4, kit.CORAL, kit.CORAL_DEEP],
    [0.9, -3.9, -4.5, 0.42, kit.SKY, kit.SKY_DEEP],
    [-8.4, 0.9, -4.8, 0.4, kit.AMBER, kit.AMBER_DEEP],
    [8.6, 0.6, -5.2, 0.4, kit.VIOLET, kit.VIOLET_DEEP],
  ];

  const cues = [];
  const end = sec(kit.frames());
  const tHello = T.start(0);
  const tJob = T.start(1);
  const tFind = T.at(1, 0.5);
  const tFix = T.at(1, 0.84);
  const tMadeUp = T.start(2);
  const tReal = T.at(2, 0.4);
  const tCrowdOut = T.end(2) + 0.05;
  const tNew = T.start(3);
  const tOwn = T.at(3, 0.56);

  kit.backdrop();
  kit.motes();
  const stage = kit.layer('stage', 1.0);

  // ------------------------------------------------------------ Pip
  const p = parts.pip('pip', stage, HOME, PIP_SCALE);
  const label = kit.text('pip-name', 'Pip', 0.55, kit.material(kit.PAPER), stage, [0, -2.25]);
  kit.fade(label, tHello + 0.5, tJob - 0.5);

  const pipPlace = (t) => {
    let [x, y] = HOME;
    for (const [t0, dest] of [[tJob, WORK], [tMadeUp + 0.1, HOME], [tNew, WORK]]) {
      const q = span(t, t0, t0 + 0.8);
      [x, y] = [mix(x, dest[0], q), mix(y, dest[1], q)];
    }
    x -= 0.25 * span(t, tOwn, tOwn + 0.25, kit.easeOut) * (1 - 0.6 * span(t, tOwn + 0.4, tOwn + 1.2));
    return [x, y];
  };

  const zRoot = p.root.z;
  for (const f of every(1)) {
    const t = sec(f);
    const [x, y] = pipPlace(t);
    key(p.root, 'loc', f, [x, y, zRoot]);
    key(p.root, 'scale', f, PIP_SCALE * Math.max(0.001, kit.backOut((t - tHello) / 0.5)));
  }
  parts.pipIdle(p);
  cues.push({ t: tHello, type: 'pop' });

  parts.pipWave(p, tHello + 0.7, tHello + 2.6);
  parts.pipBlink(p, [3.6, tJob + 1.3, tMadeUp + 1.6, tReal + 2.0, tNew + 1.1]);

  // ------------------------------------------------------------ a program with a mistake
  const a = parts.program('job', stage, [14, CARD[1]], { rows: 7, seed: 4, mistake: 3 });
  const zc = a.root.z;
  for (const f of every(1)) {
    const t = sec(f);
    let x = mix(14.0, CARD[0], span(t, tJob, tJob + 0.9, kit.easeOut));
    x = mix(x, 15.0, span(t, tMadeUp, tMadeUp + 0.8, (q) => q * q));
    key(a.root, 'loc', f, [x, CARD[1], zc]);
  }
  cues.push({ t: tJob, type: 'whoosh' });
  cues.push({ t: tMadeUp, type: 'whoosh', gain: 0.7 });

  parts.pipLook(p, tJob + 0.5, 0.13, 0.0);
  for (const f of every(1, fr(tJob), fr(tFix))) {  // the mistake twitches until it is fixed
    const t = sec(f);
    const jig = 0.035 * Math.sin(t * 31) * (0.5 + 0.5 * Math.sin(t * 5.3));
    for (const ob of a.bad.bars) key(ob, 'rot', f, jig);
  }
  for (const ob of a.bad.bars) key(ob, 'rot', fr(tFix) + 1, 0);

  const ring = a.bad.ring;
  for (const f of every(1, fr(tFind), fr(tFix + 0.6))) {
    const t = sec(f);
    const on = span(t, tFind, tFind + 0.25) * (1 - span(t, tFix, tFix + 0.5));
    alpha(ring, f, on * (0.75 + 0.25 * Math.sin((t - tFind) * 9)));
  }
  cues.push({ t: tFind, type: 'tick' });
  cues.push({ t: tFind + 0.12, type: 'tick', pitch: 1.2 });

  // Pip reaches out, a spark flies to the mistake, and the red bars turn mint.
  parts.pipArm(p, 'right', tFix - 0.55, 82, 0.25);
  const hand = [WORK[0] + PIP_SCALE * 1.3, WORK[1] + PIP_SCALE * -0.27];
  const target = [CARD[0] + a.bad.x, CARD[1] + a.bad.y];
  const spark = kit.shape('spark', kit.starPts(0.32, 0.08), kit.material('#eafff9'), stage, [0, 0], { lift: 0.3 });
  const sparkGlow = kit.shape('spark-glow', kit.circlePts(0.9), kit.glowMaterial(kit.MINT, 0.8), stage, [0, 0], { lift: 0.29 });
  const [zs, zg] = [spark.z, sparkGlow.z];
  const tFly = tFix - 0.3;
  for (const f of every(1)) {
    const t = sec(f);
    const q = span(t, tFly, tFix, (v) => v);
    let [x, y] = [mix(hand[0], target[0], q), mix(hand[1], target[1], q) + 0.9 * Math.sin(Math.PI * q)];
    const flying = tFly <= t && t <= tFix ? 1.0 : 0.0;
    const burst = span(t, tFix, tFix + 0.5, kit.easeOut);
    const bursting = tFix < t && t <= tFix + 0.6 ? 1.0 : 0.0;
    if (bursting) [x, y] = target;
    const s = 0.001 + flying * 0.6 + bursting * (0.6 + 1.6 * burst);
    const shown = flying + bursting * (1 - burst);
    key(spark, 'loc', f, [x, y, zs]);
    key(spark, 'scale', f, [s, s, 1]);
    key(spark, 'rot', f, t * 4);
    alpha(spark, f, shown);
    key(sparkGlow, 'loc', f, [x, y, zg]);
    key(sparkGlow, 'scale', f, [s * 1.3, s * 1.3, 1]);
    alpha(sparkGlow, f, shown);
  }
  for (const ob of a.bad.bars) {
    alpha(ob, fr(tFix), 1.0);
    alpha(ob, fr(tFix + 0.2), 0.0);
  }
  for (const ob of a.good) {
    alpha(ob, fr(tFix), 0.0);
    alpha(ob, fr(tFix + 0.2), 1.0);
  }
  cues.push({ t: tFly, type: 'rise', dur: 0.3, pitch: 1.5, gain: 0.6 });
  cues.push({ t: tFix, type: 'chime' });

  parts.pipArm(p, 'right', tFix + 0.35, 150, 0.2);       // a small cheer
  parts.pipEyes(p, tFix + 0.1, 1.1, 0.55);                // happy squint
  parts.pipArm(p, 'right', tMadeUp - 0.2, 18, 0.35);
  parts.pipEyes(p, tMadeUp - 0.1, 1.0, 1.0);
  parts.pipLook(p, tMadeUp + 0.2, 0.0, 0.0);

  // ------------------------------------------------------------ other programs like Pip
  CROWD.forEach(([x, y, z, sc, col, deep], i) => {
    const lay = kit.layer(`crowd${i}`, z);
    const bot = parts.pip(`bot${i}`, lay, [x, y], sc, col, deep);
    const tIn = tReal + 0.09 * i;
    const zb = bot.root.z;
    for (const f of every(1, fr(tReal - 0.2), fr(tCrowdOut + 0.8))) {
      const t = sec(f);
      const grown = kit.backOut((t - tIn) / 0.45) * (1 - span(t, tCrowdOut + 0.04 * i, tCrowdOut + 0.04 * i + 0.35));
      key(bot.root, 'scale', f, sc * Math.max(0.001, grown));
    }
    bot.root.sx = bot.root.sy = bot.root.sz = 0.001;
    hold(bot.root, 'scale', 1);
    key(bot.root, 'loc', fr(tReal), [x, y, zb]);
    key(bot.root, 'loc', fr(tCrowdOut + 0.8), [x + 0.25 * (x > 0 ? 1 : -1), y + 0.15, zb]);
    parts.pipIdle(bot, tReal - 0.2, tCrowdOut + 0.8, i * 0.7, 3);
    parts.pipLook(bot, tIn + 0.5, x > 0 ? -0.06 : 0.06, y > 0 ? -0.03 : 0.03);
    if (i % 3 === 1) parts.pipWave(bot, tIn + 0.6, tIn + 1.8, 8 + i % 4);
    cues.push({ t: tIn, type: 'blip', pitch: 0.8 + 0.06 * (i % 7), gain: 0.45 });
  });
  parts.pipLook(p, tReal + 0.5, -0.12, 0.05);
  parts.pipLook(p, tReal + 1.6, 0.12, 0.05);
  parts.pipLook(p, tCrowdOut, 0.0, 0.0);

  // ------------------------------------------------------------ a new program: Pip's own code
  const b = parts.program('own', stage, [CARD[0], 10], { rows: 7, seed: 9, tabIcon: true });
  const zb = b.root.z;
  for (const f of every(1)) {
    const t = sec(f);
    const y = mix(10.0, CARD[1], span(t, tNew, tNew + 0.9, kit.backOut));
    key(b.root, 'loc', f, [CARD[0], y, zb]);
  }
  cues.push({ t: tNew, type: 'whoosh' });
  parts.pipLook(p, tNew + 0.6, 0.13, 0.03);

  const icon = b.icon;
  for (const f of every(1)) {
    const t = sec(f);
    const s = Math.max(0.001, kit.backOut((t - tOwn) / 0.45));
    const pulse = 1 + 0.12 * Math.sin((t - tOwn) * 5) * span(t, tOwn + 0.5, tOwn + 1.0);
    key(icon, 'scale', f, s * pulse);
  }
  cues.push({ t: tOwn, type: 'pop', pitch: 1.3 });
  cues.push({ t: tOwn + 0.15, type: 'rise', dur: 1.2, pitch: 0.8, gain: 0.7 });

  parts.pipEyes(p, tOwn + 0.15, 1.35, 1.35, 0.15);        // Pip sees its own face
  parts.pipLook(p, tOwn + 0.15, 0.15, 0.06, 0.15);
  for (const f of every(1, fr(tOwn), fr(tOwn + 0.8))) {
    const t = sec(f);
    const lit = 1 + 0.9 * Math.sin(Math.PI * span(t, tOwn + 0.1, tOwn + 0.7, (v) => v));
    key(p.bulbGlow, 'scale', f, [lit, lit, 1]);
  }
  key(p.mouth, 'scale', fr(tOwn + 0.1), [1, 1, 1]);
  key(p.mouth, 'scale', fr(tOwn + 0.3), [0.6, 0.6, 1]);

  // ------------------------------------------------------------ camera
  const path = (t) => {
    const all = kit.smooth(t / end);
    const push = span(t, tOwn, end + 0.5);
    const x = -0.25 + 0.4 * all + mix(0, -0.5, push);
    const y = 0.05 * all;
    const z = kit.H0 - 0.8 * all - 3.2 * push;
    return [x, y, z];
  };

  kit.camera(path, 1.0);
  return cues;
}
