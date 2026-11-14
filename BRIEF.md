# Gödel Machines video: handoff brief

Written 2026-11-14 at the end of a planning chat in the Claude app, for the
Claude Code session that will produce the video. Nothing has been built yet.

## Goal
A video that explains recursive self-improvement (RSI) and how three machines
relate to it: the Gödel Machine, the Darwin Gödel Machine, and the
Huxley-Gödel Machine.

## Decided by the user
- Target feel: an animated explainer in the style of Kurzgesagt videos.
- Production happens in Claude Code, locally on the Mac, so native tools and
  the full machine are available for rendering.

## Still open (ask, don't assume)
- Narration voice: one of the free Kokoro voices below, the user's own
  recording, or a paid service such as ElevenLabs (needs an API key).
- Music: a licensed track the user supplies, or a simple synthesized bed
  with basic sound effects.
- Length and audience level.

## Suggestions from the planning chat (not yet agreed)
- Design an original flat-vector look in that genre. Do not copy
  Kurzgesagt's characters, logo or branding.
- Draw scenes in code (SVG/HTML), film them frame by frame in headless
  Chrome, encode with ffmpeg. A code animation framework would also work.
- Order of work: research, script, storyboard, voice, scenes timed to the
  voice, music and effects, final assembly.
- Rendering: 1920x1080 at 30 fps. Check a few full-size stills at the
  busiest moments before any full render. Encode one file per scene with
  identical settings, join them with ffmpeg's concat demuxer and `-c copy`,
  then add the audio with `-c:v copy`.

## Voice test that worked (Linux, 2 CPU cores)
- `pip install kokoro-onnx soundfile`
- Model files, from
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/
  - `kokoro-v1.0.fp16.onnx` (177 MB)
  - `voices-v1.0.bin` (28 MB)
- Usage:
  ```python
  from kokoro_onnx import Kokoro
  import soundfile as sf
  k = Kokoro("kokoro-v1.0.fp16.onnx", "voices-v1.0.bin")
  audio, sr = k.create(text, voice="bm_george", speed=0.95, lang="en-gb")
  sf.write("line.wav", audio, sr)   # 24 kHz mono
  ```
- Voices sampled for the user: `bm_george` (British male, `en-gb`),
  `af_heart` (American female, `en-us`), `am_michael` (American male,
  `en-us`). The user has not picked one yet.
- The three samples are in `Claude outputs/` in this folder
  (`voice-sample-british-male.mp3`, `voice-sample-american-female.mp3`,
  `voice-sample-american-male.mp3`).
- About 15 s of speech took about 9 s to generate.
- Levelled afterwards with `ffmpeg -af loudnorm=I=-16:TP=-1.5`.
- Checked for level and pace only; nobody has confirmed pronunciation by ear.
- Placeholder line used for the samples (not an approved script line):
  "What if a machine could rewrite its own code, and every rewrite made it
  better at rewriting itself? That idea has a name: recursive
  self-improvement. And over the last twenty years, three machines have
  tried to make it real."

## Source papers (listed from memory; verify before scripting)
- Gödel Machine: Jürgen Schmidhuber, 2003.
- Darwin Gödel Machine: Zhang, Hu, Lu, Lange, Clune, 2025.
- Huxley-Gödel Machine: Schmidhuber's group at KAUST, 2025.

## Prerequisites on the Mac
- ffmpeg, Node, Python 3 and Chrome. Everything else can be installed per
  project.
