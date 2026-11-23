# Week 12 · What does your delivery candidate let someone do?

**Thursday 26 November 2026, Hong Kong.** The lecture connects the course examples and ends with a group AMA. This separate two-hour tutorial uses your existing team project and scheduled tutor meeting. Bring the candidate you have, a playtest observation and one question. A saved build, screenshots or a sketch of the last working interaction will do if the network or demo fails. Say which parts someone actually tried.

## Two hours with your team

| Minutes | What to do |
| --- | --- |
| 0–15 | Take turns as visitor and observer. The visitor tries the first interaction with only the README or the team’s usual invitation. Where do they hesitate? If the candidate is offline, walk through the last saved version and identify what still needs a live check. |
| 15–35 | Follow one input to its visible or audible response. Pick two linked class examples below. Point to the corresponding state, asset or decision in your own project. |
| 35–55 | Compare the November 19 playtest observation with the candidate. Try the smallest change that might resolve it, or describe the check that would distinguish two possible causes. |
| 55–65 | Break. |
| 65–85 | Swap projects with another group. Ask them to try one ordinary action and one recovery, such as reconnecting or continuing without a camera. Explain what should persist. |
| 85–100 | Group AMA. Take three minutes to prepare a question, ten for questions and follow-ups, and two to choose a next check. Use the short prompt below. |
| 100–120 | Scheduled tutor and project support. Show the usable increment, evidence and main blocker. Record the feedback, next goal and owner in the team’s existing progress record. Finish at minute 120. |

**Group prompt** — “Our visitor tries ___. We saw ___. Should we change ___ or ___, and what would tell us?” One spokesperson asks, another teammate describes the evidence. With no Wi-Fi, write the question on paper or say it aloud, sketch the before/after, and pass it to the next group. If your team is still getting started, use the smallest interaction you can demonstrate and ask what to cut.

## Which class helps answer your question?

- **Can a teammate reproduce the result?** [Week 1’s public repository](../week01/README.md) gave someone else a starting point. [Week 2’s predict, break and fix exercise](../week02/README.md) asks what a change should do. Try the candidate from its documented starting state. Which step only works on its maker’s laptop?
- **Does the control change something the visitor understands?** [Week 3’s Quarry Bay tides](../week03/README.md) turn hourly heights into bars. [Week 4](../week04/README.md) gives the same data a control and a response. Choose a different day. The caption and chart should change together; the chart should still contain 24 hourly heights.
- **What signal can the visitor perceive?** Reverse the moving-dot frame order in [Week 5](../week05/README.md), or imagine doubling the tone frequency from 220 to 440 Hz in [Week 6](../week06/README.md). Direction and pitch communicate different changes. Which cue would survive a muted projector or a missed frame? Live song generation and the local speech setup were optional routes.
- **Where does shared state live?** In [Week 7](../week07/README.md) the terminal and Pygame draw the same Ball state. In [Week 9](../week09/README.md) two browser tabs receive a server snapshot. If a visitor reconnects, should the view recover the current scene, restart the experience or load a saved record?
- **What happens when input disappears?** [Week 8’s camera landmarks and team workflow](../week08/README.md) connect a hand gesture to an action; an empty camera frame can also be a test case. Compare with [Week 9’s disconnected client](../week09/README.md). Pick a visible fallback and decide who will try it on the delivery machine.
- **Who can recover which information?** [Week 10’s talking handbook](../week10/README.md) separates a cited PDF passage, saved conversation rows and Pip’s spoken answer. [Week 11](../week11/README.md) connects a signed-in visitor to their own note, or takes a Blender object into Godot. Those were alternative tutorial routes. Test a second visitor for isolation, or identify the same object after export and import, as appropriate to your project.

The published [group-project brief](../assignments/group-project.md) describes Thursday’s delivery candidate (build, deployment or installation setup). The project is 40% of the course mark. Within it, creative idea is 25%, code 50% and execution 25%. Keep the public, sd5913-owned team repository, give teammates Write access, and link the shared progress record from the README. GitHub Projects is recommended and an equivalent accessible shared record is valid. The final repository deadline is **Sunday 6 December at 23:59 HKT**. Today’s questions and peer practice carry no separate mark or upload.

## Optional worked example · the three-light world

The [recorded model episode](model-episode.json) shows speed 125 collecting two lights by tick 180. After observing the failure, the model chose 275; the unchanged engine check reached three lights and the exit at tick 166, and edits stopped. The [four-second film](evidence/model-selected-world.mp4) was captured later by deterministic replay of that final source. Compare the [provenance](evidence/provenance.json) with the [ending still](evidence/frame-end.png). What can the film show about the visitor’s view that the checker cannot?

The [optional Godot practical](godot-practice.md) retains setup, commands and the prepared-partner route for anyone who wants to reproduce the example. Thursday’s team review needs no engine, model account or installation.
