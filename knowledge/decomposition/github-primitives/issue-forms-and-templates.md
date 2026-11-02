---
type: Reference
title: Issue forms, templates and PR linking on GitHub
description: How YAML issue forms, Markdown templates, PR templates, closing keywords and the Development sidebar can shape Epic, Story and Task bodies, and where they stop enforcing.
tags: [github, issue-forms, templates, pull-requests, linking, epic-story-task]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:15:00Z }
sources:
  - {id: docs-form-syntax, title: "Syntax for issue forms (GitHub Docs)", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms", accessed: 2026-11-02}
  - {id: docs-form-schema, title: "Syntax for GitHub's form schema (GitHub Docs)", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema", accessed: 2026-11-02}
  - {id: docs-config, title: "Configuring issue templates for your repository (GitHub Docs)", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository", accessed: 2026-11-02}
  - {id: docs-about-tpl, title: "About issue and pull request templates (GitHub Docs)", resource: "https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates", accessed: 2026-11-02}
  - {id: docs-link-pr, title: "Linking a pull request to an issue (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue", accessed: 2026-11-02}
  - {id: docs-fields-use, title: "Adding and managing issue fields (GitHub Docs)", resource: "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-and-managing-issue-fields", accessed: 2026-11-02}
  - {id: cl-2026-03-05, title: "Hierarchy view improvements and file uploads in issue forms, changelog 2026-03-05", resource: "https://github.blog/changelog/", changelog_entry: "2026-03-05-hierarchy-view-improvements-and-file-uploads-in-issue-forms", accessed: 2026-11-02}
  - {id: cl-2026-04-09, title: "Release information in issue sidebar and project defaults, changelog 2026-04-09", resource: "https://github.blog/changelog/", changelog_entry: "2026-04-09-release-info-in-issue-sidebar-and-project-defaults", accessed: 2026-11-02}
  - {id: cl-2026-10-28, title: "Issue artifacts are now in public preview, changelog 2026-10-28", resource: "https://github.blog/changelog/", changelog_entry: "2026-10-28-issue-artifacts-are-now-in-public-preview", accessed: 2026-11-02}
---

# What it is

Templates shape the **body** of a new issue or PR in the web UI. They are the native
carrier for the sections an Epic or Story needs (goal, scope, out of scope, acceptance
criteria). They are a UI aid, not a validator.

# Issue forms (YAML)

File: `.github/ISSUE_TEMPLATE/<name>.yml` on the default branch[^docs-form-syntax][^docs-about-tpl].

| Top-level key | Use for E/S/T | Note |
| --- | --- | --- |
| `name`, `description`, `body` | required | name unique across templates[^docs-form-syntax] |
| `type` | preset Epic / Story / Task | org issue type[^docs-form-syntax] |
| `labels`, `assignees` | preset | labels not in the repo are skipped[^docs-form-syntax] |
| `projects` | add to a board (`OWNER/NUMBER`) | opener needs write on the project[^docs-form-syntax] |
| `title` | e.g. `"[Story] "` prefix | prefilled, editable[^docs-form-syntax] |

Body elements: `markdown`, `textarea`, `input`, `dropdown`, `checkboxes`, `upload`
(upload added 2026-03-05)[^docs-form-schema][^cl-2026-03-05].
Validations: `required` on all inputs; `min_length` on `textarea` and `input`; per-option
`required` on checkboxes[^docs-form-schema].

Hard limits on enforcement:

- `required` is enforced **"Only for public repositories"**[^docs-form-schema].
- Issue forms are still marked **public preview**[^docs-form-syntax].
- Forms cannot set [issue fields](issue-fields.md)[^docs-fields-use].
- Forms are not supported for PRs[^docs-form-syntax].
- No doc says the API applies a form. An agent creating issues by API gets no form
  checks; the body is free text.
- The submitted body is plain Markdown, one `###` heading per element (common observed
  behaviour, not stated in the pages read). A kit can parse it, but GitHub keeps no
  structured copy.

# Markdown templates and the chooser

- Markdown templates (`.md`) can preset `title`, `labels`, `type`, `assignees` in
  frontmatter[^docs-config].
- `config.yml`: `blank_issues_enabled: false` hides blank issues from Read and Triage users
  only; Write and above still see "Maintainers only"[^docs-config]. Agents usually have write.
- Org-wide defaults can come from a default community health file[^docs-about-tpl].

# PR templates

- `pull_request_template.md` in the repo root, `docs/` or `.github/` on the default
  branch[^docs-about-tpl].
- A template is text only; GitHub does not check it was filled in.

# Linking a PR to its Task or Story

| Method | Rule | Source |
| --- | --- | --- |
| Closing keyword | `close(s/d)`, `fix(es/ed)`, `resolve(s/d)` in PR body or commit message, case-insensitive | [^docs-link-pr] |
| Default branch only | keywords are ignored when the PR targets another branch | [^docs-link-pr] |
| Cross-repo | `Fixes owner/repo#N` | [^docs-link-pr] |
| Development sidebar | up to 10 issues per PR by hand; needs write | [^docs-link-pr] |
| Commit-message keyword | closes the issue on merge, but the PR is not listed as linked | [^docs-link-pr] |
| Release info | the issue's Development section shows the first release with the linked PR (2026-04-09) | [^cl-2026-04-09] |

- Closing a Task by keyword does **not** close its Story or Epic. Parents are closed by
  hand or by the kit.
- Stacked or non-default-base PRs do not auto-close. A kit that merges into a feature
  branch must close issues itself.

# Related: issue artifacts (preview)

Since 2026-10-28, Markdown, link or HTML **artifacts** can be attached to an issue, with
version history, managed by `gh issue artifact` or the web UI; public preview, no REST or
GraphQL named[^cl-2026-10-28]. A possible home for an Epic's plan or a Story's design notes,
outside the body.

[^docs-form-syntax]: Syntax for issue forms, GitHub Docs.
[^docs-form-schema]: Syntax for GitHub's form schema, GitHub Docs.
[^docs-config]: Configuring issue templates, GitHub Docs.
[^docs-about-tpl]: About issue and pull request templates, GitHub Docs.
[^docs-link-pr]: Linking a pull request to an issue, GitHub Docs.
[^docs-fields-use]: Adding and managing issue fields, GitHub Docs.
[^cl-2026-03-05]: File uploads in issue forms, 2026-03-05.
[^cl-2026-04-09]: Release info in issue sidebar, 2026-04-09.
[^cl-2026-10-28]: Issue artifacts public preview, 2026-10-28.
