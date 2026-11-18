# Week 11: authentication, deployment and creative agents

**Thursday 19 November 2026.** Choose **one** route for this separate
120-minute tutorial: deploy a small GitHub-authenticated app with a private
persistent note, or ask an agent to use Blender and bring the same object into
Godot. Both use the same workflow: state a goal, let an agent work on a branch,
inspect its diff, check
the result, open a PR, request a revision and review the new evidence.

The lecture teaches authentication/deployment first, then creative tools;
here you make and verify a change. Explain
an agent's available actions and stopping condition, distinguish a tool
acknowledgement from a useful result, and show how review changes the next
attempt. The authentication route connects Week 10's fictional local identities
and stored rows to a verified GitHub identity. The handbook embedding index
remains the source of handbook knowledge; login/session and conversation
history serve other jobs.

## Choose a route and prepare

| Minutes | Route A: authenticated app | Route B: Blender into Godot |
| --- | --- | --- |
| 0-15 | Copy template; local checks and signed-out page | Check tools; render the baseline |
| 15-35 | Trace identity/session/note; prepare own accounts | Inspect scene/Python, predict size; give a visual goal |
| 35-55 | Evidence-first PR; a small new UI behavior | Agent edits, renders and inspects; review first result |
| 55-65 | Break | Break |
| 65-85 | Secrets, deployment/sign-in or local fallback | Review request; agent revises/rerenders same PR |
| 85-100 | Persistence, isolation, failure and recovery | Export same object; import/check/view in Godot |
| 100-120 | Scheduled tutor review and group-project support | Scheduled tutor review and group-project support |

Do not try to finish both routes in two hours. If your chosen route has no
first result by minute 15, pair with a prepared machine and take turns.
Keep your own goal, diff, observation and review note. A recording can orient
you; it does not establish that your copy works. If account setup blocks
Route A, use its local tests and a prepared partner, with live
sign-in/deployment explicitly marked **not tested** when unavailable.

Both routes need Git, GitHub and a code editor. Use the coding agent already
available in your course environment; a live model may need your own account
or quota. No paid model/API is required for the core exercise: a partner can
make the proposed edit and review it using the same evidence. Label that
**human-directed work**, not an autonomous model run. Never put tokens,
cookies, client secrets or `.dev.vars` contents into an agent prompt.

- **Route A:** Node.js **22.23.3** (the template CI version) or a newer
  supported release, with npm; see the
  [template prerequisites](https://github.com/sd5913/github-oauth-d1-template#readme).
  Live deployment also needs internet, your **personal GitHub OAuth App**
  and your own Cloudflare account/Worker/D1 database. The local checks require no
  deployment credentials. The template is a separate application repository;
  do not add its packages to this PFAD Python environment.
- **Route B:** [Blender](https://www.blender.org/download/),
  [uv](https://docs.astral.sh/uv/),
  [Godot 4 standard build](https://godotengine.org/download/) and a desktop.
  The new handoff is tested on Linux x86_64 with Blender **5.3.0**, Godot
  **4.7.2** and uv **0.13.8** on 18 November. Earlier bridge acceptance
  used Blender 5.2.3 LTS. Install these applications before class; installers
  are substantial downloads. The small local render/export takes seconds.
  Windows/macOS are not rehearsed here. No dedicated
  GPU or downloaded assets are needed. `bpy` runs inside Blender's Python;
  do not install it into uv's environment.

Use [the shared PR worksheet](agent-pr-workflow.md) throughout. Its concrete
Blender reviewer request is a rehearsed scenario, not a transcript of a model
choosing actions. Retain your own actual agent/partner evidence.

For Route B use a personal PFAD fork/copy for your practice PR; do not target
the course's repository. While [Week 11 PR #14](https://github.com/sd5913/pfad/pull/14)
is unmerged, its supplied files are on `plan/week11-companion-activity`,
not yet `2026`. On GitHub's **Fork** page include all branches (uncheck the
option to copy only the default branch), then clone your fork's Week 11 branch:

```bash
git clone --branch plan/week11-companion-activity https://github.com/YOUR-ACCOUNT/pfad.git pfad-week11
cd pfad-week11
```

Replace `YOUR-ACCOUNT` with your account; keep an existing course clone
separate. The practice PR's base is your own fork's Week 11 branch. Check
`git remote -v` before pushing. This does not replace the group's required
`sd5913`-owned project repository. After an authorised course merge, the
instructor can direct you to `2026` instead.

## Route A: GitHub sign-in and a private persistent note

### 0-15: copy the template and check it locally

Open [sd5913/github-oauth-d1-template](https://github.com/sd5913/github-oauth-d1-template)
and choose **Use this template** to create your exercise repository under
your personal account, so you can administer its repository Secrets. Clone
that copy. From its root, replacing the sample repository URL/name:

```bash
git clone https://github.com/YOUR-ACCOUNT/YOUR-EXERCISE-REPO.git
cd YOUR-EXERCISE-REPO
npm ci
npm test
npm run typecheck
npm run build
npm run db:migrate:local
npm run dev
```

Keep terminal A running; open `http://127.0.0.1:3000`. Terminal B, in the
same repository, runs checks/Git. Stop the server with Ctrl+C. Follow the
template's supported Node/npm versions. First install needs npm access.
Sign-in needs the local OAuth configuration below, but credential-free checks
can run first. Expect the signed-out page and no private note; trying sign-in
before configuration is not expected to succeed. Tests use mocked OAuth
responses; they do not prove a real GitHub login or Cloudflare deployment.

### 15-35: trace identity and prepare personal accounts

Inspect `app/api/auth/github/route.ts`,
`app/api/auth/github/callback/route.ts`, `lib/handlers.ts`, `lib/session.ts`,
`app/api/note/route.ts`, `migrations/0001_notes.sql` and the deploy workflow in
your template copy. Trace this sequence:

1. `GET /api/auth/github` redirects to GitHub and sets a one-time state value.
2. GitHub returns to `APP_URL/api/auth/github/callback`; the callback verifies
   state, exchanges the short-lived code and reads GitHub's profile.
3. The app identifies the user by **immutable numeric GitHub ID** and signs a
   session cookie. A typed login name or owner ID is not proof of identity.
4. `GET /api/note` and `POST /api/note` select/update only that session user's
   D1 row. POST accepts JSON `{"body":"..."}`, maximum 2000 characters.
   `POST /api/auth/logout` ends the session.

Authentication answers "who signed in?"; an owner check answers "may this
user read/change this row?" A valid login alone does not answer the second
question. Cookies are not the stored note. A process restart must not erase
D1; an expired session should require sign-in again.

In **your personal GitHub settings**, open **Developer settings > OAuth Apps
> New OAuth App** (or **Register a new application**). Choose a public name
and homepage. Register the exact local callback:
`http://127.0.0.1:3000/api/auth/github/callback`. Generate a client secret and
store it privately. This is a personal **OAuth App**, not an installable
GitHub App. No PAT or private-repository `repo` scope is needed for sign-in.

Copy `.dev.vars.example` to `.dev.vars` using your editor, then enter your
local App client ID, client secret and a fresh session secret as the template
instructs. This file is ignored by Git. `APP_URL` defaults to
`http://127.0.0.1:3000`. Restart the local server after configuration changes.
For deployment use the final HTTPS Worker origin with **no trailing slash**
and callback `APP_URL/api/auth/github/callback`. Separate local/deployed
OAuth App registrations make the different origins easy to inspect.

In your own Cloudflare account, prepare the Worker name, account ID and D1
database using the template's setup steps. The D1 binding is `DB`; the remote
database ID identifies your database, while local migrations create a separate
local database. Create a deployment API token with the documented Workers/D1
permissions. Choose the Worker URL before setting the deployed callback;
compare the strings character by character.

Never ask an agent to obtain, read or repeat credential values. Give it
variable **names** and redacted errors, not local-file contents, OAuth codes,
cookies or secret-bearing screenshots. An agent should not need deployment
credentials to make or test the small code change below.

### 35-55: inspect first, then make a real agent change

Follow the [shared workflow](agent-pr-workflow.md#the-shared-workflow).
The template already shows save feedback, a 2000-character count and retains
text after a failed save. Ask the agent to inspect `app/note-editor.tsx`, run
checks and open the first PR with an evidence note. Do not request those
existing features again. The worksheet gives the exact request.

The reviewer then requests a **Discard unsaved changes** button: restore the
last successfully loaded/saved body without a network request. Disable it
when unchanged or saving. This small new UI behavior must preserve signed
sessions and owner-scoped queries. Revise the same PR and observe
edit/discard, save/edit/discard and failed-save/discard.

```bash
npm test
npm run typecheck
npm run build
git diff --check
git diff
```

Have a partner check the focused diff. For visible Discard acceptance, use
your own real sign-in or a prepared partner machine already signed in and
running the proposed revision. Take turns typing fictional text, discarding,
saving, editing and discarding again; check browser Network for no discard
request, then record the observations in the same PR. The partner keeps
control of their account/session; do not share passwords, cookies or secrets.
Existing server tests do not prove this UI behavior, and the template has no
browser fixture-login route. Add focused behavior coverage if your copy has
a UI test harness; distinguish that from the actual browser observations.

If neither your own sign-in nor a prepared session is available, inspect the
code/diff, run the local checks and revise the same PR, marking **Discard UI
acceptance UNTESTED**, along with any unavailable live sign-in/deployment
checks. Ask the tutor for a prepared machine, or choose the prepared Blender
route if available. Local backend fixtures cannot complete the UI check.

### 55-85: break, repository secrets and deployment

Keep the full 55-65 break. In your exercise repository open **Settings >
Secrets and variables > Actions > New repository secret**. Enter **all eight**
names here, one at a time. Some are public identifiers; one setup location
holds the complete deployment configuration for this exercise.

| Repository secret | Value you supply |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | Your Cloudflare deployment token |
| `CLOUDFLARE_ACCOUNT_ID` | Your Cloudflare account ID |
| `CLOUDFLARE_D1_DATABASE_ID` | Your own remote D1 database ID |
| `CLOUDFLARE_WORKER_NAME` | Your chosen Worker name |
| `APP_URL` | Your final HTTPS application origin |
| `OAUTH_CLIENT_ID` | Your deployed personal OAuth App client ID |
| `OAUTH_CLIENT_SECRET` | That OAuth App's client secret |
| `SESSION_SECRET` | A fresh random signing secret from the template's command |

Repository secrets belong to **GitHub Actions**. The deployment workflow
reads them, configures your Worker/D1, applies remote migrations and maps
`OAUTH_CLIENT_ID` to runtime `GITHUB_CLIENT_ID`, `OAUTH_CLIENT_SECRET` to
runtime `GITHUB_CLIENT_SECRET`, and `SESSION_SECRET` to the same runtime name.
GitHub reserves the `GITHUB_` prefix for Actions secrets, so the repository
and runtime names differ. These become **Worker runtime secrets**. The running app
needs those values after the Actions job finishes. Saving repository secrets
alone does not inject them into an already deployed Worker. PR checks run
without deployment credentials; green checks are not a deployed app.

Follow the template's main/manual Actions deployment path, confirm the job
succeeded, then open the `APP_URL` you configured. GitHub may mask that URL
in logs because it is a repository secret. The template exposes `npm run deploy`
(build, remote migrations, deploy with runtime secrets) for the configured
Actions environment. A local invocation needs all eight production environment
values supplied through a secure mechanism, not the local `.dev.vars` file;
follow the template README. Use your own infrastructure. Verify the URL matches `APP_URL` and
the OAuth callback before sign-in. Retain only the public URL and a redacted
success/failure note; never retain authorization codes or cookies in a PR.

### 85-100: persist, isolate, fail and recover

Use a short fictional note with no personal information. Record which of
these checks you actually ran:

| Check | Expected observation |
| --- | --- |
| Signed out | Private note API rejects access; no saved note displayed |
| Account A signs in and saves | Its own note appears; save succeeds |
| Reload | Account A's saved note reappears |
| Stop/restart local server | Note survives; sign in again if needed |
| Account B in a separate browser profile | A's note is absent; B has its own empty/different note |
| B saves, then A reloads | A's note remains unchanged |
| Deny GitHub authorization | No authenticated session created |
| 2001 characters sent to the API | Server rejects the save |

For the last check, the UI may prevent typing/sending more than its limit;
inspect the oversized-body test rather than bypassing it in the browser.
Account B should be a willing partner using their own profile/credentials.
Never share cookies or sign in as someone else. Inspect tests for forged or
expired sessions, invalid state and owner-scoped queries; these are distinct
from a real two-account browser check.

For a credential-free **real local Worker/D1** check, run:

```bash
npm run build
npm run test:local
```

This needs no `.dev.vars` or cloud credentials. It starts the built Worker
with an isolated local D1 database, uses fixture
signed sessions, checks two-user isolation and restarts against the same
store, then shuts down. It demonstrates local runtime/persistence behavior,
**not GitHub sign-in, NoteEditor/Discard UI behavior or remote Cloudflare
acceptance**. It supplies no browser fixture-login route; its fixtures are
not credentials for your deployed app.

If sign-in fails, compare callback, `APP_URL` and local/deployed origin;
do not remove state/cookie checks. If a note disappears after restart, verify
the same database/binding is being reopened. A newly created empty database
is a different store. For Actions failures inspect the first failing step and
secret **names**, not values; correct configuration, redeploy and rerun the
affected check. Do not delete databases as routine recovery.

Without credentials, run the local checks, inspect the mocked OAuth tests,
and make/review your UI change on the same PR. Use an already signed-in
prepared partner machine running that revision for the visible check above,
without sharing credentials. If no prepared session exists, mark **Discard
UI acceptance UNTESTED**, retain the useful code/diff/test evidence and ask
the tutor, or choose a prepared Blender route if available. Record exactly
what you observed and which live checks remain open.

## Route B: a sculpture made with an agent, then used in Godot

### 0-15: render and inspect a baseline

From the PFAD exercise repository root:

```bash
cd week11
blender --version
godot --version
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.25 --output .output/blender/before
```

Keep this directory for the remaining commands. On macOS Blender is commonly
in `/Applications/Blender.app/Contents/MacOS/`; add its directory to PATH.
For an executable named `godot4`, check `godot4 --version` instead; the helper
also accepts `GODOT_PATH` pointing to the standard Godot 4 executable.
uv uses this week's separate environment. Blender creates a disposable scene,
without loading personal work. Open `.output/blender/before/sculpture-1.25.png`,
`inspect.json` and the saved `sculpture.blend`. Expect a terracotta cube on
a floor, camera `[7,-9,6]`, scale `[1.25,1.25,1.25]` and process exit 0.
An old PNG does not prove a new run succeeded; retain PATH/render errors
and pair with a prepared machine if there is no first result by minute 15.

### 15-35: inspect, predict and give a visual goal

Read [blender_scene.py](blender_scene.py). A scene contains objects; a mesh
holds vertices/faces, its object's transform places it, and a material
controls surface appearance. Camera/light change the view without changing
mesh geometry. `bpy.data.objects.get("Sculpture")` finds the named object;
`target.scale` changes a three-number vector. The cube has side 2, so scale
1.25 gives dimensions `[2.5,2.5,2.5]`. Centre z is 1.25:
`bottom_z = centre_z - height/2 = 0`, on the floor.

Assignment, saving the scene and rendering an image are different actions.
CPU Cycles renders a 640x480 eight-sample check. The optional
[blender_variants.py](blender_variants.py) loop gives two controlled camera
views; it is deterministic code, not an agent deciding its next action.
Predict how a wider, shallower sculpture will look before requesting an edit.

### 35-55: let the agent use Blender

Use the [actual Blender-use prompt](agent-pr-workflow.md#ask-an-agent-to-use-blender).
The agent may inspect/edit the scene script, run Blender, inspect the saved
JSON and PNG, and revise after observing the result. Keep the named Sculpture,
material, camera and floor contact. A bridge is optional; CLI tool use lets
the agent operate the real application too. Stop with a focused diff and
actual render evidence. Do not attribute model decisions to a fixed script.

For the first edit use x scale `1.6 * s`, y `0.75 * s`, z `s`. At `s=1.25`
predict scale `[2.0,0.9375,1.25]`, dimensions `[4,1.875,2.5]`, bottom z 0.
Open the fresh PNG before accepting the report; inspect unexpected edits
before running them. Keep separate before/first/revised output folders.

```bash
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.25 --output .output/blender/first
git diff --check
git diff -- blender_scene.py
```

Open a practice PR with the goal, observed agent/partner actions, focused diff,
commands and before/after images. Keep generated scenes/models/caches ignored;
attach images and an evidence note manually. With no model access a partner
performs the edit/run/inspection; label it **human-directed fallback**. This
still practices Python/state/review, but does not demonstrate a model loop.

### 55-85: break, review and revise the same PR

Keep 55-65 as break. A reviewer asks: **keep vertical size, camera, material
and floor contact; reduce width to `1.3 * s` instead of `1.6 * s`.**
Pass that request to the agent on the same branch/PR. At `s=1.25` expect
scale `[1.625,0.9375,1.25]`, dimensions `[3.25,1.875,2.5]` and bottom z 0.
Have it rerender under `.output/blender/revised`, inspect image/JSON and
explain whether another revision is needed before stopping.

```bash
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.25 --output .output/blender/revised
git diff --check
```

A human reviews the result and decides on merging; the practice PR can stay
open. The worksheet also retains the optional camera-review scenario. Keep
the camera fixed for a proportion comparison so the cause is explainable.

### 85-100: export the same Sculpture and view it in Godot

Use the **saved revised scene**, rather than silently rebuilding a cube:

```bash
uv run python asset_handoff.py export .output/blender/revised/sculpture.blend
uv run python asset_handoff.py check
uv run python asset_handoff.py play
```

If you kept the baseline unchanged, substitute
`.output/blender/before/sculpture.blend` (also the default export source).
Close the Godot window with its close button. No service/bridge is started.
Predict revised dimensions in Godot: `[3.25,2.5,1.875]` because Blender Z-up
becomes Godot Y-up. Inspect `export.json` and `check.json` in `.output/godot3d/`.
The baseline instead has `[2.5,2.5,2.5]` in both applications.

Read [blender_export.py](blender_export.py): load the saved `.blend`, select
only the mesh **Sculpture**, put its origin/pivot at the bottom centre in the
export copy, and bake scale into vertices. Export meshes/materials together
as `.output/godot3d/sculpture.glb`. The source `.blend` is not rewritten.
The exporter converts axes; do not add a manual 90-degree rotation too.
`.blend` is the editable source, `.glb` the portable handoff.

[preview.gd](godot3d/preview.gd) loads the imported GLB as a `PackedScene`,
instances it under a `Node3D`, then supplies its own floor, camera and light.
The asset stays at origin with bottom Godot y=0. The existing `godot/` game
is `Node2D`, so a separate small **3D preview** hosts this mesh. Rendering does
not create collision: a solid playable object needs a chosen collision shape.
`check` performs actual engine import and scene instantiation, checking one
mesh, positive dimensions, floor contact and the terracotta material.
Lighting differs from Blender; shared material values do not imply pixel parity.

For an actual engine frame:

```bash
uv run python asset_handoff.py capture
```

Open `.output/godot3d-preview.png`. This is drawn by the running renderer,
not the headless checker. Linux uses `xvfb-run` when installed to avoid focus
changes; otherwise capture needs a working display. Windows/macOS capture is
untested; `play` is the normal visible acceptance check. No API costs/assets.

Predict a missing-source error, run it, then recover:

```bash
uv run python asset_handoff.py export .output/blender/MISSING.blend
uv run python asset_handoff.py export .output/blender/revised/sculpture.blend
uv run python asset_handoff.py check
uv run python -m unittest test_asset_handoff -v
```

First command must exit nonzero with `Source .blend not found`, without
launching Blender. An earlier GLB is not a new successful export. Restore a
valid source and rerun. Renaming Sculpture fails export; restore its name.
If it floats, fix source floor contact rather than rotating/scaling randomly
in Godot. Commands have timeouts; use Ctrl+C for a stuck process and retain
the error before retrying. The test exports an isolated baseline, not your
artwork; it cannot decide if your creative revision is good.

## Optional: inspect a live Blender bridge

[MCP for Blender](https://github.com/ahujasid/mcp-for-blender), by Siddharth
Ahuja, offers a broader third-party bridge. The supplied setup pins add-on
commit `8782963ba87a4c90482198bd7c7e17219ac3a0f7` and
`mcp-for-blender==2.2.6`, retaining its MIT notice in ignored `.tools/`.

```bash
uv run python setup_blender.py
uv run python blender_live.py
```

This opens a separate **disposable** Blender window, binds the add-on to a
free loopback port, and drives the community server over stdio. Do not open
personal work in that window. It inspects Sculpture, changes uniform scale
to 1.5, reinspects, renders and saves `sculpture-live.png/.blend` under
`.output/blender/`. After looking at the window, press Enter in the terminal
to stop the client/add-on and close the process. Result JSON must show scale
`[1.5,1.5,1.5]`, `blender_exit: 0` and `socket_closed: true`.

`get_scene_info` reads live state; the bounded adapter reads a saved inspection.
`execute_blender_code` runs Python inside Blender and has much broader powers;
the demo supplies reviewed code only. Telemetry/update checks are disabled;
asset-generation tools are outside this exercise. The demo resets scale to a
uniform value, so keep your separate proportion renders if using the extension.
Tutors can run `uv run python blender_live.py --verify` for automatic closure;
it still exercises real graphical Blender and needs a working display.

## 100-120: tutor review and project support

Show your goal, focused diff, actual result, failure/recovery, reviewer request
and revision on the same PR. Explain what your checks prove and what remains
untested. A human decides on merging. These practice artifacts add no upload
or grade. Use the scheduled **19 November** tutor discussion for what works,
feedback, one blocker and the team's next testable step.

The group project remains **40%**; **25% idea / 50% code / 25% execution**, due
**6 December 2026, 23:59 HKT**. Use a shared public **`sd5913`-owned** repository
with teammate Write access. Your personal OAuth App and Cloudflare account
do not change that requirement. Configuring Secrets in an organisation group
repository needs repository Admin access; teammate Write access alone does
not grant it. Use the personal exercise copy for today's setup.
GitHub Projects is recommended; an equivalent
accessible progress record is valid. Follow Canvas submission instructions.
Agents, authentication and Blender are inspiration, not compulsory features
or a defence.

## Week 12 preparation and optional connections

The earlier Godot world, bridge and recording instructions are retained in
[Godot preparation for Week 12](godot-week12-preparation.md). The small 3D preview above belongs to Route B; the 2D world remains
Week 12 preparation. Week 12 provides first-time setup/orientation followed
by its bounded agent/check/revise/film sequence; pair if its baseline still
fails after the allocated setup time.

[The archive](https://github.com/sd5913/pfad/tree/2025/week11) also includes
TouchDesigner, OSC/handtracking, NDI and a networked game. OSC carries addressed
control messages; NDI carries audio/video. An OSC send does not prove a
receiver used it, just as a tool response does not prove a good render.
Week 9 supplies the network/vision-message bridge. These are optional
connections, not extra installations. Orange/t-SNE/matrix projection were
removed by instructor decision; Week 10 retains handbook embeddings/retrieval.

## Sources and verification limits

Authentication/bridge setup documentation was checked through Context7 on 15 November 2026:
[Blender command line](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html),
[Blender API](https://docs.blender.org/api/current/),
[creating an OAuth App](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app),
[Actions secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets),
and [D1 migrations](https://developers.cloudflare.com/d1/reference/migrations/).
Blender glTF export and Godot import/movie APIs were checked through Context7
on 18 November 2026: [Blender glTF](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html),
[Godot 3D import](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/index.html)
and [command line](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html).
Use the [template README](https://github.com/sd5913/github-oauth-d1-template#readme)
for tested versions and exact configuration. Blender is GPL-licensed; the
community bridge/MCP SDK are MIT-licensed. Geometry is original course code;
no downloaded assets are required.

See [the asset-handoff evidence](asset-handoff-20261118.md) and
[the earlier verification record](verification-20261115.md) for actual Blender
commands and limits. Tests, headless renders, a live application bridge and
a model choosing actions are different evidence. No model episode,
student-account GitHub login or remote Cloudflare deployment is claimed by
this documentation update. Windows/macOS and projected classroom display
still need rehearsal. Retained Godot evidence is dated separately in its
preparation appendix.
