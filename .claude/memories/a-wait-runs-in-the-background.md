---
name: a-wait-runs-in-the-background
description: A wait for a workflow run or anything else that takes minutes is a background Bash call or a Monitor, never a foreground sleep, gh run watch, or polling loop; gh run watch inside it takes --interval 60
metadata:
  type: feedback
---

# A wait runs in the background

Waiting for a workflow run, or for anything else that takes minutes, is done with `Bash` and `run_in_background: true`, which notifies once when the command exits, or with `Monitor`, which reports each event. It is never a foreground `sleep`, a foreground `gh run watch`, or a polling loop in the session's own shell.

**Why:** It is the user's rule. A foreground wait holds the session busy for the whole run, so the user cannot type and scheduled reminders cannot fire. A render here runs from minutes to hours, so the rule applies to every push that starts one.

**How to apply:** Start the wait in the background, end the turn, and act on the completion notification. `gh run watch <id> --exit-status --interval 60` is fine inside the background command; it is the foreground that is the problem.

The interval is there because `gh run watch` polls every 3 seconds by default, and over a long run that trips GitHub's secondary rate limit. Once it has tripped, every `gh` call answers HTTP 403 while `gh api rate_limit` still shows every bucket full, and it clears only after several minutes without a call. When a `gh` call answers 403 that way, the next one waits behind a background `sleep` and is not retried at once.

Other work may go on while the run is in progress. Here the rule differs from its version in the sibling repos, where nothing but the wait goes on during a run; the user allows other work in this repo. Any other command that can run past a minute follows [Long-running commands in the background](long-running-commands-in-the-background.md).
