---
name: before-an-issue-is-labelled-needs-decision
description: Before the autopilot labels an issue needs decision it checks the memories and the code to see whether the issue truly needs a person, and writes what the person has to decide into the issue's body
metadata:
  type: feedback
---

# Before an issue is labelled needs decision

Two things are done before the autopilot (`.claude/skills/autopilot/SKILL.md`) labels an issue `needs decision`. The issue is checked against the memories in `.claude/memories/` and the code, to find out whether it truly needs a person. Then what the person has to decide is written into its body.

**Why:** The label takes the issue out of the autopilot's listing until a person acts. A labelled issue also stops every issue it blocks, per [Blocked-by edges set the order](blocked-by-edges-set-the-order.md). An issue labelled where a memory or the code already answers the question stalls that work for nothing, and one labelled without the question written down leaves the person to work out what is being asked. The user holds this rule in the sibling repo `cladenc`. That it holds in this repo is Claude's reading, which the user has not confirmed.

**How to apply:** Read the memories for a rule that settles the question, and the code and the other issues for a fact that does. Only when neither does, rewrite the body so that it says what is to be decided, what the choices are, and what the work needs from the answer, with a guarded edit such as `[ -s body.md ] && gh issue edit <number> --body-file body.md`. Then add the label with `gh issue edit <number> --add-label 'needs decision'`.

Claude's interpretation of what is a person's to decide in this repo: the look, voice, music, length, and audience of a new production, per [The repo is a media factory](the-repo-is-a-media-factory.md); and anything that might cost money, per [Free tools only](free-tools-only.md).

Publishing a production is not a person's to decide. The user's statement is that everything in this repository is public, so a public GitHub release of a production needs no go-ahead. That the statement covers productions still to come is Claude's reading. How a release is tagged is settled as well, per [A release is numbered by the time](a-release-is-numbered-by-the-time.md).
