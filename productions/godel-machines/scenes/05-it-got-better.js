/* Scene 05: It got better.

The first program stands over a board of a hundred problems, and twenty of
them light up. A trail of eighty steps climbs to its best descendant, which
stands over its own board, where fifty light up.
*/
'use strict';

function build(T) {
  const { fr, sec, mix, alpha } = kit;

  const FIRST_AT = [-4.6, 1.3];
  const BEST_AT = [4.6, 1.6];
  const [CELL, GAP] = [0.24, 0.06];

  /* A ten-by-ten board of problems; the first `solved` cells light up one by one from t0. */
  const board = (name, stage, centre, solved, t0, dur, colour) => {
    const pitch = CELL + GAP;
    for (let i = 0; i < 100; i++) {
      const [r, c] = [Math.floor(i / 10), i % 10];
      const at = [centre[0] + (c - 4.5) * pitch, centre[1] + (4.5 - r) * pitch];
      kit.shape(`${name}-cell${i}`, kit.rrectPts(CELL, CELL, 0.05), kit.material(kit.INK600), stage, at);
      if (i < solved) {
        const on = kit.shape(`${name}-on${i}`, kit.rrectPts(CELL, CELL, 0.05), kit.material(colour[0], colour[1]), stage, at);
        const t = t0 + dur * i / Math.max(1, solved - 1);
        alpha(on, 1, 0.0);
        alpha(on, fr(t), 0.0);
        alpha(on, fr(t) + 2, 1.0);
      }
    }
  };

  kit.state.zstep = 0.0005;
  const cues = [];
  const end = sec(kit.frames());
  const tFirst = T.start(0);
  const tSolve = T.at(0, 0.55);
  const [tRounds0, tRounds1] = [T.start(1), T.at(1, 0.45)];
  const tBest = T.at(1, 0.5);
  const tFifty = T.at(1, 0.68);

  kit.backdrop(51, kit.MINT_DEEP);
  kit.motes(undefined, 52, kit.AMBER);
  const stage = kit.layer('stage', 1.0);

  const first = kit.pip('first', stage, FIRST_AT, 1.0, ...parts.scoreColour(20));
  kit.pop(first.root, tFirst - 0.4, 1.0);
  kit.pipIdle(first);
  kit.pipBlink(first, [2.0, 5.5, 8.0]);
  kit.pipLook(first, tSolve - 0.3, 0.0, -0.1);
  kit.pipLook(first, tBest + 0.2, 0.13, 0.05);
  cues.push({ t: Math.max(0.05, tFirst - 0.4), type: 'pop' });

  board('first', stage, [FIRST_AT[0], -2.0], 20, tSolve, 0.9, [kit.MINT, kit.MINT_DEEP]);
  for (let k = 0; k < 5; k++) cues.push({ t: tSolve + 0.2 * k, type: 'tick', pitch: 1.0 + 0.05 * k, gain: 0.4 });
  const n20 = kit.text('first-count', '20', 0.5, kit.material(kit.MINT), stage, [FIRST_AT[0] - 2.3, -2.0], { face: 'JetBrainsMono' });
  kit.appear(n20, tSolve + 0.9, null, 0.3);

  // eighty rounds: a trail of steps climbing from the first program to the best one
  for (let k = 0; k < 80; k++) {
    const q = k / 79;
    const x = mix(FIRST_AT[0] + 1.3, BEST_AT[0] - 1.5, q);
    const y = mix(FIRST_AT[1] + 0.6, BEST_AT[1] + 0.4, q) + 1.6 * Math.sin(Math.PI * q);
    const dot = kit.shape(`step${k}`, kit.circlePts(0.05 + 0.03 * q, null, null, 12), kit.material(k % 10 === 9 ? kit.AMBER : kit.MIST), stage, [x, y]);
    const t = mix(tRounds0, tRounds1, q ** 0.8);
    alpha(dot, 1, 0.0);
    alpha(dot, fr(t), 0.0);
    alpha(dot, fr(t) + 2, 1.0);
  }
  cues.push({ t: tRounds0, type: 'rise', dur: tRounds1 - tRounds0, pitch: 1.0, gain: 0.5 });

  const best = kit.pip('best', stage, BEST_AT, 1.25, ...parts.scoreColour(50));
  kit.pop(best.root, tBest, 1.25);
  kit.pipIdle(best, undefined, undefined, 1.1, 2);
  kit.pipBlink(best, [tBest + 1.2]);
  alpha(best.halo, 1, 1.0);
  cues.push({ t: tBest, type: 'pop', pitch: 1.3 });
  kit.pipLook(best, tFifty - 0.3, 0.0, -0.1);
  kit.pipArm(best, 'right', tFifty + 1.0, 140, 0.3);
  kit.pipArm(best, 'left', tFifty + 1.0, 140, 0.3);

  board('best', stage, [BEST_AT[0], -2.0], 50, tFifty, 1.1, [kit.AMBER, kit.AMBER_DEEP]);
  for (let k = 0; k < 6; k++) cues.push({ t: tFifty + 0.2 * k, type: 'tick', pitch: 1.2 + 0.05 * k, gain: 0.4 });
  const n50 = kit.text('best-count', '50', 0.5, kit.material(kit.AMBER), stage, [BEST_AT[0] + 2.3, -2.0], { face: 'JetBrainsMono' });
  kit.appear(n50, tFifty + 1.1, null, 0.3);
  cues.push({ t: tFifty + 1.1, type: 'chime', gain: 0.6 });

  const path = (t) => {
    const q = kit.smooth(t / end);
    return [mix(-1.2, 1.0, q), 0.1, kit.H0 + 0.6 - 0.8 * q];
  };

  kit.camera(path, 1.0);
  return cues;
}
