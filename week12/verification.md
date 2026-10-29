# Week 12 verification record

29 October 2026. **Core model/engine/film/operator-bootstrap feasibility proven
on Linux; independent review and classroom preflight remain.** The genuine model
trace is preserved without changing its historical observations. Later actual
film, stills and sanitized metadata are under [evidence/](evidence/provenance.json).
No new paid model call, presenter operation or public CI run was made.

## Actual current environment and behavior

Linux x86_64, `/usr/bin/godot --version`:
`4.7.2.stable.arch_linux.ed1daf0bf`. This supersedes the old 4.5.1 cache.
`uv run` selected CPython 3.13.16 in this isolated weekly project. The host
system Python is 3.14.8; current course commands below use uv's Python. No
Python third-party packages are required for the new core. Existing historical
MCP smoke scripts have separate inline dependencies and are not needed here.

From this folder:

```bash
uv run python world.py inspect
uv run python world.py check
uv run python -m unittest discover -p 'test_*.py' -v
uv run python replay.py
```

The author ran these with a local writable uv cache and `--offline`, using
already installed Python/engine, not a cold installation. Twelve tests pass:
five historical addition/host-policy tests, config bounds/nonfinite rejection,
three host-budget/stop/error tests, capture metadata validation, and two actual
Godot behavior/replay tests. The metadata test does not produce a movie.

| Actual current case | Result |
| --- | --- |
| Supplied speed 125, 180 ticks | Exit 1, 2 lights, x455.000732421875, no win. |
| Changed speed 275, unchanged world goal | Exit 0, 3 lights, x840.832336425781, win 166 ticks. |
| Boundary speed 60 | Fails at 180 ticks, one light. |
| Boundary speed 480 | Passes at 95 ticks, 3 lights. |
| Put player at exit with 0/1/2 lights | All three actual state transitions reject a premature win. |
| Advance again after a win | Position/tick count stop changing. |
| Real headless main scene, fixed 30 fps/120 frames, speed 275 | Emits one actual `WORLD_REPLAY` completion at 166 ticks with 3 lights. Timing evidence only, no film/rendering acceptance. |

To check the checker, disposable project copies deliberately removed (1) the
three-pickup condition and (2) the stop-after-win guard. The first returned
`premature_exit_rejected: false`; the second returned
`stopped_after_win: false`. Both real engine runs exited 1 with `passed: false`.
These author-selected mutation checks are not the model's original episode.

The command-line host was rehearsed directly: start -> inspect -> 125 check
exit 1 -> set 275 -> check exit 0 -> attempt set 300 exit 2 -> status. The host logged
four tool actions, one mutation and `passed`; the post-pass edit was refused.
The author then restored the supplied config to 125 and reran its expected
failing baseline. Ignored `.output/host-rehearsal.json` and
`.output/human-verification.json` contain local command observations; they are
explicitly human-selected verification, not public model provenance.

## Recorded model episode: what it proves

`model-episode.json` derives from an actual current authorized Codex CLI/GPT-6
session, 29 October HKT. Exact backend model ID was unavailable. It preserves
all seven original records: inspect, failing check, model-selected speed 275,
passing check, socket-creation prerequisite observation, stop and corrected
Wayland transport observation. Its logger executed one requested action and
contains no retry/adaptation choice. A fidelity comparison checked every
original field and action argument: only executable/project paths changed;
all numeric outputs, reasons, return codes and observations match. No `/home/`
path remains. The fixture explicitly says clip false/full gate incomplete.

This proves actual model-directed adaptation from observed failure. Reading
`replay.py` is a read-only recorded replay; it does not execute tools or call a
model. The historical source hashes and starter commit are retained in the
provenance. Current W12 strengthens the checker and adds completion logging;
these newer probes are not retroactively attributed to the recorded model.

## Actual film, timed bootstrap and prepared partner rehearsal

After full local permissions became available, the author rendered the exact
original model-selected final source, speed 275, with real Godot 4.7.2 on a
separate Xvfb display and Mesa llvmpipe software OpenGL. This is a deterministic
capture after the model's genuine choice, not a new agent run. The original
source hashes are retained in `evidence/provenance.json`; the current stronger
checker and completion logger are not retroactively attributed to that model.
The actual clip `evidence/model-selected-world.mp4` is 960x540, 4.000 seconds,
120 frames at 30 fps. FFmpeg decoded every frame; ffplay played the complete
clip; beginning/middle/end images were inspected: 0 lights, then 2 with player
movement, then 3 with mint exit and COMPLETE. There are no dummy/black frames.

The current `world.py capture` helper separately passed the same real graphics,
encoding, metadata/full-decode/sample acceptance, with completion at 166 physics
ticks. Its `visual_inspection_required: true` remains intentional: each new
capture needs a person to inspect it. The public sample film is a reference,
not another learner's practice result.

The official latest-stable release endpoint was checked 29 October: 4.7.2,
published 18 August 2026 at 15:56:46 UTC. A **fresh** official Linux standard ZIP
was downloaded in **9.484 seconds**, 77,860,424 bytes, SHA-256
`cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4`.
Fresh extraction reports `4.7.2.stable.official.ed1daf0bf`. The isolated rehearsal
had no W11 project/bridge or Godot import cache. It used existing Linux x86_64,
uv, system CPython 3.14.8, FFmpeg/ffprobe, Xvfb and Mesa; prerequisite installation
and novice reading time are excluded. It does not measure every student's setup.

Download/extract/copy + editor import, file inspection, real supplied baseline
failure, human revision/passing check/capture, then two simulated learner turns
with their own config/check/session/capture and evidence retrieval took
**31.215 seconds of active scripted execution**. A follow-up fully initialized
editor orientation in 2D and normal Ctrl+Q/Enter exit took **29.312 seconds**.
The total measured active route is **60.528 seconds**, well inside the 20-minute
budget. These are separate measured stages, not a single continuous novice
trial. Early screenshots taken during initialization were rejected; an early
WM_DELETE close timed out and Ctrl+Shift+Q opened Project Manager, so those were
not counted as clean-stop proof. The final editor quit exits 0, logs only the
expected Xvfb XIM/VSync warnings and leaves no engine descendants.

`evidence/editor-orientation.png` shows the actual supplied World/files/2D tab.
The canvas is blank by design because `_draw` executes in the running scene;
the README now says to run F6/the play helper to see the actual world. The
initial baseline at 125 produces 2 lights/x455/180ticks/passed false. Both
simulated partner turns independently reset/check, change to 275/check, capture,
copy config/check/session/report/clip/three frames, validate config identity and
decode the copied clip. Copies use separate source folders and explicit swaps;
no inherited passing journal is claimed as the second learner's work. This is
an operator rehearsal, not a study with two students. The minute-20 handoff and
7+7+1 minute evidence turns remain in the README. Break 55-65 and support100-120
are intact. All cited evidence is private-path-free in the public fixture.

Windows/macOS, installing uv/FFmpeg from scratch, slow networks and novice
orientation remain unmeasured. Tutor preflight must verify the actual latest
engine and prepared partner machine; arrange the minute-20 handoff exactly as
documented. The public `ci-capture-candidate.md` is still an **unrun** normal
PR-runner proposal, not a claim of CI artifacts or a replacement for bootstrap.

## Cross-week dependency and sources

The tiny world has no handbook-search dependency. The author independently ran
W10's actual VectorIndex prepared query for the lost-card question: replacement
chunk `hb2026-p020-replacement`, PDF20/printed9, score0.815428; return chunk
score0.763087. `handbook-handoff.json` retains the real result, official2026/27
PDF SHA108956feb2ffac665f8ca0f5a8f68d7150a85fda15e219916785ec50331a4e94,
MiniLM revision1110a243fdf4706b3f48f1d95db1a4f5529b4d41/384D/attention-masked
mean/L2-normalized identity, matching query-vector/bundle hashes and four
lifetimes. It uses six short extracts, not the full137-page PDF. This direct
retriever check made no model call; no keyword search or fake vectors were used.
The lecture distinguishes this index, saved history, transient prompt and audio.
Current Godot 4.7 docs were resolved and queried through Context7 before API
work: Movie Maker/CLI timing, node physics and Project Manager/import/single-
window editor behavior. Public sources are linked from the README. No shared
workflow, remote class, presenter change, paid call or external message was
made by this author. Classroom rehearsal and independent review remain separate.
