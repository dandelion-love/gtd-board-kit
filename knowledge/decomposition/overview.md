---
type: Synthesis
title: Decomposing work into epics, stories and tasks
description: One-page synthesis of the decomposition research for a GitHub-native board worked by AI agents and one owner, and the decisions it leaves open.
tags: [decomposition, epic, story, task, synthesis]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T06:00:00Z }
---

# What this is

Research only. It records what established practice, current agent methods and GitHub
itself say about breaking work into epics, stories and tasks. It is the evidence for a
later decision; it does not set a kit rule. Each claim is sourced in the linked concepts.

# Findings

1. **The hierarchy is convention, not Scrum.** The Scrum Guide defines backlog items, a
   Product Goal and a Definition of Done, and no Epic, Story, Task or Definition of Ready.
   Epic and Story come from XP and later practice; Feature predates SAFe in Feature-Driven
   Development. See [Scrum's scope](agile-foundations/scrum-guide-2020-scope.md) and
   [origins](agile-foundations/origins-of-epic-story-feature.md).
2. **Three levels are enough; Feature is a label.** Add a level only when a different
   group owns it or a cadence is planned at it. The standard must also say whether a Task
   sits under a Story (Azure DevOps) or beside it (Jira). See
   [hierarchies compared](agile-foundations/work-item-hierarchies-compared.md).
3. **For agents, size by reviewable outcome.** One coherent unit per agent session and per
   PR, with a "done when" check, inside the length of task the agent completes reliably.
   Story points matter less. See [sizing for agents](agile-foundations/sizing-work-for-ai-agents.md)
   and [splitting patterns](agile-foundations/story-splitting-patterns.md).
4. **Agent methods split backlog from execution.** AI-DLC decomposes intent into units and
   gates each stage; Superpowers, Spec Kit and Kiro decompose a design into execution
   steps. None supplies a board. See
   [backlog vs execution decomposition](agentic-methods/backlog-vs-execution-decomposition.md).
5. **No published skill fits; borrow text and gates, install nothing.** Each candidate is
   strongest at one part (readiness gate, criteria vs Done, approval steps). See the
   [skill landscape comparison](skill-landscape/skill-landscape-comparison.md).
6. **GitHub carries every part and checks none.** Issue types, sub-issues, dependencies,
   issue fields and Projects hold the model, but GitHub never validates parent rules,
   cycles, required fields on API writes, or parent closing. The kit must. Types and issue
   fields exist only in organizations. See the
   [mapping onto GitHub](github-primitives/mapping-epic-story-task-onto-github.md).
7. **Not every Kind is work.** Spikes, research, bugs and chores are story-level work.
   A question is a flag on the item it blocks; decisions and findings are knowledge a story
   produces. See the [kind-to-level mapping](work-item-kinds/kind-to-level-mapping.md).
8. **Done needs a criterion-to-evidence chain.** Agents are documented to game tests, and
   passing tests overstate correctness. A person owns the criteria, the PR carries fresh
   evidence per criterion and lists test changes, and a person's merge is Done. See the
   [criterion-to-evidence chain](acceptance-and-verification/criterion-to-evidence-chain.md).
9. **Five gates are enough for one owner.** Epic intent, story ready, walking-skeleton
   merge, story merge, and outside effects. GitHub enforces only merge and deploy gates;
   the rest are conventions agents must keep. See the
   [minimum gate set](human-gates/minimum-gate-set-solo-owner.md).

# Decisions left to the owner

The owner has since settled these in [How work decomposes](/decisions/decomposition-standard.md); the leans below are the research's drafts.

| # | Decision | Draft lean |
| --- | --- | --- |
| 1 | Task under Story, or beside it | under: a checklist item or sub-issue; own issue only with its own PR |
| 2 | Keep `question`, `finding`, `decision` as Kinds | retire as issues; use `needs:*` and bundle concepts |
| 3 | Split `task` (enabler story vs step) | yes |
| 4 | Epic acceptance: all stories merged, or an outcome check too | both |
| 5 | Ready gate as skill text or a script over the issue graph | script, read-only |
| 6 | Unit of agent work: story or task | story = one PR, one session where possible |
| 7 | Label fallback for repos without types and fields | yes, `kind:*` labels |
| 8 | G1 for small epics; G3 for brownfield | optional for both |
| 9 | Agent identity: bot account or App | App, so the owner can review |

# Caveats

- Many sources move fast (tool versions, GitHub previews). Concepts pin versions and dates;
  re-check before relying on a limit.
- The public guard rejects URLs with a numeric path segment, so some sources cite a site's
  front page with the item named in the title, or a changelog entry by its slug.
- The decision for the kit is a separate change, after the owner answers the table above.
