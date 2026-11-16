---
name: autopilot
description: Start, restart, or stop the autopilot reminders, which keep the session solving the open issues without being asked. Use when the user says "start autopilot", "go autonomous on the open issues", "restart autopilot", or "stop autopilot", or asks to clear the reminders. Takes "start", "restart", or "stop"; "start" and "restart" also take `--skip-label <label>`, repeatable.
---

# Autopilot

The autopilot is a set of scheduled reminders. Together they keep the session solving the open issues, in the order their `blocked by` edges set, until none is left that it can take.

The work in hand is one issue or several: it begins with the lowest-numbered listed issue that no open issue blocks, and other listed issues may join it, per `.claude/memories/the-work-in-hand-can-be-several-issues.md`.

Starting the autopilot is the user's request to commit and push what it solves: each commit goes to `main` without a further go-ahead, per `.claude/memories/render-in-github-workflows.md`, and each closes at least one issue, per `.claude/memories/a-commit-closes-at-least-one-issue.md`.

Fetch `CronCreate`, `CronList`, and `CronDelete` with `ToolSearch` first.

## Reminders

A rule is a reminder only when it tells the session what to do next at the moment it fires: which work to take, to keep going, and how to hand an issue over instead of stopping. Every other rule the work is done under holds whether or not a reminder has just fired, so it is a memory, listed under "Rules that are memories".

Each reminder is indivisible: it states one rule and names one action, so no rule can be quietly dropped from a merged block of text. A rule that names two actions is written as two reminders.

Each reminder fires every ten minutes, on a minute of its own that is two or three minutes from the next, and none falls on the hour or the half hour. A reminder fires only while the session is idle, which is why every command that can run long goes in the background, per `.claude/memories/long-running-commands-in-the-background.md`.

There are four. The first, on `1,11,21,31,41,51 * * * *`, is the listing:

```text
REMINDER: When no work is in hand, run gh issue list --state open --limit 10000 --json number,title,labels --jq 'map(select(all(.labels[]; .name != "needs decision"))) | sort_by(.number) | map({number, title, labels: [.labels[].name]})' to list the open issues no label holds back, lowest number first.
```

The other three:

| Cron | Prompt |
| --- | --- |
| `4,14,24,34,44,54 * * * *` | `REMINDER: Take as the work in hand the lowest-numbered issue of the listing for which gh api repos/{owner}/{repo}/issues/<number>/dependencies/blocked_by --jq '.[].state' prints no open, alone or with other issues of the listing that you choose to solve with it.` |
| `6,16,26,36,46,56 * * * *` | `REMINDER: Continue autonomously: while an open issue can be taken, do not stop to ask or to report.` |
| `9,19,29,39,49,59 * * * *` | `REMINDER: When an issue in hand cannot go on without a person's answer, hand it to a person by labelling it 'needs decision'.` |

In a prompt, `<number>` stands for the issue being checked, and `gh api` fills in `{owner}` and `{repo}` from the repository the session runs in.

No reminder tells the session to wait for a run: after a push the work goes straight on, while a background command watches each run the push started, per `.claude/memories/every-run-is-watched.md`.

## Rules that are memories

Each file is under `.claude/memories/`.

| Rule | Memory |
| --- | --- |
| The work in hand is one issue or several. | `the-work-in-hand-can-be-several-issues.md` |
| The `blocked by` edges set the order the issues are solved in. | `blocked-by-edges-set-the-order.md` |
| An issue is brought up to date before it is worked on, and it documents one problem. | `an-issue-is-brought-up-to-date-before-work.md` |
| An issue is handed to a person only after a check that it needs one, and its body says what is to be decided. | `before-an-issue-is-labelled-needs-decision.md` |
| A commit closes at least one issue, with a `Closes #N` line for each, and each is checked to be closed after the push. | `a-commit-closes-at-least-one-issue.md` |
| After a push the work goes straight on, every run the push starts is watched to its end in the background, and a failed run is fixed in the next commit pushed. | `every-run-is-watched.md` |
| A wait for a workflow run is a background command. | `a-wait-runs-in-the-background.md` |
| A command that can take more than about a minute runs in the background. | `long-running-commands-in-the-background.md` |
| Every part of the work is done in the session itself, with no Agent or Workflow call. | `working-without-subagents.md` |
| Nothing is rendered on the local machine. | `render-in-github-workflows.md` |
| Nothing used to make a production costs money. | `free-tools-only.md` |
| Nothing that belongs to one production goes into shared code. | `the-repo-is-a-media-factory.md` |
| Nothing the user wrote is recorded word for word, in an issue or a commit as anywhere else. | `never-quote-the-user-verbatim.md` |

The other memories that `MEMORY.md` lists hold as well. Read the ones that bear on an issue before working on it: an issue that touches a script or a scene is done under the rules about writing and pictures.

## Start

Each `--skip-label <label>` puts `map(select(all(.labels[]; .name != "<label>"))) |` and a space at the very start of the listing's `--jq` program, and appends `An issue labelled '<label>' is left to a person, whatever else it carries.` to the listing's reminder. The filter stays in the `--jq` program and never moves to `--label` or `--search`, which the sibling repositories found to send the listing through GitHub's search and its limit of 1000 issues. A `--skip-label` that names `needs decision` changes nothing, since the listing leaves that label out as it stands.

An issue is blocked while `gh api repos/{owner}/{repo}/issues/<number>/dependencies/blocked_by` lists an open issue.

1. Make sure the label the autopilot leaves to a person exists: when `gh label list --search 'needs decision' --json name --jq '.[].name'` does not print `needs decision`, create it with `gh label create 'needs decision' --description 'Left to a person' --color d876e3`.
2. Run the listing's command once, its `--skip-label` filters in place. When it names no issue, say so and stop: there is nothing to schedule reminders for.
3. Call `CronList`, and `CronDelete` each job on one of the four crons whose prompt differs from that cron's reminder.
4. `CronCreate` with `recurring: true` each reminder that is not already scheduled.
5. Tell the user how many reminders are running, and the two limits that come with them: the jobs live in this session only and are gone when it ends, and recurring jobs auto-expire after seven days.
6. Read in full each memory that "Rules that are memories" names.
7. Take the lowest-numbered listed issue that no open issue blocks, alone or with other listed issues chosen to be solved with it, and solve that work. When no issue can be taken, follow "When nothing can be taken".

## When nothing can be taken

The autopilot ends itself when no work is in hand and no issue can be taken, either because the listing names no issue or because every issue it names waits on an open issue that the autopilot cannot take. Run "Stop", then tell the user which label or blocking issue holds back each issue still open, or that none is open. The reminders are not left firing with nothing to do; the user starts the autopilot again once an issue can be taken.

The watches of runs still in progress stay. Their notifications resume the session, and a run that failed is still fixed, per `.claude/memories/every-run-is-watched.md`.

## Restart

Run "Stop", then "Start" with the `--skip-label` flags that `restart` was given. That leaves exactly the four reminders, each with seven fresh days, and it is how a changed set of `--skip-label` flags takes effect.

## Stop

`CronDelete` every job `CronList` returns, then call `CronList` again to confirm it is empty and report how many jobs were deleted. A `CronList` that returns nothing is not a failure; say the schedule was already empty.
