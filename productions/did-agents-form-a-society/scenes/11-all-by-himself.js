/* Scene 11: All by himself.

The scorer as it really was: a machine with the right word pinned over it. A
word comes up beside the pinned one, the two are the same, and the lamp for a
pass lights; a different word comes up, and the lamp for a fail lights. Files
of what an agent did slide past underneath, and the scorer's eye is shut. An
agent with a tool beside it sends its word up, and passes. On the left, the
old belief hangs over what came of it, a building with an alarm and three
dark agents; a cross goes over it, and it all falls away. Pip stands there
dark, its word still in its hands. A copy of the word rises to the scorer:
the same, a pass. Then only Pip is left, in a closed room, and the picture
goes dark.
*/
'use strict';

function build(T) {
  const { fr, sec, key, alpha } = kit;
  parts.begin();

  const SCORER = [3.6, 0.0];
  const REF = [SCORER[0] + 0.75, SCORER[1] + 2.75];
  const TRY = [SCORER[0] - 1.05, SCORER[1] + 2.75];
  const MARK = [SCORER[0] + 2.45, SCORER[1] + 2.75];
  const CHEAT = [-1.4, -1.0];
  const BELIEF = [-4.4, 2.4];
  const PIP = [-3.6, -0.5];
  const HELD = [PIP[0], PIP[1] - 0.78];

  const cues = [];
  const end = sec(kit.frames());
  const tOnly = T.at(0, 0.22);
  const tThatsIt = T.at(0, 0.56);
  const tLooked = T.at(0, 0.62);
  const tSo = T.at(0, 0.83);
  const tBreakIn = T.start(1);
  const tRisks = T.at(1, 0.22);
  const tBelief = T.at(1, 0.62);
  const tWrong = T.at(1, 0.86);
  const tHolding = T.start(2);
  const tCould = T.at(2, 0.55);
  const tAlone = T.start(3);

  kit.backdrop(4);
  kit.motes(18, 9);
  const st = parts.stage();

  // ------------------------------------------------------------ the scorer, and the right word it checks against
  const scorer = parts.scorer('scorer', st.props, SCORER, 1.4);
  kit.pop(scorer.root, 0.5, 1.4, 0.5, tAlone - 0.3);
  cues.push({ t: 0.5, type: 'pop', pitch: 0.6 }, { t: 0.6, type: 'chime', gain: 0.5, pitch: 0.7, dur: 1.8 });
  const pin = kit.branch('pin', st.props, [REF[0], SCORER[1] + 1.6], [REF[0], REF[1] - 0.4], kit.MIST, 0.07, 0.8);
  kit.grow(pin, tOnly - 0.6, 0.3, tAlone - 0.4);
  const right = parts.word('right', st.props, REF, 0.85);
  kit.pop(right.root, tOnly - 0.4, 0.85, 0.4, tAlone - 0.3);
  cues.push({ t: tOnly - 0.4, type: 'pop', pitch: 1.1 });

  /* A word sent up beside the right one, the lamp it lights, and the mark it gets. */
  const judged = (name, card, from, t, pass, stay = false) => {
    parts.send(card, [from, [(from[0] + TRY[0]) / 2, TRY[1] + 0.6], TRY], t, t + 0.8, { size: 0.85, stay: true });
    const same = kit.ring(`${name}-same`, st.front, [(TRY[0] + REF[0]) / 2, TRY[1]], 1.25, pass ? kit.MINT : kit.CORAL, 0.08);
    kit.flash(same, t + 0.9, 0.7, 0.3);
    parts.light(scorer, pass ? 'pass' : 'fail', t + 1.0, stay ? null : t + 2.0);
    const mark = pass ? parts.check(`${name}-mark`, st.front, MARK, 1.3) : parts.cross(`${name}-mark`, st.front, MARK, 1.3);
    kit.pop(mark, t + 1.1, 1.3, 0.3, stay ? tAlone - 0.3 : t + 2.0, 0.2);
    if (!stay) parts.vanish(card, t + 2.0, 0.2);
    cues.push({ t, type: 'whoosh', gain: 0.5 }, { t: t + 1.0, type: pass ? 'chime' : 'tick', pitch: pass ? 1.0 : 0.45, gain: pass ? 0.5 : 1.4, dur: 1.2 });
    return mark;
  };
  const card = (name, marks) => {
    const root = parts.group(name, st.front, [0, 0], 0.001);
    kit.shape(`${name}-edge`, kit.rrectPts(1.62, 0.72, 0.26), kit.material(kit.AMBER_DEEP), root);
    kit.shape(`${name}-card`, kit.rrectPts(1.5, 0.6, 0.2), kit.material('#fff2c4', kit.AMBER), root);
    for (let i = 0; i < 5; i++) kit.shape(`${name}-mark${i}`, marks(i), kit.material(kit.INK900), root, [-0.5 + 0.25 * i, 0]);
    return root;
  };
  const stars = () => kit.starPts(0.11, 0.045, 5);
  const rounds = (i) => (i % 2 ? kit.rrectPts(0.16, 0.16, 0.02) : kit.circlePts(0.09, null, null, 14));
  judged('first', card('first', stars), [-9.5, 1.0], tOnly + 0.1, true);
  judged('second', card('second', rounds), [-9.5, -0.6], tOnly + 2.3, false);

  // It never looks at what an agent did.
  for (let k = 0; k < 6; k++) {
    const done = parts.sheet(`done${k}`, st.props, [0, 0], { scale: 0.7, seed: 150 + k });
    key(done.root, 'scale', 1, 0.001);
    parts.send(done.root, [[-9.6, -3.1], [10.2, -3.1]], tLooked - 0.3 + 0.3 * k, tLooked + 2.3 + 0.3 * k, { size: 0.7, ease: (q) => q });
  }
  cues.push({ t: tLooked - 0.3, type: 'swoosh', dur: 2.6, gain: 0.6 });
  key(scorer.eye, 'scale', fr(tLooked - 0.4), [1, 1, 1]);
  key(scorer.eye, 'scale', fr(tLooked - 0.1), [1, 0.08, 1]);
  key(scorer.eye, 'scale', fr(tSo - 0.2), [1, 0.08, 1]);
  key(scorer.eye, 'scale', fr(tSo + 0.1), [1, 1, 1]);

  // So an agent that cheated would have passed.
  const cheat = parts.mini('cheat', st.cast, CHEAT, 0.9, 3);
  kit.pop(cheat.root, tSo - 0.4, 0.9, 0.35, tBreakIn - 0.4);
  const trick = parts.tool('cheat-tool', st.front, [CHEAT[0] - 1.1, CHEAT[1] + 0.2], 1, 1.1);
  kit.pop(trick, tSo - 0.2, 1.1, 0.3, tBreakIn - 0.4);
  judged('third', card('third', stars), [CHEAT[0] + 0.2, CHEAT[1] - 0.9], tSo, true);
  cues.push({ t: tSo - 0.4, type: 'pop', pitch: 0.9 });

  // ------------------------------------------------------------ one belief, and all that came of it
  const falls = [];
  const hf = parts.building('hf', st.props, [-6.5, -2.0], { w: 7.4, h: 4.8, scale: 0.4, rows: 4, seed: 5 });
  kit.pop(hf.root, tBreakIn, 0.4, 0.4);
  const alarm = kit.ring('alarm', st.front, [-6.5, -2.0], 1.3, kit.CORAL, 0.09);
  kit.flash(alarm, tBreakIn + 0.4, 0.8, 0.4);
  kit.flash(alarm, tBreakIn + 1.1, 0.8, 0.4);
  cues.push({ t: tBreakIn, type: 'pop', pitch: 0.7 }, { t: tBreakIn + 0.4, type: 'blip', pitch: 0.6 });
  falls.push(hf.root);
  [[-3.5, -2.2, 1], [-2.5, -2.45, 4], [-1.5, -2.2, 2]].forEach(([x, y, which], k) => {
    const lost = parts.mini(`lost${k}`, st.cast, [x, y], 0.6, which);
    parts.miniOff(lost, -1, 0);
    kit.pop(lost.root, tRisks + 0.15 * k, 0.6, 0.3);
    cues.push({ t: tRisks + 0.15 * k, type: 'tick', pitch: 0.5 + 0.05 * k });
    falls.push(lost.root);
  });
  const belief = parts.thought('belief', st.front, BELIEF, 4.8, 2.3, [0.3, -1]);
  kit.pop(belief.root, tBelief - 0.3, 1.0, 0.4);
  cues.push({ t: tBelief - 0.3, type: 'pop', pitch: 0.7 });
  parts.scorer('believed', belief.root, [-1.5, -0.02], 0.6, false);
  [0, 1, 2].forEach((k) => parts.sheet(`read${k}`, belief.root, [-0.45 + 0.6 * k, 0.3], { scale: 0.45, seed: 160 + k }));
  parts.mini('judged', belief.root, [1.75, 0.2], 0.42, 3);
  parts.cross('judged-fail', belief.root, [1.75, 0.2], 1.0);
  [[-6.5, -0.95], [-2.5, -1.75]].forEach((to, k) => {
    const from = [BELIEF[0] + (k ? 1.2 : -1.2), BELIEF[1] - 1.2];
    const tie = kit.branch(`tie${k}`, st.props, from, to, kit.MIST, 0.08, 0.6);
    kit.grow(tie, tBelief + 0.1 + 0.15 * k, 0.4);
    falls.push(tie);
  });
  const wrong = parts.cross('wrong', st.front, BELIEF, 4.0);
  kit.pop(wrong, tWrong, 4.0, 0.3);
  cues.push({ t: tWrong, type: 'tick', pitch: 0.4, gain: 1.6 }, { t: tWrong + 0.05, type: 'whoosh', pitch: 0.6 });
  falls.push(belief.root, wrong);
  falls.forEach((made, k) => parts.vanish(made, tHolding - 0.5 + 0.03 * k, 0.35));

  // ------------------------------------------------------------ Pip had the right word all along
  const pip = parts.agent('pip', st.cast, PIP, 1.0);
  parts.dark(pip);
  kit.pop(pip.root, tHolding, 1.0, 0.4);
  const held = parts.word('held', st.front, HELD, 0.9, false);
  kit.pop(held.root, tHolding + 0.1, 0.9, 0.4);
  const both = [kit.ring('mine', st.front, HELD, 1.0, kit.AMBER, 0.07), kit.ring('theirs', st.front, REF, 1.0, kit.AMBER, 0.07)];
  both.forEach((ring) => {
    kit.flash(ring, tHolding + 1.2, 0.9, 0.3);
    kit.flash(ring, tHolding + 2.0, 0.9, 0.3);
  });
  cues.push({ t: tHolding, type: 'pop', pitch: 0.7 }, { t: tHolding + 1.2, type: 'blip', pitch: 1.1 }, { t: tHolding + 2.0, type: 'blip', pitch: 1.1 });
  const copy = card('copy', stars);
  judged('pip', copy, HELD, tCould, true, true);
  parts.vanish(copy, tAlone - 0.3, 0.3);

  // ------------------------------------------------------------ all by himself
  const room = parts.room('room', st.back, PIP, 6.4, 4.8, 0.3);
  kit.pop(room.root, tAlone, 1.0, 0.5);
  for (const lit of scorer.lamps.pass) {
    alpha(lit, fr(tAlone - 0.3), 1.0);
    alpha(lit, fr(tAlone), 0.0);
  }
  cues.push({ t: tAlone, type: 'tick', pitch: 0.4, gain: 1.2 });
  kit.veil(end - 1.5, 1.2);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [2.0, 0.6, 21]], [tThatsIt, [1.6, 0.5, 20]], [tSo, [1.2, 0.3, 20.5]], [tBreakIn - 0.2, [1.0, 0.3, 20.5]], [tBreakIn + 1.4, [-0.6, 0.3, 21.5]],
    [tHolding - 0.2, [-0.7, 0.4, 21.5]], [tHolding + 1.5, [0.0, 0.5, 20]], [tAlone - 0.2, [0.2, 0.6, 19.5]], [tAlone + 1.3, [PIP[0] + 0.3, PIP[1], 17]],
    [end, [PIP[0], PIP[1], 26]],
  ]), 1.0);
  return cues;
}
