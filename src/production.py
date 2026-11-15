"""Where a production's material is kept, where what is made from it goes, and its settings.

A production is one piece of media the repository makes. Its material is in
productions/<name>/:

    production.toml         its title, and any settings it wants to set
    script.md               the narration script
    scenes/<scene>.py       one Blender scene for each scene of the script
    <module>.py             what its scenes share and no other production uses,
                            such as its cast and props
    pronunciations.json     hand-written phonemes for words the voice gets wrong
    research/               source material; research/sources/ is not committed

Everything made from it goes under out/<name>/, and the finished files are
out/<name>/<name>.mp4 and out/<name>/<name>.srt.

production.toml gives the title and, in a table for each kind, any of the
settings in DEFAULTS:

    title = "Machines That Rewrite Themselves"

    [voice]
    speed = 0.95

A setting the file leaves out takes its value from DEFAULTS, and no tool keeps
a copy of one.
"""
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULTS = {
    'voice': {
        'name': 'af_heart',     # a Kokoro voice
        'lang': 'en-us',
        'speed': 0.95,
        'lead_in': 0.6,         # seconds of silence before a scene's first line
        'line_gap': 0.38,       # seconds of silence between consecutive lines
        'tail': 0.7,            # seconds of silence after a scene's last line
    },
    'picture': {
        'width': 1920,          # the kit lays scenes out for a 16:9 frame
        'height': 1080,
        'fps': 30,
        'engine': 'eevee',      # or 'cycles'
        'samples': 24,
    },
    'sound': {
        'voice_peak': 0.6,      # narration peaks sit near -4 dBFS
        'music_level': 0.36,    # music level between lines
        'music_duck': 0.65,     # share of the music removed while the narrator speaks
        'effects_level': 0.6,
        'loudness': -14.0,      # LUFS, the level the finished soundtrack is brought to
        'true_peak': -1.5,      # dBTP, the highest peak it may reach
        'loudness_range': 11.0,  # LU
    },
    'captions': {
        'row': 42,              # most characters on one caption row
        'gap': 0.05,            # seconds of blank between two captions from one line
    },
}


KINDS = {str: ('a string', str), int: ('a whole number', int), float: ('a number', (int, float))}


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


def settings(name):
    """A production's title and settings: what its production.toml gives, and the default for the rest."""
    path = folder(name) / 'production.toml'
    if not path.exists():
        raise SystemExit(f'{path} does not exist; it gives the production its title')
    given = tomllib.loads(path.read_text(encoding='utf-8'))
    title = given.pop('title', None)
    if not isinstance(title, str) or not title:
        raise SystemExit(f'{path} gives no title')
    result = {'title': title}
    for table, defaults in DEFAULTS.items():
        own = given.pop(table, {})
        if not isinstance(own, dict):
            raise SystemExit(f'{path}: {table} is a table of settings, written as [{table}]')
        for key, value in own.items():
            if key not in defaults:
                raise SystemExit(f'{path}: [{table}] has no setting named {key}')
            kind, accepted = KINDS[type(defaults[key])]
            if isinstance(value, bool) or not isinstance(value, accepted):
                raise SystemExit(f'{path}: {key} in [{table}] takes {kind}')
        result[table] = {**defaults, **own}
    if given:
        raise SystemExit(f'{path}: nothing reads {sorted(given)[0]}')
    return result
