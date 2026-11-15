# Week 11 verification: 15 November 2026

This records author checks for the [tutorial](README.md), not a claimed
student run or model episode. The existing implementation was retained.
No GitHub/Cloudflare credentials, student records or private notes were used.

## Environment and reuse

- PFAD source base: `41108250bcf2ae428dc819363bb32212b8f19fe7`.
- Linux x86_64; Blender **5.2.3 LTS**, build `e13b728c6880`; uv **0.13.7**.
- Reused `blender_scene.py`, `blender_variants.py`, the bounded
  `blender_tools.py`/`mcp_client.py`, and the existing community bridge helpers.
  No implementation replacement or source edit was needed.
- Community add-on tested pin remains
  `8782963ba87a4c90482198bd7c7e17219ac3a0f7`; package remains
  `mcp-for-blender==2.2.6`. Observed upstream HEAD on 15 November was
  `8f40787fbde8e6d8fe51c5a3553e5635fff40d2b`, **not** a tested update.
  Setup/refetch of the existing pin completed successfully in this session.
- Godot bridge observed HEAD remains
  `1209744fad78f3998f98c7394fd0f6ef50da5281`. Its retained graphical evidence
  is dated 29 October in [the preparation appendix](godot-week12-preparation.md).

## Commands and observations

Run from `week11`. Blender processes used separate ignored configuration/cache
paths under `.output`, as the supplied helpers do. Generated PNGs, `.blend`
files, scripts and logs remain ignored rather than committed to PFAD.

| Command/check | Observed result |
| --- | --- |
| `uv run python -m unittest test_world test_mcp_transport test_mcp_cleanup test_mcp_client_status test_engine` | 7 tests, no failures or skips; exit 0 |
| Direct `blender_scene.py` runs at scale 1 and 1.5 using the README's CLI flags | Each exited 0 and produced PNG, `.blend`, inspection |
| `uv run python blender_variants.py` | Both supplied camera runs exited 0; separate images/records |
| `uv run python mcp_client.py --blender list` | Two bounded tools discovered; exit 0 |
| `uv run python mcp_client.py --blender render_scene '{"scale":1.25}'` | Fresh render/inspection at scale 1.25; exit 0 |
| `uv run python mcp_client.py --blender inspect_scene` | Read the saved inspection; exit 0 |
| `uv run python mcp_client.py --blender render_scene '{"scale":5}'` | `isError: true`, exit 1, rejected before Blender launch |
| Direct `blender_scene.py -- --target MissingObject` with README flags | `Missing object: MissingObject; use Sculpture`, exit 1 |
| Repeat valid adapter render after failures | Fresh successful render/inspection; exit 0 |
| `uv run python setup_blender.py` | Reinstalled/refetched the existing tested bridge pin; exit 0 |
| `uv run python -m unittest test_blender_live` | 1 real graphical Blender/bridge/render test, passed; exit 0 |

The live acceptance test starts the community bridge, discovers its tools,
changes the real Sculpture object, reinspects it and saves/renders before
closing. Its result showed uniform scale `[1.5,1.5,1.5]`, Blender exit **0**
and `socket_closed: true`. This is a real application/bridge run with a fixed
request sequence; it does not demonstrate autonomous model decisions.

### Camera review scenario

The exact direct commands in the [worksheet](agent-pr-workflow.md) produced
three separate 640x480 PNGs and saved scenes. All processes exited 0:

| Output folder under `.output/camera-review/` | Camera | Sculpture scale |
| --- | --- | --- |
| `before-1` | `[7,-9,6]` | `[1.25,1.25,1.25]` |
| `before-2` | `[9,-7,6]` | `[1.25,1.25,1.25]` |
| `revised-2` | `[5,-10,6]` | `[1.25,1.25,1.25]` |

All three PNGs were visually inspected: the sculpture is uncropped, with
floor/shadow visible, and the revised second view shows more front and less
side than the original second view. A separate Blender process loaded the
revised saved `.blend` and checked the object's transformed bounding box:
dimensions `[2.5,2.5,2.5]`, location `[0,0,1.25]`, bottom z **0.0**.
This was a deterministic author rehearsal using existing CLI parameters;
no live model or historical reviewer conversation is claimed.

### Optional proportion scenario

Temporary copies of `blender_scene.py` changed only the scale assignment,
leaving the tracked implementation intact. At input scale 1.25:

| Attempt | Scale | Process |
| --- | --- | --- |
| Uniform baseline | `[1.25,1.25,1.25]` | Exit 0, fresh PNG/scene |
| x factor 1.6, y factor 0.75 | `[2.0,0.9375,1.25]` | Exit 0, fresh PNG/scene |
| x factor 1.3, y factor 0.75 | `[1.625,0.9375,1.25]` | Exit 0, fresh PNG/scene |

Camera stayed `[7,-9,6]`. The revised PNG was visually inspected. A separate
Blender process loaded its saved `.blend`: dimensions `[3.25,1.875,2.5]`,
location `[0,0,1.25]`, transformed bottom z **0.0**. Temporary copies and
outputs are under ignored `.output/workflow-rehearsal/`.

## What these checks do not establish

No model chose actions in these deterministic author commands. The learner
must record their own agent decisions or label their human-directed fallback.
A saved inspection differs from live scene state; a fresh headless render
differs from projected classroom viewing. Windows/macOS remain untested.

The authenticated route consumes the separate template's documented interface.
Its mocked OAuth/local runtime tests and actual credential-dependent browser
acceptance must be reported separately. This PFAD rehearsal does not establish
a personal GitHub login, remote Cloudflare deploy or real two-account
isolation. No such remote action was performed here.
