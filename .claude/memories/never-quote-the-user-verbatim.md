---
name: never-quote-the-user-verbatim
description: Never record the user's words verbatim in a memory, issue, commit message, code comment, task, feedback draft, or summary; restate what they meant in fresh words
metadata:
  type: feedback
---

Nothing the user writes is recorded word for word, anywhere: not in a memory, an issue, a commit message, a comment in code, a task, a feedback draft, a summary, or a compaction. Each of those carries the user's point restated in fresh words, with no quotation marks around the user's sentences and no unquoted copy of them either.

**Why:** The user does not want their own wording kept on record. They hold this rule in the sibling 10U-Labs repos (as `never-quote-the-user-verbatim`) and in repos one level up (as `user-words-are-never-recorded-verbatim`), and on 2026-11-14 asked for it to be adopted here. A paraphrase keeps the rule and its reason; the exact wording adds nothing a later session needs.

**How to apply:** Before writing down a correction or an instruction, restate it as the rule it sets. When a **Why:** line cites something the user said, say what they held, without quoting it. A template that asks for the user's words quoted gets a paraphrase marked as one. A term, file, label, or command that the user named keeps that name; that is not a quotation of the sentence around it. Quoting a command, a file's content, a commit message, or Claude's own wording is still fine. The memories written here before this rule were rewritten to follow it; the public git history of this repo still holds their first versions.
