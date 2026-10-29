"""Render two controlled camera variants using separate disposable Blender runs."""
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / ".output"


if __name__ == "__main__":
    environment = {**os.environ, "BLENDER_USER_CONFIG":str(OUTPUT / "blender-config"),
                   "XDG_CACHE_HOME":str(OUTPUT / "cache")}
    for number, (x, y) in enumerate([(7, -9), (9, -7)], start=1):
        folder = OUTPUT / "blender" / f"angle-{number}"
        subprocess.run(["blender", "--background", "--factory-startup", "-noaudio",
            "--python-exit-code", "1", "--python", str(ROOT / "blender_scene.py"), "--",
            "--scale", "1.25", "--camera-x", str(x), "--camera-y", str(y),
            "--output", str(folder)], check=True, env=environment, timeout=60)
        print(f"Camera {number}: ({x}, {y}, 6); inspect {folder}")
