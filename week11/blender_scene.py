"""Run INSIDE Blender: build a disposable scene, inspect/change/save/render it."""
import argparse
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

args = argparse.ArgumentParser()
args.add_argument("--scale", type=float, default=1.0)
args.add_argument("--target", default="Sculpture")
args.add_argument("--output", default=str(Path(__file__).resolve().parent / ".output/blender"))
options = args.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
if not 0.5 <= options.scale <= 2.0:
    raise ValueError("scale must be between 0.5 and 2.0")
output = Path(options.output).resolve()
output.mkdir(parents=True, exist_ok=True)
for existing in list(bpy.data.objects):
    bpy.data.objects.remove(existing, do_unlink=True)
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
sculpture = bpy.context.object
sculpture.name = "Sculpture"
material = bpy.data.materials.new("Terracotta")
material.diffuse_color = (0.8, 0.22, 0.08, 1)
material.use_nodes = True
material.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.8, 0.22, 0.08, 1)
sculpture.data.materials.append(material)
bpy.ops.mesh.primitive_plane_add(size=200)
floor = bpy.context.object
floor.name = "Floor"
bpy.ops.object.camera_add(location=(7, -9, 6))
camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, 1.1)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = camera
bpy.ops.object.light_add(type='AREA', location=(1, -3, 7))
bpy.context.object.data.energy = 1500
bpy.context.object.data.shape = 'DISK'
bpy.context.object.data.size = 5
target = bpy.data.objects.get(options.target)
if target is None:
    raise ValueError(f"Missing object: {options.target}; use Sculpture")
before = list(target.scale)
target.scale = (options.scale, options.scale, options.scale)
target.location.z = options.scale
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 8
scene.render.resolution_x = 640
scene.render.resolution_y = 480
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(output / f"sculpture-{options.scale:g}.png")
bpy.ops.wm.save_as_mainfile(filepath=str(output / "sculpture.blend"))
bpy.ops.render.render(write_still=True)
evidence = {"application":bpy.app.version_string, "target":target.name, "before":before,
    "after":list(target.scale), "render":scene.render.filepath, "saved_scene":bpy.data.filepath}
(output / "inspect.json").write_text(json.dumps(evidence, indent=2))
print("BLENDER_CHECK " + json.dumps(evidence))
