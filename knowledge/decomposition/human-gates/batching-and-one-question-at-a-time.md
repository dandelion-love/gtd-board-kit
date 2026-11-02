---
type: Practice
title: Batch the sitting, one question per message
description: Gather a person's decisions into planned sittings, and inside a sitting ask one concrete question at a time; the two rules work at different scales and do not conflict.
tags: [batching, questions, interruptions, attention]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: mark2008, title: "Mark, Gudith, Klocke (2008). The cost of interrupted work: more speed and stress. CHI 2008", resource: "https://www.ics.uci.edu/~gmark/chi08-mark.pdf", accessed: 2026-11-02}
  - {id: sk-clarify, title: "Spec Kit: clarify command", resource: "https://github.com/github/spec-kit/blob/7370e592f3cd9c06e5b698983957e227c75b30e2/templates/commands/clarify.md", accessed: 2026-11-02, commit: 7370e592f3cd9c06e5b698983957e227c75b30e2}
  - {id: sp-brainstorm, title: "Superpowers: brainstorming skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/brainstorming/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b}
  - {id: dsh-prompts, title: "dsh-superagent-prototype: 004 Prompts", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 004-prompts.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: applab, title: "AppLab backlog plugin README (v1.3.0)", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/README.md", accessed: 2026-11-02, commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6}
  - {id: aidlc-phases, title: "AI-DLC guide: Phases and stages (2.11.2)", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 04-phases-and-stages.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523}
  - {id: ancker2017, title: "Ancker et al. (2017). Repeated alerts and alert fatigue. BMC Med Inform Decis Mak 17:36", resource: "https://scholar.google.com/scholar?q=%22Effects+of+workload%2C+work+complexity%2C+and+repeated+alerts+on+alert+fatigue%22", doi: "10.1186/s12911-017-0430-8", accessed: 2026-11-02}
---

# Two scales

| Scale | Rule | Why |
| --- | --- | --- |
| Across the day | **Batch** decisions into planned sittings | Interruptions are paid for in stress: people finished interrupted tasks faster with no loss of quality, but with "more stress, higher frustration, time pressure and effort"[^mark2008] |
| Inside one message | **One question** at a time, concrete, easy to answer | Many alerts at once lower acceptance quality; each extra reminder per encounter cut acceptance 30%[^ancker2017] |

They fit together: the agent **queues** questions and does not interrupt; when the person
sits down, it presents them one by one, most important first.

# How methods do it

| Method | One question | Batch |
| --- | --- | --- |
| Spec Kit clarify | "Present EXACTLY ONE question at a time"; at most 5 per session; multiple choice (2-5 options) or an answer of 5 words or fewer[^sk-clarify] | the whole clarify pass is one sitting |
| Superpowers brainstorming | "Each message ends with one question: a single sentence with no list of example answers"[^sp-brainstorm] | the review "pile" is brought "in one message, most important first", and is "the only round of questions the check produces"[^sp-brainstorm] |
| dsh-superagent | the Executor puts one concrete question in a structured field; it is forwarded unchanged; authorised work continues meanwhile[^dsh-prompts] | the router takes decisions on several waiting candidates in one call[^dsh-prompts] |
| AppLab refine | one ticket at a time, starting with "refine this now, or later?"[^applab] | triage: "two checks, one approval batch"[^applab] |
| AI-DLC | — | a guided swarm batch ends with one Approve / Request Changes for the batch[^aidlc-phases] |

# For a GitHub board

- A question is a `needs:<who>` label plus one comment on the item it is about. Not a chat
  ping.
- The person's sitting is a saved view filtered on `needs:*` and "awaiting review". It
  shows only what waits for them.
- Questions that are not blocking go in the PR body or the release note, not as asks.

# Caveats

- The "one question" rule is design guidance in these tools, not measured by them. The
  supporting evidence (Mark 2008, Ancker 2017) is from office work and clinical alerts.

[^mark2008]: Mark, Gudith and Klocke 2008, abstract.
[^ancker2017]: Ancker et al. 2017, abstract results.
[^sk-clarify]: Spec Kit clarify command, steps 4-5.
[^sp-brainstorm]: Superpowers brainstorming, The Conversation and the written-design check.
[^dsh-prompts]: dsh-superagent 004 Prompts, principles of the built-in text.
[^applab]: AppLab backlog README, `/refine`.
[^aidlc-phases]: AI-DLC Phases and stages, Parallel Unit batches.
