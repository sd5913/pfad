"""Dependency-free checks for the Week 13 loop's printed output."""

from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).with_name("loop.py")


class LoopOutputTests(unittest.TestCase):
    def run_loop(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    def test_default_limit(self):
        self.assertEqual(self.run_loop(), "0\n1\n2\ndone\n")

    def test_zero_limit(self):
        self.assertEqual(self.run_loop("0"), "done\n")


if __name__ == "__main__":
    unittest.main()
