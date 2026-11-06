---
type: Reference
title: Linear inbox and triage
description: Linear routes subscribed-issue events into an Inbox with a Priority tab and snooze, sends email only if the in-app item is still unread, and keeps a separate Triage queue with accept, decline, duplicate and snooze actions.
tags: [notifications, linear, inbox, triage, snooze, digest, prior-art]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: linear-inbox, title: "Linear Docs: Inbox", resource: "https://linear.app/docs/inbox", accessed: 2026-11-05}
  - {id: linear-notif, title: "Linear Docs: Notifications", resource: "https://linear.app/docs/notifications", accessed: 2026-11-05}
  - {id: linear-triage, title: "Linear Docs: Triage", resource: "https://linear.app/docs/triage", accessed: 2026-11-05}
---

# What it is

Linear is an issue tracker. It is close to the kit's world: issues, assignees, and a
person who must decide what enters the work queue.

# Inbox

- You are subscribed when you create an issue, are assigned, or are mentioned. Key
  events on subscribed issues reach your Inbox.[^linear-inbox]
- A **Priority** tab, shown by default, separates items that need your attention from
  other updates. Its filter is configurable.[^linear-inbox]
- **Snooze** hides an item until a chosen time. **Reminders** put an item back in the
  Inbox at a set time.[^linear-inbox]
- Delete, mark read, and bulk "delete all read" are keyboard actions.[^linear-inbox]
- The Inbox keeps up to 2,000 open notifications.[^linear-inbox]

# Channels and delay

- Channels are Desktop, Mobile, Email and Slack, toggled per notification type in
  groups.[^linear-notif]
- Desktop, mobile and Slack are immediate. Email digests "send with time delays based on
  urgency", and only if the Inbox item is still unread.[^linear-notif]
- Delivery "may be routed to an active desktop app or browser session".[^linear-notif]
  Whether mobile is then skipped is not documented; unconfirmed.

# Triage

- Triage is a team inbox for issues from integrations or outsiders, reviewed before
  they enter the workflow.[^linear-triage]
- Actions: **Accept** (to the default status), **Decline** (cancel with a reason),
  **Mark as duplicate** (merge), **Snooze** (until a time or new activity).[^linear-triage]
- **Triage responsibility** names who is notified or auto-assigned, and can follow an
  on-call schedule from PagerDuty and others.[^linear-triage]

# What the kit can take from it

- The board is the inbox. Pushes are pointers into it, not a second inbox.
- Separate "needs you" from "updates" with a filter or column, like the Priority tab.
- **Read in app cancels the email.** Send the slower channel only if the item is still
  unacknowledged after a delay, and make the delay depend on urgency.
- Every ask should offer one-step answers that mirror Triage: accept, decline (with a
  reason), duplicate, snooze.
- Snooze should return on a time **or on new activity**, whichever is first.

[^linear-inbox]: Linear Docs, Inbox.
[^linear-notif]: Linear Docs, Notifications.
[^linear-triage]: Linear Docs, Triage.
