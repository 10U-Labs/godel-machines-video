// Tiny deterministic animation helpers. Every scene is a pure function of time:
// nothing here reads the clock, so frame N always looks the same.

export const clamp = (x, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, x));
export const lerp = (a, b, p) => a + (b - a) * p;

export const ease = {
  linear: (p) => p,
  in: (p) => p * p * p,
  out: (p) => 1 - Math.pow(1 - p, 3),
  inOut: (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
  outQuint: (p) => 1 - Math.pow(1 - p, 5),
  outBack: (p) => {
    const c1 = 1.70158;
    const c3 = c1 + 1;
    return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2);
  },
  outElastic: (p) => {
    if (p === 0 || p === 1) return p;
    return Math.pow(2, -10 * p) * Math.sin((p * 10 - 0.75) * ((2 * Math.PI) / 3)) + 1;
  },
};

// Progress 0..1 of time t through the window [start, start + dur], eased.
export function prog(t, start, dur, easing = ease.out) {
  if (dur <= 0) return t >= start ? 1 : 0;
  return easing(clamp((t - start) / dur));
}

// How visible something is at time t if it fades in at `start` and has faded
// out again by `end`.
export function during(t, start, end, fade = 0.4) {
  return prog(t, start, fade) * (1 - prog(t, end - fade, fade));
}

// Value at time t along keyframes [[time, value, easing?], ...] (numbers only).
// The easing on a keyframe shapes the approach to that keyframe.
export function kf(t, frames) {
  if (t <= frames[0][0]) return frames[0][1];
  for (let i = 1; i < frames.length; i++) {
    const [t1, v1, e = ease.inOut] = frames[i];
    if (t <= t1) {
      const [t0, v0] = frames[i - 1];
      return lerp(v0, v1, e(clamp((t - t0) / (t1 - t0))));
    }
  }
  return frames[frames.length - 1][1];
}

// Deterministic pseudo-random number in [0, 1) from an integer seed.
export function rand(seed) {
  let x = (seed * 0x9e3779b1 + 0x7f4a7c15) >>> 0;
  x ^= x >>> 16;
  x = Math.imul(x, 0x85ebca6b);
  x ^= x >>> 13;
  x = Math.imul(x, 0xc2b2ae35);
  x ^= x >>> 16;
  return (x >>> 0) / 4294967296;
}

const SVG_NS = 'http://www.w3.org/2000/svg';

// Create an SVG element with attributes, optionally appended to a parent.
export function svg(tag, attrs = {}, parent = null) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'text') el.textContent = v;
    else el.setAttribute(k, v);
  }
  if (parent) parent.appendChild(el);
  return el;
}

// Position, scale, rotate and fade an SVG element around its own origin.
export function place(el, { x = 0, y = 0, s = 1, sx = s, sy = s, r = 0, o = 1 } = {}) {
  el.setAttribute('transform', `translate(${x.toFixed(3)} ${y.toFixed(3)}) rotate(${r.toFixed(3)}) scale(${sx.toFixed(4)} ${sy.toFixed(4)})`);
  el.setAttribute('opacity', clamp(o).toFixed(4));
}

// The bundled fonts every scene draws with. A scene refuses to start without
// them, so a render can never fall back to whatever font the machine has.
const FONTS = ['400 30px Figtree', '700 30px Figtree', '500 30px "JetBrains Mono"'];

// Register the scene with the capture harness. `sfx` lists the scene's sound
// cues as [{ t, type, pitch?, dur?, gain? }] for the soundtrack mixer. In a
// normal browser tab the scene also plays in real time (add ?t=3.2 to hold a
// single moment) so it can be previewed.
export function mount({ duration, render, sfx = [] }) {
  window.SCENE = { duration, render, sfx };
  window.SCENE_READY = Promise.all(FONTS.map((f) => document.fonts.load(f))).then((loaded) => {
    const missing = FONTS.filter((_, i) => loaded[i].length === 0);
    if (missing.length) throw new Error(`Fonts did not load: ${missing.join(', ')}`);
    render(0);
  });

  if (!navigator.webdriver) {
    const hold = new URLSearchParams(location.search).get('t');
    window.SCENE_READY.then(() => {
      if (hold !== null) {
        render(Number(hold));
        return;
      }
      const start = performance.now();
      const tick = (now) => {
        render(((now - start) / 1000) % duration);
        requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }
}
