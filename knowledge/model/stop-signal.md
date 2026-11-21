---
type: Pattern
title: The stop signal
description: A person stops an item by a signed stop record the server writes for the item's owner; the worker finishes its step, writes a closing note and releases; a label mirrors the record and is never the truth.
tags: [board, stop, claims]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-21T20:00:00Z }
---

# Rule

Stopping an item mid-run used to mean closing it and hoping its worker noticed. Now the
owner records a **stop**, the worker sees it and winds down, and the board shows the item at
rest. Closing the issue still works (a holder may release a closed item), but it is not the
stop.

- **The signed record is the truth.** A stop is a `stop` record, a signed comment written by
  `item_stop` ([claim records](../../server-spec/claim-records.md#a-stop)). Each stop and
  each clear is a dated entry with its sender, so repeats can be counted and a clear never
  erases that a stop happened.
- **The label is a mirror.** The server sets `stop-requested` when it records a stop, so the
  stop shows in GitHub's own screens, and removes it when the holder releases or the owner
  clears. Nobody sets or clears the mirror by hand to mean anything: a label applied by hand
  becomes a stop only if the label event came from the owner, and then the server writes
  the record and keeps the label. Otherwise the server removes the label and records
  nothing.
- **Who may send a stop:** the item's owner: the repo owner, or a person the owner named in
  the profile. The server checks the caller; an agent, a worker of the item or anyone else
  is refused and nothing is recorded.
- **Who may clear a stop:** the owner, with `item_stop_clear`, including on an item with no
  worker. A worker clears nothing: releasing after it winds down ends the stop's effect on
  the worker, not the record.
- **A stop on an item with no worker** is recorded, shows `at-rest` and blocks every new
  claim until the owner clears it.

# What the worker does

A worker learns of the stop on its next `item_renew`, `item_report` or `item_get`: each
returns `stop` (and a warning). Then, within the **wind-down limit** (30 minutes unless
the server says another; the owner may set it per stop up to 24 hours):

1. finish the current step, and start nothing new;
2. write the closing note: `done`, `left`, `decided`, `set_aside`
   ([report vocabulary](report-vocabulary.md#closing-note));
3. `item_release`.

The server never revokes the claim. Past the limit the item shows **overdue to wind
down**, `item_renew` refuses (naming the stop) so the lease runs out by itself, and a
person decides what next. A worker that does not know the signal keeps working, and its
renew succeeds until the limit passes: the stop is a request, not a kill.

# Why

A label has no time, sender or reason, and anyone with triage rights can apply one, so the
server could not tell the owner's stop from a stranger's. A signed record can be checked,
dated and counted; the label is kept only so a person sees it at a glance.
