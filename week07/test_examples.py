# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygame==2.6.1", "watchfiles==1.3.0"]
# ///
"""Run the offline checks for the shared physics model and its views."""

from pathlib import Path
import sys
import unittest

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
suite = unittest.defaultTestLoader.discover(str(root / "week07" / "tests"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
