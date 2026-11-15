---
name: every-run-is-watched
description: After a push the autopilot goes straight on with the next work, further pushes included; every workflow run the push starts is watched to its end by a background command, and a run that failed is fixed in the next commit pushed, ahead of other work
metadata:
  type: feedback
---

# Every run is watched

After a push, the autopilot (`.claude/skills/autopilot/SKILL.md`) goes straight on with the next work, further commits and pushes included. Every workflow run the push started is watched to its end by a background command.

**Why:** A run that nobody watches can fail unseen, most of all when the session has no new work and stops. A render of the whole Gödel machines film takes about four hours, so a session that waited for each run would sit idle for most of a day. The user allows other work during a run in this repo, per [A wait runs in the background](a-wait-runs-in-the-background.md). That further pushes go on as well, that each run is watched, and that a failed run is fixed first are the user's rules for the autopilot in the sibling repo `cladenc`. That they hold in this repo is Claude's reading, which the user has not confirmed.

**How to apply:**

- Right after a push, list the runs it started: `gh run list --commit <sha> --json databaseId,workflowName,status`, where `<sha>` is the full hash that `git rev-parse HEAD` prints; a short hash lists nothing. A run takes a few seconds to appear, so when the listing shows fewer runs than the `on:` sections of the workflows in `.github/workflows/` say the push starts, list again.
- Start one watch for each run as a background `Bash` call: `perl -e 'alarm 21600; exec @ARGV' gh run watch <id> --exit-status --interval 60 --compact`, with its output sent to a file in the scratchpad.
- Go on with the work. When nothing but the watches is left, end the turn; the notification of a watch that ends resumes the session.
- A watch that ends with status 0 says the run passed. For any other status, read `gh run view <id> --json conclusion --jq .conclusion`.
- Each workflow cancels its own earlier run on `main` when a later push starts it again. A run cancelled that way is left alone, since the later run is watched in its place.
- A watch that its time limit ended, with the run still queued or in progress, is started again.
- A run that failed is fixed in the next commit the session pushes, ahead of any other work not yet pushed. Read `gh run view <id> --log-failed`, set work in the tree that is not part of the fix aside with `git stash`, push the fix as a commit of its own, and bring the work back. The issues the failed commit closed stay closed while the fix goes in.
- A session that starts or resumes while a run of an earlier push is still queued or in progress watches that run too.
- Tell the user how each run ended.

Claude's interpretation: the sibling repo `cladenc` records that the organization's free runners are shared by all its repos, so a render of a whole film holds up their runs for hours. Before a push, work out from the workflow what the push will render. A change that alters no picture does not render a film again where the issue or the workflow gives a way to reuse the clips that exist.
