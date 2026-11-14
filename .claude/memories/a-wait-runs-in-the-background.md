---
name: a-wait-runs-in-the-background
description: A wait for a workflow run or anything else that takes minutes is a background Bash call or a Monitor, never a foreground sleep, gh run watch, or polling loop; gh run watch inside it takes --interval 60
metadata:
  type: feedback
---

Waiting for a workflow run, or for anything else that takes minutes, is done with `Bash` and `run_in_background: true`, which notifies once when the command exits, or with `Monitor`, which reports each event. It is never a foreground `sleep`, a foreground `gh run watch`, or a polling loop in the session's own shell.

**Why:** The user holds this rule in the sibling 10U-Labs repos and in repos one level further up, and on 2026-11-14 asked for it to be adopted here. The reason those repos record: a foreground wait holds the session busy for the whole run, so the user cannot type and scheduled reminders cannot fire. The render workflow here runs for minutes, so the rule applies to every push that starts it.

**How to apply:** Start the wait in the background, end the turn, and act on the completion notification. `gh run watch <id> --exit-status --interval 60` is fine inside the background command; it is the foreground that is the problem.

The interval is there because `gh run watch` polls every 3 seconds by default, and over a long run that trips GitHub's secondary rate limit. Once it has tripped, every `gh` call answers HTTP 403 while `gh api rate_limit` still shows every bucket full, and it clears only after several minutes without a call. When a `gh` call answers 403 that way, the next one waits behind a background `sleep` and is not retried at once.

While the run is in progress, nothing but the wait goes on: no diagnosis, edits, or commits. This comes from the sibling versions of this memory; the user did not name it separately, and carrying it over is Claude's reading of the request. Any other command that can run past a minute follows [Long-running commands in the background](long-running-commands-in-the-background.md).
