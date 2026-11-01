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
`comment_url`, `board` (`{project, written}`) and `warnings`.

| Tool | Class | Further arguments | Refuses when |
| --- | --- | --- | --- |
| `item_get` | read | none | never, for an allowlisted issue |
| `item_claim` | work | `basis` (`explicit` or `inferred`, default `explicit`), `asked_by` (required for `explicit`), `pointed_in?`, `lease?` (default `2h`, max `72h`), `project?` | someone else holds an unexpired lease; the caller already holds it ("use item_renew"); `inferred` and **any** of: no `agent-ready` label; an `agent:<x>` label names a runtime other than the caller's (`agent:any` is fine; `agent:human` always refuses); a `needs:*`, `blocked` or `agent-proposed` label; the board (when `project` is given and readable) has a `Size` that is not in the profile's `pickup_sizes`, or no Size at all |
| `item_renew` | work | `lease?`, `project?` | the caller is not the holder |
| `item_release` | work | `done`, `remaining`, `next` (all required), `handoff_to?`, `project?` | the caller is not the holder |
| `item_report` | work | `state?`, `note?`, `attention?`, `needs?`, `links?` (URL list), `project?` | none of `state`, `attention`, `note` given; `state` not in the six words; `state` from a non-holder; `attention` without `needs`, or `needs` not a `needs:*` value of the repo's profile |

`item_report` with `attention` also adds the label `needs:<needs>` to the issue (adding is
idempotent; it never removes one). A failed label write is a warning, the record stands.
`state=dropped` releases the claim. A server MUST NOT default `needs` to a particular
person's value; when the agent omits it with an `attention`, refuse and list the profile's
values (the skill then picks the profile's `owner_needs`).

### Issues

| Tool | Class | Arguments | Notes |
| --- | --- | --- | --- |
| `capture` | work | `title`, `note?`, `repo`, `labels?` | Creates an issue. `labels` follows the same rules as `issue_labels` (and `run-agent` refuses), so an agent can file `agent-proposed` work in one call (BOARD.md rule 8) |
| `issue_comment` | work | `repo`, `number`, `body` | Plain comment on an issue or PR. A body containing a record marker ([claim-records](claim-records.md#record-format)) refuses: records come only from the `item_*` tools |
| `issue_labels` | work | `repo`, `number`, `add?`, `remove?`, `profile?` | Adds and removes labels the repo's profile declares, plus any `area:*`. A label outside the profile refuses and lists the profile's labels. Adding `run-agent` refuses (a person, or a server's own dispatch tool, starts a run). `profile` defaults to the repo's `gtd-context.json`. Does **not** set Status |

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
| Issue structure | `issue_update`, `issue_close`, `issue_reopen`, `issue_assign`, `issue_milestone`, `issue_type_set`, `issue_parent`, `sub_issue_add`, `sub_issue_remove`, `sub_issues_list`, `issue_blocked_by_add`, `issue_blocked_by_remove` (work, lists read) | Editing issues beyond labels |
| Board lifecycle | `project_create`, `project_update`, `project_template`, `project_copy`, `project_link_repo`, `project_views`, `project_reconcile`, `project_field_update`, `project_field_delete`, `project_item_remove`, `project_workflows`, `project_workflow_delete` (full) | Making and shaping boards from a profile |
| Repo setup | `repo_reconcile_labels`, `work_items_plan`, `work_items_sync` (full; plan is read) | Making a repo's labels and issues match its profile and its files |
| Actions | `actions_workflows`, `actions_runs`, `actions_run_get`, `actions_logs` (read); `actions_run`, `actions_rerun`, `actions_cancel` (full) | Reading and driving CI |
| Org setup | `org_issue_types`, `org_issue_type_set`, `webhook_*`, `repo_variables`, `repo_variable_set`, `repo_variable_delete` (full) | Organisation issue types, webhooks, variables. Webhook targets must be on an operator host allowlist |
| Run state | `run_state_post` (work), `run_state_read` (read) | Long runs on compute hosts post `start`, `phase`, `end`, `hold`, `release`, `spend` events to a run-state channel issue named in the repo's layer. `by` here is provenance text, not identity: the record is still stamped with the principal |
| Channels | `channels_list`, `channel_comments_read` (read), `channel_comment_post` (work) | Long-lived discussion issues a repo names as channels |
| Dispatch | `dispatch`, `review_status`, `clarify`, `organize` | Starting an agent run from a label, reading review state, GTD clarify and organize steps |

`project_views` (create a profile's views) is a write and sits in `full`. Agents that only
need to **read** views use `project_views_list` (read).
