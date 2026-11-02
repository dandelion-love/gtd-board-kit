---
type: Concept
title: Definition of Done for agent PRs
description: What "done" means when an agent returns work as a pull request; opened, ready and merged are different states, and only a person's merge completes the item.
tags: [definition-of-done, pull-requests, agents, review]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: scrum-guide, title: "The Scrum Guide (2020)", resource: "https://scrumguides.org/scrum-guide.html", url: "https://scrumguides.org/scrum-guide.html", accessed: 2026-11-02 }
  - { id: gh-prs, title: "GitHub Docs, About pull requests (draft PRs)", resource: "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests", url: "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests", accessed: 2026-11-02 }
  - { id: gh-protected, title: "GitHub Docs, About protected branches", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", url: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", accessed: 2026-11-02 }
  - { id: cc-best, title: "Claude Code docs, Best practices", resource: "https://code.claude.com/docs/en/best-practices", url: "https://code.claude.com/docs/en/best-practices", accessed: 2026-11-02 }
  - { id: sp-vbc, title: "obra/superpowers, verification-before-completion SKILL.md", resource: "https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md", url: "https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md", accessed: 2026-11-02, version: "plugin 7.0.1" }
---

# Criteria vs Done

- **Acceptance criteria**: per item. Did we build the right thing?
- **Definition of Done**: for every item. In the Scrum Guide it is "a formal
  description of the state of the Increment when it meets the quality measures required
  for the product"; an item that does not meet it "cannot be released or even presented
  at the Sprint Review" and returns to the backlog.[^scrum-guide]

An item is done when both hold. Scrum does not define acceptance criteria; that term
comes from wider agile practice.

# Three PR states, three meanings

| State | GitHub fact | Means |
| --- | --- | --- |
| Opened (draft) | cannot be merged; code owners not asked[^gh-prs] | work in progress, visible |
| Ready for review | code owners requested[^gh-prs] | agent claims every AC has evidence and checks are green |
| Merged | required checks and reviews passed[^gh-protected] | a person accepted it; the item is done |

**Opening a PR is not "done". Marking it ready is a claim. Merge is the only done.**
An agent must not mark ready before its own evidence is in the PR body.

# A draft DoD for agent PRs

- [ ] Every AC in the issue has an evidence row in the PR body
  ([traceability](criterion-traceability-on-github.md)).
- [ ] Evidence is fresh: commands were run on the final commit, output quoted
  ([verification before completion](verification-before-completion.md)).[^sp-vbc]
- [ ] Required checks are green **and ran** (not skipped).
- [ ] No test, fixture, snapshot or check config changed unless an AC asks for it; any
  such change is listed for the reviewer.
- [ ] UI changes carry before and after screenshots.
- [ ] Out-of-scope findings are captured as new items, not folded in.
- [ ] A person reviewed and merged.

# Supporting evidence

- Claude Code's docs: without a check to run, "looks done" is all the agent has, and you
  become the test suite; ask for evidence (command and output, or screenshot), because
  "All tests pass" alone tells you little.[^cc-best]
- The same docs recommend a reviewer that did not write the code (fresh context,
  read-only tools), and having a person approve the result at the end of an unattended
  run.[^cc-best]
- The superpowers skill's table: "Requirements met" needs a line-by-line checklist;
  "Tests passing" is **not sufficient**.[^sp-vbc]

# Caveats

- The screenshot rule is common practice, not a cited standard.
- The checklist is a draft; its items are reasoned from the sources, not measured.

# Related

- [Criterion-to-evidence chain](criterion-to-evidence-chain.md)
- [Test-gaming mitigations](test-gaming-mitigations.md)
