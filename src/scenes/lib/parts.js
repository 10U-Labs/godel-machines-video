// Reusable drawn components. Each returns the elements a scene animates.
import { svg, place, rand, lerp, clamp } from './anim.js';
import { C } from './palette.js';

export const W = 1920;
export const H = 1080;
export const MONO = "'JetBrains Mono', monospace";

// Narration timings for one scene, written by src/voice/make_voice.py.
//   T.L(n) / T.E(n)   start / end of line n (1-based), in scene seconds
//   T.word(n, 'phrase')  estimated moment the phrase is spoken in line n
//   T.offset          where the scene starts in the whole film
export async function loadTimings(sceneId) {
  const res = await fetch('/out/voice/timings.json', { cache: 'no-store' });
  const all = await res.json();
  let offset = 0;
  for (const sc of all.scenes) {
    if (sc.id === sceneId) {
      const L = (n) => sc.lines[n - 1].start;
      const E = (n) => sc.lines[n - 1].end;
      const word = (n, phrase) => {
        const text = sc.lines[n - 1].text;
        const i = text.indexOf(phrase);
        if (i < 0) throw new Error(`"${phrase}" is not in line ${n} of ${sceneId}`);
        return lerp(L(n), E(n), i / text.length);
      };
      return { duration: sc.duration, offset, lines: sc.lines, L, E, word };
    }
    offset += sc.duration;
  }
  throw new Error(`No timings for scene ${sceneId}`);
}

// Night-sky backdrop shared by every scene. Driven by film time (scene offset
// + t) so it carries on without a jump across cuts between scenes.
export function backdrop(stage) {
  const defs = svg('defs', {}, stage);
  const grad = svg('radialGradient', { id: 'backdrop-grad', cx: '40%', cy: '42%', r: '85%' }, defs);
  svg('stop', { offset: '0%', 'stop-color': C.ink700 }, grad);
  svg('stop', { offset: '55%', 'stop-color': C.ink800 }, grad);
  svg('stop', { offset: '100%', 'stop-color': C.ink900 }, grad);
  svg('rect', { width: W, height: H, fill: 'url(#backdrop-grad)' }, stage);

  const blobs = [
    { x: 1500, y: 180, r: 420, fill: C.ink600, o: 0.33, dx: 46, dy: 26, period: 47 },
    { x: 240, y: 960, r: 360, fill: C.ink600, o: 0.28, dx: -34, dy: -22, period: 61 },
    { x: 1720, y: 940, r: 240, fill: C.violetDeep, o: 0.15, dx: -26, dy: 30, period: 53 },
  ].map((b) => ({ ...b, el: svg('circle', { r: b.r, fill: b.fill }, stage) }));

  const dots = Array.from({ length: 46 }, (_, i) => ({
    x: rand(i * 3 + 1) * W,
    y: rand(i * 3 + 2) * H,
    r: 1.5 + rand(i * 3 + 3) * 2.5,
    phase: rand(i * 7 + 5) * Math.PI * 2,
    el: svg('circle', { fill: C.mist }, stage),
  }));
  for (const d of dots) d.el.setAttribute('r', d.r);

  return (filmTime) => {
    for (const b of blobs) {
      const a = (filmTime / b.period) * Math.PI * 2;
      place(b.el, { x: b.x + b.dx * Math.sin(a), y: b.y + b.dy * Math.cos(a), o: b.o });
    }
    for (const d of dots) {
      const y = (((d.y - filmTime * 1.6) % H) + H) % H;
      d.el.setAttribute('cx', d.x);
      d.el.setAttribute('cy', y.toFixed(2));
      d.el.setAttribute('opacity', (0.25 + 0.2 * Math.sin(filmTime * 1.3 + d.phase)).toFixed(3));
    }
  };
}

// Text label.
export function label(parent, str, { x = 0, y = 0, size = 40, weight = 600, fill = C.paper, anchor = 'start', mono = false } = {}) {
  const attrs = { x, y, 'font-size': size, 'font-weight': weight, fill, 'text-anchor': anchor, text: str };
  if (mono) attrs['font-family'] = MONO;
  return svg('text', attrs, parent);
}

// A program shown as a window of code. The group is centred on its own origin.
// rows: [{ indent, w, color }] gives each line of code as a bar.
export function programWindow(parent, { w = 760, h = 540, title = 'program.py', rows = [], header = 78, top = 50, rowGap = 44, barH = 20, pad = 56, indentW = 52 } = {}) {
  const g = svg('g', {}, parent);
  const L = -w / 2;
  const T = -h / 2;
  svg('rect', { x: L + 14, y: T + 20, width: w, height: h, rx: 34, fill: C.ink900, opacity: 0.45 }, g);
  svg('rect', { x: L, y: T, width: w, height: h, rx: 34, fill: C.ink600 }, g);
  svg('rect', { x: L, y: T + header, width: w, height: h - header, rx: 34, fill: C.ink700 }, g);
  svg('rect', { x: L, y: T + header, width: w, height: 40, fill: C.ink700 }, g);
  [C.coral, C.amber, C.mint].forEach((fill, i) => {
    svg('circle', { cx: L + 48 + i * 40, cy: T + header / 2 + 1, r: 12, fill }, g);
  });
  const titleEl = label(g, title, { x: L + w - 40, y: T + header / 2 + 11, size: 28, fill: C.mist, anchor: 'end' });

  const rowY = (i) => T + header + top + i * rowGap;
  const rowX = (indent = 0) => L + pad + indent * indentW;
  const bars = svg('g', {}, g);
  const lines = rows.map((r, i) => {
    const x = rowX(r.indent || 0);
    const y = rowY(i);
    const el = svg('rect', { x, y, height: barH, rx: barH / 2, fill: r.color || C.mist, width: r.w }, bars);
    return {
      el, x, y, w: r.w,
      set(frac) {
        el.setAttribute('width', Math.max(0, r.w * frac).toFixed(2));
      },
    };
  });
  return { g, w, h, L, T, header, barH, rowY, rowX, bars, lines, titleEl };
}

// Horizontal meter with a label above it. The group's origin is its left end.
export function meter(parent, { w = 760, h = 30, text = '', color = C.mint, size = 30 } = {}) {
  const g = svg('g', {}, parent);
  const textEl = label(g, text, { x: 0, y: -20, size, fill: C.mist });
  svg('rect', { x: 0, y: 0, width: w, height: h, rx: h / 2, fill: C.ink600 }, g);
  const fill = svg('rect', { x: 0, y: 0, height: h, rx: h / 2, fill: color }, g);
  return {
    g, textEl,
    set(level) {
      fill.setAttribute('width', (w * clamp(level)).toFixed(2));
    },
  };
}

// An arrow that draws itself along a path; the head rides the tip.
export function arrow(parent, d, { color = C.paper, width = 7, head = 20 } = {}) {
  const g = svg('g', {}, parent);
  const path = svg('path', { d, fill: 'none', stroke: color, 'stroke-width': width, 'stroke-linecap': 'round' }, g);
  const len = path.getTotalLength();
  path.setAttribute('stroke-dasharray', `${len} ${len}`);
  const tip = svg('path', {
    d: `M ${-head} ${-head * 0.62} L 0 0 L ${-head} ${head * 0.62}`,
    fill: 'none', stroke: color, 'stroke-width': width, 'stroke-linecap': 'round', 'stroke-linejoin': 'round',
  }, g);
  return {
    g, path, len,
    draw(p, o = 1) {
      p = clamp(p);
      path.setAttribute('stroke-dashoffset', (len * (1 - p)).toFixed(2));
      const a = path.getPointAtLength(len * p);
      const b = path.getPointAtLength(Math.max(0, len * p - 3));
      const ang = (Math.atan2(a.y - b.y, a.x - b.x) * 180) / Math.PI;
      tip.setAttribute('transform', `translate(${a.x.toFixed(2)} ${a.y.toFixed(2)}) rotate(${ang.toFixed(2)})`);
      g.setAttribute('opacity', p <= 0.001 ? 0 : clamp(o).toFixed(3));
    },
    pointAt(p) {
      return path.getPointAtLength(len * clamp(p));
    },
  };
}

// Rounded pill with a word or two in it, centred on its origin.
export function chip(parent, str, { size = 30, fill = C.ink600, color = C.paper, padX = 26, weight = 600 } = {}) {
  const g = svg('g', {}, parent);
  const w = str.length * size * 0.56 + padX * 2;
  const h = size * 1.75;
  const box = svg('rect', { x: -w / 2, y: -h / 2, width: w, height: h, rx: h / 2, fill }, g);
  const textEl = label(g, str, { x: 0, y: size * 0.35, size, weight, fill: color, anchor: 'middle' });
  return { g, w, h, box, textEl };
}

// A plain text document (not a program): a light page with lines of text.
export function docCard(parent, { w = 420, h = 520, rows = 8, title = 'notes.txt', seed = 7 } = {}) {
  const g = svg('g', {}, parent);
  const L = -w / 2;
  const T = -h / 2;
  const fold = 54;
  const page = `M ${L + 22} ${T} H ${L + w - fold} L ${L + w} ${T + fold} V ${T + h - 22} a 22 22 0 0 1 -22 22 H ${L + 22} a 22 22 0 0 1 -22 -22 V ${T + 22} a 22 22 0 0 1 22 -22 z`;
  svg('path', { d: page, fill: C.ink900, opacity: 0.4, transform: 'translate(12 18)' }, g);
  svg('path', { d: page, fill: C.paper }, g);
  svg('path', { d: `M ${L + w - fold} ${T} V ${T + fold - 14} a 14 14 0 0 0 14 14 H ${L + w} z`, fill: C.mist }, g);
  const rowY = (i) => T + 84 + i * 46;
  const lines = Array.from({ length: rows }, (_, i) => {
    const lw = (w - 110) * (0.55 + 0.45 * rand(seed + i * 5));
    const el = svg('rect', { x: L + 48, y: rowY(i), height: 16, rx: 8, fill: C.slate, width: lw }, g);
    return {
      el, w: lw, y: rowY(i),
      set(frac) {
        el.setAttribute('width', Math.max(0, lw * frac).toFixed(2));
      },
    };
  });
  const titleEl = label(g, title, { x: 0, y: T + h + 52, size: 28, fill: C.mist, anchor: 'middle' });
  return { g, w, h, L, T, lines, rowY, titleEl };
}

// A person, drawn as a simple figure: head and shoulders.
export function person(parent, { color = C.sky, shade = C.skyDeep } = {}) {
  const g = svg('g', {}, parent);
  svg('path', { d: 'M -78 150 C -78 60 -44 22 0 22 C 44 22 78 60 78 150 Z', fill: color }, g);
  svg('path', { d: 'M 0 22 C 44 22 78 60 78 150 L 30 150 C 34 90 26 50 0 22 Z', fill: shade, opacity: 0.55 }, g);
  svg('circle', { cx: 0, cy: -34, r: 46, fill: C.paper }, g);
  svg('path', { d: 'M 0 -80 A 46 46 0 0 1 0 12 A 60 60 0 0 0 0 -80 Z', fill: C.mist, opacity: 0.7 }, g);
  return { g };
}
