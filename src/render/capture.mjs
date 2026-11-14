// Films a scene page frame by frame in headless Chrome and encodes it with ffmpeg.
//
//   node src/render/capture.mjs <scene.html> --out out/scene.mp4 [--from 0 --to 12.5]
//   node src/render/capture.mjs <scene.html> --still 3.2 --out out/still.png
//
// Scene contract: the page sets window.SCENE = { duration, render(t), sfx } where
// render(t) draws the frame for time t (seconds) as a pure function of t, and
// window.SCENE_READY is a promise that resolves once fonts and assets are loaded.
// A full render also writes the scene's sound cues beside the video, as
// <name>.sfx.json, for the soundtrack mixer.

import puppeteer from 'puppeteer';
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const WIDTH = 1920;
export const HEIGHT = 1080;
export const FPS = 30;

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
};

// Static file server for the project folder, on localhost only.
function serve() {
  const server = http.createServer((req, res) => {
    const urlPath = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    const file = path.normalize(path.join(ROOT, urlPath));
    if (!file.startsWith(ROOT + path.sep)) {
      res.writeHead(403).end();
      return;
    }
    fs.readFile(file, (err, data) => {
      if (err) {
        res.writeHead(404).end('not found');
        return;
      }
      res.writeHead(200, {
        'Content-Type': MIME[path.extname(file)] || 'application/octet-stream',
        'Cache-Control': 'no-store',
      });
      res.end(data);
    });
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

function parseArgs(argv) {
  const args = { scene: null, out: null, still: null, from: null, to: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') args.out = argv[++i];
    else if (a === '--still') args.still = Number(argv[++i]);
    else if (a === '--from') args.from = Number(argv[++i]);
    else if (a === '--to') args.to = Number(argv[++i]);
    else if (!args.scene) args.scene = a;
    else throw new Error(`Unexpected argument: ${a}`);
  }
  if (!args.scene || !args.out) {
    throw new Error('Usage: capture.mjs <scene.html> --out <file> [--still seconds | --from s --to s]');
  }
  return args;
}

function startEncoder(outFile) {
  const ff = spawn(
    'ffmpeg',
    [
      '-hide_banner', '-loglevel', 'error', '-y',
      '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
      '-vf', 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
      '-r', String(FPS), '-g', String(FPS * 2),
      '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
      '-movflags', '+faststart',
      outFile,
    ],
    { stdio: ['pipe', 'inherit', 'inherit'] },
  );
  const done = new Promise((resolve, reject) => {
    ff.on('error', reject);
    ff.on('close', (code) => (code === 0 ? resolve() : reject(new Error(`ffmpeg exited with ${code}`))));
  });
  return { ff, done };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const scenePath = path.resolve(args.scene);
  if (!scenePath.startsWith(ROOT + path.sep)) throw new Error('Scene must be inside the project folder.');
  fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });

  const server = await serve();
  const { port } = server.address();
  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || undefined,
    headless: 'shell',
    args: [
      '--hide-scrollbars', '--force-color-profile=srgb', '--font-render-hinting=none',
      ...(process.env.CI ? ['--no-sandbox'] : []),
    ],
  });

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 });
    page.on('pageerror', (e) => console.error('[page error]', e.message));
    page.on('console', (m) => {
      if (m.type() === 'error' || m.type() === 'warning') console.error(`[page ${m.type()}]`, m.text());
    });

    const rel = path.relative(ROOT, scenePath).split(path.sep).map(encodeURIComponent).join('/');
    await page.goto(`http://127.0.0.1:${port}/${rel}`, { waitUntil: 'load' });
    await page.waitForFunction(() => window.SCENE_READY !== undefined, { timeout: 15000 });
    await page.evaluate(() => window.SCENE_READY);
    const duration = await page.evaluate(() => window.SCENE.duration);

    const shot = async (t) => {
      await page.evaluate((time) => window.SCENE.render(time), t);
      return page.screenshot({ type: 'png', captureBeyondViewport: false, optimizeForSpeed: true });
    };

    if (args.still !== null) {
      fs.writeFileSync(args.out, await shot(args.still));
      console.log(`still at ${args.still}s -> ${args.out}`);
      return;
    }

    const first = Math.round((args.from ?? 0) * FPS);
    const last = Math.round((args.to ?? duration) * FPS); // exclusive
    const sfx = await page.evaluate(() => window.SCENE.sfx || []);
    fs.writeFileSync(args.out.replace(/\.mp4$/, '') + '.sfx.json', JSON.stringify(sfx, null, 2));
    const { ff, done } = startEncoder(args.out);
    const started = Date.now();
    for (let f = first; f < last; f++) {
      const png = await shot(f / FPS);
      if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await done;
    const secs = (Date.now() - started) / 1000;
    const n = last - first;
    console.log(`${n} frames in ${secs.toFixed(1)}s (${(n / secs).toFixed(1)} fps) -> ${args.out}`);
  } finally {
    await browser.close();
    server.close();
  }
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
