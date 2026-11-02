---
type: Synthesis
title: Minimum gate set for a solo owner with agents (draft)
description: Five human gates, one of them enforced by GitHub, are enough for one busy owner to steer agents that decompose and build Epics, Stories and Tasks; everything else runs on the loop.
tags: [gates, synthesis, solo-owner, epic, story, task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: aidlc-phases, title: "AI-DLC guide: Phases and stages (2.11.2)", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 04-phases-and-stages.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523, version: 2.11.2}
  - {id: aidlc-modes, title: "AI-DLC guide: Interaction modes", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 07-interaction-modes.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523}
  - {id: sp-sdd, title: "Superpowers: subagent-driven-development skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/subagent-driven-development/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b}
  - {id: applab, title: "AppLab backlog plugin README (v1.3.0)", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/README.md", accessed: 2026-11-02, commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6}
  - {id: dsh-auth, title: "dsh-superagent-prototype: 002 Authorization", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 002-authorization.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: gh-approve, title: "GitHub Docs: Approving a pull request with required reviews", resource: "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews", accessed: 2026-11-02}
  - {id: ancker2017, title: "Ancker et al. (2017). Repeated alerts and alert fatigue. BMC Med Inform Decis Mak 17:36", resource: "https://scholar.google.com/scholar?q=%22Effects+of+workload%2C+work+complexity%2C+and+repeated+alerts+on+alert+fatigue%22", doi: "10.1186/s12911-017-0430-8", accessed: 2026-11-02}
  - {id: goddard2012, title: "Goddard, Roudsari, Wyatt (2012). Automation bias: a systematic review. JAMIA 19(1):121-127", resource: "https://scholar.google.com/scholar?q=%22Automation+bias%3A+a+systematic+review+of+frequency%2C+effect+mediators%2C+and+mitigators%22", doi: "10.1136/amiajnl-2011-000089", accessed: 2026-11-02}
---

# Principle

Gate where a choice fixes many later ones or cannot be undone; everywhere else, let agents
act, record and report ([on the loop](human-in-vs-on-the-loop.md)). Fewer, concrete,
non-repeated asks resist [fatigue](approval-fatigue-and-rubber-stamping.md) better than
many small ones.[^ancker2017]

# The five gates

| # | Gate | Level | Person's act | Enforced by | Borrowed from |
| --- | --- | --- | --- | --- | --- |
| G1 | [Epic intent approved](design-approval-gate.md) | Epic | read a one-screen outcome + Story list, add `agent-ready` to the Epic, or comment changes | convention | AI-DLC stage gates, Superpowers hard gate |
| G2 | [Story ready → pickup](ready-hand-move-gate.md) | Story | add `agent-ready` (batched) | convention + actor check | AppLab hand move[^applab] |
| G3 | [Skeleton merge](walking-skeleton-approval.md) | first Story of an Epic | approve + merge after the recorded verify command passed | required review | AI-DLC skeleton[^aidlc-phases] |
| G4 | [Story merge = Done](merge-approval-gate.md) | Story | approve + merge the PR | required review, if plan allows | all methods |
| G5 | Outside effects | any | approve deploy, publish, delete, spend, secret use | [environment reviewer](github-environment-required-reviewers.md) or explicit ask | Superpowers stop reasons[^sp-sdd] |

Always on, not counted as a gate: **a question or failure stops the item** (`needs:<who>`),
one concrete question, answered in the next sitting.

# What runs on the loop (no ask)

| Activity | Instead of a gate |
| --- | --- |
| Plan for a Story | in the PR body; reviewed at G4 |
| Task checkpoints inside a Story | agent records rulings ("what, why, cost if wrong")[^sp-sdd] |
| Agent decomposing an Epic into Stories | creates them `agent-proposed`; G1/G2 promote them |
| Agent proposing follow-up work | `agent-proposed` only; never `agent-ready` |
| Lanes and proactive work | `observe` first, then `auto` on a written rule[^dsh-auth] |

# Cost per Epic

For an Epic with *n* Stories: 1 (G1) + *n* labels in one sitting (G2) + *n* PR reviews
(G3/G4) + G5 only when needed. Roughly *n* + 1 decisions, two or three sittings.

# Rules that keep the gates honest

1. Agents never add `agent-ready`, never merge, never approve. A check flags any approval
   label or merge made by an agent account.
2. Agents push under their **own identity**, so the owner can be the required reviewer;
   an author cannot approve their own PR.[^gh-approve]
3. Every ask shows its evidence: command and exit code, screenshot, what was **not**
   checked. Information rather than recommendation is a documented automation-bias
   mitigator.[^goddard2012]
4. Stale approvals dismissed on new commits; a changed item is asked again.[^aidlc-phases]
5. After three rounds of changes on one gate, offer "accept as-is" or "drop".[^aidlc-modes]
6. One "needs me" view; asks are batched into sittings, never pushed as pings.

# Fallback on a plan without enforcement

On a Free private repo, G3 and G4 are conventions too. Keep them, and add a daily
after-the-fact audit of merges and approval labels by actor.

# Open questions for the owner

- Is G1 needed for small Epics (three Stories or fewer), or can G2 alone carry it?
- Should G3 be dropped when an Epic adds to an existing, working system (brownfield)?
- Is the agent identity a separate bot account, a GitHub App, or both?

[^ancker2017]: Ancker et al. 2017.
[^applab]: AppLab backlog README, refinement stops at ready.
[^aidlc-phases]: AI-DLC Phases and stages.
[^aidlc-modes]: AI-DLC Interaction modes, Accept as-is.
[^sp-sdd]: Superpowers subagent-driven-development, stop reasons and rulings.
[^dsh-auth]: dsh-superagent 002 Authorization, accept mode.
[^gh-approve]: GitHub Docs, authors cannot approve their own PRs.
[^goddard2012]: Goddard et al. 2012, mitigators.
