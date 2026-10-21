# Week 11 — connect one control to one creative tool

> **Planning draft for 2026.** The supplied Week 11 slides cover Orange,
> Blender, TouchDesigner, NDI/OSC and a networked game. Choose one small
> practical path, not a compulsory installation tour of all five.

## Proposed activity if the integration path is retained

Send one simple control value to a prepared creative-tool example.

1. Name the sender, receiver and value. Predict which visible or audible
   property should change.
2. Use a synthetic value first, without a camera or NDI setup.
3. Change the range or mapping and compare the result.
4. Stop sending. Decide what the receiver should do with a stale or absent
   value.
5. Explain the mapping and demonstrate a safe reset.

**Working evidence:** a labelled input/output sketch and one successful mapping,
plus what happens when updates stop. No additional assessed submission is set.

## Setup and fallback

A printed message/value trace can replace the live connection. Use only a
prepared, tested receiver already available in the classroom. Do not require
students to buy or sign up for a creative application.

Keep connections local and sound low. Camera/NDI are optional extensions, not
the entry point. Do not send camera footage or open network ports as a default.
Exact software versions, launch steps and shutdown behaviour still need
verification before release.

## Alternative practical: one Blender change

On a prepared copy of the archive's Blender scene, identify an object, its
attributes and the camera. Predict the result of changing one camera position,
then compare two renders. Work in a disposable scene: the old script clears
objects before importing a model. No generated asset, GPU model or paid service
is required. This is an alternative to OSC, not an additional requirement.

Begin with a short team check-in: what works, what blocks you, and what can
someone else try? The old tutorial uses this alongside the tool examples.

## Sources and release checklist

- Historical: [2025 Week 11 README](https://github.com/sd5913/pfad/blob/2025/week11/README.md),
  [OSC example](https://github.com/sd5913/pfad/blob/2025/week11/osc_demo.py),
  and [2025 index](https://github.com/sd5913/pfad/blob/2025/README.md).
- Supplied “SD5913 - PFAD - Week 11.pdf”: Orange pp18–30; Blender
  pp31–39 and pp67–68; TouchDesigner pp40–44; NDI/OSC pp45–55;
  team check-in p63; game integration pp56–60 and pp74–77. Visual review
  confirms the code and workflow screenshots. Advanced asyncio is not core.
- Activities are proposed small adaptations of these sources.
- Pending: choice of tool/focus, tested synthetic-input path,
  tested receiver, stale-data behaviour and no-install fallback.
