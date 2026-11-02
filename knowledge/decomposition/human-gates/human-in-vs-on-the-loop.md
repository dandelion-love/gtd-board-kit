---
type: Concept
title: Human in the loop vs human on the loop
description: In the loop, the agent waits for a person to approve; on the loop, it acts and the person watches and can veto or undo; agent tools are moving from the first to the second.
tags: [human-in-the-loop, human-on-the-loop, levels-of-automation]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: psw2000, title: "Parasuraman, Sheridan, Wickens (2000). A model for types and levels of human interaction with automation. IEEE Trans. SMC-A 30(3):286-297", resource: "https://scholar.google.com/scholar?q=%22A+model+for+types+and+levels+of+human+interaction+with+automation%22", doi: "10.1109/3468.844354", accessed: 2026-11-02}
  - {id: bainbridge, title: "Bainbridge (1983). Ironies of automation. Automatica 19(6):775-779", resource: "https://scholar.google.com/scholar?q=%22Ironies+of+automation%22+Bainbridge", doi: "10.1016/0005-1098(83)90046-8", accessed: 2026-11-02}
  - {id: sp-sdd, title: "Superpowers: subagent-driven-development skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b}
  - {id: kiro-autopilot, title: "Kiro docs: Autopilot", resource: "https://kiro.dev/docs/ide/chat/autopilot/", accessed: 2026-11-02}
  - {id: anthropic-auto, title: "Anthropic Engineering: Claude Code auto mode (2026-03-25)", resource: "https://anthropic.com/engineering/claude-code-auto-mode", accessed: 2026-11-02}
  - {id: dsh-auth, title: "dsh-superagent-prototype: 002 Authorization", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 002-authorization.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
---

# Definitions

| Mode | The agent | The person |
| --- | --- | --- |
| In the loop | proposes, then waits | approves each action before it happens |
| On the loop | acts, records, reports | watches, can veto in time or undo after |
| Out of the loop | acts | is not told |

These map to the levels of automation of Parasuraman, Sheridan and Wickens: from "executes
the suggestion if the human approves" through "allows the human a restricted time to veto
before automatic execution" and "executes automatically, then necessarily informs the
human", to full autonomy.[^psw2000] Their point: pick a level **per function** (gather
information, analyse, decide, act), not one level for the whole system.[^psw2000]

# The irony

Bainbridge's "ironies of automation": the more the system does, the less practice the human
gets, yet the human is kept for the hardest cases, and monitoring for rare failures is a task
humans do badly.[^bainbridge] On-the-loop oversight is not free: it needs cues that call
attention to the rare case.

# Where agent tools are now

| Tool | In the loop | On the loop |
| --- | --- | --- |
| Superpowers | design approval, plan review | execution: "a running plan does not wait on a human"; every ruling goes in a ledger with what it costs if wrong[^sp-sdd] |
| Kiro | Supervised: approve each turn with edits | Autopilot (default): no per-step approval; view, revert or interrupt[^kiro-autopilot] |
| Claude Code auto mode | — | classifiers approve; matches on more than twenty block rules are refused[^anthropic-auto] |
| dsh-superagent | explicit requests | `observe` records "would accept" without acting; `auto` acts on written rules[^dsh-auth] |

# Rule of thumb for gates

Put a person **in** the loop where an action is hard to undo or where a choice fixes many
later ones (design, skeleton, merge, anything outside the repo). Put them **on** the loop
everywhere else, with an undo path and a record. See
[minimum gate set](minimum-gate-set-solo-owner.md).

[^psw2000]: Parasuraman, Sheridan and Wickens 2000, levels of automation and four function types.
[^bainbridge]: Bainbridge 1983.
[^sp-sdd]: Superpowers subagent-driven-development, "Rulings, not stalls".
[^kiro-autopilot]: Kiro Autopilot page.
[^anthropic-auto]: Anthropic, Claude Code auto mode.
[^dsh-auth]: dsh-superagent 002 Authorization, accept mode.
