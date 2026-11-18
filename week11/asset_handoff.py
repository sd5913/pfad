"""Export the saved Blender sculpture, then import/check/play/capture it in Godot 3D."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

from world import engine

ROOT = Path(__file__).resolve().parent
DEFAULT_PROJECT = ROOT / ".output/godot3d"


def run(command, project, timeout=90):
    environment = {**os.environ, "XDG_DATA_HOME": str(project / ".data"),
                   "XDG_CACHE_HOME": str(project / ".cache")}
    result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=timeout)
    if result.returncode or "SCRIPT ERROR:" in result.stderr:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def export(source, project):
    if not source.is_file():
        raise ValueError(f"Source .blend not found: {source}; run blender_scene.py first")
    project.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "godot3d", project, dirs_exist_ok=True)
    output = run(["blender", "--background", "--factory-startup", "-noaudio",
                  "--python-exit-code", "1", "--python", str(ROOT / "blender_export.py"),
                  "--", "--source", str(source), "--output", str(project / "sculpture.glb")], project)
    record = next(json.loads(line.removeprefix("ASSET_EXPORT "))
                  for line in output.splitlines() if line.startswith("ASSET_EXPORT "))
    (project / "export.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def check(project):
    if not (project / "sculpture.glb").is_file():
        raise ValueError("Missing sculpture.glb; export the saved Blender scene first")
    run([engine(), "--headless", "--path", str(project), "--editor", "--import"], project)
    output = run([engine(), "--headless", "--path", str(project), "--script",
                  "res://check_asset.gd"], project)
    record = next(json.loads(line.removeprefix("ASSET_CHECK "))
                  for line in output.splitlines() if line.startswith("ASSET_CHECK "))
    source = json.loads((project / "export.json").read_text())
    x, y, z = source["dimensions"]
    record["matches_source_dimensions"] = all(
        abs(actual - expected) < 0.001 for actual, expected in zip(record["size"], [x, z, y]))
    record["passed"] = record["passed"] and record["matches_source_dimensions"]
    (project / "check.json").write_text(json.dumps(record, indent=2) + "\n")
    if not record["passed"]:
        raise RuntimeError(f"Godot asset check failed: {record}")
    return record


def capture(project):
    check(project)
    image = project.parent / "godot3d-preview.png"
    # A headless renderer cannot draw; Linux capture uses an isolated X display.
    command = [engine(), "--path", str(project), "--write-movie", str(image),
               "--fixed-fps", "1", "--quit-after", "1"]
    if shutil.which("xvfb-run"):
        command = ["xvfb-run", "-a", *command]
    run(command, project)
    frame = image.with_name(image.stem + "00000000.png")
    if not frame.is_file():
        raise RuntimeError(f"Godot did not write the expected movie frame: {frame}")
    frame.replace(image)
    return {"image": str(image), "method": "Godot movie PNG frame; actual 3D renderer"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["export", "check", "play", "capture"])
    parser.add_argument("source", nargs="?", type=Path,
                        default=ROOT / ".output/blender/before/sculpture.blend")
    parser.add_argument("--output", type=Path, default=DEFAULT_PROJECT)
    args = parser.parse_args()
    project = args.output.resolve()
    try:
        if args.action == "export":
            result = export(args.source.resolve(), project)
        elif args.action == "check":
            result = check(project)
        elif args.action == "capture":
            result = capture(project)
        else:
            check(project)
            subprocess.run([engine(), "--path", str(project)], check=True)
            return
        print(json.dumps(result, indent=2))
    except (ValueError, RuntimeError, subprocess.SubprocessError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
