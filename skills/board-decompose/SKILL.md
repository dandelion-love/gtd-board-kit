---
name: board-decompose
description: Break an epic into story-level issues, or a story into steps, the kit's standard way, through the gtd MCP server. Use when asked to plan, split, slice or decompose an epic, an outcome or a large issue into stories, or a story into steps, in a repo that has gtd-board-kit. It proposes work for a person to promote; it never makes work agent-ready.
metadata:
  author: gtd-board-kit
  version: 0.1.0
---

# Decompose work into stories and steps

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file's Kinds, labels and rules win over anything below. The
standard is `.gtd/kit/knowledge/decisions/decomposition-standard.md`: an epic holds
stories, a story holds steps, and a step never has a PR of its own.

Only decompose when you were pointed at it (BOARD.md rule 4). Writes need the Issue
structure group (`issue_type_set`, `sub_issue_add`, `issue_blocked_by_add`,
`issue_update`); without it, post the plan as one `issue_comment` and stop.

## 1. Read before you write

1. `profile_get`: its Kinds and `pickup_sizes`. Never use a retired Kind (`task`,
   `question`, `decision`).
2. The epic: its body, `sub_issues_list` (stories that already exist) and
   `issue_blocked_by_list`. Extend what is there; never duplicate a story.
3. Planning an epic is work on it: claim it `explicit` (`board-claim` §1, no `branch`).

## 2. The epic's outcome check

The epic needs one or two checkable criteria under a `## Outcome check` heading: what is
true when the outcome is reached, beyond "every child is closed". Missing? Append a
draft with `issue_update`, keep the person's text unchanged, and say so in your report.

## 3. Slice the stories

- **Vertical slices**: each story leaves the system working and is mergeable alone, as
  one PR in one session. Bigger than the largest `pickup_sizes` value? Split it again.
- **New system**: the first story is a walking skeleton, the thinnest end-to-end path.
  An epic that changes an existing, working system skips it.
- **Kind per story**: `story` (a user-visible change), `chore` (technical work with its
  own PR), `bug` (a failing repro), `spike` (timeboxed; its output is a `finding`) or
  `research` (sourced knowledge concepts). Plan no `finding` as work: a spike or research
  story produces it.
- **Questions** are not stories. One that blocks planning: `board-needs-person` on the
  epic. Its own `chore` or `spike` only when answering it is work.
- A choice the work will make is recorded as a Decision concept by that story's PR;
  name it in the story, never file it as an issue.

## 4. Write each story

```
<one or two lines: what changes, for whom, and why; link the epic>

## Acceptance criteria
- [ ] <one checkable statement>
- [ ] If <bad input or failure>, then <visible result>

## Steps
- [ ] <a step inside this story; no PR of its own>

Blocked by #<n>
```

- Use exactly one `## Acceptance criteria` heading. Default to a rule list, one
  checkable line each; write an event as a When / If-then line; include at least one
  error or rejection case. A spike states its timebox and the question it answers.
- Each criterion names its evidence (a test, a command and its output, a screenshot), so
  the PR can show one Evidence row per criterion.
- A `Blocked by` line only alongside a native link (step 5); prose alone fails the ready
  check.

## 5. Create and link

For each story, in dependency order:

1. `capture(title, note=<body>, repo, labels=["agent-proposed"], profile)`.
2. Kind: `issue_type_set(number, issue_type=<Kind's type name>)`. A repo without Issue
   Types uses a `kind:<kind>` label through `issue_labels` instead, never both.
3. `sub_issue_add(parent=<epic>, child=<number>, repo)`.
4. Each dependency: `issue_blocked_by_add(number, blocker, repo)`. Never make a cycle.
5. With the Board level: `project_add_item`, then a suggested `Size` with
   `project_set_field`. A person may change it.

Steps stay a checklist in the story body. Use sub-issues as steps only where
`.gtd/BOARD.local.md` says so; they are never claimed or given a PR. A step that turns
out to need its own PR is a `chore`: `capture` it `agent-proposed`.

## 6. Check each story

When `whoami` lists the Readiness group, call `item_ready(repo, number, project)` on
every story; never restate its rules. `needs-refinement`: fix what `missing` names and
check again. `ready-blocked` is fine for a story waiting on a sibling. Without the tool,
say in the report that readiness is unchecked.

## 7. Hand to a person

- Never add `agent-ready` or `run-agent`, never remove `agent-proposed`, never start a
  story you proposed: a person promotes it.
- Ask once, with everything on one screen: the outcome check, then each story's title,
  Kind, Size and blockers, with links.
  - Four stories or more: epic-intent approval comes first.
    `item_report(state="waiting", attention=..., needs=<profile's owner_needs>,
    note="Approve the plan or comment changes")`.
  - Three or fewer: no intent approval; the person adds `agent-ready` to each story.
- `item_release(done=<stories created>, remaining=<open questions>, next="a person
  promotes the stories")`. Comments asking for changes: claim again and revise.
