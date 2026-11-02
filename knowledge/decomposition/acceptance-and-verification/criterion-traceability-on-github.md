---
type: Practice
title: Criterion traceability on GitHub
description: A light requirement-to-test matrix built from what GitHub already has, linking each acceptance criterion to the check or evidence that proves it.
tags: [traceability, github, verification]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:00:00Z }
sources:
  - { id: gotel94, title: "Gotel and Finkelstein, An analysis of the requirements traceability problem, ICRE 1994", resource: "Gotel O., Finkelstein A., Proc. 1st Int. Conf. on Requirements Engineering, IEEE, 1994, pp. 94-101 (UCL Discovery record)", url: "https://discovery.ucl.ac.uk/", accessed: 2026-11-02 }
  - { id: gh-tasklists, title: "GitHub Docs, About tasklists", resource: "https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-tasklists", url: "https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-tasklists", accessed: 2026-11-02 }
  - { id: gh-protected, title: "GitHub Docs, About protected branches", resource: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", url: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", accessed: 2026-11-02 }
  - { id: gh-link, title: "GitHub Docs, Linking a pull request to an issue", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue", url: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue", accessed: 2026-11-02 }
  - { id: gh-prtemplate, title: "GitHub Docs, Creating a pull request template", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository", url: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository", accessed: 2026-11-02 }
---

# Why trace

Gotel and Finkelstein (1994) framed traceability as following a requirement's life, and
split it into pre-specification (where the requirement came from) and post-specification
(what implements and checks it). They reported most traceability problems sit on the
pre-specification side.[^gotel94] For agent work both matter: the issue records why,
the PR records how it was proved.

# The heavy version

A requirements traceability matrix: one row per requirement, columns for design, code,
test, result. Common in regulated work. Too heavy for a solo board.

# The light version with GitHub parts

| Need | GitHub part | Notes |
| --- | --- | --- |
| Criteria list with IDs | Markdown checkboxes in the issue, each prefixed `AC1`, `AC2` | Tasklist **blocks** are retired; plain checkboxes remain; sub-issues replace blocks[^gh-tasklists] |
| Issue to PR link | `Closes #n` in the PR body | works only when the PR targets the default branch; closes on merge[^gh-link] |
| Criterion to evidence | A PR body section: one row per AC with the check name, test id, command output or screenshot | a PR template puts the section in every PR; it must be on the default branch[^gh-prtemplate] |
| Machine gate | Required status checks | must be `successful`, `skipped` or `neutral` to merge[^gh-protected] |
| Human gate | Required review | a "Request changes" review blocks merge[^gh-protected] |

# Rules that keep it light

- Number criteria in the issue; never renumber after work starts.
- Test names or comments carry the AC id (`test_ac2_rejects_empty_title`), so a grep
  rebuilds the matrix.
- Every AC row in the PR names **one** kind of evidence: `test`, `check`, `command`,
  `screenshot`, or `review` (a person must look).
- An AC with no evidence row is a gap, and the PR is not ready.

# Caveats

- A required check that reports `skipped` satisfies the rule.[^gh-protected] A job that
  skips itself (for example on a path filter) can pass the gate without running. Check
  the gate's job really ran.
- Closing keywords do nothing on non-default-branch PRs.[^gh-link]
- No source here measures whether light traceability improves agent PR quality; this is
  reasoned, not proven.

# Related

- [Criterion-to-evidence chain](criterion-to-evidence-chain.md)
- [Definition of Done for agent PRs](definition-of-done-for-agent-prs.md)
