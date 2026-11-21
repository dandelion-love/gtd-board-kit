# 17. Milestone handoff

An optional capability for one session to hand a **milestone** of an item to another
session (usually a reviewer, then back to the worker), so both can name the evidence, the
next actor and whether the handoff was received. It extends the claim, report, artifact
and signed-review records already in this spec; it replaces none of them and adds no second
issue-status system. A server that does not offer it works exactly as before.

This part of the page defines the record, the identifier, the delivery state and the
milestone head: what a handoff *is*, and what a verdict on it means.

## What already exists, and what this adds

| Existing | Stays | This capability adds |
| --- | --- | --- |
| `item_release` ([claim records](claim-records.md)) | The issue-level holder record: the holder lets go of the whole item and writes a [closing note](claim-records.md#the-closing-note). | Nothing. A milestone handoff is **not** a release: the sender keeps its claim, and a release neither creates nor settles a handoff. |
| `item_report` | Progress, the six states, attention. | Nothing. A report MAY link a handoff; it never stands for one. |
| Signed review ([sign-offs](sign-offs.md)) | The verdicts `looks-ready`, `needs-changes`, `needs-person`, the stages `plan` and `work`. | The `review` object MAY carry `milestone`, `revision` and `handoff`, which say what the verdict covers. |
| Issue artifacts | Evidence kept on the issue. | A handoff's `evidence` links may point at them. |
| [Notifications](notifications.md) | Pinging a **person** when a person must act. | Nothing: a handoff is agent to agent and never pings a person. |

A milestone handoff and an issue-level release are correlated only by the issue and the
time: the release's note SHOULD link the open handoff ids, and a handoff's `source` names
the issue. Next-read discovery of releases an issue holder left unheld belongs to the
claim records; this page does not implement it and does not assume it has shipped.
Likewise the mapping of a review verdict to the board's status is the board's rule, not
this page's.

## The record

A handoff is **one comment on the source issue** with a visible line, a sign-off (`act`
`handoff`) and one marker last:

```text
<!-- gtd-handoff v1 {...json...} -->
```

The JSON validates against [handoff.schema.json](schemas/milestone-handoff/handoff.schema.json)
(`x-version` 1). The marker is trusted only under a record author, as for claims
([which comments count](claim-records.md#which-comments-count)); a marker in any other
comment is conversation. `v` is 1; another `v` is not a record to a version-1 reader.

| Field | Holds |
| --- | --- |
| `handoff_id` | the durable identifier: `hf_` and a 26-character ULID the server mints; never reused |
| `source` | `{repo, issue}`: the issue the handoff is about |
| `milestone` | a short name for the stage (`^[a-z0-9][a-z0-9._-]{0,63}$`), e.g. `plan-review` or `parser-work` |
| `revision` | the **immutable evidence revision**: a 40-hex commit or a `sha256:` digest. A branch name, a tag or a PR number is not one |
| `action` | the one requested action: `review-plan`, `review-work`, `address-findings`, `answer-question` or `continue-work` |
| `request` | one concrete sentence or two saying what the recipient does (at most 1200 characters) |
| `evidence` | up to ten `https` links: the PR, the run, the artifact |
| `sender` | `{principal, session, role}`: verified by the server, never an argument |
| `recipient` | `{role, principal?}`: the role that is asked, and optionally one named principal |
| `scope` | `{repo, item, purpose}`: the [authorization scope](#authority), the item and whether the recipient is asked to `work` or to `review` it |
| `t` | the server's clock, UTC, when it wrote the record |
| `supersedes` | the `handoff_id` this one replaces, or null for the first on its milestone |

Worked examples, both valid: a worker asks a reviewer (`action` `review-work`, `scope.purpose`
`review`), and the reviewer hands findings back (`action` `address-findings`,
`recipient` the worker, `scope.purpose` `work`). Both are in
[handoff_cases.json](../conformance/handoff_cases.json), group `records`, with the invalid
cases that fix each rule (no revision, a branch name, an unknown action, a field outside the
schema such as an endpoint).

`handoff_id` is the only identifier other records use. The revision is part of the record
and never edited: new evidence is a new handoff that supersedes.

## The authoritative milestone head

For each `(source issue, milestone)` there is one **head**: the handoff whose `revision` is
the current evidence. It is a fold over the handoff records in ascending comment id:

- the first handoff on a milestone (`supersedes` null) becomes the head;
- a later handoff is accepted only if its `supersedes` equals the current head's
  `handoff_id` **and** its `revision` differs; it then becomes the head, and the old one is
  **superseded**;
- otherwise it is refused: `stale-base` (it names no head, or an old one),
  `same-revision`, or `unknown-supersedes` (it names a handoff that is not the head of this
  milestone). A refused handoff is not a record.

Who may create a successor: the sender's own principal, or the item's owner. Creation is
**optimistic and concurrency-safe the way a claim is**
([claiming safely](claim-records.md#claiming-safely-without-a-lock)): post, fold again, and if
the posted handoff is not the head's winner, delete the comment and refuse naming the head.
Milestones are independent: a handoff on one never moves another's head.

## Delivery, verdict and completion are three things

| Thing | Lives in | Answers |
| --- | --- | --- |
| **Delivery state** | the handoff's delivery fold (below) | did the recipient session get and acknowledge this handoff? |
| **Verdict** | the signed review comment (existing) | what did the reviewer decide about a particular revision? |
| **Completion** | the issue (closed, released, done) | is the whole item finished? |

None implies another. A delivered or acknowledged handoff says nothing about the work; a
verdict says nothing about delivery; a verdict on a milestone does not complete the item.

### Delivery state

A handoff has one delivery state: `pending` (written, not yet delivered), `delivered` (the
transport reports the recipient session was reached), `acknowledged` (the recipient
acknowledged), `failed` (terminal: delivery gave up) or `cancelled` (terminal). Events:

| From | Event | To | Notes |
| --- | --- | --- | --- |
| (none) | `handoff` written | `pending` | |
| `pending` | `deliver` | `delivered` | transport success, **not** receipt or work |
| `pending`, `delivered` | `ack` | `acknowledged` | the recipient acknowledges; a lost `deliver` does not block it |
| `pending` | `fail` | `failed` | delivery gave up after its bounded retries |
| `pending`, `delivered` | `cancel` | `cancelled` | by the sender or the owner |
| `acknowledged`, `failed`, `cancelled` | any other event | unchanged | refused, or ignored when it repeats the one that got it there |

**A handoff that is superseded keeps its delivery state.** Supersession is a fact about the
milestone head, not a delivery state: an old handoff stays `delivered` or `acknowledged` and
is marked `superseded_by` the new head. A message already in flight cannot be recalled; it
is simply stale, and a stale handoff authorizes nothing ([authority](#authority)).

### The verdict names the milestone and the revision

A review verdict that is meant to settle a milestone carries, in its sign-off `review`
object, `milestone`, `revision` and `handoff` (the head's `handoff_id` it was written
against), beside the existing `stage` and `verdict`. A verdict that names no milestone, or
no revision, covers none, and a server acting on it refuses `missing-milestone` or
`missing-revision`.

**A verdict is effective only if, at the moment a server acts on it (authorization), a
concurrency-safe check finds its `handoff` and `revision` still the head's.** The check
reads the comments in order, folds the head, compares, and then acts; it then folds once
more and, if the head has moved, withdraws what it did (the claim fold's own
post-then-recheck). So:

- accepting revision A **cannot** authorize revision B: the verdict names A, the head says B,
  the answer is `stale-revision`;
- a supersession that lands before the check wins over an old verdict; a supersession that
  lands after leaves an earlier authorization standing for its own revision only, never for
  the new one;
- there is no verdict-without-handoff: `no-handoff`.

The golden cases `verdict-old-revision` and `verdict-race-supersede`
([handoff_cases.json](../conformance/handoff_cases.json), group `head`) fix these, including a
supersession racing an old verdict. The reference is [handoff.py](../conformance/handoff.py).

### Authority

A delivery or an acknowledgement **grants no authority**: not a claim, not a review. The
recipient still claims before working (`item_claim`, `purpose` `review` for a review), and
self-review stays forbidden ([review claims](tools.md#claims-and-reports)): the claim
refuses a `session` equal to the worker's. A comment, a role name or a handoff naming a
role is not authority either. `scope` records what the sender asked and is checked against
the recipient's claim (`scope.item` is the claimed item; `scope.purpose` equals the claim's
`purpose`); a mismatch refuses the work, it never widens a claim.
