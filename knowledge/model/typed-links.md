---
type: Pattern
title: Typed links between items
description: Items and register records link with a fixed set of kinds; only depends-on becomes a native GitHub link, every other kind is a Related line on both ends, and the same fold drives the issues and the OKF graph so the two cannot drift.
tags: [links, registers, knowledge-graph, blocked-by, sub-issues]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-04T16:30:00Z }
---

# Rule

When one item's meaning depends on another's, record the relation as a **typed link**, a
line in the register that holds the item, and let the sync and the graph render show it.
Never hand-write the relation into an issue body or a page: the next sync rewrites the
body, and a page edited by hand drifts from the record.

The kinds are fixed ([server spec](../../server-spec/typed-links.md#kinds)), each with
the name its far end reads:

| Kind | Far end reads | Use it when |
| --- | --- | --- |
| `depends-on` | `blocks` | the item cannot start or end until the other has |
| `follows-up` | `followed-up-by` | the item was designed from the other's result |
| `references` | `referenced-by` | the item uses the other as its comparison arm or baseline |
| `evaluates` | `evaluated-by` | the item (a test) judges the other's output |
| `rests-on` | `supports` | the item (a finding) rests on the other's result |
| `refines` | `refined-by` | the item narrows or qualifies the other's reading |
| `contradicts` | `contradicts` | the two cannot both be right |
| `corroborates` | `corroborates` | independent evidence pointing the same way |
| `supersedes` | `superseded-by` | the item replaces the other as the one to use |
| `reuses-material` | `material-reused-by` | the two used the same material, so they compare |
| `shares-listener` | `shares-listener` | the same human judged both, so they are not independent |

# Why most kinds are text

GitHub has two native relations between issues: **parent and sub-issue**, and
**blocked-by**. Each carries behaviour: a parent rolls up its children's progress and the
[Kind rules](../../server-spec/repo-context-and-profiles.md#kinds) govern what it may hold;
a blocker keeps an item out of the ready queue
([ready check](../../server-spec/ready-check.md)). A relation that should not carry that
behaviour must not borrow it.

- **Parent stays the item's own parent**, never a link. A follow-up is not a part of what
  it followed; parenting it would roll it into the other's progress.
- **Only `depends-on` is blocked-by.** It is the one kind that says "not before". A
  `follows-up` link is written after the other ended, so as a blocker it would always be
  satisfied and say nothing.
- **Every other kind is a Related line** in the mirrored body, on both ends. The line
  carries an issue reference, so GitHub also shows a backlink on the far issue's timeline,
  but the inverse is written out in the body so a reader of either issue sees it without
  the timeline.

# The graph as OKF

The links a repo holds are a graph worth reading on its own: which results a finding rests
on, which experiments a follow-up chain grew from, which tests share one listener. A repo
may render it as an OKF bundle:

- an index page with a Mermaid flowchart of the linked items, one node per item, one edge
  per link, labelled with its kind, and a table of every item and its degree;
- one page per linked item, its frontmatter naming the item, its body listing the item's
  Related lines as relative links to the other items' pages and to the issue.

The render reads the same registers through the same fold as the sync. It is generated,
never edited, and its check mode re-renders in memory and refuses a difference, so a
register change without a re-render is caught in review the way a stale index is.

# Consequences

- A register gains a way to say why two records matter to each other, which a board can
  show and a person can walk.
- A wrong link is taken back with an `unlink` line, so the register stays append-only.
- A new relation needs a kit change first. Until then, write the nearest kind and say
  the rest in `why`.
