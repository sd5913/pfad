# Godot preparation for Week 12

This is retained preparation from the earlier Week 11 tutorial. The current
[Week 11 tutorial](README.md) offers Blender or authenticated-app routes;
**Godot is not a third Week 11 route**. Return here when preparing for Week 12.
Its first-time Godot setup is also budgeted in that week's tutorial; no one
needs to complete three applications today.

Use standard [Godot](https://godotengine.org/download/) (not .NET),
[uv](https://docs.astral.sh/uv/), and a desktop that can show the game.
The retained rehearsal used Godot 4.7.2 on Linux x86_64 on 29 October 2026;
Windows/macOS remain untested. No export templates are needed to play.
Godot must be named `godot`/`godot4` on PATH or `GODOT_PATH` must point to its
full executable. In Bash/zsh: `export GODOT_PATH='/path/to/Godot'`.
In PowerShell: `$env:GODOT_PATH = 'C:/Tools/Godot/Godot.exe'`.
The optional community bridge needs Node.js 26 and npm (tested 26.12.1),
GitHub/npm access and a first installation. Keep commands in this directory:

```bash
cd week11
uv run python -m unittest test_world test_mcp_transport test_mcp_cleanup test_mcp_client_status test_engine
```

If setup blocks you, work with a prepared partner and take turns making a
change, running it and explaining its result. A recording only orients you;
it does not establish that your copy runs. None of these deterministic
commands demonstrate a model selecting its next action.


## Inspect, predict, run and change

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

## A real community MCP bridge

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
adds a `Marker` Node2D and a `Caption` Label with text `THREE LIGHTS`, requests
project launch, reads debug output, requests stop and closes stdio. Stop is
attempted even if a later request fails; bounded process cleanup also stops the
owned application if the bridge no longer responds. Inspect the saved scene.
If bridge closure fails after a successful request, the command exits nonzero.
If the request already failed, its original error is preserved and the cleanup
error is reported separately.
The server's “project started”
text is an acknowledgement: look at the actual window/debug output before
claiming it ran correctly. This is **human-directed execution**, not a model
choosing actions autonomously.

Trace the existing Caption request in [mcp_client.py](mcp_client.py). Now add a
different instruction label, `RouteHint`, to the scene created by `demo`:

```json
{"method":"tools/call","params":{"name":"add_node","arguments":{"projectPath":"ABSOLUTE/PATH/TO/week11/godot","scenePath":"probe.tscn","parentNodePath":".","nodeType":"Label","nodeName":"RouteHint","properties":{"text":"COLLECT THREE, THEN EXIT"}}}}
```

Predict: Caption should stay unchanged, and one new named Label should appear.
Replace the absolute project path, then call the tool once:

```bash
uv run python mcp_client.py add_node '{"projectPath":"ABSOLUTE/PATH/TO/week11/godot","scenePath":"probe.tscn","parentNodePath":".","nodeType":"Label","nodeName":"RouteHint","properties":{"text":"COLLECT THREE, THEN EXIT"}}'
```

PowerShell argument quoting varies: append this `add_node` request's arguments
as another `("add_node", {...})` entry after Caption in the `calls` list inside
`mcp_client.py`, then run `demo`. Open `probe.tscn` in Godot: inspect Caption's
text `THREE LIGHTS` and the new RouteHint's text `COLLECT THREE, THEN EXIT`.
Read the saved `.tscn` too; a generated name such as `@Label@2` means you repeated
a name. To reset, undo any `calls` edit, rerun `demo` (which recreates the probe)
and make the RouteHint request once. The saved nodes/properties were checked
with these real bridge calls. The supplied game
was also rendered and recorded in Godot 4.7.2; inspect your own desktop result. This does not update an editor window showing another scene.
The community server invokes Godot CLI/bundled GDScript; it is not a general
live-editor remote control.

## Make a purposeful change

Choose a quicker route, smaller pickups or a later
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

## Diagnose and recover

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

## Optional recording and provenance

`uv run python world.py capture` uses official Godot Movie Maker, 120 frames
at 30fps, then FFmpeg to write `.output/world.mp4`. It needs a working renderer
plus FFmpeg/ffprobe. The 29 October Linux software-rendered rehearsal produced
a playable 960x540 H.264 MP4, four seconds, 120 frames, with early/middle/end
frames inspected. This is deterministic replay, not an autonomous agent. The
three-second check and four-second recording serve different jobs.

The earlier rehearsal also checked real engine slow-speed failure/recovery,
community MCP discovery/project metadata/create/add-node/stop and clean
process closure. The POSIX cleanup tests include a real headless Godot case
when the pinned bridge, Node and Godot are installed; otherwise it skips.
No new graphical Godot rehearsal is claimed by the Week 11 documentation update.
Actual keyboard play and projected display still require classroom rehearsal.

Sources: [Godot command line](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html),
[Movie Maker](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html),
[community bridge source](https://github.com/Coding-Solo/godot-mcp/tree/1209744fad78f3998f98c7394fd0f6ef50da5281).
Godot and this community bridge are MIT-licensed; preserve upstream notices.
The supplied scene is course code. The old `browser/` exercise remains a
historical simulation rather than this practical.
