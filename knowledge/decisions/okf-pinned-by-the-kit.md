---
type: Decision
title: OKF is pinned by the kit
description: The kit carries the OKF specification at a pinned upstream commit, and repos that use the kit write their knowledge docs to that version.
tags: [okf, knowledge]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T04:00:00Z }
sources:
  - { id: okf-spec, resource: /references/okf-spec.md, title: Open Knowledge Format specification }
---

# Decision

- The kit copies the upstream OKF `SPEC.md` and its license unchanged into `okf/`, with
  the upstream commit and `okf_version` in `okf/PIN.json`.[^okf-spec]
- The kit's own knowledge (this bundle) follows that version, and `tests/check_kit.py`
  lints it with `tools/okf_lint.py --strict`.
- Repos that use the kit write knowledge docs to the same version, using the
  `okf-knowledge` skill, and get a newer OKF by moving their kit pin.

[^okf-spec]: Open Knowledge Format specification
