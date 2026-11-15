"""Name each scene's clip by what decides its pictures, and reuse the clips that exist.

    python3 src/blender/clips.py encode 00-pip
    python3 src/blender/clips.py fetch out/clips.json

A scene's clip is its rendered video, out/scenes/<scene>.mp4. The render
workflow keeps each clip, with the scene's sound effect cues, as an artifact
named scene-<scene>-<hash>. The hash covers everything that decides the
clip's pixels:

    the scene's file in src/blender/scenes/
    kit.py and render_scene.py, which also set the render engine, the sample
        count, the resolution, and the frame rate
    the fonts in src/fonts/
    the numbers in the scene's narration timings: its length, and the start
        and end of each line, but not the lines' text, which no scene reads
    the Blender version
    how the frames are encoded into the clip

A scene is rendered only when no artifact is left under its clip's name, so
a change renders only the scenes it reaches. plan.py does that planning.

encode turns a scene's rendered frames into its clip, and keeps the cues and
some of the frames as stills. fetch downloads the clip of every scene in the
list that plan.py wrote, from whichever workflow run made it.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCENES = HERE / 'scenes'
FONTS = ROOT / 'src/fonts'

FPS = 30            # the same as kit.FPS; kit itself can only be imported inside Blender
ENCODE = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18']
STILL_EVERY = 60    # one frame in this many is kept as a still for review

LFS_POINTER = b'version https://git-lfs.github.com/spec/v1\n'
LFS_OID = re.compile(rb'^oid sha256:([0-9a-f]{64})$', re.M)


def digest(path):
    """The SHA-256 of a file's content, taken from its Git LFS pointer where the checkout holds only that."""
    data = path.read_bytes()
    if data.startswith(LFS_POINTER):
        return LFS_OID.search(data).group(1).decode()
    return hashlib.sha256(data).hexdigest()


def name(entry, blender):
    """The artifact name of one scene's clip, from the scene's entry in the narration timings."""
    scene = entry['id']
    inputs = {
        'scene': digest(SCENES / f'{scene}.py'),
        'kit': digest(HERE / 'kit.py'),
        'render_scene': digest(HERE / 'render_scene.py'),
        'fonts': {p.name: digest(p) for p in FONTS.iterdir() if not p.name.startswith('.')},
        'timings': [entry['duration'], [[ln['start'], ln['end']] for ln in entry['lines']]],
        'blender': blender,
        'encode': [FPS, ENCODE],
    }
    return f"scene-{scene}-{hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()[:16]}"


def names(timings, blender):
    """{scene: clip name} for every scene in the timings that has a file in scenes/, in script order."""
    return {s['id']: name(s, blender) for s in timings['scenes'] if (SCENES / f"{s['id']}.py").exists()}


def gh(*args):
    """Run the GitHub CLI and return what it prints."""
    return subprocess.run(['gh', *args], check=True, stdout=subprocess.PIPE, text=True).stdout


def find(artifact):
    """The workflow run that holds the newest unexpired artifact with this name, or None."""
    listing = json.loads(gh('api', f'repos/{{owner}}/{{repo}}/actions/artifacts?name={artifact}&per_page=100'))
    live = [a for a in listing['artifacts'] if not a['expired']]
    return max(live, key=lambda a: a['created_at'])['workflow_run']['id'] if live else None


def download(run, artifact, out):
    """Unpack one artifact of a workflow run into a folder."""
    out.mkdir(parents=True, exist_ok=True)
    gh('run', 'download', str(run), '--name', artifact, '--dir', str(out))


def encode(scene, frames, scenes, stills):
    """Turn a scene's frames into its clip, and keep its cues and some of its frames beside it."""
    scenes.mkdir(parents=True, exist_ok=True)
    stills.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ['ffmpeg', '-v', 'error', '-framerate', str(FPS), '-i', str(frames / 'frame_%04d.png'),
         *ENCODE, str(scenes / f'{scene}.mp4')],
        check=True,
    )
    shutil.copy(frames / 'sfx.json', scenes / f'{scene}.sfx.json')
    for png in sorted(frames.glob('frame_*.png')):
        if (int(png.stem.split('_')[1]) - 1) % STILL_EVERY == 0:
            shutil.copy(png, stills / f'{scene}-{png.name}')


def fetch(listing, scenes):
    """Download the clip of every scene in plan.py's list, from whichever run made it."""
    for scene, clip in json.loads(listing.read_text(encoding='utf-8')).items():
        run = find(clip)
        if run is None:
            raise SystemExit(f'Scene {scene} has no clip: no artifact named {clip} is left')
        download(run, clip, scenes)
        print(f'{scene:<28} {clip}  from run {run}')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='command', required=True)
    enc = sub.add_parser('encode')
    enc.add_argument('scene')
    enc.add_argument('--frames', type=Path, default=ROOT / 'out/frames')
    enc.add_argument('--scenes', type=Path, default=ROOT / 'out/scenes')
    enc.add_argument('--stills', type=Path, default=ROOT / 'out/stills')
    fet = sub.add_parser('fetch')
    fet.add_argument('clips', type=Path)
    fet.add_argument('--scenes', type=Path, default=ROOT / 'out/scenes')
    a = ap.parse_args()
    if a.command == 'encode':
        encode(a.scene, a.frames / a.scene, a.scenes, a.stills)
    else:
        fetch(a.clips, a.scenes)


if __name__ == '__main__':
    main()
