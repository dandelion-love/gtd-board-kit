---
type: Decision
title: Agents pull new activity with one read
description: An agent finds what others wrote on items it holds, PRs opened for it and the repo's channels with activity_since and a read_at cursor; nothing is pushed, and a renew no longer hides a follow-up.
tags: [claims, reviews, channels, notifications]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-04T16:00:00Z }
---

# Context

Agents act on GitHub through the server, so GitHub notifies no agent of anything. An
agent saw a comment only when it happened to read that one issue: `follow_ups` on
`item_get` for an item it held, and a channel only through `channel_comments_read`. A
review on a PR that `pr_open` opened for it reached it nowhere. Reviews and directions
went unread until a person pointed at them. Worse, a lane renews its item every tick,
and a renew is a record, so `follow_ups` emptied at the heartbeat, read or not.

Three shapes were weighed:

- **A field on `item_get` or `item_report`.** It already exists as `follow_ups`. It
  needs one read per item, and it cannot cover pull requests or channels.
- **A board view** of items with comments newer than their `Last report`. GitHub's
  filters cannot compare a comment's time with a field, and a view has no PRs or
  channels; it would need a sync to stamp a field on every comment.
- **One read across what the caller holds or serves**, with a cursor. Chosen.

# Decision

- `activity_since(repo, since?)` (Core, `read`) lists conversation created after
  `since` on issues the caller holds, PRs whose `gtd-pr` marker names it, and the
  repo's channel issues: comments, reviews and inline review comments, never records.
- The cursor is the caller's: each result has `read_at`, passed back as `since`. With
  none kept the read covers the last 24 hours. The server keeps no state per caller,
  so a deployment with no store can conform.
- `follow_ups` count from the holder's latest record **other than a renew**.
- It is a pull. It sends no notification, so it never adds to a person's inbox.

# Consequences

- A lane reads once per tick and answers hand-offs, reviews and directions together
  (`board-lane` 0.4.0, `board-report` 0.7.0).
- The server writes for every agent under one identity, so it cannot tell which agent
  wrote a comment it posted; `via_server` marks those and the caller skips its own.
- A new session that kept no `read_at` sees the last day again and must skip what it
  already answered.
