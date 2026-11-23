"""Real Godot behavior checks in an isolated copy, with no graphical claims."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from world import PROJECT, engine


class GodotTests(unittest.TestCase):
    def test_default_fails_when_slow_and_recovers(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "project"
            shutil.copytree(PROJECT, target, ignore=shutil.ignore_patterns(".godot"))
            environment = {**os.environ, "XDG_DATA_HOME":str(Path(folder) / "data")}
            for speed, expected in [(300, True), (120, False), (360, True)]:
                config = json.loads((target / "world.json").read_text())
                config["speed"] = speed
                (target / "world.json").write_text(json.dumps(config))
                result = subprocess.run([engine(), "--headless", "--path", str(target), "--script", "res://check_world.gd", "--quit-after", "2"], env=environment, capture_output=True, text=True, timeout=15)
                checks = [json.loads(line.removeprefix("WORLD_CHECK ")) for line in result.stdout.splitlines() if line.startswith("WORLD_CHECK ")]
                self.assertEqual(len(checks), 1, result.stderr)
                self.assertEqual(checks[0]["passed"], expected)
                self.assertEqual(result.returncode, 0 if expected else 1)
                self.assertTrue(checks[0]["exit_locked_initially"])
                if expected:
                    self.assertEqual(checks[0]["collected"], 3)


if __name__ == "__main__":
    unittest.main()
