"""Install the pinned community Godot source into this week's ignored folder."""
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent
COMMIT = "1209744fad78f3998f98c7394fd0f6ef50da5281"
DEST = ROOT / ".tools/godot-mcp"

if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    for source, target in [("src/index.ts", "index.ts"), ("src/scripts/godot_operations.gd", "scripts/godot_operations.gd"), ("LICENSE", "LICENSE")]:
        output = DEST / target
        output.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://raw.githubusercontent.com/Coding-Solo/godot-mcp/{COMMIT}/{source}"
        with urllib.request.urlopen(url, timeout=30) as response:
            output.write_bytes(response.read())
    (DEST / "package.json").write_text(json.dumps({"private":True, "type":"module", "dependencies":{"@modelcontextprotocol/sdk":"1.30.0"}}))
    subprocess.run(["npm", "install", "--ignore-scripts", "--no-audit", "--no-fund"], cwd=DEST, check=True)
    print("Pinned source installed. SDK 1.30 is a course compatibility update to upstream 0.6.")
