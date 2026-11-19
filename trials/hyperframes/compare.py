"""Set a scene's Hyperframes clip beside its Blender clip.

    python3 trials/hyperframes/compare.py --blender out/trial/blender/00-pip.mp4 --hyperframes out/trial/hyperframes.mp4 \
        --seconds 41.5 --cues out/trial/new.sfx.json out/trial/blender/00-pip.sfx.json --out out/trial/compare

It writes, into --out:

    even-<frame>.jpg        one frame of each clip side by side at half size, Blender on the left, for frames spread evenly
    worst-<frame>.jpg       the same, for the frames where the two clips are least alike
    summary.md              how long the Hyperframes render took, how alike the two clips are, and whether the cues match

--seconds is how long the Hyperframes render took. The likeness is ffmpeg's
SSIM, where 1 means the same picture: over every frame, and for the worst
frames. --cues takes the scene's sound effect cues as the page gives them and
as Blender gave them, and the summary says whether they are the same.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

EVEN = 6            # stills spread evenly through the scene
WORST = 4           # stills of the frames least alike
APART = 30          # the worst frames are at least this many frames apart


def run(*command):
    return subprocess.run(command, check=True, capture_output=True, text=True)


def probe(path):
    out = run('ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries',
              'stream=width,height,r_frame_rate,nb_read_frames', '-of', 'json', str(path))
    stream = json.loads(out.stdout)['streams'][0]
    return {'width': stream['width'], 'height': stream['height'], 'rate': stream['r_frame_rate'], 'frames': int(stream['nb_read_frames'])}


def still(blender, hyperframes, n, path):
    pick = f'select=eq(n\\,{n}),scale=iw/2:ih/2'
    run('ffmpeg', '-y', '-v', 'error', '-i', blender, '-i', hyperframes, '-filter_complex',
        f'[0:v]{pick}[a];[1:v]{pick}[b];[a][b]hstack', '-frames:v', '1', '-q:v', '3', str(path))


def same_cues(new, old):
    """Whether two lists of cues are the same, and where they first differ."""
    if len(new) != len(old):
        return f'{len(new)} cues against {len(old)}'
    for i, (a, b) in enumerate(zip(new, old)):
        for name in sorted(set(a) | set(b)):
            x, y = a.get(name), b.get(name)
            numbers = isinstance(x, (int, float)) and isinstance(y, (int, float))
            if (abs(x - y) > 1e-6) if numbers else (x != y):
                return f'cue {i}, {name}: {x!r} against {y!r}'
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--blender', required=True)
    ap.add_argument('--hyperframes', required=True)
    ap.add_argument('--seconds', type=float, required=True)
    ap.add_argument('--cues', nargs=2, default=None)
    ap.add_argument('--title', default='A scene')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    old, new = probe(a.blender), probe(a.hyperframes)
    frames = min(old['frames'], new['frames'])

    log = out / 'ssim.log'
    alike = subprocess.run(['ffmpeg', '-v', 'info', '-i', a.blender, '-i', a.hyperframes, '-lavfi', f'ssim=stats_file={log}', '-f', 'null', '-'],
                           check=True, capture_output=True, text=True).stderr
    overall = re.search(r'All:([0-9.]+)', alike)
    each = sorted((float(m.group(2)), int(m.group(1)) - 1) for m in re.finditer(r'n:(\d+) .*?All:([0-9.]+)', log.read_text(encoding='utf-8')))
    worst = []
    for score, n in each:
        if all(abs(n - m) >= APART for _, m in worst):
            worst.append((score, n))
        if len(worst) == WORST:
            break
    log.unlink()

    for k in range(EVEN):
        n = min(frames - 1, round((k + 0.5) * frames / EVEN))
        still(a.blender, a.hyperframes, n, out / f'even-{n:04d}.jpg')
    for _, n in worst:
        still(a.blender, a.hyperframes, n, out / f'worst-{n:04d}.jpg')

    cues = 'not compared'
    if a.cues:
        differ = same_cues(*(json.loads(Path(p).read_text(encoding='utf-8')) for p in a.cues))
        cues = f'differ: {differ}' if differ else 'the same'
    lines = [
        f'## {a.title}',
        '',
        '| | Blender | Hyperframes |',
        '| --- | --- | --- |',
        f'| Frames | {old["frames"]} | {new["frames"]} |',
        f'| Frame | {old["width"]}x{old["height"]} at {old["rate"]} | {new["width"]}x{new["height"]} at {new["rate"]} |',
        f'| Time for the render | | {a.seconds:.0f} seconds, {new["frames"] / a.seconds:.1f} frames a second |',
        '',
        f'Likeness of the two clips (SSIM over every frame, 1 is the same picture): {overall.group(1) if overall else "not measured"}',
        '',
        'The frames least alike: ' + ', '.join(f'{n} ({score:.3f})' for score, n in worst),
        '',
        f'Sound effect cues: {cues}',
        '',
    ]
    (out / 'summary.md').write_text('\n'.join(lines), encoding='utf-8')
    print('\n'.join(lines))


main()
