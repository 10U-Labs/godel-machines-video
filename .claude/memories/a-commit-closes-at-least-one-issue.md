---
name: a-commit-closes-at-least-one-issue
description: Every commit the autopilot makes closes at least one issue, with a Closes #N line of its own for each; only the fix for a failed run and a change the user asks for directly close none; after the push each issue is read back and closed by hand if still open
metadata:
  type: feedback
---

# A commit closes at least one issue

Every commit the autopilot (`.claude/skills/autopilot/SKILL.md`) makes closes at least one issue of the work in hand. It may close more than one, and it never closes none.

**Why:** A string of commits that each touch an issue and none closes it leaves the issue's work half done on `main`, and the list of open issues stops saying what is left to do. Here an issue left open also keeps every issue it blocks out of the autopilot's reach, per [Blocked-by edges set the order](blocked-by-edges-set-the-order.md). The user holds this rule in the sibling repo `cladenc`. It was carried over on 2026-11-15, when the user asked for an autopilot skill in this repo; the user has not reviewed it for this repo.

**How to apply:**

- Commit when the work finishes at least one issue; until then it stays in the working tree. An issue whose work cannot land in one commit is split before its work starts, per [An issue is brought up to date before work](an-issue-is-brought-up-to-date-before-work.md).
- Give each issue the commit finishes a line of its own reading `Closes #N`, ahead of the attribution line. GitHub binds a closing keyword to one number, so `Closes #1, #2` closes the first and leaves the second open.
- Write `Refs #N` for an issue the commit only mentions, and keep the subject free of a closing word followed by `#N`, since a subject such as `Fix the planner (#3)` closes issue 3 on push.
- A memory, or anything else changed along the way, rides in a commit that closes an issue.
- Two kinds of commit close nothing: the fix for a failed run of the session's own push, per [Every run is watched](every-run-is-watched.md), and a change the user asks for directly. The sibling repo records both exceptions as Claude's reading, not the user's.
- Some of what an issue asks for is not in the tree, such as the repo's About text or a manual workflow run. Do that part with the push, so that no issue is closed with part of its change undone.
- After the push, read `gh issue view <N> --json state --jq .state` for each `Closes #N` line. The sibling repos have seen GitHub accept a commit on `main` and act on none of its closing lines. Close any issue still open with `gh issue close <N> --reason completed` and a comment that names the commit.
