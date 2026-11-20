/* Scene 10: The last message.

Pip stands by the board among dark agents, the dull key in its hand and its
clock down to a sliver. It thinks of a pass that will not come, and then of a
folder. A spark goes from Pip to the board, a folder appears there, and its
name is written, ending in a dull key. Back on Pip, the last of the clock
goes, and Pip goes dark. Its folder stays lit on the board.
*/
'use strict';

function build(T) {
  const { sec, alpha } = kit;
  parts.begin();

  const BOARD = [-9.6, 0.4];
  const PIP = [-4.6, -2.5];
  const HELD = [PIP[0], PIP[1] - 0.7];
  const KEY = [PIP[0] + 1.05, PIP[1] - 0.25];
  const CLOCK = [PIP[0] - 1.75, PIP[1] + 0.35];
  const OVER = [PIP[0] + 0.6, PIP[1] + 2.55];
  const PRESS = [-2.0, -2.7];
  const POST = [-11.7, 2.55];

  const cues = [];
  const end = sec(kit.frames());
  const tNews = T.start(0);
  const tTell = T.start(1);
  const tStill = T.at(1, 0.5);
  const tMade = T.start(2);
  const tWrote = T.at(2, 0.45);
  const tUp = T.start(3);

  kit.backdrop(6, kit.SKY_DEEP);
  kit.motes(14, 13);
  const st = parts.stage();

  // ------------------------------------------------------------ the board, and the agents around it, most of them dark
  parts.board('board', st.props, BOARD, { scale: 0.8 });
  const spots = [];
  for (const x of [-13.4, -12.0, -10.6, -9.2, -7.8, -6.4]) spots.push([x, -3.75 - (spots.length % 2) * 0.4], [x + 0.3, 4.3 + (spots.length % 2) * 0.35]);
  spots.push([-5.9, 2.6], [-6.0, 0.9], [-5.8, -0.8], [-4.4, 1.8], [-4.3, 0.1]);
  parts.crowd('agent', st.cast, spots, 0.52, 27).forEach((made, i) => {
    if ((i * 7 + 3) % 10 < 6) parts.miniOff(made, -1, 0);
    else parts.bob(made.root, 0, end, i * 0.9, 0.04);
  });
  parts.dark(parts.agent('presser', st.cast, PRESS, 0.8, 4));

  // ------------------------------------------------------------ Pip, a key that no longer works, and a little time
  const pip = parts.agent('pip', st.cast, PIP, 0.9);
  parts.mood(pip, 0, 'sad', 0);
  parts.word('held', st.front, HELD, 0.85, false);
  const mine = parts.doorKey('pip-key', st.front, KEY, 0.95, 0.5);
  for (const part of mine.shapes) alpha(part, 1, 0.35);
  const broken = parts.cross('broken', st.front, [KEY[0] + 0.1, KEY[1] + 0.05], 0.75);
  kit.pop(broken, tNews + 0.9, 0.75, 0.3, tTell - 0.1);
  parts.shake(mine.root, tNews + 0.9, 0.4, 0.06);
  cues.push({ t: tNews + 0.9, type: 'tick', pitch: 0.5, gain: 1.2 });
  kit.pipLook(pip, tNews, 0.11, -0.08);

  const clock = parts.clock('clock', st.front, CLOCK, 1.0, 0.09);
  parts.drain(clock, 0.3, tUp, 0.0);
  for (let t = 0.5; t < tUp - 0.2; t += 0.5) cues.push({ t, type: 'tick', pitch: 1.4, gain: 0.6 });

  // ------------------------------------------------------------ it would not help Pip pass, and Pip tells them all the same
  const over = parts.thought('over', st.front, OVER, 2.4, 1.5, [-0.6, -1]);
  kit.pop(over.root, tTell + 0.1, 1.0, 0.35, tMade + 0.2);
  cues.push({ t: tTell + 0.1, type: 'pop', pitch: 0.8 });
  const noPass = parts.group('no-pass', over.root, [0, 0]);
  parts.check('no-pass-tick', noPass, [0, 0], 1.1, kit.SLATE);
  parts.cross('no-pass-cross', noPass, [0, 0], 1.3);
  kit.pop(noPass, tTell + 0.5, 1.0, 0.3, tStill - 0.2, 0.2);
  cues.push({ t: tTell + 0.5, type: 'tick', pitch: 0.55 });
  const plan = parts.folder('plan', over.root, [-0.75, 0], { scale: 0.75, bars: [0.5, 0.7] });
  kit.pop(plan.root, tStill + 0.1, 0.75, 0.3);
  cues.push({ t: tStill + 0.1, type: 'pop', pitch: 1.1 });
  kit.pipLook(pip, tTell + 0.3, 0.05, 0.11);
  kit.pipLook(pip, tStill, -0.14, 0.06);
  parts.mood(pip, tStill + 0.2, 'flat');

  // ------------------------------------------------------------ one more folder
  const news = parts.spark('news', st.front, kit.MINT, 0.8);
  kit.pipArm(pip, 'left', tMade, 95, 0.25);
  parts.send(news, [[PIP[0] - 1.1, PIP[1]], [-7.5, 2.2], POST], tMade + 0.2, tMade + 1.1, { spin: 4 });
  kit.pipArm(pip, 'left', tMade + 1.1, 18, 0.3);
  const last = parts.folder('last', st.front, POST, { scale: 0.7, bars: [0.8, 0.5, 0.7], tail: 1.0 });
  kit.pop(last.root, tMade + 1.1, 0.7, 0.35);
  cues.push({ t: tMade + 0.2, type: 'rise', dur: 0.9, pitch: 1.2, gain: 0.5 }, { t: tMade + 1.1, type: 'pop', pitch: 1.2 });
  const written = parts.write(last, tWrote, 0.3);
  for (const t of written) cues.push({ t, type: 'tick', pitch: 1.3 });
  const sign = parts.doorKey('last-key', last.root, [last.tail + 0.5, -0.03], 0.75);
  const struck = parts.cross('last-cross', last.root, [last.tail + 0.55, -0.03], 0.7);
  const tSigned = tWrote + 0.3 * written.length;
  for (const part of sign.shapes) kit.appear(part, tSigned, null, 0.1, 0.45);
  kit.pop(struck, tSigned + 0.3, 0.7, 0.25);
  cues.push({ t: tSigned, type: 'tick', pitch: 1.3 }, { t: tSigned + 0.3, type: 'tick', pitch: 0.6 }, { t: tSigned + 0.6, type: 'chime', gain: 0.45, dur: 1.6 });
  kit.pipLook(pip, tUp - 2.2, -0.1, 0.09);

  // ------------------------------------------------------------ Pip's time is up
  const out = kit.ring('out', st.front, CLOCK, 0.65, kit.CORAL, 0.08);
  kit.flash(out, tUp, 0.9, 0.5);
  cues.push({ t: tUp, type: 'tick', pitch: 0.35, gain: 1.6 });
  parts.mood(pip, tUp - 0.4, 'worried', 0.2);
  parts.off(pip, tUp + 0.35, 0.6);
  parts.live(pip, 25, 0, tUp + 0.35);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([
    [0, [PIP[0] + 0.4, PIP[1] + 0.1, 11.5]], [tTell, [PIP[0] + 0.4, PIP[1] + 0.3, 12]], [tTell + 1.2, [PIP[0] + 0.4, PIP[1] + 0.9, 13.5]],
    [tMade + 0.2, [PIP[0] + 0.3, PIP[1] + 0.9, 13.5]], [tMade + 1.4, [-10.0, 1.9, 12.5]], [tUp - 2.6, [-10.0, 1.9, 12]],
    [tUp - 1.2, [-7.3, -0.4, 18.5]], [tUp + 0.4, [-7.2, -0.5, 18]], [end, [-7.0, -0.3, 21]],
  ]), 1.0);
  return cues;
}
