"""Course-owned bounded MCP stdio adapter for Blender CLI, not Blender MCP."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def call(name, arguments):
    if name == "inspect_scene":
        source = ROOT / ".output/blender/inspect.json"
        if not source.exists():
            raise ValueError("render_scene first; no saved inspection exists")
        return json.loads(source.read_text())
    if name != "render_scene":
        raise ValueError("unknown tool")
    scale = arguments.get("scale", 1.0)
    if type(scale) not in (int, float) or not 0.5 <= scale <= 2:
        raise ValueError("scale must be a finite number between 0.5 and 2")
    environment = {**os.environ, "BLENDER_USER_CONFIG":str(ROOT / ".output/blender-config"), "XDG_CACHE_HOME":str(ROOT / ".output/cache")}
    result = subprocess.run(["blender", "--background", "--factory-startup", "-noaudio", "--python-exit-code", "1",
        "--python", str(ROOT / "blender_scene.py"), "--", "--scale", str(scale)], capture_output=True, text=True, timeout=90, env=environment)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:] or result.stdout[-2000:])
    return call("inspect_scene", {})


def respond(request):
    method = request["method"]
    if method == "initialize":
        return {"protocolVersion":"2024-11-05", "capabilities":{"tools":{}}, "serverInfo":{"name":"pfad-blender-cli", "version":"1.0"}}
    if method == "tools/list":
        return {"tools":[{"name":"inspect_scene", "description":"Read the saved scene inspection, not live editor state", "inputSchema":{"type":"object","properties":{}}},
            {"name":"render_scene", "description":"Build, scale, save and CPU-render the disposable Sculpture scene", "inputSchema":{"type":"object","properties":{"scale":{"type":"number","minimum":0.5,"maximum":2}},"required":["scale"]}}]}
    if method == "tools/call":
        params = request["params"]
        try:
            evidence = call(params["name"], params.get("arguments", {}))
            return {"content":[{"type":"text", "text":json.dumps(evidence)}], "isError":False}
        except (ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
            return {"content":[{"type":"text", "text":str(error)}], "isError":True}
    raise ValueError("unsupported method")


if __name__ == "__main__":
    for line in sys.stdin:
        request = json.loads(line)
        if "id" not in request:
            continue
        try:
            message = {"result":respond(request)}
        except ValueError as error:
            message = {"error":{"code":-32601,"message":str(error)}}
        print(json.dumps({"jsonrpc":"2.0", "id":request["id"], **message}), flush=True)
