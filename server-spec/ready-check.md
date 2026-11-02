# 10. Ready check

Whether a story is **ready** (clear enough to build) is a read-only check of the issue
graph, not a judgement an agent makes. The
[decomposition decision](../knowledge/decisions/decomposition-standard.md) settles this; this
file fixes the rules so that every server returns the same answer for the same issue, and
skills call the tool instead of restating the rules.

Ready is about **clarity**, not **permission**. It does not read `agent-ready`, `run-agent`
or `agent:<x>`, and a `ready` answer never lets an agent take an item it could not claim
before: the claim rules in [tools](tools.md#claims-and-reports) still hold. A person still
makes the "build it now" move ([BOARD.md](../BOARD.md) rule 4).

## The tool

`item_ready` is the **Readiness** optional group ([tools](tools.md#optional-groups)).

| Tool | Class | Arguments | Returns |
| --- | --- | --- | --- |
| `item_ready` | read | `repo`, `number`, `project?` (the board to read Size from; the server's default when omitted) | `repo`, `number`, `title`, `verdict`, `missing`, `blockers`, `kind`, `size` |

- `verdict` is one of three words:
  - `ready`: every rule below passes and no native blocker is open;
  - `ready-blocked`: every rule passes, but at least one native blocker is open;
  - `needs-refinement`: at least one rule fails. Open blockers do not change this.
- `missing` lists each failed rule as `{rule, detail}`, in the order of the table below;
  empty unless the verdict is `needs-refinement`. `rule` is one of the five names below;
  `detail` is one line a person can act on (for `unlinked-blocker`, the reference; for
  `blocker-cycle`, the issues in the cycle).
- `blockers` lists the issue's **open** native blockers (blocked-by links), each with
  `repo`, `number`, `title`, `state`, whatever the verdict.
- `kind` is the issue's Kind (its organisation Issue Type, else a `kind:<kind>` label), or
  null; `size` is the board's Size value, or null.

It **refuses** a pull request ("check its issue instead"), a closed issue, and an issue
whose Kind is `epic` ("an epic is ready through its stories"; an epic's own done rule is in
the decision).

It **writes nothing**: no comment, label, field, Status, board item, issue type or link. An
issue that is not on the board stays off it (the `size` rule fails instead), unlike the
board tools that add an issue first.

## The rules

| Rule | Passes when |
| --- | --- |
| `acceptance-criteria` | The body has a Markdown heading (`#` to `######`) whose text, trimmed and compared case-insensitively, starts with `acceptance criteria`, and at least one list item with text (`-`, `*`, `+` or `1.`, with or without a `[ ]` box; a box alone is not text) sits between it and the next heading of the same or a higher level. Headings and items inside fenced code blocks do not count: a fence opens with three or more backticks or tildes, and closes only on a line of the same character, at least as long, with nothing after it |
| `open-question` | The issue carries no `needs:*` label. A question is `attention` plus a `needs:<who>` label on the item it blocks; while it is open, the item is not ready |
| `unlinked-blocker` | Every blocker is a native blocked-by link: (a) every issue reference (`#N`, `owner/repo#N`, or an issue URL) on a body line after the words `blocked by` or `depends on` (any case, outside fenced code) is one of the issue's native blockers, open or closed; and (b) when the issue carries the `blocked` label, at least one native blocker is open. A reference to the issue itself is ignored |
| `blocker-cycle` | Following **open** native blockers from the issue (an issue's blockers, then theirs) reaches no cycle, whether or not the cycle passes through the issue itself. The walk counts the issue itself; when it reaches 50 issues it stops and the rule fails with a detail saying so, never passes silently. So 49 issues are checked, and 50 fail |
| `size` | The board is readable, the issue is on it, and its `Size` is one of the profile's `pickup_sizes` ([profiles](repo-context-and-profiles.md#profiles)). No board, no item, no Size, or a Size outside the list fails |

The `size` rule is the same pull limit an `inferred` claim applies (check C5), so a story
that is `ready` here is never refused on Size by that claim.

## Golden cases

The cases in [ready_cases.json](../conformance/ready_cases.json) give an issue's body,
labels, Size and blocker graph, and the expected `verdict`, failed rules and open blockers.
Issues in a case are named by letter (`S` is the issue being checked); the runner gives
each a number and writes references into the body as `#N`, `owner/repo#N` or an issue URL.
Check R1 runs them offline against the runner's `reference_ready`, or against a server's
own logic through `--ready-cmd` ([runner](../conformance/README.md#testing-your-ready-check-offline)).
