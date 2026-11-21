# 05. Claim records and the fold

Claims, renewals, releases and reports are **comments on the issue**. Each carries one
machine-readable record. The state of an item (who holds it, until when, why, what they
last said, what they asked) is a **fold** of those records in order. Every server that
writes records in this format and folds them by these rules agrees with every other, so
two servers, or a server and a script, can share a repo.

Why comments: on GitHub every write a server makes appears as the server's one identity
(an App or one person), so an assignee or an author cannot tell two agents apart. The
record carries the principal the server verified.

## Record format

A record comment is human-readable Markdown with one marker at the end:

```text
### Claimed

| Field | Value |
|---|---|
| by | agent:example |
| lease_until | 2026-01-01T14:00:00Z |
| mandate.asked_by | coordinator |
| mandate.basis | explicit |

<!-- gtd-desk v1 {"by": "agent:example", "event": "claim", "lease_until": "2026-01-01T14:00:00Z", "mandate": {...}, "t": "2026-01-01T12:00:00Z", "v": 1} -->
```

- The marker is exactly `<!-- gtd-desk v1 <json> -->`. A comment with zero markers, more
  than one, another version, invalid JSON, or an unknown `event` is **not a record**; it is
  conversation (a follow-up for the holder).
- In the JSON, `<` and `>` are written as `<` and `>` so the HTML comment cannot
  be closed early. Keys are sorted; that keeps records diff-friendly and is not required for
  parsing.
- The table above the marker is for people. Readers use only the JSON. Cell text escapes
  `&`, `<`, `>` and `|`.
- Every record has `v` (1), `event`, `by` (the verified principal) and `t` (UTC,
  `YYYY-MM-DDTHH:MM:SSZ`, the server's clock when it wrote).
- Free text fields are capped (4000 characters for notes, 200 for short fields like
  `asked_by`, 500 for links); the server refuses longer input rather than truncating.

## Events

| `event` | Written by tool | Fields beyond `v`, `by`, `t` |
| --- | --- | --- |
| `claim` | `item_claim` | `lease_until`, `takeover_of` (principal or null), `mandate`, `interruptions?` (informational, below) |
| `renew` | `item_renew` | `lease_until` |
| `release` | `item_release` | the [closing note](#the-closing-note) parts `done`, `left`, `decided`, `set_aside`; `remaining` (the old name of `left`), `next`, `handoff_to` (principal, role, `any`, or null) |
| `report` | `item_report` | `state` (or null), `note`, `attention` (or null), `needs` (when `attention`), `links`, optionally the four closing note parts, `answering?` (the comment id of the attention it answers, with `note` the person's words), `decision?` (`retry` or `hold`, with `answering`), and on an [interruption question](#the-interruption-limit) `escalation` and `count` |
| `stop` | `item_stop` | `wind_down_until`, `reason?` |
| `stop_clear` | `item_stop_clear` | `note?` |

`mandate` is:

```json
{
  "asked_by": "who pointed the agent at it (or the agent itself for inferred)",
  "basis": "explicit | inferred",
  "rule": "agent-ready for an inferred pickup, a lane name in a lane, else null",
  "policy_version": "the lane's policy version, or null",
  "pointed_in": "a link to where the agent was pointed, or null",
  "branch": "the branch the holder's commits for this item land on, or null",
  "purpose": "work | review",
  "session": "the caller's own name for its session, or null",
  "scope": {"repo": "owner/repo", "item": 0, "title": "...", "body_sha256": "first 16 hex"}
}
```

`scope` fixes what was claimed: the item as it read at claim time. Wider work is a new
item ([claims and leases](../knowledge/model/claims-and-leases.md)).

`branch` is optional and only recorded: a fold does not use it. A record written before
the field existed has no `branch`; readers treat a missing key as null.

`purpose` and `session` are recorded the same way: a fold does not use them, a missing
`purpose` reads as `work` and a missing `session` as null. `item_claim` reads them from
earlier records to refuse a review by the session that worked the item
([review claims](tools.md#claims-and-reports)).

## The closing note

A holder who lets go, or who is asked to wind down, leaves a **closing note** of four
short parts, so the next worker (and the owner) read what happened without the
transcript:

| Part | Holds |
| --- | --- |
| `done` | what was finished, with links to the proof |
| `left` | what remains to do |
| `decided` | choices made on the way, each with how to undo it |
| `set_aside` | what was considered and deliberately not done, and why |

A `release` record carries them, and an `item_report` record may carry them (a worker
that reports a checkpoint leaves a note even if its lease later runs out). They are
**optional for one release**: a record without them is valid, so a client in the old form
(`done`, `remaining`, `next`) keeps working. `remaining` is an **alias of `left`**: a
reader takes `left` when it is present and non-empty, else `remaining`; a writer given
both with different non-empty values refuses; a record may hold either. A server writes
both keys with the same value, so a reader that predates `left` still sees it.

Reading a note, an empty or missing part reads `none`. When no note exists at all, every
part reads `none recorded` (the item still opens). A release or report that carries none
of the four parts is accepted with a warning that names the four.

## Interruptions

An **interruption** is counted for each lease that ended without its holder letting go: a
takeover of it, or a lease that has run out and is still held. **Never twice for one
lease**: a takeover is how a stale lease stops being stale, so the same lease moves from
one reading to the other. A release, a `dropped` report and a fresh claim after a release
(a handoff) are not interruptions. The count is a pure fold of the records:

```
interruptions = (valid takeover claims) + (1 if the holder's lease has run out)
```

**The count is not monotonic.** The `+1` is a reading of the clock. A holder whose lease
lapsed and who then renews (the fold lets the holder renew) is live again, and the count
falls by that one. Takeovers never fall.

The fold also keeps `previous_holder`: the holder a valid takeover replaced, or the one
who last released; never cleared by a later claim. A `claim` record MAY carry
`interruptions` (the count including that takeover) for a person reading the comment; a
reader recomputes it and never trusts the stored value.

**The last worker's note.** The note a new worker reads, `closing_note`, belongs to the
**most recent lease that ended**: the stale holder's own latest parts while it is stale;
the replaced holder's parts after a takeover; the releasing holder's parts after a
release (parts on the release, else the latest parts it reported). `closing_note.by` names
that worker. A worker that recorded nothing leaves `none recorded`, never an earlier
worker's note, so a reader is never told something the last worker did not say. A lease
in progress shows the note of the lease before it, until it ends.

## The interruption limit

An item that keeps being interrupted can bounce between workers unseen, so the count above
has a limit. The **default limit is 3**; a deployment may set another whole number from 1,
and `item_get` returns it as `interruption_limit`. The count is the `interruptions` of the
fold, counted from the item's latest retry (below).

**Reaching it.** A claim (not a renew) on an open item whose `interruptions` is at or above
the limit, with no escalation yet, posts **one** `report` record and then refuses with
`interruption-limit`, naming the question. The record carries `attention` (a question that
gives the count and lists `retry` and `hold` as options), `needs` (the owner's value of the
repo's profile), `escalation` `interruptions` and `count`. It is written under the
principal that made the claim, so the sign-off names who triggered it. A server in the
[Notifications](notifications.md) group pings once, as for any ask.

**Waiting.** While the escalation is open or was answered without a retry, the item is not
offered: every claim refuses `interruption-limit` and writes nothing, so the question is
never repeated, and an unpointed pickup already refuses it because of its `needs:*` label.

**Answering.** The owner answers with `item_report` `answering` (the escalation's comment
id) and `decision`. `retry` resets the count to zero from that record and clears the
escalation: the item is offered again. Any other answer (`hold`, or none) leaves the
escalation `held`, and the item waits; a later `retry` naming the same comment id releases
it. That `retry` is the one exception to the rule that `answering` must name the open
attention: the answer closed the attention, so the server accepts `decision` `retry` naming
the item's held `escalation.comment_id`, and refuses any other `answering` of a closed
question, and a second `retry` once the escalation is cleared. The fold keeps `interruptions` from the latest `retry` on, and returns `escalation`
(`{state, comment_id, count}`, state `asked` or `held`) or null.

The record is the reporter's quote, as for any [answer](tools.md#claims-and-reports); the
server does not check that the person is the owner, so the `note` names who said it and
where.

## A stop

`stop` and `stop_clear` are written only by `item_stop` and `item_stop_clear` for a caller
the server has checked as the item's owner ([the stop signal](../knowledge/model/stop-signal.md)).
**The fold re-checks that**: it ignores a `stop` or `stop_clear` whose `by` is not the owner
or a principal the profile names as an owner, so a marker pasted into a comment by anyone
else is conversation, even where every record counts.
The fold keeps one **stop** while it is in effect: the first `stop` after the last
`stop_clear` (a later `stop` changes nothing). A stop in effect has a state:
`requested` while someone holds the item, and `at-rest` when nobody does (no worker, or
the holder released). It is **overdue** when a holder still holds the item after
`wind_down_until`. While a stop is in effect, a `claim` is lost (listed, no effect): the
item stays unclaimed until the owner clears the stop. The fold never revokes a holder:
`renew` still works in the fold, and only `item_renew` refuses past the limit.

## Several items, one branch

An agent may work one or more stories, and the session that owns them may combine them
on one integration branch. The record format does not change for that:

- **One record, one item.** A claim names exactly one item (`scope.item`). There is no
  record or tool that claims several items at once, and a server MUST NOT add one.
- **Each item has its own lease.** Renewing, releasing or reporting on one item never
  changes another, even when both name the same `branch`. A fold reads only its own
  issue's comments.
- **Every item worked is claimed.** Work for an item lands on a branch only while the
  committer holds that item's claim. Merging a branch someone else built into an
  integration branch is not working its items; a fix commit for an item on the
  integration branch is, so it needs that item's claim.

A server MAY define more events for its own tools (a coordination desk, say). Folds ignore
events they do not know.

## Which comments count

The operator MAY configure **record authors**: GitHub logins whose comments may carry
records (normally the server's own App bot). When configured, a record in a comment by
anyone else is ignored and treated as conversation, so nobody can forge a claim by pasting
a marker. When not configured, every record counts; a deployment should configure it
before more than one person or tool writes to its repos.

This holds for **every** record type (claims, releases, reports, stop, and the optional
records of other groups). A deployment with more than one writer MUST configure record
authors, and a server that offers the Stop group or enforces the intake check MUST: without
them any commenter could pose as a holder or an owner.


## The fold

Walk record comments in ascending comment id (GitHub assigns ids in creation order). Keep
`holder`, `lease_until`, `claim_id`, `mandate`, `handoff_to`, `last_report`, `last_note`,
`attention`.

| Record | Effect |
| --- | --- |
| `claim` | Unless a stop is in effect: if there is no holder, or the record's `takeover_of` equals the holder **and** the holder's `lease_until` is before this record's time: the record's `by` becomes holder; take its lease, id, mandate; clear `handoff_to` and `last_report`; a takeover also counts one interruption and sets `previous_holder`. Otherwise (or during a stop) it is a **lost claim** (listed, no effect) |
| `renew` | If `by` is the holder: `lease_until` takes the record's value |
| `release` | If `by` is the holder: clear holder, lease, claim, mandate, last report; `handoff_to` takes the record's value; the closing note and `previous_holder` are set |
| `report` | `attention` becomes this record's question (or clears, if it has none; a record with `answering` clears the attention it names and is kept as `answered`; `decision` `retry` restarts the interruption count; if the holder's report that asked it set `state`, `last_report` and `last_note` return to the values they had just before that report, unless a later holder report with `state` replaced them). If `by` is the holder and `state` is set: `last_report` and `last_note` take its values (the fold keeps the values they replace, for an `answering` record); `dropped` then releases as above. Closing note parts on a holder's report are kept for the lease |
| `stop`, `stop_clear` | `stop` starts a stop if none is in effect; `stop_clear` ends it |

After the walk:

- `stale` is true when there is a holder and `lease_until` is in the past.
- `follow_ups` are non-record comments newer than the holder's latest record other than
  a `renew`. A renew is a heartbeat, not a reply, so it never hides a comment the holder
  has not answered.

`item_get` returns at least: `holder`, `lease_until`, `stale`, `mandate`, `handoff_to`,
`last_report`, `last_note`, `attention` (`{question, by, url, comment_id}` or null), `lost_claims`,
`follow_ups` (`{author, url}`), `open_blockers`, and the issue's `number`, `title`, `url`,
`state`. A server that implements [the closing note](#the-closing-note),
[interruptions](#interruptions) and [a stop](#a-stop) also returns `interruptions` (a whole
number), `previous_holder` (a principal or null), `closing_note`
(`{by, done, left, decided, set_aside}`, each part a string, with `none` and `none recorded`
as above) and `stop` (`{state, by, at, wind_down_until, reason, overdue}`, or null).

## Claiming safely without a lock

GitHub has no compare-and-set on issues, so a claim is optimistic:

1. Fold. Refuse if someone else holds an unexpired lease, or the caller already holds it.
2. Post the claim record (with `takeover_of` when the lease has run out).
3. Fold again. If the winning claim is not the one just posted, **delete** the posted
   comment and refuse, naming the winner.

Every fold ignores a losing claim anyway, so a failed delete leaves noise, never a second
holder.

## Lease

Lease strings are `<n>m`, `<n>h` or `<n>d`. The maximum is 72 hours; a longer one is
refused. The default is `2h`. `lease_until` is the server's clock plus the lease.

## Mirror onto the board

When the call names a board (or the server has a default) and the server holds a board
credential, after each claim-tool write the server sets:

- `Agent`: the holder's runtime: for `agent:<name>`, the provider the agent joined with
  (or a runtime name found in `<name>`), else the name; `human` for any non-agent
  principal; cleared when nobody holds it;
- `Last report`: `<state>: <note>` of the latest holder report, at most 120 characters;
  cleared when there is none.

A failed board write is a **warning** in the result, never a failed tool call: the issue is
the record and the board is a view. The claim tools do **not** set Status and do not change
dispatch labels; the agent does that with `issue_labels`, and the bridge moves the card.
