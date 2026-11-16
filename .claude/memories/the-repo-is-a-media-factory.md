---
name: the-repo-is-a-media-factory
description: The repo makes many productions, and the Gödel machines film is the first; nothing that belongs to one production goes into shared code, workflows, or repo-wide rules; says which memories hold for every production and which for that film
metadata:
  type: project
---

# The repo is a media factory

This repository is a factory for media: it makes many productions, not one video. The Gödel machines film is its first production.

**Why:** It is the user's statement of what the repo is, and no reason comes with it.

**How to apply:** Treat the Gödel machines film as one production among those to come. A production's material is in its own folder, `productions/<name>/`, and the film's is `productions/godel-machines/`; every tool under `src/` takes the production's name and writes under `out/<name>/`. A production's own choices of voice, picture, sound, and captions are settings in its `production.toml`, and `src/production.py` holds the default for each. Its music is the `[music]` table of that file, which has no default: a production that gives no table has no music. What only one production's scenes draw, such as the Gödel machines film's Pip, is in a Python file directly in that production's folder (`productions/godel-machines/parts.py`), and `src/blender/kit.py` holds what any production's scenes could use. Put nothing that belongs to a single production (its script, scenes, characters, names, voice, or music) into shared code under `src/`, into a workflow, or into a rule meant for the whole repository. The work that makes the repo fit for many productions is planned in the GitHub issues; read the open ones before restructuring anything.

`README.md` describes the factory for a reader who is new to it: a production's folder, every setting with its default, the script format, the kit's names, the sound effect cues, the artifacts a run keeps, the workflows' inputs, and the productions made so far. Claude's interpretation: a commit that changes one of those changes the README with it, since the README repeats what the code holds, and a new production gets a row in its list.

`MEMORY.md` lists the memories under headings: one for the factory, one for the autopilot, and one for each production that has memories of its own, such as the Gödel machines film and the Ultron film.

- The user's decision: the seven rules about writing and pictures hold for every production. They are [No analogies in script](no-analogies-in-script.md), [Plain everyday words](plain-everyday-words.md), [State facts plainly](state-facts-plainly.md), [Script holds only narration](script-holds-only-narration.md), [Show people, not panels](show-people-not-panels.md), [One idea at a time](one-idea-at-a-time.md), and [Every production tells a story](every-production-tells-a-story.md). Apply them to a new production without asking.
- Claude's sorting, which the user has not confirmed: the rules about how work is done (rendering in workflows, free tools, and the others under the factory heading) hold for all work in the repo, and [Video production decisions](video-production-decisions.md), [Only the four concepts](only-the-four-concepts.md), and [The Gödel film's subject and order](godel-film-subject-and-order.md) belong to the Gödel machines film alone.

The look, voice, music, length, and audience of a new production are not settled by the Gödel machines film's choices, so ask. The plain-words rule is written for a general viewer; if a production is for a different audience, ask how the rule reads for it.

Claude's interpretation, not confirmed: a production is a narrated, animated video like the first one; the user's word is media, so other kinds may follow.
