# The move to Hyperframes

This folder holds the factory's scenes while they move from Blender to [Hyperframes](https://github.com/heygen-com/hyperframes). Hyperframes is an open-source renderer, under the Apache 2.0 licence: a scene is a web page, and Hyperframes steps a headless Chrome to each frame and encodes the frames with FFmpeg.

A scene stays here until its Hyperframes clip has been set beside its Blender clip. When every scene of both finished films has been, the files move to the places the folders here mirror, the render workflows change over, and this folder goes.

## What is here

| Path | What it is | Where it moves to |
| --- | --- | --- |
| `src/hyperframes/kit.js` | The shared kit, written for a browser: the palette, the flat shapes, the materials, the motion, the stage, and the camera | `src/hyperframes/` |
| `src/hyperframes/page.html` | The page that the scripts draw into | `src/hyperframes/` |
| `src/hyperframes/page.py` | Puts a scene together as a page for Hyperframes, and writes the scene's sound effect cues | `src/hyperframes/` |
| `src/hyperframes/cues.js` | Builds a scene under Node, without drawing it, to collect its cues | `src/hyperframes/` |
| `productions/<name>/` | A production's own scripts and its scenes | `productions/<name>/` |
| `compare.py` | Sets a Hyperframes clip beside its Blender clip: stills side by side, and how alike the two are | Nowhere; it goes with this folder |

## How a scene is drawn

A scene is a `build(T)` function, where `T` holds the narration timings. It builds flat shapes set out in depth and keys their motion on frames, as the Blender scenes do, and it returns its sound effect cues. The kit draws the whole scene for any time it is asked for, so the same time always gives the same picture, in whatever order Hyperframes asks for the frames.

The kit draws with SVG. It works out where the camera sees each shape, writes that as the shape's transform, and blurs what is nearer or farther than the camera's focus.

The page loads no animation library. Hyperframes' own examples use GSAP, which costs nothing but is not open source, and the scenes do without it.

## How it runs

The `hyperframes-trial` workflow runs on a push that changes this folder, and by hand:

```sh
gh workflow run hyperframes-trial.yml
```

For each scene here, a job fetches the scene's Blender clip, with its narration timings and its cues, from the film's release. It builds the page, renders it with the version of Hyperframes that `package-lock.json` gives, and keeps an artifact named `compare-<production>-<scene>`, which holds the stills and a summary. The summary is also the job's summary.

Hyperframes sends usage data to its maker unless it is told not to, so the workflow sets `HYPERFRAMES_NO_TELEMETRY` and `DO_NOT_TRACK`.

## What the first scene showed

The first scene of the Gödel machines film has 661 frames of 1920 by 1080, at 30 frames a second. Hyperframes 0.9.16 rendered it on one GitHub runner with four cores and no graphics card.

| | Blender | Hyperframes |
| --- | --- | --- |
| Runner time for the render | 414 minutes, over 8 jobs | 90 to 103 seconds in each of five runs, in 1 job |
| Time for a frame | about 38 seconds | about 0.15 seconds |
| Likeness to the Blender clip | | 0.990 |

The likeness is ffmpeg's SSIM over every frame, where 1 means the same picture. Blender's time is from the run that rendered the film at full size, and it includes each job's setup.

The kit copies three things that Blender does, so that the films keep their look:

- Blender runs a shape's gradient across a box one unit larger on every side than the shape. So the films' glows end in a hard edge.
- Blender mixes a see-through colour with what is behind it as light. A browser mixes the two colours' sRGB numbers, which leaves a light colour over a dark one much darker.
- Blender scales a font by the box around all its glyphs, and draws a font of many weights at the file's default weight.

What still differs:

- A browser cannot mix see-through colours as light. The kit works each one out over the colour it mostly lies over, which is right there and a little off elsewhere.
- Blender draws a see-through shape as scattered dots, which shows as grain. The page's see-through shapes are smooth.
- The page blurs what is out of focus with a Gaussian blur, where Blender spreads each point into a disc.
