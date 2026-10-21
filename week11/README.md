# Week 11 — connect one control to one creative tool

**Thu 19 Nov 2026.** Follow one numeric input into a mapped visual response, then test what happens when it stops. No account, camera, audio permission, NDI, network port, Blender, Orange or TouchDesigner is needed.

## Run the browser practical

1. Open [`browser/index.html`](browser/index.html) directly in a modern browser (double-click the file, or drag it into a tab). It also works offline; do not start a web server. If you cloned the repo, the path is `pfad/week11/browser/index.html`.
2. Before pressing **Send value**, sketch `number (sender) -> Send value (boundary) -> canvas (receiver) -> orange shape`. Predict the output for `0.75`. Then send it: the orange shape has **75% opacity**, and the text readout says `Opacity: 75%`.
3. Try `0.25` (25%), `3` (clamped to 100%) and an empty input (reset to 0%). Each send replaces the previous value. The shape's opacity, not its size, changes.
4. Press **Stop / reset**: output returns to 0%. Send again and do nothing for three seconds: no new value arrives, so the receiver resets to 0%. Clearing the field also resets immediately. A silent sender is different from explicitly sending `0`.
5. In `browser/control.js`, change `mapOpacity` to reverse the response, e.g. replace `number` with `1 - number` inside the clamp. Reload the page and predict how `0.25` changes. Restore the original mapping if sharing a computer.

The button crossing is a **simulated sender/receiver boundary inside one browser page**, not OSC, an external tool connection or a claim that two programs communicate. The browser Canvas is the actual creative surface: the value really changes its drawing. `mapOpacity` checks for a finite number, clamps it to 0–1 and converts it to a percentage. Wrong or missing input resets to 0. There is no automatic live input: press Send for each update. The page starts stopped, is silent and opens no ports. The displayed text duplicates the visual result for students who cannot distinguish the shape or its colour.

Optional teacher extension only: on a **separately prepared and tested** local OSC receiver, use the same `0..1 -> 0..100%` mapping and explicitly implement validation and a stale-update reset. The browser page does not send or receive OSC and cannot verify the external tool's behaviour. Do not install or depend on that receiver for this exercise; camera/NDI are not an entry point.

## Paper-only route

Draw four boxes: `sender: 0.75 -> message: value 0.75 -> receiver: clamp then multiply by 100 -> picture: 75% opacity`. Repeat for `0.25 -> 25%`, `3 -> 100%`, and `"oops" -> 0%` (invalid). Cross out the sender-to-receiver arrow, wait three imagined seconds, and draw a blank shape with `0%` beside it. Compare your predictions with a partner. The sketch, one mapping and the missing-update decision are informal working evidence, **not a new assessed submission**.

If you have Node.js installed, `node --test week11/browser/control.test.cjs` from the repo root checks the arithmetic and invalid input; Node is not needed to run the artwork.

## Other paths, not prerequisites

The historical Week 11 materials survey Orange, Blender, TouchDesigner, NDI/OSC and a networked game. An optional Blender demonstration would require a prepared disposable scene: changing `Cube.scale` in `bpy` does not render on its own. The [2025 Week 11 README](https://github.com/sd5913/pfad/blob/2025/week11/README.md) and [OSC example](https://github.com/sd5913/pfad/blob/2025/week11/osc_demo.py) are references, not setup steps for this practical. Keep private files and footage out of demonstrations.
