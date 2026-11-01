---
type: Decision
title: Work items live on the board; a local file is only a cache
description: Epics, stories, tasks and bugs are issues on the repo's board; a markdown copy of one is a local cache that is never committed and never trusted over the issue.
tags: [contract, work-items]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T19:30:00Z }
---

# Decision

- **The issue is the record.** For a work item (epic, story, task, bug, milestone), the
  issue's title, body, Issue Type, parent, dependencies and labels, and its board item's
  fields, are authoritative. Edit the item there.
- **A local markdown copy is a cache.** An agent may write one to read offline or to
  draft, but it is gitignored, never committed, safe to delete, and regenerated from
  the issue. When the two differ, the issue wins.
- **Nothing syncs a cache back.** A tool that mirrors files to the board reads only
  files the repository tracks, so a local cache can never overwrite an issue.
- **Body too long for one issue?** Put the head in the issue and the rest in comments
  on it, never in a link to an untracked file.
- Records that are not work items, such as an append-only experiment log, may still be
  files that mirror to the board; the [per-repo layer](/decisions/per-repo-layer.md)
  says which.

# Consequences

- Moving a repo whose backlog was files: untrack the files and ignore their paths first,
  then copy each open item's body into its issue, then stop the file sync for them. In
  that order a running sync finds no files and cannot undo the copy.
- A file's history in git stops at the move; the issue's edit history and timeline
  carry it on.

See [the kit is the interface](/decisions/kit-is-the-interface.md).
