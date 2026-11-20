"""Plan which of a production's scenes a workflow run renders.

    python src/hyperframes/plan.py godel-machines [--adopt 43653948688] >> "$GITHUB_OUTPUT"

Takes every scene in out/<name>/voice/timings.json that has a file in
productions/<name>/scenes/, in script order. A scene whose clip is still kept
as an artifact (see clips.py) needs nothing. The others are rendered, each in
a job of its own.

--adopt names an earlier workflow run by its id. A scene that has no clip
under its name takes the run's clip of the scene, with the narration it was
rendered for, which is uploaded again under the scene's name and not
rendered. That is for clips rendered before a change that gives them new
names and is known to alter no picture. GitHub deletes a run's artifacts
after 90 days, and a release keeps no clips, so a clip older than that is
rendered again. A scene is taken whatever changed in it since, so adopt
before changing a picture, not after.

Writes {scene: clip name} for every scene to out/<name>/clips.json, and
prints two lines:

    render=[{"scene", "clip"}, ...]
    adopt=[{"scene", "clip", "source", "artifact", "narration"}, ...]

render lists the scenes to render, each with the name to keep its clip under.
In adopt, source and artifact say where the clip to take is kept: which
artifact of which run. narration is the run whose narration goes with a clip
that was kept without its own.
"""
import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import clips  # noqa: E402
import production  # noqa: E402

MATRIX = 256        # the most jobs one job matrix allows


def offered(run, scenes, name):
    """Where an earlier run keeps its clip of each of these scenes: {scene: (run, artifact)}.

    A run lists the clip it used for each scene of the production in its
    artifact '<name>-clips', and the clip itself may sit in a run before it. A
    run from before artifacts carried the production's name calls the list
    'clips', and one from before clips had names keeps them all in one
    artifact, 'scenes'.
    """
    held = clips.gh(
        'api', '--paginate', f'repos/{{owner}}/{{repo}}/actions/runs/{run}/artifacts?per_page=100',
        '--jq', '.artifacts[] | select(.expired | not) | .name',
    ).split()
    listing = next((kept for kept in (f'{name}-clips', 'clips') if kept in held), None)
    if listing:
        with tempfile.TemporaryDirectory() as tmp:
            clips.download(run, listing, Path(tmp))
            used = json.loads((Path(tmp) / 'clips.json').read_text(encoding='utf-8'))
        found = {scene: (clips.find(used[scene]), used[scene]) for scene in scenes if scene in used}
        return {scene: where for scene, where in found.items() if where[0] is not None}
    if 'scenes' in held:
        return {scene: (run, 'scenes') for scene in scenes}
    raise SystemExit(f'Run {run} keeps no scene clips to adopt')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('production')
    ap.add_argument('--adopt', default='')
    a = ap.parse_args()
    if a.adopt and not a.adopt.isdigit():
        raise SystemExit(f'--adopt takes the id of a workflow run, not {a.adopt!r}')

    out = production.out(a.production)
    picture = production.settings(a.production)['picture']
    timings = json.loads((out / 'voice/timings.json').read_text(encoding='utf-8'))
    names = clips.names(production.folder(a.production) / 'scenes', timings, picture)
    (out / 'clips.json').write_text(json.dumps(names, indent=1), encoding='utf-8')

    missing = [scene for scene, clip in names.items() if clips.find(clip) is None]
    offer = {}
    if a.adopt and missing:
        offer = offered(a.adopt, missing, a.production)
    render, adopt = [], []
    for s in timings['scenes']:
        scene = s['id']
        if scene not in names:
            continue
        if scene not in missing:
            print(f'{scene:<28} reused', file=sys.stderr)
        elif scene in offer:
            source, artifact = offer[scene]
            adopt.append({
                'scene': scene, 'clip': names[scene], 'source': source, 'artifact': artifact,
                'narration': a.adopt,
            })
            print(f'{scene:<28} adopted from {artifact} of {source}', file=sys.stderr)
        else:
            render.append({'scene': scene, 'clip': names[scene]})
            print(f'{scene:<28} rendered', file=sys.stderr)
    if max(len(render), len(adopt)) > MATRIX:
        raise SystemExit('More scenes than a job matrix allows')
    for output, value in (('render', render), ('adopt', adopt)):
        print(f"{output}={json.dumps(value, separators=(',', ':'))}")


if __name__ == '__main__':
    main()
