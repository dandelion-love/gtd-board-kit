#!/usr/bin/env python3
"""init_checkout.py: set up a new checkout of a work repo so agents can reach the gtd server.

Run it once in each new clone (the kit installer's session hook and `board-onboard` say so).
It resolves the server address with gtd_server.py and records it in the clone's git config
(`gtd.mcpUrl`, which lives in .git/config and is never committed). It prints which source
answered and never prints the address, and it writes no tracked file.

An address that already comes from the clone's git config, or from the committed context
file (a private repo's own choice), is left as it is.

Usage: init_checkout.py [--repo DIR]
Exit 0 when the clone resolves, 1 when no source has an address, 2 when one is malformed.
Standard library only.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gtd_server  # noqa: E402


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", default=".", help="the work repo checkout (default: here)")
    repo = Path(ap.parse_args(argv).repo)
    try:
        res = gtd_server.resolve(repo)
    except gtd_server.BadAddress as e:
        print(f"init_checkout: {e}", file=sys.stderr)
        return 2
    if not res.url:
        print(f"init_checkout: {gtd_server.not_found(res)}", file=sys.stderr)
        return 1
    if res.source in (gtd_server.Source.GIT_CONFIG, gtd_server.Source.CONTEXT):
        print(f"gtd server: resolved from the {res.source.value}; nothing to record")
        return 0
    try:
        subprocess.run(["git", "-C", str(repo), "config", "--local", gtd_server.GIT_KEY, res.url],
                       check=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"init_checkout: could not write the clone's git config: {e}", file=sys.stderr)
        return 1
    print(f"gtd server: resolved from the {res.source.value}; recorded in this clone's git "
          f"config ({gtd_server.GIT_KEY})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
