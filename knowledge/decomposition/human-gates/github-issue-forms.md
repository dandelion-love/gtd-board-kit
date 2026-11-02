---
type: Reference
title: GitHub issue forms as a readiness gate
description: Issue forms structure what a new item must say, and can add labels and projects; their required fields are enforced only in public repositories.
tags: [github, issue-forms, definition-of-ready, conventional]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T12:00:00Z }
sources:
  - {id: gh-forms, title: "GitHub Docs: Syntax for issue forms", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms", accessed: 2026-11-02}
  - {id: gh-form-schema, title: "GitHub Docs: Syntax for GitHub's form schema", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema", accessed: 2026-11-02}
---

# What it does

- Defines inputs, validations, default assignees and default labels.[^gh-forms]
- Can add the new issue to projects; the person opening it needs write on those
  projects.[^gh-forms]
- Not for PRs: "Issue forms are not supported for pull requests."[^gh-forms]
- `required: true` "Prevents form submission until element is completed. Only for public
  repositories."[^gh-form-schema]

# As a gate

It is a **shape** gate, not an approval: it makes a Story arrive with acceptance criteria,
out-of-scope and a verify step. It does not say anyone agreed to build it.

| Repo | Strength |
| --- | --- |
| public | web form refuses submit until required fields are filled[^gh-form-schema] |
| private | required is not enforced[^gh-form-schema]; the form is a template |
| any, via API | agents usually create issues through the API; the form is not in that path |

So for agent-created Stories the readiness check must be done by the agent or a check
that reads the body. The form helps humans write items agents can pick up.

# Caveats

- The docs do not say whether API-created issues are validated; the table assumes not.

[^gh-forms]: GitHub Docs, Syntax for issue forms.
[^gh-form-schema]: GitHub Docs, form schema, validations.
