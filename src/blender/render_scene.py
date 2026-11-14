"""Render one scene of the film in Blender.

    blender -b --factory-startup --python-exit-code 1 -P src/blender/render_scene.py -- \
        --scene 00-pip --timings out/voice/timings.json --out out/frames/00-pip \
        --start 1 --end 90 [--sfx out/frames/00-pip/sfx.json]

Each scene lives in src/blender/scenes/<scene id>.py and defines build(timing),
which builds the scene for the length of its narration and returns its sound
effect cues as a list of {"t": seconds, "type": ...}. Frames start..end are
rendered as PNG; --sfx also writes the cues.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kit  # noqa: E402


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scene', required=True)
    ap.add_argument('--timings', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--start', type=int, default=1)
    ap.add_argument('--end', type=int, default=None)
    ap.add_argument('--sfx', type=Path, default=None)
    ap.add_argument('--samples', type=int, default=16)
    ap.add_argument('--engine', choices=('cycles', 'eevee'), default='cycles')
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    return ap.parse_args(argv)


def main():
    a = args()
    timings = json.loads(a.timings.read_text(encoding='utf-8'))
    entry = next((s for s in timings['scenes'] if s['id'] == a.scene), None)
    if entry is None:
        raise SystemExit(f'No timings for scene {a.scene}')
    total = int(round(entry['duration'] * kit.FPS))
    kit.state['frames'] = total

    bpy.ops.wm.read_factory_settings(use_empty=True)
    spec = importlib.util.spec_from_file_location(f'scene_{a.scene}', HERE / 'scenes' / f'{a.scene}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cues = module.build(kit.Timing(entry)) or []

    a.out.mkdir(parents=True, exist_ok=True)
    if a.sfx:
        a.sfx.parent.mkdir(parents=True, exist_ok=True)
        a.sfx.write_text(json.dumps(sorted(cues, key=lambda c: c['t']), indent=1), encoding='utf-8')
    end = min(total, a.end or total)
    if a.start > end:
        return
    kit.configure(bpy.context.scene, a.out, a.start, end, a.samples, a.engine)
    bpy.ops.render.render(animation=True)


main()
