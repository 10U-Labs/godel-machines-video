/* Scene 15: A possibility.

A bowl, a line of people, and a heart hang in a row, and each one drops away.
Then two circles of four: people on the left, agents on the right. Lines grow
between the people, and the same lines between the agents; sparks run along
both at the same moments.
*/
'use strict';

function build(T) {
  const { sec } = kit;
  parts.begin();

  const [PEOPLE, AGENTS] = [[-4.0, -0.6], [4.0, -0.6]];
  const RING = [[0, 1.75], [1.9, 0], [0, -1.75], [-1.9, 0]];
  const cues = [];
  const end = sec(kit.frames());
  const GONE = [T.at(0, 0.6), T.at(0, 0.76), T.at(0, 0.9)];
  const tAppear = T.start(1);
  const tTalk = T.at(1, 0.4);
  const tWhether = T.at(1, 0.68);

  kit.backdrop(5);
  kit.motes(20, 17);
  const st = parts.stage();

  // ------------------------------------------------------------ not from bodies, not from ancestors, not from feelings
  const hung = [parts.bowl('body', st.props, [-3.6, 1.2], 1.6), parts.group('line', st.props, [0, 0.6]), parts.heart('feeling', st.props, [3.6, 1.2], 1.5)];
  [0.4, 0.33, 0.27, 0.22].forEach((s, k) => parts.human(`line${k}`, hung[1], [0.9 - 0.62 * k, 0.26 * k], s, k, -1));
  hung.forEach((made, k) => {
    const s = made.sx;
    kit.pop(made, 0.4 + 0.25 * k, s, 0.4);
    kit.key(made, 'loc', kit.fr(GONE[k]), [made.x, made.y, made.z]);
    kit.key(made, 'loc', kit.fr(GONE[k] + 0.6), [made.x, made.y - 7.5, made.z]);
    kit.key(made, 'rot', kit.fr(GONE[k]), 0.0);
    kit.key(made, 'rot', kit.fr(GONE[k] + 0.6), k === 1 ? 0.2 : -0.5);
    cues.push({ t: 0.4 + 0.25 * k, type: 'pop', pitch: 0.8 + 0.1 * k }, { t: GONE[k], type: 'whoosh', pitch: 0.8, gain: 0.5 });
  });

  // ------------------------------------------------------------ beings that are intelligent, and can talk to each other
  RING.forEach(([x, y], k) => {
    const made = parts.human(`talker${k}`, st.cast, [PEOPLE[0] + x, PEOPLE[1] + y - 0.85], 0.34, k + 1, x > 0 || (x === 0 && k === 0) ? -1 : 1);
    kit.pop(made.root, tAppear - 0.4 + 0.1 * k, 0.34, 0.4);
  });
  RING.forEach(([x, y], k) => {
    const made = parts.agent(`program${k}`, st.cast, [AGENTS[0] + x, AGENTS[1] + y], 0.62, k ? k + 1 : 0);
    kit.pop(made.root, tAppear - 0.4 + 0.1 * k, 0.62, 0.4);
    kit.pipLook(made, tTalk, -0.1 * Math.sign(x), -0.07 * Math.sign(y));
    parts.live(made, 50 + k, tAppear - 0.4);
  });
  cues.push({ t: tAppear - 0.4, type: 'swoosh', dur: 0.9, gain: 0.6 });

  const PAIRS = [[0, 1], [1, 2], [2, 3], [3, 0], [0, 2], [1, 3]];
  [[PEOPLE, 0.72, 'p'], [AGENTS, 0.62, 'a']].forEach(([at, pull, name]) => {
    PAIRS.forEach(([i, j], k) => {
      const from = [at[0] + RING[i][0] * pull, at[1] + RING[i][1] * pull];
      const to = [at[0] + RING[j][0] * pull, at[1] + RING[j][1] * pull];
      kit.grow(kit.branch(`${name}-link${k}`, st.props, from, to, kit.MINT, 0.08, 0.75), tTalk + 0.18 * k, 0.4);
      const said = parts.spark(`${name}-said${k}`, st.front, kit.MINT, 0.55);
      for (let t = tTalk + 0.7 + 0.31 * k, n = 0; t + 0.7 < end - 0.3; t += 1.9, n++) parts.send(said, n % 2 ? [to, from] : [from, to], t, t + 0.7, { spin: 3 });
    });
  });
  PAIRS.forEach((pair, k) => cues.push({ t: tTalk + 0.18 * k, type: 'tick', pitch: 1.0 + 0.08 * k, gain: 0.6 }));
  [PEOPLE, AGENTS].forEach((at, k) => {
    const either = kit.ring(`either${k}`, st.front, at, 2.9, kit.PAPER, 0.07);
    kit.flash(either, tWhether + 0.9 * k, 1.0, 0.15);
    cues.push({ t: tWhether + 0.9 * k, type: 'chime', gain: 0.45, pitch: 0.9 + 0.2 * k, dur: 1.2 });
  });

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([[0, [0, 0.5, 18.5]], [tAppear - 0.6, [0, 0.4, 19]], [tAppear + 0.8, [0, -0.3, 21.5]], [end, [0, -0.35, 20.6]]]), 1.0);
  return cues;
}
