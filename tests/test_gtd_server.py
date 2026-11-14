#!/usr/bin/env python3
"""Tests for tools/gtd_server.py, tools/init_checkout.py and the guard's work-repo mode.

Standard library only: python3 tests/test_gtd_server.py (tests/check_kit.py runs it too).
Hosts are placeholders on example domains; nothing here names a real server.
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
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import gtd_server  # noqa: E402
from gtd_server import BadAddress, Source  # noqa: E402

EMAIL = "t" + "@" + "example.com"
ENV_URL = "https://env.gtd.example.org"
GIT_URL = "https://git.gtd.example.org"
MAP_URL = "https://map.gtd.example.org"
CTX_URL = "https://ctx.gtd.example.org"


def run(*args: str, cwd: Path, env: dict | None = None, text: str | None = None):
    full = {**os.environ, **(env or {})}
    if "GTD_MCP_URL" not in (env or {}):
        full.pop("GTD_MCP_URL", None)
    return subprocess.run([sys.executable, *args], cwd=cwd, env=full, input=text or "",
                          capture_output=True, text=True, timeout=60)


class Checkout:
    """A throwaway work repo whose context file may carry mcp_url, plus a fake home."""

    def __init__(self, mcp_url: str | None = None, owner: str = "acme"):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.repo, self.home = base / "repo", base / "home"
        self.repo.mkdir()
        self.home.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        ctx = {"profile": "software", "project": {"owner": owner, "number": 1}}
        if mcp_url is not None:
            ctx["mcp_url"] = mcp_url
        (self.repo / ".github").mkdir()
        (self.repo / ".github" / "gtd-context.json").write_text(json.dumps(ctx))
        self.servers = base / "servers.json"

    def env(self, **extra: str) -> dict[str, str]:
        return {"GTD_SERVERS_FILE": str(self.servers), "GTD_PUBLIC_DENYLIST": str(self.home / "none"),
                "HOME": str(self.home), **extra}

    def set_map(self, data) -> None:
        self.servers.write_text(json.dumps(data))

    def set_git(self, url: str) -> None:
        subprocess.run(["git", "config", "--local", "gtd.mcpUrl", url], cwd=self.repo, check=True)

    def resolve(self, **env: str):
        return gtd_server.resolve(self.repo, {"GTD_SERVERS_FILE": str(self.servers), **env}, self.home)

    def close(self) -> None:
        self.tmp.cleanup()


class Resolve(unittest.TestCase):
    def setUp(self):
        self.c = Checkout()
        self.addCleanup(self.c.close)

    def test_env_alone_works_with_mcp_url_absent(self):  # AC1
        res = self.c.resolve(GTD_MCP_URL=ENV_URL)
        self.assertEqual((res.url, res.source), (ENV_URL, Source.ENV))

    def test_each_source_is_honoured(self):  # AC2
        self.c.set_map({"ACME": MAP_URL})  # keyed case-insensitively
        self.assertEqual(self.c.resolve().source, Source.USER_MAP)
        self.assertEqual(self.c.resolve().url, MAP_URL)
        self.c.set_git(GIT_URL + "/")  # a trailing slash is normalised away
        self.assertEqual((self.c.resolve().url, self.c.resolve().source), (GIT_URL, Source.GIT_CONFIG))

    def test_first_present_wins(self):  # AC2
        c = Checkout(CTX_URL)
        self.addCleanup(c.close)
        self.assertEqual(c.resolve().source, Source.CONTEXT)
        c.set_map({"acme": MAP_URL})
        self.assertEqual(c.resolve().source, Source.USER_MAP)
        c.set_git(GIT_URL)
        self.assertEqual(c.resolve().source, Source.GIT_CONFIG)
        self.assertEqual(c.resolve(GTD_MCP_URL=ENV_URL).source, Source.ENV)

    def test_local_means_resolve_locally(self):
        c = Checkout("local")
        self.addCleanup(c.close)
        self.assertIsNone(c.resolve().url)
        self.assertEqual(c.resolve(GTD_MCP_URL=ENV_URL).source, Source.ENV)

    def test_map_for_another_owner_does_not_answer(self):
        self.c.set_map({"other": MAP_URL})
        self.assertIsNone(self.c.resolve().url)

    def test_present_but_malformed_does_not_fall_through(self):
        self.c.set_map({"acme": MAP_URL})
        for bad in ("http://x.example.org", "https://x.example.org/mcp", "not a url",
                    "https://user:" + "pw" + "@x.example.org"):
            with self.assertRaises(BadAddress, msg=bad) as cm:
                self.c.resolve(GTD_MCP_URL=bad)
            self.assertIs(cm.exception.source, Source.ENV)

    def test_nothing_present_names_every_place(self):  # AC3
        res = self.c.resolve()
        self.assertIsNone(res.url)
        self.assertEqual(len(res.tried), 4)
        message = gtd_server.not_found(res)
        for place in ("$GTD_MCP_URL", "gtd.mcpUrl", "servers.json", "mcp_url"):
            self.assertIn(place, message)
        r = run(str(TOOLS / "gtd_server.py"), "--repo", str(self.c.repo), cwd=self.c.repo,
                env=self.c.env())
        self.assertEqual(r.returncode, 1)
        self.assertIn("Looked in", r.stderr)

    def test_cli_prints_source_not_address_unless_asked(self):
        env = self.c.env(GTD_MCP_URL=ENV_URL)
        base = [str(TOOLS / "gtd_server.py"), "--repo", str(self.c.repo)]
        r = run(*base, cwd=self.c.repo, env=env)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "source: environment"))
        self.assertNotIn("example.org", r.stdout)
        self.assertEqual(run(*base, "--url", cwd=self.c.repo, env=env).stdout.strip(), ENV_URL)
        self.assertEqual(run(*base, "--host", cwd=self.c.repo, env=env).stdout.strip(),
                         "env.gtd.example.org")


class InitCheckout(unittest.TestCase):
    def setUp(self):
        self.c = Checkout()
        self.addCleanup(self.c.close)
        self.cmd = [str(TOOLS / "init_checkout.py"), "--repo", str(self.c.repo)]

    def test_records_in_git_config_and_never_echoes_the_address(self):
        r = run(*self.cmd, cwd=self.c.repo, env=self.c.env(GTD_MCP_URL=ENV_URL))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("environment", r.stdout)
        self.assertNotIn("example.org", r.stdout + r.stderr)
        self.assertEqual(self.c.resolve().url, ENV_URL)  # now resolves with no env
        self.assertEqual(self.c.resolve().source, Source.GIT_CONFIG)
        status = subprocess.run(["git", "status", "--porcelain", "--ignored"], cwd=self.c.repo,
                                capture_output=True, text=True).stdout
        self.assertNotIn("servers", status)
        for p in self.c.repo.rglob("*"):  # no tracked or untracked file holds the address
            if p.is_file() and ".git" not in p.parts:
                self.assertNotIn("example.org", p.read_text())

    def test_user_map_answers_every_checkout_of_an_org(self):
        self.c.set_map({"acme": MAP_URL})
        r = run(*self.cmd, cwd=self.c.repo, env=self.c.env())
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("user map", r.stdout)

    def test_unresolved_says_where_it_looked(self):
        r = run(*self.cmd, cwd=self.c.repo, env=self.c.env())
        self.assertEqual(r.returncode, 1)
        self.assertIn("Looked in", r.stderr)

    def test_committed_address_is_left_alone(self):
        c = Checkout(CTX_URL)
        self.addCleanup(c.close)
        r = run(str(TOOLS / "init_checkout.py"), "--repo", str(c.repo), cwd=c.repo, env=c.env())
        self.assertEqual(r.returncode, 0)
        self.assertIn("nothing to record", r.stdout)
        self.assertEqual(c.resolve().source, Source.CONTEXT)


class WorkRepoGuard(unittest.TestCase):
    GUARD = str(TOOLS / "public_guard.py")

    def setUp(self):
        self.c = Checkout()
        self.addCleanup(self.c.close)

    def stage(self, text: str, name: str = "notes.md") -> None:
        (self.c.repo / name).write_text(text)
        subprocess.run(["git", "add", name], cwd=self.c.repo, check=True)

    def guard(self, *mode: str, **env: str):
        return run(self.GUARD, "--repo", str(self.c.repo), *mode, cwd=self.c.repo,
                   env=self.c.env(**env))

    def test_staged_file_with_the_resolved_host_is_refused(self):  # AC4
        self.stage("connect to env.gtd.example.org first\n")
        r = self.guard("--staged", GTD_MCP_URL=ENV_URL)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("local denylist term", r.stderr)
        self.assertEqual(self.guard("--staged").returncode, 0)  # nothing resolved: nothing to refuse

    def test_the_host_is_refused_in_text_and_messages(self):
        r = run(self.GUARD, "--repo", str(self.c.repo), "--text", cwd=self.c.repo,
                env=self.c.env(GTD_MCP_URL=ENV_URL), text="see https://env.gtd.example.org/join\n")
        self.assertEqual(r.returncode, 1)

    def test_a_longer_host_is_not_a_match(self):
        self.stage("see other-env.gtd.example.org.invalid\n")
        self.assertEqual(self.guard("--staged", GTD_MCP_URL=ENV_URL).returncode, 0)

    def test_work_repo_text_the_kit_would_refuse_is_allowed(self):
        self.stage("fixes " + "#" + "12 on board " + "acme/" + "4\n")
        self.assertEqual(self.guard("--staged", GTD_MCP_URL=ENV_URL).returncode, 0)

    def test_denylist_still_applies(self):
        deny = self.c.home / "deny.txt"
        deny.write_text("secret-lab-name\n")
        self.stage("the secret-lab-name repo\n")
        r = self.guard("--staged", GTD_PUBLIC_DENYLIST=str(deny))
        self.assertEqual(r.returncode, 1)

    def test_a_committed_address_is_not_refused(self):
        c = Checkout(CTX_URL)
        self.addCleanup(c.close)
        (c.repo / "x.md").write_text("server at ctx.gtd.example.org\n")
        subprocess.run(["git", "add", "x.md"], cwd=c.repo, check=True)
        r = run(self.GUARD, "--repo", str(c.repo), "--staged", cwd=c.repo, env=c.env())
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
