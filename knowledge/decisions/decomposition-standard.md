---
type: Decision
title: How work decomposes into epics, stories and steps
description: Epics hold stories, a story holds steps, chores are story-level work, findings are the only result Kind; a read-only ready check, two-part epic done, server-opened PRs and a small gate set keep agents honest.
tags: [contract, work-items, decomposition]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:45:00Z }
---

# Decision

The owner settled the nine questions that the
[decomposition research](/decomposition/overview.md) left open.

## Levels

1. **Epic, story, step.** An epic holds stories. A story holds **steps**: checklist items
   (or sub-issues) inside it, with no PR of their own. Feature is a label, not a level.
2. **Chore is story-level work.** Technical work that has its own PR (an enabler, a
   chore, tech debt) is a story-level issue of Kind `chore`, never a step. This replaces
   the old `task` Kind, which mixed the two levels.
3. **Spike, research and bug are story-level work** too, as the
   [kind-to-level mapping](/decomposition/work-item-kinds/kind-to-level-mapping.md)
   describes.

## Results are not work

4. **`finding` stays a Kind.** A finding is the issue that records a result, closed by
   a person's review.
5. **`question` and `decision` retire as Kinds.** A question is `attention` plus a
   `needs:<who>` label on the item it blocks; it becomes its own story only when
   answering it is work. A decision is a Decision concept in the repo's knowledge
   bundle, added by the PR of the story that made it and linked from its epic.

## Done and ready

6. **An epic is done when both hold:** every child is closed, and the epic's own
   outcome check (one or two criteria in its body) has passed, confirmed by a person.
7. **Ready is a read-only check, not a judgement.** A server tool reads the issue graph
   and returns `ready`, `needs-refinement` (with what is missing) or `ready-blocked`
   (ready, but an open blocker remains). Its rules: acceptance criteria present, no open
   question, every blocker a native dependency link, no cycle, size within the pull
   limit, and a title and summary that say what the story delivers
   ([clear titles and summaries](clear-titles-and-summaries.md)). The kit specifies it in `server-spec/` with conformance checks before any
   server builds it; skills call it rather than restate the rules.

## Agent work

8. **The unit of agent work is one or more stories.** The session that owns them may
   combine them on an integration (release-candidate) branch. The agent **claims every
   story it works on**, each with its own lease; working an unclaimed story is not
   allowed, even inside a combined branch.
9. **Agents open PRs through the gtd MCP server**, never with their own GitHub tool under
   the owner's account. The server opens the PR with its own GitHub App token and records
   which joined agent asked, so the agent's identity comes from the
   [agent sign-in](/model/agent-sign-in.md) and the owner can be the required reviewer;
   GitHub never lets an author approve their own PR. No App per agent is needed.

## Gates

10. The gate set is the [minimum gate set](/decomposition/human-gates/minimum-gate-set-solo-owner.md),
    with two skips: an epic of **three stories or fewer** skips epic-intent approval
    (story-ready covers it), and an epic that changes an **existing, working system**
    skips walking-skeleton approval.

## Carriers

11. **Kind is an organization Issue Type.** A repo without Issue Types (a personal
    account) uses a `kind:<kind>` label instead, as a fallback only; a repo that has
    types never carries both.

# Consequences

- Repos rename `task` to `chore` (story-level) or turn it into steps, and stop creating
  `question` and `decision` issues. A repo's existing items move when it next repins the
  kit; the [per-repo layer](/decisions/per-repo-layer.md) may keep a different name for
  a while and say so.
- Follow-up changes: the ready check in `server-spec/` and its runner checks; claim
  rules for combined branches (done in kit 0.14.0: `board-claim`, an optional
  `branch` on `item_claim`, conformance C14); a server tool that opens PRs;
  the board profile's Kind list.
- Until a server offers the ready tool ([ready check](../../server-spec/ready-check.md)), an agent treats an item as ready only when a person has
  added `agent-ready`.

See [work items live on the board](/decisions/work-items-live-on-the-board.md) and
[the kit is the interface](/decisions/kit-is-the-interface.md).
