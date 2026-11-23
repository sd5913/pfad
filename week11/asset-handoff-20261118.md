# Blender Sculpture to Godot: actual acceptance, 18 November 2026

This record covers a prepared local rehearsal, not a captured model session.
The worksheet gives a real agent-use request; the temporary author-generated
scene variants here are deterministic examples. No model/API calls, external
deployment, OAuth login, remote class or course merge were used for this work.

## Reuse and versions

Base: PFAD `e02fd99bc51c5df2b46c89eb4491b9da591b843d`. Reused
`blender_scene.py` for the exact saved Sculpture, its material, render, scale
and floor-contact convention; retained `blender_variants.py`, community bridge
and `world.py` unchanged. The new Python helper reuses `world.engine()` for
Godot discovery. The existing `godot/` is a Node2D game: a MeshInstance3D
needs a Node3D scene, so the added `godot3d/` preview is separate. The Week 12
bounded world/check/revise/film lesson and preparation appendix remain intact.
The OAuth template stays at `69cbed7363412daa4a7e8c2c8fc4ed02a3f1afa5`;
only its existing UI was inspected to correct the worksheet task.

Tested on Linux x86_64: Blender **5.3.0**, build `02f0899d78e3` dated
11 November; Godot **4.7.2.stable.arch_linux.ed1daf0bf**; uv **0.13.8**.
Blender's earlier 5.2.3 LTS acceptance is historical, recorded separately.
No new bridge dependency was introduced. Context7 retrieved current official
Blender export and Godot import/movie/color docs on 18 November:

- [Blender export operator](https://docs.blender.org/api/current/bpy.ops.export_scene.html)
- [Blender glTF export](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html)
- [Godot 3D import](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/index.html)
- [Godot command line/movie](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [Godot Color encodings](https://docs.godotengine.org/en/stable/classes/class_color.html)

Geometry is original course code. No external meshes/textures were downloaded.
Blender is GPL-licensed; Godot is MIT-licensed. Exported geometry/materials
and the new course source introduce no third-party asset obligations.

## Commands and observed results

From `week11/`, all these commands succeeded with exit 0:

```bash
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.25 --output .output/blender/before
uv run python asset_handoff.py export .output/blender/before/sculpture.blend
uv run python asset_handoff.py check
uv run python asset_handoff.py capture
```

The baseline source reports scale `[1.25,1.25,1.25]`, dimensions
`[2.5,2.5,2.5]`, centre z 1.25 and camera `[7,-9,6]`. Export selects only
the named Sculpture mesh, bakes its scale into vertices and gives the export
copy a bottom-centre pivot. It does not save over the source `.blend`.
glTF's built-in axis conversion changes Blender Z-up into Godot Y-up;
the preview applies no compensating rotation. Floor/camera/light are excluded
from GLB and supplied by Godot instead.

For the worksheet's first/revised examples, temporary copies of the same
scene script replaced only the uniform `target.scale` assignment. The tracked
scene code remains untouched. These are rehearsed edits, not agent transcripts:

```bash
blender --background --factory-startup -noaudio --python-exit-code 1 --python .output/blender-first.py -- --scale 1.25 --output .output/blender/first
blender --background --factory-startup -noaudio --python-exit-code 1 --python .output/blender-revised.py -- --scale 1.25 --output .output/blender/revised
uv run python asset_handoff.py export .output/blender/revised/sculpture.blend --output .output/godot3d-revised
uv run python asset_handoff.py capture --output .output/godot3d-revised
```

| Observation | Baseline | First | Revised |
| --- | --- | --- | --- |
| Blender scale | 1.25, 1.25, 1.25 | 2, 0.9375, 1.25 | 1.625, 0.9375, 1.25 |
| Blender dimensions | 2.5, 2.5, 2.5 | 4, 1.875, 2.5 | 3.25, 1.875, 2.5 |
| Source bottom z | 0 | 0 | 0 |
| Godot dimensions | 2.5, 2.5, 2.5 | Not exported | 3.25, 2.5, 1.875 |
| Godot bottom y | 0 | Not exported | -0.0000000745 (floating-point tolerance) |

Actual Godot import runs `--headless --editor --import`, then the checker
loads `preview.tscn`, instantiates the imported GLB and examines its mesh AABB
in world coordinates. It verifies one mesh, floor contact, positive size and
Terracotta. The Python check compares dimensions with the exported source
manifest, including the Y/Z swap. Instance position is `[0,0,0]`.
Godot's albedo is sRGB `[0.9063318,0.5063865,0.3133042]`; converting to linear
recovers Blender's `[0.8,0.22,0.08]` within 0.001. This check caught the
incorrect assumption that raw values should match across color encodings.

Capture runs the actual engine at 960x720 via `--write-movie`, fixed FPS 1,
one frame, on an isolated X display (`xvfb-run -a`). The renderer log identifies
OpenGL 4.6/Mesa 26.2.7 Compatibility with llvmpipe (LLVM 23.1.4). The result
is a fresh PNG drawn by the real 3D renderer, separate from the headless check.
The movie capture also leaves an ignored WAV. Benign XIM/VSync warnings occur
under Xvfb; there are no script errors. Each capture exits after its frame;
no persistent tool server is involved.

The author opened all baseline/revised Blender and Godot PNGs. The sculpture
is uncropped, grounded, and its revised proportions are visible in both
applications. Lighting, camera, ground and rendering engines differ, so the
matching material does not mean matching pixels. `play` starts the same
scene for a student's visible check; manual window interaction/classroom
projection was not used as this acceptance evidence.

## Evidence paths

Generated artifacts stay ignored under `.output/`; the integration owner
may copy selected actual images into the lecture's documented assets:

- `.output/blender/before/sculpture-1.25.png` (640x480), `inspect.json`, `sculpture.blend`.
- `.output/blender/first/sculpture-1.25.png` (640x480), matching inspection/scene.
- `.output/blender/revised/sculpture-1.25.png` (640x480), matching inspection/scene.
- `.output/godot3d-baseline.png` (960x720), preserved baseline engine frame.
- `.output/godot3d-revised.png` (960x720), preserved revised engine frame.
- `.output/godot3d-preview.png` is the most recent capture and may be overwritten.
- `.output/godot3d-revised/sculpture.glb`, `export.json` and `check.json`.

Revised source `.blend` SHA256:
`a74d5fbc43f90d60dfa070f664fc719920280b89a425bece364ea3a7c87a1408`.
Revised GLB SHA256:
`f20ee16a31480412f7c0a5ab83c2bdd586d43b7dc75d01ef646f27d2058a46e2`.

## Tests, failures and limits

The two new meaningful export-contract tests were run **before** the helper
existed: both failed at the missing export command. After implementation,
they pass using real Blender/Godot in temporary directories. The scene fixture
uses nonuniform `[1.625,0.9375,1.25]` scale, making a missing/double axis
conversion observable; a symmetric cube alone would conceal that mistake.
Tests parse actual GLB JSON for one Sculpture mesh/material and no cameras,
prove the source `.blend` is byte-identical after export, check imported
dimensions/floor/material, reject a missing source and reject a removed GLB
even when Godot has an earlier import cached.

```bash
uv run python -m unittest discover -p 'test_*.py' -v
node --test browser/control.test.cjs
git diff --check
```

Observed: **12 Python tests pass** in 66.513 seconds, including the existing
real community bridge/Blender shutdown tests, root's two cleanup regression
cases and the retained Godot2D behavior tests. **2 browser tests pass**.
`git diff --check` passes. Existing Blender 5.3 emits a `Material.use_nodes`
deprecation warning; the render succeeds and Blender 6 compatibility is
not claimed.

Actual negative command `uv run python asset_handoff.py export
.output/blender/MISSING.blend` exits 1 with `Source .blend not found`, before
launching Blender. Earlier good artifacts are retained; they must not be
represented as output of the failed command. Recovery is to export the valid
saved scene again and rerun `check`. Missing/renamed Sculpture and a floating
source object are explicitly rejected by the exporter; those extra cases
were inspected in code, not separately exercised in this rehearsal.

Limits: only a named single mesh with the original terracotta material is in
this small contract; multi-object hierarchies, textures, animation, collisions,
Godot export packages and arbitrary third-party assets are outside it.
Windows/macOS and classroom timing/display remain untested. The source
project files are copied to `.output/godot3d` during export, so rerun export
after changing those templates. No actual live model episode or live account
login/deployment is claimed. The OAuth change remains an exercise request,
not an implemented change to the template repository.
