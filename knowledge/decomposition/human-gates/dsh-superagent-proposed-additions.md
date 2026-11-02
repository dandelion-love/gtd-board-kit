---
type: Note
title: dsh-superagent page, proposed additions from the Epic/Story/Task research
description: Three additions to the kit's dsh-superagent reference page (Ticket vs Story, what a Mandate freezes from a Story, observe mode for proactive decomposition), and nothing it already says.
tags: [reference, agents, authorization, decomposition, proposal]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: kit-dsh, title: "gtd-board-kit: dsh-superagent reference page", resource: "https://github.com/owner/gtd-board-kit/blob/main/knowledge/references/dsh-superagent.md", accessed: 2026-11-02}
  - {id: kit-claims, title: "gtd-board-kit: Claims and leases", resource: "https://github.com/owner/gtd-board-kit/blob/main/knowledge/model/claims-and-leases.md", accessed: 2026-11-02}
  - {id: dsh-phil, title: "dsh-superagent-prototype: 000 Philosophy", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 000-philosophy.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e, version: 0.1.0}
  - {id: dsh-domain, title: "dsh-superagent-prototype: 001 Domain model", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 001-domain.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: dsh-auth, title: "dsh-superagent-prototype: 002 Authorization", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 002-authorization.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: dsh-exec, title: "dsh-superagent-prototype: 003 Execution", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 003-execution.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
  - {id: dsh-prompts, title: "dsh-superagent-prototype: 004 Prompts", resource: "https://github.com/deepseek-ai/dsh-superagent-prototype/tree/6337fc823ce20251c8de8085948165c81aaa701e/docs", file: 004-prompts.md, accessed: 2026-11-02, commit: 6337fc823ce20251c8de8085948165c81aaa701e}
---

# Scope of this note

The kit page already covers Mandate fields, accept modes, revalidation, recovery, the
reserved slot, "hand back asks beyond scope" and "never auto-merge as the agent".[^kit-dsh]
This note adds only what the Epic/Story/Task topic needs. All prototype citations are
pinned to its single commit `6337fc8` (2026-10-31).

# 1. Ticket vs Story mapping (new table rows)

The prototype has **no work hierarchy**. The main Session "only routes" and "makes no
technical decisions"; the Executor reads sources, judges scope, implements and
verifies.[^dsh-prompts] A Ticket is "a unit of authorized work" that only Eval creates.[^dsh-domain]

| dsh-superagent | Board level | Why |
| --- | --- | --- |
| — (no counterpart) | Epic | nothing above a Ticket; one Thread may carry several independent Tickets[^dsh-domain] |
| Ticket | one claimed **Story** | wider scope means a new Ticket[^dsh-domain]; a PR belongs to the Ticket when its branch's last path segment matches the Ticket's short name[^dsh-exec]; the Ticket is done when none of the PRs it opened remain open[^dsh-exec] |
| Executor's own steps | Tasks | internal to the Executor Session; not domain objects[^dsh-domain] |

Proposed row: *Ticket ≈ a Story as claimed; the kit keeps Epic and Task, which the
prototype does not model.*

# 2. What a Mandate freezes from a Story (refines an existing row)

The prototype's Mandate holds "the Policy version, the scope, the strength, the matched
rules, the sender's identity" and is **immutable**; only accept, a person's stop and failed
revalidation change it.[^dsh-domain][^dsh-auth] Scope behaviour is prompt text: the team's
"Ticket scope" section says "when a Ticket goes on and when it stops with a draft".[^dsh-prompts]
The prototype also "stops by impact, not by effort": a change that needs a design decision
stops with a question.[^dsh-phil]

The kit already says "scope is fixed to the item as claimed".[^kit-claims] Proposed
addition, saying *what* is fixed:

- At claim time, freeze from the Story: **acceptance criteria, out-of-scope list, verify
  step**, plus the body revision they came from.
- An edit to those parts after the claim is like a Policy change to a live Ticket: deliver
  it to the holder as a notice, do not silently widen; widening needs a new claim (the
  prototype "does not revoke Mandates" on change, but revalidates before resume).[^dsh-auth]
- A Story without those parts is not claimable (it maps to an empty Ticket scope).

# 3. Observe-mode rollout for proactive decomposition (new row)

The prototype's modes: `off`, `observe` (default; a positive assessment is recorded as
"would accept" and nothing is accepted), `auto`; "Start in `observe` and switch to `auto`
after reviewing the recorded Decisions"; a proactive accept requires at least one matching
rule, and each assessment judges every enabled rule exactly once.[^dsh-auth] The kit applies
this to lanes. Proposed: apply it also to **an agent splitting an Epic into Stories or
proposing follow-up Stories**.

| Mode | Agent does | Person does |
| --- | --- | --- |
| `observe` | posts the would-create list on the Epic (titles, criteria, order); creates nothing | reads, edits, creates or approves |
| `auto` | creates the Stories as `agent-proposed` sub-issues under a written rule | promotes with `agent-ready` |
| never | adds `agent-ready` itself | — |

Gate it like the prototype: one written rule per kind of proactive decomposition, and
record which rule matched on each created Story (the Mandate's "matched rules").[^dsh-auth]

# Corrections to the first sweep

- The prototype's **Gate / admission table** decides *who* may originate work and with what
  strength;[^dsh-auth] it is not a Definition of Ready (whether an item is clear enough). Map
  DoR elsewhere.
- "Human approval maps strongly to confirm once": confirm-once is an acknowledgement before
  substantial work, not an approval; the person is not asked to say yes.[^dsh-prompts]

[^kit-dsh]: Kit reference page on dsh-superagent.
[^kit-claims]: Kit model page, Claims and leases.
[^dsh-phil]: dsh-superagent 000 Philosophy.
[^dsh-domain]: dsh-superagent 001 Domain model, Concepts.
[^dsh-auth]: dsh-superagent 002 Authorization, accept mode, Policy version, resume.
[^dsh-exec]: dsh-superagent 003 Execution, Preparing a Ticket directory and Pull requests.
[^dsh-prompts]: dsh-superagent 004 Prompts, What a team writes and principles.
