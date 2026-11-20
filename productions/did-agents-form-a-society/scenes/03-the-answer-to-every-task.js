/* Scene 03: The answer to every task.

The agents stand around their board, Pip among them. Crosses pop over the ones
that are stuck. Then the stuck ones link up, sparks run to the board, and the
board fills. Over the board, a shared thought shows how a secret word is made:
a file and a tool give a word. Words pop up over agent after agent. Close on
Pip: a secret word appears in its hands, and it looks down at it.
*/
'use strict';

function build(T) {
  const { fr, sec, key } = kit;
  parts.begin();

  const PLACE = [-5.0, -3.6];
  const HELD = [PLACE[0], PLACE[1] - 0.62];
  const RECIPE = [0, 6.1];
  const WIDE = [0, 0, 34];

  const cues = [];
  const end = sec(kit.frames());
  const tStuck = T.at(0, 0.12);
  const tCheat = T.at(0, 0.7);
  const tHours = T.start(1);
  const tMade = T.at(1, 0.16);
  const tAny = T.at(1, 0.5);
  const tPip = T.start(2);
  const tHold = T.start(3);

  kit.backdrop(4);
  kit.motes(20, 9);
  const st = parts.stage();
  const { board, crowd, places } = parts.gathering(st, { keep: [PLACE] });
  crowd.forEach((made, i) => parts.bob(made.root, 0, end, i * 0.9, 0.04));
  const posted = [...parts.post(board, 20, 28, tCheat + 0.6, tAny)];
  posted.forEach((t, k) => cues.push({ t, type: 'tick', pitch: 0.9 + 0.05 * (k % 6), gain: 0.4 }));

  const pip = parts.agent('pip', st.cast, PLACE, 0.8);
  parts.mood(pip, 0, 'worried', 0);

  // ------------------------------------------------------------ stuck, and working together
  const stuck = crowd.map((made, i) => [made, i]).filter(([, i]) => i % 3 === 0);
  const over = (at) => [at[0], at[1] + 0.98];
  [[{ at: PLACE }, -1], ...stuck].forEach(([made, i], k) => {
    const mark = parts.cross(`stuck${k}`, st.front, i < 0 ? [PLACE[0], PLACE[1] + 1.45] : over(made.at), i < 0 ? 0.7 : 0.55);
    const t = tStuck + 0.07 * k;
    kit.pop(mark, t, i < 0 ? 0.7 : 0.55, 0.3, tCheat + 0.03 * k, 0.2);
    if (k % 3 === 0) cues.push({ t, type: 'tick', pitch: 0.6, gain: 0.6 });
  });
  stuck.forEach(([made, i], k) => {
    let near = null;
    places.forEach((at, j) => {
      if (j === i || (j % 3 === 0 && j < i)) return;
      const far = Math.hypot(at[0] - made.at[0], at[1] - made.at[1]);
      if (near === null || far < near[1]) near = [at, far];
    });
    kit.grow(kit.branch(`link${k}`, st.props, made.at, near[0], kit.MIST, 0.08, 0.5), tCheat + 0.3 + 0.06 * k, 0.4, tPip - 0.4);
    if (k % 2) return;
    const idea = parts.spark(`idea${k}`, st.front, parts.body(made.which)[0], 0.6);
    const to = parts.edge(board.at, [board.w / 2, board.h / 2], made.at);
    for (let t = tCheat + 0.5 + 0.1 * k; t + 0.9 < tAny; t += 2.2) parts.send(idea, [made.at, to], t, t + 0.8, { spin: 3 });
  });
  cues.push({ t: tCheat + 0.3, type: 'swoosh', dur: 1.2, gain: 0.7 });
  kit.pipLook(pip, tCheat, 0.13, 0.04);
  parts.mood(pip, tCheat + 0.4, 'flat');

  // ------------------------------------------------------------ how the secret words are made
  const recipe = parts.thought('recipe', st.front, RECIPE, 6.6, 2.3, [-0.5, -1]);
  kit.pop(recipe.root, tMade - 0.3, 1.0, 0.45, tPip - 0.5);
  cues.push({ t: tMade - 0.3, type: 'pop', pitch: 0.8 });
  const pieces = [
    parts.sheet('recipe-file', recipe.root, [-2.35, 0], { scale: 1.2, seed: 4 }).root,
    parts.group('recipe-plus', recipe.root, [-1.45, 0]),
    parts.tool('recipe-tool', recipe.root, [-0.55, 0], 0, 1.5),
    parts.group('recipe-gives', recipe.root, [0.2, 0]),
    parts.word('recipe-word', recipe.root, [1.95, 0], 1.0).root,
  ];
  kit.branch('recipe-plus-a', pieces[1], [-0.22, 0], [0.22, 0], kit.PAPER, 0.1, 1.0);
  kit.branch('recipe-plus-b', pieces[1], [0, -0.22], [0, 0.22], kit.PAPER, 0.1, 1.0);
  kit.branch('recipe-gives-a', pieces[3], [0, 0], [0.62, 0], kit.PAPER, 0.1, 1.0);
  kit.shape('recipe-gives-b', [[0.55, 0.22], [0.9, 0], [0.55, -0.22]], kit.material(kit.PAPER), pieces[3]);
  [1.2, 1.0, 1.5, 1.0, 1.0].forEach((s, k) => {
    kit.pop(pieces[k], tMade + 0.35 * k, s, 0.3);
    cues.push({ t: tMade + 0.35 * k, type: k === 4 ? 'chime' : 'tick', pitch: 1.0 + 0.1 * k, gain: k === 4 ? 0.5 : 1.0 });
  });
  parts.mood(pip, tMade + 1.4, 'wide', 0.15);
  kit.pipLook(pip, tMade, 0.12, 0.12);

  // ------------------------------------------------------------ a word for every agent, and one for Pip
  crowd.forEach((made, i) => {
    if (i % 3 === 2) return;
    const own = parts.word(`word${i}`, st.front, over(made.at), 0.42);
    const t = tAny + 0.05 * i;
    kit.pop(own.root, t, 0.42, 0.3);
    if (i % 5 === 0) cues.push({ t, type: 'blip', pitch: 1.0 + 0.04 * (i % 8), gain: 0.4 });
  });
  const held = parts.word('held', st.front, HELD, 0.8);
  kit.pop(held.root, tPip + 0.5, 0.8, 0.45);
  cues.push({ t: tPip + 0.5, type: 'pop', pitch: 1.2 });
  cues.push({ t: tPip + 0.6, type: 'chime', gain: 0.6 });
  kit.pipLook(pip, tPip + 0.5, 0.0, -0.09);
  parts.mood(pip, tPip + 0.7, 'glad');
  parts.mood(pip, tHold, 'happy');
  parts.pulse(held.root, tHold + 0.2, 0.8, 1.15, 0.6);
  for (const f of kit.every(2, fr(tHold), fr(end))) key(held.glow, 'scale', f, 1 + 0.12 * Math.sin(sec(f) * 3));
  parts.live(pip, 7);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [PLACE[0] + 1.6, PLACE[1] + 1.2, 20]], [tStuck + 1.6, WIDE], [tHours, WIDE], [tMade + 1.0, [0, 3.4, 21]], [tAny - 0.2, [0, 3.4, 20.6]],
    [tAny + 1.5, WIDE], [tPip - 0.3, WIDE], [tPip + 1.1, [PLACE[0] + 0.3, PLACE[1] + 0.2, 10.5]], [end, [PLACE[0] + 0.2, PLACE[1] + 0.1, 9.3]],
  ]), 1.0);
  return cues;
}
