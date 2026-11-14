"""Join the rendered scenes and the soundtrack into the film.

    python src/render/assemble.py

Takes every scene video in out/scenes/ that the narration timings list, in
script order, joins them without re-encoding, and adds out/audio/mix.wav.
Writes out/film.mp4.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FFMPEG = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", type=Path, default=ROOT / "out/voice")
    ap.add_argument("--scenes", type=Path, default=ROOT / "out/scenes")
    ap.add_argument("--mix", type=Path, default=ROOT / "out/audio/mix.wav")
    ap.add_argument("--out", type=Path, default=ROOT / "out/film.mp4")
    args = ap.parse_args()

    timings = json.loads((args.voice / "timings.json").read_text(encoding="utf-8"))
    videos = [args.scenes / f"{s['id']}.mp4" for s in timings["scenes"]]
    videos = [v for v in videos if v.exists()]
    if not videos:
        raise SystemExit(f"No rendered scenes found in {args.scenes}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        listing = Path(tmp) / "scenes.txt"
        listing.write_text("".join(f"file '{v.resolve()}'\n" for v in videos), encoding="utf-8")
        silent = Path(tmp) / "silent.mp4"
        run(*FFMPEG, "-f", "concat", "-safe", "0", "-i", listing, "-c", "copy", silent)
        run(
            *FFMPEG, "-i", silent, "-i", args.mix,
            "-c:v", "copy",
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart",
            args.out,
        )
    print(f"{len(videos)} scenes -> {args.out}")


if __name__ == "__main__":
    main()
