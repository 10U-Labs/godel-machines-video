"""Publish a production as a GitHub release that holds its film and its captions, and nothing else.

    python3 src/render/release.py godel-machines --target 0bf8678d5c1f

A workflow run keeps what it makes as artifacts, and GitHub deletes those
after 90 days. A release is kept, and anyone can see it.

The release is tagged <name>-v<time>, where <time> is the moment the release
is made, in UTC, as fourteen digits: godel-machines-v20261115172101. --target
is the commit the tag is put on, which is the commit the film was made from.
The release holds:

    <name>.mp4              the film
    <name>.srt              its closed captions

Both are read from out/<name>/. Prints the tag.
"""
import argparse
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / 'hyperframes'))
import clips  # noqa: E402
import production  # noqa: E402

NOTES = '`{name}.mp4` is the film, and `{name}.srt` holds its closed captions.\n'


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

    tag = f"{name}-v{time.strftime('%Y%m%d%H%M%S', time.gmtime())}"
    clips.gh(
        'release', 'create', tag, '--target', a.target, '--title', title, '--notes', NOTES.format(name=name),
        *map(str, finished),
    )
    print(tag)


if __name__ == '__main__':
    main()
