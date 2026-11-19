"""Set a scene's Hyperframes clip beside its Blender clip.

    python3 trials/hyperframes/compare.py --blender out/trial/blender/00-pip.mp4 --hyperframes out/trial/hyperframes.mp4 \
        --narration out/trial/blender/00-pip.wav --seconds 41.5 --out out/trial/compare

It writes, into --out:

    still-<seconds>.png     one frame of each clip side by side, Blender on the left, for each time in --at
    side-by-side.mp4        both clips side by side at half size, with the narration
    summary.md              how long the Hyperframes render took, and how alike the two clips are

--seconds is how long the Hyperframes render took; the summary sets it beside
--blender-minutes, the runner time that Blender took for the same scene.
The likeness is ffmpeg's SSIM over every frame: 1 means the same picture.
"""
import argparse
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path


def run(*command):
    return subprocess.run(command, check=True, capture_output=True, text=True)


def probe(path):
    out = run('ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries',
              'stream=width,height,r_frame_rate,nb_read_frames', '-of', 'json', str(path))
    stream = json.loads(out.stdout)['streams'][0]
    return {'width': stream['width'], 'height': stream['height'], 'rate': stream['r_frame_rate'], 'frames': int(stream['nb_read_frames'])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--blender', required=True)
    ap.add_argument('--hyperframes', required=True)
    ap.add_argument('--narration', required=True)
    ap.add_argument('--seconds', type=float, required=True)
    ap.add_argument('--blender-minutes', type=float, default=None)
    ap.add_argument('--at', default='1,2,4,7.5,9.5,10.1,10.4,12.5,14.5,16,18.5,20,21.9')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    old, new = probe(a.blender), probe(a.hyperframes)
    fps = float(Fraction(old['rate']))                  # a rational such as 30/1

    for t in (float(v) for v in a.at.split(',')):
        n = min(int(round(t * fps)), old['frames'] - 1, new['frames'] - 1)
        pick = f'select=eq(n\\,{n})'
        run('ffmpeg', '-y', '-v', 'error', '-i', a.blender, '-i', a.hyperframes, '-filter_complex',
            f'[0:v]{pick}[a];[1:v]{pick}[b];[a][b]hstack', '-frames:v', '1', str(out / f'still-{t:05.2f}.png'))

    run('ffmpeg', '-y', '-v', 'error', '-i', a.blender, '-i', a.hyperframes, '-i', a.narration, '-filter_complex',
        '[0:v]scale=iw/2:ih/2[a];[1:v]scale=iw/2:ih/2[b];[a][b]hstack[v]', '-map', '[v]', '-map', '2:a',
        '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', str(out / 'side-by-side.mp4'))

    alike = subprocess.run(['ffmpeg', '-v', 'info', '-i', a.blender, '-i', a.hyperframes, '-lavfi', 'ssim', '-f', 'null', '-'],
                           check=True, capture_output=True, text=True).stderr
    ssim = re.search(r'All:([0-9.]+)', alike)

    took, pace = 'not given', 'not given'
    if a.blender_minutes is not None:
        took = f'{a.blender_minutes:.0f} minutes'
        pace = f'{old["frames"] / (a.blender_minutes * 60):.2f}'
    alike = ssim.group(1) if ssim else 'not measured'
    lines = [
        '## Hyperframes beside Blender',
        '',
        '| | Blender | Hyperframes |',
        '| --- | --- | --- |',
        f'| Frames | {old["frames"]} | {new["frames"]} |',
        f'| Frame | {old["width"]}x{old["height"]} at {old["rate"]} | {new["width"]}x{new["height"]} at {new["rate"]} |',
        f'| Runner time for the render | {took} | {a.seconds:.0f} seconds |',
        f'| Frames a second | {pace} | {new["frames"] / a.seconds:.1f} |',
        '',
        f'Likeness of the two clips (SSIM over every frame, 1 is the same picture): {alike}',
        '',
    ]
    (out / 'summary.md').write_text('\n'.join(lines), encoding='utf-8')
    print('\n'.join(lines))


main()
