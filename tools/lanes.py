#!/usr/bin/env python3
"""lanes.py: read the standing lanes and workflow grants in a repo's .gtd/BOARD.local.md.

  python3 .gtd/kit/tools/lanes.py resume [FILE]   list lanes to re-schedule, with the pointer prompt
  python3 .gtd/kit/tools/lanes.py check  [FILE]   lint lanes and workflow grants; exit 1 on a problem

Without FILE, `resume` reads .gtd/BOARD.local.md from the default branch (origin/HEAD),
because only what a person merged counts, and falls back to the working copy with a
warning. `check` lints the working copy, so a draft is checked before it is merged.
Safe as a SessionStart hook: `resume` never fails the session. Standard library only.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

LOCAL = ".gtd/BOARD.local.md"
LANE_KEYS = ("asked_by", "basis", "grant", "policy", "switch", "item", "every", "lease")
SWITCHES = ("auto", "observe", "hold", "off")
GRANT_KEYS = ("paths", "granted_by", "date", "link")
PROMPT = "Run lane {name} as .gtd/BOARD.local.md defines it."


def read_local(path: str | None) -> tuple[str, str]:
    if path:
        return Path(path).read_text(encoding="utf-8"), path
    try:
        text = subprocess.run(["git", "show", f"origin/HEAD:{LOCAL}"], capture_output=True,
                              text=True, check=True).stdout
        return text, f"origin/HEAD:{LOCAL}"
    except (OSError, subprocess.CalledProcessError):
        p = Path(LOCAL)
        if not p.exists():
            return "", LOCAL
        print(f"NOTE could not read {LOCAL} from origin/HEAD; using the working copy, "
              "which counts only once it is merged", file=sys.stderr)
        return p.read_text(encoding="utf-8"), LOCAL


def section(text: str, title: str) -> str:
    m = re.search(rf"^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def blocks(body: str, kind: str) -> list[dict]:
    """Parse '### <kind>: <name>' blocks of '- key: value' lines; list keys collect '  - x'."""
    out: list[dict] = []
    for m in re.finditer(rf"^### {kind}:\s*(.+?)\s*$(.*?)(?=^### |\Z)", body, re.M | re.S):
        item: dict = {"name": m.group(1).strip("` ")}
        key = None
        for line in m.group(2).splitlines():
            if re.match(r"^\s*<!--", line) or not line.strip():
                continue
            top = re.match(r"^- (\w+):\s*(.*)$", line)
            sub = re.match(r"^\s{2,}- (.+)$", line)
            if top:
                key, val = top.group(1), re.sub(r"\s*<!--.*?-->\s*", "", top.group(2)).strip()
                item[key] = val if val else []
            elif sub and key is not None:
                val = re.sub(r"\s*<!--.*?-->\s*", "", sub.group(1)).strip()
                if not isinstance(item.get(key), list):
                    item[key] = [item[key]] if item.get(key) else []
                if val:
                    item[key].append(val)
        out.append(item)
    return out


def check(text: str) -> list[str]:
    problems = []
    for lane in blocks(section(text, "Standing lanes"), "lane"):
        n = lane["name"]
        for k in LANE_KEYS + ("may", "never"):
            if not lane.get(k):
                problems.append(f"lane {n}: missing {k}")
        if lane.get("switch") and lane["switch"] not in SWITCHES:
            problems.append(f"lane {n}: switch must be one of {', '.join(SWITCHES)}")
        if lane.get("may") and not isinstance(lane["may"], list):
            problems.append(f"lane {n}: may must be a list")
        if lane.get("never") and not isinstance(lane["never"], list):
            problems.append(f"lane {n}: never must be a list")
    for grant in blocks(section(text, "Workflow grants"), "grant"):
        n = grant["name"]
        for k in GRANT_KEYS:
            if not grant.get(k):
                problems.append(f"workflow grant {n}: missing {k}")
        paths = grant.get("paths") or []
        for p in paths if isinstance(paths, list) else [paths]:
            if not p.strip("`").startswith(".github/workflows/"):
                problems.append(f"workflow grant {n}: path {p} is not under .github/workflows/")
            if p.strip("`") in (".github/workflows/**", ".github/workflows/*", ".github/workflows/"):
                problems.append(f"workflow grant {n}: name the workflows; a whole-folder grant is refused")
    return problems


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("resume", "check"):
        print(__doc__)
        return 2
    path = sys.argv[2] if len(sys.argv) > 2 else (LOCAL if sys.argv[1] == "check" else None)
    if path and not Path(path).exists():
        print(f"ok: no {path}")
        return 0
    text, where = read_local(path)
    if sys.argv[1] == "check":
        problems = check(text)
        for p in problems:
            print(f"FAIL {p}")
        if not problems:
            print(f"ok: {where}")
        return 1 if problems else 0
    lanes = blocks(section(text, "Standing lanes"), "lane")
    if not lanes:
        return 0
    print(f"Standing lanes in {where} (board-lane skill, Resume):")
    for lane in lanes:
        switch = lane.get("switch", "?")
        if switch in ("auto", "observe", "hold"):
            print(f"- {lane['name']}: {switch}, every {lane.get('every') or '?'}, item "
                  f"{lane.get('item') or '?'}{' (renew-only ticks)' if switch == 'hold' else ''}. Schedule prompt: {PROMPT.format(name=lane['name'])}")
        else:
            print(f"- {lane['name']}: {switch}; do not schedule")
    for p in check(text):
        print(f"NOTE {p}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # a hook must never break a session
        print(f"NOTE lanes.py: {exc}", file=sys.stderr)
        sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] == "resume" else 1)
