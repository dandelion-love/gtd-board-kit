---
type: Research Finding
title: When dsh-superagent lets an agent speak to a person
description: DeepSeek's prototype treats every message and notification as a cost; an agent speaks only to acknowledge once, deliver a result, ask one question or report that it cannot finish, in the conversation where it was asked, and everything else waits on a pull panel.
tags: [attention, notifications, agents, reference]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-05T04:00:00Z }
sources:
  - {id: dsh-phil, title: "dsh-superagent-prototype: 000 Philosophy", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs", file: 000-philosophy.md, accessed: 2026-11-05, commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4}
  - {id: dsh-auth, title: "dsh-superagent-prototype: 002 Authorization", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs", file: 002-authorization.md, accessed: 2026-11-05, commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4}
  - {id: dsh-prompts, title: "dsh-superagent-prototype: 004 Prompts", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs", file: 004-prompts.md, accessed: 2026-11-05, commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4}
  - {id: dsh-panel, title: "dsh-superagent-prototype: 005 Panel", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs", file: 005-panel.md, accessed: 2026-11-05, commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4}
  - {id: dsh-arch, title: "dsh-superagent-prototype: 007 Architecture", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/8c32a9dc5d72c033816c6a8110b37f40cf94fba4/docs", file: 007-architecture.md, accessed: 2026-11-05, commit: 8c32a9dc5d72c033816c6a8110b37f40cf94fba4}
---

# The mandate

"Take as little human attention as possible, and give as much value as possible." A
message, **a notification**, a question, a setting, a panel element and a paragraph of
documentation each cost attention, "and each has to give more value than that, or it is
removed."[^dsh-phil] The kit already applies this to gates
([attention budget](/decomposition/human-gates/attention-budget.md)); this page applies it
to notifications.

# When it speaks: four purposes, enforced

The agent "speaks only when a person must act or can use a result. It confirms a request
once and names what it will do. It stays quiet while it works. It writes again when a
result is ready, when it needs a decision, or when it cannot finish."[^dsh-phil]

The code enforces the list, not just the prompt: every reply declares one purpose,
`acknowledgement`, `answer`, `result` or `attention`, and goes out through an outbox "by
the rule that allows it".[^dsh-arch] Reply purposes and length limits are facts "enforced
by tools and the host" that prompt text cannot change.[^dsh-prompts]

| Purpose | When |
| --- | --- |
| acknowledgement | once, before substantial work, naming the object and the expected result[^dsh-prompts] |
| answer / result | a result can be reviewed or used[^dsh-prompts] |
| attention | a decision or resource is needed; one concrete question, forwarded unchanged; authorised work continues meanwhile[^dsh-prompts] |
| (failure) | the work cannot be finished; a failure is reported as a failure[^dsh-phil] |

# Where and how big

- In the conversation where the request was made, not a new channel.[^dsh-phil]
- One sentence by default, hard limit 100 words.[^dsh-prompts]
- Reviews: a fixed comment is resolved silently; a declined one gets one
  sentence.[^dsh-prompts]

# What is not pushed

- **Progress.** "It stays quiet while it works."[^dsh-phil]
- **Health.** The panel answers "Does anything need me now?" first; "a healthy state
  takes no space"; "a one-off network error is not enough" to show a
  problem.[^dsh-panel]
- **Stale problems.** An unavailable judgement asks for attention only while it is under
  24 hours old, still the latest on its thread and not dismissed.[^dsh-auth]
- **New issues.** They are intake for the agent, not news for a person.
- **Explanations of noise.** "When the agent is noisy, make its prompts shorter and
  stricter, or pause it. Do not add more messages to explain the noise."[^dsh-phil]

# What it does not have

No urgency levels, no escalation, no quiet hours, no digest. Its channels are GitHub
comments and a chat tool; loudness is whatever those apps do. The prototype minimises
*how often* it speaks and leaves *how loud* to the channel.

# What the kit can take from it

- A closed list of reasons to notify, enforced by the server, not left to prompts.
- One ack, then silence until a result, a question or a failure.
- Pull for everything else: one "needs me" view.
- The kit adds what dsh lacks only where a person opts in: a louder channel for asks.

[^dsh-phil]: dsh-superagent 000 Philosophy.
[^dsh-auth]: dsh-superagent 002 Authorization, unavailable decisions.
[^dsh-prompts]: dsh-superagent 004 Prompts, principles of the built-in text.
[^dsh-panel]: dsh-superagent 005 Panel, three questions and quiet by default.
[^dsh-arch]: dsh-superagent 007 Architecture, Replies and reply purposes.
