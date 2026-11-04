#!/usr/bin/env python3
"""Bridge stdio MCP to a device-code-authenticated streamable HTTP server.

Requires the official Python MCP SDK. The join client owns credential storage and
refresh; this process only obtains short-lived access tokens for HTTP requests.
"""
import argparse
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

import anyio
import httpx
from mcp.client.streamable_http import streamable_http_client
from mcp.server.stdio import stdio_server


class JoinAuth(httpx.Auth):
    def __init__(self, client: str, name: str):
        self.client, self.name = client, name

    async def async_auth_flow(self, request):
        try:
            with anyio.fail_after(45):
                result = await anyio.run_process(
                    [sys.executable, self.client, "--token", "--name", self.name],
                    check=True, stdin=subprocess.DEVNULL,
                )
            token = result.stdout.decode("utf-8").strip()
            if not token or "\n" in token or "\r" in token:
                raise ValueError("invalid token")
        except Exception:
            raise RuntimeError("Agent credential unavailable; rejoin if necessary") from None
        request.headers["Authorization"] = "Bearer " + token
        yield request


async def forward(source, target):
    async with source, target:
        async for message in source:
            if isinstance(message, Exception):
                raise message
            await target.send(message)


async def run(url, client, name):
    async with httpx.AsyncClient(auth=JoinAuth(client, name), follow_redirects=False, timeout=None) as http:
        async with stdio_server() as (local_read, local_write):
            async with streamable_http_client(url, http_client=http) as (remote_read, remote_write, _):
                async with anyio.create_task_group() as group:
                    group.start_soon(forward, local_read, remote_write)
                    group.start_soon(forward, remote_read, local_write)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="HTTPS MCP endpoint")
    parser.add_argument("--join-client", required=True, type=Path)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    parsed = urlsplit(args.url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        parser.error("--url must be an HTTPS URL without userinfo or fragment")
    anyio.run(run, args.url, str(args.join_client), args.name)


if __name__ == "__main__":
    main()
