"""Smoke checks for the state change and the command shown in the lesson."""

import subprocess
import sys
import unittest
from pathlib import Path

from tile_demo import Tile


class TileDemoTest(unittest.TestCase):
    def test_choosing_blue_does_not_choose_red(self):
        blue = Tile("blue")
        red = Tile("red")
        self.assertEqual((blue.colour, red.colour), ("blue", "red"))
        self.assertFalse(blue.selected)
        self.assertFalse(red.selected)

        blue.choose()

        self.assertTrue(blue.selected)
        self.assertFalse(red.selected)

    def test_script_prints_expected_trace(self):
        script = Path(__file__).with_name("tile_demo.py")
        result = subprocess.run(
            [sys.executable, "-B", str(script)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            result.stdout.splitlines(),
            ["Before: blue=False, red=False", "After:  blue=True, red=False"],
        )
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
