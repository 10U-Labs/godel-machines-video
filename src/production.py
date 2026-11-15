"""Where a production's material is kept, and where what is made from it goes.

A production is one piece of media the repository makes. Its material is in
productions/<name>/:

    script.md               the narration script
    scenes/<scene>.py       one Blender scene for each scene of the script
    pronunciations.json     hand-written phonemes for words the voice gets wrong
    research/               source material; research/sources/ is not committed

Everything made from it goes under out/<name>/, and the finished files are
out/<name>/<name>.mp4 and out/<name>/<name>.srt.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def folder(name):
    """The folder that holds a production's material."""
    path = ROOT / 'productions' / name
    if not path.is_dir():
        raise SystemExit(f'No production named {name}: {path} is not a folder')
    return path


def out(name):
    """The folder that everything made from a production goes under."""
    folder(name)
    return ROOT / 'out' / name
