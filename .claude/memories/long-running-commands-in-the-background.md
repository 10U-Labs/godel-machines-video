---
name: long-running-commands-in-the-background
description: Any command that can run past about a minute goes in a background Bash call with a time limit and its output in a scratchpad file, and is never followed by a foreground wait
metadata:
  type: feedback
---

# Long-running commands in the background

Run every command that can take more than about a minute as a background Bash call (`run_in_background: true`), then end the turn and let its completion notification resume the work. In this repo that covers a `gh run download` of scene videos or the film, a sweep of `gh` calls over many runs or artifacts, `npm install`, `pip install`, a download of the voice model, and a long `grep` or `find` over a sibling repository, as well as the wait for a workflow run in [A wait runs in the background](a-wait-runs-in-the-background.md). Frame capture, encoding, and assembly are not among them, because per [Render in GitHub workflows](render-in-github-workflows.md) they are not run locally at all.

**Why:** The user holds this rule in the sibling 10U-Labs repos and in repos one level further up, and on 2026-11-14 asked for it to be adopted here. The reason those repos record: a foreground command holds the turn for as long as it runs, so the user cannot type and any scheduled reminder due in that time waits behind it. A background command frees the turn as soon as it starts.

**How to apply:**

- Give a command that might not end a time limit as well. macOS has no `timeout`, so use `perl -e 'alarm 60; exec @ARGV' <command>`.
- Send the output to a file in the scratchpad and read that file once the notification arrives.
- Never follow a background command with a foreground wait: no `sleep`, no `until` loop, and no rereading its output file until it fills. Any of them blocks the session again.
- Other work that does not depend on the result may go on meanwhile, including while a workflow run is in progress. Once only the result is left to wait for, end the turn. The sibling versions of this memory forbid other work during a run; the user dropped that restriction for this repo on 2026-11-14.
- A turn made of many short foreground calls also holds the session for its whole length. Split long work at its natural boundaries, such as after a batch of edits.
