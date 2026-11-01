---
type: Reference
title: DeepSeek's dsh-superagent prototype
description: An MIT-licensed research prototype of a proactive coding agent for one repository; the kit borrows its ideas on mandates, accept modes, recovery and attention, not its code.
resource: https://github.com/deepseek-ai/dsh-superagent-prototype
tags: [reference, agents, authorization]
status: stable
generated: { by: claude-code/cloud, at: 2026-11-01T06:30:00Z }
---

# What it is

A research prototype, published with DeepSeek's article *Exploring Super-agent Design*,
packaged for DeepSeek Harness. A router session judges incoming events; each accepted
piece of work (a Ticket) gets its own worker session and directory and answers where it
was asked, usually with a PR. Its own words: research code, not production-ready.

Its principle: **take as little human attention as possible, and give as much value as
possible.** It acts only when asked or when a written rule allows it, and speaks only
when someone must act or can use a result.

# What the kit takes from it

| dsh-superagent | In the kit |
| --- | --- |
| Every Ticket carries a Mandate: who asked, the basis, matched rules, policy version | A claim's `asked_by`, `basis`, `pointed_in`; a lane's `policy` |
| Accept modes `off` / `observe` / `auto`; start in `observe` and widen after reading what it would have done | Lane switches `off` / `observe` / `auto`, plus `hold`; new lanes start at `observe` |
| A Policy change is delivered to live work, and an ended Ticket is revalidated before it resumes | Every lane tick re-reads the lane from the default branch first |
| Waiting conditions belong to Sources that check again; the judge never waits | A tick never waits on a job; a later tick checks it |
| A person's pause holds until a person lifts it | `hold` and `needs:*` on the lane item; agents never lift them |
| After a restart: check your directory, git history and GitHub before repeating any outside action | The recovery step of every tick |
| Decide, store, then act; retry stored work with backoff | Report the intent on the item before a long or outside action |
| An hourly check that runs **outside** the agent and survives its crash | The lane item's lease is the heartbeat anyone can see lapse |
| Background work has a time limit, then is killed and reported as waiting | Long jobs need a completion marker; exit 0 alone proves nothing |
| One reserved worker slot so a person's follow-up is never starved | A person's direct ask comes before a lane tick |
| Hand back asks beyond the Ticket's scope; never widen it | Scope is fixed; new work is captured as `agent-proposed` |
| Auto-merge never as the agent's own account | Agents never merge |

# What the kit does not take

- One long-lived process per repository with a local store as the record: the kit's
  record is the board and the issues, reached through the gtd MCP server.
- A dedicated agent user account reading notifications: the kit's intake is people and
  coordinators pointing agents, and lanes.
- Workers with full access as the operator's OS user.
