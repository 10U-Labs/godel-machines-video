---
name: render-in-github-workflows
description: Video renderings for this repo must run in GitHub Actions workflows, not on the local Mac
metadata:
  type: feedback
---

# Render in GitHub workflows

Renderings for this video run in GitHub workflows, not on the local machine. The user directed this on 2026-11-14, after Claude had rendered scene 1 and several still frames on the Mac. It replaces the earlier plan, made in the planning chat before this repo existed, that production happens locally.

**Why:** The user gave no reason. Claude's interpretation: it matches the practice in the sibling 10U-Labs repos, where work runs in CI and not on the developer's machine.

**How to apply:** Do not run frame capture, encoding, or final assembly locally. Push to `main` and let the workflow in `.github/workflows/` render; fetch results with `gh run download`. On 2026-11-14, when Claude held back a push of script draft 6, the user told it to push and pointed out that CI costs nothing; so commit and push to `main` without asking whenever a change should be rendered or checked. Claude's interpretation, still to be confirmed by the user: this also covers still frames used to check layout, so get those from workflow artifacts too. Related: [Video production decisions](video-production-decisions.md).
