# Week 12 · Course concepts and your delivery candidate

**Thursday 26 November 2026, Hong Kong.** The lecture reviews the computing concepts from Weeks 1–11 and ends with a group AMA. This separate two-hour tutorial uses your existing team project and scheduled tutor meeting. Bring the candidate you have, a playtest observation and one question. A saved build, screenshots or a sketch of the last working interaction will do if the network or demo fails. Say which parts someone actually tried.

## Two hours with your team

| Minutes | What to do |
| --- | --- |
| 0–15 | Take turns as visitor and observer. The visitor tries the first interaction with only the README or the team’s usual invitation. Where do they hesitate? If the candidate is offline, walk through the last saved version and identify what still needs a live check. |
| 15–35 | Follow one input to its visible or audible response. Pick two concepts below and answer their prediction prompts. Then locate the corresponding rule, data or boundary in your own project. |
| 35–55 | Compare the November 19 playtest observation with the candidate. Try the smallest change that might resolve it, or describe the check that would distinguish two possible causes. |
| 55–65 | Break. |
| 65–85 | Swap projects with another group. Ask them to try one ordinary action and one relevant failure or recovery. Explain who owns the state, what should persist and what result they should see. |
| 85–100 | Group AMA. Take three minutes to prepare a question, ten for questions and follow-ups, and two to choose a next check. Use the short prompt below. |
| 100–120 | Scheduled tutor and project support. Show the usable increment, evidence and main blocker. Record the feedback, next goal and owner in the team’s existing progress record. Finish at minute 120. |

**Group prompt** — “Our visitor tries ___. We saw ___. Should we change ___ or ___, and what would tell us?” One spokesperson asks, another teammate describes the evidence. With no Wi-Fi, write the question on paper or say it aloud, sketch the before/after, and pass it to the next group. If your team is still getting started, use the smallest interaction you can demonstrate and ask what to cut.

## Which concept explains your result?

Answer the question for the class example first, then ask what in your candidate behaves the same way. Discuss it from a sketch or an observed result. Each link leads to the original exercise and its run instructions.

| Week and concept | Prediction to discuss |
| --- | --- |
| [1 · Rules and reproducibility](../week01/README.md) | If two teammates run the Schotter sketch at the same commit with the same parameters and seed, what should repeat? What changes when they vary chaos and keep the seed fixed? |
| [2 · Types, control flow and verification](../week02/README.md) | A tide height arrives as text. Which operation changes meaning? Predict what the rule should do for a valid number and for missing input before checking the output. |
| [3 · Data and visual encoding](../week03/README.md) | If the same 24 heights become a tide clock instead of a line, which values stay the same? What comparison becomes easier? |
| [4 · Events, state and views](../week04/README.md) | The visitor switches from January 31 to February. Which selection is valid, what data comes back, and how can a test check the chart and caption together? |
| [5 · Pixels and frames](../week05/README.md) | Reverse a moving dot’s frames. Which property of its motion changes? What changes when you alter frame duration? |
| [6 · Signals and speech](../week06/README.md) | Double 220 Hz to 440 Hz at the same amplitude. What should sound different? If a voice control triggers the wrong action, which observable output helps distinguish a recognition error from the response rule? |
| [7 · Classes, instances and rendering](../week07/README.md) | Step one Ball and leave the other alone. Which state changes? If both renderers show the same bad bounce, where would you check first? |
| [8 · Team delivery and vision](../week08/README.md) | A PR passes CI. What would establish that an intended visitor can run the candidate? If a landmark is missing, which decision should the app make and how could a recorded frame test it? |
| [9 · Network messages and shared state](../week09/README.md) | One tab disconnects and the other moves the dot. Which process owns it, and what does the first tab see when it reconnects? What changes if the server restarts? |
| [10 · Persistence, retrieval and memory](../week10/README.md) | Which rows reload after restart, and which belong to the selected user and conversation? For a handbook follow-up, identify the prior turn that resolves the reference, the passage that supports the answer and the observable speech result. |
| [11 · Identity, deployment and tool boundaries](../week11/README.md) | In route A, what checks identity and what limits access to one note? Which environment owns the database? In route B, what survives the Blender-to-Godot export, and what game behavior needs its own check? |

For the later weeks, these distinctions also apply if your project uses a different stack:

- **Connected and persistent state.** A reconnect can fetch the current view from a running process. A new process needs a saved record to restore earlier state. Point to the process and the storage before you predict recovery.
- **Exact and semantic retrieval.** An account or conversation ID selects specific rows. Compatible embeddings rank passages by similarity. Inspect the retrieved text before trusting a citation. Conversation memory and spoken output have their own checks.
- **Identity and authority.** An app session gives the server evidence about the caller. The server still applies the access rule to the requested record. For a tool or asset handoff, verify the visible state and behavior in the destination application.

The published [group-project brief](../assignments/group-project.md) describes Thursday’s delivery candidate (build, deployment or installation setup). The project is 40% of the course mark. Within it, creative idea is 25%, code 50% and execution 25%. Keep the public, sd5913-owned team repository, give teammates Write access, and link the shared progress record from the README. GitHub Projects is recommended and an equivalent accessible shared record is valid. The final repository deadline is **Sunday 6 December at 23:59 HKT**. Today’s questions and peer practice carry no separate mark or upload.

## Optional worked example · the three-light world

The [recorded model episode](model-episode.json) shows speed 125 collecting two lights by tick 180. After observing the failure, the model chose 275; the unchanged engine check reached three lights and the exit at tick 166, and edits stopped. The [four-second film](evidence/model-selected-world.mp4) was captured later by deterministic replay of that final source. Compare the [provenance](evidence/provenance.json) with the [ending still](evidence/frame-end.png). What can the film show about the visitor’s view that the checker cannot?

The [optional Godot practical](godot-practice.md) retains setup, commands and the prepared-partner route for anyone who wants to reproduce the example. Thursday’s team review needs no engine, model account or installation.
