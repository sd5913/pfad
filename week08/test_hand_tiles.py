"""Offline tests: no imports of camera packages, device or network."""

import subprocess
import sys
import unittest
from pathlib import Path

from hand_tiles import SAMPLE_X, tile_for_x, tile_line


class HandTilesTest(unittest.TestCase):
    def test_mapping_edges_and_missing_input(self):
        self.assertEqual(tile_for_x(0), "blue")
        self.assertEqual(tile_for_x(0.499), "blue")
        self.assertEqual(tile_for_x(0.5), "red")
        self.assertEqual(tile_for_x(1), "red")
        for bad in (None, -0.01, 1.01, float("nan"), float("inf"), "0.2"):
            with self.subTest(bad=bad):
                self.assertIsNone(tile_for_x(bad))
                self.assertIn("no input", tile_line(bad))

    def test_one_tile_highlight_only(self):
        self.assertEqual(tile_line(0.2), "[ BLUE ]    red    (blue)")
        self.assertEqual(tile_line(0.8), "  blue    [ RED ]  (red)")
        self.assertEqual(tile_line(None), "  blue      red    (no input)")

    def test_sample_command_is_deterministic(self):
        script = Path(__file__).with_name("hand_tiles.py")
        run = subprocess.run([sys.executable, "-B", str(script)],
                             capture_output=True, text=True, check=True)
        self.assertEqual(run.stdout.splitlines(), [
            "Sample coordinates (not camera images and not MediaPipe output):",
            *(f"x={x!s:>4} -> {tile_line(x)}" for x in SAMPLE_X),
        ])
        self.assertEqual(run.stderr, "")

    def test_camera_cannot_start_without_explicit_model(self):
        script = Path(__file__).with_name("hand_tiles.py")
        run = subprocess.run([sys.executable, "-B", str(script), "--camera"],
                             capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("requires --model", run.stderr)


if __name__ == "__main__":
    unittest.main()
