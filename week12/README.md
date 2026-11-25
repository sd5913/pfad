# Week 12 · Course review and group-project delivery

**Thursday 26 November 2026, Hong Kong.** The lecture reviews the computing concepts from Weeks 1–11, allows time for eSFQ and ends with an open AMA about the subject material. This separate two-hour tutorial is primarily time to move your group project forward. Focus on delivery: a deployed web app, or automated builds for your project's target platforms. Deployment gives you a version to try and refine over the coming week; it does not mean the project is finished.

By the end, another person should be able to find your URL or build, try one interaction, and give you an observation that informs your next change. Bring your existing team repository, its run instructions, the candidate you have and your main blocker. Use the project's existing tools and accounts; no new engine or model account is needed. If the network or demo fails, use a saved build, screenshots or a sketch of the last working interaction and record which live check remains. The concept prompts and Godot exercise below are light, optional references.

## Two hours with your team

| Minutes | What to do |
| --- | --- |
| 0–15 | Open the team repository and run the last working candidate using its README. Choose one interaction for a visitor to try and the delivery path that suits your project. Identify the missing URL, package or setup step. |
| 15–35 | Work on that delivery path: deploy the web app, or inspect and run the existing GitHub Actions build workflow. Share the URL or successful run with your team. If blocked, keep the last working version and identify the first failing step. |
| 35–55 | Try the delivered version on an intended device, following only the README. Compare it with the November 19 playtest observation. Fix one delivery or interaction problem, then deploy/build and check again. |
| 55–65 | Break. |
| 65–85 | Swap URLs or builds with another group. Let the visitor find the starting point without your explanation. Try one ordinary action and one relevant failure or recovery. Observe what they actually do and distinguish a delivery problem from an interaction problem. |
| 85–100 | Use that observation to make one small improvement or investigate the main blocker. Recheck the result. Update the README's access instructions and limitations, and choose the next change for the coming week. |
| 100–120 | Scheduled tutor and project support. Show the usable increment, evidence and main blocker. Record the feedback, next goal and owner in the team’s existing progress record. Finish at minute 120. |

Keep your allocated tutor meeting even if it falls earlier in the session; move the work blocks around it. Show the last working increment and the first failing step if delivery is blocked. If your team is still getting started, deliver the smallest interaction you can demonstrate and ask the tutor what to cut. Today's work adds no separate mark or upload.

## Choose a delivery path

### A · A web app someone can open

Use your project's existing deployment setup. The [Week 11 authenticated-app route](../week11/README.md) revisits the difference between local and deployed configuration. Open the public URL in a fresh browser session or on another device. Does the page load, and does the intended interaction work? If it uses a backend, check the deployed API, database, login callback and configuration too. A page loading is not evidence that saving or signing in works. Keep credentials in the host's secret settings, outside the repository.

Inspect the first failed deployment step or browser/network error before changing code. Make one focused change, deploy again and repeat the same check. If the host or Wi-Fi is unavailable, test the last saved local version using the README and record that public access still needs verification.

### B · GitHub Actions builds people can download

Start with your existing workflow in `.github/workflows/`. Identify its trigger, build/export command, target platforms and artifact-upload step. For Godot teams, compare the course [game template's build workflow](https://github.com/sd5913/godot-game-template/blob/f4e774ce11f0d9e231cb9be229490530cd6ef0fb/.github/workflows/build.yml), which exports Web, Windows and Linux. Choose the platforms appropriate to your project; every platform and app-store publication are not requirements. The [Week 8 teamwork guide](../week08/teamwork.md) explains the shared delivery workflow.

Run your project's documented trigger, open **Actions**, select the run for your commit and inspect each relevant job. A green workflow needs a downloadable result: find **Artifacts**, download the intended package, extract it and launch it on a supported device. GitHub artifact downloads may need sign-in and expire. Link the successful run and explain access and launch steps in the README. Use the project's established release channel if it already has one.

If a job fails, inspect its first meaningful error and the build/export configuration; fix the smallest cause and rerun. If no suitable device or download is available, inspect the job and package contents, try the existing local build and record the missing device check. CI success alone does not establish that the delivered experience works. Keep the last known working build while you iterate.

An installation or another delivery target agreed with your tutor remains valid. Make its setup reproducible and test it with a visitor using the equipment you have.

### Examples from class

These projects are in development, not model answers. Their pages and successful build artifacts were checked on 25 November; links and artifact availability can change.

| Project | Delivery to inspect | What to notice |
| --- | --- | --- |
| BothPls | [Web app](https://the-aliien-repo-oqpi.vercel.app) · [source](https://github.com/sd5913/The-Aliien-Repo) | A URL is a direct invitation to try the mobile web interface. Check the interaction separately from page access. |
| Pixel Paws | [Web game](https://sd5913.github.io/Pixel-Paws/) · [successful build run](https://github.com/sd5913/Pixel-Paws/actions/runs/45406859556) | The run provides web and Android debug packages. Its release job was skipped; artifacts are not a published release. |
| Monster Staff Access | [Windows build run](https://github.com/sd5913/ae4pa/actions/runs/45606353689) · [source](https://github.com/sd5913/ae4pa) | Download, extract and try the package on Windows. Package presence does not establish complete gameplay or save/reload behavior. |

### Deliver → try → observe → refine

Give a visitor the URL or build and the README. Predict what the chosen interaction should do, then watch without coaching. Record the version/commit, device, action, expected result and actual observation in your existing shared progress record. Pick one small change, name its owner and repeat the check on the next delivery. Keep the README clear about what works and what remains unfinished. Use this loop over the next week rather than waiting for a perfect version before sharing.

**Next Thursday, 3 December: quiz at 10:30 in TU103, followed by the final group-project review.** Bring the usable increment, test/playtest evidence and main blocker. There are only three days from that review to the final repository deadline: **Sunday 6 December 2026, 23:59 HKT**. Follow Canvas for the existing submission instructions.

## Optional · which concept explains your result?

If a concept would help explain your project's behavior, spend up to ten minutes on one prompt, then return to the project. Answer for the class example first and ask what in your candidate behaves the same way. Discuss it from a sketch or an observed result. Each link leads to the original exercise and its run instructions.

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

The [optional Godot practical](godot-practice.md) retains setup, commands and the prepared-partner route for anyone who wants to reproduce the example later. It is a longer self-study resource, not today's required tutorial. You can simply inspect the film and trace; today's project work needs no new engine or model account.
