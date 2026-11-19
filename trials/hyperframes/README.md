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

## What the trial found

The scene has 661 frames of 1920 by 1080, at 30 frames a second. Hyperframes 0.9.16 rendered it on one GitHub runner with four cores and no graphics card.

| | Blender | Hyperframes |
| --- | --- | --- |
| Runner time for the render | 414 minutes, over 8 jobs | 97 to 103 seconds in each of four runs, in 1 job |
| Time for a frame | about 38 seconds | about 0.15 seconds |
| Likeness to the Blender clip | | 0.990 |

The likeness is ffmpeg's SSIM over every frame, where 1 means the same picture. Blender's time is from the run that rendered the film at full size, and it includes each job's setup.

### The look

Every shape is where Blender puts it: Pip, the page of code with the same lines, the crowd, the spark, and the specks. Colours measured at matching points differ by a few steps out of 255.

The first render did not look like the Blender clip. It took three more to bring the two together, and each had to copy something that Blender does and that the Blender kit's code does not say:

- Blender runs a shape's gradient across a box one unit larger on every side than the shape. So the film's glows end in a hard edge, and do not fade to nothing as `glow_material` in `src/blender/kit.py` describes them.
- Blender mixes a see-through colour with what is behind it as light. A browser mixes the two colours' sRGB numbers, which leaves a light colour over a dark one much darker.
- Blender scales a font by the box around all its glyphs, and draws a font of many weights at the file's default weight. For Figtree that is seven eighths of a browser's size, and the light weight.

What still differs:

- A browser cannot mix see-through colours as light. The kit works each one out over the colour it mostly lies over, which is right there and a little off elsewhere: a speck that drifts across Pip's eye is brighter than in Blender.
- Blender draws a see-through shape as scattered dots, which shows as grain on the shine of Pip's body. The page's shine is smooth.
- The page blurs what is out of focus with a Gaussian blur, where Blender spreads each point into a disc. Out-of-focus specks are a little softer at the edge.

### The work

The scene took about 1,070 lines of JavaScript: 700 for the kit, 190 for Pip and the page of code, and 180 for the scene. The kit holds only what this scene uses. It has no people, score tags, or branches, which other scenes of the film need.

The scene uses none of what Hyperframes offers for writing a video: no timeline, no animation library, and no ready-made blocks. It uses the renderer alone, through the event that Hyperframes sends for each frame. Hyperframes' lint gives the page one warning, that a timed element holds another element, and the render goes ahead.

### What it does not show

The trial rendered one scene. A scene with more shapes, or more of them blurred, takes longer, and nothing here measures by how much. It also leaves open how a page's clip would be named and kept from run to run, as `src/blender/clips.py` does for a Blender clip.
