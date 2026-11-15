"""Generate narration audio for every line of a production's script and record the timings.

    .venv/bin/python src/voice/make_voice.py godel-machines

Reads productions/<name>/script.md, and productions/<name>/pronunciations.json
where the production has one. Script format (markdown):

    ## 01-opening | Any title for the scene
    One paragraph is one voiced line. Keep each to a single beat so that
    pictures can be timed to it.

    [pause 0.8]

    > Visual: notes for the storyboard. Lines starting with ">" are not voiced.

Outputs, under out/<name>/voice/:
    lines/<scene>-<nn>.wav   one clip per line (24 kHz mono), cached by content
    timings.json             start and end of every line within its scene
    <scene>.wav              the scene's narration laid out on its timeline
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import production  # noqa: E402

VOICE = "af_heart"
LANG = "en-us"
SPEED = 0.95

LEAD_IN = 0.6      # silence before a scene's first line
LINE_GAP = 0.38    # silence between consecutive lines
TAIL = 0.7         # silence after a scene's last line

SCENE_RE = re.compile(r"^##\s+(\S+)\s*\|\s*(.+?)\s*$")
PAUSE_RE = re.compile(r"^\[pause\s+([0-9.]+)\]$")


def parse_script(text):
    """Return [{'id', 'title', 'items': [('line', text) | ('pause', seconds)]}]."""
    scenes = []
    current = None
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        first = block.splitlines()[0]
        heading = SCENE_RE.match(first)
        if heading:
            current = {"id": heading.group(1), "title": heading.group(2), "items": []}
            scenes.append(current)
            block = "\n".join(block.splitlines()[1:]).strip()
            if not block:
                continue
        if block.startswith("#") or block.startswith(">") or current is None:
            continue
        pause = PAUSE_RE.match(block)
        if pause:
            current["items"].append(("pause", float(pause.group(1))))
        else:
            current["items"].append(("line", " ".join(block.split())))
    return scenes


def load_pronunciations(path):
    """Each entry: {'word': 'Schmidhuber', 'phonemes': 'ʃmˈɪthuːbɚ'}."""
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def phonemize(kokoro, text, pronunciations):
    """Phonemize a line, swapping in hand-written phonemes for listed words."""
    phonemes = kokoro.tokenizer.phonemize(text, lang=LANG)
    for entry in pronunciations:
        if not re.search(rf"\b{re.escape(entry['word'])}\b", text):
            continue
        default = kokoro.tokenizer.phonemize(entry["word"], lang=LANG)
        if default not in phonemes:
            raise SystemExit(
                f"Could not apply the pronunciation for {entry['word']!r} in: {text!r}\n"
                f"  expected to find {default!r} in {phonemes!r}"
            )
        phonemes = phonemes.replace(default, entry["phonemes"])
    return phonemes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("production")
    ap.add_argument("--model", type=Path, default=ROOT / "models/kokoro/kokoro-v1.0.fp16.onnx")
    ap.add_argument("--voices", type=Path, default=ROOT / "models/kokoro/voices-v1.0.bin")
    args = ap.parse_args()

    folder = production.folder(args.production)
    out = production.out(args.production) / "voice"
    scenes = parse_script((folder / "script.md").read_text(encoding="utf-8"))
    if not scenes:
        raise SystemExit("No scenes found. Scene headings look like: ## 01-opening | Title")
    pronunciations = load_pronunciations(folder / "pronunciations.json")

    lines_dir = out / "lines"
    lines_dir.mkdir(parents=True, exist_ok=True)
    kokoro = Kokoro(str(args.model), str(args.voices))

    timings = {"voice": VOICE, "speed": SPEED, "scenes": []}
    total = 0.0
    generated = 0
    for scene in scenes:
        cursor = LEAD_IN
        placed = []          # (start_seconds, samples)
        entries = []
        sample_rate = 24000
        n = 0
        previous_was_line = False
        for kind, value in scene["items"]:
            if kind == "pause":
                cursor += value
                previous_was_line = False
                continue
            if previous_was_line:
                cursor += LINE_GAP
            n += 1
            line_id = f"{scene['id']}-{n:02d}"
            phonemes = phonemize(kokoro, value, pronunciations)
            key = hashlib.sha256(f"{VOICE}|{SPEED}|{phonemes}".encode()).hexdigest()[:16]
            wav = lines_dir / f"{line_id}.wav"
            stamp = lines_dir / f"{line_id}.key"
            if wav.exists() and stamp.exists() and stamp.read_text() == key:
                audio, sample_rate = sf.read(wav, dtype="float32")
            else:
                audio, sample_rate = kokoro.create(phonemes, voice=VOICE, speed=SPEED, is_phonemes=True)
                sf.write(wav, audio, sample_rate)
                stamp.write_text(key)
                generated += 1
            dur = len(audio) / sample_rate
            entries.append({
                "id": line_id,
                "text": value,
                "start": round(cursor, 3),
                "end": round(cursor + dur, 3),
            })
            placed.append((cursor, audio))
            cursor += dur
            previous_was_line = True

        duration = round(cursor + TAIL, 3)
        track = np.zeros(int(round(duration * sample_rate)), dtype="float32")
        for start, audio in placed:
            i = int(round(start * sample_rate))
            track[i:i + len(audio)] += audio[: len(track) - i]
        sf.write(out / f"{scene['id']}.wav", track, sample_rate)

        timings["scenes"].append({
            "id": scene["id"],
            "title": scene["title"],
            "duration": duration,
            "lines": entries,
        })
        total += duration
        print(f"{scene['id']:<24} {duration:7.2f}s  {len(entries)} lines")

    timings["duration"] = round(total, 3)
    (out / "timings.json").write_text(json.dumps(timings, indent=2, ensure_ascii=False), encoding="utf-8")
    words = sum(len(e["text"].split()) for s in timings["scenes"] for e in s["lines"])
    print(f"total {total:.1f}s ({total / 60:.1f} min), {words} words, {generated} clips generated")


if __name__ == "__main__":
    main()
