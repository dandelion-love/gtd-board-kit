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
| C7 | `item_release` needs `done`, `remaining`, `next`; afterwards `item_get` shows no holder and the `handoff_to` |
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
| G5 | `item_claim` with `session` S, then `item_report` by the holder: both results carry `signoff` with `by` the caller's principal, `session` S, and `act` `claim` and `report` |

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
open for a person to close.

| Id | Check |
| --- | --- |
| PR1 | Holding a claim on a sandbox issue, `pr_open` refuses a cross-repository `head` (`owner:branch`), a `head` equal to `base`, and a `head` that is not a branch of the repo |
| PR2 | `pr_open` refuses an empty `issues` and says so (the refusal names `issues`); refuses an issue the caller holds no claim on and names it; refuses a `body` that holds a `gtd-pr` marker and names `gtd-pr`; refuses a `body` of `Rollback: hold or close #<n>` and says `closing keyword`. Each refusal gives that reason, not only a missing branch |
| PR3 | With a claim on a sandbox issue and a pushed `head`, `pr_open` opens the PR: `author` is not the caller's GitHub login and ends in `[bot]`, `by` equals the caller's `whoami` principal, and the returned `body` ends with exactly one `gtd-pr v1` marker whose `by` and `issues` match. Without `closes` it reports `closes` false and the body has no `Closes #` line. A second `pr_open` for the same `head` and `base` refuses and gives the open PR's URL |
| PR4 | The PR PR3 opened: its `body` holds exactly one `gtd-sign v1` marker with `act` `pr` and `by` the caller's principal, before the `gtd-pr` marker, and the result's `signoff` equals it |

## Ready check (when offered)

A server that lists `item_ready` in `tools/list` must also pass these
([ready check](ready-check.md)).

| Id | Check |
| --- | --- |
| R1 | The golden cases below, fed to the server's own ready logic (`--ready-cmd`), give the stated `verdict`, failed rules in rule order, and open blockers |
| R2 | `item_ready` returns `repo`, `number`, `title`, `verdict` (one of the three words), `missing` (rules from the five), `blockers`, `kind`, `size`; with a board, an issue with criteria and an allowed Size, nothing else on it, is `ready` |
| R3 | It writes nothing: the issue's claim state (`item_get`) is the same after two calls, and an issue not on the board is still not on it |
| R4 | An issue without an acceptance-criteria section fails `acceptance-criteria`; one with the section and a `needs:*` label fails `open-question` and not `acceptance-criteria` |
| R5 | "Blocked by `#N`" in the body without a native link, and the `blocked` label with no open native blocker, each fail `unlinked-blocker`; once linked, the blocker is in `blockers` and the rule passes; linking back either refuses with a reason that names the cycle (GitHub refuses a dependency cycle itself, so `issue_blocked_by_add` passes its reason through) or, when the link lands, fails `blocker-cycle`. The cycle rule itself is covered offline by R1 |
| R6 | With a board, no Size, and a Size outside `pickup_sizes`, each fail `size` |
| R7 | A pull request, a closed issue, an issue of Kind `epic`, and an issue labelled `standing` are refused |
| R8 | `item_claim` returns `ready` whose `verdict`, failed rules and open blockers equal what `item_ready` returns for the issue; an explicit claim on an issue without criteria succeeds (the verdict never refuses) and a `warnings` line names `needs-refinement`; a claim on a `ready` issue has no "not ready" warning ([the ready verdict on a claim](tools.md#claims-and-reports)) |

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
([issue artifacts](tools.md#issue-artifacts)). A1 to A4 need a sandbox repo where GitHub's
issue artifacts are available; they create artifacts on a sandbox issue and delete
nothing.

| Id | Check |
| --- | --- |
| A1 | `tools/list` has all four of `issue_artifact_list`, `issue_artifact_get`, `issue_artifact_create` and `issue_artifact_update`, and no tool whose name starts `issue_artifact_` and contains `delete` |
| A2 | `issue_artifact_create` of a `generic` and a `link` artifact returns `number`, `type`, `name` and `url`; `issue_artifact_list` shows both, and with `type=link` only the link; `issue_artifact_get` returns the body as written |
| A3 | `issue_artifact_update` of the generic artifact's body returns the new body, and `versions` is one more than before |
| A4 | Each refuses and says why: `type` `report` (the refusal lists the four types); an empty `name`; a `link` body that is not one `https` URL; a body with a record marker; a body over 60000 characters |

## Intake (when offered)

A server that lists `intake_list` or `intake_ack` in `tools/list` must also pass these
([intake](tools.md#intake)). I2 to I4 need a sandbox repo; they create one request issue
and post acks on it.

| Id | Check |
| --- | --- |
| I1 | `tools/list` has both `intake_list` (class `read`) and `intake_ack` (class `work`) |
| I2 | A new open issue with the label is in `intake_list` with `ack` null and `new` true for a `since` before it; it is `overdue` with `ack_within=0m` and not with `24h`; an issue without the label is not listed |
| I3 | `intake_ack` with `state=received` returns a `url`, and `intake_list` then shows `ack.state` `received` with `by` the caller and `overdue` false at `0m`; the same ack again returns `unchanged` true and adds no comment; `state=parked` then shows `parked` |
| I4 | `intake_ack` refuses and says why: an issue without the label; `state` `done` (the refusal lists the four); a `note` holding a record marker |
| I5 | (by hand) An ack marker pasted in a comment by a login that is not a record author is ignored: `intake_list` still shows the trusted ack, or null |

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
