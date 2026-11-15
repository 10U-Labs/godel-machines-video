"""Read a production's opening in several candidate voices, so a narrator can be picked by ear.

    python src/voice/sample_voices.py kokoro godel-machines
    python src/voice/sample_voices.py pocket godel-machines

Writes one WAV per voice to out/<name>/voice-samples/, plus a text file that lists
each voice and its licence. Every model and voice here is free to use in a
published video; the Pocket TTS voices under a non-commercial licence are left
out. Kokoro asks for no credit. Pocket TTS's weights are CC BY 4.0, so a
production that uses one of its voices should credit Kyutai. Both models run on a plain CPU.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import production  # noqa: E402

LINES = 6           # how many voiced lines of the first scene each voice reads
PEAK = 0.7          # every sample is brought to the same peak, for a fair comparison

# (voice, language code, description). Kokoro's model and voices are Apache 2.0.
KOKORO = [
    ("am_michael", "en-us", "American man; the voice of the first renders"),
    ("am_fenrir", "en-us", "American man"),
    ("am_puck", "en-us", "American man"),
    ("am_onyx", "en-us", "American man"),
    ("af_heart", "en-us", "American woman; the voice of the Gödel machines film"),
    ("af_bella", "en-us", "American woman"),
    ("bm_george", "en-gb", "British man"),
    ("bm_fable", "en-gb", "British man"),
    ("bf_emma", "en-gb", "British woman"),
]

# (voice, licence of the recording the voice is built from). The model's code is
# MIT, but its weights are CC BY 4.0, so every voice here calls for a credit to Kyutai.
POCKET = [
    ("marius", "CC0, Unmute voice donations"),
    ("javert", "CC0, Unmute voice donations"),
    ("peter_yearsley", "CC0, Voice-Zero, a LibriVox reader"),
    ("stuart_bell", "CC0, Voice-Zero, a LibriVox reader"),
    ("bill_boerst", "CC0, Voice-Zero, a LibriVox reader"),
    ("caro_davy", "CC0, Voice-Zero, a LibriVox reader"),
    ("alba", "CC BY 4.0, voice actor Alba MacKenna; needs a credit"),
    ("george", "CC BY 4.0, VCTK dataset; needs a credit"),
]


def opening(script):
    """The first LINES voiced lines of the first scene, with the pauses between them."""
    from make_voice import parse_script

    items, lines = [], 0
    for kind, value in parse_script(script.read_text(encoding="utf-8"))[0]["items"]:
        if kind == "line":
            lines += 1
            if lines > LINES:
                break
        items.append((kind, value))
    while items and items[-1][0] == "pause":
        items.pop()
    return items


def assemble(items, speak, sample_rate, line_gap):
    """Join the spoken lines, with a short gap between lines or the script's own pause."""
    parts, previous_was_line = [], False
    for kind, value in items:
        if kind == "pause":
            parts.append(np.zeros(int(value * sample_rate), dtype="float32"))
            previous_was_line = False
            continue
        if previous_was_line:
            parts.append(np.zeros(int(line_gap * sample_rate), dtype="float32"))
        parts.append(np.asarray(speak(value), dtype="float32").reshape(-1))
        previous_was_line = True
    audio = np.concatenate(parts)
    return audio * (PEAK / max(float(np.abs(audio).max()), 1e-9))


def kokoro_samples(items, out, args, voice):
    """Every Kokoro voice at the production's speed, which Kokoro alone can set."""
    from kokoro_onnx import Kokoro

    kokoro = Kokoro(str(args.model), str(args.voices))
    notes = []
    for name, lang, who in KOKORO:
        audio = assemble(
            items, lambda text: kokoro.create(text, voice=name, speed=voice["speed"], lang=lang)[0],
            24000, voice["line_gap"])
        sf.write(out / f"kokoro-{name}.wav", audio, 24000, subtype="PCM_16")
        notes.append(f"kokoro-{name}.wav: Kokoro, {who}. Apache 2.0.")
        print(notes[-1], f"{len(audio) / 24000:.1f}s", flush=True)
    return notes


def pocket_samples(items, out, args, voice):
    import torch
    from pocket_tts import TTSModel

    model = TTSModel.load_model()
    notes = []
    for name, licence in POCKET:
        torch.manual_seed(0)  # the model samples at random; fix it so a rerun sounds the same
        try:
            state = model.get_state_for_audio_prompt(name)
        except Exception as error:  # one missing voice should not cost the others
            print(f"pocket-{name}: skipped, {type(error).__name__}: {error}", flush=True)
            continue
        audio = assemble(
            items, lambda text: model.generate_audio(state, text).detach().cpu().numpy(),
            model.sample_rate, voice["line_gap"])
        sf.write(out / f"pocket-{name}.wav", audio, model.sample_rate, subtype="PCM_16")
        notes.append(f"pocket-{name}.wav: Pocket TTS (model CC BY 4.0, credit Kyutai); recording {licence}.")
        print(notes[-1], f"{len(audio) / model.sample_rate:.1f}s", flush=True)
    if not notes:
        raise SystemExit("No Pocket TTS voice could be loaded")
    return notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("engine", choices=["kokoro", "pocket"])
    ap.add_argument("production")
    ap.add_argument("--model", type=Path, default=ROOT / "models/kokoro/kokoro-v1.0.fp16.onnx")
    ap.add_argument("--voices", type=Path, default=ROOT / "models/kokoro/voices-v1.0.bin")
    args = ap.parse_args()

    items = opening(production.folder(args.production) / "script.md")
    out = production.out(args.production) / "voice-samples"
    out.mkdir(parents=True, exist_ok=True)
    voice = production.settings(args.production)["voice"]
    notes = (kokoro_samples if args.engine == "kokoro" else pocket_samples)(items, out, args, voice)
    text = "\n\n".join(value for kind, value in items if kind == "line")
    (out / f"{args.engine}-voices.txt").write_text(
        "\n".join(notes) + "\n\nEach voice reads:\n\n" + text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
