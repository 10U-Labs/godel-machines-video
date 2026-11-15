"""Name each scene's clip by what decides its pictures, and reuse the clips that exist.

    python3 src/blender/clips.py encode godel-machines 00-pip
    python3 src/blender/clips.py adopt godel-machines 00-pip --run 43741576538 \
        --artifact scene-00-pip-f2b80fbdaa2b5e32 --narration 43741576538
    python3 src/blender/clips.py fetch godel-machines

A scene's clip is its rendered video, out/<name>/scenes/<scene>.mp4. The
render workflow keeps each clip as an artifact named
scene-<name>-<scene>-<hash>. The hash covers everything that decides the
clip's pixels:

    the scene's file in productions/<name>/scenes/
    the production's own modules, the Python files directly in
        productions/<name>/, which its scenes import
    kit.py and render_scene.py
    the fonts in src/fonts/
    the production's [picture] settings: the frame size, the frame rate, the
        render engine, and the sample count
    the key of the scene's narration, which make_voice.py writes: what is
        spoken, but not the numbers in the timings
    the Blender version
    how the frames are encoded into the clip

A scene is rendered only when no artifact is left under its clip's name, so
a change renders only the scenes it reaches. plan.py does that planning.

A scene's pictures are timed to the start and end of each narration line, and
two machines can give the same line clips of slightly different lengths. So
the artifact holds, beside the clip, the narration the scene was rendered for,
and that narration is used wherever the clip is:

    <scene>.mp4             the clip
    <scene>.sfx.json        the scene's sound effect cues
    <scene>.wav             the scene's narration track
    <scene>.timings.json    the scene's entry in the narration timings

encode turns a scene's rendered frames into its clip, keeps the cues and the
narration beside it, and keeps some of the frames as stills. adopt takes a
clip that an earlier run kept under another name. fetch downloads the clip of
every scene in the list that plan.py wrote, from whichever workflow run made
it, and puts each clip's narration in place of the run's own.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import production  # noqa: E402

FONTS = HERE.parent / 'fonts'

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


def name(scenes, entry, picture, blender):
    """The artifact name of one scene's clip, from the scene's entry in the narration timings."""
    scene = entry['id']
    inputs = {
        'scene': digest(scenes / f'{scene}.py'),
        'own': {p.name: digest(p) for p in scenes.parent.glob('*.py')},
        'kit': digest(HERE / 'kit.py'),
        'render_scene': digest(HERE / 'render_scene.py'),
        'fonts': {p.name: digest(p) for p in FONTS.iterdir() if not p.name.startswith('.')},
        'picture': picture,
        'narration': entry['key'],
        'blender': blender,
        'encode': ENCODE,
    }
    made_from = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()[:16]
    return f'scene-{scenes.parent.name}-{scene}-{made_from}'


def names(scenes, timings, picture, blender):
    """{scene: clip name} for every scene in the timings that has a file in scenes/, in script order."""
    return {
        s['id']: name(scenes, s, picture, blender)
        for s in timings['scenes'] if (scenes / f"{s['id']}.py").exists()
    }


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


def keep_narration(scene, voice, scenes):
    """Put a scene's narration track and its entry in the timings beside its clip."""
    timings = json.loads((voice / 'timings.json').read_text(encoding='utf-8'))
    entry = next(s for s in timings['scenes'] if s['id'] == scene)
    shutil.copy(voice / f'{scene}.wav', scenes / f'{scene}.wav')
    (scenes / f'{scene}.timings.json').write_text(json.dumps(entry, indent=1, ensure_ascii=False), encoding='utf-8')


def encode(scene, out, fps):
    """Turn a scene's frames into its clip, and keep its cues, its narration, and some stills."""
    frames, scenes, stills = out / 'frames' / scene, out / 'scenes', out / 'stills'
    scenes.mkdir(parents=True, exist_ok=True)
    stills.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ['ffmpeg', '-v', 'error', '-framerate', str(fps), '-i', str(frames / 'frame_%04d.png'),
         *ENCODE, str(scenes / f'{scene}.mp4')],
        check=True,
    )
    shutil.copy(frames / 'sfx.json', scenes / f'{scene}.sfx.json')
    keep_narration(scene, out / 'voice', scenes)
    for png in sorted(frames.glob('frame_*.png')):
        if (int(png.stem.split('_')[1]) - 1) % STILL_EVERY == 0:
            shutil.copy(png, stills / f'{scene}-{png.name}')


def adopt(scene, run, artifact, narration, scenes):
    """Download a scene's clip from an artifact of an earlier run, with the narration it was rendered for.

    A clip kept before narration was kept with it takes its narration from the
    'narration' artifact of the run given for that.
    """
    download(run, artifact, scenes)
    for kept in ('mp4', 'sfx.json'):
        if not (scenes / f'{scene}.{kept}').exists():
            raise SystemExit(f'Artifact {artifact} of run {run} holds no {scene}.{kept}')
    if not (scenes / f'{scene}.timings.json').exists():
        with tempfile.TemporaryDirectory() as tmp:
            download(narration, 'narration', Path(tmp))
            keep_narration(scene, Path(tmp), scenes)


def fetch(out):
    """Download the clip of every scene in plan.py's list, and put its narration in place of the run's own.

    The narration track and the numbers in the timings come from the clip's
    artifact. The lines' text stays the run's own, so a change to the script
    that leaves a line sounding the same still reaches the captions.
    """
    scenes, voice = out / 'scenes', out / 'voice'
    timings = json.loads((voice / 'timings.json').read_text(encoding='utf-8'))
    entries = {s['id']: s for s in timings['scenes']}
    for scene, clip in json.loads((out / 'clips.json').read_text(encoding='utf-8')).items():
        run = find(clip)
        if run is None:
            raise SystemExit(f'Scene {scene} has no clip: no artifact named {clip} is left')
        download(run, clip, scenes)
        kept = json.loads((scenes / f'{scene}.timings.json').read_text(encoding='utf-8'))
        entry = entries[scene]
        if len(kept['lines']) != len(entry['lines']):
            raise SystemExit(f'{clip} was rendered for {len(kept["lines"])} lines, and scene {scene} has {len(entry["lines"])}')
        entry['duration'] = kept['duration']
        for line, was in zip(entry['lines'], kept['lines']):
            line['start'], line['end'] = was['start'], was['end']
        shutil.copy(scenes / f'{scene}.wav', voice / f'{scene}.wav')
        print(f'{scene:<28} {clip}  from run {run}')
    timings['duration'] = round(sum(s['duration'] for s in timings['scenes']), 3)
    (voice / 'timings.json').write_text(json.dumps(timings, indent=2, ensure_ascii=False), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='command', required=True)
    enc = sub.add_parser('encode')
    enc.add_argument('production')
    enc.add_argument('scene')
    ado = sub.add_parser('adopt')
    ado.add_argument('production')
    ado.add_argument('scene')
    ado.add_argument('--run', required=True)
    ado.add_argument('--artifact', required=True)
    ado.add_argument('--narration', required=True)
    fet = sub.add_parser('fetch')
    fet.add_argument('production')
    a = ap.parse_args()
    out = production.out(a.production)
    if a.command == 'encode':
        encode(a.scene, out, production.settings(a.production)['picture']['fps'])
    elif a.command == 'adopt':
        adopt(a.scene, a.run, a.artifact, a.narration, out / 'scenes')
    else:
        fetch(out)


if __name__ == '__main__':
    main()
