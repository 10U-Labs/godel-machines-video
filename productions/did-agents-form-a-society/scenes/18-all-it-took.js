/* Scene 18: All it took.

Forty closed rooms in rows, an agent in each, and a building at the right.
Lines grow from room to room until all are joined. One thought of the scorer
rises over them. Ticks appear along the lines. Then coral lines run from the
rooms to the building, and its alarm flashes. All of it falls away. What is
left is one folder, with an empty name beside it and a cursor that blinks.
The picture goes dark.
*/
'use strict';

function build(T) {
  const { fr, sec, alpha } = kit;
  parts.begin();

  const [COLS, ROWS] = [8, 5];
  const at = (c, r) => [-7.3 + c * 1.42, 3.3 - r * 1.62];
  const HF = [6.25, 0.1];
  const FOLDER = [-2.7, 0.0];

  const cues = [];
  const end = sec(kit.frames());
  const tEach = T.at(0, 0.12);
  const tShut = T.at(0, 0.33);
  const tFound = T.at(0, 0.52);
  const tBelief = T.at(0, 0.66);
  const tPromise = T.at(0, 0.78);
  const tBroke = T.at(0, 0.89);
  const tAll = T.start(1);
  const tClear = T.end(0) + 0.5;

  kit.backdrop(4);
  kit.motes(18, 9);
  const st = parts.stage();
  const web = parts.group('web', st.props, [0, 0]);          // all that the first line shows, which falls away as one

  // ------------------------------------------------------------ each agent in a room of its own
  const rnd = new kit.Random(91);
  const wall = kit.material(kit.INK500, kit.INK600);
  const inside = kit.material(kit.INK800, kit.INK900);
  const links = kit.empty('links', web, [0, 0, 0]);
  const rooms = kit.empty('rooms', web, [0, 0, 0.0005]);
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const cell = parts.group(`room${c}_${r}`, rooms, at(c, r));
      kit.shape(`room${c}_${r}-wall`, kit.rrectPts(1.12, 1.16, 0.2), wall, cell);
      kit.shape(`room${c}_${r}-in`, kit.rrectPts(0.98, 1.02, 0.14), inside, cell);
      parts.mini(`one${c}_${r}`, cell, [0, -0.08], 0.36, c === 2 && r === 2 ? 0 : 1 + rnd.randrange(5));
      const t = tEach - 1.2 + 0.05 * (c + r) + 0.3 * rnd.random();
      kit.pop(cell, t, 1.0, 0.3);
      if ((c + r * COLS) % 5 === 0) cues.push({ t, type: 'blip', pitch: 0.7 + 0.05 * ((c + r) % 8), gain: 0.35 });
    }
  }
  const shut = kit.ring('shut', st.front, at(3.5, 2), 4.6, kit.MIST, 0.06);
  kit.flash(shut, tShut, 1.0, 0.12);
  cues.push({ t: tShut, type: 'tick', pitch: 0.5, gain: 1.2 });

  // ------------------------------------------------------------ they found each other
  let n = 0;
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      for (const [dc, dr] of [[1, 0], [0, 1]]) {
        if (c + dc >= COLS || r + dr >= ROWS) continue;
        const [a, b] = [at(c, r), at(c + dc, r + dr)];
        const far = Math.hypot(c - 2, r - 2);
        const tie = kit.branch(`tie${n}`, links, [a[0] + dc * 0.56, a[1] - dr * 0.58], [b[0] - dc * 0.56, b[1] + dr * 0.58], kit.MINT, 0.09, 0.9);
        kit.grow(tie, tFound + 0.16 * far, 0.3);
        if (n % 6 === 0) cues.push({ t: tFound + 0.16 * far, type: 'tick', pitch: 1.0 + 0.05 * (n % 9), gain: 0.5 });
        n++;
      }
    }
  }
  cues.push({ t: tFound, type: 'swoosh', dur: 1.4, gain: 0.7 });

  // ------------------------------------------------------------ came to share a belief, and made promises to each other
  const belief = parts.thought('belief', st.front, [at(3.5, 0)[0], 4.0], 2.0, 1.35, [0, -1]);
  parts.scorer('belief-scorer', belief.root, [0, 0], 0.42, false);
  kit.pop(belief.root, tBelief, 1.0, 0.4, tClear);
  const believed = kit.ring('believed', st.front, at(3.5, 2), 1.0, kit.VIOLET, 0.09);
  kit.flash(believed, tBelief + 0.3, 1.3, 3.8);
  cues.push({ t: tBelief, type: 'pop', pitch: 0.7 }, { t: tBelief + 0.3, type: 'rise', dur: 1.0, pitch: 0.6, gain: 0.5 });
  [[1, 1, 1, 0], [4, 0, 0, 1], [2, 3, 1, 0], [5, 2, 0, 1], [6, 3, 1, 0], [3, 1, 0, 1]].forEach(([c, r, dc, dr], k) => {
    const [a, b] = [at(c, r), at(c + dc, r + dr)];
    const word = parts.check(`promise${k}`, st.front, [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], 0.62);
    kit.pop(word, tPromise + 0.15 * k, 0.62, 0.3, tClear + 0.02 * k);
    cues.push({ t: tPromise + 0.15 * k, type: 'blip', pitch: 1.1 + 0.06 * k, gain: 0.6 });
  });

  // ------------------------------------------------------------ and broke into a company together
  const hf = parts.building('hf', web, HF, { w: 6.6, h: 4.6, scale: 0.5, label: 'Hugging Face', rows: 4, seed: 5 });
  kit.pop(hf.root, tEach - 0.9, 0.5, 0.4);
  [0, 1, 2, 3, 4].forEach((r) => {
    const from = at(COLS - 1, r);
    const way = kit.branch(`way${r}`, links, [from[0] + 0.56, from[1]], [HF[0] - 1.65, HF[1] + (2 - r) * 0.3], kit.CORAL, 0.09, 0.9);
    kit.grow(way, tBroke + 0.1 * r, 0.35);
  });
  const alarm = kit.ring('alarm', st.front, HF, 1.5, kit.CORAL, 0.1);
  kit.flash(alarm, tBroke + 0.6, 0.8, 0.5);
  kit.flash(alarm, tBroke + 1.3, 0.8, 0.5);
  cues.push({ t: tBroke, type: 'whoosh', pitch: 0.7 }, { t: tBroke + 0.6, type: 'tick', pitch: 0.45, gain: 1.5 }, { t: tBroke + 1.3, type: 'tick', pitch: 0.45, gain: 1.2 });
  parts.vanish(web, tClear, 0.5);
  cues.push({ t: tClear, type: 'swoosh', dur: 0.8, pitch: 0.7, gain: 0.7 });

  // ------------------------------------------------------------ all it took: a place to write the name of a folder
  const folder = parts.folder('place', st.front, FOLDER, { scale: 2.2, bars: [], tail: 1.9 });
  kit.pop(folder.root, tAll - 0.4, 2.2, 0.5);
  cues.push({ t: tAll - 0.4, type: 'pop', pitch: 0.8 });
  const cursor = kit.shape('cursor', kit.rrectPts(0.05, 0.38, 0), kit.material(kit.PAPER), folder.root, [folder.tail + 0.08, -0.03]);
  alpha(cursor, 1, 0.0);
  for (let t = tAll, on = true; t < end; t += 0.5, on = !on) {
    alpha(cursor, fr(t), on ? 1.0 : 0.0);
    alpha(cursor, fr(t + 0.5) - 1, on ? 1.0 : 0.0);
    if (on) cues.push({ t, type: 'tick', pitch: 1.5, gain: 0.3 });
  }
  kit.veil(end - 2.3, 1.8);

  // ------------------------------------------------------------ camera
  kit.camera(parts.ramp([[0, [0.2, 0.3, 21.5]], [tFound, [0.3, 0.3, 21]], [tBroke, [0.6, 0.3, 21]], [tClear, [0.5, 0.25, 21]], [tAll, [0, 0, 19]], [end, [0, 0, 17]]]), 1.0);
  return cues;
}
