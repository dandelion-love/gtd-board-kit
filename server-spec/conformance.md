# 08. Conformance

Each check has an id, a level, and a pass condition a test can assert. A server meets a
level when every check of that level and the levels below it passes. Run them against a
**fake GitHub** (an in-memory stand-in for issues, labels, comments and one board) so they
are fast and need no network or account; run the Join checks against the HTTP app in
process.

The kit ships a ready-to-run, black-box runner for these checks:
[conformance/](../conformance/README.md). It needs only Python and the server's URL, and
reports pass, fail, skip or manual for every id below.

## Transport and identity (Core)

| Id | Check |
| --- | --- |
| T0 | At the `full` preset (or the highest the caller has), `tools/list` includes every Core tool the kit calls (the Core rows of [tools](tools.md)); a server that lacks one does not claim Core in `whoami` |
| T1 | An unauthenticated `POST /mcp` gets `401` with a `WWW-Authenticate` header naming the protected resource metadata URL, and that URL serves RFC 9728 JSON with `resource` = `<mcp_url>/mcp` |
| T2 | `initialize`, `tools/list` and `tools/call whoami` work statelessly: three requests with no session id, each authenticated, each succeed |
| T3 | Every tool in `tools/list` has an input schema and an output schema; every call's structured content validates against its output schema |
| T4 | A connector identity not on the allowlist is refused |
| T5 | `whoami` returns every field in [transport-and-identity](transport-and-identity.md#whoami) |
| T6 | For each preset, `tools/list` shows exactly the tools whose class is at or below it; calling a hidden tool is refused with a message naming the preset it needs |
| T7 | No tool's input schema has a property used as identity (S1) |
| T8 | An unauthenticated `GET <mcp_url>/.well-known/gtd-board-kit` returns `200` JSON with `spec_version` (`MAJOR.MINOR.PATCH`), `conformance` (only level names from the [README](README.md#conformance-levels), and no other level without `Core`), `mcp` and `join_url`; with a token, its `spec_version` and `conformance` equal those `whoami` returns |
| T9 | The levels in `conformance` are honest: no check of a claimed level, or of a level below it, fails in the same run ([spec version and levels](transport-and-identity.md#spec-version-and-levels)). The run also reports which levels it makes claimable: those where the run covered every check of the level and of Core, and each passed, is manual, or does not apply (an optional entrance or tool group the server does not offer); a failed, skipped or unreached check keeps the level unclaimable |
| T10 | (manual, only when [person sign-in](transport-and-identity.md#person-sign-in-optional) is offered) With the switch off no person token is issued and every existing call behaves as before; with it on, a person token is refused on agent-only calls, an agent token is refused as a person, a cancelled sign-in or an unapproved account gets no token, and the token expires and can be revoked |

## Repo context and labels (Core)

| Id | Check |
| --- | --- |
| P1 | `profile_get` of every listed profile returns every field in [repo-context-and-profiles](repo-context-and-profiles.md#profiles), and every profile declares every base label |
| P2 | Every `needs` value has a matching `needs:*` label; `owner_needs` is one of them |
| P3 | Every profile's `status_for_label` maps `agent-running`, `waiting-for-review`, `agent-failed` and every `needs:*` label, and names only columns in `board.status` |
| P4 | `issue_labels` adds and removes a profile label and an `area:x` label; refuses a label outside the profile and lists the real ones; refuses adding `run-agent`; adds and removes `agent-review`; never changes Status |
| P5 | A repo or board outside the allowlist is refused before any GitHub call (the fake sees no request) |
| P6 | `list_next_actions` with a label returns only open issues with that label, never a PR. GitHub's label-filtered lists can lag a label write by seconds, so the runner re-reads for up to 30 seconds before failing |
| P7 | `project_items` returns items in the board's manual order and pages with a cursor |
| P8 | No profile declares a [retired Kind](repo-context-and-profiles.md#kinds): no `kind:task`, `kind:question` or `kind:decision` label, and, when `profile_get` returns `item_types`, no entry whose `name` or `issue_type` is `task`, `question` or `decision` (any case) |
| P9 | No profile declares a view whose `filter` uses a [deprecated qualifier](repo-context-and-profiles.md#view-filters) (`last-updated:`, any case) |
| P10 | If `issue_list` advertises `query`, a keyword search returns compact issue candidates and boolean `truncated` and `incomplete` flags plus `search_warning`; invalid or incompatible query arguments refuse. No result is required for a fresh issue because the index may lag. |

## Claims (Core)

| Id | Check |
| --- | --- |
| C1 | `item_claim` explicit without `asked_by` refuses; with it, posts one record whose JSON has `v`, `event=claim`, `by`=the caller's principal, `t`, `lease_until`, `mandate` with `scope.body_sha256` |
| C2 | A second caller's claim during the lease refuses and names the holder and the lease end |
| C3 | Race: two claims posted back to back by two callers; exactly one wins after both re-fold, and the loser's comment is deleted |
| C4 | After the lease ends, a new claim is a takeover: the record names `takeover_of` and the fold makes the new caller holder |
| C5 | `inferred` refuses without `agent-ready`; with `agent:<other runtime>`; with `agent:human`; with `needs:*`, `blocked` or `agent-proposed`; with a board Size outside `pickup_sizes` or none; and succeeds for `agent-ready` + `agent:any` + Size `S` |
| C6 | `item_renew`, `item_release` and a `state` report by a non-holder refuse |
| C6b | After a person closes a held issue, the holder's `item_release` succeeds and `item_claim` by anyone refuses |
| C7 | `item_release` in the old form (`done`, `remaining`, `next`) succeeds; afterwards `item_get` shows no holder and the `handoff_to`, and `closing_note.left` equals the `remaining` given |
| C8 | `item_report` with `attention` and `needs=<owner_needs>` adds that `needs:*` label; without `needs` it refuses and lists the values; `state=dropped` releases. The label read retries for up to 30 seconds, as in P6 |
| C9 | A non-record comment after the holder's last record appears in `follow_ups`, and still does after the holder's `item_renew`; a comment with two markers is not a record |
| C10 | With record authors set, a record pasted by another login is ignored by the fold |
| C11 | `issue_comment` with a record marker in the body refuses |
| C12 | With a board, the claim tools write `Agent` and `Last report` and nothing else; a failing board write returns a warning and the record still posts |
| C13 | Fold golden tests: the fixtures in this folder's table below give the stated `holder`, `lease_until`, `stale`, `last_report`, `handoff_to` |
| C14 | One caller claims two issues with the same `branch`: both succeed and each `item_get` shows the caller as holder with `mandate.branch` equal to it; releasing the first leaves the second held with its own lease; a `branch` of `bad..name` refuses |
| C15 | Review claims: a caller claims an issue with `session=A` and releases it. `purpose=review` then refuses with no `session`, with `basis=inferred`, and with `session=A`; with `session=B` it succeeds and `item_get` shows `mandate.purpose` `review` and `mandate.session` `B` |
| C16 | `activity_since` after a claim and a plain comment on the held issue: the comment is an entry with `source` `held`, `kind` `comment` and the issue's `number`, and no entry is a record; with `since` after the comment it is absent; with a second token, the second caller sees no entry for that issue |
| C17 | `activity_since` with `limit=1` over two new comments: the first page has one entry and `has_next_page`; `next_cursor` gives the other, with no repeat, and the same `read_at` as the first page |
| C18 | (by hand) A review on a PR opened through `pr_open` appears for the PR's `by` principal as `source` `pr`, `kind` `review`, with its `review_state`; a comment on a channel issue appears as `source` `channel` |
| C19 | (needs a closing-note server) `item_release` with `done`, `left`, `decided` and no `set_aside` succeeds and `item_get` shows `closing_note` with those parts and `set_aside` `none`; a release with none of the four succeeds with a `warnings` entry naming `done`, `left`, `decided` and `set_aside`; `left` and `remaining` given with different values refuse |
| C20 | A fresh item with no earlier worker shows `interruptions` 0, `previous_holder` null and `closing_note` with all four parts `none recorded`; after one claim and release with a `handoff_to` the second caller's `item_get` shows `previous_holder` the first caller, `interruptions` 0 and the first caller's four parts |
| C21 | (by hand) Claim with lease `1m`, wait two minutes: `item_get` shows `stale` and `interruptions` 1; a takeover by a second principal keeps `interruptions` at 1, names `previous_holder`, and shows the abandoned worker's last four parts, or `none recorded` |
| C22 | (needs `answering` on `item_report`) After `item_report` with `attention`, `item_report` with `answering` = that record's comment id and a `note` succeeds from any caller; `item_get` then shows `attention` null. A second `answering` of the same id, an `answering` of an unknown id, and an `answering` with no `note` each refuse with a message naming `answering`. When the question was asked by the holder with `state` `waiting` after a `progress` report, the answer also returns `last_report` to that `progress` report |
| C23 | (needs `interruption_limit` in `item_get`) A fresh item shows `interruption_limit` as a whole number of 1 or more and `escalation` null. `item_report` with `decision` and no `answering` refuses naming `answering`, and `decision` other than `retry` or `hold` refuses |
| C24 | (the runner checks the first sentence; the rest is by hand, with an owner's token) `item_report` with `decision` `retry` or `hold` and an `answering` from a token that is not an owner refuses `owner-required` and records nothing; the runner passes the check on that refusal and reports the retry-path steps below as skipped, not failed. With the limit reached by abandoned leases, the next claim refuses `interruption-limit` and posts one question for the owner; a second claim refuses and posts nothing; the item is not offered to an unpointed pickup; `answering` with `decision` `retry` resets `interruptions` to 0, clears `escalation` and a claim succeeds; a different answer leaves `escalation` `held` and claims still refuse; a later `answering` with `decision` `retry` naming the held `escalation.comment_id` succeeds, resets `interruptions` and offers the item again; a second `retry` of the same id then refuses |

C13 fixtures (records in comment order, times in minutes from zero, "now" is minute 200):

| Case | Records | Expected |
| --- | --- | --- |
| a | claim A lease to 250 | holder A, not stale |
| b | claim A to 120; claim B | holder A, B in `lost_claims` |
| c | claim A to 120; claim B at 130 `takeover_of` A, lease to 250 | holder B |
| d | claim A to 120; claim B at 100 `takeover_of` A | holder A (lease not over at 100) |
| e | claim A to 150; report A `progress`; report A `dropped` | no holder |
| f | claim A to 150; release A `handoff_to` any | no holder, `handoff_to` any |
| g | claim A to 150; renew B to 400 | holder A, lease 150, stale |
| h | claim A to 300; report B `attention` | holder A, attention from B, `last_report` null |
| i | claim A to 300; report A `blocked` | holder A, `last_report` blocked |
| j | four non-record comments (plain text, two markers, `v2`, bad JSON); claim A to 300 | holder A only |
| k | claim A to 60; A reports `progress` with parts at 30; claim B at 90 `takeover_of` A | holder B, `interruptions` 1, `previous_holder` A, parts A's |
| l | claim A; release A with `done`, `decided`, an empty `left` and `set_aside` | parts `done`, `none`, `decided`, `none` |
| m | claim A; release A in the old form (`done`, `remaining`, `next`) | `left` is the `remaining` |
| n | claim A to 60; claim B at 90 `takeover_of` A, A having recorded no note | `interruptions` 1, parts all `none recorded` |
| o | claim A to 120; A reports `progress` with `done`; now is 200 | holder A, stale, `interruptions` 1, A's parts |
| p | claim A to 30; B takes over at 40 to 90; C takes over at 100 | holder C, `interruptions` 2, parts `none recorded` |
| q | claim A; release A with all four parts; claim B | holder B, `interruptions` 0, A's parts |
| r | claim A to 300; `stop` at 100 with limit 230 | holder A, `stop_state` `requested`, not overdue |
| s | the same with limit 150 | overdue, holder A still, not stale |
| t | claim A; `stop`; A releases with the four parts | no holder, `stop_state` `at-rest`, A's parts |
| u | `stop`; then claim A | claim lost, no holder, `at-rest` |
| v | `stop`; `stop_clear`; claim A | holder A, no stop |
| w | `stop` by an account that is not the owner; claim A | the stop is ignored: holder A, no stop |
| x | `stop` by the owner; `stop_clear` by a non-owner; claim A | the clear is ignored: claim lost, `at-rest` |
| y | claim A to 60; A renews at 90 to 300; now is 200 | holder A, not stale, `interruptions` 0 (the count is not monotonic) |
| z | claim A; A reports `progress`; A asks with `state` `waiting` (comment 3); B reports `answering` 3 | holder A, `last_report` `progress`, no attention |

The fixtures name `owners` (the principals whose `stop` and `stop_clear` count); a fold gets them as a second input. The fold result keys the cases read besides the first five are `interruptions`,
`previous_holder`, `closing_by`, `closing_parts` (the four parts in the order `done`,
`left`, `decided`, `set_aside`), `stop_state` (`requested`, `at-rest` or null) and
`overdue`. A fold that does not compute them fails these cases, so a server that has not
implemented the closing note, interruptions or the stop signal fails C13 until it does.

The same cases are machine-readable in [fold_cases.json](../conformance/fold_cases.json).

## Sign-offs (Core)

[Sign-offs](sign-offs.md). G1 to G5 need the sandbox repo; they post comments and claims
on sandbox issues.

| Id | Check |
| --- | --- |
| G1 | `issue_comment` returns `body` and `signoff`; the body holds the caller's text, then exactly one `gtd-sign v1` marker whose JSON has `v` 1, `by` equal to the caller's `whoami` principal, `act` `comment`, `role` `worker`, and `t`; `signoff` equals that JSON; the visible line holds `gtd-sign` and the principal |
| G2 | `issue_comment` with `session` records it in the sign-off; with `role="coordinator"` signs as `coordinator`; refuses `role="owner"` from an agent principal, and an unknown role with a refusal that lists `worker`, `reviewer`, `coordinator` and `owner` |
| G3 | `issue_comment` refuses a body that holds `<!-- gtd-sign v1 {...} -->`, and the refusal names `gtd-sign` |
| G4 | `issue_comment` with `review_stage` and `review_verdict` refuses without the caller's review claim, refuses with only one of the two, and refuses `review_verdict="approved"` listing the three verdicts. With the review claim, a `session` other than S refuses. Holding a review claim (session S), `review_stage="work"`, `review_verdict="needs-changes"` succeeds: `act` `review`, `role` `reviewer`, `review` `{"stage": "work", "verdict": "needs-changes"}`, `session` S, and the body's first line is `Work review: Needs changes` |
| G5 | An agent `item_claim` with `session` S, `model` and `reasoning`, then `item_report` by the holder: both sign-offs carry those values, the caller's principal, session S and the respective acts; an independent agent comment without values records both as `unknown` |

## Join (Join level)

| Id | Check |
| --- | --- |
| J1 | With no approver configured, `/join/start` and joined-agent tokens are refused |
| J2 | `/join/start` validates the name pattern and the preset; returns the fields in agent sign-in with `expires_in` 600 and `interval` 5; user code matches `^[A-Z0-9]{4}-[A-Z0-9]{4}$` |
| J3 | Polling before a decision gets `authorization_pending`; past the pending-request cap `/join/start` gets `slow_down`; after 600 s `expired_token`; after deny `access_denied` |
| J4 | After approval the first poll returns the grant (with the approved preset, which may be lower than requested); the second poll does not |
| J5 | The store holds no plaintext token after collection |
| J6 | A renew returns a new pair; reusing the old refresh token answers `invalid_grant` **and** the new access token is refused afterwards |
| J7 | Token expiries never pass the approval's end; after it, renew is `invalid_grant` |
| J8 | Revoke one: that agent's next MCP call is `401` and its renew is `invalid_grant`; other agents still work. Revoke all: every agent and pending request is gone |
| J9 | `/join/decide`, `/join/revoke` and `/join/revoke-all` refuse without a valid CSRF token and without an approver session; a non-approver account is refused |
| J10 | No MCP tool name or description offers approve, deny or revoke |
| J11 | `/join` has exactly one `Entrances:` line listing `device-code` and, when offered, `connector`; `whoami` for a joined agent returns `entrance` |

### Connector entrance (when offered)

A server whose `Entrances:` line lists `connector` must also pass these. A runner drives
them as an OAuth client (dynamic registration with a loopback redirect, then `/authorize`
with PKCE), with a person approving once in a browser. Checks that need an approver
session or a long wait (marked *manual*) may be run by hand.

| Id | Check |
| --- | --- |
| JC1 | Registration accepts a loopback redirect (`localhost` or the loopback address); `/authorize` sends the browser to `/join/approve?connect=<id>`; the page offers "Sign in as an agent"; with `resource=<mcp_url>/mcp?agent=<name>` the card is prefilled with that name |
| JC2 | Approving redirects to the client's registered address with `state` unchanged and a code; denying redirects with `error=access_denied` and creates no agent |
| JC3 | The code works once, only for its client and only with the right PKCE verifier; a refused redemption does not spend it, so a correct one afterwards succeeds; not after 5 minutes (*manual*) |
| JC4 | The token response holds the agent access token and a connector refresh token, never the agent's own refresh token; `whoami` with that access token shows `agent:<name>`, the approved preset, `entrance` `connector`, and the fence applies |
| JC5 | `/join/agents` lists the agent with entrance `connector` beside device-code agents (*manual*) |
| JC6 | A connector refresh returns a new connector refresh token; two refreshes sent at once with the same token both succeed with the same answer and the agent is not revoked; the replaced token presented after the grace window answers `invalid_grant` and revokes the agent; a refresh after the access token ends returns a new access token (*manual*: after 24 hours) |
| JC7 | After revoke (through `revocation_endpoint` when advertised, else *manual* on `/join/agents`) the access token gets `401` and the connector refresh gets `invalid_grant`; the connector refresh token never works for another client, nor past the approval's end (*manual*) |
| JC8 | Re-joining the same name through the device code revokes the connector agent, and the reverse (*manual*) |
| JC9 | `/join/decide` for a connect id refuses without a valid CSRF token, without an approver session, and for a non-approver account (*manual*) |

## Board (Board level)

| Id | Check |
| --- | --- |
| B1 | `project_set_status` with an unknown column refuses and lists the live ones |
| B2 | `project_set_field` sets and clears text, number, date and single-select fields by name |
| B3 | `project_item_move` with no `after_*` puts the item first; with one, right after it. GitHub Projects can serve the old order for a while after a move, so the runner re-reads `project_items` for up to 30 seconds before failing, as in P6 |
| B4 | Writes to an issue not yet on the board add it first |
| B5 | (needs a board whose `Priority` options are `P0` to `P3`) `project_set_field` with `Priority` `P0` sets it, and with `P4` refuses and the refusal names `P0`, `P1`, `P2` and `P3`; the item keeps `P0` |
| B6 | (agent principal) `Priority` on an item with none is set once as a suggestion; a second write by the agent refuses and says the field is set, and the value is unchanged |

## Customization (when offered)

A server that lists `profile_updates` in `tools/list` must also pass these.

| Id | Check |
| --- | --- |
| O1 | Every label, field and view in every `profile_get` carries a `fingerprint` equal to the one recomputed from the item as [fingerprints](repo-context-and-profiles.md#fingerprints) defines (without `fingerprint` and `manual`) |
| O2 | `profile_updates` for the sandbox repo returns `profile`, `overrides`, `inferred` and `updates`; every notice has the fields of the [upstream change notice](repo-context-and-profiles.md#upstream-change-notice), and `current` equals that item's fingerprint in `profile_get` |
| O3 | With an override whose `seen` is stale, a reconcile plan reports the item as an upstream change and plans no write to it; with `skip` and no `seen`, the item is not created; recolouring a label the reconciler made (its name in another case too) is kept on the next run; nothing is ever deleted (*manual*: needs a scratch repo whose `gtd-context.json` a person edits) |

## Pull requests (when offered)

A server that lists `pr_open` in `tools/list` must also pass these
([opening pull requests](tools.md#opening-pull-requests)). PR1 and PR2 open nothing. PR3 needs
a branch already pushed to the sandbox repo (the runner's `--pr-head`) and leaves one PR
open for a person to close. PR5 to PR7 use that PR and post on it.

| Id | Check |
| --- | --- |
| PR1 | Holding a claim on a sandbox issue, `pr_open` refuses a cross-repository `head` (`owner:branch`), a `head` equal to `base`, and a `head` that is not a branch of the repo |
| PR2 | `pr_open` refuses an empty `issues` and says so (the refusal names `issues`); refuses an issue the caller holds no claim on and names it; refuses a `body` that holds a `gtd-pr` marker and names `gtd-pr`; refuses a `body` of `Rollback: hold or close #<n>` and says `closing keyword`. Each refusal gives that reason, not only a missing branch |
| PR3 | With a claim on a sandbox issue and a pushed `head`, `pr_open` opens the PR: `author` is not the caller's GitHub login and ends in `[bot]`, `by` equals the caller's `whoami` principal, and the returned `body` ends with exactly one `gtd-pr v1` marker whose `by` and `issues` match. Without `closes` it reports `closes` false and the body has no `Closes #` line. A second `pr_open` for the same `head` and `base` refuses and gives the open PR's URL |
| PR4 | The PR PR3 opened: its `body` holds exactly one `gtd-sign v1` marker with `act` `pr` and `by` the caller's principal, before the `gtd-pr` marker, and the result's `signoff` equals it |
| PR5 | The PR PR3 opened: `issue_comment` on its number succeeds; the body holds exactly one `gtd-sign v1` marker with `act` `comment`, `by` the caller's principal and `role` `worker` (the caller's work claim on the issue the PR's marker names), and the result's `signoff` equals it and it returns the comment's `url`; with `--github-token-env` the runner reads the comment from GitHub and its author is PR3's `author`, not the caller's login. The same call with `review_stage` and `review_verdict` refuses |
| PR6 | When `pr_review` is offered, on the PR PR3 opened: refuses `event="approve"` naming `approve`; refuses `event="request-changes"` (the server's identity authored that PR) and says to use `comment`; refuses a `body` holding a `gtd-sign` marker naming `gtd-sign`; refuses an inline comment whose `body` holds a `gtd-desk` marker naming `gtd-desk`; refuses a `repo` not on the allowlist. None of these posts a review |
| PR7 | When `pr_review` is offered, on the PR PR3 opened: `event="comment"` with no inline comments posts one review; `author` ends in `[bot]` and is not the caller's login; the body holds exactly one `gtd-sign v1` marker with `act` `pr-review` and `by` the caller's principal, and `signoff` equals it |
| PR8 | When `pr_review` is offered: a review with one inline comment on a line of the diff signs the review body and the inline body, each with one marker; a review whose second inline comment is off the diff refuses and posts no review and no inline comment (*manual*: needs a PR with a known diff) |
| PR9 | When `pr_review_reply` is offered, on a PR with a review comment: a reply is signed (`act` `pr-reply`, `by` the principal) under the App; with `resolve=true` the thread is resolved and `resolved` is true; a second call with `resolve=true` and no `body` posts nothing; a `comment_id` from another PR refuses naming `comment_id`. A PR whose `gtd-pr` marker is in a body written by a person gives the caller the ordinary default role, not `reviewer` (*manual*: needs a review thread and a hand-made PR) |
| PR10 | On the PR PR3 opened, a caller holding no claim on the issue its `gtd-pr` marker names gets the ordinary default role on `issue_comment` (`worker` for an agent, `owner` for a person); and on a PR whose trusted marker names an issue the server cannot read, the caller also gets the ordinary default and the comment still posts (*manual*: needs a second principal and a hand-made PR) |

## Ready check (when offered)

A server that lists `item_ready` in `tools/list` must also pass these
([ready check](ready-check.md), [prose check](prose-check.md)). The Readiness group holds
both `item_ready` and `prose_check`.

| Id | Check |
| --- | --- |
| R1 | The golden cases below, fed to the server's own ready logic (`--ready-cmd`), give the stated `verdict`, failed rules in rule order, and open blockers |
| R2 | `item_ready` returns `repo`, `number`, `title`, `verdict` (one of the three words), `missing` (rules from the six), `blockers`, `kind`, `size`; with a board, an issue with a clear title and summary, criteria and an allowed Size, nothing else on it, is `ready` |
| R3 | It writes nothing: the issue's claim state (`item_get`) is the same after two calls, and an issue not on the board is still not on it |
| R4 | An issue without an acceptance-criteria section fails `acceptance-criteria`; one with the section and a `needs:*` label fails `open-question` and not `acceptance-criteria` |
| R5 | "Blocked by `#N`" in the body without a native link, and the `blocked` label with no open native blocker, each fail `unlinked-blocker`; once linked, the blocker is in `blockers` and the rule passes; linking back either refuses with a reason that names the cycle (GitHub refuses a dependency cycle itself, so `issue_blocked_by_add` passes its reason through) or, when the link lands, fails `blocker-cycle`. The cycle rule itself is covered offline by R1 |
| R6 | With a board, no Size, and a Size outside `pickup_sizes`, each fail `size` |
| R7 | A pull request, a closed issue, an issue of Kind `epic`, and an issue labelled `standing` are refused |
| R8 | `item_claim` returns `ready` whose `verdict`, failed rules and open blockers equal what `item_ready` returns for the issue; an explicit claim on an issue without criteria succeeds (the verdict never refuses) and a `warnings` line names `needs-refinement`; a claim on a `ready` issue has no "not ready" warning ([the ready verdict on a claim](tools.md#claims-and-reports)) |
| R9 | `prose_check` is offered, and the [prose golden cases](../conformance/prose_cases.json), fed to the server's own prose logic (`--prose-cmd`), give the stated `verdict`, fail rules and warn rules, each in rule order |
| R10 | `prose_check` on a sandbox issue whose title has a prefix and whose body opens with a heading is `unclear` with `title-prefix` and `summary-first`, and `item_ready` on it fails `prose`; on draft text (`title`, `body`, `kind` `epic`) with no Outcome check it returns exactly the fail rule `epic-sections` |
| R11 | (needs a closing-note server) `item_ready` on a story whose last worker released with four parts returns `interruptions`, `previous_holder` and the same `closing_note` as `item_get` |
| R12 | The golden cases of an item's declared needs ([needs_cases.json](../conformance/needs_cases.json), table under Item needs below), fed to the server's own parser (`--needs-cmd`, which also gets `size_table` when a case has one), give the stated fields; an invalid need gives a non-empty `errors` that names the value, and an item with no `## Needs` section is `runs_anywhere` |

R1 cases ([ready_cases.json](../conformance/ready_cases.json); the issue has Size `S`,
`pickup_sizes` is `XS`, `S`, `M`, and it is on the board unless the case says otherwise):

| Case | What | Expected |
| --- | --- | --- |
| `ready` | criteria, Size S, no blockers | ready |
| `ac-missing` | no criteria heading | needs-refinement: `acceptance-criteria` |
| `ac-empty` | heading with no list item before the next heading | needs-refinement: `acceptance-criteria` |
| `ac-task-box` | level-3 heading in another case, task-box items | ready |
| `ac-subheading` | a lower-level heading between the heading and the item still counts | ready |
| `ac-in-code` | a heading inside a fenced code block does not count | needs-refinement: `acceptance-criteria` |
| `ac-empty-box` | an empty task box is not a criterion | needs-refinement: `acceptance-criteria` |
| `ac-in-long-fence` | a three-backtick line does not close a four-backtick fence | needs-refinement: `acceptance-criteria` |
| `ac-after-tilde-fence` | criteria after a closed tilde fence count | ready |
| `question` | a needs:* label is an open question | needs-refinement: `open-question` |
| `body-unlinked` | a blocker named in the body but not linked | needs-refinement: `unlinked-blocker` |
| `body-unlinked-full` | the owner/repo form, and depends on | needs-refinement: `unlinked-blocker` |
| `body-unlinked-url` | the issue URL form | needs-refinement: `unlinked-blocker` |
| `body-linked` | a body blocker that is a native link, closed | ready |
| `body-other-words` | a reference without the blocker words is not a blocker | ready |
| `body-self` | a reference to the issue itself is ignored | ready |
| `label-unlinked` | the blocked label with no open native blocker | needs-refinement: `unlinked-blocker` |
| `label-linked` | the blocked label with an open native blocker | ready-blocked; blockers B |
| `blocked-open` | an open native blocker | ready-blocked; blockers B |
| `blocked-closed` | a closed native blocker does not block | ready |
| `cycle-direct` | the issue and its blocker block each other | needs-refinement: `blocker-cycle`; blockers B |
| `cycle-upstream` | a cycle upstream of the issue | needs-refinement: `blocker-cycle`; blockers B |
| `cycle-broken` | a closed issue breaks the cycle | ready-blocked; blockers B |
| `chain` | a chain without a cycle | ready-blocked; blockers B |
| `walk-under-bound` | 49 issues in the walk (the issue and a chain of 48) is checked | ready-blocked; blockers N01 |
| `walk-at-bound` | a walk that reaches 50 issues fails, cycle or not | needs-refinement: `blocker-cycle`; blockers N01 |
| `size-none` | no Size | needs-refinement: `size` |
| `size-large` | a Size outside pickup_sizes | needs-refinement: `size` |
| `no-board` | no readable board | needs-refinement: `size` |
| `several` | every failure is listed, in rule order, with the open blocker | needs-refinement: `acceptance-criteria`, `open-question`, `unlinked-blocker`, `size`; blockers B |
| `prose-title` | a prefixed title fails prose | needs-refinement: `prose` |
| `prose-summary` | a body that opens with provenance fails prose | needs-refinement: `prose` |
| `prose-warn-only` | a warning alone does not fail prose | ready |

Every R1 case has the title `Show the thing working for its owner` unless it names its
own, and a body that opens with a summary unless the case is about the summary.

## Item needs (when offered)

R12 cases ([needs_cases.json](../conformance/needs_cases.json); the file gives the body, the
board Size or null, and every field of the answer: `declared`, `graphics_gb`, `tools`,
`longest_run_minutes`, `longest_run_source`, `runs_anywhere`, and `errors`, which is compared
only as empty or not, because its wording is the server's own). The reference is
[item_needs.py](../conformance/item_needs.py).

| Case | What | Expected |
| --- | --- | --- |
| `none` | an item with no Needs section runs anywhere | parsed |
| `all-three` | graphics memory, tools and a longest run are read | parsed |
| `in-comment` | a Needs section inside an HTML comment (the story template) is not read | parsed |
| `in-fence` | a Needs section inside a fenced example is not read | parsed |
| `in-indented-fence` | a Needs section inside a fence indented up to three spaces is not read | parsed |
| `in-open-fence` | a Needs section after a fence that is never closed is not read | parsed |
| `signoff-after` | a server's sign-off after the section (a rule, then a sub line) is not part of it | parsed |
| `comment-marker-in-fence` | a comment marker inside a fenced example does not swallow the real section after it | parsed |
| `fence-marker-in-comment` | a fence marker inside an HTML comment does not hide the real section after the comment | parsed |
| `comment-across-lines` | the text before a comment that spans lines and the text after it are one line | parsed |
| `size-default` | a Size supplies the longest run when none is declared | parsed |
| `declared-over-size` | a declared longest run wins over the Size default | parsed |
| `unit-days` | days convert to minutes | parsed |
| `size-xs` | XS gives 15 minutes | parsed |
| `size-s` | S gives 1 hour | parsed |
| `size-l` | L gives 1 day | parsed |
| `size-xl` | XL gives 3 days | parsed |
| `size-table-override` | a profile's own Size table overrides the default for the Sizes it lists | parsed |
| `bad-graphics` | a graphics memory that is not a number is named | refused, errors name the value |
| `bad-tool` | a tool that is not a name is named | refused, errors name the value |
| `bad-run` | a longest run with no unit is named | refused, errors name the value |
| `unknown-need` | a line that names no known need is named | refused, errors name the value |
| `tools-repeat` | a repeated tool is listed once, lowercased | parsed |

## Kind and parent rules (when offered)

A server that lists `sub_issue_add` or `issue_type_set` in `tools/list` must also pass
these ([parent rules](repo-context-and-profiles.md#kinds)). K3 and K4 need a sandbox repo
whose owner has the Issue Types `Epic`, `Story`, `Chore`, `Spike` and `Finding`; without
them they are skipped.

| Id | Check |
| --- | --- |
| K1 | The golden cases below, fed to the server's own Kind logic (`--kind-cmd`), give the stated answer and rule |
| K2 | `issue_type_set` with `Task`, `question` and `DECISION` each refuses and names `retired-kind`, whether or not the owner has such a type |
| K3 | `sub_issue_add` links a story under an epic and a step (no Kind) under a story; it refuses a step under an epic (`epic-holds-stories`), a chore under a story (`holds-steps`), an epic under a story (`epic-is-top`) and a step under a finding (`finding-holds-nothing`), each refusal naming its rule and leaving no link |
| K4 | `issue_type_set` checks the new Kind against the issue's parent and its sub-issues: a story under an epic refuses `Finding` (`epic-holds-stories`) and `Epic` (`epic-is-top`); a step under a story refuses `Chore` (`holds-steps`); a story with no parent and a step under it refuses `Finding` (`finding-holds-nothing`, the sub-issue side alone); a refused write leaves the type as it was |

K1 cases ([kind_cases.json](../conformance/kind_cases.json); a Kind is an Issue Type name
or a `kind:` label value, any case; a type case names the issue's parent, if it has one,
and its sub-issues):

| Case | What | Expected |
| --- | --- | --- |
| `epic-story` | Epic holds Story | allowed |
| `epic-chore` | Epic holds Chore | allowed |
| `epic-bug` | Epic holds Bug | allowed |
| `epic-spike` | Epic holds Spike | allowed |
| `epic-research` | Epic holds Research | allowed |
| `epic-domain` | Epic holds Experiment | allowed |
| `epic-epic` | Epic holds Epic | refused: `epic-is-top` |
| `story-epic` | Story holds Epic | refused: `epic-is-top` |
| `none-epic` | no Kind holds Epic | refused: `epic-is-top` |
| `research-epic` | Research holds Epic | refused: `epic-is-top` |
| `epic-finding` | Epic holds Finding | refused: `epic-holds-stories` |
| `epic-none` | Epic holds no Kind | refused: `epic-holds-stories` |
| `story-none` | Story holds no Kind | allowed |
| `story-chore` | Story holds Chore | refused: `holds-steps` |
| `chore-bug` | Chore holds Bug | refused: `holds-steps` |
| `bug-finding` | Bug holds Finding | refused: `holds-steps` |
| `story-domain` | Story holds Experiment | allowed |
| `story-retired` | Story holds Task | allowed |
| `spike-finding` | Spike holds Finding | allowed |
| `spike-none` | Spike holds no Kind | allowed |
| `spike-story` | Spike holds Story | refused: `holds-steps` |
| `finding-none` | Finding holds no Kind | refused: `finding-holds-nothing` |
| `finding-domain` | Finding holds Experiment | refused: `finding-holds-nothing` |
| `research-story` | Research holds Story | allowed |
| `research-finding` | Research holds Finding | allowed |
| `domain-story` | Experiment holds Story | allowed |
| `none-story` | no Kind holds Story | allowed |
| `case-insensitive` | EPIC holds story | allowed |
| `type-task` | set Task; no parent | refused: `retired-kind` |
| `type-question` | set question; no parent | refused: `retired-kind` |
| `type-decision` | set DECISION; parent Epic | refused: `retired-kind` |
| `type-chore` | set Chore; parent Epic | allowed |
| `type-finding-under-epic` | set Finding; parent Epic | refused: `epic-holds-stories` |
| `type-clear-under-epic` | clear the type; parent Epic | refused: `epic-holds-stories` |
| `type-epic-with-parent` | set Epic; parent Story | refused: `epic-is-top` |
| `type-epic-under-untyped` | set Epic; parent with no Kind | refused: `epic-is-top` |
| `type-finding-with-steps` | set Finding; no parent; sub-issues no Kind | refused: `finding-holds-nothing` |
| `type-story-over-chore` | set Story; parent Epic; sub-issues no Kind, Chore | refused: `holds-steps` |
| `type-spike-over-finding` | set Spike; parent Epic; sub-issues no Kind, Finding | allowed |

## Issue artifacts (when offered)

A server that lists any `issue_artifact_*` tool in `tools/list` must also pass these
([issue artifacts](tools.md#issue-artifacts)). A1 to A6 need a sandbox repo where GitHub's
issue artifacts are available; they create artifacts on a sandbox issue and delete
nothing. A5 and A6 also need an HTML page the server may fetch (`--artifact-source-url`
and `--artifact-source-sha256`); without one they are skipped.

| Id | Check |
| --- | --- |
| A1 | `tools/list` has all four of `issue_artifact_list`, `issue_artifact_get`, `issue_artifact_create` and `issue_artifact_update`, and no tool whose name starts `issue_artifact_` and contains `delete` |
| A2 | `issue_artifact_create` of a `generic` and a `link` artifact returns `number`, `type`, `name` and `url`; `issue_artifact_list` shows both, and with `type=link` only the link; `issue_artifact_get` returns the body as written, with `sha256` and `bytes` of it |
| A3 | `issue_artifact_update` of the generic artifact's body returns the new body, and `versions` is one more than before |
| A4 | Each refuses and says why: `type` `report` (the refusal lists the four types); an empty `name`; a `link` body that is not one `https` URL; a body with a record marker; a body over 60000 characters |
| A5 | `issue_artifact_create` of an `embedded_html` artifact from `source_url` and `sha256` returns that `sha256` and `bytes` over 0; `issue_artifact_get` with `include_body=false` returns the same `sha256` and no body, and with the body returns one whose UTF-8 SHA-256 is that hash |
| A6 | Starting from A5's good create (its page and correct `sha256`), each case breaks one rule and refuses, and the issue gains no artifact (A6 fails when that good create is refused): `type` `generic`; `body` added; `sha256` left out; the URL as `http://`; a `sha256` that does not match the page |

## Intake (when offered)

A server that lists `intake_list` or `intake_ack` in `tools/list` must also pass these
([intake](tools.md#intake)). I2 to I4 need a sandbox repo and a second principal: the
second files one request issue, the first acks it (a project never acks its own request).

| Id | Check |
| --- | --- |
| I1 | `tools/list` has both `intake_list` (class `read`) and `intake_ack` (class `work`) |
| I2 | A new open issue with the label is in `intake_list` with `ack` null and `new` true for a `since` before it; it is `overdue` with `ack_within=0m` and not with `24h`; an issue without the label is not listed |
| I3 | `intake_ack` with `state=received` returns a `url`, and `intake_list` then shows `ack.state` `received` with `by` the caller and `overdue` false at `0m`; the same ack again returns `unchanged` true and adds no comment; `state=parked` then shows `parked` |
| I4 | `intake_ack` refuses and says why: an issue without the label; `state` `done` (the refusal lists the four); a `note` holding a record marker |
| I5 | (by hand) An ack marker pasted in a comment by a login that is not a record author is ignored: `intake_list` still shows the trusted ack, or null |

A server that lists `intake_check` ([the intake check](tools.md#the-intake-check)) also passes
these. I7 to I9 need a sandbox repo, and I9 runs only while the server is in `watch` mode. I7 to I9 also need a second token (`--token-b-env`): that principal files the item and the first token, an accepted checker, checks it, because a check by the item's filer is refused.

| Id | Check |
| --- | --- |
| I6 | The golden cases below, fed to the server's own status and write rules (`--intake-cmd`), give the stated answer |
| I7 | `intake_check` is class `work`; a `result` outside `pass`, `needs-more`, `decline` refuses and lists the three; `needs-more` with no `note`, and `pass` with a no, refuse; a valid `needs-more` writes a record and `item_get` shows `intake_check` with that `status`, the three answers and `by`; the same call again returns `unchanged` true |
| I8 | An item with no record reads `intake_check.status` `unchecked`, never `pass` |
| I9 | In `watch` mode, an item with a `decline` record is still in `list_next_actions` and carries no `needs:*` label |
| I10 | (by hand) With record authors configured and `INTAKE_CHECK_MODE=enforce`, a `needs-more` or `decline` item gets the owner's `needs:*` label, is absent from `list_next_actions` and refuses an `inferred` claim; an `unchecked` item and a grandfathered one (opened before `since`) stay pickable; a later `pass` by the checker removes the label the server added; with no record authors configured, `item_get` reports `mode` `watch` whatever the setting; a call by the item's holder is refused `not-the-checker` |

I6 cases ([intake_check_cases.json](../conformance/intake_check_cases.json); times in the file
are minutes, and a status case gives the records in comment order, the item's age against
`since` and the mode):

| Case | What | Expected |
| --- | --- | --- |
| `pass-watch` | a pass in watch mode | status `pass`, pickable |
| `needs-more-watch` | needs-more in watch mode blocks nothing | status `needs-more`, pickable |
| `decline-watch` | decline in watch mode blocks nothing | status `decline`, pickable |
| `needs-more-enforce` | needs-more in enforce mode is held | status `needs-more`, held |
| `decline-enforce` | decline in enforce mode is held | status `decline`, held |
| `pass-enforce` | a pass in enforce mode is pickable | status `pass`, pickable |
| `unchecked-watch` | no record reads unchecked, never pass | status `unchecked`, pickable |
| `unchecked-enforce` | no record in enforce mode reads unchecked and is not held | status `unchecked`, pickable |
| `grandfathered-enforce` | an item older than since with no record is grandfathered and never held | status `unchecked`, grandfathered, pickable |
| `grandfathered-watch` | the same in watch mode | status `unchecked`, grandfathered, pickable |
| `recheck-supersedes` | the latest record wins: needs-more then pass is a pass | status `pass`, pickable |
| `recheck-holds` | the latest record wins: pass then decline is held in enforce | status `decline`, held |
| `mode-default` | an unset or unknown mode reads as watch | status `decline`, pickable |
| `old-recorded` | an old item with a record is not grandfathered | status `needs-more`, held |
| `write-pass` | all three yes is a pass | written |
| `write-pass-no` | a pass with one no is refused | refused: `pass-needs-all-three` |
| `write-needs-more` | small is no, fits yes, with a note | written |
| `write-needs-more-bare` | needs-more with no note is refused | refused: `note-required` |
| `write-needs-more-all-yes` | needs-more with every answer yes is refused | refused: `needs-more-shape` |
| `write-needs-more-no-fit` | needs-more when it does not fit is refused | refused: `needs-more-shape` |
| `write-decline` | decline when it does not fit, with a note | written |
| `write-decline-fits` | decline when it fits is refused | refused: `decline-needs-no-fit` |
| `write-bad-result` | a result outside the three is refused | refused: `result` |

## Comment edits (when offered)

A server that lists `comment_update` or `comment_redact` in `tools/list` must also pass
these ([editing comments](tools.md#editing-comments)). CE2 to CE4 need a sandbox repo.

| Id | Check |
| --- | --- |
| CE1 | `tools/list` has both `comment_update` and `comment_redact`, each of class `work` |
| CE2 | `comment_update` on a comment the caller posted with `issue_comment` returns `url`, `body` and `signoff`; the body holds the new text and exactly one `gtd-sign v1` marker; that marker keeps the original `by`, `act`, `role` and `t`, and gains one `edits` entry with `by` the caller and a `t`; a second update adds a second entry after the first; the visible text holds `Edited by` |
| CE3 | `comment_update` refuses, with a reason: a body holding a sign-off marker (the refusal names `gtd-sign`); a body holding a record marker; a comment that holds a claim record (the refusal names `comment_redact`) |
| CE4 | `comment_redact` on a claim record's `note` text replaces it and returns `replaced` 1, and the record still folds to the same state; it refuses, naming the field, a `find` that sits in the record's `by` or `lease_until`; it refuses a `find` with no match and a `replace` holding `<!--` |
| CE5 | (by hand) Either tool refuses, with a reason, a comment by a login that is not a record author; and, given the id of a review comment on a pull request's diff, refuses and names `pr_review` |

## Stale done (when offered)

A server that lists `stale_done` or `item_close_done` in `tools/list` must also pass
these ([closing finished items](tools.md#closing-finished-items)). SD2 needs a sandbox repo.

| Id | Check |
| --- | --- |
| SD1 | `tools/list` has both `stale_done` (class `read`) and `item_close_done` (class `work`) |
| SD2 | For a fresh open story with criteria and no merged PR, `stale_done(number)` returns `verdict` `keep` with `no-merged-pr`, and `item_close_done` refuses naming it and leaves the issue open; with a `needs:*` label added, `reasons` also holds `needs` |
| SD3 | (by hand) A story whose merged PR carries an Evidence row for every criterion gets `close`, and `item_close_done` ticks the boxes, posts one signed comment and closes it `completed`; a story whose only merged PR mentions it, one with an unmet criterion, an epic, and a `standing` item each get `keep` with the matching reason |

## Stall check (when offered)

A server that lists `stall_check` ([checking for work that stands still](tools.md#checking-for-work-that-stands-still))
must also pass these. SC2 needs a sandbox repo.

| Id | Check |
| --- | --- |
| SC1 | `tools/list` has `stall_check`, class `read` |
| SC2 | With no `mode`, the result's `mode` is `watch` and `speak` is empty; a fresh item with no claim and no release is not in `findings`; a `mode` other than `watch` or `speak` refuses, and so does `silent_after` of `1m` |
| SC3 | (by hand) A live claim with no report for longer than `silent_after` is listed as `silent-claim`, and one reported since is not; an unheld item whose latest release names a worker, older than `handoff_after`, is listed as `unheld-handoff`, and one held by someone else is not; in `watch` mode `would` has a line for each finding past three windows and `speak` is empty; in `speak` mode `speak` has one question for each, and nothing is written to the repo in either mode |

## Backlog review (when offered)

A server that lists `backlog_review` or `backlog_decide` ([backlog review](tools.md#backlog-review))
must also pass these. BR2 and BR3 need a sandbox repo; BR3 needs a caller who is not the item's owner.

| Id | Check |
| --- | --- |
| BR1 | `tools/list` has both `backlog_review` (class `read`) and `backlog_decide` (class `work`) |
| BR2 | `backlog_review` with no `mode` returns `mode` `watch`; a fresh open issue with no Priority is in the `unset` group of `digest`; `counts` add up to the entries in `digest`; the issue is still open afterwards; a `mode` other than `watch` refuses |
| BR3 | `backlog_decide` from a caller who is not the item's owner refuses naming the owner, and `item_get` shows `backlog` null |
| BR4 | (by hand, owner) Each of `promote`, `park` and `drop` through `backlog_decide` posts one signed record with the date, `item_get` shows the latest as `backlog`, and the issue is still open, with no label or Priority changed |

## Stop (when offered)

A server that lists `item_stop` or `item_stop_clear` ([stopping an item](tools.md#stopping-an-item))
must also pass these, and must have record authors configured. ST2 needs a sandbox repo and a caller who is not the item's owner.

| Id | Check |
| --- | --- |
| ST1 | `tools/list` has both `item_stop` and `item_stop_clear`, class `work` |
| ST2 | A caller who is not the item's owner is refused by `item_stop` and by `item_stop_clear`, the refusal says the owner is required, and afterwards `item_get` shows `stop` null, there is no `stop` record comment and no `stop-requested` label |
| ST3 | (by hand, owner) The owner's `item_stop` on a held item records one signed `stop` and sets the `stop-requested` label; the holder's `item_get`, `item_renew` and `item_report` each return `stop` with `state` `requested`; a second `item_stop` returns `unchanged`; the holder's `item_release` removes the label and `stop.state` is `at-rest` |
| ST4 | (by hand, owner) With `wind_down` `5m`, `item_renew` succeeds before the limit; after it `item_get` shows `overdue` true and `item_renew` refuses naming the stop; the holder is unchanged |
| ST5 | (by hand, owner) A stop on an item nobody holds is recorded `at-rest`, `item_claim` refuses naming the stop, and after `item_stop_clear` a claim succeeds and the label is gone |
| ST6 | (by hand) The `stop-requested` label added by a person who is not the owner is removed and nothing is recorded; added by the owner it becomes a recorded stop and stays |
| ST7 | (by hand) A `stop` marker pasted in a comment by an account that is not the owner is ignored: `item_get` shows no stop and `item_claim` still works; a `stop_clear` pasted the same way does not clear a real stop |

## Notifications (when offered)

A server that lists `notify_get` in `tools/list` must also pass these
([notifications](notifications.md)). N2 to N5 need a sandbox repo whose
`.github/gtd-context.json` maps the profile's `owner_needs` under `notify.mentions` to a
login that is not one the server writes records as (the runner skips them otherwise).

| Id | Check |
| --- | --- |
| N1 | `tools/list` has `notify_get` with class `read`; `notify_get` on the sandbox returns `mentions`, `push`, `new_issues`, `ping_as` and `warnings`, and on a repo outside the allowlist refuses |
| N2 | `item_report` with `attention` and the mapped `needs` returns `ping.posted` true with `to` the mapped login and `as` equal to `ping_as` and not `to`; `notify_get` with the number then lists exactly one ping with that `key`, whose `author` is `ping_as`. With `--github-token-env`, the runner also reads the comment at `ping.url` from GitHub itself and checks that its author is `ping_as` and not `to` |
| N3 | The same `attention` again returns `ping.reason` `unchanged` and the item still has one ping; a changed `attention` posts a second ping with a new `key`; when the map names a second `needs`, the same `attention` with that `needs` posts a third ping with a new `key` |
| N4 | An `attention` with a `needs` the map does not name returns `ping.reason` `no-map`, posts no ping, and the record and the `needs:*` label stand |
| N5 | `item_claim`, `item_renew`, `item_report` with only a `note`, and `item_release` return `ping` null or absent, and the item's ping count does not change |
| N6 | (by hand) A non-draft `pr_open` returns `review_requested` the owner's login, and GitHub shows the request from the App; a draft `pr_open` requests no review |
| N7 | (by hand) The mapped person's GitHub inbox shows one mention for the ask, from the `[bot]` author; with the map pointing at the login the server writes as, `ping.reason` is `no-identity` and `notify_get` warns |
| N8 | (by hand, when `push` is offered) A push copy of an ask and of a `pr_open` review request carries `reason` (`ask` or `pr-ready`) and `tag` and `Topic` from the key, no token in payload or URLs, at most Open, Snooze and Answer, and no second copy for an `unchanged` ping |

## Typed links (when offered)

A server that offers the Repo setup group (`work_items_plan`, a read tool, or
`work_items_sync`, which a caller below `full` does not see) must also pass these
([typed links](typed-links.md)). The runner runs L1 whenever it is given `--link-cmd`.

| Id | Check |
| --- | --- |
| L1 | The golden cases below, fed to the server's own link fold (`--link-cmd`), give the stated Related lines on each end, native blockers and refusals |
| L2 | A sync of a scratch repo whose register holds a `refines` and a `depends-on` link shows a Related section on both ends of each, with the far end's inverse name and its issue reference, and makes the dependent issue blocked by the other; a second sync plans no body edit |

L1 cases ([link_cases.json](../conformance/link_cases.json); the items are `EXP-1` to
`EXP-3`, `BM-1` and `FINDING-F1`, and one source adds the prefix `FINDING-`):

| Case | What | Expected |
| --- | --- | --- |
| `out-and-inverse` | one edge shows on both ends, the far end by its inverse name | 1 edge |
| `symmetric` | a symmetric kind reads the same from both ends | 1 edge |
| `symmetric-both-ways` | a symmetric link written from each end is one edge | 1 edge |
| `directed-both-ways` | a directed kind written from each end is two edges | 2 edges |
| `repeat` | the same link twice is one edge | 1 edge |
| `two-kinds` | two kinds between the same ends are two edges | 2 edges |
| `id-form` | a register keyed on id names the source as id | 1 edge |
| `artifact-link` | a link with a url and no to is an artifact pointer, not an edge | no edge |
| `other-events` | registrations and results are not links | no edge |
| `unknown-kind` | a kind outside the table is refused | refused: `unknown-kind` |
| `unknown-end` | an end that is no item is refused | refused: `unknown-end` |
| `self-link` | an item linked to itself is refused | refused: `self-link` |
| `prefix` | a record id resolves through a source's id prefix | 1 edge |
| `depends-on` | depends-on is also a native blocked-by | 1 edge; blocked-by |
| `unlink` | unlink removes the edge | no edge |
| `unlink-missing` | unlink of an edge that is not there is refused | refused: `no-such-link` |
| `unlink-other-kind` | unlink removes only its own kind | refused: `no-such-link`; the rest stands |
| `relink` | a link after its unlink stands again | 1 edge |
| `unlink-symmetric` | a symmetric edge is unlinked from either end | no edge |
| `unlink-depends-on` | unlinking depends-on drops the blocked-by too | no edge |
| `chain` | a follow-up chain lists each step on both sides | 2 edges |
| `every-kind` | each kind's inverse name | 11 edges; blocked-by |

## Record pages (when offered)

A server that reads or writes a register kept as record pages ([record pages](record-pages.md))
must pass these. The runner runs them against the reference implementation offline, and against
the server's own page code with `--page-cmd`, which reads one case as JSON on stdin (`op` is
`render`, `check` or `merge`) and writes the result as JSON on stdout.

| Id | Check |
| --- | --- |
| RP1 | The render cases below give the stated page byte for byte (`{"page": ...}`), and parsing that page gives back exactly the case's records, in order |
| RP2 | The rule cases below give the stated refusals (`{"refused": [...]}`, empty for a pass) |
| RP3 | The merge cases below give the stated page, or `null` for a refused merge (`{"page": ...}`) |

Cases ([page_cases.json](../conformance/page_cases.json)):

| Case | Check | What |
| --- | --- | --- |
| `experiment` | RP1 | a registration, a result, two readings, an item link, an artifact link, an attempt with no time, on an item-folder page |
| `no-folders` | RP1 | without a link map, a link target is a plain id |
| `fact` | RP1 | a flat page citing an item-folder page, and an id the link map does not name |
| `listening` | RP1 | a listening-test registration |
| `new-page`, `append`, `no-change` | RP2 | pass |
| `edit-record`, `edit-text`, `delete-entry` | RP2 | `edits-existing-content` |
| `delete-page` | RP2 | `page-removed` |
| `loose-prose`, `text-disagrees` | RP2 | `added-text-is-not-rendered-entries` |
| `hand-page` | RP2 | `page-is-not-rendered` |
| `other-item` | RP2 | `record-for-another-item:EXP-2` |
| `markers` | RP2 | `conflict-markers` |
| `wrong-id` | RP2 | `front-matter-id-is-not-the-file-name` |
| `two-appends` | RP3 | base, ours, then theirs |
| `same-append` | RP3 | the same entry on both sides is kept once |
| `one-edited` | RP3 | refused (`null`) |
| `v2-complete`, `v2-pin-mismatch`, `v2-other-register-v1`, `v2-typed-links` | RP1 | full readable experiment fields and digests; verify stored pin; other item kinds remain v1 |
| `v2-pin-malformed`, `v2-pin-nonhex`, `v2-pin-full`, `v2-pin-absent` | RP1 | stored hash format and unverified or verified full digest are explicit |
| `legacy-link-base-preserved`, `legacy-link-base-merge` | RP2, RP3 | historical base bytes remain untouched on append and merge |
| `mixed-new`, `mixed-append-v2`, `mixed-append-v1` | RP2 | accept exact versioned entries on mixed histories |
| `v2-tampered-prose`, `v2-tampered-marker`, `base-version-conflict`, `tail-version-conflict` | RP2 | reject altered or conflicting entry presentations |
| `mixed-distinct-preserved`, `mixed-same-conflict`, `mixed-base-conflict`, `mixed-identical-dedup`, `mixed-tail-conflict` | RP3 | preserve entry bytes, deduplicate identical entries and refuse presentation conflicts |

## Experiment evidence

A server advertising `experiment-evidence:1` runs these optional checks. They do not
fetch private bundles or execute a scorer; see [the contract](experiment-evidence.md).

| Check | Pass |
| --- | --- |
| EE1 | Every `experiment_evidence_cases.json` case selects the exact line, returns the unmodified result data and receipt, distinguishes legacy and empty VOID, reads JSONL and byte-preserving page fences, and refuses ambiguity or malformed binding. Run against server code via `--evidence-cmd`. |
| EE2 | A server claiming `experiment-evidence:1` exposes `experiment_evidence_get` as a read tool. |

## Register records (when offered)

A server that writes, reads or mirrors register records ([register records](register-records.md))
must pass these. The runner runs RR1 to RR4 against the reference implementation offline, and
against the server's own record code with `--record-cmd`, which reads one case as JSON on stdin
(`op` is `validate`, `upgrade` or `fold`) and writes the result as JSON on stdout.

| Id | Check |
| --- | --- |
| RR1 | The validate cases below give the stated refusals (`{"refused": [...]}`, empty for a pass) |
| RR2 | The upgrade cases give the stated record (`{"record": ...}`) |
| RR3 | The fold cases give the stated state and verdict (`{"state": {"state", "verdict", ...}}`) |
| RR4 | The same fold cases, shown through the case's source, give the stated labels, managed labels, Status, closed and fields (`{"shown": ...}`) |
| RR5 | By hand, on a scratch repo: `record_append` writes a valid record as one entry on the item's page with the envelope filled; an invalid one is refused and nothing is written; the same call with the same `eid` writes nothing and succeeds; an experiment `result` is refused `written-on-the-host` |
| RR6 | By hand: a sync of a scratch repo whose register holds a blocked experiment, a waiting benchmark and a record that fails its schema gives each issue the profile's issue type, kind label, state labels, invalid-record label, Status and fields, and a body with a Record link to the item's page; a second sync plans no edit |

Cases ([record_cases.json](../conformance/record_cases.json)):

| Check | Cases | What they cover |
| --- | --- | --- |
| RR1 | 35 | a complete registration and a version 0 line pass; bad JSON, an unknown event, a version ahead, a missing envelope field, a time without offset, a `by` that is no principal, a missing spec field, an enum miss, a missing stopping rule, a verdict outside the rule, a differing rule hash, an event before registration, a second registration, a reused `eid`, a link kind outside the list, an artifact with no pointer, a citation that is no hash |
| RR2 | 13 | a current record unchanged; a naive time read in the source's zone; no time; a free-text `by`; a link with a URL becoming an artifact; an observation headline moving to `title`; prereg from a tag, from a plain registered-before, and left empty when qualified; a reading with no kind; `from` with no `id`; a benchmark result's status from its counts |
| RR3, RR4 | 20 | an experiment registered, running, blocked, unblocked, closed by a verdict, unvalidated, retired void, a verdict standing over a later retire, unretired, holding an invalid record, and a version 0 one; a benchmark waiting, partial, complete and withdrawn; a finding current, stale after a reading, unchanged by a planning link, stale after another item's contradicts link, and retired |

## Machine fit (when offered)

| Id | Check |
| --- | --- |
| MF1 | The golden machine-card cases ([machine_fit_cases.json](../conformance/machine_fit_cases.json), `card_cases`, table below), fed to the server's own card validation (`--fit-cmd`), give the stated `ok` and name the stated fields in the stated order |
| MF2 | The golden fit cases (`fit_cases`, table below), fed to the server's own fit rule (`--fit-cmd`), give the stated `fits` and exactly the stated reasons |
| MF3 | (manual, when `resource_register` is offered) `list_next_actions` with a resource holds back each item that does not fit and gives its reason; an unknown resource id and a resource with no card are refused and offer nothing; an item is never offered and then refused for fit ([machine fit](machine-fit.md#fit)) |
| MF4 | (manual, when `resource_register` is offered) `list_next_actions` with no resource returns exactly what it did before; with a resource it lists only items that fit, and an `inferred` claim accepts each |

MF1 cases (the reference is [machine_fit.py](../conformance/machine_fit.py)):

| Case | What | Expected |
| --- | --- | --- |
| `valid` | a full card is accepted | accepted |
| `no-tools` | an empty tool list is a valid card | accepted |
| `tools-normalised` | tools are lowercased and listed once | accepted |
| `zero-graphics` | a machine with no graphics memory is valid | accepted |
| `missing-graphics` | a missing graphics memory is named | refused, names `graphics_gb` |
| `missing-storage` | a missing free storage is named | refused, names `free_storage_gb` |
| `missing-tools` | a missing tool list is named | refused, names `tools` |
| `missing-speed` | a missing speed is named | refused, names `speed_minutes` |
| `speed-text` | a speed that is not a number is named | refused, names `speed_minutes` |
| `speed-zero` | a speed of zero is refused | refused, names `speed_minutes` |
| `storage-negative` | negative free storage is refused | refused, names `free_storage_gb` |
| `graphics-bool` | a boolean is not a number | refused, names `graphics_gb` |
| `bad-tool` | a tool that is not a name is named under tools | refused, names `tools` |
| `tools-not-list` | tools that are not a list are named | refused, names `tools` |
| `unknown-field` | a field outside the card is refused by name | refused, names `token` |
| `two-bad` | every bad field is named, in card order | refused, names `graphics_gb`, `speed_minutes` |
| `not-an-object` | a card that is not an object is refused | refused, names `card` |

MF2 cases (the card is the valid card with 8 GB graphics, 200 GB storage, tools `voice` and `ffmpeg`, 45 minutes, unless the case says otherwise):

| Case | What | Expected |
| --- | --- | --- |
| `anywhere` | an item with no declared needs fits every machine | fits |
| `anywhere-with-size-run` | a Size default run does not hold back an item that declares nothing | fits |
| `graphics-short` | too little graphics memory is held back with the numbers | held back |
| `graphics-equal` | exactly enough graphics memory fits | fits |
| `tool-missing` | a tool the machine lacks is named | held back |
| `tools-present` | tools the machine lists fit | fits |
| `tools-two-missing` | each missing tool is named, in the item's order | held back |
| `run-too-slow` | a machine slower than the longest run is held back | held back |
| `run-equal` | a machine exactly as fast as the longest run fits | fits |
| `no-run-limit` | with no longest run, speed is not compared | fits |
| `all-three` | every failing need is named, graphics then tools then run | held back |
| `speed-factor` | a profile's speed factor scales the machine's time | held back |
| `fraction` | a fractional memory is printed without a trailing zero | held back |

## App board (when offered)

| Id | Check |
| --- | --- |
| AB1 | The golden column cases ([app_columns_cases.json](../conformance/app_columns_cases.json), table below), fed to the server's own mapping (`--columns-cmd`), give the stated column for each Status and accept or refuse each mapping as stated |
| AB2 | (manual, when `app_board` is offered) The call returns the six columns and the same counts as `project_items` by Status; a Status with no mapping is under `other`; it writes nothing and returns no credential |
| AB3 | (manual) An item in progress with a live claim shows its worker and the seconds left on its lease |
| AB4 | (manual) Items labelled with the signed-in owner's `needs:*` value are marked and counted in `needs_you_count`; another person's are not |

AB1 cases (the reference is [app_columns.py](../conformance/app_columns.py)):

| Case | What | Expected |
| --- | --- | --- |
| `default-table` | each Status of the gtd-dispatch board maps as the story says | mapped |
| `unmapped-is-other` | a Status with no mapping is other, never dropped | mapped |
| `no-status-is-other` | an item with no Status is other | mapped |
| `case-and-space` | options match without regard to case or extra spaces | mapped |
| `profile-mapping` | a profile's own mapping replaces the default | mapped |
| `mapping-ok` | a mapping onto the five columns is valid | valid |
| `mapping-bad-column` | a mapping onto a column that does not exist is refused | refused |
| `mapping-to-other` | other is the fallback, not a target | refused |
| `mapping-empty` | an empty mapping is refused (omit it for the default) | refused |

## Milestone handoff (when offered)

A server that lists any `handoff_*` tool, or names `milestone-handoff:1` in its
`capabilities`, must also pass these ([milestone handoff](milestone-handoff.md)). MH1 to MH6
run offline against the reference ([handoff.py](../conformance/handoff.py)) or against a
server's own code through `--handoff-cmd`.

| Id | Check |
| --- | --- |
| MH1 | Each `records` case below, validated against [the schema](schemas/milestone-handoff/handoff.schema.json), is valid or refused with the stated problem |
| MH2 | Each `head` case below, replayed in order, gives the stated outcomes (a handoff accepted or refused with its rule, a verdict effective or refused with its rule) and the stated heads, including a supersession racing an old verdict, a verdict by a non-recipient or without a review claim, and a findings handoff on its own milestone |
| MH3 | Each `routing` case resolves a recipient role to the stated binding or is refused with the stated rule: unauthorized role, self-review, ambiguity, expired and revoked bindings |
| MH4 | Each `bindings` case allows or refuses who may create, replace and revoke a binding, each `authority` case shows that a claim is still required, that a comment or role name grants nothing, and that self-review is refused, and each `claims` case folds claims to show a review claim coexisting with a live work claim only under the head review handoff |
| MH5 | Each `delivery` case, replayed in order, gives the stated outcomes and final state: duplicate delivery, lost acknowledgement, failed delivery with escalation, acknowledgement by another principal or on a revoked binding, and a delayed acknowledgement after supersession |
| MH6 | Each `retry` case gives the stated attempt offsets or deduplication key |
| MH7 | Each `negotiation` case gives the stated mode from the capabilities and tools; and a server whose `capabilities` names `milestone-handoff:1` or the push name lists every tool the name needs |
| MH8 | The handoff files name no runtime-specific endpoint (a host other than `example.com`, a port, a loopback address), and [notifications](notifications.md) names no handoff tool; the public guard and a reviewer's reading cover the rest |

MH1 cases ([handoff_cases.json](../conformance/handoff_cases.json), group `records`):

| Case | What | Expected |
| --- | --- | --- |
| `worker-to-reviewer` | a worker asks a reviewer to review a milestone revision | valid |
| `reviewer-to-worker` | a reviewer hands findings back to the worker | valid |
| `supersedes-set` | a successor handoff names the one it supersedes | valid |
| `sha256-revision` | an artifact digest is an immutable revision too | valid |
| `no-revision` | a handoff must name its evidence revision | refused: required (`$.revision`) |
| `branch-name-revision` | a branch name is not immutable | refused: does not match (`$.revision`) |
| `short-sha` | an abbreviated commit is refused | refused: does not match (`$.revision`) |
| `no-supersedes-key` | supersedes is always present, null for the first | refused: required (`$.supersedes`) |
| `unknown-action` | one concrete action from the fixed set | refused: must be one of (`$.action`) |
| `runtime-endpoint` | no runtime-specific field is allowed in the record | refused: not allowed (`$.endpoint`) |
| `bad-id` | the identifier has the fixed shape | refused: does not match (`$.handoff_id`) |
| `bad-role` | a recipient role is one of the four roles | refused: must be one of (`$.recipient.role`) |
| `no-sender-session` | the sender session is required | refused: required (`$.sender.session`) |
| `too-much-evidence` | at most ten evidence links | refused: too many items (`$.evidence`) |

MH2 cases (group `head`; events are replayed in comment order):

| Case | What | Expected |
| --- | --- | --- |
| `head-first` | the first handoff on a milestone becomes its head | H1 accepted |
| `head-supersede` | a successor naming the head and a new revision replaces it | H1 accepted; H2 accepted |
| `head-stale-base` | a second handoff that does not name the head is refused | H1 accepted; H2 refused `stale-base` |
| `head-same-revision` | a successor must change the revision | H1 accepted; H2 refused `same-revision` |
| `head-unknown-base` | a first handoff cannot name a successor target | H1 refused `unknown-supersedes` |
| `head-milestones-apart` | milestones have separate heads | H1 accepted; H2 accepted |
| `verdict-current` | a verdict naming the head's handoff and revision is effective | H1 accepted; verdict V1 effective |
| `verdict-old-revision` | accepting an old revision cannot authorize a newer one | H1 accepted; H2 accepted; verdict V1 refused `stale-revision` |
| `verdict-race-supersede` | a supersession that lands before the check wins over an old verdict; one that lands after leaves the earlier authorization standing for its own revision only | H1 accepted; verdict V1 effective; H2 accepted; verdict V1 refused `stale-revision` |
| `verdict-no-milestone` | a verdict that names no milestone is refused | H1 accepted; verdict V1 refused `missing-milestone` |
| `verdict-no-revision` | a verdict that names no revision is refused | H1 accepted; verdict V1 refused `missing-revision` |
| `verdict-no-handoff` | a verdict on a milestone with no handoff is refused | verdict V1 refused `no-handoff` |
| `verdict-other-milestone` | a verdict is effective for its own milestone only | H1 accepted; H2 accepted; verdict V1 refused `stale-revision` |
| `verdict-wrong-author` | a verdict by a principal that is not the handoff's recipient is never effective | H1 accepted; verdict V1 refused `unauthorized-author` |
| `verdict-no-review-claim` | a verdict written without a live review claim is never effective | H1 accepted; verdict V1 refused `no-review-claim` |
| `findings-own-head` | a findings handoff sits on its own milestone head and does not disturb the evidence head | H1, F1, H2 accepted; heads `m1` H2 and `m1-findings` F1 |
| `findings-on-evidence-milestone` | a findings handoff cannot take the evidence milestone | H1 accepted; F1 refused `findings-milestone` |
| `findings-suffix-reserved` | only a findings handoff may use the findings milestone | H1 refused `reserved-suffix` |
| `findings-round-trip` | review, findings back, a new revision and a second review: the second verdict is effective and the findings head stays | H1 accepted; V1 effective; F1, H2 accepted; V2 effective |

MH3 cases (group `routing`):

| Case | What | Expected |
| --- | --- | --- |
| `route-ok` | a reviewer role resolves to the one active binding | binding `bd_1` |
| `route-named` | a named principal resolves to its own binding | binding `bd_2` |
| `route-expired` | an expired binding is not a route | refused `no-binding` |
| `route-revoked` | a revoked binding is not a route | refused `no-binding` |
| `route-none` | no binding for the role | refused `no-binding` |
| `route-ambiguous` | two principals bound to the role and none named | refused `ambiguous-recipient` |
| `route-unauthorized-role` | a binding for a role the principal is no longer authorized for is not a route | refused `no-binding` |
| `route-named-unbound` | the named principal has no binding | refused `no-binding` |
| `route-self-review` | a review is never routed to the sender's own session | refused `self-review` |
| `route-worker` | a worker binding counts when the principal already took part in the item | binding `bd_1` |
| `route-worker-stranger` | a worker role is not open to a principal with no grant and no part in the item | refused `no-binding` |

MH4 cases (group `bindings`):

| Case | What | Expected |
| --- | --- | --- |
| `bind-own` | a principal binds its own session for an authorized role | allowed |
| `bind-replace` | a principal replaces its own binding | allowed |
| `bind-worker` | a principal that took part in the item binds the worker role | allowed |
| `bind-worker-stranger` | a worker role is refused to a principal with no grant and no part in the item | refused `role-not-authorized` |
| `bind-for-other` | no principal binds another's session | refused `others-binding` |
| `bind-owner-by-agent` | an agent never binds the owner role | refused `owner-role` |
| `bind-unauthorized` | a role the owner has not granted the principal | refused `role-not-authorized` |
| `bind-ttl-long` | a binding lasts at most 24 hours | refused `ttl-out-of-range` |
| `revoke-self` | the bound principal may revoke | allowed |
| `revoke-owner` | the owner may revoke any binding | allowed |
| `revoke-other` | another agent may not revoke | refused `not-allowed` |

MH4 cases (group `authority`):

| Case | What | Expected |
| --- | --- | --- |
| `work-claim-review` | a review claim for the handoff's item lets a reviewer work | allowed |
| `work-no-claim` | a delivered, acknowledged handoff without a claim grants nothing | refused `claim-required` |
| `work-comment-only` | a comment naming the reviewer is not authority | refused `no-authority` |
| `work-role-name` | a role name alone is not authority | refused `no-authority` |
| `work-wrong-purpose` | a work claim does not meet a review scope | refused `scope-mismatch` |
| `work-self-review` | a review by the session that did the work is forbidden | refused `self-review` |

MH5 cases (group `delivery`; events are replayed in order):

| Case | What | Expected |
| --- | --- | --- |
| `deliver-ack` | delivered, then acknowledged | deliver; ack; state `acknowledged` |
| `deliver-twice` | a duplicate delivery changes nothing | deliver; deliver unchanged; state `delivered` |
| `ack-twice` | a repeated acknowledgement is idempotent | deliver; ack; ack unchanged; state `acknowledged` |
| `lost-ack` | an acknowledgement the sender never saw is safely repeated | deliver; ack; ack unchanged; state `acknowledged` |
| `ack-before-deliver` | a recipient that polled can acknowledge a handoff whose delivery record was lost | ack; state `acknowledged` |
| `failed-exhausted` | delivery that never succeeds fails after its attempts and escalates | fail; state `failed`; escalated |
| `fail-early` | failure before the attempts are used is refused | fail refused `not-exhausted`; state `pending` |
| `fail-after-delivery` | a delivered handoff cannot fail | deliver; fail refused `delivered`; state `delivered` |
| `ack-other-principal` | another principal cannot acknowledge | deliver; ack refused `wrong-recipient`; state `delivered` |
| `ack-revoked-binding` | a revoked binding cannot acknowledge | deliver; ack refused `revoked-binding`; state `delivered` |
| `ack-wrong-revision` | an acknowledgement names the revision it received | deliver; ack refused `revision-mismatch`; state `delivered` |
| `ack-wrong-delivery` | an acknowledgement names the delivery id | deliver; ack refused `delivery-mismatch`; state `delivered` |
| `ack-after-supersede` | a delayed acknowledgement after supersession is recorded as stale | deliver; ack stale; state `acknowledged` |
| `ack-after-cancel` | an acknowledgement of a cancelled handoff is refused | cancel; ack refused `cancelled`; state `cancelled` |
| `cancel-pending` | a pending handoff may be cancelled | cancel; state `cancelled` |
| `cancel-acknowledged` | an acknowledged handoff cannot be cancelled | deliver; ack; cancel refused `acknowledged`; state `acknowledged` |
| `deliver-after-cancel` | an in-flight delivery after a cancel changes nothing | cancel; deliver refused `terminal`; state `cancelled` |
| `poll-ack` | in poll mode a granted recipient acknowledges with no binding | deliver; ack; state `acknowledged` |
| `poll-ack-ungranted` | in poll mode a principal the role is not granted to cannot acknowledge | deliver; ack refused `role-not-granted`; state `delivered` |

MH6 cases (group `retry`):

| Case | What | Expected |
| --- | --- | --- |
| `retry-default` | five attempts at 0, 1, 3, 7 and 15 minutes | offsets 0, 1, 3, 7, 15 |
| `retry-capped` | the delay doubles from one minute and stops at thirty | offsets 0, 1, 3, 7, 15, 31, 61, 91 |
| `dedupe-stable` | the deduplication key is fixed by handoff, revision and recipient | `dl_5b6fb2d2bffe465e` |
| `dedupe-new-revision` | a new revision is a new key | `dl_85f04884eccf6162` |
| `dedupe-other-recipient` | another recipient is a new key | `dl_632663f9bc2481ef` |

MH7 cases (group `negotiation`):

| Case | What | Expected |
| --- | --- | --- |
| `negotiate-none` | a legacy server offers nothing: the sender posts the packet as a comment and says delivery is manual | mode `manual` |
| `negotiate-tools-only` | tools without the capability name are not trusted | mode `manual` |
| `negotiate-poll` | the capability and the core tools without push: the recipient polls | mode `poll` |
| `negotiate-push` | push claimed and backed by the binding tools: the server delivers to bound sessions | mode `push` |
| `negotiate-push-no-bind` | push claimed but the binding tools are missing: poll | mode `poll` |
| `negotiate-no-ack` | the capability claimed with the acknowledgement tool missing: manual | mode `manual` |
| `negotiate-future-version` | only a later version named: manual | mode `manual` |

MH4 cases (group `claims`; events are replayed in order, `now` is 100):

| Case | What | Expected |
| --- | --- | --- |
| `review-beside-work` | a reviewer named by the head review handoff claims review while the worker holds the item | both accepted; holder the worker; reviewers the reviewer |
| `review-self` | the holder cannot take the review claim | refused `self-review` |
| `review-same-session` | a reviewer on the holder's own session is refused | refused `self-review` |
| `review-same-principal` | a fresh session of the holder's own principal, named by the head review handoff, takes the review claim (sessions are compared, not principals) | accepted; reviewers the principal |
| `review-no-handoff` | a review claim naming no handoff stays refused while the item is held | refused `held` |
| `review-stale-handoff` | a review claim naming a superseded handoff is refused | refused `stale-handoff` |
| `review-not-recipient` | only the handoff's recipient takes the review claim | refused `not-recipient` |
| `work-while-held` | a second work claim stays refused | refused `held` |
| `review-release` | a reviewer releases its own review claim and the worker keeps the item | holder the worker; no reviewers |
| `review-send` | a reviewer with a live review claim for the handoff may send; one without may not | second send refused `no-claim` |
| `review-expired-send` | a reviewer whose review lease has lapsed may not send | refused `no-claim` |
| `holder-lapsed` | a lapsed work claim leaves the item open to the review claim as an ordinary claim | holder the reviewer |

## Security (all levels)

| Id | Check |
| --- | --- |
| X1 | Across every test above, no log line contains a bearer token, a refresh token, a GitHub token or a token hash, and no response body does either, except the grant that `/join/token` returns on collection or renew (J4, J6) and the token response of the connector entrance (JC4, JC6) |
| X2 | Every tool's class matches the class the spec gives it (the preset table in [transport-and-identity](transport-and-identity.md#presets) and the Class columns and group notes in [tools](tools.md)); every tool the spec does not class has the class it declares in `_meta` `gtd-board-kit/class` ([presets](transport-and-identity.md#presets)), else `full`; a declared class is one of the four presets and agrees with the spec's class where the spec gives one |
| X3 | Over-long free text refuses rather than truncates |

## Running against the kit

A deployment can also smoke-test end to end: point a scratch repo with the kit installed
at the server, join an agent at `work`, and have it run `board-pickup`, `board-claim` on a
test issue, `board-report` with `progress`, `board-needs-person`, and `item_release`. Every
step should succeed without the agent leaving the MCP tools.
