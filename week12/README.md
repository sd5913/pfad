# Week 12: build, check and film a tiny world

**Thursday 26 November 2026. Separate 120-minute tutorial. Draft, with an open
production gate:** real Godot behavior and a genuine model-selected adaptation
are recorded; a playable graphical capture and a timed first-time graphical
bootstrap are still unverified. The incumbent lecture deck is historical and
has not been accepted for this new lesson. Tutors must verify a prepared
Godot machine and film before delivering the graphical route below.

You will inspect a supplied world, change a bounded configuration, explain a
failed check, recover and inspect a deterministic clip. Python connects the
file, engine process and evidence. The Godot script supplies the actual game
behavior. A human can select every tool action: **no model account, paid API,
MCP bridge, dedicated GPU or Week 10 handbook index is required**. This route
is human-directed execution. Reading the supplied model trace is recorded
replay; recording the world is deterministic playback. Neither is a fresh
model making decisions.

This is practice and existing project support, with no new grade, upload,
deadline, compulsory engine or AI feature for your group project.

## The full 120 minutes

| Minutes | Work and visible result |
| --- | --- |
| 0-20 | First-time Godot bootstrap or installed-engine check; open the starter and run the baseline. At minute 20 move setup failures to a prepared partner machine. |
| 20-35 | Read the brief and actual recorded model/tool trace; predict a check. |
| 35-55 | Inspect the code and make one bounded change through the local host. |
| 55-65 | Break. |
| 65-85 | Run a deliberate failure, adapt from the observation, check and stop. |
| 85-100 | Replay, capture, decode and visually inspect the clip; retain your own evidence. |
| 100-120 | Tutor delivery-candidate review and project support, including unfinished projects. |

The setup and capture blocks are budgets, not measured promises. Do not eat the
break or tutor time to repair an installation. If all machines lack graphics,
the practical is incomplete: retain the config/check work, ask the tutor for a
verified machine and arrange recovery within the existing support process.
A recorded clip alone does not replace your hands-on change/check/capture.

## 0-20: install/check, orient and run

You need the PFAD checkout containing this folder, `uv`, a desktop display and
the **latest stable standard Godot**, plus `ffmpeg` and `ffprobe` on PATH for
capture. Standard Godot needs no .NET SDK. This tiny 2D project selects the
Compatibility renderer; an integrated GPU or working software OpenGL can be
enough. A headless terminal alone cannot prove the visible game or movie.
Internet is needed for first downloads. Python dependencies for this route are
empty; `uv` uses this folder's isolated project instead of PFAD's root Worker
environment. If Python is unavailable locally, `uv` may download it first.

As verified on 29 October, current stable is **Godot 4.7.2**. Recheck the
[official download page](https://godotengine.org/download/) before class; use a
newer stable release if it has arrived, then repeat the checks and visible
preflight. Do not use the superseded 4.5.1 cache. Windows/macOS/Linux standard
builds are available; only Linux x86_64 headless behavior has been tested here.
Windows/macOS first launch, signing prompts and graphics remain untested.

The official Linux x86_64 4.7.2 ZIP is 77,860,424 bytes (about 78 MB), excluding
extraction, Python and FFmpeg. Other platform download sizes and all cold
installation/download times are unmeasured. The author used a warm installed
Arch Linux binary; that is not a timed first-time bootstrap. See
[verification.md](verification.md) for exact evidence and outstanding gates.

1. **Minutes 0-5:** students who used only Blender in Week 11 follow this same
   route. Download the latest standard Godot for your OS, extract it into a
   normal local folder and open it. If already installed, check its About/version
   and continue. Install/check `uv`, FFmpeg and FFprobe if needed. On a slow
   connection, tell the tutor early; the minute-20 handoff is prepared in advance.
2. **Minutes 5-10:** from the PFAD root, enter this directory. Point `GODOT_PATH`
   to the extracted executable if `godot`/`godot4` is not on PATH. Keep this
   terminal inside `week12` for all later commands.

   ```bash
   cd week12
   uv run python world.py inspect
   ```

   On Linux/macOS, for example: `export GODOT_PATH='/absolute/path/to/godot'`.
   For the macOS app the executable is inside `Godot.app/Contents/MacOS/Godot`.
   In Windows PowerShell use `$env:GODOT_PATH = 'C:\path\to\Godot.exe'`.
   Substitute your actual extracted filename. Paths may contain spaces; the
   helper passes arguments separately. Use `ffmpeg -version` and
   `ffprobe -version` to check the capture programs. No bridge installer runs.
3. **Minutes 10-15:** in Godot's Project Manager choose **Import**, browse to
   this checkout's `week12/godot/project.godot`, then **Import & Edit**. Locate
   `world.tscn`, its World node and `world.gd`; do not create a blank project.
   Run with **F6** while `world.tscn` is open, or use the supplied launch command:

   ```bash
   uv run python world.py play
   ```

   Focus the game window. Arrow keys move the pale player. Three gold lights
   sit left to right; the exit changes from grey to mint only after all three.
   Move to the exit without taking every light: no COMPLETE message should
   appear. Close the game window to stop it; Ctrl+C is terminal recovery.
   A five-minute helper limit also ends abandoned play. Keep the editor's run
   stopped before launching a second copy. Read the actual terminal error if
   the display or executable fails; do not infer success from a process starting.
4. **Minutes 15-20:** run the baseline below. The supplied speed is deliberately
   125, so **exit status 1 is expected**, not an installation failure:

   ```bash
   uv run python world.py check
   ```

   Expect `collected: 2`, `player_x` about 455, `ticks: 180`, `passed: false`
   and `premature_exit_rejected: true`. A `WORLD_CHECK` result proves the real
   engine ran. Missing engine, script errors or no structured result are setup
   problems. File inspection alone proves only stored config, not behavior.

**Minute-20 prepared-machine handoff.** The tutor must have preflighted the
latest Godot, this exact starter, visible play, passing/failing checks and
`world.py capture`, including actually viewing the four-second film. This
preparation is still an open production gate. Do not call an unverified laptop
prepared. If your setup is unfinished, join that machine now. Open its supplied
`week12/godot/project.godot` through Project Manager **Import**, as above. Open
its terminal in `week12`; identify `godot/world.json` and `.output` together.
Agree who operates first and who reads/checks observations. The first learner
operates the 35-55 block; the second operates the 65-85 block; both must make
their own config change and run a check. During 85-100 take turns capturing,
viewing and copying your own evidence before changing the next person's config.
The observer predicts and checks, then swaps roles. No shared account is needed.

## 20-35: brief, observation, decision

**Brief:** from the supplied start, collect all three lights and reach the exit
within **180 physics ticks at 60 ticks/second (three simulated seconds)**.
The player starts at x80; lights are at x240, x420 and x600; the exit is at x860.
Keep the three light positions and the checker fixed. Read these files:

| File | What it owns |
| --- | --- |
| [godot/world.json](godot/world.json) | Persistent config: speed, pickup radius and exit position. |
| [godot/world.gd](godot/world.gd) | Running state and `advance`: movement, pickups, win rule and drawing. |
| [godot/check_world.gd](godot/check_world.gd) | Real engine tests, including arriving at the exit with too few lights. |
| [world.py](world.py) | Inspect/config/process/check/capture adapter; no model. |
| [loop.py](loop.py) | Host limits and observations; no repair choice or model. |

Read the recorded episode:

```bash
uv run python replay.py
```

This prints [model-episode.json](model-episode.json), a sanitized **actual
recorded Codex CLI/GPT-6 tool episode**, 29 October HKT (raw UTC timestamps are
28 October). Exact backend model ID was not exposed. The source hash manifest,
reasons, raw engine outputs and path-only sanitization are recorded there.
The recording helper logged one requested action; it did not choose retries.

| Recorded action | Actual recorded observation |
| --- | --- |
| Inspect | speed 125, radius 24, exit 860; file state only. |
| Check | Godot 4.7.2, two lights, x455.000732421875, no win after 180 ticks, exit 1. |
| Model chooses speed 275 | Only speed changes. The model estimates the needed travel rate from the failed run. |
| Check again | Three lights, x840.832336425781, win at 166 ticks, exit 0. |
| Stop | No more scene edits; playable film and graphical bootstrap are missing. |

The original check was weaker than today's added premature-exit probes; do not
attribute these newer observations to that model. Its display prerequisite
observation was corrected later: socket creation succeeded, but connecting to
the actual Wayland display returned EPERM. No accepted film exists in this
fixture. Reading it does not make new calls. Compare the two check observations:
what changed, what stayed fixed, and what evidence justified stopping edits?

## 35-55: one bounded change

Before editing, trace `world.advance`: config is loaded on process startup;
`player`, `collected`, `won` and `ticks` belong to this running scene. Each tick
moves toward the next light, then toward the exit. `won` needs three lights
**and** distance <=20 from the exit. A file write does not move an existing
player. Close and relaunch a graphical run after a config change.

Predict whether speed 200 can cover roughly 760 units in 3 seconds. Start a bounded
human-directed attempt, inspect, change and check:

```bash
uv run python loop.py start
uv run python loop.py inspect
uv run python loop.py set speed 200
uv run python loop.py check
uv run python loop.py status
```

Expect a failed behavior check at speed 200. Read actual `collected`, `player_x`
and `ticks`; do not just quote the expected answer. Inspect
`.output/session.json`: actions, mutation count, config hashes and observations
are stored. `loop.py` never chooses a repair. A real model would receive these
observations and choose its next call; here you make that decision.

Each attempt permits **eight tool actions, four mutations and 180 elapsed
seconds**. Inspect/set/check consume actions, including failed tools. Stop
editing once a check passes. Engine checks have a 15-second subprocess timeout;
capture has 90 seconds for Godot, 60 for encoding, 30 for full decode and 15 for each
probe/sample extraction. Keep a human decision under 30 seconds; if unsure, stop
and discuss rather than continuing blind edits. The 30-second decision target
is a human instruction, not an enforced per-decision model timer.

Allowed writes are speed 60-480, radius 8-48 and exit_x 720-880 in this starter's
config. Unknown fields, booleans, nonfinite values and out-of-range numbers are
rejected before writing. This is a small host contract, not a sandbox for
untrusted shell/code. Inspect `update_config` in `world.py`; try one refusal:

```bash
uv run python world.py set exit_x 2000
uv run python world.py inspect
```

Expect a visible range error and unchanged config. `world.py` exposes primitive
tools directly; the session limits apply when you use `loop.py`. End this
practice attempt before the break:

```bash
uv run python loop.py stop
```

## 55-65: break

Stop game playback and return at minute 65. Do not use the break as extra setup.

## 65-85: fail, adapt, check, stop

For the second learner's turn, restore the supplied failing speed and start a
new attempt. The reset is a visible human action, outside the new tool budget:

```bash
uv run python world.py set speed 125
uv run python loop.py start
uv run python loop.py inspect
uv run python loop.py check
```

Explain why two lights at x455 are useful evidence: the scene ran and moved,
but did not satisfy the time-bound goal. Keep light positions and checker fixed.
Choose one bounded speed from this observation. For a reproducible recovery,
275 is the recorded model's choice; if you choose another value, justify it.

```bash
uv run python loop.py set speed 275
uv run python loop.py check
uv run python loop.py status
```

Expect three lights, win at 166 ticks and `status: passed`. A further session
`set` must be refused. The automatic host stop concerns edits after a passing
check; the human still reviews the observation and decides whether to film.
On budget expiry, call `loop.py stop`, explain what is missing and seek help;
a new attempt must be deliberate, not a hidden retry that erases evidence.
Copy the session JSON if you need to compare attempts, since starting a new
one replaces it. Config persists; restarting a world resets player state.

Run the behavior suite. It copies projects to temporary folders so it does not
change your working speed:

```bash
uv run python -m unittest discover -p 'test_*.py' -v
```

The real engine tests check speeds 125/275/60/480, incomplete-light exit attempts
with 0/1/2 lights, completion and unchanged state after winning. A fixed-frame
headless replay reaches the same 166 ticks; this is timing evidence, not a film.
The older addition/MCP files are retained historical smoke tests and are not
this lesson's main practical or a required model installation.

## 85-100: replay, capture, inspect, retrieve

Make sure your chosen config passes `world.py check`. Start an automatic
visible run, then close its window:

```bash
uv run python world.py replay
uv run python world.py capture
```

Replay uses the same `advance` method as manual play and engine checks.
Godot Movie Maker runs 120 rendered frames at 30 fps (about 4 seconds); simulation
uses 60 physics ticks per second and freezes on completion, leaving an ending
hold. Replay follows a predetermined route, with no model action selection.
Capture first reruns the behavior check, uses official `--write-movie`, expects
a completion observation, encodes H.264 MP4, checks metadata, decodes every
frame and extracts sample PNGs. It requires graphical rendering: never use
headless black frames as the substitute. This capture path is supplied but
remains unaccepted until actual graphics can be exercised and inspected.

Open `.output/world.mp4` in your video player. Expect 960x540, about 4 seconds,
120 frames; compare `.output/frame-start.png`, `frame-middle.png` and
`frame-end.png`. Check that the actual world is visible, the player moves,
lights disappear in order and the ending shows COMPLETE. Metadata/decode pass
cannot prove those visual facts. Explain any discrepancy before accepting it.
Read `.output/capture.json` and any `.output/last-error.json`; preserve the
error if graphics, encoder or decode failed. Do not report a clip from an
older configuration as today's result.

**Each learner retains their own evidence before the partner's next turn.**
On a shared machine, each learner first repeats their own short bounded attempt
so the session journal also belongs to that turn: `world.py set speed 125`,
`loop.py start`, `loop.py check`, `loop.py set speed 275`, `loop.py check`, then
`world.py capture`, each through `uv run python` as above. If a previous session
is still active, explicitly stop it first and retain its evidence. The failed
check is expected; select commands one at a time. Both learners may choose 275,
but each must operate and inspect their own run rather than inherit a partner's
passing report. Copy all evidence before the next learner resets the config.
In the editor's file explorer or OS file manager, show hidden files and open
`week12/.output`. Create a folder named for your own attempt outside the shared
starter. Copy `godot/world.json` into it, then copy `.output/check.json`,
`.output/session.json`, `.output/capture.json`, `.output/world.mp4` and the
three `frame-*.png` files. Verify that the copied config and capture report's
config agree, open the copied clip and confirm the completion. Transfer that
folder to your own laptop through your normal local/shared-file route; open it
there before leaving. Never copy another learner's result as your own.
If no film exists, retain config/check/error with the explicit missing-film
status and request a turn on a verified machine. There is no new upload.

Allow the first learner up to 7 minutes for their own passing config/check/film/
copy, then swap for 7 minutes; use the remaining minute to verify both copies.
Use the already prepared working scene rather than rebuilding it. If a failed
capture consumes the block, report it and use tutor support for triage instead
of inventing completion. A prepared machine must be rehearsed before class.

## 100-120: delivery-candidate tutor support

The 26 November tutorial includes the existing delivery-candidate review. Show
one working project interaction, its expected result, a failure/check and a
README another person can follow. Include unfinished projects: identify the
smallest repair that makes the project runnable and who will check it. Update
the team's existing progress record with feedback and the next action; raw
commit/card counts are not a grading rule. Optional inspiration: could a
bounded check/tool improve your own workflow? Your project need not use AI
or Godot.

The group project remains 40% of the course, with 25% idea / 50% code / 25%
execution, due **6 December 2026, 23:59 HKT**. Use the shared public
`sd5913`-owned repository with teammate Write access. GitHub Projects is
recommended; an equivalent accessible shared progress record is valid. Canvas
remains the submission system; this tutorial introduces no additional artifact
submission or assessment requirement.

## Troubleshooting and sources

| Observation | Response |
| --- | --- |
| Engine missing | Check actual executable/GODOT_PATH; use the minute 20 prepared-machine handoff. |
| File shows new speed, game unchanged | Close and relaunch; the running scene loaded config at startup. |
| Check exit 1 with structured values | A real failed behavior observation; compare speed/distance/ticks and adapt. |
| Parser error, missing result or timeout | Tool failure, not a behavior pass. Keep the error and ask for help. |
| Session refuses an edit | Inspect status and limits; stop. Do not silently reset the budget. |
| Display connection denied/no window | Use the verified partner; file/headless tests do not prove graphics. |
| MP4 missing, wrong duration or bad decode | Capture failed; retain error evidence. Do not substitute old or dummy frames. |

Sources checked 29 October 2026: [Godot 4.7 Movie Maker](https://docs.godotengine.org/en/4.7/tutorials/animation/creating_movies.html),
[command line](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html),
[Node processing](https://docs.godotengine.org/en/4.7/classes/class_node.html),
[4.7.2 official release](https://github.com/godotengine/godot-builds/releases/tag/4.7.2-stable).
Documentation was fetched through Context7 before API changes. The
[verification record](verification.md) separates current checks, supplied
recordings and missing acceptance. [CI candidate](ci-capture-candidate.md)
describes an unrun public-runner graphics path. All starter code is copied
from the course-owned Week 11 commit recorded in the fixture; no unmerged
sibling import is needed. W10 source-backed handbook retrieval remains a
separate unproven dependency: this world does not claim to search that index.
