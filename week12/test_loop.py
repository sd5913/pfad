"""Host limits and file edits; no model is simulated by these tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import world


class LoopTests(unittest.TestCase):
    def test_missing_engine_observation_stops_instead_of_prompting_blind_repair(self):
        from loop import Session
        with tempfile.TemporaryDirectory() as folder:
            session = Session(Path(folder) / "session.json", clock=lambda: 100)
            session.start()
            with patch.object(world, "check", return_value={"returncode": 1, "passed": False, "stderr": "parse error"}):
                with self.assertRaisesRegex(RuntimeError, "structured"):
                    session.run("check")
            self.assertEqual(session.read()["status"], "blocked")

    def test_bounded_host_records_and_refuses_edits_after_check_pass(self):
        self.assertIsNotNone(importlib.util.find_spec("loop"), "bounded host is not supplied")
        from loop import Session
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            config = path / "world.json"
            config.write_text('{"speed":125,"pickup_radius":24,"exit_x":860}')
            session = Session(path / "session.json", clock=lambda: 100)
            session.start()
            with patch.object(world, "CONFIG", config):
                session.run("set", "speed", 275)
                self.assertEqual(json.loads(config.read_text())["speed"], 275)
                # Engine acceptance itself is covered by test_engine; isolate host policy here.
                with patch.object(world, "check", return_value={"passed": True, "checks": {"passed": True}}):
                    session.run("check")
                before = config.read_bytes()
                with self.assertRaisesRegex(ValueError, "passed"):
                    session.run("set", "speed", 300)
                self.assertEqual(config.read_bytes(), before)
            self.assertEqual(session.read()["actions"], 2)
            self.assertEqual(session.read()["mutations"], 1)

    def test_action_time_and_mutation_limits_refuse_before_write(self):
        self.assertIsNotNone(importlib.util.find_spec("loop"), "bounded host is not supplied")
        from loop import Session
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            config = path / "world.json"
            config.write_text('{"speed":125,"pickup_radius":24,"exit_x":860}')
            now = [0]
            session = Session(path / "session.json", clock=lambda: now[0])
            session.start()
            with patch.object(world, "CONFIG", config):
                for speed in [150, 175, 200, 225]:
                    session.run("set", "speed", speed)
                before = config.read_bytes()
                with self.assertRaisesRegex(ValueError, "mutation"):
                    session.run("set", "speed", 275)
                self.assertEqual(config.read_bytes(), before)
            session.stop("test complete")
            session.start()
            now[0] = 181
            with self.assertRaisesRegex(ValueError, "time"):
                session.run("inspect")
            session.stop("timeout observed")
            session.start()
            with patch.object(world, "inspect", return_value={"file_state_only": True}):
                for _ in range(8):
                    session.run("inspect")
            with self.assertRaisesRegex(ValueError, "action"):
                session.run("inspect")


if __name__ == "__main__":
    unittest.main()
