---
name: memory-links-are-markdown-links
description: One memory points at another with a Markdown link to its file, written as title in square brackets then file name in parentheses, never the double-bracket form, which GitHub shows as plain text
metadata:
  type: feedback
---

A memory that points at another memory uses a standard Markdown link to its file, such as `[Render in GitHub workflows](render-in-github-workflows.md)`. It never uses the double-bracket form `[[render-in-github-workflows]]`, even though the session's own memory instructions ask for that form.

**Why:** The memory files are committed to this public repository and read as Markdown on GitHub. Markdown has no double-bracket syntax, so GitHub shows such a link as literal brackets that go nowhere, and a linter cannot check it, so a renamed or deleted memory leaves a dead reference nobody sees. The user holds this rule in `wan-synthesizer` and in a repo one level further up, and on 2026-11-14 asked for it to be adopted here.

**How to apply:** Use this form whenever a memory is written or edited, and convert any double-bracket link found in an existing memory. Link only to a memory file that exists; a name with no file yet is not linked at all, so file that memory first. Double brackets inside a code span that are not links, such as a TOML section header, stay as they are. The two source versions differ on the link text (one uses the file's slug, the other the target's heading); Claude's choice here is the target's title as `MEMORY.md` lists it.
