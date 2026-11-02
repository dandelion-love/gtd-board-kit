---
type: Comparison
title: Epic, story and task skills compared (2025-2026)
description: One rubric scores twelve agent skills and tools that decompose or refine work; no single one fits a GitHub-native, agent-run board, so borrow text and gates from five of them and install none.
tags: [comparison, skills, decomposition, definition-of-ready, human-gate, github-native]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: bp-skill, title: "github/awesome-copilot skills/breakdown-plan/SKILL.md", resource: "https://github.com/github/awesome-copilot/blob/81f9382067ced59c16ce9e34cd32465199f44438/skills/breakdown-plan/SKILL.md", commit: 81f9382067ced59c16ce9e34cd32465199f44438, accessed: 2026-11-02 }
  - { id: gi-skill, title: "github/awesome-copilot skills/github-issues/SKILL.md", resource: "https://github.com/github/awesome-copilot/blob/81f9382067ced59c16ce9e34cd32465199f44438/skills/github-issues/SKILL.md", commit: 81f9382067ced59c16ce9e34cd32465199f44438, accessed: 2026-11-02 }
  - { id: rh-skill, title: "toddward/red-hat-agile-skill SKILL.md", resource: "https://github.com/toddward/red-hat-agile-skill/blob/141eb736e4978166cd33287f67ca5a4423973852/SKILL.md", commit: 141eb736e4978166cd33287f67ca5a4423973852, accessed: 2026-11-02 }
  - { id: keel-skill, title: "williamweatherholtz/keel backlog-refinement SKILL.md", resource: "https://github.com/williamweatherholtz/keel/blob/5015c2de05c5709154b8513005e87e5a1fe331d2/.claude/skills/backlog-refinement/SKILL.md", commit: 5015c2de05c5709154b8513005e87e5a1fe331d2, accessed: 2026-11-02 }
  - { id: apo-skill, title: "alirezarezvani/claude-skills product-team/agile-product-owner SKILL.md (plugin 2.14.5)", resource: "https://github.com/alirezarezvani/claude-skills/blob/e4a1dc3695908dd5a6c811cc76ab7aa4cf95f2f0/product-team/agile-product-owner/skills/agile-product-owner/SKILL.md", commit: e4a1dc3695908dd5a6c811cc76ab7aa4cf95f2f0, accessed: 2026-11-02 }
  - { id: apo-script, title: "agile-product-owner scripts/user_story_generator.py", resource: "https://github.com/alirezarezvani/claude-skills/blob/e4a1dc3695908dd5a6c811cc76ab7aa4cf95f2f0/product-team/agile-product-owner/skills/agile-product-owner/scripts/user_story_generator.py", commit: e4a1dc3695908dd5a6c811cc76ab7aa4cf95f2f0, accessed: 2026-11-02 }
  - { id: apo-page, title: "alirezarezvani/claude-skills repository page (stars)", resource: "https://github.com/alirezarezvani/claude-skills", accessed: 2026-11-02 }
  - { id: pm-usw, title: "louis3979/pm-tech-skills user-story-writer SKILL.md", resource: "https://github.com/louis3979/pm-tech-skills/blob/f655a7b550c03d7872dacb018d4ec9d7905f877d/pm-tech-product/skills/user-story-writer/SKILL.md", commit: f655a7b550c03d7872dacb018d4ec9d7905f877d, accessed: 2026-11-02 }
  - { id: pm-acg, title: "louis3979/pm-tech-skills acceptance-criteria-generator SKILL.md", resource: "https://github.com/louis3979/pm-tech-skills/blob/f655a7b550c03d7872dacb018d4ec9d7905f877d/pm-tech-product/skills/acceptance-criteria-generator/SKILL.md", commit: f655a7b550c03d7872dacb018d4ec9d7905f877d, accessed: 2026-11-02 }
  - { id: pm-readme, title: "louis3979/pm-tech-skills README and marketplace.json (3.2.0)", resource: "https://github.com/louis3979/pm-tech-skills/blob/f655a7b550c03d7872dacb018d4ec9d7905f877d/README.md", commit: f655a7b550c03d7872dacb018d4ec9d7905f877d, accessed: 2026-11-02 }
  - { id: pm-page, title: "louis3979/pm-tech-skills repository page (stars)", resource: "https://github.com/louis3979/pm-tech-skills", accessed: 2026-11-02 }
  - { id: al-refine, title: "applab-nl/claude-code-plugins backlog/skills/refine/SKILL.md", resource: "https://github.com/applab-nl/claude-code-plugins/blob/a5ce3da2c4a8be46e1d06c09037cff6b325127e6/backlog/skills/refine/SKILL.md", commit: a5ce3da2c4a8be46e1d06c09037cff6b325127e6, accessed: 2026-11-02 }
  - { id: bm-tickets-tpl, title: "bmad-code-org/BMAD-METHOD bmad-agent-po tickets-template.toml", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/skills/bmad-agent-po/assets/tickets-template.toml", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-slice, title: "bmad-code-org/BMAD-METHOD bmad-agent-po references/slice.md", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/skills/bmad-agent-po/references/slice.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-ticket-tpl, title: "bmad-code-org/BMAD-METHOD bmad-agent-po ticket-template.md", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/skills/bmad-agent-po/assets/ticket-template.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: bm-changelog, title: "bmad-code-org/BMAD-METHOD CHANGELOG.md", resource: "https://github.com/bmad-code-org/BMAD-METHOD/blob/bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41/CHANGELOG.md", commit: bd70c643a7ec85d1ec2e88076b3fbdd8e4517f41, accessed: 2026-11-02 }
  - { id: tm-readiness, title: "timo-jakob/timos-claude-code-plugins development/agents/story-readiness.md", resource: "https://github.com/timo-jakob/timos-claude-code-plugins/blob/14cbf932262c24c694dde5f3085f3edf8067ae85/development/agents/story-readiness.md", commit: 14cbf932262c24c694dde5f3085f3edf8067ae85, accessed: 2026-11-02 }
  - { id: cc-structure, title: "automazeio/ccpm skill/ccpm/references/structure.md", resource: "https://github.com/automazeio/ccpm/blob/3294c85b92b7846c1aec328ef40068022c841c5e/skill/ccpm/references/structure.md", commit: 3294c85b92b7846c1aec328ef40068022c841c5e, accessed: 2026-11-02 }
  - { id: saga-market, title: "Saga on the Visual Studio Marketplace (Haribrothers.saga)", resource: "https://marketplace.visualstudio.com/items?itemName=Haribrothers.saga", version: 0.1.0, accessed: 2026-11-02 }
  - { id: saga-repo, title: "haribrothers/saga repository (README, LICENSE, git history)", resource: "https://github.com/haribrothers/saga/tree/afbffa2d9bd6cf735cd8ac87c3d1afa484f1f080", commit: afbffa2d9bd6cf735cd8ac87c3d1afa484f1f080, accessed: 2026-11-02 }
  - { id: sk-tti, title: "github/spec-kit extensions/github/commands/speckit.github.taskstoissues.md", resource: "https://github.com/github/spec-kit/blob/7370e592f3cd9c06e5b698983957e227c75b30e2/extensions/github/commands/speckit.github.taskstoissues.md", commit: 7370e592f3cd9c06e5b698983957e227c75b30e2, accessed: 2026-11-02 }
  - { id: sk-deprecated, title: "github/spec-kit templates/commands/taskstoissues.md (deprecation notice)", resource: "https://github.com/github/spec-kit/blob/7370e592f3cd9c06e5b698983957e227c75b30e2/templates/commands/taskstoissues.md", commit: 7370e592f3cd9c06e5b698983957e227c75b30e2, accessed: 2026-11-02 }
  - { id: sk-page, title: "github/spec-kit repository page (stars)", resource: "https://github.com/github/spec-kit", accessed: 2026-11-02 }
---

# Scope

Twelve candidates, each read at a pinned commit on 2026-11-02. Each strong candidate has
its own file:

- [breakdown-plan and github-issues](github-awesome-copilot-breakdown.md)
- [Red Hat agile skill](red-hat-agile-skill.md)
- [Keel backlog-refinement](keel-backlog-refinement.md)
- [AppLab backlog plugin](applab-backlog-plugin.md)
- [BMAD Method](bmad-method.md)
- [story-readiness gate](timos-story-readiness-gate.md), new in this sweep
- [CCPM](ccpm-project-manager-skill.md), new in this sweep

The packaging format is covered in [Agent Skills](agent-skills-standard.md). The weaker
candidates are summed up in the short section below.

# Rubric

Each criterion is scored from 0 to 3.

| Criterion | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Hierarchy | none | one level | two or three levels | three or more levels with sizing rules |
| Templates | none | output shape only | templates for some levels | full templates for every level |
| AC style | none | free checkboxes | one format with guidance | format plus coverage rules plus a measurability rule |
| DoD / DoR | none | named only | one as a template | DoD kept apart from AC, or a pass/fail ready gate |
| Dependencies | none | prose | structured field | native blocked-by, or a checked acyclic graph |
| Human gate | none | implicit review | explicit confirm step | a step only a person can take |
| GitHub-native fit | none | via sync or mirror | issues and labels | native sub-issues, types and blocked-by |
| Maintenance / provenance | unknown | one author, low use | active, or org-owned with a stale file | org-backed, active, licensed, released |
| Safety (bundled code) | opaque binary or unattended push | scripts that write remotely or install | local scripts, or instructions to add CI | text only |

# Scores

| Candidate | Hier | Tmpl | AC | DoD/DoR | Deps | Gate | GitHub | Maint | Safety | Total /27 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BMAD Method, main-branch ticket tree | 3 | 3 | 3 | 3 | 3 | 3 | 1 | 3 | 2 | **24** |
| story-readiness gate and refine-issue | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 1 | 1 | **21** |
| awesome-copilot breakdown-plan | 3 | 3 | 1 | 2 | 2 | 1 | 2 | 2 | 2 | 18 |
| awesome-copilot github-issues (companion) | 2 | 2 | 1 | 0 | 3 | 1 | 3 | 3 | 3 | 18 |
| AppLab backlog (refine, nightshift) | 1 | 2 | 2 | 3 | 3 | 3 | 2 | 1 | 1 | 18 |
| Red Hat agile skill | 2 | 3 | 3 | 3 | 2 | 1 | 0 | 1 | 2 | 17 |
| Keel backlog-refinement | 2 | 1 | 3 | 3 | 2 | 2 | 0 | 1 | 1 | 15 |
| CCPM | 2 | 2 | 1 | 2 | 2 | 1 | 2 | 2 | 1 | 15 |
| pm-tech-skills (user-story-writer, AC generator) | 2 | 2 | 3 | 2 | 1 | 1 | 0 | 1 | 3 | 15 |
| Agile Product Owner | 2 | 2 | 2 | 2 | 1 | 1 | 0 | 2 | 2 | 14 |
| Spec Kit taskstoissues | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 3 | 2 | 13 |
| Saga for VS Code | 3 | 2 | 2 | 1 | 0 | 2 | 0 | 1 | 1 | 12 |

The totals rank, but they do not decide. A kit needs the best answer per **criterion**,
and that answer comes from a different candidate each time. The judgements behind each
score are in the concept files.

# Weaker candidates in brief

- **Agile Product Owner** (`alirezarezvani/claude-skills`; repo 28.7k stars, MIT, plugin
  2.14.5, file changed 2026-10-30):[^apo-page] [^apo-skill]
  - minimum criteria counts by story size (1-2 points need 3-4 criteria, 13 or more means
    split), five epic-splitting techniques, an INVEST table, a DoD checklist;
  - its `user_story_generator.py` is pure Python with no input or output. It prints
    canned stories with criteria like "Then the result is displayed", which is weaker than
    the rules in its own text;[^apo-script]
  - the README claims "5,200+" stars, but the page shows 28.7k.[^apo-page]
- **pm-tech-skills** (3 stars, MIT, 3.2.0, first commit 2026-09-11):[^pm-page] [^pm-readme]
  - 58 skills in 3 plugins;
  - `acceptance-criteria-generator` has the widest coverage taxonomy found: happy,
    negative, **permission**, **state**, and boundary or concurrency cases, each
    "independently testable";[^pm-acg]
  - `user-story-writer` also asks for an **epic-level** DoD that is more than "all
    stories closed".[^pm-usw]
- **Spec Kit `taskstoissues`** (142.7k stars):[^sk-page]
  - turns each `T001`-style task into a **flat** issue, skipping IDs already filed, and
    refuses any repo other than the git remote;[^sk-tti]
  - the core command is deprecated in favour of a `github` extension (September to
    October 2026);[^sk-deprecated]
  - no epic or story hierarchy.
- **Saga for VS Code** (publisher Haribrothers, v0.1.0, 4 installs, MIT; 47 commits from
  2026-06-27 to 2026-07-04, none since):[^saga-market] [^saga-repo]
  - epics, stories and typed subtasks, INVEST checks, Gherkin with a happy path and an
    edge case, split proposals that a person reviews before saving;
  - two-way sync to **Jira Cloud and Azure DevOps only**;
  - sends registered context files to the AI provider you choose.[^saga-market]

# Findings by criterion

| Criterion | Best source | What it does |
| --- | --- | --- |
| Hierarchy and templates | breakdown-plan | Epic, Feature, Story or Enabler, Task templates with a DoD per level[^bp-skill] |
| GitHub mechanics | github-issues | Native sub-issues, issue types over labels, blocked-by through REST or GraphQL[^gi-skill] |
| AC versus DoD | Red Hat | AC per story, DoD once per project; "accepted" differs from "done"[^rh-skill] |
| Measurable criteria | Keel | One Gherkin scenario per behaviour; every Then has a value and a unit[^keel-skill] |
| AC coverage | pm-tech-skills | Happy, negative, permission, state and boundary classes[^pm-acg] |
| Ready gate | story-readiness | Four pass/fail checks and READY or NEEDS_REFINEMENT JSON, from a read-only judge[^tm-readiness] |
| Dependencies | story-readiness and BMAD | Judge whether a dependency is declared, not whether it is closed; `after` is a prerequisite, not order[^tm-readiness] [^bm-tickets-tpl] |
| Human gate | AppLab and BMAD | A ready column separate from a hand-moved pickup column; `refined` only on the person's approval; `plan_checkpoint` and `done_checkpoint`[^al-refine] [^bm-ticket-tpl] [^bm-tickets-tpl] |
| Story size for agents | BMAD | "sized for one agent session", not one sprint[^bm-slice] |
| Parallel hints | CCPM | `parallel` and `conflicts_with` fields per task[^cc-structure] |

# Recommendation: borrow text and gates, install nothing

1. **Templates.** Start from breakdown-plan's Epic and Story sections. Store children as
   native sub-issues and kinds as issue types, as github-issues describes. Drop its
   Actions-workflow section and sprint KPIs.
2. **Acceptance criteria.** Use Given/When/Then, one scenario per behaviour. Every Then
   names a value and a unit (Keel). Cover happy, error, boundary and, where it applies,
   permission and state cases (pm-tech-skills).
3. **DoD apart from AC.** Write one project DoD. Each story says only how it fits the DoD,
   and the epic has its own "Done when" (Red Hat, BMAD). Write this in your own words:
   Red Hat has no licence.
4. **A ready gate as a pure judge.** A read-only check returns READY or NEEDS_REFINEMENT
   with the questions that would unblock the story. It tests:
   - criteria are testable;
   - scope is bounded;
   - prerequisites are declared as native blocked-by, and the graph is acyclic;
   - nothing contradicts.

   A declared but open blocker means READY-but-queued (story-readiness). Add AppLab's
   "which files, by verified path" question.
5. **Two human gates.** The agent may move a story to Ready; only a person moves it to
   the build queue (AppLab). A story is marked refined only when the person approves its
   criteria. A build stops at "built", and a person marks it done (BMAD).
6. **Size stories to one agent session.** Mark parallel-safe work and file conflicts in
   fields (BMAD, CCPM).
7. **Do not adopt:**
   - any plugin's bundled scripts;
   - AppLab's spec merge into main without a PR;
   - breakdown-plan's workflow generation;
   - CCPM's `init.sh`;
   - auto-accept thresholds or an AI approver where a person must merge;
   - BMAD's full persona method.

# First-sweep claims checked

| Claim | Verdict |
| --- | --- |
| breakdown-plan "best GitHub fit" | Partly. Strong templates, but checkbox children and labels, and it suggests writing workflows. github-issues and story-readiness are more native |
| Red Hat "borrow as template" | Licence problem: there is no licence. Borrow the ideas only |
| Keel 0.2.0 with a DoR gate | Confirmed. The DoR checklist itself is not written in the file |
| AppLab "one draft PR per ticket" and a hand-move gate | Confirmed. It also merges spec commits to main without a PR |
| BMAD sharding, story files, readiness gate, sprint-status contract | **Outdated.** shard-doc retired, create-story deprecated, readiness folded into sprint-planning (v6.11, Aug 2026); main replaces these with a PO ticket tree[^bm-changelog] |
| Saga syncs only to Jira and Azure DevOps | Confirmed. It is also v0.1.0 with 4 installs and no commits since July 2026 |
| "Only AI-DLC and the AppLab hand-move make approval a real step" | Wrong now. BMAD (`refined`, checkpoints) and story-readiness (a person approves the rewrite) also have structural gates |
| Agile Product Owner "provenance thin, single-author" | Single author, but a 28.7k-star repo that is actively released. Thin on GitHub fit, not on maintenance |

# Open questions

- Should the kit's ready gate be a skill (text) or a deterministic script over the issue
  graph? The source splits the two: an agent judges the specification, a script enforces
  sequencing.
- Is one agent session the right story size for the owner's agents, or should a story
  allow several sessions, with tasks as the session unit?
- Star counts and versions above were taken on one day. They change quickly.

[^bp-skill]: github/awesome-copilot skills/breakdown-plan/SKILL.md
[^gi-skill]: github/awesome-copilot skills/github-issues/SKILL.md
[^rh-skill]: toddward/red-hat-agile-skill SKILL.md
[^keel-skill]: williamweatherholtz/keel backlog-refinement SKILL.md
[^apo-skill]: alirezarezvani/claude-skills product-team/agile-product-owner SKILL.md (plugin 2.14.5)
[^apo-script]: agile-product-owner scripts/user_story_generator.py
[^apo-page]: alirezarezvani/claude-skills repository page (stars)
[^pm-usw]: louis3979/pm-tech-skills user-story-writer SKILL.md
[^pm-acg]: louis3979/pm-tech-skills acceptance-criteria-generator SKILL.md
[^pm-readme]: louis3979/pm-tech-skills README and marketplace.json (3.2.0)
[^pm-page]: louis3979/pm-tech-skills repository page (stars)
[^al-refine]: applab-nl/claude-code-plugins backlog/skills/refine/SKILL.md
[^bm-tickets-tpl]: bmad-code-org/BMAD-METHOD bmad-agent-po tickets-template.toml
[^bm-slice]: bmad-code-org/BMAD-METHOD bmad-agent-po references/slice.md
[^bm-ticket-tpl]: bmad-code-org/BMAD-METHOD bmad-agent-po ticket-template.md
[^bm-changelog]: bmad-code-org/BMAD-METHOD CHANGELOG.md
[^tm-readiness]: timo-jakob/timos-claude-code-plugins development/agents/story-readiness.md
[^cc-structure]: automazeio/ccpm skill/ccpm/references/structure.md
[^saga-market]: Saga on the Visual Studio Marketplace (Haribrothers.saga)
[^saga-repo]: haribrothers/saga repository (README, LICENSE, git history)
[^sk-tti]: github/spec-kit extensions/github/commands/speckit.github.taskstoissues.md
[^sk-deprecated]: github/spec-kit templates/commands/taskstoissues.md (deprecation notice)
[^sk-page]: github/spec-kit repository page (stars)
