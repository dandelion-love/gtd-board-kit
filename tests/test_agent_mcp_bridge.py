import importlib.util
import subprocess
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import anyio
import httpx


spec = importlib.util.spec_from_file_location("agent_mcp_bridge", Path(__file__).resolve().parents[1] / "tools" / "agent_mcp_bridge.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class AuthenticationTests(unittest.TestCase):
    def test_helper_uses_closed_input_and_authenticates_request(self):
        async def check():
            async def helper(*args, **kwargs):
                self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
                self.assertTrue(kwargs["check"])
                return SimpleNamespace(stdout=b"test-token\n")
            with patch.object(bridge.anyio, "run_process", helper):
                flow = bridge.JoinAuth("join.py", "agent").async_auth_flow(httpx.Request("POST", "https://example.test/mcp"))
                request = await anext(flow)
                self.assertEqual(request.headers["Authorization"], "Bearer test-token")
                await flow.aclose()
        anyio.run(check)

    def test_failed_helper_refuses_request(self):
        async def check():
            async def helper(*args, **kwargs):
                raise RuntimeError("helper failed")
            with patch.object(bridge.anyio, "run_process", helper):
                flow = bridge.JoinAuth("join.py", "agent").async_auth_flow(httpx.Request("POST", "https://example.test/mcp"))
                with self.assertRaisesRegex(RuntimeError, "credential unavailable"):
                    await anext(flow)
        anyio.run(check)

    def test_multiline_helper_output_is_rejected(self):
        async def check():
            async def helper(*args, **kwargs):
                return SimpleNamespace(stdout=b"bad\nvalue")
            with patch.object(bridge.anyio, "run_process", helper):
                flow = bridge.JoinAuth("join.py", "agent").async_auth_flow(httpx.Request("POST", "https://example.test/mcp"))
                with self.assertRaisesRegex(RuntimeError, "credential unavailable"):
                    await anext(flow)
        anyio.run(check)


if __name__ == "__main__":
    unittest.main()
