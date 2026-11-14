---
name: script-holds-only-narration
description: The script file carries the narration and no source notes; more generally, do not add sections or material to a deliverable that the user did not ask for
metadata:
  type: feedback
---

# Script holds only narration

The script holds the narration, and nothing the user did not ask for. On 2026-11-14 the user, reading script draft 4, asked why it carried source notes and pointed out that they had never requested them. Claude had added a block of notes under every scene (paper sections, exact quotations, numbers left out of the narration) so that each claim could be traced. Claude removed all of them in draft 5.

**Why:** The user's stated point was that this was not requested. Claude's interpretation: material nobody asked for gets in the way of reading the script, and the same would hold for any other deliverable.

**How to apply:** Keep `script/script.md` to its title, the short note on its format, the scene headings, the voiced lines, and the pauses. The list of joins at the top stayed in draft 5 because the user asked for that rule to be applied and has not objected to the list; remove it if they do. Claude still checks every fact against the papers before it is narrated or shown, but that checking stays out of the script and out of new files. The removed notes are in git history (`git show 693a8be:script/script.md`) if a number or quotation is needed for a scene. Before adding a section, file, or feature to any deliverable that the user did not ask for, leave it out or ask. Related: [State facts plainly](state-facts-plainly.md).
