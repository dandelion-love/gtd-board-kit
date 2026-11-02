---
type: Reference
title: GitHub awesome-copilot breakdown-plan (and the github-issues skill)
description: The GitHub-owned breakdown-plan skill has the fullest Epic-to-Task issue templates, but it models children as checkbox lists and labels; its sibling github-issues skill supplies the native sub-issue, type and blocked-by mechanics.
resource: https://github.com/github/awesome-copilot/tree/81f9382067ced59c16ce9e34cd32465199f44438/skills/breakdown-plan
tags: [skill, decomposition, github-native, templates, epic, story]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: bp-skill, title: "skills/breakdown-plan/SKILL.md", resource: "https://github.com/github/awesome-copilot/blob/81f9382067ced59c16ce9e34cd32465199f44438/skills/breakdown-plan/SKILL.md", commit: 81f9382067ced59c16ce9e34cd32465199f44438, accessed: 2026-11-02 }
  - { id: bp-history, title: "git log of skills/breakdown-plan (file last changed in caab1f62, 2026-02-24)", resource: "https://github.com/github/awesome-copilot/commit/caab1f623bb68a330f294a11279597d7ae7be737", commit: caab1f623bb68a330f294a11279597d7ae7be737, accessed: 2026-11-02 }
  - { id: bp-epic-pm, title: "skills/breakdown-epic-pm/SKILL.md", resource: "https://github.com/github/awesome-copilot/blob/81f9382067ced59c16ce9e34cd32465199f44438/skills/breakdown-epic-pm/SKILL.md", commit: 81f9382067ced59c16ce9e34cd32465199f44438, accessed: 2026-11-02 }
  - { id: gi-skill, title: "skills/github-issues/SKILL.md (last changed d277f399, 2026-10-07)", resource: "https://github.com/github/awesome-copilot/blob/81f9382067ced59c16ce9e34cd32465199f44438/skills/github-issues/SKILL.md", commit: 81f9382067ced59c16ce9e34cd32465199f44438, accessed: 2026-11-02 }
  - { id: gi-subissues, title: "skills/github-issues/references/sub-issues.md", resource: "https://github.com/github/awesome-copilot/blob/81f9382067ced59c16ce9e34cd32465199f44438/skills/github-issues/references/sub-issues.md", commit: 81f9382067ced59c16ce9e34cd32465199f44438, accessed: 2026-11-02 }
  - { id: gi-deps, title: "skills/github-issues/references/dependencies.md", resource: "https://github.com/github/awesome-copilot/blob/81f9382067ced59c16ce9e34cd32465199f44438/skills/github-issues/references/dependencies.md", commit: 81f9382067ced59c16ce9e34cd32465199f44438, accessed: 2026-11-02 }
  - { id: ac-repo, title: "github/awesome-copilot repository page (stars, license)", resource: "https://github.com/github/awesome-copilot", accessed: 2026-11-02 }
---

# Provenance

| Fact | Value |
| --- | --- |
| Owner | GitHub (the `github` organisation); MIT licence[^ac-repo] |
| Stars / forks | 40.3k / 5.2k on 2026-11-02[^ac-repo] |
| Pinned commit | `81f9382` (repo HEAD, 2026-11-02)[^bp-skill] |
| breakdown-plan history | Added as a prompt on 2025-08-04; converted to a skill on 2026-02-24; unchanged since[^bp-history] |
| Bundled scripts | None. One `SKILL.md` file[^bp-skill] |

The collection is very active. This file is not: it has not changed for eight months.

# The breakdown-* family

| Skill | Job |
| --- | --- |
| `breakdown-epic-pm` | Epic PRD: goal, personas, journeys, functional and non-functional requirements, KPIs, out of scope, business value[^bp-epic-pm] |
| `breakdown-epic-arch`, `breakdown-feature-prd`, `breakdown-feature-implementation`, `breakdown-test` | Architecture, feature PRD, technical plan, test plan |
| `breakdown-plan` | Turns those files into a project plan plus an issue-creation checklist[^bp-skill] |

`breakdown-plan` expects those earlier files under `docs/ways-of-work/plan/...` before it
runs.[^bp-skill]

# What breakdown-plan defines

- **Hierarchy:** Epic, then Feature, then Story or Enabler, then Test and Task.[^bp-skill]
- **Issue templates** for Epic, Feature, User Story and Technical Enabler. Each has
  acceptance criteria as a checkbox list and a **Definition of Done** checklist, plus
  labels, a parent link and an estimate.[^bp-skill]
- **Story statement:** "As a {user}, I want {goal} so that {benefit}". Criteria are
  "specific testable requirement" checkboxes. Gherkin is not used.[^bp-skill]
- **Principles named, not enforced:** INVEST, Definition of Ready and Definition of
  Done appear as one-line bullets. Nothing checks them as pass or fail.[^bp-skill]
- **Dependencies:** "Blocks" and "Blocked by" sections in the body, and four dependency
  types: blocks, related, prerequisite, parallel.[^bp-skill]
- **Sizing:** Fibonacci points 1 to 8 for stories ("13+ needs breakdown"); t-shirt sizes
  for epics and features.[^bp-skill]
- **Board:** Kanban columns (Backlog, Sprint Ready, In Progress, In Review, Testing,
  Done) and Projects custom fields (Priority, Value, Component, Estimate, Sprint, Epic).[^bp-skill]

# Gaps for an agent-run GitHub board

- **Children as checkboxes.** Child issues are `- [ ] #N` lines in the parent body. The
  skill never mentions native sub-issues, issue types or native blocked-by.[^bp-skill]
- **Workflows.** Section 9 tells the agent to write GitHub Actions workflows that create
  issues and move cards.[^bp-skill] A kit whose agents may not touch workflow files must
  remove this section.
- **No human gate.** The output is a plan file and a checklist, and nothing in the skill
  makes a person approve them. Approval happens only if someone reviews the plan.
- **Team assumptions.** Sprint velocity, focus factor and "stakeholder satisfaction"
  KPIs assume a team, not one owner working with agents.

# The companion that fixes the storage layer: `github-issues`

The same collection has a newer `github-issues` skill. It was added 2026-01-08 and last
changed 2026-10-07.[^gi-skill] It covers:

- native **sub-issues**: up to 100 per parent, nested up to 8 levels[^gi-subissues];
- **issue types**: "prefer issue types over labels for categorization", and set the type
  through `gh api`, since `gh issue create` has no `--type` flag[^gi-skill];
- native **blocked-by** dependencies through REST or GraphQL, since no MCP tool exists
  for them[^gi-deps];
- org-level **issue fields** for priority and dates.[^gi-skill]

Taken together: the breakdown-plan **templates** for content, and the github-issues
**mechanics** for structure.

# What to borrow

- The Epic, Story and Enabler template sections, the per-level DoD checklists and the
  four dependency types, as text.
- Swap the checkbox child lists for sub-issues, and swap the `epic` and `user-story`
  labels for issue types, following github-issues.
- Drop the Actions-workflow section and the sprint KPIs.

See the scores in [the landscape comparison](skill-landscape-comparison.md).

# Caveats

- The first sweep said breakdown-plan has "a Projects board configuration with custom
  fields" and "best GitHub fit". The fields are there, but as prose to set up by hand,
  and the hierarchy uses checkboxes, not sub-issues. Its GitHub fit is good for a 2025
  design and partial for 2026 GitHub.

[^bp-skill]: skills/breakdown-plan/SKILL.md
[^bp-history]: git log of skills/breakdown-plan (file last changed in caab1f62, 2026-02-24)
[^bp-epic-pm]: skills/breakdown-epic-pm/SKILL.md
[^gi-skill]: skills/github-issues/SKILL.md (last changed d277f399, 2026-10-07)
[^gi-subissues]: skills/github-issues/references/sub-issues.md
[^gi-deps]: skills/github-issues/references/dependencies.md
[^ac-repo]: github/awesome-copilot repository page (stars, license)
