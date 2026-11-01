---
type: Reference
title: Open Knowledge Format specification
description: Google Cloud's open format for knowledge as markdown files with YAML frontmatter; the kit pins version 0.2.
resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
tags: [okf, specification]
status: stable
generated: { by: claude-code/cloud, at: 2026-11-01T04:00:00Z }
---

# What it is

OKF represents knowledge as a directory of markdown files, each with YAML frontmatter
that requires only `type`. `index.md` and `log.md` are reserved. Version 0.2 adds
provenance (`sources` with footnotes), trust (`generated`, `verified`), lifecycle
(`status`, `stale_after`) and attested computations.

# In the kit

The pinned copy is `okf/SPEC.md`; the commit is in `okf/PIN.json`. The older copy
under `knowledge-catalog/okf` upstream is a frozen snapshot and is not used.
