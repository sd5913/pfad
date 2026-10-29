# Week 11: Python controls a creative application

**Thursday 19 November 2026.** Complete **one** application path: the Godot
tiny world or the Blender scene/render alternative. Inspect a real application,
make a purposeful change, trace an MCP request and verify the result. This is
a separate 120-minute tutorial; no ClassPoint account or paid model is needed.

By the end you should distinguish source files, running application state,
a tool request and the observed result. Explain why a successful tool response
alone does not prove that an artwork is correct.

## Route and prerequisites

| Minutes | Activity |
| --- | --- |
| 0-15 | Set up one application and inspect the supplied scene |
| 15-35 | Inspect/change through the direct application API |
| 35-55 | Trace a real MCP request and check its application effect |
| 55-65 | Break |
| 65-85 | Make a purposeful change and run/render the result |
| 85-100 | Trigger a failure, diagnose it and recover |
| 100-120 | Playtest-and-feedback tutor review/project support |

Use a current standard Godot editor or Blender, [uv](https://docs.astral.sh/uv/),
and a desktop that can display the application or its output image. The latest
installed versions checked on 29 October were **Godot 4.7.2** and **Blender 5.2.3
LTS** on Linux x86_64. Use the latest stable release; rerun the checks if it
changes. Both have Windows and macOS builds, but this exercise has **not** been
rehearsed there. Choose standard Godot, not .NET. No export templates are needed
to play/record in Godot. No dedicated GPU, camera, microphone or model is required.

The community Godot bridge additionally needs **Node.js 26** and npm (tested
26.12.1); first installation needs internet. The Blender course adapter needs
only Python and Blender; the optional live community bridge adds a local Python
environment installed by the supplied setup command. `bpy` runs inside Blender's Python, not uv's Python.
Do not install `bpy` into this weekly environment.

From the PFAD repository root:

```bash
cd week11
uv run python -m unittest test_world test_mcp_transport
```

Keep this directory for all commands. uv uses its separate environment and
lockfile. Godot must be named `godot`/`godot4` on PATH, or set `GODOT_PATH` to
its full executable path. In Bash/zsh: `export GODOT_PATH='/path/to/Godot'`.
In PowerShell: `$env:GODOT_PATH = 'C:/Tools/Godot/Godot.exe'`.
Check Blender with `blender --version`; add its executable directory to PATH
if missing. On macOS this is commonly
`/Applications/Blender.app/Contents/MacOS/`.

If you cannot reach a first application result by minute 15, join a prepared
partner machine running your chosen path. Open this same `week11` directory,
take turns operating, and retain your own changed configuration or `.blend`,
check/inspection result and image/playtest note. A recording helps orientation
but does not replace making and checking your own change.

## Godot path: three lights and an exit

### 0-35: inspect, predict, run and change

Open [world.py](world.py), [godot/world.gd](godot/world.gd) and
[godot/world.json](godot/world.json). Python validates a configuration file and
starts a **separate Godot process**. GDScript implements the world inside
Godot. This is not Python running natively inside the game engine.

```bash
uv run python world.py inspect
uv run python world.py check
uv run python world.py play
```

File inspection reports `file_state_only: true`. The real engine check must
report `passed: true`, three collected lights and `won_by_180_frames: true`.
In the window, move with arrow keys. The exit begins locked: collect all three
yellow lights, then reach the exit on the right. Close the window to stop.

Predict: if movement speed halves, can playback still win within three seconds?
Inspect `advance()`: `speed * delta` is distance moved during one time step.
The same behavior serves play, deterministic replay and checks.

```bash
uv run python world.py set speed 360
uv run python world.py check
uv run python world.py play
```

Observe faster movement and compare `ticks` in `.output/check.json`. The check
runs 180 steps at 1/60 second; this is simulated time, not a wall-clock benchmark
or a keyboard test. It does not judge whether the game is fun. The window loads
config at startup: close and restart after edits.

### 35-55: a real community MCP bridge

[Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp) is third-party,
not an official Godot feature. Setup fetches source commit
`1209744fad78f3998f98c7394fd0f6ef50da5281` (version 0.1.1) and its MIT license
into ignored `.tools/`. The course updates its declared MCP SDK 0.6 to the
**tested 1.30.0** runtime. Node 26 executes the TypeScript directly.

```bash
uv run python setup_bridge.py
uv run python mcp_client.py list
uv run python mcp_client.py demo
```

Setup needs GitHub/npm access. A fresh source/runtime installation passed on
29 October: 3.606 seconds with an empty npm cache on the author machine. This
is bridge setup time, not a first-time Godot editor download measurement. If setup fails, continue direct application work and pair with a
prepared bridge machine. Do not label an unexecuted request a successful tool run.

`demo` initializes MCP, inspects the actual project, creates `godot/probe.tscn`,
adds a `Marker` Node2D, requests project launch, reads debug output, requests
stop and closes stdio. Inspect the saved scene. The server's “project started”
text is an acknowledgement: look at the actual window/debug output before
claiming it ran correctly. This is **human-directed execution**, not a model
choosing actions autonomously.

Trace this request in [mcp_client.py](mcp_client.py):

```json
{"method":"tools/call","params":{"name":"add_node","arguments":{"projectPath":"ABSOLUTE/PATH/TO/week11/godot","scenePath":"probe.tscn","parentNodePath":".","nodeType":"Label","nodeName":"Caption","properties":{"text":"THREE LIGHTS"}}}}
```

Replace the absolute project path, then call the same tool:

```bash
uv run python mcp_client.py add_node '{"projectPath":"ABSOLUTE/PATH/TO/week11/godot","scenePath":"probe.tscn","parentNodePath":".","nodeType":"Label","nodeName":"Caption","properties":{"text":"THREE LIGHTS"}}'
```

PowerShell argument quoting varies: edit the `calls` list inside `mcp_client.py`
instead and run `demo`. Open `probe.tscn` in Godot and inspect Caption's text.
The saved Label/property were checked in the real engine. The supplied game
was also rendered and recorded in Godot 4.7.2; inspect your own desktop result. This does not update an editor window showing another scene.
The community server invokes Godot CLI/bundled GDScript; it is not a general
live-editor remote control.

### 55-85: break, then make a purposeful change

Keep the full 55-65 break. Choose a quicker route, smaller pickups or a later
exit. Change exactly one setting and explain the design tradeoff:

```bash
uv run python world.py set pickup_radius 16
uv run python world.py check
uv run python world.py play
```

Check both behavior and appearance. Allowed settings: `speed` 60-480,
`pickup_radius` 8-48, `exit_x` 720-880. These are course choices, not Godot API
limits. Inspect `BOUNDS` and `update_config()`; bad input is rejected before
writing, rather than silently clamped.

### 85-100: diagnose and recover

```bash
uv run python world.py set speed 120
uv run python world.py check
```

Expect failure: after 180 steps, x is near 440 and only two lights are collected.
The engine ran but missed the declared time budget. Read the fields before
changing anything. Decide a better value, explain why and rerun:

```bash
uv run python world.py set speed 300
uv run python world.py set pickup_radius 24
uv run python world.py check
```

The checked default recovers: three lights, x=840, success at tick 152.
Try `uv run python world.py set exit_x 2000`: rejection must preserve the old
config. For a missing-node experiment, set the MCP parent to `MissingParent`,
read the error and restore `.`. Transport success and useful app results differ.

Missing engine: check `GODOT_PATH`. Wrong project: compare the absolute path
with `inspect`. Script error: read stderr and undo the last small edit.
Graphics failure: use a prepared partner machine. A headless check cannot
establish that the artwork is displayed.

## Blender alternative: a sculpture and checked renders

### 0-35: use the actual Python API

The script builds a disposable scene: Sculpture cube, floor, camera and light.
It clears objects only in its new background process and never loads your
personal `.blend` files.

```bash
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.5
```

Open `.output/blender/sculpture-1.png` and `sculpture-1.5.png`. Compare apparent
size and shadow with the same camera. Inspect `.output/blender/inspect.json`
and open `sculpture.blend`. The `before` scale is `[1,1,1]`; `after` must match
the request. Assignment changes scene data; `save_as_mainfile()` saves it;
`bpy.ops.render.render(write_still=True)` produces the image. Three operations,
three separate results.

Read [blender_scene.py](blender_scene.py): `bpy.data.objects.get()` finds the
named object, `target.scale` is a vector property, and the camera uses
`to_track_quat('-Z', 'Y')` to aim at a target. CPU Cycles renders 640x480 with
eight samples. Predict what changes if you move the camera rather than the cube.

### 35-55: application work through MCP

```bash
uv run python mcp_client.py --blender list
uv run python mcp_client.py --blender render_scene '{"scale":1.25}'
uv run python mcp_client.py --blender inspect_scene
```

[blender_tools.py](blender_tools.py) is a **course-owned bounded MCP stdio
adapter** using the official Blender CLI and our Python script. It is not the
third-party Blender MCP add-on. Its two tools render the supplied scene at
scale 0.5-2 and inspect the last saved result. Inspect actual PNG/`.blend` after
the response. The background process must also exit: an existing image alone
cannot prove clean shutdown. `isError: true` means failure even if an older PNG exists.

The wider [MCP for Blender](https://github.com/ahujasid/blender-mcp), by Siddharth
Ahuja, is now packaged as `mcp-for-blender` 2.2.6. Its Python MCP server connects
to an add-on inside live Blender over localhost TCP (default 9876). Its
`execute_blender_code` is broader than the supplied adapter. The supplied live demonstration passed startup, discovery, scene inspection,
scale change to 1.5, a second live inspection, CPU render/save and clean shutdown
in real Blender 5.2.3. It is an optional alternative to the simpler course
adapter; no paid asset generation or model call is involved.

```bash
uv run python setup_blender.py
uv run python blender_live.py
```

The setup fetches the pinned MIT-licensed add-on and installs `mcp-for-blender`
2.2.6 in ignored `.tools/blender-env`; it changes no global client or Blender
preferences. The demo creates a **disposable separate Blender window**, binds
its add-on to a free loopback port, then drives the community server over stdio.
It inspects Sculpture, changes its live scale, inspects again and saves/renders
`.output/blender/sculpture-live.blend` and `sculpture-live.png`. Inspect the
object in the window; press Enter in the terminal to close the client, stop the
add-on and quit this window. Do not open personal work in this disposable
process. `.output/blender-live-result.json` must show scale `[1.5,1.5,1.5]`,
`blender_exit: 0` and `socket_closed: true`.

Read the request sequence in [blender_live.py](blender_live.py) and the local
startup/stop hook in [blender_addon_boot.py](blender_addon_boot.py).
`get_scene_info` reads the running Blender scene; the course adapter's
`inspect_scene` reads a saved JSON file. They answer different questions.
`execute_blender_code` executes Python inside Blender and can do far more than
change a scale; this example supplies reviewed code for the disposable scene.
The helper disables the bridge's telemetry and update check. Do not select
asset or generation tools: they are outside this exercise.

For automatic closure, tutors can run
`uv run python blender_live.py --verify`; this exercises the real GUI/render
path and needs a working display. Fresh add-on/package installation passed in
4.602 seconds on the author machine with an empty uv cache; Blender itself
was already installed. Download times vary.

### 55-100: break, compose, fail and recover

Keep the 55-65 break. Predict which faces become more visible when the camera
moves from `(7, -9, 6)` to `(9, -7, 6)`, keeping sculpture scale at 1.25:

```bash
uv run python blender_variants.py
```

Compare `.output/blender/angle-1/sculpture-1.25.png` with the corresponding
`angle-2` image and read each `inspect.json`. The loop in
[blender_variants.py](blender_variants.py) enumerates a list of camera pairs,
starts Blender with those command-line arguments and keeps each output in its
own folder. The sculpture is unchanged; camera position changes the observation.
Change the second pair to `(5, -10)` and rerun. Check the camera coordinates
and render before restoring `(9, -7)`. Two controlled variants are enough to
explain the archive's multi-angle dataset idea without AI-generated meshes or
a large dataset. `to_track_quat` keeps the camera looking at the target; moving
a camera and rotating a sculpture are different edits.

```bash
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --target MissingObject
```

Expect nonzero exit and `Missing object: MissingObject; use Sculpture`.
An earlier PNG is not the failed run's output. Remove the bad target and
rerender. A tool call with scale 5 must return `isError: true` before launch.

If managed-machine settings/cache writes fail, use the course adapter: it
redirects those paths into `.output`. If a render exists but shutdown hangs,
stop with Ctrl+C, preserve the error and ask the tutor. Do not repeat launches
indefinitely. The saved scene still allows inspection while shutdown is diagnosed.

## 100-120: tutor review and project support

Show one purposeful change, an actual application result and failure/recovery.
Explain which process owns each operation and whether inspection reads a file
or live state. Retain your own scene/config, check/inspection and image/playtest
note. These are practice evidence, not a new upload or grade. Use remaining
time for the scheduled **19 November** tutor discussion: what works, feedback,
a blocker and the team's next testable step.

The group project remains **40%**; **25% idea / 50% code / 25% execution**, due
**6 December 2026, 23:59 HKT**. Use a shared public `sd5913`-owned repository
with teammate Write access. GitHub Projects is recommended; an equivalent
accessible progress record is valid. Follow Canvas submission instructions.
These tools inspire projects; they are not mandatory features or a defence.

## Next week and extensions

Week 12 uses Godot. Blender-only students receive first-time Godot setup and
orientation at minutes 0-20, then join a prepared partner machine if the
baseline still fails. You do not need both applications today.

Optional `uv run python world.py capture` uses official Godot Movie Maker,
120 frames at 30fps, then FFmpeg to write `.output/world.mp4`. It needs a
working graphical renderer plus FFmpeg/ffprobe. The Linux software-rendered
route was verified on 29 October: a playable 960x540 H.264 MP4, four seconds,
120 frames, with early/middle/end frames inspected for collection and completion.
This is deterministic replay of the supplied world, not an autonomous agent. The three-second check and four-second recording serve different jobs.

[The archive](https://github.com/sd5913/pfad/tree/2025/week11) includes
TouchDesigner, OSC/handtracking, NDI and a networked game. OSC carries addressed
control messages; NDI transports audio/video. An OSC send does not prove a
receiver used it, just as a tool acknowledgement does not prove the scene is
correct. Week 9 supplies the network/vision-message bridge. These are optional
creative extensions, not more installations. Orange/t-SNE/matrix projection
requirements were removed by instructor decision; Week 10 keeps the handbook
embedding/retriever knowledge path.

## Sources and verification limits

Checked 29 October 2026 through current documentation and primary sources:
[Blender API](https://docs.blender.org/api/current/),
[Godot CLI](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html),
[Movie Maker](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html),
[Coding-Solo source](https://github.com/Coding-Solo/godot-mcp/tree/1209744fad78f3998f98c7394fd0f6ef50da5281),
[MCP for Blender](https://github.com/ahujasid/blender-mcp/tree/8782963ba87a4c90482198bd7c7e17219ac3a0f7).
Godot is MIT-licensed; Blender is GPL-licensed; both community bridges and MCP
SDK are MIT-licensed. Geometry is original course code; no downloaded assets.

Verified: Godot 4.7.2 actual engine behavior and slow-speed failure/recovery;
community MCP discovery/project metadata/create/add-node/stop; actual graphical
Godot capture and full MP4 decode; Blender 5.2.3 CPU-rendered PNG/scene; course
MCP adapter clean exit; live third-party Blender bridge change/reinspection/
render/save/clean close; fresh public installation of both bridges.
Four automated tests pass, including an opt-in real Blender acceptance test:

```bash
uv run python -m unittest test_world test_mcp_transport test_engine
uv run python -m unittest test_blender_live
```

The last command needs Blender, its installed bridge and a working display.
On a Linux CI machine with Xvfb installed, prefix it with `xvfb-run -a`.
Windows/macOS and classroom rehearsal remain outstanding. Actual keyboard
play and projected display should be rehearsed on the teaching machine.
A tool launch response, headless check or trace does not close those gaps. The old `browser/`
exercise remains a historical simulation and is not the core practical.
