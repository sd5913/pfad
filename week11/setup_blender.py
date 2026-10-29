"""Install the community bridge locally; never alter global Blender/client config."""
from pathlib import Path
import os
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent
COMMIT = "8782963ba87a4c90482198bd7c7e17219ac3a0f7"


if __name__ == "__main__":
    target = ROOT / ".tools/blender-addon.py"
    target.parent.mkdir(exist_ok=True)
    for source, name in [("addon.py", "blender-addon.py"), ("LICENSE", "blender-addon-LICENSE")]:
        url = f"https://raw.githubusercontent.com/ahujasid/mcp-for-blender/{COMMIT}/{source}"
        with urllib.request.urlopen(url, timeout=30) as response:
            (target.parent / name).write_bytes(response.read())
    environment = ROOT / ".tools/blender-env"
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        subprocess.run(["uv", "venv", str(environment)], check=True)
    subprocess.run(["uv", "pip", "install", "--python", str(python), "mcp-for-blender==2.2.6"], check=True)
    print("Installed mcp-for-blender 2.2.6 in .tools; no client/add-on preferences changed.")
