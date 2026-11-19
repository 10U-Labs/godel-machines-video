/* Scene 02: Better at getting better.

Pip and its own code sit at the two ends of a loop. An idea travels from Pip
into the code, and the better code comes back as a better Pip. Each lap runs
faster and lifts the meter under Pip by more than the last one.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, alpha, every } = kit;
  const radians = (deg) => deg * Math.PI / 180;

  const PIP_AT = [-4.4, 0.2];
  const CODE_AT = [4.4, 0.2];
  const R = 2.84;                       // radius of both arcs of the loop
  const TOP_C = [0.0, 0.16];            // centre of the upper arc (Pip to code)
  const BOT_C = [0.0, 0.24];            // centre of the lower arc (code back to Pip)
  const [A0, A1] = [156.3, 23.7];       // the upper arc runs from A0 down to A1 degrees
  const STEPS = 14;                     // bars in the meter

  /* Point on the loop: q from 0 to 0.5 crosses the top arc to the code, 0.5 to 1 comes back. */
  const onLoop = (q) => {
    if (q < 0.5) {
      const a = radians(mix(A0, A1, q / 0.5));
      return [TOP_C[0] + R * Math.cos(a), TOP_C[1] + R * Math.sin(a)];
    }
    const a = radians(mix(-A1, -A0, (q - 0.5) / 0.5));
    return [BOT_C[0] + R * Math.cos(a), BOT_C[1] + R * Math.sin(a)];
  };

  const arrowhead = (name, parent, tip, angle, mat) => {
    const pts = [[0.0, 0.0], [-0.42, 0.22], [-0.42, -0.22]];
    const [c, s] = [Math.cos(angle), Math.sin(angle)];
    return kit.shape(name, pts.map(([x, y]) => [x * c - y * s, x * s + y * c]), mat, parent, tip);
  };

  const cues = [];
  const end = sec(kit.frames());
  const tIdea = T.at(0, 0.2);
  const tWrite = T.at(0, 0.66);
  const tBack = T.start(1);
  const tOwn = T.at(1, 0.62);
  const tTitle = T.start(4) + 0.1;
  const tResult = T.at(4, 0.6);

  kit.backdrop(21);
  kit.motes(undefined, 22, kit.AMBER);
  const stage = kit.layer('stage', 1.0);

  // ------------------------------------------------------------ the loop
  const loopMat = kit.material(kit.MIST, null, 0.55);
  const top = kit.shape('arc-top', kit.arcPts(R, 0.09, A1 + 4, A0 - 4), loopMat, stage, TOP_C);
  const bot = kit.shape('arc-bottom', kit.arcPts(R, 0.09, -A0 + 4, -A1 - 4), loopMat, stage, BOT_C);
  // Both arcs run with falling angle, so each arrow points along angle - 90 degrees at the arc's end.
  const [aTop, aBot] = [radians(A1 + 4), radians(-A0 + 4)];
  const tipTop = [TOP_C[0] + R * Math.cos(aTop), TOP_C[1] + R * Math.sin(aTop)];
  const tipBot = [BOT_C[0] + R * Math.cos(aBot), BOT_C[1] + R * Math.sin(aBot)];
  const headTop = arrowhead('head-top', stage, tipTop, aTop - Math.PI / 2, loopMat);
  const headBot = arrowhead('head-bottom', stage, tipBot, aBot - Math.PI / 2, loopMat);
  const hot = kit.shape('arc-bottom-hot', kit.arcPts(R, 0.16, -A0 + 4, -A1 - 4), kit.material(kit.AMBER), stage, BOT_C);
  alpha(hot, 1, 0.0);
  for (const [ob, t0] of [[top, tWrite - 0.3], [headTop, tWrite - 0.3], [bot, tBack - 0.3], [headBot, tBack - 0.3]]) {
    kit.fade(ob, t0, null, 0.4);
  }
  for (const f of every(1, fr(tResult - 0.2), fr(tResult + 2.6))) {
    const t = sec(f);
    alpha(hot, f, span(t, tResult, tResult + 0.3) * (1 - span(t, tResult + 2.0, tResult + 2.5)) * (0.7 + 0.3 * Math.sin((t - tResult) * 8)));
  }

  // ------------------------------------------------------------ Pip and Pip's code
  const p = parts.pip('pip', stage, PIP_AT, 1.15);
  parts.pipIdle(p);
  parts.pipBlink(p, [2.6, 9.2, 14.2, 21.0, 24.5]);
  parts.pipLook(p, 0.3, 0.1, 0.03);
  const codeGlow = kit.shape('code-glow', kit.rrectPts(4.6, 5.2, 1.5), kit.glowMaterial(kit.AMBER, 0.7, 1.2), stage, CODE_AT);
  alpha(codeGlow, 1, 0.0);
  const code = parts.program('code', stage, CODE_AT, { rows: 6, w: 3.0, h: 3.6, seed: 14, tabIcon: true, scale: 0.85 });

  // ------------------------------------------------------------ the meter under Pip
  const lit = [];
  for (let i = 0; i < STEPS; i++) {
    const h = 0.18 + 0.075 * i;
    const x = PIP_AT[0] - 1.75 + i * 0.25;
    const pts = kit.rrectPts(0.17, h, 0.06).map(([px, py]) => [px, py + h / 2]);
    kit.shape(`step${i}`, pts, kit.material(kit.INK600), stage, [x, -2.75]);
    lit.push(kit.shape(`step${i}-on`, pts, kit.material(kit.AMBER, kit.AMBER_DEEP), stage, [x, -2.75]));
  }

  // ------------------------------------------------------------ the laps
  // Each lap: an idea goes from Pip to the code (first half) and comes back (second half).
  const laps = [[tWrite, tWrite + 0.9, tBack, tBack + 0.9]];      // the first lap is told slowly
  let at = T.start(2);
  for (const dur of [1.7, 1.3]) {
    laps.push([at, at + dur / 2, at + dur / 2, at + dur]);
    at += dur + 0.6;
  }
  at = Math.max(at, T.start(3));
  for (const dur of [1.0, 0.8, 0.65, 0.55]) {
    laps.push([at, at + dur / 2, at + dur / 2, at + dur]);
    at += dur + 0.12;
  }
  at = Math.max(at, T.start(4) + 0.4);
  while (at + 0.6 < end - 0.2) {
    laps.push([at, at + 0.3, at + 0.3, at + 0.6]);
    at += 0.75;
  }
  const gains = [1, 2, 3, 4, 3];                                         // bars each lap lights
  const level = [1];
  for (const g of gains) level.push(Math.min(STEPS, level[level.length - 1] + g));
  while (level.length < laps.length + 1) level.push(STEPS);

  /* Spark position and whether it shows, at time t. */
  const where = (t) => {
    for (const [a0, a1, b0, b1] of laps) {
      if (a0 <= t && t <= a1) return [onLoop(0.5 * (t - a0) / (a1 - a0)), 1.0];
      if (b0 <= t && t <= b1) return [onLoop(0.5 + 0.5 * (t - b0) / (b1 - b0)), 1.0];
      if (a1 < t && t < b0) return [onLoop(0.5), 0.0];
    }
    return [onLoop(0.0), 0.0];
  };

  const sparks = [];
  [[1.0, 0.0], [0.7, 0.045], [0.5, 0.09], [0.35, 0.135]].forEach(([size, lag], k) => {
    const sOb = kit.shape(`spark${k}`, kit.starPts(0.28 * size, 0.08 * size), kit.material('#fff3cf'), stage, [0, 0], { lift: 0.3 });
    const gOb = kit.shape(`spark${k}-glow`, kit.circlePts(0.8 * size), kit.glowMaterial(kit.AMBER, 0.8), stage, [0, 0], { lift: 0.29 });
    sparks.push([sOb, gOb, lag]);
  });
  for (const f of every(1)) {
    const t = sec(f);
    for (const [sOb, gOb, lag] of sparks) {
      let [[x, y], on] = where(t - lag);
      if (lag === 0 && tIdea <= t && t < tWrite) {          // the idea first appears over Pip's head
        const q = span(t, tIdea, tIdea + 0.35, kit.backOut);
        [x, y, on] = [PIP_AT[0] + 0.1, PIP_AT[1] + 2.0 + 0.08 * Math.sin(t * 4), q];
      }
      key(sOb, 'loc', f, [x, y, sOb.z]);
      key(gOb, 'loc', f, [x, y, gOb.z]);
      key(sOb, 'rot', f, t * 3);
      alpha(sOb, f, on);
      alpha(gOb, f, on);
    }
  }
  cues.push({ t: tIdea, type: 'pop', pitch: 1.4 });

  // arrivals: the code glows; returns: Pip pulses and the meter climbs
  const grown = [];
  laps.forEach(([, a1, , b1], k) => {
    for (const [f, a] of [[fr(a1) - 2, 0.0], [fr(a1), 0.9], [fr(a1 + 0.5), 0.0]]) alpha(codeGlow, f, a);
    cues.push({ t: a1, type: 'tick', pitch: 1.0 + 0.05 * Math.min(k, 8), gain: 0.7 });
    cues.push({ t: b1, type: 'blip', pitch: 0.9 + 0.08 * Math.min(k, 8), gain: 0.6 });
    const [before, after] = [level[k], level[k + 1]];
    for (let i = before; i < after; i++) {
      alpha(lit[i], fr(b1) - 1, 0.0);
      alpha(lit[i], fr(b1 + 0.05 * (i - before)) + 2, 1.0);
    }
    grown.push(b1);
  });
  for (let i = 0; i < STEPS; i++) {
    if (i < level[0]) alpha(lit[i], 1, 1.0);
    else if (!Object.keys(lit[i].keys).length) alpha(lit[i], 1, 0.0);
  }
  for (const f of every(1)) {
    const t = sec(f);
    const past = grown.filter((b) => b <= t);
    const pulse = past.reduce((sum, b) => sum + 0.12 * Math.exp(-(t - b) * 7), 0);
    key(p.root, 'scale', f, 1.15 * (1 + 0.03 * Math.min(past.length, 6)) * (1 + pulse));
  }
  cues.push({ t: laps[0][3], type: 'chime', gain: 0.8 });

  parts.pipLook(p, tWrite - 0.2, 0.13, 0.05);
  parts.pipLook(p, tBack + 0.3, 0.0, 0.0);
  parts.pipEyes(p, laps[0][3], 1.1, 0.6);                   // pleased
  parts.pipEyes(p, laps[0][3] + 1.0, 1.0, 1.0);
  parts.pipLook(p, tOwn - 0.2, 0.13, 0.03);
  const icon = code.icon;
  for (const f of every(1, fr(tOwn), fr(tOwn + 1.0))) {
    const q = span(sec(f), tOwn, tOwn + 1.0, (v) => v);
    const s = 1 + 0.5 * Math.sin(Math.PI * q);
    key(icon, 'scale', f, [s, s, 1]);
  }
  cues.push({ t: tOwn, type: 'pop', pitch: 1.2, gain: 0.6 });
  parts.pipLook(p, T.start(2), 0.06, 0.06);

  // ------------------------------------------------------------ the name
  const title = kit.text('title', 'recursive self-improvement', 0.62, kit.material(kit.PAPER), stage, [0, 3.75]);
  kit.fade(title, tTitle, null, 0.6);
  cues.push({ t: tTitle, type: 'swoosh', gain: 0.5 });

  // ------------------------------------------------------------ camera
  const path = (t) => {
    const q = kit.smooth(t / end);
    const push = span(t, T.start(3), T.start(4));
    return [0.0, 0.1 * q, kit.H0 - 0.6 * q - 1.0 * push + 1.0 * span(t, T.start(4), T.start(4) + 1.5)];
  };

  kit.camera(path, 1.0);
  return cues;
}
