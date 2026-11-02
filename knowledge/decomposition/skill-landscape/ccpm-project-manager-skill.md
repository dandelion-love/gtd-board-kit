---
type: Reference
title: CCPM (Claude Code Project Manager) skill
description: The most-adopted GitHub-issues-native decomposition skill turns a PRD into an epic and numbered task files with depends_on, parallel and conflicts_with metadata, then syncs them as GitHub sub-issues; it has no story level and no approval gate before it writes.
resource: https://github.com/automazeio/ccpm/tree/3294c85b92b7846c1aec328ef40068022c841c5e/skill/ccpm
tags: [skill, decomposition, github-native, sub-issues, parallel-agents]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: cc-skill, title: "skill/ccpm/SKILL.md", resource: "https://github.com/automazeio/ccpm/blob/3294c85b92b7846c1aec328ef40068022c841c5e/skill/ccpm/SKILL.md", commit: 3294c85b92b7846c1aec328ef40068022c841c5e, accessed: 2026-11-02 }
  - { id: cc-structure, title: "skill/ccpm/references/structure.md", resource: "https://github.com/automazeio/ccpm/blob/3294c85b92b7846c1aec328ef40068022c841c5e/skill/ccpm/references/structure.md", commit: 3294c85b92b7846c1aec328ef40068022c841c5e, accessed: 2026-11-02 }
  - { id: cc-sync, title: "skill/ccpm/references/sync.md", resource: "https://github.com/automazeio/ccpm/blob/3294c85b92b7846c1aec328ef40068022c841c5e/skill/ccpm/references/sync.md", commit: 3294c85b92b7846c1aec328ef40068022c841c5e, accessed: 2026-11-02 }
  - { id: cc-plan, title: "skill/ccpm/references/plan.md", resource: "https://github.com/automazeio/ccpm/blob/3294c85b92b7846c1aec328ef40068022c841c5e/skill/ccpm/references/plan.md", commit: 3294c85b92b7846c1aec328ef40068022c841c5e, accessed: 2026-11-02 }
  - { id: cc-init, title: "skill/ccpm/references/scripts/init.sh", resource: "https://github.com/automazeio/ccpm/blob/3294c85b92b7846c1aec328ef40068022c841c5e/skill/ccpm/references/scripts/init.sh", commit: 3294c85b92b7846c1aec328ef40068022c841c5e, accessed: 2026-11-02 }
  - { id: cc-readme, title: "README.md", resource: "https://github.com/automazeio/ccpm/blob/3294c85b92b7846c1aec328ef40068022c841c5e/README.md", commit: 3294c85b92b7846c1aec328ef40068022c841c5e, accessed: 2026-11-02 }
  - { id: cc-git, title: "Repository git history (first 2025-08-19; skill relaunch 7d7e462, 2026-03-18; HEAD 2026-10-19)", resource: "https://github.com/automazeio/ccpm/commit/7d7e4623bc6d4c0c9ba66ca6bfecd7e5261dc697", commit: 7d7e4623bc6d4c0c9ba66ca6bfecd7e5261dc697, accessed: 2026-11-02 }
  - { id: cc-page, title: "Repository page (stars)", resource: "https://github.com/automazeio/ccpm", accessed: 2026-11-02 }
---

# Why it is here

It is the most widely adopted skill that makes **GitHub Issues the shared record** of a
decomposition. The first sweep did not list it.

# Provenance

| Fact | Value |
| --- | --- |
| Owner | automazeio; MIT licence[^cc-readme] |
| Stars / forks | 8.3k / 832 on 2026-11-02[^cc-page] |
| History | First commit 2025-08-19. Relaunched as an Agent Skills skill on 2026-03-18 (`7d7e462`). The skill folder is unchanged since then; repo HEAD is `3294c85`, 2026-10-19[^cc-git] |
| Harnesses | Claude Code, Codex, OpenCode, Factory, Amp, Cursor and more[^cc-readme] |
| Bundled scripts | 14 bash scripts. `init.sh` runs `gh auth login`, installs a third-party `gh` extension (`yahsan2/gh-sub-issue`) and creates labels with `--force`[^cc-init] |

# Flow

PRD, then Epic, then Task files, then GitHub sync, then parallel agents.[^cc-skill]

- **Plan:** a PRD from guided brainstorming, with user stories that "include acceptance
  criteria" and success criteria that are "measurable". Then a technical epic.[^cc-plan]
- **Structure:** the epic becomes numbered task files `001.md`, `002.md` and so on. Each
  has `depends_on`, `parallel` and `conflicts_with` in its frontmatter, plus acceptance
  criteria checkboxes, an effort size (XS to XL) and a Definition of Done checklist.[^cc-structure]
- **Sync:** the epic becomes an issue labelled `epic`. Tasks become **sub-issues** through
  the `gh-sub-issue` extension when it is installed. Files are renamed to their issue
  numbers, and dependency arrays are rewritten to real issue numbers.[^cc-sync]
- **Execute:** parallel agents work in an epic worktree.

# What is good

- **`parallel` and `conflicts_with`** are explicit fields. They answer the question an
  orchestrator of many agents asks, "can these run at once?", in data rather than prose.[^cc-structure]
- A repository safety check runs before any GitHub write, so it never syncs to the
  template repo.[^cc-sync]
- Progress is posted to issues as comments, with an "Acceptance Criteria Status" section.[^cc-sync]

# Gaps

- **Two levels only:** Epic, then Task. There is no Story level and no INVEST.
- **Dependencies stay in frontmatter.** It does not create native blocked-by edges.[^cc-sync]
- **No gate before writing.** Sync creates issues straight away. The only confirmations
  are before overwriting files and when re-syncing within 5 minutes.[^cc-sync] [^cc-plan]
- It classifies issues by labels (`epic`, `task`, `feature`), not issue types.[^cc-sync]
- The skill text has not changed since March 2026.

# What to borrow

- The `parallel` and `conflicts_with` fields, as text, for stories or tasks a
  coordinator may hand to several agents.
- The pre-write repository safety check.
- Not the install script: it installs a third-party extension and changes authentication.

[^cc-skill]: skill/ccpm/SKILL.md
[^cc-structure]: skill/ccpm/references/structure.md
[^cc-sync]: skill/ccpm/references/sync.md
[^cc-plan]: skill/ccpm/references/plan.md
[^cc-init]: skill/ccpm/references/scripts/init.sh
[^cc-readme]: README.md
[^cc-git]: Repository git history (first 2025-08-19; skill relaunch 7d7e462, 2026-03-18; HEAD 2026-10-19)
[^cc-page]: Repository page (stars)
