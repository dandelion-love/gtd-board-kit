#!/usr/bin/env python3
"""gtd_server.py: find the gtd server's address for a checkout, without committing it.

A public work repo must not publish the server's address, so `mcp_url` in
`.github/gtd-context.json` is optional there. Every kit tool and skill resolves the address
in this order and the first source present wins:

  1. $GTD_MCP_URL
  2. the clone's git config, `gtd.mcpUrl` (it lives in .git/config, so it is never committed)
  3. the user-level map ~/.config/gtd/servers.json (or the file named by $GTD_SERVERS_FILE),
     a JSON object keyed by the board owner in gtd-context.json: {"<owner>": "<url>"}
  4. `mcp_url` in gtd-context.json; the value "local" or no key means "resolve locally"

An address is the server's base URL: https, a host, no path. A source that is present but
malformed is an error naming the source; it never falls through to the next one.

Usage:
  gtd_server.py [--repo DIR]            print which source answered (never the address)
  gtd_server.py [--repo DIR] --url      print the address
  gtd_server.py [--repo DIR] --host     print the host only
Exit 0 when resolved, 1 when no source has it (the message names each place looked in), 2 on
a malformed value. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from urllib.parse import urlsplit

ENV_VAR = "GTD_MCP_URL"
SERVERS_ENV_VAR = "GTD_SERVERS_FILE"
GIT_KEY = "gtd.mcpUrl"
CONTEXT_FILE = Path(".github") / "gtd-context.json"
LOCAL = "local"


class Source(str, Enum):
    ENV = "environment"
    GIT_CONFIG = "git config"
    USER_MAP = "user map"
    CONTEXT = "context file"


class BadAddress(ValueError):
    def __init__(self, source: Source, why: str):
        super().__init__(f"{source.value}: {why}")
        self.source = source


@dataclass
class Resolution:
    url: str | None = None
    source: Source | None = None
    tried: list[str] = field(default_factory=list)

    @property
    def host(self) -> str | None:
        return urlsplit(self.url).hostname if self.url else None

    @property
    def committed(self) -> bool:
        """The address came from a tracked file, so it is meant to be public in that repo."""
        return self.source is Source.CONTEXT


def normalise(value: str, source: Source) -> str:
    value = value.strip().rstrip("/")
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.hostname:
        raise BadAddress(source, "the address must be an https URL with a host")
    if parts.path or parts.query or parts.fragment or parts.username or parts.password:
        raise BadAddress(source, "the address is the base URL: no path, query or credentials")
    return f"https://{parts.netloc}"


def _context(repo: Path) -> dict:
    try:
        data = json.loads((repo / CONTEXT_FILE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def board_owner(repo: Path) -> str | None:
    project = _context(repo).get("project")
    if isinstance(project, dict):
        owner = project.get("owner")
    elif isinstance(project, str) and "/" in project:
        owner = project.split("/", 1)[0]
    else:
        owner = None
    return owner if isinstance(owner, str) and owner else None


def servers_file(env: dict[str, str], home: Path) -> Path:
    return Path(env.get(SERVERS_ENV_VAR) or home / ".config" / "gtd" / "servers.json")


def _git_config(repo: Path) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(repo), "config", "--local", "--get", GIT_KEY],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return out or None


def _user_map(repo: Path, env: dict[str, str], home: Path) -> str | None:
    owner = board_owner(repo)
    if not owner:
        return None
    try:
        data = json.loads(servers_file(env, home).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    for key, value in data.items():
        if isinstance(key, str) and key.lower() == owner.lower() and isinstance(value, str):
            return value
    return None


def resolve(repo: Path, env: dict[str, str] | None = None,
            home: Path | None = None) -> Resolution:
    """The first source that has an address; raises BadAddress for a malformed one."""
    env = dict(os.environ) if env is None else env
    home = Path.home() if home is None else home
    owner = board_owner(repo)
    committed = _context(repo).get("mcp_url")
    candidates = (
        (Source.ENV, f"${ENV_VAR}", env.get(ENV_VAR)),
        (Source.GIT_CONFIG, f"git config {GIT_KEY} (in this clone's .git/config)",
         _git_config(repo)),
        (Source.USER_MAP, f"{servers_file(env, home)}" + (f" (key {owner})" if owner else
                                                           " (needs a board owner in the context file)"),
         _user_map(repo, env, home)),
        (Source.CONTEXT, f"mcp_url in {CONTEXT_FILE.as_posix()}",
         committed if isinstance(committed, str) and committed.strip().lower() != LOCAL else None),
    )
    tried: list[str] = []
    for source, place, value in candidates:
        tried.append(place)
        if value and value.strip():
            return Resolution(normalise(value, source), source, tried)
    return Resolution(None, None, tried)


def not_found(res: Resolution) -> str:
    places = "\n".join(f"  {i}. {p}" for i, p in enumerate(res.tried, 1))
    return ("no gtd server address found. Looked in, in order:\n" + places +
            "\nSet one of them (init_checkout.py records it in the clone), then ask your person "
            "only if you cannot.")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=".", help="the work repo checkout (default: here)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--url", action="store_true", help="print the address")
    g.add_argument("--host", action="store_true", help="print the host only")
    a = ap.parse_args(argv)
    try:
        res = resolve(Path(a.repo))
    except BadAddress as e:
        print(f"gtd_server: {e}", file=sys.stderr)
        return 2
    if not res.url:
        print(f"gtd_server: {not_found(res)}", file=sys.stderr)
        return 1
    print(res.url if a.url else res.host if a.host else f"source: {res.source.value}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
