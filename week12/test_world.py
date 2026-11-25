"""Behavior checks for the bounded Python/application boundary."""
import tempfile
import unittest
from pathlib import Path

from world import load_config, update_config


class ConfigTests(unittest.TestCase):
    def test_update_keeps_other_values_and_rejects_invalid_without_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "world.json"
            target.write_text('{"speed":180,"pickup_radius":24,"exit_x":700}')
            update_config(target, "speed", 240)
            self.assertEqual(load_config(target)["speed"], 240)
            before = target.read_bytes()
            for key, value in [("speed", -1), ("exit_x", 2000), ("pickup_radius", True), ("script", 5),
                               ("speed", float("nan")), ("speed", float("inf")), ("speed", "275")]:
                with self.assertRaises(ValueError):
                    update_config(target, key, value)
                self.assertEqual(target.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
