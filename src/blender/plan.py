"""Split the film's Blender scenes into chunks of frames for parallel render jobs.

    python src/blender/plan.py out/voice/timings.json --chunk 60

Prints a JSON list of {"scene", "start", "end"} for every scene in the timings
that has a file in src/blender/scenes/, in script order.
"""
import argparse
import json
from pathlib import Path

FPS = 30
SCENES = Path(__file__).resolve().parent / 'scenes'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('timings', type=Path)
    ap.add_argument('--chunk', type=int, default=60)
    a = ap.parse_args()
    timings = json.loads(a.timings.read_text(encoding='utf-8'))
    chunks = []
    for s in timings['scenes']:
        if not (SCENES / f"{s['id']}.py").exists():
            continue
        total = int(round(s['duration'] * FPS))
        for start in range(1, total + 1, a.chunk):
            chunks.append({'scene': s['id'], 'start': start, 'end': min(total, start + a.chunk - 1)})
    if len(chunks) > 256:
        raise SystemExit(f'{len(chunks)} chunks is more than a job matrix allows; raise --chunk')
    print(json.dumps(chunks, separators=(',', ':')))


if __name__ == '__main__':
    main()
