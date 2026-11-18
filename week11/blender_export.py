"""Run inside Blender: export only Sculpture from a saved scene, without resaving it."""
import argparse
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", required=True)
parser.add_argument("--output", required=True)
options = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
bpy.ops.wm.open_mainfile(filepath=str(Path(options.source).resolve()))
target = bpy.data.objects.get("Sculpture")
if target is None or target.type != "MESH":
    raise ValueError("Saved scene must contain a mesh named Sculpture")
bpy.ops.object.select_all(action="DESELECT")
target.select_set(True)
bpy.context.view_layer.objects.active = target
corners = [target.matrix_world @ Vector(corner) for corner in target.bound_box]
bottom = min(corner.z for corner in corners)
if abs(bottom) > 0.001:
    raise ValueError(f"Sculpture must touch the Blender floor z=0; bottom is {bottom}")
# Change only the export copy: the pivot sits beneath the object's centre.
bpy.context.scene.cursor.location = (target.location.x, target.location.y, bottom)
bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
target.location = (0, 0, 0)
output = Path(options.output).resolve()
output.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(output), export_format="GLB", use_selection=True,
                          export_yup=True, export_materials="EXPORT")
print("ASSET_EXPORT " + json.dumps({"blender": bpy.app.version_string,
      "source": str(Path(options.source).resolve()), "object": target.name,
      "dimensions": list(target.dimensions), "source_bottom_z": bottom,
      "pivot": "bottom centre", "output": str(output)}))
