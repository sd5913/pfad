"""Real Blender export and Godot import contract, in disposable directories."""
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent


class AssetHandoffTests(unittest.TestCase):
    def test_saved_sculpture_exports_material_size_and_floor_pivot(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            scene_script = folder / "scene.py"
            scene_script.write_text((ROOT / "blender_scene.py").read_text().replace(
                "target.scale = (options.scale, options.scale, options.scale)",
                "target.scale = (options.scale * 1.3, options.scale * 0.75, options.scale)"))
            baseline = subprocess.run([
                "blender", "--background", "--factory-startup", "-noaudio",
                "--python-exit-code", "1", "--python", str(scene_script),
                "--", "--scale", "1.25", "--output", str(folder / "before")],
                capture_output=True, text=True, timeout=90)
            self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
            source = folder / "before/sculpture.blend"
            original = source.read_bytes()
            project = folder / "preview"
            result = subprocess.run([
                sys.executable, str(ROOT / "asset_handoff.py"), "export", str(source),
                "--output", str(project)], capture_output=True, text=True, timeout=90)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(source.read_bytes(), original, "export must not rewrite the source")
            data = (project / "sculpture.glb").read_bytes()
            magic, version, length = struct.unpack_from("<4sII", data)
            self.assertEqual((magic, version, length), (b"glTF", 2, len(data)))
            json_length, chunk_type = struct.unpack_from("<I4s", data, 12)
            self.assertEqual(chunk_type, b"JSON")
            gltf = json.loads(data[20:20 + json_length])
            self.assertEqual([node["name"] for node in gltf["nodes"]], ["Sculpture"])
            self.assertEqual(len(gltf["meshes"]), 1)
            self.assertEqual(gltf["materials"][0]["name"], "Terracotta")
            self.assertFalse(gltf.get("cameras"))
            checked = subprocess.run([
                sys.executable, str(ROOT / "asset_handoff.py"), "check", "--output", str(project)],
                capture_output=True, text=True, timeout=90)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            report = json.loads((project / "check.json").read_text())
            self.assertTrue(report["passed"])
            self.assertEqual(report["mesh_count"], 1)
            self.assertEqual(report["size"], [3.25, 2.5, 1.875])
            self.assertAlmostEqual(report["bottom_y"], 0, places=5)
            self.assertTrue(report["terracotta"])
            (project / "sculpture.glb").unlink()
            failed = subprocess.run([
                sys.executable, str(ROOT / "asset_handoff.py"), "check", "--output", str(project)],
                capture_output=True, text=True, timeout=30)
            self.assertNotEqual(failed.returncode, 0)

    def test_missing_source_fails_without_creating_project(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder) / "preview"
            result = subprocess.run([
                sys.executable, str(ROOT / "asset_handoff.py"), "export", str(Path(folder) / "missing.blend"),
                "--output", str(project)], capture_output=True, text=True, timeout=30)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Source .blend not found", result.stdout + result.stderr)
            self.assertFalse(project.exists())
