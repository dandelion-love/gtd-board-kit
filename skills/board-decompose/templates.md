# Epic and story bodies

Part of the `board-decompose` skill. Read `.gtd/kit/BOARD.md` and the skill's `SKILL.md`
first. These are the bodies the skill writes; `templates/issues/` holds the same shapes
as GitHub issue templates a person can copy into `.github/ISSUE_TEMPLATE/`.

The sections come from the decomposition research: the epic carries the goal, scope and
out of scope, its own "done when" and the decisions it makes
([templates](../../knowledge/decomposition/github-primitives/issue-forms-and-templates.md),
[landscape](../../knowledge/decomposition/skill-landscape/skill-landscape-comparison.md)), and the
plan a person approves at G1 fits on one screen
([epic intent](../../knowledge/decomposition/human-gates/design-approval-gate.md)).

## Epic

```
<One line: the outcome, for whom, and why now.>

## Problem
<What is wrong or missing today, with links to evidence.>

## Outcome check
- [ ] <Checkable: what is true when the outcome is reached, beyond "every child is closed".>

## Scope
- <What this epic changes.>

## Out of scope
- <What it deliberately leaves alone, so no story drifts into it.>

## Stories
| # | Story | Kind | Size | Blocked by |
| --- | --- | --- | --- | --- |
| #<n> | <title> | story | S | #<m> |

## Decisions
- <A choice this epic's work makes: the Decision concept and the story whose PR records it.>

## Risks and open questions
- <Risk or question; who answers it (a needs:* label on the item it blocks).>

## Gates
- G1 epic intent: <needed (four stories or more) or skipped>
- G3 walking skeleton: <#n, or skipped (changes an existing, working system)>
```

- The **Stories** table is the plan as approved; the native sub-issues stay the record.
  Update the table when a story is added, split or dropped, in the same session.
- Keep the person's text. A missing section is appended as a draft under its heading,
  marked `_Draft by an agent; edit freely._`, and named in your report.
- Every section is present. One with nothing in it says `None.` so a reader knows it
  was considered.

## Story

```
<One or two lines: what changes, for whom, and why; link the epic.>

## Acceptance criteria
- [ ] AC1: <one checkable statement>; Evidence: <test, command and output, screenshot, file>
- [ ] AC2: If <bad input or failure>, then <visible result>; Evidence: <...>

## Steps
- [ ] <a step inside this story; no PR of its own>

Blocked by #<n>
```

- Exactly one `## Acceptance criteria` heading. A rule list, one checkable line each;
  an event as a When / If-then line; at least one error or rejection case. A spike states
  its timebox and the question it answers.
- Number them `AC1`, `AC2`, ... and name each one's evidence, so the PR shows one
  Evidence row per id (the PR check).
- A `Blocked by` line only alongside a native link; prose alone fails the ready check.
