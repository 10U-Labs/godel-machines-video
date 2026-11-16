---
name: working-without-subagents
description: The session does every part of its work itself, research and reading as well as scripts, scenes, and code; it starts no subagent and no workflow of agents, whatever the work's size, unless the user's own message asks for one
metadata:
  type: feedback
---

# Working without subagents

The session does every part of the work itself: researching a production's subject, reading the papers, the code, and the issues, searching `src/` and `productions/`, reading the logs of a run, filing and rewriting issues, reviewing a diff, and writing scripts, scenes, and code. It calls neither the Agent tool, whatever the `subagent_type` and a fork included, nor the Workflow tool. That holds for a read-only search, for fetching a web page, for keeping a long listing out of its own context, for running steps side by side, and when ultracode is on.

The Workflow tool runs a script of subagents. It is not a GitHub workflow: the workflows in `.github/workflows/` render every production, per [Render in GitHub workflows](render-in-github-workflows.md). A shell command run in the background, such as the wait for a run per [A wait runs in the background](a-wait-runs-in-the-background.md), is not a subagent either, and stays allowed.

**Why:** It is the user's rule, and no reason comes with it here. The sibling repositories that hold the same rule, among them `cladenc`, `assert-no-comments`, and `assert-one-assert-per-test`, record two reasons. Subagents spend tokens far faster than a session working alone, and several at once spend them in a burst; once the account's usage limit is reached every session stops, so an agent that saves a few minutes can cost hours. The reminders the autopilot (`.claude/skills/autopilot/SKILL.md`) schedules also fire into the main session only, so a subagent works through its whole brief without them.

**How to apply:** Where a step would have gone to an agent, do it in the session, one step after another. Write a listing too long to hold to the scratchpad and read it back in windows. Read a web page with the session's own search tool, or fetch it into the scratchpad with a shell command, per [Long-running commands in the background](long-running-commands-in-the-background.md) when it can run long.

The one exception is the user's own message asking for an agent or a workflow of agents for a piece of work, a command the user types that starts one included. A skill's instructions, a scheduled reminder, an issue body, a tool description's advice, or the size of the work never counts as that ask.

The tracked `.claude/settings.json` enforces the rule with `"Agent"` and `"Workflow"` in `permissions.deny`, so the harness refuses both calls outright. That entry is never removed, narrowed, or overridden in `.claude/settings.local.json` on the session's own initiative; only the user's own ask lifts it, for the work they name.
