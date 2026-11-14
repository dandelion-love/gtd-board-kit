#!/usr/bin/env python3
"""lanes.py: read the standing lanes, workflow grants and merge grants in a repo's .gtd/BOARD.local.md.

  python3 .gtd/kit/tools/lanes.py resume [FILE]   list lanes to re-schedule, with the pointer prompt
  python3 .gtd/kit/tools/lanes.py check  [FILE]   lint lanes and workflow grants; exit 1 on a problem
  python3 .gtd/kit/tools/lanes.py check --merged [--covers PATH]
                                                  lint the default branch's copy only; with --covers,
                                                  exit 0 only if a merged grant names PATH
  python3 .gtd/kit/tools/lanes.py check --merged --merge PATH [PATH ...]
                                                  exit 0 only if ONE merged merge grant names
                                                  every PATH (the PR's changed files, from
                                                  git diff --name-only --no-renames)
  python3 .gtd/kit/tools/lanes.py check --merged [--base REF] --head REF --merge PATH [PATH ...]
                                                  the same, and a PATH that is a record page of a
                                                  register the grant names is covered when the PR
                                                  (REF against BASE, default origin/HEAD) only
                                                  appends valid records to it

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
MERGE_KEYS = ("paths", "granted_by", "date", "link")
# A merge grant can never cover these: they hold the rules and the grants themselves.
NEVER_MERGE = (".github/", ".gtd/")
REGISTER_KINDS = ("experiment", "benchmark", "finding")
LAYOUTS = ("flat", "item-folder")
REGISTER_KEYS = ("kind", "folder", "layout")
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


EXAMPLE_PREFIX = "example-"


def blocks(body: str, kind: str) -> list[dict]:
    """Parse '### <kind>: <name>' blocks of '- key: value' lines; list keys collect '  - x'.

    A block named ``example-*`` (the template's placeholders) is skipped everywhere: it
    is never linted, resumed, or counted as a grant."""
    out: list[dict] = []
    for m in re.finditer(rf"^### {kind}:\s*(.+?)\s*$(.*?)(?=^### |\Z)", body, re.M | re.S):
        item: dict = {"name": m.group(1).strip("` ")}
        if item["name"].startswith(EXAMPLE_PREFIX):
            continue
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
    pages = register_pages(text)
    for name, spec in pages.items():
        problems += register_problems(name, spec)
    for grant in blocks(section(text, "Merge grants"), "merge"):
        n = grant["name"]
        for k in MERGE_KEYS:
            if k == "paths" and grant.get("registers"):
                continue  # a grant may name registers instead of exact files
            if not grant.get(k):
                problems.append(f"merge grant {n}: missing {k}")
        regs = grant.get("registers") or []
        if regs and not isinstance(regs, list):
            problems.append(f"merge grant {n}: registers must be a list")
            regs = []
        for r in regs:
            if r not in pages:
                problems.append(f"merge grant {n}: register {r} has no block under ## Register pages")
        paths = grant.get("paths") or []
        for p in paths if isinstance(paths, list) else [paths]:
            p = p.strip("`")
            if p.startswith(NEVER_MERGE):
                problems.append(f"merge grant {n}: {p} is under .github/ or .gtd/; never granted")
            if any(c in p for c in "*?[") or p.endswith("/"):
                problems.append(f"merge grant {n}: name exact files; {p} is a pattern or folder")
    return problems


def register_pages(text: str) -> dict[str, dict]:
    """The repo's register page declarations: ``### register: <name>`` blocks under
    ``## Register pages`` with ``kind``, ``folder``, ``layout`` and optional ``type`` and
    ``links`` (a list of ``prefix: target``). A merge grant names these registers."""
    out: dict[str, dict] = {}
    for b in blocks(section(text, "Register pages"), "register"):
        links = {}
        for row in b.get("links") if isinstance(b.get("links"), list) else []:
            prefix, sep, target = row.partition(": ")
            if sep and prefix.strip() and target.strip():
                links[prefix.strip().strip("`")] = target.strip().strip("`")
        out[b["name"]] = {**b, "links": links}
    return out


def register_problems(name: str, spec: dict) -> list[str]:
    """Lint one register block: what a grant that names it would cover."""
    probs = [f"register {name}: missing {k}" for k in REGISTER_KEYS if not spec.get(k)]
    if spec.get("kind") and spec["kind"] not in REGISTER_KINDS:
        probs.append(f"register {name}: kind must be one of {', '.join(REGISTER_KINDS)}")
    if spec.get("layout") and spec["layout"] not in LAYOUTS:
        probs.append(f"register {name}: layout must be one of {', '.join(LAYOUTS)}")
    folder = str(spec.get("folder") or "").strip("`").rstrip("/")
    if folder and (folder.startswith(("/", ".")) or ".." in folder.split("/")
                   or any(c in folder for c in "*?[") or folder.startswith(NEVER_MERGE)
                   or (folder + "/").startswith(NEVER_MERGE)):
        probs.append(f"register {name}: folder {folder} must be a plain folder in the repo, "
                     "not a pattern and not under .github/ or .gtd/")
    return probs


def page_item(path: str, spec: dict) -> str | None:
    """The item a path is the record page of, under ``spec``'s folder and layout, else None.
    Flat: ``<folder>/<id>.md``. Item folders: ``<folder>/<id>/README.md``."""
    if register_problems("x", spec):
        return None
    folder = str(spec["folder"]).strip("`").rstrip("/")
    if not path.startswith(folder + "/"):
        return None
    rest = path[len(folder) + 1:].split("/")
    if spec["layout"] == "flat":
        ok = len(rest) == 1 and rest[0].endswith(".md")
        item = rest[0][:-3] if ok else ""
    else:
        ok = len(rest) == 2 and rest[1] == "README.md"
        item = rest[0] if ok else ""
    return item if ok and _page_modules()[0].SAFE_ID.match(item) else None


def _page_modules():
    """The reference page and record code, from this kit's conformance folder."""
    root = str(Path(__file__).resolve().parent.parent / "conformance")
    if root not in sys.path:
        sys.path.insert(0, root)
    import record_pages
    import register_records
    return record_pages, register_records


def page_refusals(spec: dict, item: str, old: str | None, new: str | None) -> list[str]:
    """Why the change from ``old`` to ``new`` is not only valid appended records of the
    page; [] is a pass. Uses the page rule, then validates each added record against the
    schema with the page's earlier records as context."""
    pages, records = _page_modules()
    type_ = spec.get("type") or spec["name"]
    refused = pages.check_page(old, new, item=item, kind=type_, folders=spec.get("links") or None)
    if refused:
        return refused
    before = pages.parse_page(old) if old is not None else []
    out = []
    for i, line in enumerate(pages.parse_page(new)[len(before):]):
        out += [f"record {len(before) + i + 1}: {r}" for r in
                records.validate(spec["kind"], line, prior=before + pages.parse_page(new)[len(before):len(before) + i])]
    return out


def covering_grants(text: str, paths: list[str], read=None) -> tuple[list[str], list[str]]:
    """(names of merged merge grants that cover every one of ``paths``, why not).

    A path is covered by a grant's exact ``paths``, or, when ``read(path) -> (old, new)``
    is given, by a register the grant names: the path is a record page of it and the change
    only appends valid records. One grant must cover every path."""
    want = [p.strip() for p in paths if p.strip()]
    if not want or any(p.startswith(NEVER_MERGE) for p in want):
        return [], ["no paths, or a path under .github/ or .gtd/"]
    pages = register_pages(text)
    names, why = [], []
    for g in blocks(section(text, "Merge grants"), "merge"):
        if not all(g.get(k) for k in MERGE_KEYS if k != "paths") or not (g.get("paths") or g.get("registers")):
            continue
        listed = {p.strip("`") for p in g.get("paths")} if isinstance(g.get("paths"), list) else set()
        regs = [pages[r] for r in (g.get("registers") if isinstance(g.get("registers"), list) else [])
                if r in pages and not register_problems(r, pages[r])]
        ok = True
        for path in want:
            if path in listed:
                continue
            if read is None or not regs:
                ok = False
                continue
            reasons = []
            for spec in regs:
                item = page_item(path, spec)
                if item is None:
                    continue
                old, new = read(path)
                bad = page_refusals(spec, item, old, new)
                if not bad:
                    break
                reasons.append(f"{path}: {', '.join(bad)}")
            else:
                ok = False
                why += reasons or [f"{path}: not named by grant {g['name']}"]
                continue
        if ok:
            names.append(g["name"])
    return names, why


def git_reader(base: str, head: str):
    """``read(path) -> (old, new)``: the file at ``base`` and at ``head``, None where absent."""
    def show(ref, path):
        r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    return lambda path: (show(base, path), show(head, path))


def merge_covers(text: str, paths: list[str], read=None) -> list[str]:
    """Names of merged merge grants that cover every one of ``paths``: exact files, and
    with ``read``, record pages of a named register (see ``covering_grants``)."""
    return covering_grants(text, paths, read)[0]


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
        if "--merge" in args:
            files = args[args.index("--merge") + 1:]
            head = args[args.index("--head") + 1] if "--head" in args else None
            base = args[args.index("--base") + 1] if "--base" in args else "origin/HEAD"
            named, why = covering_grants(text, files, git_reader(base, head) if head else None)
            if problems or not named:
                print(f"FAIL no merged merge grant names every changed file: {' '.join(files) or '(none)'}")
                for w in why:
                    print(f"FAIL {w}")
                return 1
            print(f"ok: {len(files)} file(s) covered by merge grant {', '.join(named)}")
            return 0
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
