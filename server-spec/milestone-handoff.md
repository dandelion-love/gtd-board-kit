# 17. Milestone handoff

An optional capability for one session to hand a **milestone** of an item to another
session (usually a reviewer, then back to the worker), so both can name the evidence, the
next actor and whether the handoff was received. It extends the claim, report, artifact
and signed-review records already in this spec; it replaces none of them and adds no second
issue-status system. A server that does not offer it works exactly as before.

Reading order: this page defines the record, the identifier, the delivery state and the
milestone head (what a handoff *is*, and what a verdict on it means); then
[routing and delivery](#routing-and-delivery) (how it reaches a session);
[instructions and privacy](#instructions-and-privacy) (what agents do, and what this page
never contains); and [capability negotiation](#capability-negotiation) (how an agent finds
out whether a server offers it).

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

A handoff whose `action` is `address-findings` lives on its own milestone, the reviewed
milestone's name plus the suffix `-findings` (`m1` reviewed, findings on `m1-findings`), so a
findings handoff has a head of its own and never fights the evidence head. The pair is
enforced: `address-findings` on any other milestone is refused `findings-milestone`, and any
other action on a `-findings` milestone is refused `reserved-suffix`. A full round trip
(review `m1`, findings on `m1-findings`, a new revision of `m1` superseding the first, a
second review) is the case `findings-round-trip`.

Who may create a successor: the sender's own principal, or the item's owner. Creation is
**optimistic and concurrency-safe the way a claim is**
([claiming safely](claim-records.md#claiming-safely-without-a-lock)): post, fold again, and if
the posted handoff is not the head's winner, delete the comment and refuse naming the head.
A server that deletes the losing comment MUST log its comment id (or leave a tombstone
comment naming it) so that a later reader can tell a withdrawn handoff from a missing one.
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
- there is no verdict-without-handoff: `no-handoff`;
- the verdict's author must be the handoff's recipient (the named principal, or a principal
  the role is granted to) **and** hold a live review claim for that handoff, otherwise it is
  never effective: `unauthorized-author`, `no-review-claim`.

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

**A review claim beside a work claim.** A reviewer must be able to claim review while the
worker still holds the item, or the review the handoff asks for could never start. So a
`purpose` `review` claim is accepted next to a live work claim only when it names (`handoff`)
the head handoff of a milestone, that handoff asks for a review and its recipient is the
caller, and the caller's session differs from the holder's (otherwise `self-review`). It is a
separate, scoped claim: it takes nothing from the holder, it covers only that handoff's
milestone and purpose, it ends on its own lease or release, and the holder's claim, lease and
interruption count are unchanged. A review claim naming no handoff, a superseded one or a
handoff addressed to someone else is refused (`held`, `stale-handoff`, `not-recipient`). The
holder and a reviewer with a live review claim for the handoff may `handoff_send`. The cases
in group `claims` fold these claims.

## Routing and delivery

### Bindings

A handoff names a **role**, and a role is not a place. A **binding** connects an authorized
principal in a role to a runtime **session** the server can reach: `{binding_id, principal,
role, session, created_by, created_at, expires_at, revoked_at}`. The binding holds a
session **name** only: never an address, URL or credential ([privacy](#instructions-and-privacy)).

| Act | Who may | Rule |
| --- | --- | --- |
| Create | the principal, for **its own** session | the role is `worker` and the principal already took part in the item (it holds or held a claim, or wrote a report or handoff on it), or the owner granted that principal the role in the repo's context (`handoff.roles`, a map from role to principals); never `owner`; the call is authenticated, the principal comes from the token and never from an argument |
| Replace | the same principal | a new binding for the same principal and role revokes the old one at once |
| Revoke | the bound principal, or the owner | takes effect immediately; nobody else may revoke |
| Expire | the clock | every binding has `expires_at`, at most 24 hours after creation (default 8); rebinding is how it is extended |

An expired or revoked binding is not a route. A server MAY keep bindings in any store; it
MUST be able to list them to the owner and to the bound principal (`handoff_bindings`).

**Resolving a role.** Given the handoff's `recipient`, the server takes the active bindings
(not revoked, not expired) of principals authorized for the role, limited to the named
principal if the handoff names one:

- a `worker` binding counts only for a principal granted the role or one that took part in
  the item; a stranger's binding is not a route;
- none: `no-binding`; the handoff stays `pending`, and polling still reaches it;
- more than one distinct principal and none named: `ambiguous-recipient`; the sender names
  one;
- a review whose binding's session equals the sender's: `self-review`; it is never routed.

A binding routes a message. It grants **nothing else**: a claim is still needed before work
([authority](#authority)), a comment or a role name alone grants no authority, and
self-review stays forbidden. The cases `route-*`, `bind-*`, `revoke-*` and `work-*`
([handoff_cases.json](../conformance/handoff_cases.json)) fix all of this, including the
rejection of unauthorized routing, self-review and an expired or revoked binding.

### Delivery

- **At least once.** The server tries to reach the recipient session until it records
  `deliver` or runs out of attempts. A recipient MUST treat a repeat as the same handoff.
- **A stable deduplication key.** `delivery_id` is `dl_` and the first 16 hex characters of
  the SHA-256 of `handoff_id|revision|recipient_principal`: the same on every retry, a new
  one for a new revision or another recipient. Every message carries it.
- **Acknowledgement is idempotent and bound.** `handoff_ack` names the `delivery_id`, the
  `revision` and the caller's principal; it is accepted only when the caller is the
  recipient (the named principal, or the one the role resolved to) **and**, in push mode,
  holds an active binding. In poll mode there are no bindings, so the caller must instead be
  a principal the role is granted to (`role-not-granted` otherwise). Another principal, or a
  revoked or expired binding in push mode, is refused
  (`wrong-recipient`, `revoked-binding`); a wrong id or revision is refused
  (`delivery-mismatch`, `revision-mismatch`). The same acknowledgement again returns
  `unchanged` and changes nothing, so a lost acknowledgement is safely repeated.
- **After supersession.** An acknowledgement that arrives after the handoff was superseded
  is **recorded**, because the recipient did receive it, but marked `stale` with the head
  named; it authorizes nothing, and the recipient reads the new head before it acts. A
  repeat of an old acknowledgement is `unchanged`.
- **Bounded retry.** At most `max_attempts` (default 5) attempts; attempt *k+1* follows
  attempt *k* after a delay that starts at one minute, doubles and stops growing at thirty
  (offsets 0, 1, 3, 7 and 15 minutes for five attempts).
- **Escalation.** When the attempts are used up with no delivery, the server records `fail`
  (terminal) and escalates once: an ordinary ask on the source issue (the `needs:` label for
  the profile's `owner_needs`, with the one-line question "handoff `<id>` could not be
  delivered to `<role>`"), which is the existing way a person is told when a person must act
  ([notifications](notifications.md)). A handoff delivered but not acknowledged within
  `ack_within` (default 24 hours) reads `overdue` in `handoff_list`; its state does not
  change.
- **In flight.** A message already sent cannot be unsent. Cancelling or superseding stops
  further attempts and marks the record; a recipient that gets a stale or cancelled message
  reads `handoff_get` and finds the state and the head. **A stale message authorizes no
  work.**
- **Transport success is not receipt, and receipt is not completion.** `deliver` only says the
  transport reached a session; only `ack` says the recipient took it; the work is complete
  only when the item says so.

The cases `deliver-*`, `ack-*`, `lost-ack`, `failed-exhausted`, `cancel-*`, `retry-*` and
`dedupe-*` fix the states, including a duplicate delivery, a lost acknowledgement, a failed
delivery and an acknowledgement after supersession.

### Tools

The optional **Milestone handoff** group ([tools](tools.md#optional-groups)). `repo` and
`number` name the source issue; none of these takes an identity argument.

| Tool | Class | Arguments | Returns |
| --- | --- | --- | --- |
| `handoff_send` | work | `repo`, `number`, `milestone`, `revision`, `action`, `request`, `recipient_role`, `recipient_principal?`, `evidence?`, `supersedes?`, `session?` | the record, `handoff_id`, `delivery_id`, `state`, `head`, `route` (`bound` or the refusal rule), `warnings` |
| `handoff_get` | read | `repo`, `handoff_id` | the record, `state`, `superseded_by`, `head` (the milestone's current `{handoff_id, revision}`), `stale`, `verdicts` (each `{url, verdict, revision, effective}`) |
| `handoff_list` | read | `repo`, `number?`, `role?`, `state?`, `since?`, `limit?`, `cursor?` | handoffs with `state`, `overdue`, `stale`; for a recipient to poll |
| `handoff_ack` | work | `repo`, `handoff_id`, `delivery_id`, `revision`, `session?` | `state`, `unchanged`, `stale`, `head` |
| `handoff_cancel` | work | `repo`, `handoff_id`, `reason?` | `state` |
| `handoff_bind` | work | `role`, `session`, `expires_in?` (at most `24h`) | the binding |
| `handoff_unbind` | work | `binding_id` | the binding, revoked |
| `handoff_bindings` | read | `principal?` | the caller's bindings (the owner sees all) |

`issue_comment` takes the three optional `review_milestone`, `review_revision` and
`review_handoff` of [sign-offs](sign-offs.md#review-verdicts) on this capability; they are
refused unless all three are given and the revision is a commit or digest.

`handoff_send` refuses: a caller who holds no claim on the item (a worker's `purpose` `work`
claim, or a reviewer's `review` claim: the sender must be the item's current holder); a
pull request or a closed issue; a `revision` that is not a commit or digest; a refused head
(`stale-base`, `same-revision`, `unknown-supersedes`); a recipient routed to the sender's own
session (`self-review`); a `request` holding a record, `gtd-pr`, sign-off or handoff marker.
A refused send writes nothing. `no-binding` is **not** a refusal: the handoff is written
`pending` and retried.

## Instructions and privacy

### What an agent does

The agent-facing form of this section is the model page
[milestone handoff](../knowledge/model/milestone-handoff.md) and the instructions in the
`board-report` and `board-review` skills. The contract they follow:

- **A compact packet, one next action.** A handoff carries a packet of at most 1200
  characters: the milestone, the immutable revision, links to the evidence (never pasted
  logs), and **one** concrete requested action from the fixed set. A handoff that asks for
  two things is two handoffs.
- **Independent work continues.** While a milestone waits, the sender keeps working on
  anything else it is authorized and claimed for, and does not hold its lease idle. A
  `waiting` report is for a sender with nothing else to do.
- **The recipient claims first.** A reviewer claims the item (`purpose` `review`) before it
  reviews, reads `handoff_get` to confirm the handoff is the head and not stale, and writes a
  verdict that names the milestone and the revision. A verdict that cannot name them is not
  written.
- **A new revision is a new handoff** that supersedes the old; the sender never edits a
  revision.
- **Never claim a wake-up the server did not promise.** Without the push capability a
  release, a report or a comment does not wake a session; the sender says delivery is
  manual or polled and tells its person.

### Legacy servers

A server without the capability stays fully usable. The sender writes the same packet as a
signed comment on the issue (`issue_comment`), links it from a report, and says delivery is
**manual**. The recipient finds it by polling: `activity_since` on the items it holds,
`list_next_actions` with the `agent-review` label, or `handoff_list` where only polling is
offered. Nothing in this page changes how a legacy server behaves.

### Privacy and the public kit

- **No runtime-specific detail.** The record, the schema, the tools, the fixtures and the
  instructions name no endpoint, host, port, webhook, queue, chat product or deployment. How
  a server reaches a bound session is its own business; a binding holds a session **name**.
  Conformance check MH8 and the public guard read these files for it.
- **Agent delivery is not human notification.** A handoff never pings a person and no
  handoff tool appears in [notifications](notifications.md). When a person must act (a
  handoff that could not be delivered), the existing ask and its ping rules apply
  unchanged. A change to who is pinged, or when, is out of scope here.
- **Out of scope**: a delivery daemon, model scheduling, new chats, automatic promotion or
  merge, and any scientific or product acceptance policy.

## Capability negotiation

A server says it offers the capability in the `capabilities` list of `whoami` and of the
well-known document ([transport and identity](transport-and-identity.md#whoami)):

| Name | Means | Needs these tools |
| --- | --- | --- |
| `milestone-handoff:1` | records, state, head, verdicts and polling | `handoff_send`, `handoff_get`, `handoff_list`, `handoff_ack`, `handoff_cancel` |
| `milestone-handoff-push:1` | the server also delivers to bound sessions | the five above and `handoff_bind`, `handoff_unbind`, `handoff_bindings` |

An agent trusts the **name** and checks the **tools** that must back it, then picks a mode:

| Mode | When | What the agent does |
| --- | --- | --- |
| `push` | both names, all eight tools | send; the server delivers to a bound session; the recipient may poll too |
| `poll` | `milestone-handoff:1` and its five tools, no push | send; tell the recipient's person or lane; the recipient polls `handoff_list` |
| `manual` | anything else: no name, a missing tool, or a version it does not know | post the packet as a signed comment, say delivery is manual |

Tools without the name are not trusted, and a name without its tools falls back, so a
half-built server never makes an agent believe a handoff was delivered. A server that lists
either name while a required tool is missing fails MH7. Examples (the `negotiation` cases):
a legacy server with only `item_get` and `issue_comment` gives `manual`; a server with the
five tools and `milestone-handoff:1` gives `poll`; adding the push name and the binding tools
gives `push`; `milestone-handoff:2` alone gives `manual`.

