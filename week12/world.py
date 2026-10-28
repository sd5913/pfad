"""Course-owned Godot config/check/capture adapter; no model calls."""
import argparse
import hashlib
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


def load_config(path=None):
    return json.loads(Path(path or CONFIG).read_text())


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
    try:
        result = subprocess.run([engine(), "--path", str(PROJECT), *args], capture_output=True, text=True, timeout=timeout, env=environment)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"Godot exceeded {timeout}s and was stopped; inspect the project and engine logs") from error
    return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def inspect():
    return {"project":str(PROJECT), "scene":"World (Node2D)", "config":load_config(),
            "pickups":[240,420,600], "player_start":[80,300], "file_state_only":True}


def check():
    result = execute(["--headless", "--script", "res://check_world.gd"], timeout=15)
    for line in result["stdout"].splitlines():
        if line.startswith("WORLD_CHECK "):
            result["checks"] = json.loads(line.removeprefix("WORLD_CHECK "))
    result["passed"] = result["returncode"] == 0 and result.get("checks", {}).get("passed", False)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "check.json").write_text(json.dumps(result, indent=2))
    return result


def validate_movie(probe):
    videos = [item for item in probe.get("streams", []) if item.get("codec_type") == "video"]
    if len(videos) != 1:
        raise ValueError("expected exactly one video stream")
    video = videos[0]
    if (video.get("width"), video.get("height")) != (960, 540):
        raise ValueError("expected a 960x540 clip")
    if not 3.9 <= float(probe.get("format", {}).get("duration", 0)) <= 4.1:
        raise ValueError("expected about four seconds")
    if int(video.get("nb_frames", 0)) != 120:
        raise ValueError("expected 120 frames")


def capture():
    OUTPUT.mkdir(exist_ok=True)
    movie = OUTPUT / "world.avi"
    clip = OUTPUT / "world.mp4"
    for path in (movie, clip, OUTPUT / "capture.json", *OUTPUT.glob("frame-*.png")):
        path.unlink(missing_ok=True)
    if not check()["passed"]:
        raise RuntimeError("behavior check failed; adapt and check before filming")
    result = execute(["--write-movie", str(movie), "--fixed-fps", "30", "--quit-after", "120", "--", "--replay"], timeout=90)
    if result["returncode"] != 0 or not movie.exists():
        raise RuntimeError(f"capture failed: {result}")
    completions = [json.loads(line.removeprefix("WORLD_REPLAY "))
                   for line in result["stdout"].splitlines() if line.startswith("WORLD_REPLAY ")]
    if len(completions) != 1 or not completions[0]["won"] or completions[0]["collected"] != 3 or completions[0]["ticks"] > 180:
        raise RuntimeError("capture run did not report the checked completion within 180 ticks")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(movie), "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(clip)], check=True, timeout=60)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,nb_frames", "-of", "json", str(clip)], capture_output=True, text=True, check=True, timeout=15)
    metadata = json.loads(probe.stdout)
    validate_movie(metadata)
    subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(clip), "-f", "null", "-"], check=True, timeout=30, capture_output=True)
    samples = []
    for name, second in [("start", 0), ("middle", 1.5), ("end", 3.9)]:
        image = OUTPUT / f"frame-{name}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(second), "-i", str(clip), "-frames:v", "1", str(image)], check=True, timeout=15)
        samples.append({"path": str(image), "sha256": hashlib.sha256(image.read_bytes()).hexdigest()})
    report = {"clip":str(clip), "probe":metadata, "capture":result, "decoded_all_frames":True,
              "samples":samples, "visual_inspection_required":True,
              "config":load_config(), "config_sha256":hashlib.sha256(CONFIG.read_bytes()).hexdigest()}
    (OUTPUT / "capture.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "set", "check", "play", "replay", "capture"])
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
        OUTPUT.mkdir(exist_ok=True)
        subprocess.run([engine(), "--path", str(PROJECT), *(["--", "--replay"] if args.action == "replay" else [])], check=True, timeout=300,
                       env={**os.environ, "XDG_DATA_HOME":str(OUTPUT / "data")})
        return
    print(json.dumps(result, indent=2))
    if args.action == "check" and not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        OUTPUT.mkdir(exist_ok=True)
        (OUTPUT / "last-error.json").write_text(json.dumps({"error": str(error)}, indent=2) + "\n")
        raise SystemExit(f"world tool failed: {error}")
