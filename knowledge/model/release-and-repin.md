---
type: Pattern
title: Release and repin
description: How a slice that changes the kit and the server ships in a fixed order, stays compatible with workers on the old kit, is checked live, can be rolled back, and rides a release train.
tags: [release, versioning, compatibility]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-21T20:00:00Z }
---

# Rule

Workers use the kit and the server while new work is built, so every slice says when it
ships, what deploy it needs, which repos repin, and how a worker still on the old kit
keeps working. An epic carries this in its `## Release` table (see
`skills/board-decompose/templates.md`); the rules below are stated once, here.

A **repin** is a change in a work repo that moves its kit pin to a newer kit commit.

# Sequence

1. **Kit first, no repin.** Merge the kit change with a version bump. Use a merge commit,
   not a squash, when a repin will pin that commit.
2. **Server next.** Merge the server change. It accepts both the old and the new call.
3. **Deploy.** The server's owner deploys. An agent does not run it.
4. **Live check.** Run the standard live check below on the live server. If it fails, roll
   back and stop.
5. **Repin last,** one repo at a time in the order the owner set. Kit skills tell workers
   what to do, so they must not name an argument the server does not accept yet.

# Expand, then contract

- **Expand.** A slice adds fields and tools in one release and never removes, renames or
  tightens what a worker on the old kit uses. An old field stays as an alias, a new part
  is optional, and a missing part gets a neutral value, not a refusal.
- **Contract.** Anything removed or tightened waits for a later release, after every
  worker has repinned.
- **Breaking?** A slice that cannot be additive says so in the table's `Breaking` column
  and needs the owner's go before its deploy.
- A new refusal that could hide existing items or block existing callers ships in watch
  mode first (record what it would do, change nothing) and enforces only after the owner
  reviewed the record.

# Standard live check

On a sandbox item, never a real one, after each deploy. All four parts pass:

1. `whoami` shows the expected spec version.
2. A claim, renew and release round trip, with old arguments only.
3. The slice's new field or tool, used once.
4. One old-client call the slice could have broken, still succeeding.

Name the check in the story's evidence.

# Rollback

Send server traffic back to the previous revision and keep one spare revision until the
next release passes its live check. If a repin already merged, repin back to the previous
kit commit. Config and secret changes (a new setting or credential on the server) are the
owner's step, listed per slice with a safe default; the slice must work with the setting
absent.

# Certification

When a slice changes the spec version, the conformance run at that version comes before
the claim. The owner approves any runner join; an agent never approves its own.

# Release trains

Budget is limited, so slices ship in trains: one kit release, one deploy and one repin
change per repo per train, at most one train a week unless the owner says otherwise. Merge
trains where they can be merged. The plan lists which stories ride which train, and the
change that defines this process merges before the first train.

# Review

A reviewer checks the epic's `## Release` section. It passes when it holds either `None.`
(nothing ships) or a table whose header is exactly `Slice | Kit change | Server change |
Config or secret | Breaking | Live check`, in that order, with a filled row for each story
that changes the kit or the server. A missing heading, a table with other or reordered
columns, a row left empty or still holding the template's placeholder comments, or a
change with no row is reported as missing or malformed. For an existing epic with no
Release section, the fix is to append the section as a draft marked `_Draft by an agent;
edit freely._`, keeping the person's text, as `board-decompose` does for any missing
section.

# Why

Agents and servers move on different clocks (see
[server version and levels](server-version.md)). An order that puts the server's
acceptance before any repin, and a check that uses the old call as well as the new, keep
live workers working while the contract grows.
