# 13. Prose check

A board is read by people skimming titles in a list. An epic or story whose title or first
lines do not say what it delivers costs every reader a click and a guess. The
[clear titles and summaries decision](../knowledge/decisions/clear-titles-and-summaries.md)
sets the standard; this file fixes the rules a server checks, so every server gives the same
answer for the same text.

The check has two halves:

- **Fail** rules are mechanical: a prefix, a subtitle, a list, code in the title, a length
  outside the limits, a body that opens with something other than a summary. A story that
  fails one is not ready: the [ready check](ready-check.md) fails its `prose` rule.
- **Warn** rules are hints for a judgement a reviewer makes: a title that does not start
  with a verb, an "and", a spec-only word. They never change a verdict.

Nothing refuses a write for prose. The writes listed below return the findings as warnings,
and the agent or person fixes the text.

## The standard, in short

- **Title**: an imperative verb, then one outcome a person or agent gains, in plain words,
  25 to 72 characters. No prefix ("Epic:", "Server:", "Part 3:", "[x]"), no subtitle, no list,
  no tool, file, field or label names.
- **Body**: opens with a summary of one to three sentences: who it helps, what is wrong or
  missing today, and what they can do once it closes. Parent epic, origin, evidence links,
  revisions and approvals go last, under `## Context`.
- **Epic**: the summary is the hypothesis ("For <who>, <outcome>. Today <problem>."), then
  `## Problem` and `## Outcome check` as the epic template has them.

## The tool

`prose_check` is in the **Readiness** optional group ([tools](tools.md#optional-groups)).

| Tool | Class | Arguments | Returns |
| --- | --- | --- | --- |
| `prose_check` | read | (`repo` and `number`) or (`title`, `body?`, `kind?`) | `verdict`, `findings`, and `repo`, `number`, `kind` when an issue was read |

- With `repo` and `number` it reads the issue's title, body and [Kind](repo-context-and-profiles.md#kinds).
  With `title` it checks the text given, so an agent can check a draft before `capture`;
  `kind` defaults to `story`.
- It works on every Kind, epics included. A pull request refuses ("a PR title follows the
  repo's commit rules").
- `verdict` is `clear` (no fail finding) or `unclear` (at least one).
- `findings` lists `{rule, level, detail}` in the order of the tables below; `level` is
  `fail` or `warn`; `detail` is one line a person can act on (the words that broke the
  rule, or the length).
- It writes nothing.

## Prose warnings on writes

A server that offers `prose_check` SHOULD also return `prose_warnings` (the same
`findings`, or an empty list) from `capture`, `issue_update` when it changes a title or a
body, and `organize`. They never refuse and never change what is written.

## The rules

Text is checked after trimming and collapsing runs of whitespace in the title. Body rules
read only lines outside fenced code blocks (fences as in the
[ready check](ready-check.md#the-rules)), and skip lines that hold only an HTML comment.
Word lists (`verbs`, `jargon`, `provenance_starts`, `code_extensions`) live in
[prose_cases.json](../conformance/prose_cases.json); a server uses those lists as given.

### Title

| Rule | Level | Fails or warns when |
| --- | --- | --- |
| `title-prefix` | fail | The title starts with `[`, or a colon ends one of its first four words (`Epic: ...`, `Part 3: ...`, `Server spec: ...`) |
| `title-subtitle` | fail | After any prefix, the title holds `:`, `;`, `→`, `->`, or a dash with a space on each side (`-`, `–`, `—`) |
| `title-list` | fail | The title holds two commas or more |
| `title-code` | fail | The title holds a backtick; a word with `_` between letters or digits; a word ending in `.` plus one of `code_extensions`; `#` followed by a digit; or a date `YYYY-MM-DD` |
| `title-length` | fail | The title is shorter than 25 or longer than 72 characters (Unicode code points) |
| `title-verb` | warn | The first word, lower-cased with surrounding punctuation removed, is not in `verbs` |
| `title-and` | warn | The title holds the word `and` (any case) |
| `title-jargon` | warn | A word of the title, lower-cased with surrounding punctuation removed, is in `jargon` |

### Body

The **summary** is the first paragraph: the first line that is not blank, and the lines after
it up to a blank line or a heading.

| Rule | Level | Fails when |
| --- | --- | --- |
| `summary-first` | fail | The body has no line; or its first line is a heading, a list item (`-`, `*`, `+`, `1.`), a table row (starts with `\|`), a quote (`>`), or starts with an issue reference (`#N`, `owner/repo#N`) or `http`; or it starts, ignoring case, with one of `provenance_starts` |
| `summary-length` | fail | The summary is longer than 400 characters, its lines joined with one space |
| `epic-sections` | fail | Kind `epic` only: no heading whose text starts (ignoring case) with `problem`, or none that starts with `outcome check` |

## In the ready check

The [ready check](ready-check.md)'s sixth rule, `prose`, runs these rules on the story's
title and body with its Kind (`story` when it has none) and fails when any fail finding
is returned. Its `detail` names the failed rules. Warn findings do not count.

## Golden cases

[prose_cases.json](../conformance/prose_cases.json) gives a `title`, a `body` and a `kind`
for each case, with the expected `verdict`, failed rules and warned rules, each in rule
order. Check R9 runs them offline against the runner's `reference_prose`, or against a
server's own logic through `--prose-cmd`
([runner](../conformance/README.md#testing-your-prose-check-offline)).
