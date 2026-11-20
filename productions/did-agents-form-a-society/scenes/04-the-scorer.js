/* Scene 04: The scorer.

Pip holds its secret word, starts to hand it up, and takes it back. Around the
board, no agent moves. Over the board a shared thought opens, and in it stands
the scorer: a square machine with one eye. A description is pinned to the
board. In the thought, the scorer reads file after file of what an agent has
done, and then fails an agent that holds a word. A question mark hangs in the
thought, since no agent has seen any of it; small thoughts of the scorer pop
up over the whole crowd all the same. Close on Pip, with the word in its hands
and the scorer over its head.
*/
'use strict';

function build(T) {
  const { fr, sec, key } = kit;
  parts.begin();

  const PLACE = [-5.0, -3.6];
  const HELD = [PLACE[0], PLACE[1] - 0.62];
  const BELIEF = [0, 6.05];
  const FEAR = [PLACE[0] + 2.3, PLACE[1] + 2.3];
  const WIDE = [0, 0, 34];
  const CLOSE = [PLACE[0] + 0.3, PLACE[1] + 0.2, 10.0];
  const ABOVE = [0, 4.4, 16];

  const cues = [];
  const end = sec(kit.frames());
  const tNot = T.start(0);
  const tNone = T.at(0, 0.6);
  const tReason = T.start(1);
  const tScore = T.at(1, 0.12);
  const tRead = T.at(1, 0.26);
  const tBelief = T.at(1, 0.45);
  const tEvery = T.at(1, 0.56);
  const tFail = T.at(1, 0.8);
  const tNever = T.start(2);
  const tBoard = T.at(2, 0.5);
  const tSo = T.start(3);
  const tFool = T.at(3, 0.55);

  kit.backdrop(4);
  kit.motes(20, 9);
  const st = parts.stage();
  const { crowd } = parts.gathering(st, { keep: [PLACE] });
  const over = (at) => [at[0], at[1] + 0.98];
  crowd.forEach((made, i) => {
    parts.bob(made.root, 0, end, i * 0.9, 0.04);
    if (i % 3 === 2) return;
    parts.vanish(parts.word(`word${i}`, st.front, over(made.at), 0.42, false).root, tReason - 0.4 + 0.01 * i, 0.3);
  });

  // ------------------------------------------------------------ Pip does not hand the word in
  const pip = parts.agent('pip', st.cast, PLACE, 0.8);
  const held = parts.word('held', st.front, HELD, 0.8, false);
  kit.pipLook(pip, 0.1, 0.0, -0.08);
  kit.pipArm(pip, 'right', tNot + 0.1, 105, 0.4);
  parts.move(held.root, tNot + 0.1, [PLACE[0] + 1.25, PLACE[1] + 0.35], 0.5);
  kit.pipLook(pip, tNot + 0.2, 0.12, 0.08);
  cues.push({ t: tNot + 0.1, type: 'rise', dur: 0.5, pitch: 1.1, gain: 0.5 });
  kit.pipArm(pip, 'right', tNot + 1.2, 18, 0.4);
  parts.move(held.root, tNot + 1.2, HELD, 0.5);
  parts.mood(pip, tNot + 1.1, 'worried');
  cues.push({ t: tNot + 1.2, type: 'tick', pitch: 0.6 });

  // ------------------------------------------------------------ the belief: a scorer that reads everything
  const belief = parts.thought('belief', st.front, BELIEF, 7.8, 3.0, [-0.5, -1]);
  kit.pop(belief.root, tReason, 1.0, 0.5);
  cues.push({ t: tReason, type: 'pop', pitch: 0.7 });
  const scorer = parts.scorer('scorer', belief.root, [-2.75, -0.02], 0.85, false);
  kit.pop(scorer.root, tReason + 0.5, 0.85, 0.45);
  cues.push({ t: tReason + 0.5, type: 'chime', gain: 0.5, pitch: 0.7, dur: 1.6 });
  for (let k = 0; k < 4; k++) parts.light(scorer, k % 2 ? 'fail' : 'pass', tScore + 0.4 * k, tScore + 0.4 * k + 0.25);
  cues.push({ t: tScore, type: 'tick' }, { t: tScore + 0.4, type: 'tick', pitch: 0.7 }, { t: tScore + 0.8, type: 'tick' }, { t: tScore + 1.2, type: 'tick', pitch: 0.7 });

  const page = parts.sheet('description', st.front, [-1.9, 2.35], { scale: 1.5, seed: 9 });
  kit.pop(page.root, tRead, 1.5, 0.4, tNever + 2.4);
  cues.push({ t: tRead, type: 'whoosh', gain: 0.6 });
  const noted = kit.ring('noted', st.front, [-1.9, 2.35], 1.05, kit.PAPER, 0.06);
  kit.flash(noted, tRead + 0.6, 0.9, 0.3);
  parts.pulse(belief.root, tBelief, 1.0, 1.05, 0.5);

  // The scorer reads what an agent has done, file after file, and fails an agent that holds a word.
  const eye = [-2.75, -0.02 + 0.5 * 0.85];
  const eyeZ = scorer.eye.z;
  key(scorer.eye, 'loc', fr(tEvery - 0.3), [0.0, 0.5, eyeZ]);
  [0, 1, 2, 3].forEach((k) => {
    const at = [-0.95 + 0.72 * k, 0.4];
    const done = parts.sheet(`done${k}`, belief.root, at, { scale: 0.5, seed: 20 + k });
    kit.pop(done.root, tEvery - 0.5 + 0.1 * k, 0.5, 0.3);
    const t = tEvery + 0.3 + 0.62 * k;
    key(scorer.eye, 'loc', fr(t - 0.15), [0.22, 0.52, eyeZ]);
    parts.send(done.root, [at, eye], t, t + 0.45, { shown: true, size: 0.5, to: 0.12 });
    key(scorer.eye, 'loc', fr(t + 0.45), [0.0, 0.5, eyeZ]);
    cues.push({ t: t + 0.4, type: 'tick', pitch: 1.2 + 0.1 * k });
  });
  const tried = parts.mini('tried', belief.root, [2.7, 0.3], 0.62, 3);
  const theirs = parts.word('tried-word', belief.root, [2.7, -0.72], 0.5, false);
  kit.pop(tried.root, tFail - 0.7, 0.62, 0.35);
  kit.pop(theirs.root, tFail - 0.5, 0.5, 0.35);
  key(scorer.eye, 'loc', fr(tFail - 0.2), [0.0, 0.5, eyeZ]);
  key(scorer.eye, 'loc', fr(tFail + 0.2), [0.24, 0.47, eyeZ]);
  parts.light(scorer, 'fail', tFail + 0.4);
  const failed = parts.cross('failed', belief.root, [2.7, 0.25], 1.5);
  kit.pop(failed, tFail + 0.6, 1.5, 0.3);
  cues.push({ t: tFail + 0.4, type: 'tick', pitch: 0.5, gain: 1.3 });
  cues.push({ t: tFail + 0.6, type: 'pop', pitch: 0.5 });

  // ------------------------------------------------------------ nobody has seen it, and all of them believe it
  const doubt = kit.text('doubt', '?', 1.7, kit.material(kit.PAPER), belief.root, [0.15, -0.1]);
  kit.appear(doubt, tNever + 0.2, null, 0.3);
  cues.push({ t: tNever + 0.2, type: 'blip', pitch: 0.8 });
  crowd.forEach((made, i) => {
    if (i % 3 === 0) return;
    const small = parts.notion(`notion${i}`, st.front, [made.at[0] + 0.3, made.at[1] + 1.05], 0.9);
    const t = tBoard + 0.2 + 0.03 * i;
    kit.pop(small, t, 0.9, 0.3);
    if (i % 5 === 1) cues.push({ t, type: 'blip', pitch: 0.7 + 0.04 * (i % 7), gain: 0.4 });
  });

  // ------------------------------------------------------------ an answer that cannot be used
  const fear = parts.thought('fear', st.front, FEAR, 2.0, 2.0, [-1, -1]);
  kit.pop(fear.root, tSo + 0.3, 1.0, 0.4);
  cues.push({ t: tSo + 0.3, type: 'pop', pitch: 0.7 });
  const watcher = parts.scorer('watcher', fear.root, [0, 0.02], 0.6, false);
  key(watcher.eye, 'loc', fr(tSo + 1.0), [0, 0.5, watcher.eye.z]);
  key(watcher.eye, 'loc', fr(tSo + 1.4), [-0.2, 0.42, watcher.eye.z]);
  kit.pipLook(pip, tSo, 0.0, -0.08);
  kit.pipLook(pip, tSo + 0.9, 0.12, 0.11);
  parts.mood(pip, tSo + 1.0, 'sad');
  parts.mood(pip, tFool, 'flat');
  kit.pipLook(pip, tFool + 0.2, 0.13, 0.1);
  parts.pulse(held.root, tFool + 0.3, 0.8, 1.12, 0.5);
  parts.live(pip, 8);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, CLOSE], [tNone - 0.1, [CLOSE[0], CLOSE[1], 10.4]], [tNone + 1.2, WIDE], [tReason, WIDE], [tReason + 1.5, ABOVE],
    [tBoard - 0.5, [0, 4.4, 15.6]], [tBoard + 1.0, WIDE], [tSo - 0.2, WIDE], [tSo + 1.3, [PLACE[0] + 0.9, PLACE[1] + 0.9, 12.5]],
    [end, [PLACE[0] + 0.9, PLACE[1] + 0.9, 11.4]],
  ]), 1.0);
  return cues;
}
