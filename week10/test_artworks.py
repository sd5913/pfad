"""Run with python -m unittest discover -s week10 -p 'test_*.py'."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from artworks import Artwork


SCRIPT = Path(__file__).with_name("artworks.py")


class ArtworkTests(unittest.TestCase):
    def run_demo(self, action, path, *options):
        return subprocess.run(
            [sys.executable, str(SCRIPT), action, "--file", str(path), *options],
            capture_output=True, text=True, check=False,
        )

    def test_only_one_object_changes(self):
        amber = Artwork("a1", "Amber", 2, "e1")
        blue = Artwork("a2", "Blue", 7, "e1")
        amber.view()
        self.assertEqual((amber.views, blue.views), (3, 7))

    def test_save_and_reload_in_separate_processes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "artworks.json"
            self.assertEqual(self.run_demo("save", path).returncode, 0)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual([art["id"] for art in data["artworks"]], ["a1", "a2"])
            self.assertEqual([art["views"] for art in data["artworks"]], [3, 7])
            self.assertEqual(data["exhibitions"][0]["id"], "e1")
            loaded = self.run_demo("load", path)
            self.assertEqual(loaded.returncode, 0, loaded.stderr)
            self.assertIn("After reload + view(): a1=4 (not saved)", loaded.stdout)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), data)
            self.assertIn("File exists", self.run_demo("save", path).stderr)

    def test_missing_file_and_invalid_reference(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.json"
            missing = self.run_demo("load", path)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("No such file", missing.stderr)
            broken = Path(folder) / "broken.json"
            self.assertEqual(self.run_demo("save", broken, "--broken-link").returncode, 0)
            result = self.run_demo("load", broken)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unresolved exhibition_id e99 for artwork a2", result.stderr)

    def test_duplicate_ids_are_not_valid_relationship_targets(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicates.json"
            self.assertEqual(self.run_demo("save", path).returncode, 0)
            data = json.loads(path.read_text(encoding="utf-8"))
            data["artworks"][1]["id"] = "a1"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_demo("load", path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Duplicate artwork ID a1", result.stderr)

            data["artworks"][1]["id"] = "a2"
            data["exhibitions"].append({"id": "e1", "name": "Other"})
            path.write_text(json.dumps(data), encoding="utf-8")
            result = self.run_demo("load", path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Duplicate exhibition ID e1", result.stderr)


if __name__ == "__main__":
    unittest.main()
