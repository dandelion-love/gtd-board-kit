#!/usr/bin/env python3
"""agent_guard.py: early, cheap refusals for Claude Code and Codex agents in a work repo.

Two PreToolUse rules and a SessionStart reminder, shared by both agents:

  1. No own PR create while the gtd server offers `pr_open`. An agent hands work back
     through `pr_open` (BOARD.md, `board-claim`), never its own GitHub tool: any MCP
     `create_pull_request`, `gh pr create`, `hub pull-request`, or a POST to `/pulls`
     with `gh api` or `curl` is denied. Set GTD_GUARD_PR_OPEN=off in the agent's
     environment for a repo whose gtd server does not offer `pr_open` yet.
  2. No edits under `.github/workflows/**` unless a workflow grant merged into
     `.gtd/BOARD.local.md` names that path (`lanes.py check --merged --covers`). Covers
     Claude's Write/Edit/MultiEdit/NotebookEdit, Codex's apply_patch, shell writes and
     GitHub MCP file writes. Reading workflows stays allowed.

SessionStart prints a three-line reminder, which both agents add to the session context.

This is an accelerator, not the guarantee: the gtd server and the PR check enforce the
same rules for every agent, including ones without hooks. So the guard fails open: a
malformed event or an internal error allows the call.

Modes (each reads one hook event as JSON on stdin):
  --claude-hook   Claude Code (wired by install/settings.snippet.json)
  --codex-hook    Codex, from <repo>/.codex/hooks.json:
                    {"hooks": {
                      "SessionStart": [{"hooks": [{"type": "command", "command":
                        "python3 \\"$(git rev-parse --show-toplevel)/.gtd/kit/tools/agent_guard.py\\" --codex-hook"}]}],
                      "PreToolUse": [{"matcher": "Bash|apply_patch|mcp__.*", "hooks": [{"type": "command",
                        "command": "python3 \\"$(git rev-parse --show-toplevel)/.gtd/kit/tools/agent_guard.py\\" --codex-hook"}]}]}}

A denial is printed as {"hookSpecificOutput": {"hookEventName": "PreToolUse",
"permissionDecision": "deny", ...}} with exit 0, the form both agents read.
Standard library only.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from enum import Enum
from pathlib import Path, PurePosixPath

TOOLS = Path(__file__).resolve().parent
WORKFLOWS = ".github/workflows"
PR_OPEN_ENV = "GTD_GUARD_PR_OPEN"

REMINDER = """Board work: read .gtd/kit/BOARD.md, then .gtd/BOARD.local.md, before touching the board.
Call whoami on the gtd MCP server first; reach the board only through it.
Claim every story you work (item_claim) before you commit, and hand back with pr_open."""


class Adapter(Enum):
    CLAUDE = "--claude-hook"
    CODEX = "--codex-hook"


class Event(str, Enum):
    PRE_TOOL_USE = "PreToolUse"
    SESSION_START = "SessionStart"


class Switch(str, Enum):
    ON = "on"
    OFF = "off"


# File-edit tools and the input keys that name the edited file, per agent.
EDIT_TOOLS: dict[Adapter, dict[str, tuple[str, ...]]] = {
    Adapter.CLAUDE: {"Write": ("file_path",), "Edit": ("file_path",),
                     "MultiEdit": ("file_path",), "NotebookEdit": ("notebook_path",)},
    Adapter.CODEX: {},  # Codex edits through apply_patch, parsed below
}
SHELL_TOOLS = {"Bash"}           # both agents report shell and exec_command as Bash
PATCH_TOOLS = {"apply_patch"}    # Codex
MCP_PR_CREATE = re.compile(r"^mcp__.+__create_pull_request$")
MCP_FILE_WRITE = re.compile(r"^mcp__.+__(create_or_update_file|delete_file|push_files)$")

PATCH_PATH = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+?)\s*$|^\*\*\* Move to: (.+?)\s*$",
                        re.M)
SEGMENT_SPLIT = re.compile(r"\|\||&&|[;|\n]")
WRITE_VERBS = {"mv", "rm", "tee", "touch", "mkdir", "truncate", "chmod", "dd", "unlink",
               "rmdir"}
COPY_VERBS = {"cp", "install", "ln", "rsync"}  # only the last argument is written
GIT_WRITE = {"rm", "mv", "checkout", "restore", "apply", "am"}
IN_PLACE = {"sed", "perl", "ruby"}


def deny(reason: str) -> int:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": Event.PRE_TOOL_USE.value,
        "permissionDecision": "deny",
        "permissionDecisionReason": f"agent_guard: {reason}"}}))
    return 0


def pr_open_offered() -> bool:
    value = os.environ.get(PR_OPEN_ENV, Switch.ON.value).strip().lower()
    return value != Switch.OFF.value


def repo_root(cwd: str) -> Path:
    try:
        out = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return Path(out)
    except (OSError, subprocess.CalledProcessError):
        return Path(cwd)


def rel_path(path: str, cwd: str, root: Path) -> str:
    """The path relative to the repo root, with forward slashes ('' when outside it)."""
    p = Path(path.strip().strip("'\""))
    if not p.is_absolute():
        p = Path(cwd) / p
    try:
        rel = Path(os.path.normpath(p)).relative_to(os.path.normpath(root))
    except ValueError:
        return ""
    return PurePosixPath(*rel.parts).as_posix()


def is_workflow(rel: str) -> bool:
    # Lower-cased: on a case-insensitive disk .GitHub/Workflows is the same folder.
    low = rel.lower()
    return low == WORKFLOWS or low.startswith(WORKFLOWS + "/")


def granted(rel: str, root: Path) -> bool:
    """A merged workflow grant names this exact path (lanes.py is the authority)."""
    lanes = TOOLS / "lanes.py"
    if not lanes.exists() or rel.lower() == WORKFLOWS:
        return False
    try:
        r = subprocess.run([sys.executable, str(lanes), "check", "--merged", "--covers", rel],
                           cwd=str(root), capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.SubprocessError):
        return False
    return r.returncode == 0


def origin_repo(root: Path) -> str | None:
    """`owner/repo` of the checkout's origin, lower-cased, or None."""
    try:
        url = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    m = re.search(r"github\.com[:/]([^/\s]+)/([^/\s]+?)(?:\.git)?/?$", url)
    return f"{m.group(1)}/{m.group(2)}".lower() if m else None


def mcp_target_is_checkout(data: dict, root: Path) -> bool:
    """A GitHub MCP write names its repo; this checkout's grants count only for this repo."""
    owner, repo = str(data.get("owner") or ""), str(data.get("repo") or "")
    if "/" in repo and not owner:
        owner, repo = repo.split("/", 1)
    here = origin_repo(root)
    return bool(here and owner and repo and f"{owner}/{repo}".lower() == here)


def workflow_denial(paths: list[str], cwd: str, root: Path, *,
                    grants_apply: bool = True) -> str | None:
    for path in paths:
        rel = rel_path(path, cwd, root)
        if rel and is_workflow(rel) and not (grants_apply and granted(rel, root)):
            return (f"{rel} is under .github/workflows/; agents never create or edit "
                    "workflows unless a merged workflow grant in .gtd/BOARD.local.md names "
                    "that path. Ask your person instead (board-needs-person).")
    return None


def words(segment: str) -> list[str]:
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def shell_workflow_paths(command: str) -> list[str]:
    """Workflow paths a shell command writes, removes or creates. Reads are not listed."""
    out: list[str] = []
    for seg in SEGMENT_SPLIT.split(command):
        if WORKFLOWS not in seg.lower():
            continue
        targets = [w for w in re.findall(r"[^\s'\"<>]+", seg) if WORKFLOWS in w.lower()]
        redirected = [m for m in re.findall(r">>?\s*['\"]?([^\s'\"]+)", seg)
                      if WORKFLOWS in m.lower()]
        w = words(seg)
        while w and re.match(r"^\w+=", w[0]):  # FOO=bar cmd
            w = w[1:]
        if w and w[0] in ("sudo", "command", "env"):
            w = w[1:]
        verb = Path(w[0]).name if w else ""
        writes = (verb in WRITE_VERBS
                  or (verb == "git" and len(w) > 1 and w[1] in GIT_WRITE)
                  or (verb in IN_PLACE and any(a.startswith("-i") or a == "--in-place"
                                               for a in w[1:])))
        if redirected:
            out += redirected
        elif writes:
            out += targets
        elif verb in COPY_VERBS:
            dest = [a for a in w[1:] if not a.startswith("-")][-1:]
            out += [d for d in dest if WORKFLOWS in d.lower()]
    return out


def patch_paths(patch: str) -> list[str]:
    return [a or b for a, b in PATCH_PATH.findall(patch)]


def shell_pr_create(command: str) -> bool:
    for seg in SEGMENT_SPLIT.split(command):
        w = words(seg)
        while w and re.match(r"^\w+=", w[0]):
            w = w[1:]
        if not w:
            continue
        verb = Path(w[0]).name
        if verb == "gh" and w[1:3] == ["pr", "create"]:
            return True
        if verb == "hub" and len(w) > 1 and w[1] == "pull-request":
            return True
        if verb in ("gh", "curl") and (verb == "curl" or w[1:2] == ["api"]):
            if not any(re.search(r"(^|/)repos/[^/\s]+/[^/\s]+/pulls/?$", a.split("?")[0])
                       for a in w):
                continue
            joined = " ".join(w)
            method = re.search(r"(?:-X|--method|--request)\s*=?\s*([A-Za-z]+)", joined)
            if method:
                if method.group(1).upper() == "POST":
                    return True
                continue
            # gh api and curl both POST once a body is given.
            if re.search(r"(^|\s)(-f|-F|--field|--raw-field|--input|-d|--data\S*|--json)\b",
                         joined):
                return True
    return False


def pr_denial() -> str:
    return ("open the PR with the gtd server's pr_open, never your own GitHub tool "
            "(BOARD.md, board-claim). If this repo's gtd server does not offer pr_open, "
            f"your person sets {PR_OPEN_ENV}=off for it.")


def pre_tool_use(adapter: Adapter, event: dict) -> int:
    tool = str(event.get("tool_name") or "")
    data = event.get("tool_input") or {}
    if not isinstance(data, dict):
        return 0
    cwd = str(event.get("cwd") or os.getcwd())
    root = repo_root(cwd)

    if pr_open_offered():
        if MCP_PR_CREATE.match(tool):
            return deny(pr_denial())
        if tool in SHELL_TOOLS and shell_pr_create(str(data.get("command") or "")):
            return deny(pr_denial())

    paths: list[str] = []
    grants_apply = True
    if tool in EDIT_TOOLS[adapter]:
        paths = [str(data[k]) for k in EDIT_TOOLS[adapter][tool] if data.get(k)]
    elif tool in SHELL_TOOLS:
        paths = shell_workflow_paths(str(data.get("command") or ""))
    elif adapter is Adapter.CODEX and tool in PATCH_TOOLS:
        paths = patch_paths(str(data.get("command") or data.get("patch") or data.get("input") or ""))
    elif MCP_FILE_WRITE.match(tool):
        # Repo paths, not local ones: resolve them against the root itself.
        names = [data.get("path")] + [f.get("path") for f in data.get("files") or []
                                      if isinstance(f, dict)]
        paths = [str(root / n) for n in names if n]
        # Another repo's write is never covered by this checkout's grants.
        grants_apply = mcp_target_is_checkout(data, root)
    reason = workflow_denial(paths, cwd, root, grants_apply=grants_apply)
    return deny(reason) if reason else 0


def session_start() -> int:
    print(REMINDER)
    return 0


def run(adapter: Adapter, raw: str) -> int:
    try:
        event = json.loads(raw)
    except ValueError:
        return 0
    if not isinstance(event, dict):
        return 0
    name = event.get("hook_event_name")
    if name == Event.SESSION_START.value:
        return session_start()
    if name == Event.PRE_TOOL_USE.value or (name is None and "tool_name" in event):
        return pre_tool_use(adapter, event)
    return 0


def main(argv: list[str]) -> int:
    modes = {a.value: a for a in Adapter}
    if not argv or argv[0] not in modes:
        print(__doc__)
        return 0 if argv and argv[0] in ("-h", "--help") else 2
    try:
        return run(modes[argv[0]], sys.stdin.read())
    except Exception as exc:  # noqa: BLE001 - fail open: the server and the PR check are the guarantee
        print(f"agent_guard: internal error, allowing the call: {exc}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
