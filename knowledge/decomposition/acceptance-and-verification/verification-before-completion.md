---
type: Practice
title: Verification before completion
description: Evidence before claims; an agent may say work passes or is done only after running the proving command fresh and reading its full output.
tags: [verification, agents, evidence]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: sp-vbc, title: "obra/superpowers, verification-before-completion SKILL.md", resource: "https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md", url: "https://raw.githubusercontent.com/obra/superpowers/main/skills/verification-before-completion/SKILL.md", accessed: 2026-11-02, version: "plugin 7.0.1" }
  - { id: cc-best, title: "Claude Code docs, Best practices", resource: "https://code.claude.com/docs/en/best-practices", url: "https://code.claude.com/docs/en/best-practices", accessed: 2026-11-02 }
---

# The rule

From the superpowers skill: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION
EVIDENCE".[^sp-vbc] Its gate:

1. Identify the command that proves the claim.
2. Run it in full, fresh.
3. Read the full output and exit code; count failures.
4. Check the output supports the claim.
5. Only then claim, with the evidence.

# What counts as evidence

From the skill's own table:[^sp-vbc]

| Claim | Needs | Not enough |
| --- | --- | --- |
| Tests pass | test output, 0 failures | a previous run, "should pass" |
| Build succeeds | build exit 0 | lint passing |
| Bug fixed | the original symptom now passes | code changed |
| Regression test works | red-green: fails without the fix, passes with it | passes once |
| Sub-agent completed | the diff shows the change | the agent says "success" |
| Requirements met | line-by-line checklist | tests passing |

The last row is the link to acceptance criteria: green tests do not prove every
criterion was covered.

# Red flags

"Should", "probably", "seems to"; satisfaction before running anything; trusting a
sub-agent's report.[^sp-vbc]

# Same idea, first-party

Claude Code's best practices: give the agent a check to run; ask for the command and its
output or a screenshot; for an unwatched session that is the only evidence you
have.[^cc-best]

# Limits

- Fresh evidence proves the command passed, not that the command checks the right
  thing. An agent that edited the test still gets a fresh green run. Pair with
  [test-gaming mitigations](test-gaming-mitigations.md).
- The skill is a prompt; nothing enforces it. CI and required checks are the enforced
  copy.

# Related

- [Definition of Done for agent PRs](definition-of-done-for-agent-prs.md)
- [Criterion-to-evidence chain](criterion-to-evidence-chain.md)
