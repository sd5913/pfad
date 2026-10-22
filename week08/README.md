# Week 8 — one piece that works (Thu 29 Oct 2026)

Bring your [Week 7 idea and mock-up](../week07/README.md). Today your team
will choose one small interaction, make a change reviewable, distinguish two
kinds of project setup, and map one hand landmark to a tile response. These are
working notes, **not a new assessed submission**. Ask your instructor about
team scope under the current project brief; do not invent a new deadline.

## 1. Team plan and pull request

1. Name a visitor, one action, and one visible response. Example: "When the
   visitor's index fingertip moves left, the blue tile lights up; when it moves
   right, the red tile lights up." Agree what happens with no hand in view.
2. Put the smallest working slice first: draw tiles, map a coordinate, show
   feedback, ask a teammate to test; defer extra gestures, sounds, and other
   features to a backlog. Call the working slice an **increment**. Use these
   Scrum terms to communicate, not as mandatory new team roles.
3. On a small feature branch in **your team's repo**, commit one focused change
   and open a pull request. State what changed, how to run it, what you actually
   tested, and what remains untested. A teammate reviews the code **and tries
   the interaction**. Resolve conflicts together and test again after merging.
   A green PR check is not proof of a usable visitor experience. See the
   [Git reference](../reference/git.md); this exercise does not ask you to
   merge or publish the course repository.

An earlier [two-object class trace](tile_demo.py) remains available:
`python -B week08/tile_demo.py` prints `Before: blue=False, red=False` then
`After:  blue=True, red=False`. It models independent object state, **not**
a clickable UI or hand tracking. This week's visible interaction is below.

## 2. Safe, repeatable setup (no accounts or real keys needed)

Swap run instructions with a teammate: working directory, exact command,
packages, safe inputs, expected output, and how to stop. Never paste a real
credential, private roster, or camera frame into a public repo, PR, prompt,
log, or screenshot. The tile sample needs only Python 3 and no key. Discuss
these two separate services with **fake values only**; don't create a secret,
environment, account, or deployment for this exercise:

| Question | GitHub Actions environment | Codex cloud environment |
|---|---|---|
| Where? | Repository's **Settings → Environments** (admin permissions may be needed) | Codex cloud settings for a connected repo, if your team actually uses Codex cloud |
| What for? | Deployment protection rules and environment-scoped variables/secrets used by **jobs** that reference that environment | Reproducible cloud task runtime: setup commands, dependencies, variables, and separately managed secrets for a Codex **agent task** |
| How is a value used? | A workflow job explicitly declares `environment: demo`; its steps can reference `secrets.DEMO_TOKEN` if an admin has separately configured it | A Codex cloud task uses the settings of its selected cloud environment; this does **not** configure a GitHub Actions job |
| Here? | Paper example only: `DEMO_TOKEN=NOT_A_REAL_TOKEN` | Paper example only: `DEMO_TOKEN=NOT_A_REAL_TOKEN` |

A GitHub workflow file does **not** contain the secret's value. Environment
secrets are not available to a job until its environment's protection rules,
if any, pass. Conversely, creating a Codex cloud environment does not grant
GitHub Actions access to its settings, and neither service gives an agent
permission to use a tool just because it is installed. Don't expose secrets
to untrusted pull-request code. For the real project, ask your team which
service (if either) is used and who can manage its settings; use only the
minimum access necessary. Our offline example below uses **neither** service.

References: [GitHub: managing environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments),
[GitHub: using secrets in workflows](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets),
[OpenAI: Codex cloud](https://developers.openai.com/codex/cloud).
Settings and availability can vary by plan or organisation; check current
provider guidance rather than assuming everyone has an account.

## 3. Hand → coordinate → tile

[Open `hand_tiles.py`](hand_tiles.py). It uses the MediaPipe **Hand Landmarker
Task** only in explicit camera mode. The first detected hand's **index
fingertip, landmark 8**, has a normalized horizontal coordinate `x`.
We mirror the camera frame so moving your hand left selects blue. Both paths
call the same `tile_for_x(x)` function:

| `x` | Visible response |
|---|---|
| `0 <= x < 0.5` | highlight `[ BLUE ]`; red is plain |
| `0.5 <= x <= 1` | highlight `[ RED ]`; blue is plain |
| no hand, invalid or out-of-range coordinate | neither selected; show `no input` immediately |

**First, no camera or installation.** From the `pfad` repo root:

```bash
python -B week08/hand_tiles.py
python -B -m unittest discover -s week08 -p 'test_*.py'
```

If `python` isn't Python 3 use `python3` (or `py -3` on Windows). The five
built-in test coordinates are `0.20, 0.49, 0.50, 0.80, None` and are not
camera data or MediaPipe predictions. Expect blue, blue, red, red, then
`no input` in the terminal's visible tile strip. In particular `0.50` is red.
The tests use only the standard library; no device, model, network, packages,
or permission prompt. Change one sample coordinate (for example, `0.49` to
`0.51`), predict the result, run again, and restore it. The terminal strip
is a deliberately simple visible tile display, not a window or a gesture
recognizer. Try a different threshold in `tile_for_x` **and its tests** if
your design calls for it.

**Optional local webcam on a machine with a camera and graphical desktop.**
Ask permission before pointing a camera at anyone. Install packages in your
own isolated Python 3.12 environment, and obtain the model from the
[Google Hand Landmarker guide](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python)
([Google sample model download](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)).
Place the downloaded `.task` **outside your repo**, then run from the repo
root, replacing the path with your own downloaded file:

```bash
uv run --no-project --python 3.12 --with mediapipe --with opencv-python --with numpy week08/hand_tiles.py --camera --model /path/outside/pfad/hand_landmarker.task
```

This optional command requires `uv`, network for first-time package install,
a compatible desktop/webcam, camera permission, and a **manually downloaded**
model. It never downloads a model by itself. `--camera` is the only path that
opens the camera. The local window shows only the coloured tile display, not
the video feed; press `q` in that window to release the camera. Code does not
write frames, record audio/video, or upload anything. Close other apps using
the camera if it cannot open. Camera hardware and MediaPipe's inference are
**not** exercised by the offline tests or CI. If you cannot or do not wish to
use a camera, use the sample command and describe that limitation honestly.

Talk it through: where is the input acquired, which line extracts landmark 8,
which function maps both kinds of `x`, and where is the response drawn? Have a
teammate try the no-camera command; ask them whether `no input` is clear enough
without labels or sound. A visitor test is still needed for your own project.

## Sources and scope

- [Google Hand Landmarker Python guide](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python): Tasks API, 21 landmarks per hand, normalized image coordinates, video mode. Historical [2025 Week 8](https://github.com/sd5913/pfad/tree/2025/week08) offers broader vision examples but is not the required 2026 setup.
- The older Week 8 PDF covered team workflow, branches, containers and vision; it is background, not a 2026 deadline or a Docker/Compose requirement. The former container paper trace is **not** part of this Week 8 core.
- The [PR checks](../.github/workflows/upcoming-practicals.yml) run these offline tests; they do not install MediaPipe, access the camera, set secrets, deploy, or publish this course.
