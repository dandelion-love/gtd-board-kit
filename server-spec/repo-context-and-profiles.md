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
| `overrides` | no | The repo's deliberate departures from its profile ([below](#per-repo-customization-and-upstream-changes)) |

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
| `fingerprint` on every label, field and view | string | That item's declaration fingerprint ([below](#fingerprints)) |
| `pickup_sizes` | list of strings | Size options an unpointed (`inferred`) pickup may take. Default `XS`, `S`, `M` |
| `status_for_label` | list of rules | The label-to-Status map ([below](#the-label-to-status-map)) |

A server MAY return more (item types, done checks, file sources); item types follow
[Kinds](#kinds). The repo's
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

### Kinds

What an item **is** is its Kind ([how work decomposes](../knowledge/decisions/decomposition-standard.md)).
These are the standard Kinds. A profile uses the ones its repos need and MAY add domain
Kinds of its own (an experiment, a benchmark):

| Kind | Level | Done when |
| --- | --- | --- |
| `epic` | Top; holds stories | Every child is closed and its own outcome check passed, confirmed by a person |
| `story` | Under an epic | Its acceptance criteria are met and its PR merged by a person |
| `chore` | Story level: technical work with its own PR (an enabler, tech debt) | Its PR merged and the technical outcome shown |
| `bug` | Story level | A failing repro now passes and the fix merged |
| `spike` | Story level, timeboxed | A finding merged and the next step decided |
| `research` | Story level, or an epic when it needs several stories | Sourced knowledge concepts merged and reviewed by a person |
| `finding` | The issue that records a result | A person reviewed it |

A **step** is not a Kind: it is a checklist item (or sub-issue) inside a story, with no PR
of its own.

**Retired Kinds.** A profile MUST NOT declare these, as an item type or as a label:

| Retired | What replaces it |
| --- | --- |
| `task` | `chore` when it has its own PR, otherwise a step in its story |
| `question` | `attention` plus a `needs:<who>` label on the item it blocks ([report vocabulary](../knowledge/model/report-vocabulary.md)); its own `chore` or `spike` only when answering it is work |
| `decision` | A Decision concept in the repo's knowledge bundle, added by the PR of the story that made it and linked from its epic |

**Carriers.** A Kind is an organization Issue Type named after it in title case (`Chore`).
A repo without Issue Types (a personal account) uses a `kind:<kind>` label instead; a repo
that has Issue Types never carries both.

When `profile_get` returns `item_types` (a list of `{name, issue_type?, ...}`, each the
vocabulary of one kind of item), no entry's `name` or `issue_type` may be a retired Kind,
compared without case.

**Parent rules.** GitHub accepts any sub-issue under any issue; the kit does not. A
server that offers the Issue structure tools ([tools](tools.md#optional-groups)) checks
every link it makes (`sub_issue_add`) and every Kind it sets (`issue_type_set`) against
these rules, and refuses a write that breaks one, naming the
rule. An issue's Kind is read as `item_ready` reads it: its Issue Type's name, else its
`kind:<kind>` label, lower case; an issue with neither has no Kind. A **standard Kind** is
one in the table above; a profile's domain Kinds, retired Kinds still on old issues, and
no Kind are not standard.

| Rule | A link from parent P to child C refuses when |
| --- | --- |
| `epic-is-top` | C is an `epic`. An epic is never a sub-issue |
| `epic-holds-stories` | P is an `epic` and C is a `finding` or has no Kind. An epic holds story-level work (`story`, `chore`, `bug`, `spike`, `research`, or a domain Kind) |
| `holds-steps` | P is a `story`, `chore` or `bug` and C has a standard Kind; or P is a `spike` and C has a standard Kind other than `finding`. Their sub-issues are steps, with no Kind and no PR of their own; a spike's finding records its result |
| `finding-holds-nothing` | P is a `finding`. A finding has no sub-issues |
| `retired-kind` | (on `issue_type_set`) the new type is a [retired Kind](#kinds), compared without case. The refusal names the Kind that replaces it |

A `research` issue is story-level work or, when it needs several stories, an epic, so it
may hold any Kind but an epic. A domain Kind as P is not checked.

`issue_type_set` checks the new Kind both ways: against the issue's parent (the issue as
C) and against each of its sub-issues (the issue as P). Clearing the type checks the
issue as C with no Kind. A refused write changes nothing: no link, no type. Links made
outside the server (GitHub's own UI) are not checked; the rules bind what the server
writes. The golden pairs are in [kind_cases.json](../conformance/kind_cases.json).

**Moving a repo off the retired Kinds** happens when it next repins the kit. Issues of
Issue Type `Task` (or label `kind:task`) move to `Chore` (`kind:chore`), or become steps of
the story they belong to. An open question moves onto the item it blocks as `attention`
plus `needs:<who>`, and the question issue closes with a link. A decision issue's content
moves into a Decision concept, and the issue closes with a link. A reconciler never
deletes an Issue Type or a label ([what a reconciler does](#what-a-reconciler-does)), so
a person disables the retired Issue Types once no open issue uses them. The repo's
[per-repo layer](../knowledge/decisions/per-repo-layer.md) may keep an old name for a
while, and says so.

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

## Per-repo customization and upstream changes

A profile is a starting point. A repo may delete a view it does not want, reshape a
field, or recolour a label, and the next reconcile must not undo that. When the profile
later changes an item the repo departed from, the change must not be applied, and it must
not be lost either: an agent surfaces it so a person can choose.

This section covers labels, board fields and board views (the **items**). It applies to
any reconciler: a nightly job, an MCP tool such as `project_reconcile`, or a script.

### Fingerprints

An item's **fingerprint** is the first 12 hex digits of the SHA-256 of its declaration in
canonical JSON: the item's object as `profile_get` returns it, without its `fingerprint`
key and without the advisory key `manual` (steps for a person, which reconcile never
applies, so rewording them is no upstream change), serialised with object keys sorted by code point, no whitespace (`,` and `:` as
separators), non-ASCII characters written as themselves, and encoded as UTF-8. In Python:

```python
item = {k: v for k, v in item.items() if k not in ("fingerprint", "manual")}
hashlib.sha256(json.dumps(item, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False).encode()).hexdigest()[:12]
```

Golden values: `{"name": "Inbox", "layout": "table", "filter": "status:Inbox"}` gives
`9c5ee7e85d3e`, and `{"name": "Engage — Now", "layout": "board"}` (an em dash) gives
`14d526f52c0e`.

Two declarations with the same fingerprint are the same declaration. A server that
returns `fingerprint` MUST compute it this way, so a fingerprint recorded by one tool can
be compared by another.

### Comparable shapes

A fingerprint identifies a **declaration**; it is never compared with a live item, which
the platform reports back normalised and without advisory keys. A reconciler compares a
live item with a declaration, or with what it last set, by the item's **comparable
shape**: only what the platform reads back.

| Kind | Name match | Comparable shape |
| --- | --- | --- |
| label | case-insensitive | colour as six lowercase hex digits (no `#`), description (missing = empty) |
| field | exact | type; for a single select, its option names in order |
| view | exact | layout, filter (trimmed), group-by field names, column field names |

A reconciler MAY compare more of a view (visible fields, sort) when its platform reads
them back reliably, but then MUST do so both when it records and when it compares.

### Overrides: the repo's explicit choices

`overrides` in `.github/gtd-context.json` names items by kind and name:

```json
{
  "overrides": {
    "views":  {"Roadmap": {"mode": "skip", "seen": "3f2a9c01b7de"}},
    "fields": {"Priority": {"mode": "keep"}},
    "labels": {"area:docs": {"mode": "keep", "seen": "b1c4e0a95f13"}}
  }
}
```

| Key | Meaning |
| --- | --- |
| `mode: skip` | Never create the item. If it exists, leave it alone |
| `mode: keep` | The item may exist, but its shape is the repo's: never reset, rename or recreate it |
| `mode: follow` | Follow the profile: cancels an inferred mode, so a deleted item is created again |
| `seen` | Optional. The fingerprint of the profile's declaration the repo last decided about, or `removed` once the repo has decided about the profile dropping the item |

A change to `overrides` is a change to a tracked file, so it goes through review like any
other. A server MUST NOT trust it for authorization.

### The ledger: choices inferred from what a person did

A person who deletes a view in the board's UI has made a choice without writing it down. A
reconciler that creates items SHOULD keep a **ledger** of the items it created, each with
the fingerprint it created from. Where the ledger lives is the deployment's choice (for
example the board's own description), but it MUST survive between runs and be readable
by `profile_updates`.

From the ledger, a reconciler infers:

| Ledger says | Board has | Inferred mode |
| --- | --- | --- |
| created | no such item | `skip` (a person deleted it) |
| created | the item, its shape differing from the shape the reconciler last set | `keep` (a person reshaped it) |
| created | the item, in the shape the reconciler last set | none: the item still follows the profile |
| nothing | the item, differing from the profile's declaration | `keep`, with no recorded fingerprint (it predates the ledger, so whose change it is is unknown) |

An explicit override wins over an inferred one. An item whose live shape matches the
profile's current declaration has no inferred mode, whatever the ledger says. An item
that is neither in the ledger nor in `overrides` and is missing from the board is new: a
reconciler creates it as usual. An inferred `skip` of an item the profile no longer
declares is no notice (both sides dropped it), and the reconciler forgets it.

So the ledger holds, per item, the fingerprint of the declaration it applied and the
shape it set (or that shape's fingerprint). A reconciler infers only from a **complete**
read of the board or repo: when a read fails or may be partial (an unfinished page, an
error), it infers nothing and writes nothing that depends on the ledger for that target
in that run. Inferred modes are recomputed every run, never stored as overrides.

**Shared boards.** Fields and views belong to the board, and several repos may name one
board. A reconciler then combines their overrides for board items: a departure wins over
`follow` (`keep` over `skip`), the `seen` of the winning entry is used, and a
disagreement between repos is reported for a person. Labels belong to each repo and are
never combined.

### What a reconciler does

1. It never creates an item whose mode is `skip`, and never changes, renames or recreates
   an item whose mode is `keep`.
2. It never deletes an item, including one the profile no longer declares.
3. For each item whose mode is `skip` or `keep` (a departure from the profile; `follow`
   is not one, and an item with `follow` is reconciled like any other), it compares the
   profile's current fingerprint with the recorded one: `seen`, else the ledger's
   fingerprint for the item. When they differ, or when no fingerprint is recorded at all,
   it reports an **upstream change**. When the profile no longer declares the item, it
   reports one unless `seen` is `removed`, or the item is in neither the ledger nor a
   `seen` (a repo's own item the profile never had). Either way it writes nothing for
   that item.
4. It lists upstream changes in its plan and apply output, and SHOULD keep them visible
   in one place in the repo (for example one open issue labelled `needs:triage` that it
   updates rather than duplicates).
5. When a person decides, the decision is recorded in `overrides`: the same `mode` with
   `seen` set to the current fingerprint (or to `removed`, for a `removed` notice) keeps
   the repo's choice; `follow` (for an inferred mode) or removing the entry (for an
   explicit one) takes the profile's version. A tool that writes an override always
   writes `seen`: an override without one stays an upstream change until a person
   records one. The next
   reconcile then creates a missing item, and reports a differing one as work for a person
   where the platform cannot update it in place. Once the item matches the profile
   again, a `follow` entry can be removed.

### Upstream change notice

`profile_updates` returns, and a reconciler reports, each upstream change as:

| Field | Meaning |
| --- | --- |
| `kind` | `label`, `field` or `view` |
| `name` | The item's name |
| `mode` | `skip` or `keep` |
| `source` | `explicit` (from `overrides`) or `inferred` (from the ledger) |
| `change` | `changed` (the declaration differs) or `removed` (the profile no longer declares it) |
| `seen` | The recorded fingerprint, or null when none was recorded |
| `current` | The profile's fingerprint now, or null for `removed` |
| `declaration` | The profile's declaration now, or null for `removed`, so an agent can show what is new |

The list is empty when nothing a repo departed from has changed. An item with a mode whose
fingerprint matches is not a notice.
