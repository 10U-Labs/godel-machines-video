"""Where a production's material is kept, where what is made from it goes, and its settings.

A production is one piece of media the repository makes. Its material is in
productions/<name>/:

    production.toml         its title, whether its script is ready, and any
                            settings it wants to set
    script.md               the narration script
    scenes/<scene>.js       the pictures of one scene of the script
    <script>.js             what its scenes share and no other production uses,
                            such as its cast and props
    pronunciations.json     hand-written phonemes for words the voice gets wrong
    research/               source material; research/sources/ is not committed

Everything made from it goes under out/<name>/, and the finished files are
out/<name>/<name>.mp4 and out/<name>/<name>.srt.

production.toml gives the title, says whether the script is ready, and gives,
in a table for each kind, any of the settings in DEFAULTS:

    title = "Machines That Rewrite Themselves"
    ready = true

    [voice]
    speed = 0.95

A setting the file leaves out takes its value from DEFAULTS, and no tool keeps
a copy of one.

ready says whether the production's script is ready to be made into a video.
A file that leaves it out, or gives false, has a draft, and the productions
workflow renders nothing for a draft.

The music is the exception, since a default tune would be one production's
music in shared code. A production whose file has no [music] table has no
music, and one whose file has the table gives all four of its settings:

    [music]
    bpm = 80                # the tempo, in beats a minute
    chords = [              # played in turn, each for two bars; MIDI note numbers
        { bass = 38, notes = [57, 60, 64, 65, 69] },
        { bass = 34, notes = [58, 62, 65, 69] },
    ]
    arpeggio = [0, 2, 1, 3]     # one step each half beat; a step picks one of the chord's notes, counted from 0
    arpeggio_from = 6.0         # seconds from the start at which the arpeggio fades in

src/audio/synth.py says how a tune is played.

Run with a production's name, this file prints the production's title and
settings as JSON, which is how the productions workflow reads ready:

    python3 src/production.py godel-machines
"""
import json
import sys
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

MUSIC = ('bpm', 'chords', 'arpeggio', 'arpeggio_from')


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


def whole(value):
    return isinstance(value, int) and not isinstance(value, bool)


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def music(path, own):
    """Check a production's [music] table and return it."""
    def stop(what):
        raise SystemExit(f'{path}: {what}')

    if not isinstance(own, dict):
        stop('music is a table of settings, written as [music]')
    for key in own:
        if key not in MUSIC:
            stop(f'[music] has no setting named {key}')
    for key in MUSIC:
        if key not in own:
            stop(f'[music] gives no {key}, and nothing gives a tune a default')
    if not number(own['bpm']) or own['bpm'] <= 0:
        stop('bpm in [music] takes a number above 0')
    chords = own['chords']
    if not (isinstance(chords, list) and chords and all(
            isinstance(c, dict) and set(c) == {'bass', 'notes'} and whole(c['bass'])
            and isinstance(c['notes'], list) and c['notes'] and all(whole(n) for n in c['notes'])
            for c in chords)):
        stop('chords in [music] takes a list of chords, each written as { bass = 38, notes = [57, 60, 64] }')
    if not (isinstance(own['arpeggio'], list) and all(whole(n) and n >= 0 for n in own['arpeggio'])):
        stop('arpeggio in [music] takes a list of whole numbers, each 0 or more')
    if not number(own['arpeggio_from']) or own['arpeggio_from'] < 0:
        stop('arpeggio_from in [music] takes a number of seconds, 0 or more')
    return own


def settings(name):
    """A production's title and settings: what its production.toml gives, and the default for the rest.

    'ready' is whether the production's script is ready to be made into a
    video, and is False where the file does not say. The music has no default:
    'music' is the production's [music] table, or None.
    """
    path = folder(name) / 'production.toml'
    if not path.exists():
        raise SystemExit(f'{path} does not exist; it gives the production its title')
    given = tomllib.loads(path.read_text(encoding='utf-8'))
    title = given.pop('title', None)
    if not isinstance(title, str) or not title:
        raise SystemExit(f'{path} gives no title')
    ready = given.pop('ready', False)
    if not isinstance(ready, bool):
        raise SystemExit(f'{path}: ready takes true or false')
    result = {'title': title, 'ready': ready}
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
    result['music'] = music(path, given.pop('music')) if 'music' in given else None
    if given:
        raise SystemExit(f'{path}: nothing reads {sorted(given)[0]}')
    return result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Give the name of one production, a folder in productions/')
    print(json.dumps(settings(sys.argv[1]), indent=1, ensure_ascii=False))
