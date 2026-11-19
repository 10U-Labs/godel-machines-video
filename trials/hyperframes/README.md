# The Hyperframes trial

This folder tries [Hyperframes](https://github.com/heygen-com/hyperframes) as the tool that renders a scene's pictures, in place of Blender. Hyperframes is an open-source renderer, under the Apache 2.0 licence: a scene is a web page, and Hyperframes steps a headless Chrome to each frame and encodes the frames with FFmpeg.

The trial renders one scene that the factory has already made, the first scene of the Gödel machines film, and sets the result beside the scene's Blender clip. It asks two things: whether the look carries over, and how long the render takes.

Nothing else in the factory uses this folder. The voice, the music, the sound effects, the captions, and the film's assembly are untouched.

## What is here

| File | What it is |
| --- | --- |
| `kit.js` | The part of `src/blender/kit.py` that the scene needs, written for a browser: the palette, the flat shapes, the materials, the motion, the stage, and the camera |
| `godel-machines/parts.js` | Pip and the page of code, from `productions/godel-machines/parts.py` |
| `godel-machines/scenes/00-pip.js` | The scene, from `productions/godel-machines/scenes/00-pip.py` |
| `page.html` | The page that the scripts draw into |
| `build.py` | Puts a scene together as a page for Hyperframes, with the scene's length and narration timings written in |
| `compare.py` | Sets the Hyperframes clip beside the Blender clip: stills, a side-by-side video, and a summary |

## How a scene is drawn

A scene is still a `build(T)` function, where `T` holds the narration timings, and it still builds flat shapes set out in depth. The difference is in how motion is given. In Blender a scene keys values on frames. Here each moving value is a function of the time, or a `Track` keyed on a few frames, and the kit draws the whole scene for any time it is asked for. Hyperframes asks for one frame at a time, in any order, so the same time always gives the same picture.

The kit draws with SVG. It works out where the camera sees each shape, writes that as the shape's transform, and blurs what is nearer or farther than the camera's focus.

The page loads no animation library. Hyperframes' own examples use GSAP, which costs nothing but is not open source, and the trial does without it.

## How it runs

The `hyperframes-trial` workflow runs on a push that changes this folder, and by hand:

```sh
gh workflow run hyperframes-trial.yml
```

It fetches the scene's Blender clip, with its narration and timings, from the film's release. It builds the page, renders it with a pinned version of Hyperframes, and keeps two artifacts:

| Artifact | What it holds |
| --- | --- |
| `hyperframes-trial-clip` | The scene as Hyperframes rendered it |
| `hyperframes-trial-compare` | Stills of both clips side by side with Blender on the left, a side-by-side video with the narration, and the summary |

The run's summary gives the time the render took beside Blender's time for the same scene.

Hyperframes sends usage data to its maker unless it is told not to, so the workflow sets `HYPERFRAMES_NO_TELEMETRY` and `DO_NOT_TRACK`.
