---
name: a-release-is-numbered-by-the-time
description: A release is tagged with the UTC time it is made, as fourteen digits after a v, the way every 10U-Labs repo that releases does; never a count such as v1; in this repo the production's name comes first
metadata:
  type: feedback
---

# A release is numbered by the time

A release carries the time it is made, in UTC, as the fourteen digits that `date -u +%Y%m%d%H%M%S` prints, after a `v`: `v20261115172101`. It never carries a count such as `v1`.

**Why:** It is the user's rule, and it is how the organization's repositories that release already work. The `release.yml` of each sibling repo, such as `orfmi`, `contains-snippet`, `cladenc`, and the `assert-*` checks, makes the version with that `date` command, tags the commit `v<time>`, and creates the GitHub release under that tag. Claude's interpretation: a time needs no look at the releases made before, so two runs cannot pick the same number.

**How to apply:** Take the time in the step that makes the release, and use it for the tag and the release alike. In this repo a release belongs to one production, and the tags of every production share one list, so the production's name comes first: `<production>-v<time>`, such as `godel-machines-v20261115172101`. That prefix is Claude's choice, which the user has not confirmed. `src/render/release.py` makes the release and takes the time as it does. The sibling repos also move a tag named `latest` to each release; whether a production gets one is the user's to say. Read a sibling's `.github/workflows/release.yml` before changing how a release is made here. Related: [The repo is a media factory](the-repo-is-a-media-factory.md).
