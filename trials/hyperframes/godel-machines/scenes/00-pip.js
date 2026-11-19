/* Scene 00: A program that fixes programs.

Pip pops in and waves. A program with a red mistake slides in; Pip spots the
mistake and fixes it. Other programs like Pip appear all around, then go. A
new program drops in, and its title bar shows Pip's own face.

It is productions/godel-machines/scenes/00-pip.py, line for line, written for
the trial's kit. The sound effect cues are left out: the trial compares pictures.
*/
'use strict';

function build(T) {
  const { Track, backOut, easeOut, fr, mix, sec, smooth, span, within } = kit;

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

  p.root.move.loc = (t) => {
    let [x, y] = HOME;
    for (const [t0, dest] of [[tJob, WORK], [tMadeUp + 0.1, HOME], [tNew, WORK]]) {
      const q = span(t, t0, t0 + 0.8);
      x = mix(x, dest[0], q);
      y = mix(y, dest[1], q);
    }
    x -= 0.25 * span(t, tOwn, tOwn + 0.25, easeOut) * (1 - 0.6 * span(t, tOwn + 0.4, tOwn + 1.2));
    return [x, y];
  };
  p.root.move.scale = (t) => PIP_SCALE * Math.max(0.001, backOut((t - tHello) / 0.5));
  parts.pipIdle(p);

  parts.pipWave(p, tHello + 0.7, tHello + 2.6);
  parts.pipBlink(p, [3.6, tJob + 1.3, tMadeUp + 1.6, tReal + 2.0, tNew + 1.1]);

  // ------------------------------------------------------------ a program with a mistake
  const a = parts.program('job', stage, [14, CARD[1]], { rows: 7, seed: 4, mistake: 3 });
  a.root.move.loc = (t) => {
    let x = mix(14.0, CARD[0], span(t, tJob, tJob + 0.9, easeOut));
    x = mix(x, 15.0, span(t, tMadeUp, tMadeUp + 0.8, (q) => q * q));
    return [x, CARD[1]];
  };

  parts.pipLook(p, tJob + 0.5, 0.13, 0.0);
  for (const bar of a.bad.bars) {  // the mistake twitches until it is fixed
    bar.move.rot = (t) => {
      if (t > sec(fr(tFix))) return 0;
      const at = within(t, fr(tJob), fr(tFix));
      return 0.035 * Math.sin(at * 31) * (0.5 + 0.5 * Math.sin(at * 5.3));
    };
  }

  a.bad.ring.move.alpha = (t) => {
    if (t < sec(fr(tFind))) return 0;
    const at = within(t, fr(tFind), fr(tFix + 0.6));
    const on = span(at, tFind, tFind + 0.25) * (1 - span(at, tFix, tFix + 0.5));
    return on * (0.75 + 0.25 * Math.sin((at - tFind) * 9));
  };

  // Pip reaches out, a spark flies to the mistake, and the red bars turn mint.
  parts.pipArm(p, 'right', tFix - 0.55, 82, 0.25);
  const hand = [WORK[0] + PIP_SCALE * 1.3, WORK[1] + PIP_SCALE * -0.27];
  const target = [CARD[0] + a.bad.x, CARD[1] + a.bad.y];
  const spark = kit.shape('spark', kit.starPts(0.32, 0.08), kit.material('#eafff9'), stage, [0, 0], { lift: 0.3 });
  const sparkGlow = kit.shape('spark-glow', kit.circlePts(0.9), kit.glowMaterial(kit.MINT, 0.8), stage, [0, 0], { lift: 0.29 });
  const tFly = tFix - 0.3;
  const flight = (t) => {
    const q = span(t, tFly, tFix, (v) => v);
    let x = mix(hand[0], target[0], q);
    let y = mix(hand[1], target[1], q) + 0.9 * Math.sin(Math.PI * q);
    const flying = tFly <= t && t <= tFix ? 1.0 : 0.0;
    const burst = span(t, tFix, tFix + 0.5, easeOut);
    const bursting = tFix < t && t <= tFix + 0.6 ? 1.0 : 0.0;
    if (bursting) [x, y] = target;
    return { x, y, s: 0.001 + flying * 0.6 + bursting * (0.6 + 1.6 * burst), a: flying + bursting * (1 - burst) };
  };
  spark.move.loc = (t) => [flight(t).x, flight(t).y];
  spark.move.scale = (t) => [flight(t).s, flight(t).s, 1];
  spark.move.rot = (t) => t * 4;
  spark.move.alpha = (t) => flight(t).a;
  sparkGlow.move.loc = spark.move.loc;
  sparkGlow.move.scale = (t) => [flight(t).s * 1.3, flight(t).s * 1.3, 1];
  sparkGlow.move.alpha = spark.move.alpha;
  for (const bar of a.bad.bars) bar.move.alpha = new Track(1.0).key(tFix, 1.0).key(tFix + 0.2, 0.0);
  for (const bar of a.good) bar.move.alpha = bar.shown.key(tFix, 0.0).key(tFix + 0.2, 1.0);

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
    const f0 = fr(tReal - 0.2);
    const f1 = fr(tCrowdOut + 0.8);
    bot.root.move.scale = (t) => {
      const at = within(t, f0, f1);
      const grow = backOut((at - tIn) / 0.45) * (1 - span(at, tCrowdOut + 0.04 * i, tCrowdOut + 0.04 * i + 0.35));
      return sc * Math.max(0.001, grow);
    };
    bot.root.move.loc = new Track([x, y]).key(tReal, [x, y]).key(tCrowdOut + 0.8, [x + 0.25 * (x > 0 ? 1 : -1), y + 0.15]);
    parts.pipIdle(bot, tReal - 0.2, tCrowdOut + 0.8, i * 0.7);
    parts.pipLook(bot, tIn + 0.5, x > 0 ? -0.06 : 0.06, y > 0 ? -0.03 : 0.03);
    if (i % 3 === 1) parts.pipWave(bot, tIn + 0.6, tIn + 1.8, 8 + i % 4);
  });
  parts.pipLook(p, tReal + 0.5, -0.12, 0.05);
  parts.pipLook(p, tReal + 1.6, 0.12, 0.05);
  parts.pipLook(p, tCrowdOut, 0.0, 0.0);

  // ------------------------------------------------------------ a new program: Pip's own code
  const b = parts.program('own', stage, [CARD[0], 10], { rows: 7, seed: 9, tabIcon: true });
  b.root.move.loc = (t) => [CARD[0], mix(10.0, CARD[1], span(t, tNew, tNew + 0.9, backOut))];
  parts.pipLook(p, tNew + 0.6, 0.13, 0.03);

  b.icon.move.scale = (t) => {
    const s = Math.max(0.001, backOut((t - tOwn) / 0.45));
    const pulse = 1 + 0.12 * Math.sin((t - tOwn) * 5) * span(t, tOwn + 0.5, tOwn + 1.0);
    return s * pulse;
  };

  parts.pipEyes(p, tOwn + 0.15, 1.35, 1.35, 0.15);        // Pip sees its own face
  parts.pipLook(p, tOwn + 0.15, 0.15, 0.06, 0.15);
  p.bulbGlow.move.scale = (t) => {
    const at = within(t, fr(tOwn), fr(tOwn + 0.8));
    const flash = 1 + 0.9 * Math.sin(Math.PI * span(at, tOwn + 0.1, tOwn + 0.7, (v) => v));
    return [flash, flash, 1];
  };
  p.mouth.move.scale = new Track([1, 1, 1]).key(tOwn + 0.1, [1, 1, 1]).key(tOwn + 0.3, [0.6, 0.6, 1]);

  // ------------------------------------------------------------ camera
  kit.camera((t) => {
    const all = smooth(t / end);
    const push = span(t, tOwn, end + 0.5);
    return [-0.25 + 0.4 * all + mix(0, -0.5, push), 0.05 * all, kit.H0 - 0.8 * all - 3.2 * push];
  }, 1.0);
}

if (typeof module !== 'undefined') module.exports = build;
