#!/usr/bin/env python3
"""public_guard.py: refuse to let private data into this PUBLIC repository.

Every agent and every person runs this before a commit or a push, through the git hooks in
.githooks/ and the Claude Code hooks in .claude/settings.json. It is strict on purpose: a
false alarm costs a rewrite of one line, a leak cannot be taken back.

Modes:
  --staged              scan what is staged for commit (pre-commit)
  --message FILE        scan a commit message (commit-msg)
  --range A..B          scan the files changed and the commit messages in a range (pre-push)
  --new REF             scan a ref the remote has never seen: whole tree + new commits
  --all                 scan every tracked file (tests, a manual check)
  --text                scan text on stdin
  --claude-hook         read a Claude Code PreToolUse event on stdin; block (exit 2) a git
                        commit or push, or a GitHub write tool, that would carry private data

Built-in rules are generic and name nothing private. Private names you also want blocked
(repo names, machine names, board titles, people) go in a denylist that lives OUTSIDE the
repo: the file named by $GTD_PUBLIC_DENYLIST, or ~/.config/gtd/public-denylist.txt. One
term per line, matched case-insensitively; a line starting with re: is a regular
expression; # starts a comment. Never commit that file.

Exit status: 0 clean, 1 private data found, 2 blocked (Claude hook mode).
Standard library only.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THIS_REPO = "gtd-board-kit"
ALLOWED_EMAILS = re.compile(r"(noreply@anthropic\.com|@users\.noreply\.github\.com)$", re.I)

# (name, pattern, applies to messages too). Generic shapes of private data only.
RULES: list[tuple[str, re.Pattern[str], bool]] = [
    ("secret or token", re.compile(
        r"(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|gtdj_[A-Za-z0-9_-]{8,}"
        r"|sk-ant-[A-Za-z0-9_-]{8,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"), True),
    ("Windows drive path", re.compile(r"(?<![A-Za-z])[A-Za-z]:\\[^\s`'\"]"), True),
    ("private filesystem path", re.compile(
        r"(/mnt/(?:project|user)-(?:files|data)|/Users/[A-Za-z]|/home/(?!user\b)[a-z][\w-]*/)"), True),
    ("issue or PR number", re.compile(r"(?<![\w&/])(?:[\w.-]+/[\w.-]+)?#\d+\b"), True),
    ("board number", re.compile(r"(projects(?:V2)?/\d+|\b[A-Za-z][\w-]*/\d+\b)"), True),
    ("long numeric id", re.compile(r"(?<![\w.])\d{7,}(?![\w.])"), True),
    ("cloud host or account", re.compile(
        r"([\w-]+\.run\.app|[\w-]+\.iam\.gserviceaccount\.com|\b\d{1,3}(?:\.\d{1,3}){3}\b)"), True),
    ("claude.ai link", re.compile(r"claude\.ai/(?:code/)?(?:artifact|project|session)", re.I), False),
    ("email address", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), True),
]


def denylist() -> list[re.Pattern[str]]:
    path = os.environ.get("GTD_PUBLIC_DENYLIST") or str(
        Path.home() / ".config" / "gtd" / "public-denylist.txt")
    out: list[re.Pattern[str]] = []
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return out
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            out.append(re.compile(line[3:], re.I))
        else:
            out.append(re.compile(re.escape(line), re.I))
    return out


def org_of_origin() -> str | None:
    try:
        url = subprocess.run(["git", "-C", str(ROOT), "remote", "get-url", "origin"],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    m = re.search(r"github\.com[:/]([^/]+)/", url)
    return m.group(1) if m else None


def scan(text: str, where: str, *, message: bool = False) -> list[str]:
    """Return one finding per offending line. Never prints the matched secret in full."""
    found: list[str] = []
    org = org_of_origin()
    other_repo = re.compile(
        rf"github\.com/{re.escape(org)}/(?!{THIS_REPO}\b)[\w.-]+", re.I) if org else None
    deny = denylist()
    for n, line in enumerate(text.splitlines(), 1):
        if message and re.match(r"^(Co-Authored-By|Claude-Session|Signed-off-by):", line):
            continue
        hits: list[str] = []
        for name, rx, in_msgs in RULES:
            if message and not in_msgs:
                continue
            for m in rx.finditer(line):
                if name == "email address" and ALLOWED_EMAILS.search(m.group(0)):
                    continue
                hits.append(name)
                break
        if other_repo and other_repo.search(line):
            hits.append("another repo in this org")
        if any(rx.search(line) for rx in deny):
            hits.append("local denylist term")
        if hits:
            shown = line.strip()
            shown = shown[:60] + ("…" if len(shown) > 60 else "")
            found.append(f"{where}:{n}: {', '.join(sorted(set(hits)))}: {shown}")
    return found


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True,
                          check=True).stdout


def is_text(blob: bytes) -> bool:
    return b"\0" not in blob[:8000]


def scan_staged() -> list[str]:
    out: list[str] = []
    for path in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split("\0"):
        if not path:
            continue
        blob = subprocess.run(["git", "-C", str(ROOT), "show", f":{path}"],
                              capture_output=True, check=True).stdout
        if is_text(blob):
            out += scan(blob.decode("utf-8", "replace"), path)
        out += scan(path, f"{path} (file name)")
    return out


def scan_range(rng: str) -> list[str]:
    out: list[str] = []
    head = rng.split("..")[-1]
    for path in git("diff", "--name-only", "--diff-filter=ACMR", "-z", rng).split("\0"):
        if not path:
            continue
        blob = subprocess.run(["git", "-C", str(ROOT), "show", f"{head}:{path}"],
                              capture_output=True, check=True).stdout
        if is_text(blob):
            out += scan(blob.decode("utf-8", "replace"), f"{head[:8]}:{path}")
    return out + scan_messages(git("rev-list", rng).split())


def scan_all() -> list[str]:
    out: list[str] = []
    for path in git("ls-files", "-z").split("\0"):
        if not path:
            continue
        p = ROOT / path
        if p.is_symlink() or not p.is_file():
            continue
        blob = p.read_bytes()
        if is_text(blob):
            out += scan(blob.decode("utf-8", "replace"), path)
    return out


def strings_in(obj) -> list[str]:
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        return [s for v in obj.values() for s in strings_in(v)]
    if isinstance(obj, list):
        return [s for v in obj for s in strings_in(v)]
    return []


def claude_hook() -> int:
    """PreToolUse: exit 2 with a reason on stderr blocks the tool call."""
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    tool = event.get("tool_name", "")
    data = event.get("tool_input", {}) or {}
    findings: list[str] = []
    if tool == "Bash":
        cmd = data.get("command", "")
        if re.search(r"\bgit\b[^|;&]*\bcommit\b", cmd):
            findings += scan_staged()
            m = re.search(r"-m\s+(\"[^\"]*\"|'[^']*')", cmd)
            if m:
                findings += scan(m.group(1)[1:-1], "commit message", message=True)
            if re.search(r"\s-a\b|--all\b", cmd):
                findings += ["git commit -a: stage files explicitly so the guard can see them"]
        if re.search(r"\bgit\b[^|;&]*\bpush\b", cmd):
            findings += scan_outgoing()
    elif tool.startswith("mcp__github__"):
        if data.get("repo") != THIS_REPO:
            return 0
        message_fields = {"message", "title", "body", "commit_message"}
        for key, value in data.items():
            for s in strings_in(value):
                findings += scan(s, f"{tool}.{key}", message=key in message_fields)
    if findings:
        print("public_guard: this repository is PUBLIC; private data found, call blocked:\n"
              + "\n".join(findings[:20])
              + "\nMove repo-specific details to the private repo's .gtd/BOARD.local.md.",
              file=sys.stderr)
        return 2
    return 0


def scan_tree(ref: str) -> list[str]:
    out: list[str] = []
    for line in git("ls-tree", "-r", "-z", ref).split("\0"):
        if not line:
            continue
        meta, path = line.split("\t", 1)
        if meta.split()[0] == "120000":
            continue  # symlink: its target is a path, not content
        blob = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", meta.split()[2]],
                              capture_output=True, check=True).stdout
        if is_text(blob):
            out += scan(blob.decode("utf-8", "replace"), f"{ref[:8]}:{path}")
    return out


def scan_messages(revs: list[str]) -> list[str]:
    out: list[str] = []
    for sha in revs:
        out += scan(git("log", "-1", "--format=%B", sha), f"commit {sha[:8]} message",
                    message=True)
        out += scan(git("log", "-1", "--format=%an <%ae>%n%cn <%ce>", sha),
                    f"commit {sha[:8]} author", message=True)
    return out


def scan_new(head: str) -> list[str]:
    """A ref the remote has never seen: the whole tree, plus every commit not on a remote."""
    remote = [r for r in git("for-each-ref", "--format=%(objectname)", "refs/remotes").split()]
    revs = git("rev-list", head, *(["--not", *remote] if remote else [])).split()
    return scan_tree(head) + scan_messages(revs)


def scan_outgoing() -> list[str]:
    """What a plain `git push` of the current branch would send."""
    try:
        upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}").strip()
    except subprocess.CalledProcessError:
        return scan_new("HEAD")
    return scan_range(f"{upstream}..HEAD")


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    mode = argv[0]
    if mode == "--claude-hook":
        return claude_hook()
    if mode == "--staged":
        findings = scan_staged()
    elif mode == "--message":
        findings = scan(Path(argv[1]).read_text(encoding="utf-8"), "commit message",
                        message=True)
    elif mode == "--range":
        findings = scan_range(argv[1])
    elif mode == "--new":
        findings = scan_new(argv[1])
    elif mode == "--all":
        findings = scan_all()
    elif mode == "--text":
        findings = scan(sys.stdin.read(), "stdin")
    else:
        print(f"unknown mode {mode}", file=sys.stderr)
        return 2
    if findings:
        print("public_guard: this repository is PUBLIC; private data found:\n"
              + "\n".join(findings), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
