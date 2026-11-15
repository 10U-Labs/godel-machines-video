---
name: render-in-github-workflows
description: Renderings for any production run in GitHub Actions workflows, never on the local Mac; commit and push to main without asking whenever a change should be rendered or checked
metadata:
  type: feedback
---

# Render in GitHub workflows

Renderings in this repo, for any production, run in GitHub workflows, not on the local machine.

**Why:** It is the user's rule, and no reason comes with it. Claude's interpretation: it matches the practice in the sibling 10U-Labs repos, where work runs in CI and not on the developer's machine.

**How to apply:** Do not run frame capture, encoding, or final assembly locally. Push to `main` and let the workflow in `.github/workflows/` render; fetch results with `gh run download`. A push renders the productions whose folders it changes; after a push of shared code alone, start the render with `gh workflow run productions.yml -f production=<name>`. Commit and push to `main` without asking whenever a change should be rendered or checked: that is the user's instruction as well, and its reason is that the runners cost nothing. Claude's interpretation, still to be confirmed by the user: the rule also covers still frames used to check layout, so get those from workflow artifacts too. Related: [Video production decisions](video-production-decisions.md).
