---
name: script-holds-only-narration
description: A production's script file carries the narration and no source notes; more generally, do not add sections or material to a deliverable that the user did not ask for
metadata:
  type: feedback
---

# Script holds only narration

A production's script holds the narration, and nothing the user did not ask for. It is the user's rule, and it holds for every production (see [The repo is a media factory](the-repo-is-a-media-factory.md)). Source notes are the case in point: a block under each scene that lists paper sections, exact quotations, and numbers left out of the narration, so that each claim can be traced, does not belong in a script.

**Why:** The user's reason is that such material was not asked for. Claude's interpretation: material nobody asked for gets in the way of reading the script, and the same holds for any other deliverable.

**How to apply:** Keep a production's script (for the Gödel machines film, `productions/godel-machines/script.md`) to its title, the short note on its format, the scene headings, the voiced lines, and the pauses. In that film's script, the list of joins at the top is there because it applies a test the user put forward (see [Every production tells a story](every-production-tells-a-story.md)), and the user has not objected to the list; remove it if they do. Claude still checks every fact against its sources before it is narrated or shown, but that checking stays out of the script and out of new files. Source notes for the Gödel machines film can be read with `git show 693a8be:script/script.md` when a scene needs a number or a quotation. Before adding a section, file, or feature to any deliverable that the user did not ask for, leave it out or ask. Related: [State facts plainly](state-facts-plainly.md).
