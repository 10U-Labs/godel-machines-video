"""Put one scene of a production together as a page that Hyperframes renders.

    python3 src/hyperframes/page.py godel-machines 00-pip
    npx hyperframes render out/godel-machines/pages/00-pip --output out/godel-machines/pages/00-pip.mp4

Each scene lives in productions/<name>/scenes/<scene id>.js and defines
build(T), which builds the scene for the length of its narration and returns
its sound effect cues as a list of {t: seconds, type: ...}. A scene uses the
shared kit (kit.js) and any script of its own production, a .js file directly
in productions/<name>/. The narration timings are read from
out/<name>/voice/timings.json.

The page is written to out/<name>/pages/<scene id>/:

    index.html              page.html, with the scene's size and length written in
    assets/setup.js         the frame size, the frame rate, the number of
                            frames, and the scene's narration timings
    assets/kit.js           the shared kit
    assets/own/             the production's own scripts, loaded in name order
    assets/scene.js         the scene
    assets/fonts/           the fonts in src/fonts/

The scene's cues are written to out/<name>/scenes/<scene id>.sfx.json. They
come from running the same scripts under Node (see cues.js), which also shows
that the scene builds before any frame is rendered.

The frame size and the frame rate are the production's [picture] settings (see
src/production.py). Frames count from 1, and frame f shows the scene at
(f - 1) / fps seconds.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import production  # noqa: E402

FONTS = HERE.parent / 'fonts'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('production')
    ap.add_argument('scene')
    a = ap.parse_args()

    out = production.out(a.production)
    folder = production.folder(a.production)
    timings = json.loads((out / 'voice/timings.json').read_text(encoding='utf-8'))
    entry = next((s for s in timings['scenes'] if s['id'] == a.scene), None)
    if entry is None:
        raise SystemExit(f'No timings for scene {a.scene}')
    scene = folder / 'scenes' / f'{a.scene}.js'
    if not scene.exists():
        raise SystemExit(f'{scene} does not exist')
    picture = production.settings(a.production)['picture']
    frames = int(round(entry['duration'] * picture['fps']))

    page = out / 'pages' / a.scene
    if page.exists():
        shutil.rmtree(page)
    assets = page / 'assets'
    (assets / 'own').mkdir(parents=True)
    (assets / 'fonts').mkdir()
    shutil.copy(HERE / 'kit.js', assets / 'kit.js')
    own = sorted(folder.glob('*.js'))
    for path in own:
        shutil.copy(path, assets / 'own' / path.name)
    shutil.copy(scene, assets / 'scene.js')
    for path in FONTS.glob('*.ttf'):
        shutil.copy(path, assets / 'fonts' / path.name)

    scripts = ['kit.js'] + [f'own/{path.name}' for path in own] + ['scene.js']
    setup = {
        'width': picture['width'],
        'height': picture['height'],
        'fps': picture['fps'],
        'frames': frames,
        'timings': {'duration': entry['duration'], 'lines': [{'start': ln['start'], 'end': ln['end']} for ln in entry['lines']]},
        'scripts': scripts,
    }
    (assets / 'setup.js').write_text(f'const SETUP = {json.dumps(setup)};\n', encoding='utf-8')
    values = {
        'title': entry['title'],
        'width': picture['width'],
        'height': picture['height'],
        'duration': f'{frames / picture["fps"]:.6f}',
        'scripts': '\n'.join(f'    <script src="assets/{script}"></script>' for script in scripts),
    }
    html = (HERE / 'page.html').read_text(encoding='utf-8')
    for name, value in values.items():
        html = html.replace('{{' + name + '}}', str(value))
    (page / 'index.html').write_text(html, encoding='utf-8')

    cues = subprocess.run(['node', str(HERE / 'cues.js'), str(page)], check=True, stdout=subprocess.PIPE, text=True).stdout
    (out / 'scenes').mkdir(parents=True, exist_ok=True)
    (out / 'scenes' / f'{a.scene}.sfx.json').write_text(cues, encoding='utf-8')
    print(f'{page}: {frames} frames at {picture["fps"]} a second, {picture["width"]}x{picture["height"]}, {len(json.loads(cues))} cues')


if __name__ == '__main__':
    main()
