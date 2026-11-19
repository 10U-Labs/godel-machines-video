---
name: sentience-film-production-decisions
description: "The settled production choices for the sentience film (general public, no length limit, agents drawn as Pip from the Gödel machines film, voice Kokoro af_heart, look and music left to Claude); they are that film's alone, so ask for a new production"
metadata:
  node_type: memory
  type: project
  originSessionId: b47a5860-4fad-454c-8e69-bda25da8f3e0
  modified: 2026-11-19T09:45:24.468Z
---

# The sentience film's production decisions

These production choices are settled for the sentience film, whose material is in `productions/are-agents-sentient/`:

- Audience: the general public. The narration assumes no technical background and no knowledge of the incident it is about.
- Length: no limit. The content decides how long the film runs.
- The agents: each agent is drawn as Pip, the round program with a screen for a face from the Gödel machines film.
- Narration voice: Kokoro `af_heart` at speed 0.95, the narrator of the Gödel machines film. Kokoro is Apache 2.0, so the film owes no credit for the voice.
- Look: Claude's choice. The film uses the shared kit's flat shapes and its palette, as the Gödel machines film does, so that Pip looks as it does there; one agent is told from another by its body colour, and the researchers and the staff of Hugging Face are drawn as people.
- Music: Claude's choice. The film has a tune of its own in the `[music]` table of its `production.toml`.

**Why:** Each is a matter of taste that the user decides. The audience, the length, Pip, and the voice are the user's choices. The user leaves the rest of the look and the music to Claude, so Claude may change those two without asking, and the user may overrule either.

**How to apply:** Treat these as decided for the sentience film; don't ask again. Don't cut its script to reach a target length. Pip is drawn by `pip` in `productions/godel-machines/parts.js`, and a scene's page loads only its own production's scripts and the shared kit, so drawing Pip in this film means moving `pip` and its moves into `src/hyperframes/kit.js`. That move gives every clip of the Gödel machines film a new name and alters none of its pictures, so its clips are adopted and not rendered again. They are this film's choices alone, so ask about the look, voice, music, length, and audience of a new production, per [The repo is a media factory](the-repo-is-a-media-factory.md). What the film is about is in [The sentience film's subject](sentience-film-subject.md).
