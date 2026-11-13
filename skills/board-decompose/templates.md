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

## Titles and summaries

Every title and every body's first lines follow the
[prose check](../../server-spec/prose-check.md)
([why](../../knowledge/decisions/clear-titles-and-summaries.md)). In short:

- **Title**: an imperative verb, then one outcome a person or agent gains, in plain words,
  25 to 72 characters. No prefix (`Epic:`, `Server:`, `Part 3:`, `[docs]`), no subtitle, no
  list, no tool, file, field or label names, no issue numbers or dates.
- **Summary**: the body opens with one to three sentences, under 400 characters: who it
  helps, what is wrong or missing today, what they can do once it closes.
- **Context last**: parent epic, origin, evidence links, revisions and approvals go under
  `## Context` at the end.

| Instead of | Write |
| --- | --- |
| Part 3: the export retries on a busy store | Retry the export when the store is busy |
| Server: export_job gets a backoff parameter | Retry the export without flooding the store |
| Epic: lanes get slots, intake rules, and a review label | Let a lane run several agents in parallel without idling |
| Flow metrics contract: wait reasons, cycle time | Define how wait time and cycle time are recorded |
| Warn on a missing kit, and review plan PRs | Two stories: "Warn at session start when the kit is missing", "Review a plan PR as the plan itself" |

A summary, before and after:

- Before: "Part of the export epic (gap 2). Today a 429 from the store is logged and dropped."
- After: "When the store is busy, the nightly export retries instead of dropping rows, so
  owners stop finding gaps in the next day's report. Today a busy store loses the batch."

When the server offers `prose_check`, run it on each title and body before `capture` and fix
every `fail`; weigh each `warn`.

## Epic

```
For <who>, <the outcome>. Today <what is wrong>. <One more line if needed.>

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

## Context
<Where this came from, evidence links, revisions and approvals.>
```

- The **Stories** table is the plan as approved; the native sub-issues stay the record.
  Update the table when a story is added, split or dropped, in the same session.
- When you ask for G1, also save the plan as a `plan` issue artifact on the epic
  (`issue_artifact_create`, when offered), so what the person approved stays on record.
- Keep the person's text. A missing section is appended as a draft under its heading,
  marked `_Draft by an agent; edit freely._`, and named in your report.
- Every section is present. One with nothing in it says `None.` so a reader knows it
  was considered.

## Story

```
When <situation>, <who> can <outcome>, so <benefit>. Today <what happens instead>.

## Acceptance criteria
- [ ] AC1: <one checkable statement>; Evidence: <test, command and output, screenshot, file>
- [ ] AC2: If <bad input or failure>, then <visible result>; Evidence: <...>

## Steps
- [ ] <a step inside this story; no PR of its own>

Blocked by #<n>

## Context
<Origin, evidence links, revisions and approvals. The parent link shows the epic.>
```

- Exactly one `## Acceptance criteria` heading. A rule list, one checkable line each;
  an event as a When / If-then line; at least one error or rejection case. A spike states
  its timebox and the question it answers.
- Number them `AC1`, `AC2`, ... and name each one's evidence, so the PR shows one
  Evidence row per id (the PR check). Evidence that should stay on the issue (a link, a
  report, a diagram) goes in an issue artifact
  ([where evidence goes](../../knowledge/model/evidence-places.md)); never a sub-issue.
- A `Blocked by` line only alongside a native link; prose alone fails the ready check.
