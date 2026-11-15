# Media factory

This repository makes narrated, animated videos. Each one is made from a script and from scene code, and comes out with a voice, pictures, music, sound effects, and closed captions. GitHub Actions renders it, and every tool it uses is free.

Each video is called a production. The ones made so far are listed under [Productions](#productions).

## How a production is made

A production goes through five steps. Each is a tool under `src/`:

1. `src/voice/make_voice.py` reads the script aloud, one audio clip for each line, and records when each line starts and ends. The voice is [Kokoro](https://github.com/thewh1teagle/kokoro-onnx), an open-source voice model that runs on a plain CPU.
2. `src/blender/render_scene.py` renders each scene in [Blender](https://www.blender.org/). A scene's pictures are timed to the lines of its narration, and its frames are encoded into a clip.
3. `src/audio/mix.py` builds the soundtrack from the narration, the production's music, and the sound effects its scenes ask for. `src/audio/synth.py` makes the music and the effects from numbers, so no recording or sample is used.
4. `src/render/assemble.py` joins the clips and the soundtrack into the finished video, which the code calls the film.
5. `src/render/captions.py` writes the closed captions from the script's lines and their timings.

The workflows in `.github/workflows/` run these steps. Nothing is rendered on a developer's machine.

## A production's folder

A production's material is in a folder of its own, `productions/<name>/`. The name is used for the folder, for the finished files, and in the commands below.

| File | What it holds |
| --- | --- |
| `production.toml` | The title, and any settings the production sets |
| `script.md` | The narration script |
| `scenes/<scene id>.py` | One Blender scene for each scene of the script |
| `<module>.py` | What the production's scenes share and no other production uses, such as its cast and props; optional |
| `pronunciations.json` | Hand-written phonemes for words the voice gets wrong; optional |
| `research/` | Source material; optional, and `research/sources/` is not committed |

Everything made from the folder goes under `out/<name>/`, which is not committed. The finished files are `out/<name>/<name>.mp4` and `out/<name>/<name>.srt`.

Shared code under `src/` holds nothing that belongs to one production.

### Settings

`production.toml` gives the production's title and, in a table for each kind, any setting the production wants to change:

```toml
title = "Machines That Rewrite Themselves"

[voice]
speed = 0.95
```

A setting the file leaves out takes its default, which `src/production.py` holds. A setting that nothing reads is an error.

`[voice]` sets the narrator:

| Setting | Default | Meaning |
| --- | --- | --- |
| `name` | `"af_heart"` | The Kokoro voice |
| `lang` | `"en-us"` | The language the lines are read in |
| `speed` | `0.95` | How fast the voice speaks |
| `lead_in` | `0.6` | Seconds of silence before a scene's first line |
| `line_gap` | `0.38` | Seconds of silence between two lines |
| `tail` | `0.7` | Seconds of silence after a scene's last line |

The `voices` workflow reads the opening of a production's script in several candidate voices, so that a narrator can be picked by ear. Start it with `gh workflow run voices.yml -f production=<name>`.

`[picture]` sets the frame and how Blender renders it:

| Setting | Default | Meaning |
| --- | --- | --- |
| `width` | `1920` | The frame's width in pixels |
| `height` | `1080` | The frame's height in pixels; the shared scene kit lays scenes out for a 16:9 frame |
| `fps` | `30` | Frames a second |
| `engine` | `"eevee"` | Blender's render engine, `"eevee"` or `"cycles"` |
| `samples` | `24` | Render samples for each frame |

`[sound]` sets the levels of the soundtrack:

| Setting | Default | Meaning |
| --- | --- | --- |
| `voice_peak` | `0.6` | The narration's peak level, where 1 is full scale |
| `music_level` | `0.36` | The music's level between lines |
| `music_duck` | `0.65` | The share of the music taken away while the narrator speaks |
| `effects_level` | `0.6` | The level of the sound effects |
| `loudness` | `-14.0` | The loudness the finished soundtrack is brought to, in LUFS |
| `true_peak` | `-1.5` | The highest peak it may reach, in dBTP |
| `loudness_range` | `11.0` | Its loudness range, in LU |

`[captions]` sets how the closed captions are broken up:

| Setting | Default | Meaning |
| --- | --- | --- |
| `row` | `42` | The most characters on one caption row |
| `gap` | `0.05` | Seconds of blank between two captions made from one line |

`[music]` is the production's tune, and has no default. A production whose file has no `[music]` table has no music, and one whose file has the table gives all four of its settings:

```toml
[music]
bpm = 80                # the tempo, in beats a minute
chords = [              # played in turn, each for two bars; MIDI note numbers
    { bass = 38, notes = [57, 60, 64, 65, 69] },
    { bass = 34, notes = [58, 62, 65, 69] },
]
arpeggio = [0, 2, 1, 3]     # one step each half beat; a step picks one of the chord's notes, counted from 0
arpeggio_from = 6.0         # seconds from the start at which the arpeggio fades in
```

## The script

`script.md` is a Markdown file that holds every line the narrator speaks:

```markdown
# Any title

Text before the first scene heading is not voiced.

## 01-opening | A title for the scene

One paragraph is one voiced line. Keep each line to one beat, so that pictures can be timed to it.

A second paragraph is a second line.

[pause 0.8]

> A paragraph that starts with ">" is a note, and is not voiced.
```

- A scene starts at a heading of the form `## <scene id> | <title>`. The id has no spaces, and it names the scene's file, `scenes/<scene id>.py`. Scenes play in the order the script gives them.
- Each paragraph under the heading is one voiced line. A paragraph may run over several lines of the file.
- `[pause 0.8]`, as a paragraph of its own, puts 0.8 seconds of silence between two lines, in place of the usual gap.
- A paragraph that starts with `>` or `#` is not voiced, and neither is anything before the first scene heading.

The captions show each line as the script writes it.

`pronunciations.json` lists the words the voice gets wrong, each with the phonemes to speak in its place:

```json
[
  { "word": "Schmidhuber", "phonemes": "ʃmˈɪthuːbɚ" }
]
```

## A scene

A scene's file, `productions/<name>/scenes/<scene id>.py`, defines one function, `build(T)`. It builds the whole scene in Blender, for the length of the scene's narration, and returns the scene's sound effect cues.

```python
import kit


def build(T):
    kit.backdrop()
    stage = kit.layer('stage', 1.0)

    disc = kit.shape('disc', kit.circle_pts(1.2), kit.material(kit.MINT, kit.MINT_DEEP), stage, (0, 0.5))
    kit.pop(disc, T.start(0))

    label = kit.text('label', 'A program is text', 0.5, kit.material(kit.PAPER), stage, (0, -1.8))
    kit.appear(label, T.start(1))

    kit.camera(lambda t: (0, 0, kit.H0 - 0.5 * t / T.duration))
    return [{'t': T.start(0), 'type': 'pop'}]
```

`T` holds the scene's narration timings, in seconds from the start of the scene:

| Name | What it gives |
| --- | --- |
| `T.duration` | The scene's length |
| `T.start(i)` | When line `i` starts; lines count from 0 |
| `T.end(i)` | When line `i` ends |
| `T.at(i, share)` | A moment part way through line `i`, where a share of 0 is its start and 1 is its end |

### The kit

`src/blender/kit.py` is the shared kit that every scene imports. A scene is built from flat shapes set out in depth, so a moving camera gives parallax, and what is near or far goes soft. Every surface gives off its own colour, so a colour comes out as it is written and a scene needs no lights.

Positions and sizes are in screen units at depth 0: the frame runs from -8 to 8 across and from -4.5 to 4.5 up.

| Kind | Names in `kit` |
| --- | --- |
| Colours | The palette, such as `INK900`, `MINT`, `AMBER`, `CORAL`, `VIOLET`, `SKY`, and `PAPER`; `material` for a flat colour or a gradient; `glow_material` |
| Depth | `layer` for a sheet at one depth; `empty` for a point that other shapes hang from |
| Shapes | `shape`, which fills a list of points; the points come from `circle_pts`, `rrect_pts`, `bar_pts`, `capsule_pts`, `arc_pts`, and `star_pts` |
| Text | `text`, in the fonts `Figtree` and `JetBrainsMono` |
| Time | `fr` turns seconds into a frame, and `sec` a frame into seconds; `every` lists frames; `span`, `mix`, `smooth`, `ease_out`, and `back_out` shape a movement |
| Motion | `key` sets a value at a frame; `alpha`, `track`, `fade`, `appear`, `pop`, `grow`, and `flash` are built on it |
| The stage | `backdrop`, `motes`, `camera`, and `veil` |
| Props | `person`, `branch`, `tag`, `ring`, and `screen_stand` |

The docstring of each says what it takes.

What only one production's scenes draw goes in a Python file directly in the production's folder, such as `productions/godel-machines/parts.py`. A scene imports it by its name, as in `import parts`. Where the production and the shared code both have a module of one name, the shared one is imported.

### Sound effect cues

`build` returns a list of cues, and each cue places one sound effect in the scene:

```python
{'t': 2.4, 'type': 'tick', 'pitch': 1.1, 'gain': 0.4}
```

| Key | Meaning |
| --- | --- |
| `t` | When the effect starts, in seconds from the start of the scene |
| `type` | The effect: `pop`, `tick`, `blip`, `rise`, `whoosh`, `swoosh`, or `chime` |
| `pitch` | Scales the effect's frequency; optional, 1 as it stands |
| `gain` | Scales its level; optional, 1 as it stands |
| `dur` | Its length in seconds, for `rise`, `whoosh`, `swoosh`, and `chime`; optional |

## Rendering

### Render a production

A push to `main` that changes anything in `productions/<name>/` renders that production. A push that changes only shared code renders nothing by itself. To render after such a push, or at any other time, start the workflow by hand:

```sh
gh workflow run productions.yml -f production=<name>
```

A run keeps what it makes as artifacts, which GitHub deletes after 90 days:

| Artifact | What it holds |
| --- | --- |
| `<name>-film` | The film, `<name>.mp4`, and its captions, `<name>.srt` |
| `scene-<name>-<scene id>-<hash>` | One scene's clip, with its sound effect cues and the narration it was rendered for |
| `<name>-stills-<scene id>` | One frame in every 60 of a scene the run rendered, for a quick look |
| `<name>-narration` | The narration tracks and their timings |
| `<name>-clips` | The name of each scene's clip |
| `<name>-frames-<scene id>-<first frame>` | The frames of a scene the run rendered, kept for three days |

Fetch the film of a run with its id:

```sh
gh run list --workflow productions.yml
gh run download <run id> --name <name>-film
```

### Correct a production

Rendering the pictures is the slow part. The first production has nine scenes and about 6,800 frames, and rendering all of it takes about four hours. So a run renders a scene only when it has to.

Each scene's clip is kept under a name that ends in a hash of everything that decides the clip's pictures:

- the scene's file;
- the Python files directly in the production's folder;
- `src/blender/kit.py` and `src/blender/render_scene.py`;
- the fonts in `src/fonts/`;
- the production's `[picture]` settings;
- what the scene's narration says: its lines as they are spoken, its pauses, and the `[voice]` settings;
- the Blender version, and how the frames are encoded into the clip.

A run renders a scene only when no artifact is left under its clip's name, so a correction costs what it reaches:

| Correction | Rendered again |
| --- | --- |
| How the captions are broken up or timed | Nothing |
| A spelling fix in the script that leaves the spoken line the same | Nothing |
| The music, how an effect sounds, or the `[sound]` levels | Nothing; the soundtrack is mixed again and joined to the same clips |
| The pictures or the cues of one scene | That scene |
| The narration of one scene | That scene, because its pictures follow its narration |
| A module of the production, the kit, the fonts, the `[picture]` or `[voice]` settings, or the Blender version | Every scene |

Some changes give clips new names and alter no picture, such as moving a function from one file of a production to another. A run then takes the clips of an earlier run in place of rendering them, when it is given that run's id to adopt:

```sh
gh workflow run productions.yml -f production=<name> -f adopt=<run id>
```

Every scene that has no clip under its new name takes the earlier run's clip of the scene. Nothing checks that the pictures are the same: a scene's clip is taken whatever has changed in the scene since. So adopt before a change that alters a picture, never after.

### Keep a production

To keep a production longer than 90 days, publish it as a GitHub release:

```sh
gh workflow run productions.yml -f production=<name> -f release=true
```

The run ends by making a release tagged `<name>-v<time>`, where the time is the moment the release is made, in UTC, as fourteen digits: `godel-machines-v20261115172101`. The release holds the film, its captions, and, for each scene, an archive named `<clip name>.zip` that holds what the scene's artifact holds. The repository is public, so anyone can see a release. No push makes one.

Fetch a released film and its captions with the tag:

```sh
gh release download <tag> --pattern '<name>.*'
```

Once the artifacts are gone, a run takes the scene clips back from a release in place of rendering them, when it is given the tag to adopt:

```sh
gh workflow run productions.yml -f production=<name> -f adopt=<tag>
```

## Productions

| Name | Title | What it is |
| --- | --- | --- |
| `godel-machines` | Machines That Rewrite Themselves | A film of nearly four minutes on recursive self-improvement and three machines built on it: the Gödel Machine, the Darwin Gödel Machine, and the Huxley-Gödel Machine |

Each production's film is in its [releases](https://github.com/10U-Labs/media-factory/releases).
