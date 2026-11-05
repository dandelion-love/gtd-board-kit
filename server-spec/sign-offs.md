# 12. Sign-offs

Everything a server writes on GitHub for a caller appears under the server's one
identity (an App or one person), so GitHub's author line cannot say which agent wrote a
comment, in which role, or in which session. A **sign-off** says it: a short visible line
a person reads, and one machine-readable marker a script or a search finds. The server
writes it; the caller never does.

## What carries one

| Write | Tool | `act` |
| --- | --- | --- |
| A comment on an issue or PR | `issue_comment` | `comment`, or `review` when the call carries a review verdict |
| A claim record | `item_claim`, `item_renew`, `item_release`, `item_report` | `claim`, `renew`, `release`, `report` |
| A pull request body | `pr_open` (when offered) | `pr` |
| A pull request review, and each inline comment it posts | `pr_review` (when offered) | `pr-review` |
| A reply on a pull request's review thread | `pr_review_reply` (when offered) | `pr-reply` |
| A ping comment | `item_report` (Notifications group, [notifications](notifications.md)) | `ping` |
| A comment from an optional tool (a channel post, a run-state event, ...) | that tool | a name the server chooses, lower case with hyphens (`channel`, `run-state`) |

The `issue_comment`, claim and `pr_open` rows are required (Core, and PR4 when `pr_open`
is offered), and so are the `pr_review` and `pr_review_reply` rows wherever those tools
are offered (PR5 to PR9); any other optional tool SHOULD sign the same way. A
review's inline comments show on GitHub apart from its body, so each one carries its own
sign-off, with the review's `act`, role and session. An issue artifact is **not** signed:
its body is the content itself (a `link` body must stay one URL). The `report` that names the artifact is signed. Text a server writes for
itself, not for a caller (a board status update, a sync's comment), MAY carry a sign-off
whose `by` is the server's own name.

## Format

The sign-off is a rule, one visible line, then the marker:

```text
---
<sub>gtd-sign · agent:example · reviewer · review · session review-7 · 2026-01-01T12:00:00Z</sub>

<!-- gtd-sign v1 {"act": "review", "by": "agent:example", "review": {"stage": "work", "verdict": "needs-changes"}, "role": "reviewer", "session": "review-7", "t": "2026-01-01T12:00:00Z", "v": 1} -->
```

- The marker is exactly `<!-- gtd-sign v1 <json> -->`, encoded as a
  [record's](claim-records.md#record-format) (sorted keys, `<` and `>` escaped).
  A body with zero sign-off markers, more than one, another version or invalid JSON is
  **unsigned**.
- The sign-off is the last thing in the body, except a record marker (`gtd-desk`) or a
  `gtd-pr` marker, which stays last: the sign-off sits just above it.
- The visible line starts with the word `gtd-sign`, then the principal, the role and the
  act, then `session <name>` when there is one, then `t`. It is for people and for
  search; readers use only the JSON.

### Fields

| Field | Required | Value |
| --- | --- | --- |
| `v` | yes | `1` |
| `by` | yes | The principal the server verified ([transport and identity](transport-and-identity.md)): `agent:<name>`, `<idp>:<id>` (a person, for example `github:<login>`), or `local:<name>` on stdio. Never a tool argument |
| `role` | yes | One of the roles below |
| `act` | yes | From the table above |
| `t` | yes | UTC, `YYYY-MM-DDTHH:MM:SSZ`, the server's clock |
| `session` | no | The caller's own name for its session, at most 200 characters. Stated by the caller, not verified: it tells two sessions of one agent apart, it is not identity |
| `review` | only when `act` is `review` | `{"stage": <stage>, "verdict": <verdict>}` |

### Roles

| `role` | Who | Default when |
| --- | --- | --- |
| `worker` | Does the item: builds, writes, reports progress | an agent's call names no role and holds no review claim |
| `reviewer` | Checks work another session did | the caller's live claim on the item has `purpose` `review` |
| `coordinator` | Points, splits or hands work to others; runs a lane | never a default; the caller names it |
| `owner` | A person deciding: approves, answers, accepts | the caller is a person (not `agent:` or `local:`) |

An agent principal may not sign as `owner`: the call refuses. An unknown role refuses and
lists the four.

### Review verdicts

`issue_comment` takes `review_stage` and `review_verdict` together (one without the other
refuses). They name the [review](tools.md#review-requests) stage and its outcome:

| `review_stage` | Means | | `review_verdict` | Visible as |
| --- | --- | --- | --- | --- |
| `plan` | No PR yet: is it ready to build? | | `looks-ready` | `Looks ready` |
| `work` | A PR exists: is the work done? | | `needs-changes` | `Needs changes` |
| | | | `needs-person` | `Needs a person` |

- A review sign-off needs the caller's **live review claim** on the issue (`item_claim`
  with `purpose="review"`); without one the call refuses. So the rule that no session
  reviews work it did holds on the verdict as well as on the claim.
- The sign-off's `session` is the review claim's. A `session` argument that differs
  refuses, so a verdict is never attributed to the session that worked the item.
- The role is `reviewer`; any other `role` with a verdict refuses.
- The body's first line is the verdict line, `<Stage> review: <Verdict>` (for example
  `Work review: Needs changes`). When the caller's first line is not already that, the
  server writes it above the body.

### Session on records

An `item_*` record's sign-off carries the `session` of the caller's live claim
(`mandate.session`), so every record of a claim names its session without the caller
repeating it.

## Trust and forgery

- `issue_comment`, `pr_open`, `pr_review`, `pr_review_reply`, the issue artifact tools
  and every optional tool that posts a caller's text refuse a body that holds a sign-off marker, naming `gtd-sign`. Only the
  server writes one.
- A reader trusts a sign-off only on a comment whose GitHub author is the server's
  identity: the same record authors as [C10](conformance.md#claims-core). A sign-off
  pasted by anyone else is text.
- A person's own comment on GitHub needs no sign-off: its GitHub author is the person.

## Pull request writes

A comment on a PR (`issue_comment` with a PR's number), a review (`pr_review`) and a
review-thread reply (`pr_review_reply`) are signed exactly as above, with these rules on
top. They hold for every server that offers `pr_open`, `pr_review` or `pr_review_reply`.

- **Identity.** The server writes them with the same App credential `pr_open` uses, never
  under the account of a person it may act for, even on a server that otherwise acts as
  the caller. A server whose own identity is already not a person (an App installation in
  server mode) may use it. If no such identity is available, the write fails without
  posting: it never falls back to a person's account. So the owner's approval is never
  their own, a reader can trust the sign-off ([trust and forgery](#trust-and-forgery)),
  and a mention in it reaches the person ([notifications](notifications.md)).
- **Authorization first.** The server checks the repo and the caller exactly as it does
  for an issue write (P5, the caller's access in user mode) **before** it uses its App
  credential for any read or write. The App's wider rights never widen the caller's: a
  denied caller causes no App call, and a refusal quotes nothing from a PR the caller may
  not read.
- **Role default.** With no `role` argument, the role follows the caller's claims on the
  issues the PR's `gtd-pr` marker names: `reviewer` under a live review claim on any of
  them, else `worker` under a live work claim, else the ordinary default (`worker` for an
  agent, `owner` for a person). Only a single valid `gtd-pr` marker in a PR body whose
  GitHub author is the server's own identity selects those claims. A forged marker (any
  other author), a malformed one, or an issue the server cannot read gives the ordinary
  default; it never raises the role.
- **No verdict on a PR.** A review verdict (`review_stage`, `review_verdict`) goes on the
  issue under a review claim, never on a PR: `issue_comment` refuses one on a PR number.
  A `pr_review` is a code review, not a board verdict.

## Results

Every signed write returns `signoff`, the marker's JSON as an object. `issue_comment`
also returns the posted `body` and the comment's `url`.

## Finding who said what

[Who said what](../knowledge/model/who-said-what.md) has the search recipes and the
reader's rules.
