---
type: Concept
title: Approval fatigue and rubber-stamping
description: When approvals are frequent and mostly yes, people stop reading them; the evidence says cut the count and the repeats, not add more prompts.
tags: [approval-fatigue, alert-fatigue, rubber-stamping, human-factors]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: anthropic-auto, title: "Anthropic Engineering: Claude Code auto mode (2026-03-25)", resource: "https://anthropic.com/engineering/claude-code-auto-mode", accessed: 2026-11-02}
  - {id: ancker2017, title: "Ancker et al. (2017). Effects of workload, work complexity, and repeated alerts on alert fatigue in a clinical decision support system. BMC Med Inform Decis Mak 17:36", resource: "https://scholar.google.com/scholar?q=%22Effects+of+workload%2C+work+complexity%2C+and+repeated+alerts+on+alert+fatigue%22", doi: "10.1186/s12911-017-0430-8", accessed: 2026-11-02}
  - {id: bainbridge, title: "Bainbridge (1983). Ironies of automation. Automatica 19(6):775-779", resource: "https://scholar.google.com/scholar?q=%22Ironies+of+automation%22+Bainbridge", doi: "10.1016/0005-1098(83)90046-8", accessed: 2026-11-02}
  - {id: aidlc-phases, title: "AI-DLC guide: Phases and stages (2.11.2)", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 04-phases-and-stages.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523}
  - {id: sp-brainstorm, title: "Superpowers: brainstorming skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b}
  - {id: dsh-phil, title: "dsh-superagent-prototype: 000 Philosophy", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 000-philosophy.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: gh-protected, title: "GitHub Docs: About protected branches", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", accessed: 2026-11-02}
---

# Evidence

| Finding | Source |
| --- | --- |
| Claude Code users accept 93% of manual permission prompts; Anthropic names the risk "approval fatigue, where people stop paying close attention to what they're approving" | Anthropic, primary[^anthropic-auto] |
| Clinicians: likelihood of accepting a reminder dropped 30% for each extra reminder per encounter, and 10% for each 5-point rise in the share of repeated reminders | Ancker et al. 2017[^ancker2017] |
| Same study: no effect of overall workload, and no decline over time for a new alert; the driver is the number and repetition of alerts at one moment | Ancker et al. 2017[^ancker2017] |
| A human kept only to monitor a mostly-right system is badly placed to catch its rare failure | Bainbridge 1983[^bainbridge] |

The Ancker result is the useful one for design: fatigue is driven by **many prompts at once
and repeated prompts**, not by a busy day as such.[^ancker2017]

# What rubber-stamping looks like with agents

- Approving a design you were not shown: Superpowers counts "they said 'sounds good' to the
  idea" as no approval.[^sp-brainstorm]
- Approving a checkpoint whose work then changed: AI-DLC asks again when the work changed
  after the question.[^aidlc-phases] GitHub's equivalent is dismissing stale approvals on new
  commits.[^gh-protected]
- Approving a long plan in one click after skimming it. No method here measures this.

# Design responses

1. **Fewer, later, concrete gates.** Ask at the points that fix many later choices; let the
   rest run [on the loop](human-in-vs-on-the-loop.md).
2. **No repeats.** One question per decision; never re-ask something already answered.
   dsh-superagent: "Tune for less noise ... Do not add more messages to explain the
   noise."[^dsh-phil]
3. **Make yes cost something to fake.** Show the evidence in the ask (AI-DLC shows
   "Verified with `<command>` (exit 0)").[^aidlc-phases]
4. **Move routine approvals to machines.** Anthropic's answer to 93% was classifiers plus
   block rules, with a measured 17% false-negative rate on real overeager actions, which it
   calls "the honest number".[^anthropic-auto] Automation does not remove the gate's risk; it
   moves it.

See [automation bias](automation-bias.md) and [batching](batching-and-one-question-at-a-time.md).

# Caveats

- The 93% figure is Anthropic's own telemetry statement, not a peer-reviewed study.
- Ancker et al. studied clinical alerts, not code approvals; transfer is by analogy.

[^anthropic-auto]: Anthropic, Claude Code auto mode.
[^ancker2017]: Ancker et al. 2017, abstract results and conclusions.
[^bainbridge]: Bainbridge 1983.
[^sp-brainstorm]: Superpowers brainstorming, Red Flags.
[^aidlc-phases]: AI-DLC Phases and stages, Unit checkpoints.
[^dsh-phil]: dsh-superagent 000 Philosophy, Responsibility.
[^gh-protected]: GitHub Docs, dismiss stale approvals.
