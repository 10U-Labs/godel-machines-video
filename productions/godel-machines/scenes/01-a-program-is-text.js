/* Scene 01: A program is text.

A blank page appears beside Pip and fills with numbered lines of plain
instructions, then folds into a file. A stream of files passes under Pip, who
reads each one; the stream stops at a file marked with Pip's face. Pip opens
it, and one instruction is crossed out and rewritten.
*/
'use strict';

function build(T) {
  const { fr, sec, span, mix, key, hold, alpha, every } = kit;

  const LINES = ['read the program', 'run its tests', 'find the line that fails', 'write a fix', 'run the tests again'];
  const NEW_LINE = 'write three fixes, keep the best';
  const CHANGED = 3;

  const PAGE_AT = [1.3, 0.1];
  const [PAGE_W, PAGE_H] = [8.4, 5.0];
  const PIP_SIDE = [-5.6, -0.3];
  const PIP_TOP = [0.0, 1.5];
  const STREAM_Y = -2.2;
  const GAP = 1.75;

  /* A page of numbered instructions. Each line hides under a cover that can wipe away. */
  const page = (stage) => {
    const root = kit.empty('page', stage, [PAGE_AT[0], PAGE_AT[1], kit.nextZ(stage)]);
    kit.shape('page-shadow', kit.rrectPts(PAGE_W + 0.6, PAGE_H + 0.6, 0.6), kit.glowMaterial(kit.INK900, 0.7, 0.8), root, [0.15, -0.2]);
    kit.shape('page-paper', kit.rrectPts(PAGE_W, PAGE_H, 0.24), kit.material(kit.INK700), root);
    kit.shape('page-bar', kit.rrectPts(PAGE_W, 0.64, 0.24).map(([x, y]) => [x, y + PAGE_H / 2 - 0.32]), kit.material(kit.INK600), root);
    kit.shape('page-bar-fill', kit.rrectPts(PAGE_W, 0.32, 0).map(([x, y]) => [x, y + PAGE_H / 2 - 0.48]), kit.material(kit.INK600), root);
    [kit.CORAL, kit.AMBER, kit.MINT].forEach((c, i) => {
      kit.shape(`page-dot${i}`, kit.circlePts(0.09), kit.material(c), root, [-PAGE_W / 2 + 0.34 + i * 0.28, PAGE_H / 2 - 0.32]);
    });
    const icon = parts.badge('page-badge', root, [PAGE_W / 2 - 0.5, PAGE_H / 2 - 0.32]);
    const left = -PAGE_W / 2 + 0.55;
    const mono = { face: 'JetBrainsMono', align: 'LEFT' };
    const rows = LINES.map((body, i) => {
      const y = PAGE_H / 2 - 1.25 - i * 0.78;
      const num = kit.text(`num${i}`, `${i + 1}`, 0.36, kit.material(kit.AMBER), root, [left, y], mono);
      const words = kit.text(`line${i}`, body, 0.36, kit.material(kit.PAPER), root, [left + 0.6, y], mono);
      const cover = kit.shape(`cover${i}`, kit.rrectPts(PAGE_W - 0.7, 0.6, 0).map(([x, y2]) => [x - (PAGE_W - 0.7) / 2, y2]),
        kit.material(kit.INK700), root, [PAGE_W / 2 - 0.25, y]);
      return { num, words, cover, y };
    });
    const fresh = kit.text('line-new', NEW_LINE, 0.36, kit.material(kit.MINT), root, [left + 0.6, rows[CHANGED].y], mono);
    const newCover = kit.shape('cover-new', kit.rrectPts(PAGE_W - 1.3, 0.6, 0).map(([x, y2]) => [x - (PAGE_W - 1.3) / 2, y2]),
      kit.material(kit.INK700), root, [PAGE_W / 2 - 0.25, rows[CHANGED].y]);
    const strike = kit.shape('strike', kit.barPts(0.22 * LINES[CHANGED].length + 0.2, 0.07), kit.material(kit.CORAL), root,
      [left + 0.5, rows[CHANGED].y + 0.02]);
    const cursor = kit.shape('cursor', kit.rrectPts(0.2, 0.42, 0.03), kit.material(kit.MINT), root, [left + 0.6, rows[CHANGED].y]);
    return { root, rows, icon, fresh, newCover, strike, cursor, left };
  };

  const cues = [];
  const end = sec(kit.frames());
  const tBlank = T.start(0) + 0.2;
  const tText = T.start(1) + 0.2;
  const tList = T.at(1, 0.5);
  const tFile = T.at(1, 0.8);
  const tStream = T.start(2);
  const tOwn = T.at(2, 0.52);
  const tOpen = T.start(3);
  const tChange = T.at(3, 0.58);

  kit.backdrop(11);
  kit.motes(undefined, 12);
  const stage = kit.layer('stage', 1.0);

  // ------------------------------------------------------------ Pip
  const p = kit.pip('pip', stage, PIP_SIDE, 1.2);
  const zp = p.root.z;
  for (const f of every(1)) {
    const t = sec(f);
    const q1 = span(t, tStream - 0.3, tStream + 0.5);
    const q2 = span(t, tOpen, tOpen + 0.6);
    const x = mix(mix(PIP_SIDE[0], PIP_TOP[0], q1), PIP_SIDE[0], q2);
    const y = mix(mix(PIP_SIDE[1], PIP_TOP[1], q1), PIP_SIDE[1], q2);
    key(p.root, 'loc', f, [x, y, zp]);
  }
  kit.pipIdle(p);
  kit.pipBlink(p, [2.4, 7.0, tStream + 2.0, tOpen + 1.5]);
  kit.pipLook(p, 0.4, 0.13, 0.02);

  // ------------------------------------------------------------ the page of instructions
  const pg = page(stage);
  const root = pg.root;
  const zr = root.z;
  for (const f of every(1)) {
    const t = sec(f);
    const grown = kit.backOut((t - tBlank) / 0.45);
    const shrink = span(t, tFile, tFile + 0.45, (v) => v * v);
    const reopen = kit.backOut((t - tOpen - 0.1) / 0.55);
    const s = t < tOpen ? Math.max(0.001, grown * (1 - shrink)) : Math.max(0.001, reopen);
    const x = t < tOpen ? mix(PAGE_AT[0], 0.0, shrink) : mix(0.0, PAGE_AT[0], span(t, tOpen, tOpen + 0.6));
    const y = t < tOpen ? mix(PAGE_AT[1], STREAM_Y, shrink) : mix(STREAM_Y, PAGE_AT[1], span(t, tOpen, tOpen + 0.6));
    key(root, 'loc', f, [x, y, zr]);
    key(root, 'scale', f, [s, s, 1]);
  }
  cues.push({ t: tBlank, type: 'pop' });
  pg.icon.sx = pg.icon.sy = pg.icon.sz = 0.001;
  hold(pg.icon, 'scale', 1);
  hold(pg.icon, 'scale', fr(tOpen));
  key(pg.icon, 'scale', fr(tOpen + 0.3), [1, 1, 1]);

  pg.rows.forEach((row, i) => {                    // the lines appear one by one
    const t0 = tText + 0.32 * i;
    hold(row.cover, 'scale', fr(t0));
    key(row.cover, 'scale', fr(t0 + 0.3), [0.001, 1, 1]);
    cues.push({ t: t0, type: 'tick', pitch: 0.9 + 0.05 * i });
    const num = row.num;
    hold(num, 'scale', fr(tList + 0.15 * i));
    key(num, 'scale', fr(tList + 0.15 * i + 0.12), [1.45, 1.45, 1]);
    key(num, 'scale', fr(tList + 0.15 * i + 0.3), [1, 1, 1]);
    cues.push({ t: tList + 0.15 * i, type: 'blip', pitch: 1.0 + 0.08 * i, gain: 0.5 });
  });

  // crossed out and rewritten
  const left = pg.left;
  const strike = pg.strike;
  [strike.sx, strike.sy, strike.sz] = [0.001, 1, 1];
  hold(strike, 'scale', 1);
  hold(strike, 'scale', fr(tChange));
  key(strike, 'scale', fr(tChange + 0.25), [1, 1, 1]);
  const old = pg.rows[CHANGED];
  for (const ob of [old.words, strike]) {
    alpha(ob, 1, 1.0);
    alpha(ob, fr(tChange + 0.45), 1.0);
    alpha(ob, fr(tChange + 0.6), 0.0);
  }
  const cover = pg.newCover;
  alpha(cover, 1, 0.0);                      // the cover for the new line waits until the old line is gone
  alpha(cover, fr(tChange + 0.55), 0.0);
  alpha(cover, fr(tChange + 0.56) + 1, 1.0);
  alpha(pg.fresh, 1, 0.0);
  alpha(pg.fresh, fr(tChange + 0.55), 0.0);
  alpha(pg.fresh, fr(tChange + 0.56) + 1, 1.0);
  const tType = tChange + 0.6;
  const tTyped = Math.min(end - 0.3, tType + 0.9);
  hold(cover, 'scale', fr(tType));
  key(cover, 'scale', fr(tTyped), [0.001, 1, 1]);
  const cur = pg.cursor;
  const zc = cur.z;
  const width = 0.216 * NEW_LINE.length;
  for (const f of every(1)) {
    const t = sec(f);
    const q = span(t, tType, tTyped, (v) => v);
    const on = tChange + 0.5 <= t ? 1.0 : 0.0;
    const blink = (t < tType || t > tTyped) && Math.trunc(t * 3) % 2 ? 1.0 : 0.0;
    key(cur, 'loc', f, [left + 0.6 + width * q + 0.1, old.y, zc]);
    alpha(cur, f, on * (1.0 - blink));
  }
  cues.push({ t: tChange, type: 'swoosh', dur: 0.4, gain: 0.6 });
  for (let k = 0; k < 8; k++) cues.push({ t: tType + k * 0.11, type: 'tick', pitch: 1.1 + 0.03 * (k % 3), gain: 0.6 });

  // ------------------------------------------------------------ files streaming past
  // The page becomes the first file. More files come in from the right, and
  // the stream slows so that Pip's own file stops right under Pip.
  const mine = 4;
  const count = mine + 3;
  const x0 = [0.0];
  for (let i = 1; i < count; i++) x0.push(9.5 + (i - 1) * GAP);
  const [tGo, tSlow, dStop] = [tStream, tOwn - 0.6, 0.9];
  const v = x0[mine] / ((tSlow - tGo) + dStop / 2);     // speed that ends with Pip's file at x = 0

  const travel = (t) => {
    if (t < tGo) return 0.0;
    if (t < tSlow) return v * (t - tGo);
    const q = Math.min(1.0, (t - tSlow) / dStop);
    return v * (tSlow - tGo) + v * dStop * (q - q * q / 2);
  };

  const files = x0.map((x, i) => parts.fileIcon(`file${i}`, stage, [x, STREAM_Y], 1.25, i === mine, i));
  files.forEach((fi, i) => {
    const ob = fi.root;
    const z = ob.z;
    let tPass = null;
    for (const f of every(1)) {
      const t = sec(f);
      const x = x0[i] - travel(t);
      key(ob, 'loc', f, [x, STREAM_Y, z]);
      if (tPass === null && i !== 0 && i !== mine && t >= tGo && x <= 0) tPass = t;
      if (i === 0) {
        const s = 1.25 * Math.max(0.001, kit.backOut((t - tFile - 0.3) / 0.4));
        key(ob, 'scale', f, [s, s, 1]);
      }
    }
    if (i === mine) {
      for (const f of every(1, fr(tOwn - 0.3), fr(tOpen))) {
        const t = sec(f);
        alpha(fi.glow, f, span(t, tOwn - 0.2, tOwn + 0.2) * (0.75 + 0.25 * Math.sin((t - tOwn) * 6)));
      }
      alpha(fi.glow, fr(tOpen) + 6, 0.0);
    } else if (tPass !== null) {                    // a flash as each file passes under Pip
      alpha(fi.glow, fr(tPass - 0.15), 0.0);
      alpha(fi.glow, fr(tPass), 0.8);
      alpha(fi.glow, fr(tPass + 0.3), 0.0);
      cues.push({ t: tPass, type: 'blip', pitch: 1.2, gain: 0.35 });
    }
    hold(ob, 'scale', fr(tOpen));   // every file goes as the page reopens
    key(ob, 'scale', fr(tOpen + 0.25), [0.001, 0.001, 1]);
  });
  cues.push({ t: tFile + 0.3, type: 'pop', pitch: 0.8 });
  cues.push({ t: tGo, type: 'whoosh', dur: 1.4, gain: 0.6 });
  cues.push({ t: tOwn, type: 'chime', pitch: 0.9, gain: 0.7 });

  // Pip follows the files with its eyes, then looks down at its own file
  kit.pipLook(p, tText, 0.13, 0.0);
  kit.pipLook(p, tStream + 0.2, 0.08, -0.08);
  for (let k = 0; k < 4; k++) {
    kit.pipLook(p, tStream + 0.5 + 0.55 * k, -0.06, -0.08, 0.45);
    kit.pipLook(p, tStream + 0.75 + 0.55 * k, 0.08, -0.08, 0.05);
  }
  kit.pipLook(p, tOwn - 0.3, 0.0, -0.1, 0.3);
  kit.pipEyes(p, tOwn, 1.2, 1.2, 0.2);
  kit.pipEyes(p, tOpen, 1.0, 1.0, 0.3);
  kit.pipLook(p, tOpen + 0.3, 0.13, 0.02);
  kit.pipArm(p, 'right', tChange - 0.35, 75, 0.25);
  kit.pipArm(p, 'right', tTyped + 0.2, 18, 0.35);

  // ------------------------------------------------------------ camera
  const path = (t) => {
    const q = kit.smooth(t / end);
    return [-0.2 + 0.3 * q, 0.05 * q, kit.H0 - 1.0 * q];
  };

  kit.camera(path, 1.0);
  return cues;
}
