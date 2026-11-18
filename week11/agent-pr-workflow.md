# From an agent request to a reviewed PR

Use this worksheet with either [Week 11 route](README.md). The observable
result matters: an attractive image or correctly isolated stored note needs
more than a successful tool response. A PR keeps the proposed change,
review request, revision and evidence together for a human decision.

## The shared workflow

1. **State the goal and acceptance criterion.** Name the user-visible result,
   files the agent may change, tools it may run, what must stay fixed, and
   what observation would make it stop. Inspect the supplied code first.
2. **Create a branch and give the request.** From your own exercise checkout,
   run `git status` and `git switch -c week11-reviewed-change`. Use another
   name if that branch exists. Do not give the agent deployment credentials
   or permission to merge. With no model access, a partner performs this step;
   record that it was human-directed.
3. **Inspect the diff, then check the application.** Run `git diff --check`
   and `git diff`. Read unexpected edits before executing them. Run the
   route's tests/build/render, inspect actual output and retain failures.
   A model may decide its next action after a tool result; record the actual
   sequence instead of attributing decisions to a fixed script.
4. **Open a PR with evidence.** Stage only intended source/evidence notes,
   commit them and push your branch to your own exercise repository. Use
   GitHub's **Compare & pull request** and set the base to your own
   fork/exercise repository, not the upstream course repository. State the goal, before/after,
   commands/exit results, acceptance checks and limits. Attach PNGs manually
   if useful; keep generated scenes/caches and credentials out of Git.
5. **Ask a person to review.** Request a specific review of the result and
   reasoning. The reviewer should make a concrete request that can be checked.
   A tool response or a generic "looks good" does not replace that review.
6. **Revise the same branch and PR.** Give the review to the agent, inspect
   its diff, rerun affected checks and attach the new observation. Commit
   and push to the existing branch; GitHub updates the same PR. Reply to the
   review with what changed and what you verified.
7. **Human merge decision.** The person responsible for the repository checks
   the final diff, CI and application evidence, then decides to merge or ask
   again. You may leave a practice PR open; there is no new merge requirement
   or graded submission.

If a check fails, keep the failing observation and make a small revision.
Do not repeatedly ask the agent to "fix everything" without reading its
changes. Do not remove checks just to obtain a green result. Stop and ask
the tutor if the change needs broader access than the agreed scope.

## Ask an agent to use Blender

This is an **example request**, not a captured autonomous episode. Give it
to the coding agent available in your own environment, or ask a partner to
perform the same work and label that human-directed fallback. The agent can
use terminal tools to run Blender; the optional live bridge is another route,
not a prerequisite for operating the application.

> From the PFAD repository root inspect `week11/blender_scene.py`,
> `week11/blender_export.py` and `week11/asset_handoff.py` first. Then use
> `week11/` for commands. Work only in the disposable scene, not personal files.
> Make Sculpture wider and shallower: replace uniform scale with x `1.6 * s`,
> y `0.75 * s`, z `s`. Keep its name, terracotta material, camera, light and
> bottom on the floor. You may edit the scene script, run Blender in background,
> read saved inspection JSON and open the rendered PNG to judge the result.
> If the handoff fails, you may make a focused change to `blender_export.py`
> to preserve the mesh/material/axis contract; explain that diff and rerun
> the checks rather than weakening them.
> Render scale 1.25 into `.output/blender/first` from `week11/`; compare with
> `.output/blender/before`. If the image is cropped or floats, inspect the
> cause and make a focused revision before rendering again. Explain dimensions
> and floor contact. Do not just report a successful command. Stop with a
> small diff, fresh image/inspection paths, actual commands/exits and any limits
> so I can review. Keep generated outputs ignored; no model/API purchases,
> asset downloads, personal files, external deployment or merge.

The goal is a visible sculpture. The available actions are inspect, edit,
run Blender, view output and revise. The state is script plus saved scene;
observations include errors, JSON and PNG. The stop condition is a grounded,
uncropped model with a small reviewable diff and evidence. Record where the
model actually chose its next action; a fixed command list does not prove
that decision happened.

Before accepting, open the image and inspect scale `[2.0,0.9375,1.25]`,
dimensions `[4,1.875,2.5]`, centre z 1.25 and bottom z 0. The camera stays
`[7,-9,6]`. Create the first PR with the actual result. A concrete review is:

> Reduce x from `1.6 * s` to `1.3 * s`; keep everything else fixed. Rerender
> into `.output/blender/revised`, inspect it, and update this same PR. Then
> export that saved scene with `uv run python asset_handoff.py export
> .output/blender/revised/sculpture.blend`, run `check`, and show the same
> model in `play` or `capture`. Stop with both application observations.

Expect revised Blender dimensions `[3.25,1.875,2.5]`, Godot dimensions
`[3.25,2.5,1.875]`, bottom Godot y=0 and retained material. Blender Z-up is
converted by the exporter; do not rotate it a second time. The GLB excludes
the render camera/light/floor. Godot supplies its own preview scene. There
is no collision yet. Human review judges the creative result separately
from export/import checks. No actual model session is claimed by this prompt.

## Optional worked camera review scenario

This is a **rehearsed design/review scenario**, not a historical model session
or a fabricated PR screenshot. The supplied `blender_variants.py` already
contains the first implementation: two cameras `(7,-9,6)` and `(9,-7,6)`.
Its Python loop selects the calls deterministically. The actual review delta
below changes the second position to `(5,-10,6)`.

### Goal, first implementation and evidence

The artist wants two distinguishable views of the same terracotta sculpture,
with no crop and no change to its proportions, material, light, floor contact
or look target. At scale 1.25, both saved inspections should report sculpture
scale `[1.25,1.25,1.25]`; the saved object's dimensions are `[2.5,2.5,2.5]`,
centre z 1.25 and bottom z 0. Only the camera changes the observation.

In your branch, a suitable first request is:

> Inspect `blender_scene.py` and `blender_variants.py`. Render the supplied
> two-camera implementation, then create a short `week11-camera-evidence.md`
> with camera coordinates, unchanged scale, observed difference and command
> results. Do not edit scene code yet. Use only the disposable course scene,
> keep generated output ignored, and stop after I can review the comparison.

This first PR contains the evidence note rather than an unnecessary rewrite
of an already supplied implementation. Look at the agent's diff before
running its commands; check that its note matches your own observations.
Render separate baseline paths from the PFAD `week11` directory:

```bash
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.25 --camera-x 7 --camera-y -9 --output .output/camera-review/before-1
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.25 --camera-x 9 --camera-y -7 --output .output/camera-review/before-2
```

Open each `sculpture-1.25.png`, `inspect.json` and saved `sculpture.blend`.
Compare front and side face visibility. The render's visual difference and
the saved camera coordinates are separate evidence. Check both process exits.
An earlier image or a test of a helper function cannot establish this run.
Stage only your evidence note and open a PR as described in step 4.

### Reviewer request and focused revision

The reviewer asks:

> Keep the first pose and sculpture unchanged. Try second camera `(5,-10,6)`,
> aimed at the same target. Rerender both and attach the new comparison to
> this PR. Check that scale and floor contact still match the first attempt.

Give that request to the agent on the same branch. It should propose a small
diff in `blender_variants.py`:

```diff
-    for number, (x, y) in enumerate([(7, -9), (9, -7)], start=1):
+    for number, (x, y) in enumerate([(7, -9), (5, -10)], start=1):
```

Inspect the entire diff; there is no need to change the sculpture or bridge.
Run the actual variant loop, then retain the revised image under a separate
path so it can be compared with the baseline:

```bash
uv run python blender_variants.py
blender --background --factory-startup -noaudio --python-exit-code 1 --python blender_scene.py -- --scale 1.25 --camera-x 5 --camera-y -10 --output .output/camera-review/revised-2
uv run python -m unittest test_world test_mcp_transport test_mcp_cleanup test_mcp_client_status
git diff --check
git diff -- blender_variants.py blender_scene.py
```

Expected: the first camera remains `[7,-9,6]`, the second becomes
`[5,-10,6]`, both scales remain `[1.25,1.25,1.25]`, and both PNGs show the
same grounded sculpture. Inspect the saved second scene if the shadow makes
floor contact ambiguous. The second image should show more front and less
side than `(9,-7,6)`; your human reviewer judges whether that meets the goal.
If the object is cropped or the composition is weaker, request another
bounded revision with fresh evidence rather than treating the coordinate
change alone as success.

Update your evidence note, commit/push to the same branch, and reply:

> Changed only the second camera. Attached old/new images and inspection
> values; rerender and checks completed with the recorded exits. Sculpture
> scale/location, first camera, target, light and material remain unchanged.
> This was a local render; I have not claimed a live model/bridge run.

Replace that example with your **actual** observations. The tutorial's
[verification record](verification-20261115.md) separately identifies which
commands the author rehearsed.

### Optional proportion review

A different design goal could ask for a wider, shallower sculpture. In
`blender_scene.py`, first trying x `1.6 * s`, y `0.75 * s`, z `s` yields
scale `[2.0,0.9375,1.25]` at `s=1.25`. A reviewer may ask for x `1.3 * s`
instead, yielding `[1.625,0.9375,1.25]`. The revised dimensions are
`[3.25,1.875,2.5]`. Retain `target.location.z = options.scale`: bottom z stays
0 because vertical scale still equals `s`. Keep the camera fixed for this
comparison; otherwise you cannot attribute the visual difference to proportion.

These numeric changes were rehearsed using temporary copies of the script;
they are not part of the supplied implementation. Do not claim an invented
model exchange. Give a live agent/partner the goal, inspect its actual diff
and compare your own fresh renders if choosing this extension.

## Authenticated-app review prompt

Use your template-copy repository rather than PFAD. Save feedback, the live
2000-character count and retaining text after failed save **already exist**
in `app/note-editor.tsx`. The first request is inspection and evidence:

> Inspect the page/editor, session handling, owner-scoped note queries and
> tests. Run tests, typecheck and build; record actual exits. Write a short
> evidence note explaining which save/count/error behaviors already exist,
> what the server checks prove and what still needs a browser/live-account
> check. Do not edit implementation yet or read secrets. Stop with an
> evidence-only diff so I can open/review the first PR.

After reviewing that first PR, request a concrete new behavior:

> Add a `Discard unsaved changes` button to `app/note-editor.tsx`. It restores
> the last successfully loaded/saved body, clears stale feedback and sends no
> network request. Disable it while saving or when text is unchanged. Keep
> sessions, owner-scoped server queries and the save contract unchanged.
> Revise this same branch/PR. Run checks, inspect the UI and stop with a
> focused diff and actual evidence. Do not read secrets, deploy or merge.

Check: type/discard returns to the loaded body; save/edit/discard returns
to the last successful save; a failed save does not become the discard target;
and no discard POST appears in browser Network. Use a labelled local fixture
or your own real sign-in; record which. Existing server tests do not prove
the new button works. Add focused UI coverage if a harness is available, or
retain actual browser evidence with that testing gap explicit. Then complete
the README's persistence/two-account checks when credentials are available.

## A compact evidence note

Use plain text or Markdown in your own exercise repository:

```text
Goal and stopping condition:
Files/actions allowed:
Branch and PR:
Agent model/account or human-directed fallback:
What I predicted:
First diff and observed result:
Commands and actual exits:
Reviewer request:
Revision on the same PR:
Rerun result and before/after evidence:
What remains untested:
Human review/merge decision:
```

For an agent run add the observed sequence of actions and observations,
including where it chose a next action or stopped. Do not label predetermined
calls an autonomous episode. Evidence notes contain no tokens, cookies,
`.dev.vars` contents, authorization codes or private user data.
