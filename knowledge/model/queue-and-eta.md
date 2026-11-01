---
type: Pattern
title: Queue and ETA
description: The queue is the card order of a view with no sort and the ETA is a date field; both are native, so a person's edit in the UI or API wins.
tags: [board, queue, eta]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T06:10:00Z }
---

# Rule

- **Queue:** the manual card order of the repo's queue view. A sorted view hides manual
  order, so the queue view has none. People reorder by dragging (the API call is
  `updateProjectV2ItemPosition`). Agents read the order fresh and take the first item
  they may claim. They move a card only to place work they capture or hand back.
- **ETA:** a date field, `Target date` by default, with `Start date` for the start.
  The agent writes its estimate and repeats it in its report. A value that differs from
  the agent's last report was set by a person: it stands, and the agent reports when it
  can't meet it.
- **Order between items:** native blocked-by links, not prose.
- **Serial resource:** when a lane owns a resource and the head of its queue slips, the
  lane recomputes Start and Target dates for the items behind it from the head's new
  ETA. A date a person set stands; the conflict is reported, not overwritten.

The repo names its queue view and fields in its own layer; see
[the kit is the interface](/decisions/kit-is-the-interface.md).
