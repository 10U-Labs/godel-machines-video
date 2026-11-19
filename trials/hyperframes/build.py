"""Put one scene of a production together as a page that Hyperframes renders.

    python3 trials/hyperframes/build.py godel-machines 00-pip --timings out/trial/blender/00-pip.timings.json \
        --out out/trial/page

The page is page.html with the scene's length and narration timings written in.
Beside it, in assets/, go the trial's kit, the production's own scripts
(trials/hyperframes/<production>/*.js), the scene's script
(trials/hyperframes/<production>/scenes/<scene id>.js), and the fonts in
src/fonts/. The frame size and the frame rate are the production's [picture]
settings, and the scene has as many frames as Blender renders for it.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import production  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('production')
    ap.add_argument('scene')
    ap.add_argument('--timings', required=True, help='the scene\'s narration timings, as a run keeps them with its clip')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    picture = production.settings(a.production)['picture']
    entry = json.loads(Path(a.timings).read_text(encoding='utf-8'))
    frames = int(round(entry['duration'] * picture['fps']))
    scripts = sorted((HERE / a.production).glob('*.js')) + [HERE / a.production / 'scenes' / f'{a.scene}.js']

    out = Path(a.out)
    assets = out / 'assets'
    (assets / 'fonts').mkdir(parents=True, exist_ok=True)
    for path in [HERE / 'kit.js'] + scripts:
        shutil.copy(path, assets / path.name)
    for path in (ROOT / 'src/fonts').glob('*.ttf'):
        shutil.copy(path, assets / 'fonts' / path.name)

    values = {
        'title': entry['title'],
        'width': picture['width'],
        'height': picture['height'],
        'fps': picture['fps'],
        'frames': frames,
        'duration': f'{frames / picture["fps"]:.6f}',
        'timings': json.dumps({'duration': entry['duration'], 'lines': [{'start': ln['start'], 'end': ln['end']} for ln in entry['lines']]}),
        'scripts': '\n'.join(f'    <script src="assets/{path.name}"></script>' for path in scripts),
    }
    page = (HERE / 'page.html').read_text(encoding='utf-8')
    for name, value in values.items():
        page = page.replace('{{' + name + '}}', str(value))
    (out / 'index.html').write_text(page, encoding='utf-8')
    print(f'{out / "index.html"}: {frames} frames at {picture["fps"]} a second, {picture["width"]}x{picture["height"]}')


main()
