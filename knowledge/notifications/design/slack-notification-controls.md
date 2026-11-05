---
type: Reference
title: Slack notification controls
description: Slack lets each person choose everything or only mentions, set keyword and per-channel exceptions, schedule quiet hours, delay mobile pushes while they are active, and let a sender break through Do Not Disturb once a day.
tags: [notifications, slack, mentions, do-not-disturb, quiet-hours, prior-art]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: slack-config, title: "Slack Help Center: Configure your Slack notifications (search the article title)", resource: "https://slack.com/help", accessed: 2026-11-05}
  - {id: slack-dnd, title: "Slack Help Center: Pause notifications with Do Not Disturb (search the article title)", resource: "https://slack.com/help", accessed: 2026-11-05}
---

# What it is

Slack is a chat tool used by millions of people, so its notification settings show what
a large, busy audience will tolerate. It is also a likely channel for the kit's pings.

# Mechanisms

| Control | What it does |
| --- | --- |
| What to notify about | **Everything** or **Mentions and direct messages**, with per-channel exceptions[^slack-config] |
| Keywords | notify on exact, case-insensitive word matches in joined channels[^slack-config] |
| Notification schedule | limit notifications to set days and hours; outside them, notifications pause[^slack-config] |
| Mobile delay | send mobile push only when inactive; default is 10 minutes after desktop activity stops[^slack-config] |
| Do Not Disturb | pause all notifications for a time or on a recurring schedule[^slack-dnd] |
| DND override | a sender sees a snooze icon and may force one urgent DM through, once per day[^slack-dnd] |
| VIP list | named people can still reach you while paused[^slack-dnd] |

# Design lessons

- **Mentions are the default unit of "for you".** A message addressed to you is the
  signal; channel traffic is not.
- **Device routing.** Slack does not push to the phone while you are at the desk. A
  second copy of the same message is noise.
- **Quiet hours are recurring and owned by the receiver.**
- **Breakthrough is rationed.** The sender, not the receiver, decides it is urgent, but
  only once a day. Scarcity keeps the override meaningful.
- **Nothing is lost.** Paused messages are still there after the pause ends.[^slack-dnd]

# What the kit can take from it

- Only notify the owner when an item is **addressed to them** (an ask), never for
  general board activity.
- Respect a receiver-owned quiet-hours schedule; hold pushes and deliver when it ends.
- Give agents a rationed break-through (for example one per day across all agents) for
  truly blocking asks, and log every use.
- If the owner is active on the board, do not also push to the phone.
- When posting to Slack, post to a direct message or mention the owner. Posting to an
  unmentioned channel means the owner never sees it if they chose mentions-only.

Slack article links carry long numeric IDs that this repo's public-content guard blocks,
so the sources point to the Help Center front page; search the article title there.

[^slack-config]: Slack Help, Configure your Slack notifications.
[^slack-dnd]: Slack Help, Pause notifications with Do Not Disturb.
