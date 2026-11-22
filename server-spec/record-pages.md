# 15. Record pages

A register can keep each item (an experiment, a listening test, a finding) as one Markdown
page instead of as lines in one shared JSONL file. The page is the record: an OKF concept
([okf/SPEC.md](../okf/SPEC.md)) that only ever grows. This section fixes the page format,
the addendum-only rule, how two branches' additions merge, and what a server that reads or
writes a register must do when its records are pages. The reference implementation is
[conformance/record_pages.py](../conformance/record_pages.py); checks RP1 to RP3 run its
golden cases.

Why pages: one shared append-only file conflicts whenever two branches append to it, and a
file of long one-line JSON records is unreadable in a forge's web view. One page per item
gives each item its own history, its own diff and a readable view, and keeps the records
themselves byte for byte.

## The page

```
---
type: "Experiment"
id: "EXP-1"
title: "..."
format: okf-register-v1
opened: "2026-01-02 10:00:00"
---

# EXP-1 — ...

_Addendum-only record. ..._

## register · 2026-01-02 10:00:00

**Hypothesis.** ...

<details><summary>Record · sha256 0123456789abcdef</summary>

(a fenced block opened by ```json record, holding the record line, then a closing fence)

</details>
```

- **The file** is in one folder per register, in one of two layouts the repository picks
  per register: **flat**, `<folder>/<id>.md`, or **item folders**, `<folder>/<id>/README.md`,
  so the item's other files (results, keys, cards) sit beside its page and a forge shows the
  page when the folder is opened. Only the page is a record; the other files in an item
  folder are not under this rule. The id is the item's id: a record's `id`, or a link
  record's `from` when it has no `id`, and it is the file's stem (flat) or the folder's name
  (item folders). Ids are 1 to 121 characters of letters, digits, `.`, `_` and `-`, starting
  with a letter or digit.
- **The front matter** is written once, from the item's first record, and never changes:
  `type` (the register's kind), `id`, `title` (the first record's `title`, else its
  `statement`, else the id; whitespace collapsed, at most 200 characters), `format`
  (`okf-register-v1`) and `opened` (the first record's `t`). Nothing that changes, such as a
  status, belongs in it.
- **An entry** is one record: a level-two heading (the record's `event`, its `t` or
  `no time`, and its `by` when present), the readable text written from the record, and the
  record line inside `<details>`, in a fence whose info string is `json record`.
- **The record line is the record**, byte for byte as the register line it replaces, so its
  sha256 is the line hash anything already cites. The readable text is a view of it.
- **The readable text** is written by the reference renderer and nothing else. Version 1
  summaries clip long values and remain valid byte for byte. A version 2 entry is used for
  an experiment item (an id beginning `EXP-`); other item kinds continue to use version 1.
  Its heading is followed by `<!-- okf-entry-v2 -->` and the record's fields are written in
  labelled, Markdown-safe prose without clipping, including nested method and qualification
  values. Its details title and visible record digest carry the full SHA-256 of the exact
  UTF-8 record line. The fenced line remains unchanged. The page front-matter format stays
  `okf-register-v1`; the marker versions entries, not the page or record schema.
- For an experiment registration with a `spec` object, version 2 computes a full rule digest
  from the eight fields `hypothesis`, `arms`, `metric`, `decision_rule`, `falsified_by`,
  `void_if`, `cannot_answer` and `n_planned`. Include absent fields as JSON null, serialize
  the object with UTF-8, `ensure_ascii=False` and sorted keys using the JSON encoder's normal
  separators, then SHA-256 the bytes. Mark it verified against the stored pin only when a
  lowercase 16-character prefix or 64-character full digest matches. Otherwise state that the
  computed digest is unverified; label a valid stored prefix, valid full digest, or invalid
  stored format accurately, and never invent a missing suffix. Records without an experiment registration spec have no computed
  rule digest. Values are escaped as Markdown-safe text (including raw HTML and lines that
  open a heading, fence or table), but not truncated.
- A writer MAY pass a map from id prefix to a link target, so that a link's target and a
  finding's citations render as relative links to their pages. A target is the page's path relative to
  the linking page's own folder, with `{id}` standing for the id (`../{id}/README.md` from one
  item folder to another, `../../listening/{id}.md` from an item folder to a flat register).
  The map is the repository's, one per register since the relative paths differ, and a
  checker uses the same one.

## The addendum-only rule

For each page, between a base revision and a head:

| Refusal | When |
| --- | --- |
| `edits-existing-content` | the base page is not a byte prefix of the head page |
| `added-text-is-not-rendered-entries` | what was added is not exactly whole entries rendered from their own records |
| `page-is-not-rendered` | a page new since the base is not exactly the render of its records |
| `page-removed` | a page at the base is gone at the head (deleted or renamed) |
| `record-for-another-item:<id>` | an entry's record belongs to another item |
| `front-matter-id-is-not-the-file-name` | the front matter's `id` is not the file's stem, or its item folder's name |
| `conflict-markers` | the page holds a line opening with `<<<<<<< ` or `>>>>>>> ` |
| `bad-record-json` | a record line is not JSON |
| `conflicting-record-presentation` | an appended entry repeats an existing record with different valid rendered bytes |

A change the rule refuses is never written by a tool. A correction is a new record (a
reading, a retire), never an edit. A repository runs the rule in its writers and in CI
against the pull request's base.

## Merging

Two branches that each append to the same page are merged as: the base, then the first
side's new entries, then the second side's entries the first side lacks. Preserve each
incoming entry's exact bytes, including its version. Identical record and entry bytes are
kept once; if the same record is presented with different valid entry bytes in the base or
between branches, refuse the merge rather than silently discard either presentation. A
single appended tail that presents the same record in two different versions is invalid.
The merge is refused when either side breaks the rule against the base. A line-based union merge MUST
NOT be used: entries share identical lines (the fences, the closing tag, blank lines), and a
union merge interleaves them while reporting success. A repository wires this merge as a git
merge driver, and where the driver is not installed git falls back to an ordinary conflict.

## A server and record pages

A profile source that reads a register MAY name a page folder instead of a file
([profiles](repo-context-and-profiles.md#profiles)), as
`pages: {folder, layout, type, links}`: the folder, `flat` or `item-folder`, the front
matter's `type`, and the link map its pages are rendered with. Then a server:

- **reads** a register as the record lines of all its pages: across pages in time order of
  each record's `t`, each page's own order kept. Every fold here (claims excepted, which are
  comments, not registers) depends only on the order within one item, and a link and its
  unlink are on the same page, the `from` item's ([writing a link](typed-links.md#writing-a-link));
- **writes** a record by appending its rendered entry to its item's page, or by creating the
  page from the record when the item has none. It refuses, before writing, a record whose
  page would fail the rule;
- **links** to an item's page where it links to the register today (an issue body, a tool
  result).

A server that writes pages must produce the reference renderer's bytes exactly, or the
repository's own check refuses its entries; RP1 and RP3 fix those bytes.
