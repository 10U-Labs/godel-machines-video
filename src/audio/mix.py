"""Build a production's soundtrack from narration, sound effects, and its music, if it sets any.

    python src/audio/mix.py godel-machines

Works under out/<name>/. Reads voice/timings.json and voice/<scene>.wav (from
make_voice.py) and scenes/<scene>.sfx.json (written by
src/hyperframes/page.py). Every scene that has a rendered video in scenes/
is included, in script order. Writes audio/mix.wav and the three stems beside
it. The levels are the production's [sound] settings and the tune is its
[music] settings (see src/production.py). A production that sets no music has
a silent music stem.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

import synth

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import production  # noqa: E402

SR = synth.SR


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("production")
    args = ap.parse_args()
    out = production.out(args.production)
    voice_dir, scenes_dir, audio_dir = out / "voice", out / "scenes", out / "audio"
    settings = production.settings(args.production)
    sound, tune = settings["sound"], settings["music"]

    timings = json.loads((voice_dir / "timings.json").read_text(encoding="utf-8"))
    scenes = [s for s in timings["scenes"] if (scenes_dir / f"{s['id']}.mp4").exists()]
    if not scenes:
        raise SystemExit(f"No rendered scenes found in {scenes_dir}")
    total = sum(s["duration"] for s in scenes)
    n = int(round(total * SR))

    narration = np.zeros((n, 2))
    effects = np.zeros((n, 2))
    offset = 0.0
    for scene in scenes:
        voice, rate = sf.read(voice_dir / f"{scene['id']}.wav", dtype="float64")
        if rate != SR:
            voice = resample_poly(voice, SR, rate)
        synth.place(narration, synth.pan(voice), offset)

        cues = json.loads((scenes_dir / f"{scene['id']}.sfx.json").read_text(encoding="utf-8"))
        for i, cue in enumerate(cues):
            clip = synth.sfx(cue["type"], seed=i, pitch=cue.get("pitch", 1.0), dur=cue.get("dur"))
            synth.place(effects, clip * cue.get("gain", 1.0), offset + cue["t"])
        offset += scene["duration"]

    narration *= sound["voice_peak"] / np.percentile(np.abs(narration), 99.95)
    effects *= sound["effects_level"]

    # Lower the music while the narrator is speaking, and let it rise in the gaps.
    level = np.abs(narration).max(axis=1)
    speaking = np.clip(synth.lowpass((level > 0.02).astype(float), 1.5) * 1.4, 0, 1)
    music = synth.music(total, **tune) if tune else np.zeros((n, 2))
    music = np.pad(music, ((0, max(0, n - len(music))), (0, 0)))[:n]  # the bed can be a sample out
    music = music * sound["music_level"] * (1 - sound["music_duck"] * speaking)[:, None]

    mix = narration + music + effects
    peak = np.abs(mix).max()
    if peak > 0.98:
        mix *= 0.98 / peak

    audio_dir.mkdir(parents=True, exist_ok=True)
    for name, track in (("mix", mix), ("narration", narration), ("music", music), ("effects", effects)):
        sf.write(audio_dir / f"{name}.wav", track, SR, subtype="PCM_16")

    def db(x):
        return 20 * np.log10(max(float(np.sqrt((x ** 2).mean())), 1e-9))

    print(f"{len(scenes)} scenes, {total:.1f}s; mix peak {min(peak, 0.98):.2f}")
    print(f"RMS in dBFS: narration {db(narration):.1f}, music {db(music):.1f}, effects {db(effects):.1f}")


if __name__ == "__main__":
    main()
