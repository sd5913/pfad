# Week 12 verification record

29 October 2026. **Full production acceptance incomplete.** No playable film,
graphical application acceptance, first-time graphical bootstrap timing or
prepared-partner rehearsal has passed here. The new long lecture deck has not
been authored; the incumbent addition/MCP deck remains historical draft work.

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

## Missing proof and exact recovery route

The coordinator's current display transport connect returned EPERM. No further
GUI/crash attempt was made, and no headless black frames, dummy movie or fake
screenshot was generated. `world.py play`, visible replay and actual Movie
Maker/FFmpeg capture remain unaccepted here. The helper code checks a fresh
behavior result, engine completion, 960x540/about 4 seconds/120 frames, full decode
and sample extraction, but these capture operations still need actual exercise
on a graphics path. Metadata/decode checks alone cannot prove the intended
scene or action: view the real clip and all sample frames.

`ci-capture-candidate.md` supplies the coordinator with an ordinary read-only
public PR-runner proposal: current official 4.7.2 ZIP/checksum, Mesa software
OpenGL/Xvfb, actual engine tests/capture, ffprobe, full decode, samples and
seven-day artifact retention. It has not run. Nothing in this record claims a
CI artifact exists or that a runner substitutes for student bootstrap timing.

Official Linux 4.7.2 standard ZIP: 77,860,424 bytes, SHA-256
`cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4`.
The coordinator verified the current release. Cold download/extraction/
first visible baseline/capture duration is unmeasured. Windows/macOS setup,
all graphical paths and partner evidence retrieval are untested. A warm
installed Linux check is not a first-time graphical bootstrap. Before class,
recheck latest stable and time the README's 0-20 minute route; prepare and verify
a partner machine, rehearse each learner's turn and retrieval, and keep the
55-65 break/100-120 support blocks intact.

The W10 current handbook PDF/index/real-encoder/source-backed retriever proof
has not been supplied here. The tiny world has no handbook search dependency;
no fake retrieval or source claim is substituted. The conditional lecture
handoff remains an explicit open dependency.

Current Godot 4.7 docs were resolved and queried through Context7 before API
changes (Movie Maker/CLI timing; SceneTree and physics callbacks). GitHub Actions
read-only token/artifact retention docs were fetched for the CI proposal.
The README links primary sources and states precise prerequisites/limits.
No release, shared workflow, remote class, presenter, paid call or external
message was made by this author.
