"""Run inside a disposable GUI Blender process; the upstream add-on stays local."""
import importlib.util
import json
import os
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pfad_blender_addon", ROOT / ".tools/blender-addon.py")
addon = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = addon
spec.loader.exec_module(addon)
addon.register()
bpy.context.scene.blendermcp_auto_start_server = False
server = addon.BlenderMCPServer(host="127.0.0.1", port=int(os.environ["PFAD_BLENDER_PORT"]))
bpy.types.blendermcp_server = server
server.start()
if not server.running:
    raise RuntimeError("Could not start the disposable Blender bridge")
(ROOT / ".output/blender-live-ready.json").write_text(json.dumps({"port":server.port, "running":server.running}))


def stop_when_requested():
    if (ROOT / ".output/blender-live-stop").exists():
        server.stop()
        addon.unregister()
        bpy.ops.wm.quit_blender()
        return None
    return 0.1


bpy.app.timers.register(stop_when_requested, first_interval=0.1)
