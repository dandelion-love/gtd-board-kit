#!/usr/bin/env python3
"""lanes.py: read the standing lanes and workflow grants in a repo's .gtd/BOARD.local.md.

  python3 .gtd/kit/tools/lanes.py resume [FILE]   list lanes to re-schedule, with the pointer prompt
  python3 .gtd/kit/tools/lanes.py check  [FILE]   lint lanes and workflow grants; exit 1 on a problem
  python3 .gtd/kit/tools/lanes.py check --merged [--covers PATH]
                                                  lint the default branch's copy only; with --covers,
                                                  exit 0 only if a merged grant names PATH

Without FILE, `resume` reads .gtd/BOARD.local.md from the default branch (origin/HEAD),
because only what a person merged counts, and falls back to the working copy with a
warning, and then schedules nothing. `check` lints the working copy, so a draft is
checked before it is merged; `check --merged` is the authorization check and never falls
back to the working copy.
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
BOARD_DOWN = ("continue", "hold")
GRANT_KEYS = ("paths", "granted_by", "date", "link")
PROMPT = "Run lane {name} as .gtd/BOARD.local.md defines it."


def read_merged() -> str | None:
    """The default branch's copy, or None if it can't be read. Says which commit it read,
    because a clone that hasn't fetched reads a stale default branch."""
    try:
        text = subprocess.run(["git", "show", f"origin/HEAD:{LOCAL}"], capture_output=True,
                              text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    try:
        info = subprocess.run(["git", "log", "-1", "--format=%h %cI", "origin/HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
        print(f"NOTE read origin/HEAD at {info}; run git fetch first if that looks old",
              file=sys.stderr)
    except (OSError, subprocess.CalledProcessError):
        pass
    return text


def read_local(path: str | None) -> tuple[str, str, bool]:
    """(text, where, merged). merged is False when the text is not the default branch's."""
    if path:
        return Path(path).read_text(encoding="utf-8"), path, False
    merged = read_merged()
    if merged is not None:
        return merged, f"origin/HEAD:{LOCAL}", True
    p = Path(LOCAL)
    return (p.read_text(encoding="utf-8") if p.exists() else ""), LOCAL, False


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
        if lane.get("on_board_down") and lane["on_board_down"] not in BOARD_DOWN:
            problems.append(f"lane {n}: on_board_down must be one of {', '.join(BOARD_DOWN)}")
        if lane.get("capacity") and not str(lane["capacity"]).isdigit():
            problems.append(f"lane {n}: capacity must be a whole number")
        if lane.get("capacity") and not lane.get("resource"):
            problems.append(f"lane {n}: capacity needs a resource")
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
    args = sys.argv[2:]
    if sys.argv[1] == "check" and "--merged" in args:
        text = read_merged()
        if text is None:
            print(f"FAIL cannot read {LOCAL} from origin/HEAD; nothing is granted")
            return 1
        covers = args[args.index("--covers") + 1] if "--covers" in args else None
        problems = check(text)
        for p in problems:
            print(f"FAIL {p}")
        if covers:
            named = [g["name"] for g in blocks(section(text, "Workflow grants"), "grant")
                     if covers in [p.strip("`") for p in (g.get("paths") or [])
                                   if isinstance(g.get("paths"), list)]]
            if not named:
                print(f"FAIL no merged workflow grant names {covers}")
                return 1
            print(f"ok: {covers} is covered by grant {', '.join(named)}")
        return 1 if problems else 0
    path = args[0] if args else (LOCAL if sys.argv[1] == "check" else None)
    if path and not Path(path).exists():
        print(f"ok: no {path}")
        return 0
    text, where, merged = read_local(path)
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
    if not merged and not path:
        print(f"NOTE could not read {LOCAL} from origin/HEAD, so no lane is scheduled: only "
              "what a person merged counts. Fetch the default branch and run resume again.")
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
