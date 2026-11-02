---
type: Reference
title: AppLab backlog plugin (refine and nightshift)
description: A tracker-agnostic Claude Code plugin whose refine skill promotes a ticket to READY only when six questions are answered and then stops, leaving the move to the build queue as a person's hand-move; its nightshift half builds unattended.
resource: https://github.com/applab-nl/claude-code-plugins/tree/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog
tags: [plugin, refinement, definition-of-ready, human-gate, github-issues]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: al-readme, title: "backlog/README.md", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/README.md", commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, accessed: 2026-11-02 }
  - { id: al-refine, title: "backlog/skills/refine/SKILL.md", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/skills/refine/SKILL.md", commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, accessed: 2026-11-02 }
  - { id: al-changelog, title: "backlog/CHANGELOG.md (1.3.0, 2026-09-05)", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/CHANGELOG.md", commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, accessed: 2026-11-02 }
  - { id: al-plugin, title: "backlog/.claude-plugin/plugin.json and LICENSE", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/.claude-plugin/plugin.json", commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, accessed: 2026-11-02 }
  - { id: al-scripts, title: "backlog/scripts/build_preview.sh and render_testplan.py", resource: "https://github.com/applab-nl/claude-code-plugins/tree/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/scripts", commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, accessed: 2026-11-02 }
  - { id: al-page, title: "Repository page (stars)", resource: "https://github.com/applab-nl/claude-code-plugins", accessed: 2026-11-02 }
---

# Provenance

| Fact | Value |
| --- | --- |
| Owner | AppLab, a company account; MIT licence in the plugin folder[^al-plugin] |
| Stars / forks | 1 / 0 on 2026-11-02[^al-page] |
| Plugin version | 1.3.0, 2026-09-05; the plugin's first commit was 2026-08-24[^al-changelog] |
| Pinned commit | `a5ce3da` (repo HEAD, 2026-11-01); plugin last changed in `e9aa2d3`, 2026-09-05 |
| Trackers | Linear, Jira or GitHub Issues, detected once and written to a committed `.claude/backlog.json`[^al-readme] |
| Bundled scripts | `build_preview.sh` (merges branches, pushes a preview branch) and `render_testplan.py`[^al-scripts] |

# refine: one board edge only

```
Backlog --refine--> READY --person, by hand--> Todo --> In Progress
```

Refinement moves a ticket along one edge and stops there.[^al-readme] The five phases:[^al-readme]

1. **Queue**: backlog tickets, scored by priority plus recency.
2. **Triage**: parallel sub-agents look for proof that a ticket has already shipped.
   Only shipped code counts as proof, not a spec file of the same name. They also look
   for duplicates elsewhere on the board. All proposed closes go to the person in one
   approval batch.
3. **Prepare**: one read-only recon agent per ticket returns the files a change would
   touch and the closest prior work.
4. **Refine**: an interview, one ticket at a time.
5. **Land**: specs go on their own branch, which is then merged into main without a PR.

**The readiness gate is six questions.** The interview runs until each one can be
answered:[^al-refine]

- What does the user see, and where?
- What triggers it, and what happens on the unhappy path?
- Which files does it touch? Each path must be checked and must exist.
- What is out of scope?
- How do you verify it works?
- What flag or config does it ship behind?

"Six boxes ticked means the ticket moves to the ready column." If any box is open, the
ticket stays where it is, with one line naming the open box. A ticket blocked by an open
`blockedBy` relation also stays put: "Ready means implementable now."[^al-refine]

**Ticket template** written back:[^al-refine]

- Summary;
- Context, with the original text quoted, never dropped;
- Scope;
- Codebase: only paths the recon found;
- **Acceptance criteria** as `- [ ]` "observable, checkable statements";
- Out of scope;
- Spec and Plan links, only if those files exist.

Field rules: set an estimate; record dependencies as `blockedBy` and `blocks` relations,
"not in prose"; propose a split into sub-issues when there are 3 or more separate
deliverables; **never set priority**, because the person owns it.[^al-refine]

# Two columns, two roles (1.3.0)

The ready column means "refined and implementable". The pickup column means "planned".
Refine may write only the first. "The user moves a ticket here by hand." On a board with
no separate ready column, "the gate simply isn't there".[^al-changelog] [^al-readme]

# nightshift: unattended build

nightshift builds from the pickup column, never the ready column. It admits only tickets
that have acceptance criteria. It runs one agent per ticket, each in its own worktree,
test first. Each ticket gets a branch and its own draft PR. A preview branch merges them
all for testing but gets no PR. A branch that conflicts is left out, never resolved by
the agent. "Nightshift never merges anything, never moves a ticket to done."[^al-readme]

# Gaps

- It has no decomposition from a vision or PRD; it assumes the tickets already exist.
  "Sub-issues are refined individually."[^al-refine]
- It has no epic or story model of its own, and no Gherkin.
- The **Land** phase merges spec commits into main without a PR. That conflicts with a
  rule that every change goes through a PR.[^al-readme]
- nightshift pushes branches and opens PRs with no one watching. That is fine for the
  owner's repo, but it is a reason to borrow the text, not install the plugin.

# Caveats

- The first sweep said nightshift opens "one draft pull request per ticket". That is
  right, and it also builds a shared preview branch with no PR.[^al-readme]

[^al-readme]: backlog/README.md
[^al-refine]: backlog/skills/refine/SKILL.md
[^al-changelog]: backlog/CHANGELOG.md (1.3.0, 2026-09-05)
[^al-plugin]: backlog/.claude-plugin/plugin.json and LICENSE
[^al-scripts]: backlog/scripts/build_preview.sh and render_testplan.py
[^al-page]: Repository page (stars)
