---
type: Comparison
title: Human gates across agent methods
description: Which human approval points AI-DLC, Superpowers, Spec Kit, Kiro, the AppLab backlog plugin and dsh-superagent have, and which of them can be waived.
tags: [gates, comparison, ai-dlc, superpowers, spec-kit, kiro]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: aidlc-phases, title: "AI-DLC guide: Phases and stages (2.11.2)", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 04-phases-and-stages.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523, version: 2.11.2}
  - {id: aidlc-audit, title: "AI-DLC guide: State and audit", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 10-state-and-audit.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523}
  - {id: aidlc-changelog, title: "AI-DLC CHANGELOG 2.11.2", resource: "https://github.com/awslabs/aidlc-workflows/blob/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/CHANGELOG.md", accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523}
  - {id: superpowers, title: "Superpowers skills (v7.0.1)", resource: "https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b, version: 7.0.1}
  - {id: spec-kit, title: "Spec Kit workflows and commands (1.2.5)", resource: "https://github.com/github/spec-kit/tree/7370e592f3cd9c06e5b698983957e227c75b30e2", accessed: 2026-11-02, commit: 7370e592f3cd9c06e5b698983957e227c75b30e2, version: 1.2.5}
  - {id: kiro-feature, title: "Kiro docs: Feature specs", resource: "https://kiro.dev/docs/specs/feature-specs/", accessed: 2026-11-02}
  - {id: kiro-autopilot, title: "Kiro docs: Autopilot", resource: "https://kiro.dev/docs/ide/chat/autopilot/", accessed: 2026-11-02}
  - {id: applab, title: "AppLab backlog plugin README (v1.3.0)", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/README.md", accessed: 2026-11-02, commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, version: 1.3.0}
  - {id: dsh, title: "dsh-superagent-prototype docs 000-004", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", files: "000-philosophy.md to 004-prompts.md", accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e, version: 0.1.0}
---

# Gate matrix

`H` = a person must act; `opt` = on by default, can be switched off; `—` = not in the method;
`agent` = the agent checks itself, no person.

| Gate | AI-DLC 2.11.2 | Superpowers 7.0.1 | Spec Kit 1.2.5 | Kiro | AppLab backlog 1.3.0 | dsh-superagent 0.1.0 |
| --- | --- | --- | --- | --- | --- | --- |
| [Design / spec](design-approval-gate.md) | H, every stage[^aidlc-phases] | H, hard gate[^superpowers] | opt, workflow gate[^spec-kit] | opt, Quick Spec skips[^kiro-feature] | — (refine interview) | confirm once, then work[^dsh] |
| [Ready → pickup](ready-hand-move-gate.md) | — | — | checklist yes/no[^spec-kit] | — | H, hand move[^applab] | admission gate (who asked)[^dsh] |
| [Plan](plan-approval-gate.md) | opt, Plan Approval[^aidlc-phases] | H, review + method choice[^superpowers] | opt, workflow gate[^spec-kit] | Supervised: per turn[^kiro-autopilot] | — | — |
| [Walking skeleton](walking-skeleton-approval.md) | H when skeleton-on[^aidlc-phases] | — | — | — | — | — |
| Per-task checkpoints | waivable ("Continue automatically")[^aidlc-phases] | none; rulings ledger[^superpowers] | — | Supervised only[^kiro-autopilot] | — | — |
| [Merge](merge-approval-gate.md) | outside method | H, 3 options[^superpowers] | — | — | H, per-ticket draft PR[^applab] | people merge by default[^dsh] |
| [Done](done-acceptance-gate.md) | H per Unit + exit 0[^aidlc-phases] | agent, fresh evidence[^superpowers] | — | — | test plan for person[^applab] | ready Report → awaiting review[^dsh] |
| Failure / question | H, never waived[^aidlc-phases] | 4 stop reasons[^superpowers] | — | — | `blocked` reported[^applab] | one structured question[^dsh] |

# Audit of approvals

| Method | Where the approval is recorded |
| --- | --- |
| AI-DLC | `audit/` shards in the repo; the record keeps the reply each decision was made on[^aidlc-audit][^aidlc-changelog] |
| Superpowers | design and plan docs committed; rulings ledger during execution[^superpowers] |
| Spec Kit | persisted workflow run state; checklist checkboxes are reviewer-owned[^spec-kit] |
| AppLab | board column history and the PRs[^applab] |
| dsh-superagent | immutable Mandate with Policy version; Decision history per Thread[^dsh] |

# Reading the matrix

- Only AI-DLC and AppLab make a **pre-build** approval a real, separate step that the
  method itself waits on, which agrees with the first sweep.
- Everyone keeps a person at the **end** (merge or Done). That is the floor.
- The trend across 2026 releases is fewer stops in the middle: AI-DLC's "Continue
  automatically", Superpowers' "rulings, not stalls", Kiro's Autopilot default.[^aidlc-phases][^superpowers][^kiro-autopilot]

# Caveats

- Kiro was read from its docs only; no repo to pin.
- Spec Kit's gates exist only when you run its workflow engine; run command by command,
  the README asks you to review each result before continuing, as convention.[^spec-kit]

[^aidlc-phases]: AI-DLC Phases and stages.
[^aidlc-audit]: AI-DLC State and audit.
[^aidlc-changelog]: AI-DLC CHANGELOG, 2.11.2 summary.
[^superpowers]: Superpowers brainstorming, writing-plans, subagent-driven-development, finishing-a-development-branch, verification-before-completion.
[^spec-kit]: Spec Kit workflow.yml, workflows README, implement command, README.
[^kiro-feature]: Kiro Feature specs.
[^kiro-autopilot]: Kiro Autopilot page.
[^applab]: AppLab backlog README.
[^dsh]: dsh-superagent docs 000-004.
