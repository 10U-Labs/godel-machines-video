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

**How to apply:** Treat these as decided for the sentience film; don't ask again. Don't cut its script to reach a target length. Pip is drawn by `pip` in `src/hyperframes/kit.js`, with its moves beside it, so this film's scenes call the kit for it and give each agent a body colour. Claude's interpretation, not confirmed: the society film is about the same incident, and its `productions/did-agents-form-a-society/parts.js` already draws the incident's things, such as the board, a folder with a name, the scorer, the secret word, and a company's building; what this film draws as well moves from there into the kit before this film's scenes are written, as Pip did, and the society film's clips are then adopted, per [Every run is watched](every-run-is-watched.md). They are this film's choices alone, so ask about the look, voice, music, length, and audience of a new production, per [The repo is a media factory](the-repo-is-a-media-factory.md). What the film is about is in [The sentience film's subject](sentience-film-subject.md).
