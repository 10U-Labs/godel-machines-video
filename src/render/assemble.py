"""Join a production's rendered scenes and its soundtrack into the finished video.

    python src/render/assemble.py godel-machines

Works under out/<name>/. Takes every scene video in scenes/ that the narration
timings list, in script order, joins them without re-encoding, and adds
audio/mix.wav, brought to the loudness in the production's [sound] settings
(see src/production.py). Writes <name>.mp4.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import production  # noqa: E402

FFMPEG = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("production")
    args = ap.parse_args()
    out = production.out(args.production)
    video = out / f"{args.production}.mp4"
    sound = production.settings(args.production)["sound"]
    loudness = f"loudnorm=I={sound['loudness']:g}:TP={sound['true_peak']:g}:LRA={sound['loudness_range']:g}"

    timings = json.loads((out / "voice/timings.json").read_text(encoding="utf-8"))
    videos = [out / "scenes" / f"{s['id']}.mp4" for s in timings["scenes"]]
    videos = [v for v in videos if v.exists()]
    if not videos:
        raise SystemExit(f"No rendered scenes found in {out / 'scenes'}")

    with tempfile.TemporaryDirectory() as tmp:
        listing = Path(tmp) / "scenes.txt"
        listing.write_text("".join(f"file '{v.resolve()}'\n" for v in videos), encoding="utf-8")
        silent = Path(tmp) / "silent.mp4"
        run(*FFMPEG, "-f", "concat", "-safe", "0", "-i", listing, "-c", "copy", silent)
        run(
            *FFMPEG, "-i", silent, "-i", out / "audio/mix.wav",
            "-c:v", "copy",
            "-af", loudness, "-ar", "48000",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart",
            video,
        )
    print(f"{len(videos)} scenes -> {video}")


if __name__ == "__main__":
    main()
