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
