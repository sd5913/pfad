"""Exercise actual Godot state transitions in disposable starter copies."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from world import PROJECT, engine


class GodotTests(unittest.TestCase):
    def test_fixed_frame_replay_reaches_completion_using_shared_behavior(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder) / "godot"
            shutil.copytree(PROJECT, project, ignore=shutil.ignore_patterns(".godot"))
            (project / "world.json").write_text('{"speed":275,"pickup_radius":24,"exit_x":860}')
            result = subprocess.run(
                [engine(), "--headless", "--path", str(project), "--fixed-fps", "30",
                 "--quit-after", "120", "--", "--replay"],
                capture_output=True, text=True, timeout=15,
                env={**os.environ, "XDG_DATA_HOME": str(Path(folder) / "data")})
            self.assertEqual(result.returncode, 0, result.stderr)
            completions = [json.loads(line.removeprefix("WORLD_REPLAY "))
                           for line in result.stdout.splitlines() if line.startswith("WORLD_REPLAY ")]
            self.assertEqual(len(completions), 1, result.stdout + result.stderr)
            self.assertEqual(completions[0]["collected"], 3)
            self.assertEqual(completions[0]["ticks"], 166)
            self.assertTrue(completions[0]["won"])

    def test_fail_adapt_stop_and_exit_rejects_incomplete_collection(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder) / "godot"
            shutil.copytree(PROJECT, project, ignore=shutil.ignore_patterns(".godot"))
            config_path = project / "world.json"
            for speed, expected in [(125, False), (275, True), (60, False), (480, True)]:
                with self.subTest(speed=speed):
                    config_path.write_text(json.dumps({"speed": speed, "pickup_radius": 24, "exit_x": 860}))
                    result = subprocess.run(
                        [engine(), "--headless", "--path", str(project), "--script", "res://check_world.gd"],
                        capture_output=True, text=True, timeout=15,
                        env={**os.environ, "XDG_DATA_HOME": str(Path(folder) / "data")})
                    reports = [json.loads(line[12:]) for line in result.stdout.splitlines()
                               if line.startswith("WORLD_CHECK ")]
                    self.assertEqual(len(reports), 1, result.stderr)
                    report = reports[0]
                    self.assertEqual(report["passed"], expected, report)
                    self.assertEqual(result.returncode, 0 if expected else 1, result.stderr)
                    self.assertTrue(report.get("premature_exit_rejected"), report)
                    self.assertEqual(report.get("premature_exit_cases"), [0, 1, 2])
                    self.assertLessEqual(report["ticks"], 180)
                    if expected:
                        self.assertEqual(report["collected"], 3)
                        self.assertTrue(report["won_by_180_frames"])
                        self.assertTrue(report["stopped_after_win"])
                    elif speed == 125:
                        self.assertEqual(report["collected"], 2)
                        self.assertAlmostEqual(report["player_x"], 455, places=2)


if __name__ == "__main__":
    unittest.main()
