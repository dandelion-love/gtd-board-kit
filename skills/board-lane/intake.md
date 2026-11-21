# Intake: requests between projects

Part of the `board-lane` skill. Read `.gtd/kit/BOARD.md` and the skill's `SKILL.md`
first. Uses the server's optional Intake tools, `intake_list` and `intake_ack`
(server spec, tools, Intake). Without them, a repo with an Intake section names its
fallback in `.gtd/BOARD.local.md`.

A **request** is an open issue another project's agent files in this repo with the
intake label. It is `agent-proposed`: no agent builds it until a person says so (rule 4).
The intake's job is that the request is **seen**, **answered** and, if the path between
the projects dies, that a person **finds out**.

## The receiving end: an intake lane

An intake lane is a standing lane whose `may` is "ack requests in the intake" (and,
if the person allows, "hand back requests that belong to another project"). Its block
names `label`, `ack_within` and the owner's `needs` value in the repo's Intake section.
One tick:

1. `intake_list(repo, label, ack_within, since=<last read_at>)`. Keep `read_at`.
2. Each request with `ack` null:
   - `observe`: `item_report(state="progress", note="would ack #n received")` on the
     lane item.
   - `auto`: `intake_ack(state="received", thread=<the lane item>)`.
   Either way, if it is `new`, tell the owner in one line: what it asks and that it needs
   their call. That line is the only message; a tick with nothing new says nothing.
3. A request that belongs to another project: under `auto` with that line in `may`,
   `intake_ack(state="handed-back", note="belongs to <whose>")`. Otherwise say so to the
   owner in the same one line.
4. A request with `comments_since` above 0, or with a `reply_on` issue that has new
   conversation: read it and answer where it was written, or bring it to the owner if
   only they can answer.
5. When the owner decides, record their decision on the request: `taken` with
   `thread` = where the work is, or `parked`. The `note` quotes their words and links
   them. That decision is the work's mandate (who asked, which rule, which policy).

The lane never sets `taken` on its own, never adds `agent-ready`, and never builds a
request: that is a new item, pointed by a person.

## The intake check: clear, small, fits

The intake lane also checks each new item before it is ordered. This **reuses** the lane
above: same lane, same `intake_list` read, same owner line. What changes, and what does not:

| Part | Changes? |
| --- | --- |
| The lane block, its switch (`observe` first, then `auto`) and its `may` | no; add "check new items" to `may` |
| `intake_list`, `intake_ack` and the ack states | no; `intake_list` rows gain `check` (below) |
| One tick's order | the check comes after the ack of step 2 |
| `intake_check` (new) | records the result on the item |
| Pickup | in `enforce` mode, `list_next_actions` omits an item whose result is `needs-more` or `decline` |

Three questions, answered from the item alone:

1. **Clear**: does it say who it helps, what is wrong today and what changes, with
   criteria a person could tick? (The ready check's `acceptance-criteria` and `prose`
   rules answer most of this: `item_ready`, `prose_check`.)
2. **Small enough**: can one agent finish it in one pull request? Size XL, or an epic's
   whole plan, is not small enough.
3. **Fits**: is it work this board exists for (its purpose in `.gtd/BOARD.local.md`)?

Record the answer with `intake_check(repo, number, result, clear, small, fits, note)`:

| `result` | When | `note` |
| --- | --- | --- |
| `pass` | all three are yes | optional |
| `needs-more` | clear or small is no, and it fits | required: what to add or split |
| `decline` | it does not fit | required: why, in one line |

A sample record (the visible line a person reads; the marker follows it):

```text
Intake check: needs-more. clear: yes. small: no. fits: yes.
Note: covers three outcomes; split the export and the import.
<!-- gtd-intake-check v1 {"by": "agent:example", "clear": true, "fits": true, "note": "covers three outcomes; split the export and the import", "result": "needs-more", "small": false, "t": "2026-01-01T12:00:00Z", "v": 1} -->
```

Only the lane's principal (a checker the repo names) or the owner records a check; a worker never records one on its own item, and a later `pass` lifts the hold the server added.

An item with **no record reads `unchecked`**, never `pass`. A new check replaces the
last one. Never touch the item's text, labels or `agent-ready`: the check only records;
a person decides what to do with `needs-more` and `decline`.

**Mode.** The server's check mode is `watch` or `enforce`, and `item_get` shows it as
`intake_check.mode`. It starts in **`watch`** (the default; a server setting named
`INTAKE_CHECK_MODE`, changed only by the owner): the check records a result and blocks
nothing. In `enforce`, a `needs-more` or `decline` result also adds the owner's `needs:*`
label and keeps the item out of the pickup queue. Enforcing starts only after the owner
has read the watch record. Items that existed before the server began checking are
**grandfathered**: they read `unchecked` with `grandfathered` true and are never held in
either mode.

A tick under `observe` reports "would record needs-more on item n" and writes nothing.

## The filing end: liveness

1. File the request with `capture` in the other project's intake repo, with its label.
   Say who you are, what you ask, and where to reply (your coordination issue).
2. Track it on an item of your own: `item_report(state="waiting", note="waiting for
   <repo>#<n> ack", links=[<request url>])`.
3. Each tick of your lane: `intake_list(repo=<their repo>, label=<their label>,
   ack_within=<their ack_within>)` and find your request.
   - `ack` set: report it on your item once (`progress`); follow `thread`. `parked` or
     `handed-back` ends your wait: say so and move on.
   - `overdue`: `item_report(state="waiting", attention="no ack on <repo>#<n> after
     <ack_within>; the path between the projects may be down", needs=<owner_needs>)` on
     your item. That puts it in your owner's "Needs a person" view. Once only: the
     `needs:*` label stays until a person removes it.

The intake and its `ack_within` for each project you file to are listed under "Files to"
in your repo's Intake section.
