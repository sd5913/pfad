"""Human-directed real MCP for Blender scene/change/render/stop demonstration."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

from mcp_client import Session

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / ".output"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Render a checked variant and close automatically")
    parser.add_argument("--scale", type=float, default=1.5)
    options = parser.parse_args()
    if not 0.5 <= options.scale <= 2:
        parser.error("scale must be a finite number between 0.5 and 2")
    OUTPUT.mkdir(exist_ok=True)
    environment = {**os.environ, "BLENDER_USER_CONFIG":str(OUTPUT / "blender-config"),
                   "XDG_CACHE_HOME":str(OUTPUT / "cache"), "XDG_DATA_HOME":str(OUTPUT / "data"),
                   "BLENDER_MCP_DISABLE_TELEMETRY":"1", "BLENDERMCP_NO_UPDATE_CHECK":"1"}
    addon = ROOT / ".tools/blender-addon.py"
    bridge_python = ROOT / ".tools/blender-env" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not addon.exists() or not bridge_python.exists():
        raise SystemExit("Run uv run python setup_blender.py first.")
    baseline = OUTPUT / "blender/sculpture.blend"
    build = subprocess.run(["blender", "--background", "--factory-startup", "-noaudio", "--python-exit-code", "1",
        "--python", str(ROOT / "blender_scene.py")], capture_output=True, text=True, env=environment, timeout=60)
    if build.returncode:
        raise RuntimeError(build.stderr + build.stdout)
    with socket.socket() as chooser:
        chooser.bind(("127.0.0.1", 0))
        port = chooser.getsockname()[1]
    environment["PFAD_BLENDER_PORT"] = str(port)
    ready, stop = OUTPUT / "blender-live-ready.json", OUTPUT / "blender-live-stop"
    ready.unlink(missing_ok=True)
    stop.unlink(missing_ok=True)
    render = OUTPUT / "blender/sculpture-live.png"
    result_path = OUTPUT / "blender-live-inspection.json"
    render.unlink(missing_ok=True)
    result_path.unlink(missing_ok=True)
    log = (OUTPUT / "blender-live.log").open("w")
    application = subprocess.Popen(["blender", "--factory-startup", "-noaudio", str(baseline),
        "--python-exit-code", "1", "--python", str(ROOT / "blender_addon_boot.py")], env=environment, stdout=log, stderr=log)
    session = None
    trace = []
    try:
        deadline = time.monotonic() + 30
        while not ready.exists():
            if application.poll() is not None or time.monotonic() > deadline:
                raise RuntimeError("Blender bridge startup failed; see .output/blender-live.log")
            time.sleep(0.1)
        command = [str(bridge_python), "-m", "blender_mcp.server", "--host", "127.0.0.1", "--port", str(port)]
        # The SDK server reads telemetry settings before connecting to Blender.
        session = Session(command, env={"BLENDER_MCP_DISABLE_TELEMETRY":"1", "BLENDER_MCP_CONTEXT_LOG":"0"})
        session.request("initialize", {"protocolVersion":"2024-11-05", "capabilities":{}, "clientInfo":{"name":"pfad-creative-demo", "version":"1"}})
        session.send({"method":"notifications/initialized"})
        tools = [tool["name"] for tool in session.request("tools/list")["tools"]]
        for name, arguments in [("get_scene_info", {"query":"Sculpture", "fields":["scale"]}),
            ("execute_blender_code", {"code":f"import bpy\nobj = bpy.data.objects['Sculpture']\nobj.scale = ({options.scale}, {options.scale}, {options.scale})\nobj.location.z = {options.scale}\nprint(list(obj.scale))"}),
            ("get_scene_info", {"query":"Sculpture", "fields":["scale"]})]:
            response = session.request("tools/call", {"name":name, "arguments":arguments})
            trace.append({"tool":name, "arguments":arguments, "response":response})
            if response.get("isError"):
                raise RuntimeError(response)
        code = ("import bpy, json\n" + f"bpy.context.scene.render.filepath = {str(render)!r}\n" +
            "bpy.ops.render.render(write_still=True)\n" + f"bpy.ops.wm.save_as_mainfile(filepath={str(OUTPUT / 'blender/sculpture-live.blend')!r})\n" +
            f"with open({str(result_path)!r}, 'w') as handle:\n    json.dump({{'scale':list(bpy.data.objects['Sculpture'].scale)}}, handle)\n")
        response = session.request("tools/call", {"name":"execute_blender_code", "arguments":{"code":code}})
        trace.append({"tool":"execute_blender_code", "response":response})
        if response.get("isError") or not render.exists() or not result_path.exists():
            raise RuntimeError(response)
        if not options.verify:
            input("Inspect Sculpture in Blender, then press Enter here to close this disposable session. ")
    finally:
        if session:
            session.close()
        stop.touch()
        try:
            application.wait(timeout=15)
        except subprocess.TimeoutExpired:
            application.terminate()
            application.wait(timeout=5)
        log.close()
        (OUTPUT / "blender-live-trace.json").write_text(json.dumps(trace, indent=2))
    with socket.socket() as probe:
        closed = probe.connect_ex(("127.0.0.1", port)) != 0
    result = {**json.loads(result_path.read_text()), "tools":tools, "render":str(render),
              "blender_exit":application.returncode, "socket_closed":closed, "port":port}
    (OUTPUT / "blender-live-result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    if application.returncode or not closed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
