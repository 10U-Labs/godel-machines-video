---
name: video-production-decisions
description: The settled production choices for the Gödel Machines video (look, voice, music, length, audience)
metadata:
  type: project
---

# Video production decisions

The user settled these production choices for the Gödel machines film (2026-11-14):

- Look: an animated explainer with the feel of Kurzgesagt videos. The look itself is original flat-vector artwork drawn in code; nothing of Kurzgesagt's (characters, logo, branding) is copied. The feel was the user's decision in the planning chat that preceded this repo; the original look was proposed there and has been followed since.
- Narration voice: Kokoro `af_heart` (American woman, `en-us`, speed 0.95), set in `src/voice/make_voice.py`. The user chose it by ear on 2026-11-14 from seventeen free samples reading the film's opening. Before that, `am_michael` was judged off after the first render, and a Pocket TTS voice (`alba`) was picked and then dropped once the user learned it needs credits. Kokoro is Apache 2.0, so the film owes no credit for the voice.
- Music: a synthesized bed with basic sound effects that Claude generates; no licensed track.
- Length: no limit. The content decides how long the video runs.
- Audience: the general public, with the constraint in [No analogies in script](no-analogies-in-script.md).

**Why:** These were open questions in the handoff brief from the planning chat (`BRIEF.md`, which the user had Claude delete on 2026-11-14 once everything in it was settled or out of date).

**How to apply:** Treat these as decided for the Gödel machines film; don't ask again. Don't cut its script to reach a target length. They were settled when the repo made nothing else, so ask about the look, voice, music, length, and audience of a new production (see [The repo is a media factory](the-repo-is-a-media-factory.md)).
