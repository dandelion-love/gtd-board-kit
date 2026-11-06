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
| `claim` | `item_claim` | `lease_until`, `takeover_of` (principal or null), `mandate` |
| `renew` | `item_renew` | `lease_until` |
| `release` | `item_release` | `done`, `remaining`, `next`, `handoff_to` (principal, role, `any`, or null) |
| `report` | `item_report` | `state` (or null), `note`, `attention` (or null), `needs` (when `attention`), `links` |

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

## The fold

Walk record comments in ascending comment id (GitHub assigns ids in creation order). Keep
`holder`, `lease_until`, `claim_id`, `mandate`, `handoff_to`, `last_report`, `last_note`,
`attention`.

| Record | Effect |
| --- | --- |
| `claim` | If there is no holder, or the record's `takeover_of` equals the holder **and** the holder's `lease_until` is before this record's time: the record's `by` becomes holder; take its lease, id, mandate; clear `handoff_to` and `last_report`. Otherwise it is a **lost claim** (listed, no effect) |
| `renew` | If `by` is the holder: `lease_until` takes the record's value |
| `release` | If `by` is the holder: clear holder, lease, claim, mandate, last report; `handoff_to` takes the record's value |
| `report` | `attention` becomes this record's question (or clears, if it has none). If `by` is the holder and `state` is set: `last_report` and `last_note` take its values; `dropped` then releases as above |

After the walk:

- `stale` is true when there is a holder and `lease_until` is in the past.
- `follow_ups` are non-record comments newer than the holder's latest record other than
  a `renew`. A renew is a heartbeat, not a reply, so it never hides a comment the holder
  has not answered.

`item_get` returns at least: `holder`, `lease_until`, `stale`, `mandate`, `handoff_to`,
`last_report`, `last_note`, `attention` (`{question, by, url}` or null), `lost_claims`,
`follow_ups` (`{author, url}`), `open_blockers`, and the issue's `number`, `title`, `url`,
`state`.

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
