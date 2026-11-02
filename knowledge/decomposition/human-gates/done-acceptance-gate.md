---
type: Pattern
title: Done acceptance gate
description: Done is accepted by a person on evidence the agent produced fresh; the agent's own verification is a precondition, not the acceptance.
tags: [gates, definition-of-done, verification, human-approval]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: sp-verify, title: "Superpowers: verification-before-completion skill (v7.0.1)", resource: "https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion/SKILL.md", accessed: 2026-11-02, commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b, version: 7.0.1}
  - {id: aidlc-phases, title: "AI-DLC guide: Phases and stages (2.11.2)", resource: "https://github.com/awslabs/aidlc-workflows/tree/c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523/docs/guide", file: 04-phases-and-stages.md, accessed: 2026-11-02, commit: c8ed1a7a3ee9dbd87447d0e4c544cbce2d4fb523, version: 2.11.2}
  - {id: dsh-prompts, title: "dsh-superagent-prototype: 004 Prompts", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 004-prompts.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: dsh-exec, title: "dsh-superagent-prototype: 003 Execution", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 003-execution.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: applab, title: "AppLab backlog plugin README (v1.3.0)", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/README.md", accessed: 2026-11-02, commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6}
  - {id: gh-projects-auto, title: "GitHub Docs: Using the built-in automations", resource: "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations", accessed: 2026-11-02}
---

# Two steps, two owners

| Step | Owner | Question |
| --- | --- | --- |
| Verify | agent | Did I run the command that proves the claim, just now, and read its output? |
| Accept | person | Does this meet the Story's criteria and the Definition of Done? |

# Agent-side verification (precondition)

- Superpowers: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE" — identify the
  command, run it in full, read the output, then claim, with the evidence.[^sp-verify]
- dsh-superagent "honest delivery": opening a PR is not readiness, a draft is marked
  unfinished, a UI change without a real before screenshot is not ready.[^dsh-prompts]
- AppLab: each agent verifies against each acceptance criterion and pushes its branch even
  when `partial` or `blocked`; "Honest WIP is the morning's most useful signal."[^applab]

# Person-side acceptance

- AI-DLC: per Unit, the recorded verification command must exit 0 and the person must
  approve; a checkpoint whose work changed after it was asked is asked again.[^aidlc-phases]
- dsh-superagent: "Awaiting review" means a `ready` Report with a PR; a Ticket is done when
  none of the PRs it opened remain open.[^dsh-exec]

# Merge and Done: one act or two?

On GitHub, a merged PR sets its project item to Done by default, and a closed issue does
too.[^gh-projects-auto] So for a Story with one PR, **merge is acceptance**: fold the two
gates into one. Keep them separate only when acceptance needs something the diff cannot show
(a deploy, a person trying the feature). Then the Story stays open after merge until the
person closes it.

# Epic done

An Epic is done when its Stories are done and a person closes it. That is a short
look at the outcome, not a re-review of the code.

[^sp-verify]: Superpowers verification-before-completion, The Iron Law and Gate Function.
[^dsh-prompts]: dsh-superagent 004 Prompts, "Honest delivery".
[^dsh-exec]: dsh-superagent 003 Execution, Ticket stages and Pull requests.
[^applab]: AppLab backlog README, `/nightshift`.
[^aidlc-phases]: AI-DLC Phases and stages, Unit checkpoints.
[^gh-projects-auto]: GitHub Docs, built-in workflows (item closed, PR merged).
