# Week 11: agents, Blender and authenticated apps

**Thursday 19 November 2026.** Choose **one** route for this separate
120-minute tutorial: change and render a Blender sculpture, or deploy a small
GitHub-authenticated app with a private persistent note. Both use the same
workflow: state a goal, let an agent work on a branch, inspect its diff, check
the result, open a PR, request a revision and review the new evidence.

The lecture explains the systems; here you make and verify a change. Explain
an agent's available actions and stopping condition, distinguish a tool
acknowledgement from a useful result, and show how review changes the next
attempt. The authentication route connects Week 10's fictional local identities
and stored rows to a verified GitHub identity. The handbook embedding index
remains the source of handbook knowledge; login/session and conversation
history serve other jobs.

## Choose a route and prepare

| Minutes | Route A: Blender | Route B: authenticated app |
| --- | --- | --- |
| 0-15 | Check tools; render the baseline | Copy the template; run local checks |
| 15-35 | Inspect scene code; state a visual goal | Trace identity/session/note; prepare personal OAuth and D1 |
| 35-55 | Agent branch, focused edit, diff and render | Agent branch, focused UI edit, checks and PR |
| 55-65 | Break | Break |
| 65-85 | Review request; revise the same PR; rerender | Repository secrets; deploy and test sign-in |
| 85-100 | Failure/recovery; explain evidence limits | Persistence and second-account isolation; recover |
| 100-120 | Scheduled tutor review and group-project support | Scheduled tutor review and group-project support |

Do not try to finish both routes in two hours. If your chosen route has no
first result by minute 15, pair with a prepared machine and take turns.
Keep your own goal, diff, observation and review note. A recording can orient
you; it does not establish that your copy works. If account setup blocks
Route B, use its local tests and a prepared partner, with live
sign-in/deployment explicitly marked **not tested** when unavailable.

Both routes need Git, GitHub and a code editor. Use the coding agent already
available in your course environment; a live model may need your own account
or quota. No paid model/API is required for the core exercise: a partner can
make the proposed edit and review it using the same evidence. Label that
**human-directed work**, not an autonomous model run. Never put tokens,
cookies, client secrets or `.dev.vars` contents into an agent prompt.

- **Route A:** [Blender](https://www.blender.org/download/),
  [uv](https://docs.astral.sh/uv/) and a desktop that can display the image or
  application. Tested on Linux x86_64 with Blender **5.2.3 LTS** and uv
  **0.13.7** on 15 November. Windows/macOS are not rehearsed here. No dedicated
  GPU or downloaded assets are needed. `bpy` runs inside Blender's Python;
  do not install it into uv's environment.
- **Route B:** Node.js **22.23.3** (the template CI version) or a newer
  supported release, with npm; see the
  [template prerequisites](https://github.com/sd5913/github-oauth-d1-template#readme).
  Live deployment also needs internet, your **personal GitHub OAuth App**
  and your own Cloudflare account/Worker/D1 database. The local checks require no
  deployment credentials. The template is a separate application repository;
  do not add its packages to this PFAD Python environment.

Use [the shared PR worksheet](agent-pr-workflow.md) throughout. Its concrete
Blender reviewer request is a rehearsed scenario, not a transcript of a model
choosing actions. Retain your own actual agent/partner evidence.

For Route A use a personal PFAD fork/copy for your practice PR; do not target
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

## Route A: a sculpture seen from two cameras

### 0-15: render a baseline

From the PFAD repository root:

```bash
cd week11
blender --version
uv run python -m unittest test_world test_mcp_transport test_mcp_cleanup test_mcp_client_status
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.25 --output .output/blender/before
```

Keep this directory for Route A commands. Blender must be on PATH; on macOS
its executable is commonly in `/Applications/Blender.app/Contents/MacOS/`.
uv uses this week's separate environment and lockfile. The script creates a
**disposable** scene in a new background process, without loading personal
`.blend` work.

Open `.output/blender/before/sculpture-1.25.png` and `sculpture.blend`.
A terracotta cube should sit on a floor, with a camera, light and shadow.
Read the adjacent `inspect.json`: `after` should be `[1.25,1.25,1.25]`, camera
`[7,-9,6]`, and application version should match your Blender. Expect process
exit 0 as well as files. On failure, read the error, check PATH and pair if
needed. An old PNG is not evidence that a new command succeeded.

### 15-35: inspect, predict and write the goal

Read [blender_scene.py](blender_scene.py) and
[blender_variants.py](blender_variants.py). `bpy.data.objects.get()` finds the
named object; `target.scale` is a three-number vector. The original cube has
side length 2, so scale 1.25 produces dimensions 2.5 by 2.5 by 2.5.
`target.location.z = options.scale` puts its centre at half its height:
`bottom_z = centre_z - height/2 = 1.25 - 1.25 = 0`, on the floor.

Assignment changes scene state, `save_as_mainfile()` saves it, and
`bpy.ops.render.render(write_still=True)` produces the image: three separate
results. CPU Cycles renders 640x480 at eight samples, a small check rather
than a final-quality artwork. `to_track_quat('-Z', 'Y')` aims the camera at
its target. Predict how a different camera changes the visible faces without
changing Sculpture's proportions.

```bash
uv run python blender_variants.py
```

Open `.output/blender/angle-1/sculpture-1.25.png` and the `angle-2` image.
Compare the two `inspect.json` files: cameras are `(7,-9,6)` and `(9,-7,6)`;
the sculpture scale stays 1.25. This deterministic loop makes two controlled
observations. It retains the archive's multi-angle dataset idea without a
large dataset or AI-generated mesh.

State the visual goal and a stopping condition before requesting an edit.
For example: keep the same sculpture, scale, floor contact, camera target,
light and material; make the second view show more of the front face and
less of the side. The worksheet gives a concrete camera revision and the
render/inspection evidence needed to judge it.

### 35-55: agent branch, focused edit and PR

Follow [steps 1-4 of the worksheet](agent-pr-workflow.md#the-shared-workflow).
Create your branch. In the worked scenario the two-camera implementation
already exists, so first ask the agent to inspect/render it and write a short
evidence note; do not request an unnecessary code rewrite. Inspect `git diff`
and check the note against your observations. Keep the original images for
review; the camera-code revision comes after the reviewer request.

```bash
uv run python blender_variants.py
uv run python -m unittest test_world test_mcp_transport test_mcp_cleanup test_mcp_client_status
git diff --check
git diff -- blender_variants.py blender_scene.py
```

The existing tests check transport/world behavior; they do **not** establish
that a new camera composition is good. Open a PR with your goal, focused diff,
commands, before/after images and known limits. Ask a partner to review the
image, not just the successful process exit. The worksheet shows how to save
images under separate output paths so rerunning does not erase the baseline.

### 55-85: break, then revise the same PR

Keep the full 55-65 break. A useful specific reviewer request is: "For the
second camera use `(5,-10,6)` instead of `(9,-7,6)`. Keep the first camera,
sculpture scale and floor contact. Show fresh images and inspection records."
Ask the agent to revise **the existing branch and PR**, inspect the new diff,
and rerun the preceding render/check commands. The changed second camera
should be `[5,-10,6]`; both sculpture scales should remain `[1.25,1.25,1.25]`.
The two PNGs should show the same sculpture from different views.

Reply to the review with the changed code and rerun evidence. A human decides
whether to merge after checking it. An agent's "done" message is not that
decision; a practice PR does not need to be merged during the tutorial.

Optional proportion extension: change only the assignment to
`target.scale = (options.scale * 1.3, options.scale * 0.75, options.scale)`.
At scale 1.25 expect `[1.625,0.9375,1.25]`, dimensions `[3.25,1.875,2.5]`,
and bottom z 0 because vertical scale/location remain paired. Compare a fresh
render against the uniform cube. If an agent also changes vertical scale,
ask it to explain and preserve the floor-contact calculation; inspect the
saved scene instead of accepting the explanation alone.

### 85-100: tools, failure and recovery

The course-owned [bounded MCP adapter](blender_tools.py) runs the same
Blender CLI/script. It is **not** the broader third-party Blender add-on.

```bash
uv run python mcp_client.py --blender list
uv run python mcp_client.py --blender render_scene '{"scale":1.25}'
uv run python mcp_client.py --blender inspect_scene
uv run python mcp_client.py --blender render_scene '{"scale":5}'
```

Expect two tools, then a successful render/inspection. The last call must exit
nonzero with `isError: true`: scale must be between 0.5 and 2 and no new render
is launched. In PowerShell, if inline JSON quoting fails, use
`uv run python mcp_client.py --blender render_scene` for its default scale 1,
and use the following missing-object command for the failure check.

```bash
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --target MissingObject
```

Expect nonzero exit and `Missing object: MissingObject; use Sculpture`.
Recover by removing the bad target and rerunning the last successful command.
Do not count an earlier PNG as output of the failed command.
`inspect_scene` reads a **saved JSON file**, not a live editor. If settings or
cache writes fail, the adapter redirects them into `.output`. If shutdown
hangs, preserve the error, stop with Ctrl+C and ask the tutor; do not launch
an unbounded series of copies.

The supplied adapter/client/variant commands select calls in code. They are
**deterministic human-directed tools**, not an autonomous agent. In your
coding-agent run the model may choose to inspect, edit, check or revise after
an observation. Record the next-action decisions you actually observed, its
available actions and the condition that made it stop.

### Optional: inspect a live Blender bridge

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

## Route B: GitHub sign-in and a private persistent note

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

### 35-55: an agent change on a branch

Follow the [shared workflow](agent-pr-workflow.md#the-shared-workflow).
Request a small UI change such as clearer save feedback and a visible 2000
character limit. Preserve sign-in, signed sessions and owner-scoped queries.
Acceptance: the count tracks typed text, a failed save is shown as a failure,
and saving remains limited to the signed-in user's note. Read the diff:

```bash
npm test
npm run typecheck
npm run build
git diff --check
git diff
```

Open a PR with observations and checks. Ask a partner for a concrete revision,
such as preserving typed text on a failed save. Revise the **same PR** and
rerun affected checks. Local ownership tests are useful before accounts are
ready; UI tests alone do not prove real OAuth or two-account isolation.

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
store. It demonstrates local runtime/persistence behavior, **not GitHub
sign-in or remote Cloudflare acceptance**. Its fixtures are not credentials
for your deployed app.

If sign-in fails, compare callback, `APP_URL` and local/deployed origin;
do not remove state/cookie checks. If a note disappears after restart, verify
the same database/binding is being reopened. A newly created empty database
is a different store. For Actions failures inspect the first failing step and
secret **names**, not values; correct configuration, redeploy and rerun the
affected check. Do not delete databases as routine recovery.

Without credentials, run the local checks, inspect the mocked OAuth tests,
and make/review your UI change. Pair on a prepared deployment if available.
Record exactly what you observed and which live checks remain open.

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
[Godot preparation for Week 12](godot-week12-preparation.md). Godot is not a
third Week 11 route. Week 12 provides first-time setup/orientation followed
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

Setup documentation was checked through Context7 on 15 November 2026:
[Blender command line](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html),
[Blender API](https://docs.blender.org/api/current/),
[creating an OAuth App](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app),
[Actions secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets),
and [D1 migrations](https://developers.cloudflare.com/d1/reference/migrations/).
Use the [template README](https://github.com/sd5913/github-oauth-d1-template#readme)
for tested versions and exact configuration. Blender is GPL-licensed; the
community bridge/MCP SDK are MIT-licensed. Geometry is original course code;
no downloaded assets are required.

See [the verification record](verification-20261115.md) for actual Blender
commands and limits. Tests, headless renders, a live application bridge and
a model choosing actions are different evidence. No model episode,
student-account GitHub login or remote Cloudflare deployment is claimed by
this documentation update. Windows/macOS and projected classroom display
still need rehearsal. Retained Godot evidence is dated separately in its
preparation appendix.
