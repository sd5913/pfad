"""Exercise real stdio discovery and errors without a model or paid API."""
import sys
import unittest

from mcp_client import ROOT, Session


class TransportTests(unittest.TestCase):
    def test_discovery_and_bad_scale_are_real_tool_results(self):
        session = Session([sys.executable, str(ROOT / "blender_tools.py")])
        try:
            hello = session.request("initialize", {"protocolVersion":"2024-11-05", "capabilities":{}, "clientInfo":{"name":"test","version":"1"}})
            self.assertIn("tools", hello["capabilities"])
            session.send({"method":"notifications/initialized"})
            listing = session.request("tools/list")
            self.assertIn("render_scene", [tool["name"] for tool in listing["tools"]])
            for value in [True, -1, "large", 5]:
                result = session.request("tools/call", {"name":"render_scene", "arguments":{"scale":value}})
                self.assertTrue(result["isError"])
                self.assertIn("scale", result["content"][0]["text"])
        finally:
            session.close()
        self.assertIsNotNone(session.process.poll())


if __name__ == "__main__":
    unittest.main()
