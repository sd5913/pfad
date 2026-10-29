"""Opt-in acceptance test: a genuine third-party bridge changes real Blender."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent


class BlenderLiveTests(unittest.TestCase):
    def test_live_scene_change_render_and_clean_shutdown(self):
        result = subprocess.run([sys.executable, str(ROOT / "blender_live.py"), "--verify"],
                                cwd=ROOT, capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        record = json.loads((ROOT / ".output/blender-live-result.json").read_text())
        self.assertEqual(record["scale"], [1.5, 1.5, 1.5])
        self.assertEqual(record["blender_exit"], 0)
        self.assertTrue(record["socket_closed"])
        self.assertIn("execute_blender_code", record["tools"])
        self.assertTrue(Path(record["render"]).read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
