# 06. Tools

Names and argument names are the contract: the kit's skills call them literally. Types are
JSON Schema types. `repo` is always `owner/repo`; `project` is always `owner/number`.
"Class" is the preset class from [transport-and-identity](transport-and-identity.md#presets).

Common rules for every tool:

- `repo` and `project` are checked against the allowlists before anything else. When a tool
  allows them to be omitted, the server's default is used, and a server with no default
  refuses.
- Tools that do not use `project` MUST still accept it and ignore it, so an agent following
  "pass `repo` and `project` on every call" (BOARD.md rule 2) is never refused for it.
- Reads re-read GitHub; no cross-request cache ([architecture](architecture.md#where-state-lives)).
- Results are structured content. A list result that can be long is paged with
  `limit` and `cursor`, and returns `has_next_page` and `next_cursor`.
- A single-select value (Status, Priority, Size) is resolved by **name** against the
  board's live options at call time; an unknown name refuses and lists the real ones.

## Level: Core

### Identity and context

| Tool | Class | Arguments | Returns |
| --- | --- | --- | --- |
| `whoami` | desk | none | see [transport-and-identity](transport-and-identity.md#whoami) |
| `profile_list` | read | none | `profiles`: `{name, description}` list, and `default` |
| `profile_get` | read | `name?` | the profile, see [repo-context-and-profiles](repo-context-and-profiles.md#profiles) |

### Finding work

| Tool | Class | Arguments | Returns |
| --- | --- | --- | --- |
| `list_next_actions` | read | `repo`, `context?` (one label; empty for all open), `limit?` (default 30) | open **issues** (never PRs) with `number`, `title`, `labels`, `url` |
| `issue_list` | read | `repo`, `state?` (`open`, `closed`, `all`), `labels?` (all must match), `limit?` | the same shape |
| `issue_blocked_by_list` | read | `repo`, `number` | the issues blocking it (native blocked-by links), each with `repo`, `number`, `title`, `state` |
| `project_get` | read | `project` | board `id`, `title`, `url`, `fields` (name, type, options), `status_options` (the live column names) |
| `project_items` | read | `project`, `limit?` (1 to 100, default 50), `cursor?` | one page of items **in the board's manual order**: `repo`, `number`, `title`, `labels`, `state`, `status`, and every field value by name |
| `project_item_find` | read | `repo`, `number`, `project` | the item for that issue with every field value, archived or not; refuses if it is not on the board |
| `project_views_list` | read | `project` | the board's views: `number`, `name`, `layout`, `filter`, `fields`, `sort`, `group_by` |

### Claims and reports

Semantics and records are in [claim-records](claim-records.md). All five take `repo` and `number`,
refuse a pull request ("claim its issue instead"). `item_claim`, `item_renew` and
`item_report` refuse a closed issue; `item_get` and `item_release` work on one, so a holder
can still let go of an item a person closed to stop it (a standing lane's fast stop). Each write returns the folded item as `item_get` does, plus `event`,
`comment_url`, `board` (`{project, written}`) and `warnings`; `item_claim` also returns `ready` (below).

| Tool | Class | Further arguments | Refuses when |
| --- | --- | --- | --- |
| `item_get` | read | none | never, for an allowlisted issue |
| `item_claim` | work | `basis` (`explicit` or `inferred`, default `explicit`), `asked_by` (required for `explicit`), `pointed_in?`, `lease?` (default `2h`, max `72h`), `branch?`, `purpose?` (`work` or `review`, default `work`), `session?`, `project?` | someone else holds an unexpired lease; `session` longer than 200 characters; `review` and **any** of: `inferred`; no `session`; `session` equal to the `mandate.session` of an earlier `work` claim on the issue (below); `branch` is not a valid branch name (below); the caller already holds it ("use item_renew"); `inferred` and **any** of: no `agent-ready` label; an `agent:<x>` label names a runtime other than the caller's (`agent:any` is fine; `agent:human` always refuses); a `needs:*`, `blocked` or `agent-proposed` label; the board (when `project` is given and readable) has a `Size` that is not in the profile's `pickup_sizes`, or no Size at all |
| `item_renew` | work | `lease?`, `project?` | the caller is not the holder |
| `item_release` | work | `done`, `remaining`, `next` (all required), `handoff_to?`, `project?` | the caller is not the holder |
| `item_report` | work | `state?`, `note?`, `attention?`, `needs?`, `links?` (URL list), `project?` | none of `state`, `attention`, `note` given; `state` not in the six words; `state` from a non-holder; `attention` without `needs`, or `needs` not a `needs:*` value of the repo's profile |

`branch` names the branch the caller's commits for this item land on: the item's own
`gtd/issue-<n>` branch, or an integration (release-candidate) branch that combines
several stories. The server stores it as `mandate.branch` and never reads or writes the
branch itself. A valid name is 1 to 200 characters of letters, digits, `.`, `_`, `-` and
`/`; it does not start with `-` or `/`, end with `/`, `.` or `.lock`, or contain `..` or
`//`. Each call claims **one** item; claiming several stories for one branch is one call
per story (see [claim records](claim-records.md#several-items-one-branch)).

**Review claims.** `purpose="review"` claims an item to review it (the kit's
`board-review` skill), not to build it. It is a normal claim: one holder, a lease, the
same records and fold. `session` is an opaque name the caller gives for its own session
(a runtime session id, or a token it makes once and reuses); the server stores it as
`mandate.session` and never checks it against anything else. A review claim refuses
when its `session` matches the `mandate.session` of any earlier `claim` record on the
issue whose purpose is `work` (a missing `purpose` reads as `work`), so **no session
reviews work it did**. A fresh session of the same principal may review: the principal is
not compared. The check is honest-mistake protection, not a defence against a caller that
lies about its session. `item_ready` is not run for a review claim, and `ready` is null.

**The ready verdict on a claim.** A server that offers `item_ready`
([ready check](ready-check.md)) runs it on the issue before it writes the claim and returns
the answer as `ready`: `{verdict, missing, blockers}`, the same values `item_ready` gives
for that issue and board. A verdict other than `ready` adds one line to `warnings` naming
the verdict and the failed rules (`not ready: needs-refinement (acceptance-criteria)`).
The claim **never refuses on the verdict**, for `explicit` or `inferred`: a person who
pointed an agent at an item has made the call, and an `inferred` claim already has its
label and Size rules above. `ready` is null when the server does not offer `item_ready`,
when `item_ready` would refuse the issue (an epic), or when the check fails; a failed check
adds a warning and the claim goes ahead. Only `item_claim` returns it; `item_renew` does
not re-run the check.

`item_report` with `attention` also adds the label `needs:<needs>` to the issue (adding is
idempotent; it never removes one). A failed label write is a warning, the record stands.
`state=dropped` releases the claim. A server MUST NOT default `needs` to a particular
person's value; when the agent omits it with an `attention`, refuse and list the profile's
values (the skill then picks the profile's `owner_needs`).

### New activity

An agent that holds an item, opened a PR through `pr_open`, or takes part in a channel
must see what other people and agents wrote there since it last looked, without reading
each issue in turn. `activity_since` is that one read. It is a **pull**: it sends no
notification to anyone, so it never adds to a person's inbox (a person is notified only
when they must act).

| Tool | Class | Arguments | Returns |
| --- | --- | --- | --- |
| `activity_since` | read | `repo`, `since?` (RFC 3339; default 24 hours before the read), `limit?` (1 to 100, default 50), `cursor?` | `since` (the one used), `read_at`, `entries`, `scanned` (`{held, prs, channels}`), `warnings`, `has_next_page`, `next_cursor` |

What it covers, in `repo`, for the **caller's principal** only:

| `source` | Which issues | Which conversation |
| --- | --- | --- |
| `held` | every issue, open or closed, whose fold names the caller as holder | issue comments |
| `pr` | every pull request whose `gtd-pr` marker names the caller in `by` ([opening pull requests](#opening-pull-requests)) | issue comments, reviews (any state, with or without a body) and inline review comments |
| `channel` | every channel issue of the repo (the Channels group's rule) | issue comments |

An entry is conversation created **after** `since`: never a claim record, a run-state
record, an item body or anything else a reader parses as a record (a pasted marker from
an untrusted author is conversation, as in the fold). Entries are oldest first, ordered
by `created_at` then the entry's own id. Each has `source`, `repo`, `number`, `title`
(of the issue or PR), `kind` (`comment`, `review` or `review_comment`), `author` (the
GitHub login), `via_server`, `created_at`, `url` (of the entry) and `excerpt` (the first
500 characters of its body, empty for a bare review), plus `review_state` on a review
and `path` on a review comment.

`via_server` is true when the author is an identity the server writes as (a record
author). The server writes for every agent under that identity, and some deployments
write as a person's own account, so such an entry may be the caller's own comment,
another agent's or that person's. The caller skips only the entries whose `url` its own
writes returned.

A server may find the issues by listing those **updated** after `since` (a new comment
or review updates its issue). It caps that scan; past the cap it reads the most recently
updated first and adds a warning naming the cap.

**The cursor.** `read_at` is the read's watermark: the server's clock when the first
page was read (GitHub times are whole seconds, so a server may set it a second early). A
read lists only entries created at or before `read_at`, and every page of it returns the
same `read_at`: `next_cursor` carries it, so an entry written while the caller pages
waits for the next read instead of slipping past the cursor. Pass `next_cursor` with the
same `since` until `has_next_page` is false, then keep `read_at` and pass it as `since`
next time: each entry comes once. A caller with nothing kept omits `since` and gets the
last 24 hours; a caller that keeps `read_at` before the last page skips the entries
still unread.

### Issues

| Tool | Class | Arguments | Notes |
| --- | --- | --- | --- |
| `capture` | work | `title`, `note?`, `repo`, `labels?` | Creates an issue. `labels` follows the same rules as `issue_labels` (so `run-agent` refuses and `agent-review` is allowed), so an agent can file `agent-proposed` work in one call (BOARD.md rule 8) |
| `issue_comment` | work | `repo`, `number`, `body` | Plain comment on an issue or PR. A body containing a record marker ([claim-records](claim-records.md#record-format)) refuses: records come only from the `item_*` tools |
| `issue_labels` | work | `repo`, `number`, `add?`, `remove?`, `profile?` | Adds and removes labels the repo's profile declares, plus any `area:*`. A label outside the profile refuses and lists the profile's labels. Adding `run-agent` refuses (a person, or a server's own dispatch tool, starts a run); adding `agent-review` is allowed (an agent may ask another session to review its work); removing either is allowed. `profile` defaults to the repo's `gtd-context.json`. Does **not** set Status |

### Optional on Core, needed by some skills

| Tool | Class | Arguments | Notes |
| --- | --- | --- | --- |
| `project_report` | work | `project`, `profile?`, `post?` (default false), `force?` | Builds the board's status update from labels, fields and claims: a health (`ON_TRACK`, `AT_RISK`, `OFF_TRACK`) and sections for "step in", "in flight", "done this week", "progress". With `post`, posts it only when the health changed or the last post is a week old, unless `force` |

## Level: Board

All take `project`. Writes to an issue's item add the issue to the board first if needed.

| Tool | Class | Arguments | Notes |
| --- | --- | --- | --- |
| `project_add_item` | work | `repo`, `number`, `project` | Returns the item id |
| `project_set_status` | work | `repo`, `number`, `status`, `project` | Status by column name, live options; used where the repo has no bridge |
| `project_set_field` | work | `repo`, `number`, `field`, `value?`, `clear?`, `project` | Any field by name. Single select by option name; text and number as text; date as `YYYY-MM-DD`. `clear=true` clears |
| `project_item_move` | work | (`repo` and `number`) or `item_id`; (`after_repo` and `after_number`) or `after_item_id`, or none for the top; `project` | Changes the board's manual order (the queue) |
| `project_item_archive` | work | `repo`, `number`, `unarchive?`, `project` | |
| `project_status_update` | work | `body` (at most 2048 bytes), `state?`, `project` | Posts a board-level status update |
| `project_draft_add`, `project_draft_update`, `project_draft_convert` | work | draft `title`, `body`; `item_id`; target `repo` | Draft items and turning one into an issue |

## Optional groups

A server MAY offer any of these. A repo that relies on one says so in its
`.gtd/BOARD.local.md`; the core skills never require them. Names are reserved: a server
that offers the capability uses the name.

| Group | Tools | What for |
| --- | --- | --- |
| Issue structure | `issue_update`, `issue_close`, `issue_reopen`, `issue_assign`, `issue_milestone`, `issue_type_set`, `issue_parent`, `sub_issue_add`, `sub_issue_remove`, `sub_issues_list`, `issue_blocked_by_add`, `issue_blocked_by_remove` (work, lists read). `issue_close` takes `repo`, `number`, `reason?` (`completed` or `not_planned`); the blocked-by pair takes `repo`, `number`, `blocker`, `blocker_repo?`, and `issue_blocked_by_add` passes GitHub's reason through when GitHub refuses a link (it refuses a dependency cycle); `sub_issue_add` takes `repo`, `parent`, `child`, `child_repo?`, `replace_parent?`; `issue_type_set` takes `repo`, `number`, `issue_type` or `clear`; `issue_parent` (read) returns an issue's parent or null. `sub_issue_add` and `issue_type_set` refuse a write that breaks a [parent rule](repo-context-and-profiles.md#kinds), naming the rule | Editing issues beyond labels |
| Readiness | `item_ready` (read): `repo`, `number`, `project?` | Whether a story is ready to build: `ready`, `needs-refinement` (with what is missing) or `ready-blocked`, by the rules in [ready check](ready-check.md). Writes nothing |
| Board lifecycle | `project_create`, `project_update`, `project_template`, `project_copy`, `project_link_repo`, `project_views`, `project_reconcile`, `project_field_update`, `project_field_delete`, `project_item_remove`, `project_workflows`, `project_workflow_delete` (full) | Making and shaping boards from a profile |
| Repo setup | `repo_reconcile_labels`, `work_items_plan`, `work_items_sync` (full; plan is read) | Making a repo's labels and issues match its profile and its files. A sync shows the items' [typed links](typed-links.md) on both ends and makes `depends-on` a native blocked-by |
| Customization | `profile_updates` (read): `repo`, `project?`; returns `profile`, `overrides` (the repo's explicit ones), `inferred` (from the ledger, each `{kind, name, mode}`) and `updates` (each an [upstream change notice](repo-context-and-profiles.md#upstream-change-notice)) | Surfacing profile changes to items the repo skipped or reshaped. A reconciler in the Board lifecycle or Repo setup groups follows [what a reconciler does](repo-context-and-profiles.md#what-a-reconciler-does) |
| Actions | `actions_workflows`, `actions_runs`, `actions_run_get`, `actions_logs` (read); `actions_run`, `actions_rerun`, `actions_cancel` (full) | Reading and driving CI |
| Org setup | `org_issue_types`, `org_issue_type_set`, `webhook_*`, `repo_variables`, `repo_variable_set`, `repo_variable_delete` (full) | Organisation issue types, webhooks, variables. Webhook targets must be on an operator host allowlist |
| Run state | `run_state_post` (work), `run_state_read` (read) | Long runs on compute hosts post `start`, `phase`, `end`, `hold`, `release`, `spend` events to a run-state channel issue named in the repo's layer. `by` here is provenance text, not identity: the record is still stamped with the principal |
| Channels | `channels_list`, `channel_comments_read` (read), `channel_comment_post` (work) | Long-lived discussion issues a repo names as channels |
| Dispatch | `dispatch`, `review_status`, `clarify`, `organize` | Starting an agent run from a label, reading review state, GTD clarify and organize steps. A server that starts runs from `run-agent` also starts a review run from `agent-review`: see [review requests](#review-requests) |
| Issue artifacts | `issue_artifact_list`, `issue_artifact_get` (read); `issue_artifact_create`, `issue_artifact_update` (work) | Evidence and plans kept on an issue as GitHub issue artifacts. See [issue artifacts](#issue-artifacts) |
| Pull requests | `pr_open` (work) | Opening a pull request under the server's own identity for the agent that asked, so the owner can review and approve it. See [opening pull requests](#opening-pull-requests) |

`project_views` (create a profile's views) is a write and sits in `full`. Agents that only
need to **read** views use `project_views_list` (read).

## Opening pull requests

An author can never approve their own pull request on GitHub. When an agent opens a PR
with a GitHub tool signed in as the owner, the owner is the author and cannot be its
required reviewer. `pr_open` lets the server open the PR instead: GitHub records the
server's own App as the author, and the PR records which principal asked for it. The
agent's identity comes from its sign-in, so no agent needs a GitHub App of its own.

The agent still pushes its branch first, with whatever git access its host gives it.
`pr_open` only opens the PR.

| Argument | Type | Notes |
| --- | --- | --- |
| `repo` | string | `owner/repo`, checked against the allowlist |
| `head` | string | A branch in `repo`. A cross-repository head (`owner:branch`) refuses |
| `base` | string, optional | The branch to merge into. Defaults to the repo's default branch |
| `title` | string | At most 256 characters |
| `body` | string | At most 60000 characters. The server adds the provenance block below |
| `issues` | integer list | The issues this PR works on, at least one. The caller must hold a live claim on each ([claim-records](claim-records.md)) |
| `draft` | boolean, optional | Default false |
| `closes` | boolean, optional | Default false. True only when the work is verified (tested). See below |

The server MUST, in this order, refuse before it creates anything when:

1. `repo` is not allowed (P5);
2. `title` or `body` is too long (X3), or `body` already holds a `gtd-pr` marker (below),
   or `body` holds a **closing keyword** before an issue reference (below);
3. `issues` is empty, or the caller does not hold an unexpired lease on one of them. The
   refusal names each such issue and says to claim it first;
4. `head` is cross-repository, equals `base`, is not a branch of `repo`, or already has an
   open PR into `base` (the refusal gives that PR's URL);
5. a commit message between `base` and `head` holds a closing keyword before an issue
   reference. The refusal names the commit and says to reword it.

**Closing keywords.** GitHub closes an issue when a PR merges into the default branch and
its body or one of its commit messages says `close`, `closes`, `closed`, `fix`, `fixes`,
`fixed`, `resolve`, `resolves` or `resolved` (any case, optionally followed by `:`) then
an issue reference: `#<n>`, `owner/repo#<n>`, or an issue URL. It does this anywhere in the
text, so a rollback note such as "hold or close #<n>" closes that item on merge. That breaks
the items that must stay open (a lane's item, a standing chore) and closes stories before
anyone tested them. Only the server writes a closing line (`closes`, below), so it refuses
the caller's text that holds one, in either mode, and names the keyword and the reference.
The refusal says `closing keyword`. A branch name never closes an issue.

Then it opens the PR **with its own GitHub App credential, never the caller's**, even on a
server that otherwise acts as the caller. A server without such a credential does not offer
`pr_open`. The body it writes is the caller's `body`, a blank line, then this block:

```text
---
Opened through the gtd MCP server for **agent:example**. Works on #<first issue>, #<second issue>.

<!-- gtd-pr v1 {"by": "agent:example", "issues": [12, 15], "t": "2026-01-01T12:00:00Z", "v": 1} -->
```

- `by` is the caller's principal from its token (S1); there is no argument for it.
- The visible line says `Closes #n` for each issue instead of `Works on #n` only when
  `closes` is true, the PR is not a draft, and `base` is the repo's default branch, so
  merging closes the stories. Any other PR leaves its issues open for a person to close
  after testing.
- The JSON follows the record rules in [claim-records](claim-records.md#record-format):
  `<` and `>` escaped, keys sorted.

It returns `number`, `url`, `author` (the login GitHub shows as author), `by`, `head`,
`base`, `draft`, `issues`, `closes` (whether merging closes the issues) and `body` (the
body as written, with the block).

`pr_open` is `work`, so a `work` agent can use it. It changes nothing else: no labels, no
Status, no claim records; the agent reports with the `item_*` tools as usual.

Two GitHub settings decide whether the owner can then approve:

- The owner reviews as themselves, which works because the App is the author.
- A branch rule that requires approval of the most recent push refuses a reviewer who made
  that push. If the agent's host pushes with the owner's own credential, the owner cannot
  approve under that rule. Turn the rule off, or have the agent push with an identity that
  is not the owner's.

## Issue artifacts

GitHub issue artifacts are named, versioned pieces of content attached to an issue
(GitHub calls the feature a public preview). The kit uses them for evidence and plans
that should stay on the issue after its PR merges
([where evidence goes](../knowledge/model/evidence-places.md)).

| Tool | Class | Arguments | Returns |
| --- | --- | --- | --- |
| `issue_artifact_list` | read | `repo`, `number`, `type?` | Each artifact's `number`, `type`, `name`, `url`, `updated_at` |
| `issue_artifact_get` | read | `repo`, `number`, `artifact` | The artifact with `body` and `versions` (how many) |
| `issue_artifact_create` | work | `repo`, `number`, `type`, `name`, `body` | The artifact as `issue_artifact_get` returns it |
| `issue_artifact_update` | work | `repo`, `number`, `artifact`, `name?`, `body?` | The same; GitHub keeps the old version |

- `type` is one of GitHub's four: `generic` (a Markdown document), `plan` (a Markdown
  plan), `link` (the body is one `https` URL) or `embedded_html` (a self-contained HTML
  file). Any other value refuses and lists the four.
- `name` is 1 to 256 characters; `body` is at most 60000 characters (X3). A `link` body
  that is not a single `https` URL refuses.
- A body holding a record marker or a `gtd-pr` marker refuses, as `issue_comment` does.
- There is no delete tool: deleting an artifact also deletes its history, so only a
  person deletes one. A server offers all four tools or none.
- The repo and issue are checked against the allowlist first (P5); a pull request number
  refuses.

## Review requests

`agent-review` is a person's request for an agent to **review an issue**, distinct from
`agent-ready` (permission to build) and `run-agent` (build now). A person adds it, or an
agent asks for a second look at its own finished work; either way the reviewer is another
session, because a review claim (`item_claim` with `purpose="review"`) refuses the session
that claimed the item to work it. A server in the Dispatch group
that starts runs from `run-agent` treats `agent-review` the same way, with the review
procedure of the kit's `board-review` skill as the task. Without such a server, an agent
that is pointed at the board finds these items with `list_next_actions(context=
"agent-review")`.

A review changes no text the person wrote, adds no `agent-ready` and starts no build. It
ends with one comment of findings, the label removed and a report.

