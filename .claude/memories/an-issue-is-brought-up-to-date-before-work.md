---
name: an-issue-is-brought-up-to-date-before-work
description: Before the autopilot works on an issue it brings the title and body up to date with the code as it stands, without widening it, and checks that it documents one problem that one commit can solve; one that holds more is split
metadata:
  type: feedback
---

# An issue is brought up to date before work

Before the autopilot (`.claude/skills/autopilot/SKILL.md`) works on an issue, it brings the issue's title and body up to date with the code as it stands.

**Why:** An issue is written ahead of its work. It relies on names, files, and behaviour that earlier issues build, and those can come out differently from what was planned; issues 2 to 8 each rely on what the issues before them build. An issue is read as the current statement of the work, so a stale one is corrected before its work starts and is not worked around. The user holds this rule in the sibling repo `cladenc`. It was carried over on 2026-11-15, when the user asked for an autopilot skill in this repo; the user has not reviewed it for this repo.

**How to apply:** Read the issue, then the code it names and relies on. Where they disagree and the code is right, rewrite the issue with a guarded edit such as `[ -s body.md ] && gh issue edit <number> --body-file body.md`. Keep the shape the issues here have: a section for the problem and a section for the change, one line for each paragraph, each term explained where it is first used, and nothing of the user's quoted, per [Never quote the user verbatim](never-quote-the-user-verbatim.md). Where the disagreement is a question only a person can settle, see [Before an issue is labelled needs decision](before-an-issue-is-labelled-needs-decision.md).

Bringing an issue up to date does not widen it. An issue asks for what its title asks and nothing more.

Check at the same time that the issue documents one problem, names one change that solves it, and can land in one commit, per [A commit closes at least one issue](a-commit-closes-at-least-one-issue.md). An issue that holds more is split into one issue for each problem, and the issue itself is kept as the part its title leads with. A split divides problems, not lists of files: two symptoms of one defect stay together. Each new part gets its edges per [Blocked-by edges set the order](blocked-by-edges-set-the-order.md).
