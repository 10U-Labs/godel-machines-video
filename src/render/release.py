"""Publish a production as a GitHub release that keeps its film, its captions, and its scene clips.

    python3 src/render/release.py godel-machines --target 0bf8678d5c1f

A workflow run keeps what it makes as artifacts, and GitHub deletes those
after 90 days. A release is kept, and anyone can see it.

The release is tagged <name>-v<time>, where <time> is the moment the release
is made, in UTC, as fourteen digits: godel-machines-v20261115172101. --target
is the commit the tag is put on, which is the commit the film was made from.
The release holds:

    <name>.mp4              the film
    <name>.srt              its closed captions
    <clip name>.zip         for each scene, what the artifact under its clip's
                            name holds (see src/hyperframes/clips.py): the clip,
                            its sound effect cues, and the narration it was
                            rendered for

The film and the captions are read from out/<name>/. The scenes are the ones
in out/<name>/clips.json, which src/hyperframes/plan.py wrote, and each one's clip
is downloaded from whichever workflow run made it.

Prints the tag. A later run takes the clips back from the release when it is
given the tag to adopt (see src/hyperframes/plan.py).
"""
import argparse
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / 'hyperframes'))
import clips  # noqa: E402
import production  # noqa: E402

NOTES = """\
`{name}.mp4` is the film, and `{name}.srt` holds its closed captions.

Each `scene-{name}-<scene>-<hash>.zip` holds one scene of the film: its clip, its sound effect cues, and the narration the clip was rendered for. A later render takes these clips in place of rendering the scenes again.
"""


def pack(out, packed):
    """Put each scene's clip, as its artifact holds it, into an archive named after the clip, and return the archives."""
    archives = []
    for scene, clip in json.loads((out / 'clips.json').read_text(encoding='utf-8')).items():
        run = clips.find(clip)
        if run is None:
            raise SystemExit(f'Scene {scene} has no clip: no artifact named {clip} is left')
        with tempfile.TemporaryDirectory() as tmp:
            clips.download(run, clip, Path(tmp))
            archives.append(shutil.make_archive(str(packed / clip), 'zip', tmp))
        print(f'{scene:<28} {clip}  from run {run}', file=sys.stderr)
    return archives


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('production')
    ap.add_argument('--target', required=True)
    a = ap.parse_args()
    name = a.production
    out = production.out(name)
    title = production.settings(name)['title']
    finished = [out / f'{name}.mp4', out / f'{name}.srt']
    for path in finished:
        if not path.exists():
            raise SystemExit(f'{path} does not exist; the release holds the finished film and its captions')

    with tempfile.TemporaryDirectory() as tmp:
        archives = pack(out, Path(tmp))
        tag = f"{name}-v{time.strftime('%Y%m%d%H%M%S', time.gmtime())}"
        clips.gh(
            'release', 'create', tag, '--target', a.target, '--title', title, '--notes', NOTES.format(name=name),
            *map(str, finished), *archives,
        )
    print(tag)


if __name__ == '__main__':
    main()
