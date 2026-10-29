"""Course-owned Godot config/check/capture adapter; no model calls."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "godot"
CONFIG = PROJECT / "world.json"
OUTPUT = ROOT / ".output"
BOUNDS = {"speed": (60, 480), "pickup_radius": (8, 48), "exit_x": (720, 880)}


def load_config(path=CONFIG):
    return json.loads(Path(path).read_text())


def update_config(path, key, value):
    if key not in BOUNDS or type(value) not in (int, float):
        raise ValueError("choose speed, pickup_radius or exit_x and a finite number")
    low, high = BOUNDS[key]
    if not low <= value <= high:
        raise ValueError(f"{key} must be between {low} and {high}")
    config = load_config(path)
    config[key] = value
    Path(path).write_text(json.dumps(config, indent=2) + "\n")
    return config


def engine():
    choice = os.environ.get("GODOT_PATH") or shutil.which("godot") or shutil.which("godot4")
    if not choice:
        raise RuntimeError("Godot missing: set GODOT_PATH to the standard Godot 4 executable")
    return choice


def execute(args, timeout=60):
    OUTPUT.mkdir(exist_ok=True)
    environment = {**os.environ, "XDG_DATA_HOME":str(OUTPUT / "data")}
    result = subprocess.run([engine(), "--path", str(PROJECT), *args], capture_output=True, text=True, timeout=timeout, env=environment)
    return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def inspect():
    return {"project":str(PROJECT), "scene":"World (Node2D)", "config":load_config(),
            "pickups":[240,420,600], "player_start":[80,300], "file_state_only":True}


def check():
    result = execute(["--headless", "--script", "res://check_world.gd", "--quit-after", "2"], timeout=15)
    for line in result["stdout"].splitlines():
        if line.startswith("WORLD_CHECK "):
            result["checks"] = json.loads(line.removeprefix("WORLD_CHECK "))
    result["passed"] = result["returncode"] == 0 and result.get("checks", {}).get("passed", False)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "check.json").write_text(json.dumps(result, indent=2))
    return result


def capture():
    OUTPUT.mkdir(exist_ok=True)
    movie = OUTPUT / "world.avi"
    result = execute(["--write-movie", str(movie), "--fixed-fps", "30", "--quit-after", "120", "--", "--replay"], timeout=90)
    if result["returncode"] != 0 or not movie.exists():
        raise RuntimeError(f"capture failed: {result}")
    clip = OUTPUT / "world.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(movie), "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(clip)], check=True, timeout=60)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height,nb_frames", "-of", "json", str(clip)], capture_output=True, text=True, check=True)
    return {"clip":str(clip), "probe":json.loads(probe.stdout), "capture":result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "set", "check", "play", "capture"])
    parser.add_argument("key", nargs="?")
    parser.add_argument("value", nargs="?", type=float)
    args = parser.parse_args()
    if args.action == "inspect":
        result = inspect()
    elif args.action == "set":
        result = update_config(CONFIG, args.key, args.value)
    elif args.action == "check":
        result = check()
    elif args.action == "capture":
        result = capture()
    else:
        subprocess.run([engine(), "--path", str(PROJECT)], check=True)
        return
    print(json.dumps(result, indent=2))
    if args.action == "check" and not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
