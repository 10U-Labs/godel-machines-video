"""Render one scene of a production in Blender.

    blender -b --factory-startup --python-exit-code 1 -P src/blender/render_scene.py -- \
        --production godel-machines --scene 00-pip --start 1 --end 90 [--sfx]

Each scene lives in productions/<name>/scenes/<scene id>.py and defines
build(timing), which builds the scene for the length of its narration and
returns its sound effect cues as a list of {"t": seconds, "type": ...}. The
narration timings are read from out/<name>/voice/timings.json. Frames
start..end are rendered as PNG into out/<name>/frames/<scene id>/; --sfx also
writes the cues there, as sfx.json.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import kit  # noqa: E402
import production  # noqa: E402


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--production', required=True)
    ap.add_argument('--scene', required=True)
    ap.add_argument('--start', type=int, default=1)
    ap.add_argument('--end', type=int, default=None)
    ap.add_argument('--sfx', action='store_true')
    ap.add_argument('--samples', type=int, default=24)
    ap.add_argument('--engine', choices=('cycles', 'eevee'), default='eevee')
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    return ap.parse_args(argv)


def main():
    a = args()
    out = production.out(a.production)
    frames = out / 'frames' / a.scene
    timings = json.loads((out / 'voice/timings.json').read_text(encoding='utf-8'))
    entry = next((s for s in timings['scenes'] if s['id'] == a.scene), None)
    if entry is None:
        raise SystemExit(f'No timings for scene {a.scene}')
    total = int(round(entry['duration'] * kit.FPS))
    kit.state['frames'] = total

    bpy.ops.wm.read_factory_settings(use_empty=True)
    spec = importlib.util.spec_from_file_location(
        f'scene_{a.scene}', production.folder(a.production) / 'scenes' / f'{a.scene}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cues = module.build(kit.Timing(entry)) or []

    frames.mkdir(parents=True, exist_ok=True)
    if a.sfx:
        (frames / 'sfx.json').write_text(json.dumps(sorted(cues, key=lambda c: c['t']), indent=1), encoding='utf-8')
    end = min(total, a.end or total)
    if a.start > end:
        return
    kit.configure(bpy.context.scene, frames, a.start, end, a.samples, a.engine)
    bpy.ops.render.render(animation=True)


main()
