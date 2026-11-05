---
type: Concept
title: Attention budget
description: Treat the owner's attention as the scarce input; every gate, message and setting must give more value than the attention it costs, or it goes. Names the four stop reasons, the only times an agent asks first.
tags: [attention, gates, design-principle]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: dsh-phil, title: "dsh-superagent-prototype: 000 Philosophy", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 000-philosophy.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: dsh-prompts, title: "dsh-superagent-prototype: 004 Prompts", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 004-prompts.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: dsh-exec, title: "dsh-superagent-prototype: 003 Execution", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 003-execution.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: sp-sdd, title: "Superpowers: subagent-driven-development skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b}
  - {id: kit-dsh, title: "gtd-board-kit: dsh-superagent reference page", resource: "https://github.com/owner/gtd-board-kit/blob/main/knowledge/references/dsh-superagent.md", accessed: 2026-11-02}
---

# The principle

dsh-superagent's core rule: "Take as little human attention as possible, and give as much
value as possible." Every message, question, setting, panel element and paragraph of
documentation "has to give more value than that, or it is removed."[^dsh-phil] The kit's
reference page already records this principle;[^kit-dsh] this page applies it to gates.

# Spending rules, applied to gates

| Rule | Source | Gate consequence |
| --- | --- | --- |
| Speak only when a person must act or can use a result | dsh[^dsh-phil] | no progress pings; a gate is an ask, not a status |
| Confirm concretely, once | dsh[^dsh-prompts] | one ack when work starts, naming object and result |
| A panel lists first what waits for a person; a healthy state takes no space | dsh[^dsh-phil] | one "needs me" view; green items invisible |
| Chat messages one sentence by default, hard limit 100 words | dsh[^dsh-prompts] | the ask fits on a phone screen; detail is a link |
| "Should I continue?" prompts waste their time | Superpowers[^sp-sdd] | no mid-plan check-ins |
| A session parked on a question "costs their whole day and buys nothing" | Superpowers[^sp-sdd] | decide, record the ruling, keep going, unless one of the stop reasons applies |
| One reserved worker slot for a person's follow-up | dsh[^dsh-exec] | the owner's reply is never queued behind agent work |

# Decide, or stop and ask

A mandate already given is acted on, not re-approved. Inside the item's scope, decide
each reversible choice, record the choice and how to undo it on the item, and keep going;
report it with the work. These are the **stop reasons**, the only times an agent asks
first:

1. **Spending, deleting, or anything irreversible.**
2. **Grants, policy and lane switches.**
3. **Research or product direction**: which measure decides, what runs next.
4. **Work outside the item's scope.**

Anything else is decided and recorded. An ask that does not block the work waits for the
hand-back: it is the one action in the ready report, not a stop. BOARD.md rule 7 and the
`board-needs-person` and `board-report` skills apply this list; it is named only here.

# A budget, not a slogan

A rough way to make it concrete for one owner:

- Count **asks per week**: gates plus questions. Track it.
- Each gate type must justify itself by what it caught. A gate that never changes an outcome
  over a month is a candidate to move [on the loop](human-in-vs-on-the-loop.md).
- When the count rises, cut asks first (bigger batches, fewer gates per Story), before
  adding explanation. dsh: "Do not add more messages to explain the noise."[^dsh-phil]

# Open questions

- What weekly ask count is sustainable for one owner? None of the sources gives a number.

[^dsh-phil]: dsh-superagent 000 Philosophy.
[^dsh-prompts]: dsh-superagent 004 Prompts, principles of the built-in text.
[^dsh-exec]: dsh-superagent 003 Execution, Concurrency.
[^sp-sdd]: Superpowers subagent-driven-development, "Continuous execution" and "Rulings, not stalls".
[^kit-dsh]: Kit reference page on dsh-superagent.
