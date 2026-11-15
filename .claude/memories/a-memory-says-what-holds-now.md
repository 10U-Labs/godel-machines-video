---
name: a-memory-says-what-holds-now
description: A memory states a rule or fact as it holds now, with its reason and how to apply it; it is not a history, so it carries no dates of conversations, no account of what was proposed, answered, or done, and no note of where a rule came from
metadata:
  type: feedback
---

# A memory says what holds now

A memory states a rule or a fact as it holds now, the reason for it, and how to apply it. It is not a history: it tells nothing of how the rule came about.

**Why:** It is the user's rule, and no reason comes with it. Claude's interpretation: a memory is read to decide what to do next, and an account of what was said, proposed, or done on which day changes nothing about that. It makes the memory long, and it goes stale. What happened is kept where it happened, in the issues, the commits, and the transcript.

**How to apply:** The list is Claude's reading of the rule.

- Write in the present tense: what the rule is, not when or how it was set.
- Give the reason as a reason, not as an event. A sentence that opens with a date, or with what the user did after seeing something, is an event.
- Leave out the date of a conversation, what Claude proposed first, what the user answered, which draft or render was on the table, and the order things were decided in.
- Leave out where a rule came from: that it was adopted from another repo, on which day, and at which request.
- Leave out the state of the work: what a commit, a draft, or a session did, and how the tree stood on some day.
- Say whose the rule is, since that decides whether it may be reopened: the user's rule, or Claude's interpretation that the user has not confirmed. That is a fact about the rule, not a story.
- A case that shows what the rule means stays, written as an example and not as an incident.
- When a rule changes, rewrite the memory to say the new rule. Do not add a paragraph that says it changed.
- Before saving, ask whether the memory would read the same if it were written a month from now. What would differ is history.

The entries of `MEMORY.md` follow the same rule. Related: [Never quote the user verbatim](never-quote-the-user-verbatim.md), which covers the user's words where this covers what was said and done.
