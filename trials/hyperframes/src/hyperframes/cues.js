/* Print a scene's sound effect cues, by building the scene without drawing it.

    node src/hyperframes/cues.js out/godel-machines/pages/00-pip

Takes the folder of a page that page.py wrote, runs the page's scripts in the
order the page loads them, and calls the scene's build(T). Prints the cues it
returns as JSON, in order of time. A scene that fails to build stops here,
before any frame is rendered.
*/
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const page = process.argv[2];
if (!page) {
  console.error('Give the folder of a page that page.py wrote');
  process.exit(2);
}
const context = vm.createContext({ console });
const run = (script) => {
  vm.runInContext(fs.readFileSync(path.join(page, 'assets', script), 'utf8'), context, { filename: script });
};
run('setup.js');
for (const script of vm.runInContext('SETUP.scripts', context)) run(script);
const cues = vm.runInContext(`
  kit.setup({ fps: SETUP.fps, frames: SETUP.frames, width: SETUP.width, height: SETUP.height });
  JSON.stringify((build(new kit.Timing(SETUP.timings)) || []).sort((a, b) => a.t - b.t), null, 1);
`, context);
console.log(cues);
