---
name: the-work-in-hand-can-be-several-issues
description: The work the autopilot takes is the lowest-numbered listed issue that no open issue blocks, alone or with other listed issues it chooses; a blocked issue joins only when every open issue blocking it is already in the work
metadata:
  type: feedback
---

# The work in hand can be several issues

The work the autopilot takes on is not limited to one issue. It begins with the lowest-numbered listed issue that no open issue blocks, and other listed issues may be added to it. The autopilot is the skill in `.claude/skills/autopilot/SKILL.md`.

**Why:** Issues that change the same code share one design, and taken one at a time each is designed without the others in view. The user holds this rule in the sibling repos `cladenc` and `assert-no-comments`. It was carried over on 2026-11-15, when the user asked for an autopilot skill in this repo; the user has not reviewed it for this repo.

**How to apply:** Which issues to add is the session's choice. An issue that an open issue blocks joins only when every open issue blocking it is already in the work, and it is closed no earlier than they are, in the same commit or a later one; that keeps the order the edges set, per [Blocked-by edges set the order](blocked-by-edges-set-the-order.md). An issue labelled `needs decision`, or carrying a label that `--skip-label` names, never joins. Each commit closes at least one of the work's issues, per [A commit closes at least one issue](a-commit-closes-at-least-one-issue.md). When an issue of the work turns out to need a person, it is labelled per [Before an issue is labelled needs decision](before-an-issue-is-labelled-needs-decision.md) and leaves the work, with its edits and the issues it blocks, and the rest goes on.

Claude's interpretation: every issue added costs the session's context its whole body and its share of the code, so add one only where solving it apart would mean designing the same code twice.
