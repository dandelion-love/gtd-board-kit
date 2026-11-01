# 04. Repo context, profiles and labels

## `.github/gtd-context.json`

Every work repo carries this file. Agents read it from the checkout; the server reads it
through the GitHub API when a tool needs the repo's profile and none was passed.

```json
{
  "profile": "software",
  "project": "owner/number",
  "mcp_url": "https://gtd.example.com"
}
```

| Key | Required | Meaning |
| --- | --- | --- |
| `profile` | yes | The profile name the repo follows ([below](#profiles)) |
| `project` | no | The repo's board as `owner/number`. No board: board tools are not used |
| `mcp_url` | for joined agents | The server's base URL, https, no path |

A server MUST ignore keys it does not know (deployments add their own, for example a
manifest version stamp). It MUST NOT trust the file for authorization: the allowlists
decide what may be touched, the file only says what the repo intends.

## Profiles

A **profile** is a named vocabulary for one kind of repo (a software repo, a research lab,
a coordination board, a personal GTD list). It says which labels exist, which Status
columns the board has, which fields, and which views. The server holds a catalogue of
profiles; `profile_list` and `profile_get` expose it. Which profiles exist and what they
are called is the deployment's choice.

`profile_get(name)` returns at least:

| Field | Type | Meaning |
| --- | --- | --- |
| `name`, `description` | string | |
| `labels` | list of `{name, color, description}` | Every label the profile declares, the base labels below first |
| `needs` | list of strings | The `needs:*` values this profile has, without the prefix |
| `owner_needs` | string | Which `needs` value means "the owner" (the default when an agent is unsure) |
| `board.status` | list of strings | Status column names in board order |
| `board.fields` | list of `{name, type, options?}` | `type` is `single_select`, `text`, `number`, `date` or `iteration` |
| `board.views` | list of `{name, layout, filter?, sort?, group_by?, fields?}` | The views a board of this profile should have |
| `pickup_sizes` | list of strings | Size options an unpointed (`inferred`) pickup may take. Default `XS`, `S`, `M` |
| `status_for_label` | list of rules | The label-to-Status map ([below](#the-label-to-status-map)) |

A server MAY return more (item types, done checks, file sources). The repo's
`.gtd/BOARD.local.md` can narrow or rename on top of a profile; that is the agent's
business, not the server's.

### Base labels every profile has

The kit's skills rely on these names. A profile MUST declare all of them and MAY add its
own. Colours and descriptions are free.

| Family | Labels |
| --- | --- |
| Dispatch | `run-agent`, `agent-running`, `waiting-for-review`, `agent-failed`, `blocked`, `accepted` |
| Whom it waits for | `needs:triage`, plus one `needs:<owner_needs>`, plus any others the profile wants |
| Who may take it | `agent:any`, `agent:human`, plus one `agent:<runtime>` per runtime that may be routed to (`agent:claude`, `agent:codex`, ...) |
| May it be pulled | `agent-ready`, `agent-proposed` |
| Area | `area:*` is free-form; a server allows any label with that prefix |

Meanings are in [labels are signals](../knowledge/model/labels-are-signals.md).

### Board fields the kit reads or writes

A board for any profile SHOULD have these, because the skills use them by these default
names (a repo can rename them in `.gtd/BOARD.local.md`):

| Field | Type | Used for |
| --- | --- | --- |
| `Status` | single select | The column; set by the bridge or `project_set_status` |
| `Priority` | single select | Pickup order |
| `Size` | single select (`XS`, `S`, `M`, `L`, `XL`) | Whether an unpointed pickup is allowed |
| `Agent` | text | Mirror of the current holder's runtime, written by the claim tools |
| `Last report` | text | Mirror of the latest report, written by the claim tools |
| `Start date`, `Target date` | date | The ETA ([queue and ETA](../knowledge/model/queue-and-eta.md)) |

## The label-to-Status map

The map is data. A bridge reads it at run time; nothing in the bridge names a label or a
column. The default map for a profile comes from the server (`status_for_label`), and a
repo can override it with `.github/gtd-label-status-map.json` in the same shape:

```json
{
  "schema": 1,
  "status_field": "Status",
  "rules": [
    {"trigger": "closed-or-merged", "status": "Done"},
    {"trigger": "label", "label": "accepted",           "status": "Done"},
    {"trigger": "label", "label": "blocked",            "status": "Blocked"},
    {"trigger": "label", "label": "agent-failed",       "status": "Ready"},
    {"trigger": "label", "label": "waiting-for-review", "status": "In Review"},
    {"trigger": "label", "label": "agent-running",      "status": "In Progress"},
    {"trigger": "label", "label": "needs:owner",        "status": "Ready"},
    {"trigger": "label", "label": "needs:triage",       "status": "Backlog"},
    {"trigger": "label", "label": "agent-proposed",     "status": "Backlog"}
  ]
}
```

Rules (any bridge, any language):

1. **Order is precedence.** The first rule that matches wins. A closed issue or merged PR
   is matched by `closed-or-merged` before any label.
2. **No match is a no-op**, and says so in one log line. Labels outside the map never
   fail the bridge.
3. **A match naming a Status the board does not have is a hard failure**, never a silent
   skip: the board would quietly stop telling the truth.
4. Every dispatch label the skills write (`agent-running`, `waiting-for-review`,
   `agent-failed`) and every `needs:*` label of the profile is mapped.
5. The bridge leaves alone an item whose Status is owned by something else the repo
   declares (for example a file of record that mirrors to the board).
6. Writes made by the bridge's own identity must not re-trigger it (a loop guard on the
   event's sender).

The column names above are an example. Each profile's own map names its own columns.
