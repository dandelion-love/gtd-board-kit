# 16. Register records

A register is an append-only log of records about items: experiments, benchmarks (listening
tests and other instruments) and findings. [Record pages](record-pages.md) fix where the
records live and how a page grows. This section fixes **what a record says**: the envelope
every record carries, the events of each register and the fields each requires, how an older
record is read in the current shape without being changed, how a register folds into an
item's state, and how that state shows on GitHub. The reference implementation is
[conformance/register_records.py](../conformance/register_records.py); the schemas are in
[schemas/register-records/](schemas/register-records/); checks RR1 to RR4 run the golden
cases in [conformance/record_cases.json](../conformance/record_cases.json).

Why: a register written by several tools and many agents drifts when each tool restates the
rules. One schema, one validator and one upgrader, copied by every writer and reader and held
to the same cases, is the one place the rules change.

## The envelope

Every record a writer writes carries these fields. The line hash (the sha256 of the exact
line) stays what anything else cites.

| Field | Type | Meaning |
| --- | --- | --- |
| `event` | string | The event, one of its register's events below |
| `v` | integer | The schema version of this event's shape. The current version is 1. A record without `v` is version 0 |
| `id` | string | The item the record is about (a link's source item) |
| `eid` | string | A unique id for this record, minted by the writer: a ULID (26 characters of Crockford base32) |
| `t` | string | When, `YYYY-MM-DD HH:MM:SS+00:00`: UTC, with its offset |
| `by` | string | Who decided it, as a principal ([transport and identity](transport-and-identity.md)): `agent:<name>` or `<idp>:<id>` |
| `for` | string | Optional: on whose instruction, when an agent records a person's decision |
| `via` | string | What wrote it: `<tool>@<version or commit>` |
| `note` | string | Free text for a person, where the event takes one |

Rules:

- **Order is the page's order**, never `t`. `t` orders a merged view across pages only.
- **`eid` makes a write idempotent.** A writer given a record whose `eid` is already in the
  register writes nothing when the line is byte-identical, and refuses (`eid-reused`) when it
  is not.
- No machine names. `via` names a tool, not a host.

## Events

A field listed as required must be present and not empty. Fields that are not listed are
allowed and kept; a writer reports them (`unknown-fields`, a warning, not a refusal) so a new
habit is seen. A field becomes required only in a new version. "Or `none: <reason>`" means
the value is either the thing itself or a string starting `none:` that says why not, so the
author always answers the question.

### Experiment

| Event | Required | Rules |
| --- | --- | --- |
| `register` | `title`, `rule_hash`, `spec` | `spec` requires `hypothesis`, `arms`, `n_planned`, `metric`, `decision_rule` (an object: verdict name to condition), `falsified_by`, `void_if`, `cannot_answer`, `resolves`, `prereg` (`CLEAN`, `PARTIAL` or `POST-HOC`), `preregistered_by`, and `baseline` (the arm or item the result is read against, or `none: <reason>`); `stopping_rule` when `arms` has more than one entry. Optional `spec_file`: `{path, resolved_sha256, code_commit}` |
| `launch` | `resource` | Queued behind other work |
| `start` | `resource` | Running |
| `attempt` | `instance`, `outcome`, `hours`, `cost_estimated`, `cost_is_estimate` | `outcome`: `completed`, `failed`, `killed`, `preempted`, `unknown`. Optional `resumed_from`: `{eid, step}` |
| `observation` | `kind`, `title` | `kind`: `finding`, `threat`, `precondition`, `provenance`, `instrument`, `sealed`, `note` |
| `deviation` | `what`, `original`, `reason`, `timing`, `impact` | A change from the registration. `timing`: `before-data`, `after-data-access`, `after-results-known` |
| `result` | `verdict`, `rule_hash`, `note` | `verdict` is a key of the registration's `decision_rule`, or `VOID`. Optional `data`, `artifacts` (a list of `{path or uri, sha256, role}`), `code` (`{commit, dirty}`), `run_dirs`, `env` |
| `reading` | `of`, `kind`, `says`, `because` | What a result means now; the result is unchanged. `of`: the sha256 of the result line read, or null for the experiment as a whole. `kind`: `interim`, `reading`, `stage-read`, `exploratory`, `ruling` |
| `link`, `unlink` | `to`, `kind`, `why` | An item link ([typed links](typed-links.md)) |
| `artifact` | `kind`, `why`, and `url` or `local` | A pointer to something outside the register. `kind`: `run`, `pr`, `checkpoint`, `bucket`, `hub`, `page`, `other` |
| `block`, `unblock` | `note` | |
| `retire`, `unretire` | `kind`, `note` | `retire` `kind`: `void`, `abandoned`, `superseded`, `retired`. `unretire` needs `note` only |

### Benchmark

| Event | Required | Rules |
| --- | --- | --- |
| `register` | `title`, `spec_hash`, `spec`, `experiments` | `spec` requires `question`, `arms`, `material`, `metric`, `resolves`, `cannot_answer`, `decision_rule` (an object, or the string `DESCRIPTIVE`), `instrument` (`{profile, version}`, the instrument definition used), `listener`, `positive_control` (the case shown to detect the kind of difference ruled out, or `none: <reason>`) and `reference_anchor` (what the judge hears first as the scale, or `none: <reason>`). Optional `screening`: rules that drop a judge or a trial, declared before judging |
| `result` | `status`, `measured`, `judged`, `available`, `note` | `status`: `complete`, `partial`, `withdrawn`. Optional `verdict` (a key of `decision_rule`), `artifacts` |
| `reading` | `of`, `kind`, `says`, `because`, `changes` | `kind` as for an experiment |
| `deviation`, `link`, `unlink`, `artifact`, `retire`, `unretire` | as for an experiment | |

### Finding

| Event | Required | Rules |
| --- | --- | --- |
| `fact` | `section`, `statement`, `rests_on`, `caveat` | `rests_on`: a list of `{id, of, verdict}`, `of` the cited result line's sha256. Optional `supersedes`: a finding id |
| `open` | `statement`, `detail`, `rests_on` | A question tested but not settled |
| `retire` | `because` | |

## Validation

A writer validates a record before writing it and refuses on any of these. A version 0
record is checked only for `bad-json`, `unknown-event` and `missing:id`; it is never
refused for lacking what version 1 added.

| Refusal | When |
| --- | --- |
| `bad-json` | the line is not one JSON object |
| `unknown-event` | `event` is not an event of the register |
| `version-ahead` | `v` is above the version this code knows |
| `missing:<field>` | a required field is absent or empty (`spec.` prefixes a spec field) |
| `bad-type:<field>` | a field has the wrong JSON type |
| `bad-value:<field>` | a value is outside its enum, or does not match its pattern |
| `verdict-not-in-rule` | a result's verdict is neither `VOID` nor a key of the registration's `decision_rule` |
| `rule-hash-differs` | a result's `rule_hash` is not the registration's |
| `not-registered` | the item has no registration and the record is not one |
| `registered-twice` | a second registration for an item |
| `eid-reused` | the `eid` is already in the register on a different line |

The last five need the item's earlier records; the others need the record alone.

## Reading older records: the upgrade

A register's history is never rewritten. A reader passes each record through the upgrade,
which returns the current shape and lists what it assumed under `_upgraded`. The bytes, and
so the line hash, are untouched. Every reader that folds, shows or checks a register reads
through the upgrade; only the line hash is taken from the raw line.

Upgrading a version 0 record:

| Version 0 | Read as |
| --- | --- |
| `t` without an offset | that local time in the source's `timezone`; `_upgraded` names `t` |
| no `t` | `t` null; folds use page order |
| no `eid` | `eid` = `h:` and the first 24 hex digits of the line hash |
| no `by`, or a `by` that is not a principal | `by` = `unknown`, the original text kept as `by_text` |
| a `link` with `url` or `local` and no `to` | an `artifact` record with the same `kind`, `why` (else `note`) and pointer |
| an `observation` whose `kind` is not in the list | `kind` = `note`, `title` = the old `kind` |
| a registration's `spec.preregistration_status` | `spec.prereg` = `CLEAN`, `PARTIAL` or `POST-HOC` when the text opens with one; `CLEAN` when it opens "Registered" or "Written" and says "before" with no qualifying word (after, seen, informed, blocked, partial, post-hoc, not clean); else null. The text is kept as `spec.prereg_note` |
| a `reading` with no `kind` | `kind` = `reading` |
| a record with `from` and no `id` | `id` = `from` |
| a benchmark result with no `status` | `complete` when it states a verdict or `judged` is at least `available`, else `partial` |

Rules for later changes:

- Adding an optional field or a new event needs no version: readers ignore what they do not
  know.
- Making a field required, or changing what one means, raises that event's version and adds
  an upgrade step from the version before.
- A change that cannot be upgraded is a new event.
- A writer always writes the current version.

## The fold

A reader folds an item's upgraded records, in page order, into a state:

- **Experiment**: `registered`; `queued` after a `launch`; `started` after a `start`; `blocked`
  while a `block` stands (an `unblock` lifts it); `verdict` after a result whose verdict passes
  the two result checks above, `void` when that verdict is `VOID`; `unvalidated` when a result
  fails them; `void`, `abandoned` or `retired` (for `superseded` and `retired`) after a
  `retire` that no valid result precedes; an `unretire` folds as if the retire had not happened.
  A valid result is never overridden by a later retire.
- **Benchmark**: `registered`; `partial` or `complete` from its latest result's `status`
  (`withdrawn` folds back to `registered`); `void`, `abandoned` or `retired` after a retire
  unless already `complete`.
- **Finding**: `fact` or `open` from its latest record; `retired` after a retire; `stale` when,
  after the finding's own `t`, an item it rests on gains a `result`, `reading`, `deviation` or
  `artifact` record, or a link of a kind that reads evidence (`refines`, `contradicts`,
  `corroborates`, `supersedes`, `shares-listener`) from or to it. The other link kinds say how
  work was planned and change no result. Staleness is computed, never written; this is the
  one comparison across items, so it compares `t`, upgraded to UTC.

The fold also gives: the verdict, the `prereg` value, hours and cost summed over attempts,
the first `launch` or `start` time, who and on what (`by` and `resource` of the latest of
those), and the latest report (the newest `launch`, `start`, `attempt`, `result`, `block`, `unblock`,
`retire`, `unretire`, `reading` or `deviation` with a `note`, or a reading's `says`).

## On GitHub

A server that mirrors register items to issues and a board (the Repo setup group) shows
each item from its fold, the same way every time, so a person can read an item's state from
the issue alone. A profile source configures the names:

| Shown as | From | Source key |
| --- | --- | --- |
| Issue type | the item's register | the profile's item type for that register |
| Title | `<id> — <title>` | |
| Kind label | every item of the source carries it | `kind_label` |
| State labels | each label whose fold state holds, removed when it no longer holds | `state_labels`: fold state to label |
| Invalid-record label | the item holds a record that fails validation at its own version | `invalid_label` |
| Board Status | the fold state | `status_map` |
| Open or closed | closed when the Status is in `closed`, reopened when it leaves it | `closed` |
| Board fields | verdict, prereg, GPU hours, spend, start date, agent, latest report | `fields` |
| Body | the sections below | |

The body, in order: a marker; the item type; **Purpose** (an experiment's hypothesis, a
benchmark's question, a finding's statement); **Rule** (the decision rule's verdict names);
**State** (the fold state, the verdict and the latest report); **Results** (each result's
verdict or status, and the first lines of its note); **Readings** (the five newest);
**Related** ([typed links](typed-links.md)); **Record**: a link to the item's page
([record pages](record-pages.md)), never to a register file that no longer exists; and, when
any record fails validation, **Record warnings**, one line per refusal with the record's
hash. A sync owns exactly the labels it manages (the kind label, the state labels and the
invalid-record label) and never touches any other label.

## Writers

Only a writer appends a record, and every writer runs the same checks in the same order:
validation of the record alone; the checks that need the item's records; the page's
addendum-only rule ([record pages](record-pages.md)); `eid` reuse. A server tool that
appends records for a caller fills `by` from the caller's principal, `via` from itself,
`eid` and `t`, and takes none of them as arguments. A record a writer refuses is never
written. A result that carries a machine's facts (its environment, its run directories, its
measured cost) is written on that machine, not by a server.

### The Registers tools

`record_append` takes the register (`experiment`, `benchmark` or `finding`) and the record
without its envelope; it fills `v`, `eid` (unless the record brings one, for a retry), `t`,
`by` from the caller's principal and `via` from the server, then runs the checks above and
the page rule, and appends the entry as one commit on the default branch that moves only if
the branch has not moved (re-reading and re-checking on a lost race). It returns the line,
its sha256 and the page's path, or the refusals and writes nothing. It refuses an
experiment `result` or `attempt` and a benchmark `result` (`written-on-the-host`), which carry
a machine's facts. `record_get` returns the item's records upgraded, each with its line
hash and any refusals, its fold, and what [On GitHub](#on-github) shows for it.

