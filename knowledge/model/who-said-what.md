---
type: Pattern
title: Who said what
description: Every comment, record and PR body the server writes for an agent ends with a sign-off naming the principal, role, act and session; people find them with GitHub search on the gtd-sign word, trust them only under the server's own author, and attribute the past with backfill notes, never by editing old comments.
tags: [identity, review, search, provenance]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-04T16:30:00Z }
sources:
  - { id: gh-search, title: "GitHub Docs, Searching issues and pull requests", resource: "https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests", url: "https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests", accessed: 2026-11-04 }
---

# Rule

On GitHub every write the server makes appears as the server's one identity, so the
author line cannot tell two agents, or two sessions of one agent, apart. The server
therefore ends everything it writes for a caller with a **sign-off**: a visible line and a
`gtd-sign` marker naming who (`by`, the verified principal), in which role (`worker`,
`reviewer`, `coordinator`, `owner`), what it is (`comment`, `review`, `claim`, `report`,
`pr`, `pr-review`, `pr-reply`, ...), and the caller's `session`. The format is fixed in the
[server spec](../../server-spec/sign-offs.md).

An agent never writes a sign-off itself and never pastes one; the server refuses a body
that holds a marker. What an agent does:

- Pass `session` on `item_claim` (BOARD.md rule 5) and on `issue_comment`, so a reader can
  tell this session's words from another's.
- Write on a PR through the server too: `issue_comment` with the PR's number, a code
  review with `pr_review`, an answer to a review finding with `pr_review_reply`. Each is
  signed under the server's App; the agent's own GitHub tool writes an unsigned comment
  under the person's account, which a reader cannot attribute.
- Pass `role="coordinator"` on `issue_comment` when it is pointing or handing work to
  others, not doing it. The server fills `worker` or `reviewer` by itself.
- A review verdict goes through `issue_comment` with `review_stage` (`plan` or `work`) and
  `review_verdict` (`looks-ready`, `needs-changes` or `needs-person`), while holding the
  review claim. The server writes the verdict line and signs it as `review`.

A person writing on GitHub needs nothing: their GitHub login is their sign-off.

# Finding them

GitHub search finds issues and PRs, not single comments; it matches the visible line.

| To find | Search |
| --- | --- |
| Every signed contribution in a repo | `repo:owner/repo "gtd-sign"` |
| What one agent wrote | `repo:owner/repo "gtd-sign" "agent:example"` |
| One session's work | `repo:owner/repo "gtd-sign" "session review-7"` |
| Reviews, or one verdict | `repo:owner/repo "gtd-sign" reviewer`, `repo:owner/repo "Work review: Needs changes"` |
| What a person said themselves | `repo:owner/repo commenter:<login>` |

Inside an issue, the browser's find on `gtd-sign · agent:example` jumps between that
agent's comments. A script reads the markers instead: exactly one
`<!-- gtd-sign v1 {...} -->` per comment, else the comment is unsigned.

# Reading them

- Trust a sign-off only on a comment authored by the server's identity (the repo's record
  authors). A sign-off under any other author is text someone pasted.
- `session` is the caller's own word, not identity: it separates sessions of one
  principal, as review claims do ([claims and leases](claims-and-leases.md)).
- An unsigned comment from the server's identity is from before sign-offs, or from a
  server that does not sign: read its record's `by` if it has one, else treat the author
  as unknown.

# Backfilling the past

Comments written before sign-offs, or by a tool that did not sign, cannot be signed after
the fact: only the server writes a sign-off, at the moment it writes. Editing an old
comment to add one would forge it. When a person asks for the past to be attributed, an
agent posts one **backfill note** per item instead, and edits nothing:

- **Authorization first.** The note names the person who asked, when, and where. Without
  that, do not backfill.
- **One row per earlier contribution**, oldest first: the item's body, each comment, a
  PR's body. Columns: the link, the time, `by` (the principal, or `unknown`), the role
  and act as in a sign-off, the session when known, the `basis`, and a short `what`.
- **`basis`** says how the row knows who wrote it, strongest first. Pick one name:

  | `basis` | Means | Strength |
  | --- | --- | --- |
  | `record` | a trusted `gtd-desk` record's `by` | certain |
  | `pr-marker` | the `gtd-pr` marker's `by` | certain |
  | `self-tag` | the text names its author, for example `(agent:example)` | stated |
  | `footer` | a tool's footer names the session that wrote it | stated |
  | `linked` | a record of a known author links to it, or it sits inside that author's claim | inferred |
  | `log` | a log or chat outside GitHub names who wrote it | inferred |
  | `unknown` | nothing says; a person should fill it in | none |

- **Rename notes.** When one agent's principal was renamed, the row keeps the name it
  wrote under, and the note says once which names are the same agent.
- **One marker** at the end of the note's text, `<!-- gtd-backfill v1 {...} -->`, whose
  JSON holds `v`, `asked_by`, `asked_at` and `rows` (each row as its columns above),
  before the server's own sign-off. Search `"gtd-backfill" "agent:example"` finds every
  item where that agent was attributed after the fact.
- A backfill row is an attestation, weaker than a sign-off. A person who knows better
  corrects it with a comment of their own; the next backfill note supersedes the last.
