"""Name each scene's clip by what decides its pictures, and reuse the clips that exist.

    python3 src/hyperframes/clips.py keep godel-machines 00-pip
    python3 src/hyperframes/clips.py adopt godel-machines 00-pip --source 43741576538 \
        --artifact scene-00-pip-f2b80fbdaa2b5e32 --narration 43741576538
    python3 src/hyperframes/clips.py fetch godel-machines

A scene's clip is its rendered video, out/<name>/scenes/<scene>.mp4. The
render workflow keeps each clip as an artifact named
scene-<name>-<scene>-<hash>. The hash covers everything that decides the
clip's pixels:

    the scene's file in productions/<name>/scenes/
    the production's own scripts, the .js files directly in
        productions/<name>/, which its scenes use
    kit.js, page.html, page.py, and cues.js
    the fonts in src/fonts/
    the production's [picture] settings: the frame size and the frame rate
    the key of the scene's narration, which make_voice.py writes: what is
        spoken, but not the numbers in the timings
    package-lock.json, which gives the version of Hyperframes and of
        everything it depends on
    the options that Hyperframes renders the clip with

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

An artifact is deleted 90 days after its run. src/render/release.py keeps the
same four files of each scene in a GitHub release, as an asset named
<clip name>.zip.

keep takes the clip that Hyperframes rendered from a scene's page (see
page.py), checks that it has a frame for every frame of the scene, keeps the
narration beside it and the cues that page.py wrote, and keeps some of its
frames as stills. adopt takes a clip that an earlier run or a release kept,
under another name or the same one; --source is the run's id or the release's
tag. fetch downloads the clip of every scene in the list that plan.py wrote,
from whichever workflow run made it, and puts each clip's narration in place
of the run's own. render prints the options that Hyperframes renders a clip
with, for the render workflow to pass on.
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
LOCK = HERE.parents[1] / 'package-lock.json'

RENDER = ['--crf', '18']    # the options Hyperframes renders a clip with; the render workflow reads them from here
STILL_EVERY = 60            # one frame in this many is kept as a still for review

LFS_POINTER = b'version https://git-lfs.github.com/spec/v1\n'
LFS_OID = re.compile(rb'^oid sha256:([0-9a-f]{64})$', re.M)


def digest(path):
    """The SHA-256 of a file's content, taken from its Git LFS pointer where the checkout holds only that."""
    data = path.read_bytes()
    if data.startswith(LFS_POINTER):
        return LFS_OID.search(data).group(1).decode()
    return hashlib.sha256(data).hexdigest()


def name(scenes, entry, picture):
    """The artifact name of one scene's clip, from the scene's entry in the narration timings."""
    scene = entry['id']
    inputs = {
        'scene': digest(scenes / f'{scene}.js'),
        'own': {p.name: digest(p) for p in scenes.parent.glob('*.js')},
        'page': {p: digest(HERE / p) for p in ('kit.js', 'page.html', 'page.py', 'cues.js')},
        'fonts': {p.name: digest(p) for p in FONTS.iterdir() if not p.name.startswith('.')},
        'picture': picture,
        'narration': entry['key'],
        'hyperframes': digest(LOCK),
        'render': RENDER,
    }
    made_from = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()[:16]
    return f'scene-{scenes.parent.name}-{scene}-{made_from}'


def names(scenes, timings, picture):
    """{scene: clip name} for every scene in the timings that has a file in scenes/, in script order."""
    return {
        s['id']: name(scenes, s, picture)
        for s in timings['scenes'] if (scenes / f"{s['id']}.js").exists()
    }


def gh(*args):
    """Run the GitHub CLI and return what it prints."""
    return subprocess.run(['gh', *args], check=True, stdout=subprocess.PIPE, text=True).stdout


def find(artifact):
    """The workflow run that holds the newest unexpired artifact with this name, or None."""
    listing = json.loads(gh('api', f'repos/{{owner}}/{{repo}}/actions/artifacts?name={artifact}&per_page=100'))
    live = [a for a in listing['artifacts'] if not a['expired']]
    return max(live, key=lambda a: a['created_at'])['workflow_run']['id'] if live else None


def download(source, artifact, out):
    """Unpack into a folder what a workflow run keeps as an artifact, or a release as an asset.

    A run is given by its id, which is all digits, and a release by its tag.
    The release's asset is <artifact>.zip.
    """
    out.mkdir(parents=True, exist_ok=True)
    if str(source).isdigit():
        gh('run', 'download', str(source), '--name', artifact, '--dir', str(out))
        return
    with tempfile.TemporaryDirectory() as tmp:
        gh('release', 'download', source, '--pattern', f'{artifact}.zip', '--dir', tmp)
        shutil.unpack_archive(Path(tmp) / f'{artifact}.zip', out)


def keep_narration(scene, voice, scenes):
    """Put a scene's narration track and its entry in the timings beside its clip."""
    timings = json.loads((voice / 'timings.json').read_text(encoding='utf-8'))
    entry = next(s for s in timings['scenes'] if s['id'] == scene)
    shutil.copy(voice / f'{scene}.wav', scenes / f'{scene}.wav')
    (scenes / f'{scene}.timings.json').write_text(json.dumps(entry, indent=1, ensure_ascii=False), encoding='utf-8')


def keep(scene, out, fps):
    """Take the clip that Hyperframes rendered from a scene's page, and keep its narration and some stills beside it.

    The clip is out/<name>/pages/<scene>.mp4. It has to hold one frame for
    every frame of the scene, or the film's pictures would drift from its
    sound, and it has to hold pictures alone.
    """
    scenes, stills = out / 'scenes', out / 'stills'
    stills.mkdir(parents=True, exist_ok=True)
    rendered, clip = out / 'pages' / f'{scene}.mp4', scenes / f'{scene}.mp4'
    if not (scenes / f'{scene}.sfx.json').exists():
        raise SystemExit(f'Scene {scene} has no cues: page.py writes them when it builds the page')
    timings = json.loads((out / 'voice/timings.json').read_text(encoding='utf-8'))
    entry = next(s for s in timings['scenes'] if s['id'] == scene)
    wanted = int(round(entry['duration'] * fps))
    probe = subprocess.run(
        ['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_type,nb_read_frames', '-of', 'json', str(rendered)],
        check=True, stdout=subprocess.PIPE, text=True,
    )
    streams = json.loads(probe.stdout)['streams']
    if [s['codec_type'] for s in streams] != ['video']:
        raise SystemExit(f'{rendered} holds {[s["codec_type"] for s in streams]}, where a clip holds one video stream and nothing else')
    if int(streams[0]['nb_read_frames']) != wanted:
        raise SystemExit(f'{rendered} has {streams[0]["nb_read_frames"]} frames, and scene {scene} has {wanted}')
    shutil.copy(rendered, clip)
    keep_narration(scene, out / 'voice', scenes)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ['ffmpeg', '-v', 'error', '-i', str(clip), '-vf', f"select='not(mod(n,{STILL_EVERY}))'", '-fps_mode', 'vfr',
             str(Path(tmp) / '%04d.png')],
            check=True,
        )
        for k, png in enumerate(sorted(Path(tmp).glob('*.png'))):
            shutil.copy(png, stills / f'{scene}-frame_{k * STILL_EVERY + 1:04d}.png')


def adopt(scene, source, artifact, narration, scenes):
    """Download a scene's clip from an earlier run or from a release, with the narration it was rendered for.

    A clip kept before narration was kept with it takes its narration from the
    'narration' artifact of the run given for that.
    """
    download(source, artifact, scenes)
    for kept in ('mp4', 'sfx.json'):
        if not (scenes / f'{scene}.{kept}').exists():
            raise SystemExit(f'{artifact} of {source} holds no {scene}.{kept}')
    if not (scenes / f'{scene}.timings.json').exists():
        if not narration:
            raise SystemExit(f'{artifact} of {source} holds no narration for {scene}, and no run is given to take it from')
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
    kee = sub.add_parser('keep')
    kee.add_argument('production')
    kee.add_argument('scene')
    sub.add_parser('render')
    ado = sub.add_parser('adopt')
    ado.add_argument('production')
    ado.add_argument('scene')
    ado.add_argument('--source', required=True)
    ado.add_argument('--artifact', required=True)
    ado.add_argument('--narration', default='')
    fet = sub.add_parser('fetch')
    fet.add_argument('production')
    a = ap.parse_args()
    if a.command == 'render':
        print(' '.join(RENDER))
        return
    out = production.out(a.production)
    if a.command == 'keep':
        keep(a.scene, out, production.settings(a.production)['picture']['fps'])
    elif a.command == 'adopt':
        adopt(a.scene, a.source, a.artifact, a.narration, out / 'scenes')
    else:
        fetch(out)


if __name__ == '__main__':
    main()
