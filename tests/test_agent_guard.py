#!/usr/bin/env python3
"""Tests for tools/agent_guard.py: both adapters, both rules, the reminder, failing open.

Standard library only: python3 tests/test_agent_guard.py (tests/check_kit.py runs it too).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "tools" / "agent_guard.py"
CLAUDE, CODEX = "--claude-hook", "--codex-hook"
EMAIL = "t" + "@" + "example.com"  # built at run time so the public guard stays quiet


def git(*args: str, cwd: Path) -> None:
    subprocess.run(["git", "-c", "user.name=t", "-c", f"user.email={EMAIL}", *args],
                   cwd=cwd, check=True, capture_output=True)


class Repo:
    """A throwaway work repo with an origin, so lanes.py can read the merged grants."""

    def __init__(self, grant: str | None = None):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        origin, self.root = base / "origin.git", base / "work"
        git("init", "-q", "--bare", str(origin), cwd=base)
        git("clone", "-q", str(origin), str(self.root), cwd=base)
        (self.root / ".gtd").mkdir()
        body = "# local\n"
        if grant:
            body += ("\n## Workflow grants\n\n### grant: ci\n- paths:\n"
                     f"  - {grant}\n- granted_by: owner\n- date: 2026-01-01\n"
                     "- link: https://example.com/approval\n")
        (self.root / ".gtd" / "BOARD.local.md").write_text(body)
        git("add", "-A", cwd=self.root)
        git("commit", "-qm", "base", cwd=self.root)
        git("push", "-q", "origin", "HEAD", cwd=self.root)
        git("remote", "set-head", "origin", "-a", cwd=self.root)

    def close(self) -> None:
        self.tmp.cleanup()


def run(adapter: str, event: dict | str, env: dict | None = None) -> subprocess.CompletedProcess:
    raw = event if isinstance(event, str) else json.dumps(event)
    return subprocess.run([sys.executable, str(GUARD), adapter], input=raw,
                          capture_output=True, text=True, env={**os.environ, **(env or {})}, check=False)


class GuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = Repo(grant=".github/workflows/granted.yml")
        cls.cwd = str(cls.repo.root)

    @classmethod
    def tearDownClass(cls):
        cls.repo.close()

    def tool(self, adapter: str, name: str, data: dict, env: dict | None = None):
        r = run(adapter, {"hook_event_name": "PreToolUse", "cwd": self.cwd,
                          "tool_name": name, "tool_input": data}, env)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)["hookSpecificOutput"] if r.stdout.strip() else None

    def assertDenied(self, adapter, name, data, env=None):
        out = self.tool(adapter, name, data, env)
        self.assertIsNotNone(out, f"{adapter} {name} {data} was allowed")
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertEqual(out["hookEventName"], "PreToolUse")

    def assertAllowed(self, adapter, name, data, env=None):
        self.assertIsNone(self.tool(adapter, name, data, env), f"{adapter} {name} {data}")

    # Rule 1: own PR create.
    def test_mcp_pr_create_denied_for_both(self):
        for adapter in (CLAUDE, CODEX):
            self.assertDenied(adapter, "mcp__github__create_pull_request",
                              {"owner": "o", "repo": "r", "title": "t", "head": "h", "base": "main"})

    def test_shell_pr_create_denied(self):
        for cmd in ("gh pr create --fill",
                    "git push -u origin HEAD && gh pr create --title t --body b",
                    "GH_REPO=o/r gh pr create",
                    "hub pull-request -m t",
                    "gh api repos/o/r/pulls -f title=t -f head=h -f base=main",
                    "gh api --method POST repos/o/r/pulls --input body.json",
                    "curl -X POST https://api.github.com/repos/o/r/pulls -d @b.json"):
            for adapter in (CLAUDE, CODEX):
                self.assertDenied(adapter, "Bash", {"command": cmd})

    def test_pr_reads_allowed(self):
        for cmd in ("gh pr view 1", "gh pr list", "gh api repos/o/r/pulls",
                    "gh api repos/o/r/pulls -X GET -f state=open",
                    "gh api repos/o/r/pulls/N/comments -f body=x", "echo gh pr create"):
            self.assertAllowed(CLAUDE, "Bash", {"command": cmd})
        self.assertAllowed(CLAUDE, "mcp__gtd__pr_open", {"repo": "o/r"})

    def test_pr_rule_switched_off(self):
        off = {"GTD_GUARD_PR_OPEN": "off"}
        self.assertAllowed(CLAUDE, "mcp__github__create_pull_request", {}, off)
        self.assertAllowed(CODEX, "Bash", {"command": "gh pr create"}, off)
        # The workflow rule still holds with the switch off.
        self.assertDenied(CLAUDE, "Write", {"file_path": ".github/workflows/x.yml"}, off)

    # Rule 2: workflow edits.
    def test_claude_edit_tools(self):
        for name, key in (("Write", "file_path"), ("Edit", "file_path"),
                          ("MultiEdit", "file_path"), ("NotebookEdit", "notebook_path")):
            self.assertDenied(CLAUDE, name, {key: ".github/workflows/ci.yml"})
            self.assertDenied(CLAUDE, name, {key: f"{self.cwd}/.github/workflows/ci.yml"})
            self.assertAllowed(CLAUDE, name, {key: "docs/workflows/ci.yml"})
        self.assertDenied(CLAUDE, "Write", {"file_path": ".GitHub/Workflows/ci.yml"})
        self.assertDenied(CLAUDE, "Write", {"file_path": "docs/../.github/workflows/ci.yml"})

    def test_codex_apply_patch(self):
        patch = ("*** Begin Patch\n*** Add File: .github/workflows/new.yml\n+on: push\n"
                 "*** End Patch\n")
        self.assertDenied(CODEX, "apply_patch", {"command": patch})
        moved = ("*** Begin Patch\n*** Update File: docs/a.yml\n*** Move to: "
                 ".github/workflows/a.yml\n*** End Patch\n")
        self.assertDenied(CODEX, "apply_patch", {"command": moved})
        ok = "*** Begin Patch\n*** Update File: src/app.py\n@@\n-a\n+b\n*** End Patch\n"
        self.assertAllowed(CODEX, "apply_patch", {"command": ok})

    def test_shell_workflow_writes(self):
        for cmd in ("echo x > .github/workflows/ci.yml",
                    "cat >> .github/workflows/ci.yml <<EOF",
                    "sed -i s/a/b/ .github/workflows/ci.yml",
                    "rm -rf .github/workflows",
                    "mkdir -p .github/workflows",
                    "cp /tmp/ci.yml .github/workflows/ci.yml",
                    "git checkout main -- .github/workflows/ci.yml",
                    "cd repo && tee .github/workflows/ci.yml < x"):
            for adapter in (CLAUDE, CODEX):
                self.assertDenied(adapter, "Bash", {"command": cmd})

    def test_shell_workflow_reads_allowed(self):
        for cmd in ("cat .github/workflows/ci.yml", "ls .github/workflows",
                    "grep -r on: .github/workflows", "git diff .github/workflows",
                    "cp .github/workflows/ci.yml /tmp/ci.yml",
                    "cat .github/workflows/ci.yml > /tmp/copy.yml"):
            self.assertAllowed(CLAUDE, "Bash", {"command": cmd})

    def test_mcp_file_writes(self):
        self.assertDenied(CLAUDE, "mcp__github__create_or_update_file",
                          {"path": ".github/workflows/ci.yml", "content": "x"})
        self.assertDenied(CODEX, "mcp__github__push_files",
                          {"files": [{"path": "README.md"}, {"path": ".github/workflows/ci.yml"}]})
        self.assertAllowed(CLAUDE, "mcp__github__create_or_update_file", {"path": "README.md"})

    def test_merged_grant_allows_named_path_only(self):
        self.assertAllowed(CLAUDE, "Write", {"file_path": ".github/workflows/granted.yml"})
        self.assertAllowed(CODEX, "Bash", {"command": "echo x > .github/workflows/granted.yml"})
        self.assertDenied(CLAUDE, "Write", {"file_path": ".github/workflows/other.yml"})
        self.assertDenied(CLAUDE, "Bash", {"command": "rm -rf .github/workflows"})

    # SessionStart and failing open.
    def test_session_start_reminder(self):
        for adapter in (CLAUDE, CODEX):
            r = run(adapter, {"hook_event_name": "SessionStart", "source": "startup",
                              "cwd": self.cwd})
            self.assertEqual(r.returncode, 0)
            lines = r.stdout.strip().splitlines()
            self.assertEqual(len(lines), 3)
            self.assertIn("BOARD.md", lines[0])
            self.assertIn("whoami", lines[1])
            self.assertIn("item_claim", lines[2])

    def test_fails_open(self):
        for raw in ("", "not json", "[]", json.dumps({"hook_event_name": "PreToolUse",
                                                     "tool_name": "Write", "tool_input": 3})):
            r = run(CLAUDE, raw)
            self.assertEqual((r.returncode, r.stdout), (0, ""), raw)
        self.assertAllowed(CLAUDE, "Read", {"file_path": ".github/workflows/ci.yml"})


def snippet_wires_guard() -> list[str]:
    """install/settings.snippet.json runs the guard for SessionStart and PreToolUse."""
    hooks = json.loads((ROOT / "install" / "settings.snippet.json").read_text())["hooks"]
    problems = []
    for event in ("SessionStart", "PreToolUse"):
        cmds = [h["command"] for g in hooks.get(event, []) for h in g["hooks"]]
        if not any("agent_guard.py" in c and CLAUDE in c for c in cmds):
            problems.append(f"settings.snippet.json {event} does not run agent_guard.py")
    matchers = " ".join(g.get("matcher", "") for g in hooks.get("PreToolUse", []))
    for name in ("Bash", "Write", "Edit", "create_pull_request"):
        if name not in matchers:
            problems.append(f"settings.snippet.json PreToolUse matcher misses {name}")
    return problems


class SnippetTest(unittest.TestCase):
    def test_snippet(self):
        self.assertEqual(snippet_wires_guard(), [])


if __name__ == "__main__":
    unittest.main()
