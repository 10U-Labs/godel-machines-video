"""Build the film's soundtrack from narration, a music bed, and sound effects.

    python src/audio/mix.py

Reads out/voice/timings.json and out/voice/<scene>.wav (from make_voice.py) and
out/scenes/<scene>.sfx.json (written by capture.mjs). Every scene that has a
rendered video in out/scenes/ is included, in script order. Writes
out/audio/mix.wav and the three stems beside it.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

import synth

ROOT = Path(__file__).resolve().parents[2]
SR = synth.SR

VOICE_PEAK = 0.6        # narration peaks sit near -4 dBFS
MUSIC_LEVEL = 0.36      # music level between lines
MUSIC_DUCK = 0.65       # share of the music removed while the narrator speaks
EFFECTS_LEVEL = 0.6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", type=Path, default=ROOT / "out/voice")
    ap.add_argument("--scenes", type=Path, default=ROOT / "out/scenes")
    ap.add_argument("--out", type=Path, default=ROOT / "out/audio")
    args = ap.parse_args()

    timings = json.loads((args.voice / "timings.json").read_text(encoding="utf-8"))
    scenes = [s for s in timings["scenes"] if (args.scenes / f"{s['id']}.mp4").exists()]
    if not scenes:
        raise SystemExit(f"No rendered scenes found in {args.scenes}")
    total = sum(s["duration"] for s in scenes)
    n = int(round(total * SR))

    narration = np.zeros((n, 2))
    effects = np.zeros((n, 2))
    offset = 0.0
    for scene in scenes:
        voice, rate = sf.read(args.voice / f"{scene['id']}.wav", dtype="float64")
        if rate != SR:
            voice = resample_poly(voice, SR, rate)
        synth.place(narration, synth.pan(voice), offset)

        cues = json.loads((args.scenes / f"{scene['id']}.sfx.json").read_text(encoding="utf-8"))
        for i, cue in enumerate(cues):
            clip = synth.sfx(cue["type"], seed=i, pitch=cue.get("pitch", 1.0), dur=cue.get("dur"))
            synth.place(effects, clip * cue.get("gain", 1.0), offset + cue["t"])
        offset += scene["duration"]

    narration *= VOICE_PEAK / np.percentile(np.abs(narration), 99.95)
    effects *= EFFECTS_LEVEL

    # Lower the music while the narrator is speaking, and let it rise in the gaps.
    level = np.abs(narration).max(axis=1)
    speaking = np.clip(synth.lowpass((level > 0.02).astype(float), 1.5) * 1.4, 0, 1)
    music = synth.music(total)
    music = np.pad(music, ((0, max(0, n - len(music))), (0, 0)))[:n]  # the bed can be a sample out
    music = music * MUSIC_LEVEL * (1 - MUSIC_DUCK * speaking)[:, None]

    mix = narration + music + effects
    peak = np.abs(mix).max()
    if peak > 0.98:
        mix *= 0.98 / peak

    args.out.mkdir(parents=True, exist_ok=True)
    for name, track in (("mix", mix), ("narration", narration), ("music", music), ("effects", effects)):
        sf.write(args.out / f"{name}.wav", track, SR, subtype="PCM_16")

    def db(x):
        return 20 * np.log10(max(float(np.sqrt((x ** 2).mean())), 1e-9))

    print(f"{len(scenes)} scenes, {total:.1f}s; mix peak {min(peak, 0.98):.2f}")
    print(f"RMS in dBFS: narration {db(narration):.1f}, music {db(music):.1f}, effects {db(effects):.1f}")


if __name__ == "__main__":
    main()
