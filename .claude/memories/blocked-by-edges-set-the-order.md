---
name: blocked-by-edges-set-the-order
description: The autopilot takes only issues that no open issue blocks, so blocked-by edges decide its order; on 2026-11-15 the user had issues 1 to 8 chained in number order, three edges for order alone; how to read, write, and remove an edge with gh api
metadata:
  type: project
---

# Blocked-by edges set the order

The autopilot (`.claude/skills/autopilot/SKILL.md`) takes only issues that no open issue blocks, so the `blocked by` edges between issues, which GitHub calls issue dependencies, decide the order it works in. On 2026-11-15 the user asked that these edges make the autopilot solve the issues open that day, 1 to 8, in order. Each of issues 2 to 8 was given an edge to the issue one number below it.

**Why:** The user asked for the order and gave no reason. Four of the seven edges restate a dependency that the issue bodies name. Three state the order alone: 4 on 3, 5 on 4, and 6 on 5. The sibling repos hold a rule that an edge is written only where the block is real and that an order is not a dependency. That rule was not adopted here.

**How to apply:** Do not remove an edge of that chain because it names no real dependency.

- Read: an issue is blocked while `gh api repos/{owner}/{repo}/issues/<number>/dependencies/blocked_by --jq '.[].state'` prints `open`. `gh api` fills in `{owner}` and `{repo}`. The issues that an issue blocks are under `.../dependencies/blocking`.
- Write: `gh api repos/{owner}/{repo}/issues/<number>/dependencies/blocked_by -F issue_id=<id>`, where `<number>` is the issue that waits and `<id>` is the blocker's numeric id from `gh api repos/{owner}/{repo}/issues/<n> --jq .id`, not the node id that `gh issue view --json id` returns. `-F` sends the id as a number; sent with `-f`, as a string, it is rejected with HTTP 422.
- Remove: `gh api -X DELETE repos/{owner}/{repo}/issues/<number>/dependencies/blocked_by/<id>`.
- An issue split off from one of the chain, per [An issue is brought up to date before work](an-issue-is-brought-up-to-date-before-work.md), gets the edges that put it where its work belongs: blocked by what it builds on, and blocking what builds on it.

Claude's interpretation: the request covered those eight issues. For an issue filed later, write an edge where it cannot be finished before another is closed, and ask the user before chaining issues for order alone. An edge cannot keep a later issue out of the autopilot's reach; only the `needs decision` label or a `--skip-label` does that.
