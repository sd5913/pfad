# Week 7 — from an idea to one interaction

**22 October 2026.** The midterm is 10:00–10:30 HKT. After the quiz: a short
classes demonstration, the team-registration demo, then two team activities.
Follow the instructor's quiz instructions; this activity does not change them.

## After the quiz: one class, two views

The instructor demonstrates this example from the laptop. Classes are the only
new theory in this part of the lesson; watching the demo is enough. Running or
remixing it yourself is optional practice, with no additional submission.

### 1. Two balls, two sets of attributes

Open [ball.py](ball.py). `Ball` is a **class**, a definition we use to create
objects. `red` and `blue` are two **instances** of that class. Each has its own
position (`x`, `y`), velocity (`vx`, `vy`) and `radius`. `__init__` sets their
starting attributes. In a method, `self` means the particular ball receiving
the call.

Run from the repository root:

```bash
uv run week07/ball.py
```

Predict the output before running it:

```text
Before: red=(16, 8), blue=(44, 14)
After red.update(0.1): red=(17.40, 7.78), blue=(44, 14)
After blue.update(0.1): red=(17.40, 7.78), blue=(43.00, 13.38)
```

`red.update(0.1)` advances red by one tenth of a second. Blue stays where it
was until its own method is called. The class is shared; each object's
attributes are separate. Trace `self.vy += GRAVITY * seconds`, then the position
updates. Gravity changes vertical velocity; collisions reverse and reduce the
velocity at a wall or floor. Coordinates start at the top left, so increasing
`y` moves down.

### 2. One moving model, two ways to draw it

```bash
uv run week07/ball_both.py
```

Keep the terminal visible beside the graphical window. The terminal draws
`R` and `B`; Pygame draws coloured circles. Both draw the **same ball objects
from the same simulation**, with gravity and bouncing in both views. Only the
rendering changes. The terminal has a coarser grid, so small movements can
remain in the same character cell. `uv` downloads Pygame and `watchfiles`
automatically on the first run; no flags or separate installation are needed.

### 3. Edit the class while both views are open

Keep [ball.py](ball.py) open in your editor. Change one value, predict the
result, then save:

- Change `GRAVITY = 28` to `GRAVITY = 56` for stronger downward acceleration.
- Change `BOUNCE = 0.82` to `BOUNCE = 1` to preserve more speed at collisions.
- Change one starting `vx` or `vy` in `starting_balls()` to affect only that ball.
- Change a line in `Ball.update()` to change the behaviour shared by both balls.

`watchfiles` notices the save, reloads `Ball` and restarts both views together
from their starting positions. Both windows stay open. This is a reset using
the new class, rather than migration of objects already in flight. A syntax
error or an immediately failing update keeps the previous working model moving;
an error encountered later freezes the last valid state. Read the terminal's
error message, fix the code and save again to recover.

In the graphical window, **Space** pauses/resumes and **R** resets. Closing it
or pressing **Ctrl+C** in the terminal stops both views. Each renderer can also
run by itself:

```bash
uv run week07/ball_play.py      # ASCII only; Ctrl+C stops it
uv run week07/ball_pygame.py    # Pygame only; close the window to stop
uv run week07/ball_both.py      # both views, synchronized
```

All three watch the same `ball.py` and reload on save. Starting the renderers
separately gives each its own simulation clock; use `ball_both.py` to keep them
exactly in sync. No display, API key or model download is needed for ASCII.

Focus on `ball.py` during the explanation. [ball_live.py](ball_live.py) supplies
the simulation clock and reload support; [ball_play.py](ball_play.py) and
[ball_pygame.py](ball_pygame.py) supply the renderers; [ball_both.py](ball_both.py)
starts the synchronized pair. They are supporting code
to explore later, not additional theory for today's lecture. Offline checks
run with `uv run week07/test_examples.py`.

## First, form your team

Use the Canvas group-registration route demonstrated in class. If you do not
have a group, ask for help. Follow the instructor's existing team arrangements;
this page does not set a team size.

Build something you want to use: an ambitious useful app, a creative tool or a
game mashup. AI can help you develop it, but AI does not have to be inside the
finished product. Reinvent an interaction, not somebody else's code or assets.
Use original or licensed material.

## Activity 1: tell us what happens — 20 minutes

Include team formation and registration in this time. Pick one representative
and one team name. Submit **one ClassPoint text response** with:

- Team name.
- Intended user or player.
- What that person does.
- How the program responds.
- What you are reinventing or combining.
- The first interaction you want to test.

Keep it concrete. “The player presses this button, and this changes” gives you
something to discuss and test. A list of technologies does not yet describe an
experience.

## Activity 2: show one moment — 20 minutes

Make **one image mock-up** of a screen or moment of use. Show the action and the
response from Activity 1. Add arrows or short labels if that makes it clearer.

A photograph of a paper sketch is enough. The same representative submits the
image on ClassPoint using the same team name. Do not spend this time making a
logo or setting up a new image-generation account.

These are today's two idea-development submissions. There is no extra
prototype, video, pitch deck or critique submission. Use remaining class time
for feedback, helping people find a group, and checking your separate
Assignment 3 progress.

## Before you leave: protect time for Assignment 3

This is **individual work**, not a third team submission. Open the
[Assignment 3 brief](https://github.com/sd5913/teaching/blob/main/syllabus/03-interactive-experience.md)
and your own repository. Due **Sunday 1 November 2026, 23:59 HKT**: your own
public GitHub repository URL goes to Canvas. Does your experience have one
working user input, a meaningful response and feedback? Have you tried an
ordinary mistake? Note one next fix and when you will test it with someone.
Check the brief for `README.md`, `PROCESS.md`, credits and submission details;
the group mock-up is not a substitute for your individual project. If time is
tight, work on this before optional practice.

## Tutorial: try one small change (optional practice)

After the two group activities, use an example you already know. This is a
proposed practice route, not an additional assessed deliverable or a promise to
finish a group prototype today.

1. Choose the smallest interaction related to your idea. Use
   [Week 4's control and response](../week04/README.md),
   [Week 5's images and frames](../week05/README.md), or
   [Week 6's sound and browser sketches](../week06/README.md).
   Keep its existing setup instructions open.
2. Before editing, write what one input should do. Predict the result.
3. Change one value, mapping or function. Run it. Compare the result with your
   prediction. Keep API calls, paid models and model downloads out of the core
   exercise.
4. Try an edge case: the smallest/largest accepted value, no input, a repeated
   click, or Stop followed by Start. Pick one that makes sense for your example.
5. Swap roles. Have another person explain the input, the response and the line
   responsible for the change. Keep a short note of what worked and what did
   not, for your own next step.

If setup is not ready, trace the existing example together on paper and mark
the change you would test. You can still explain the interaction without
installing a new stack. If working in your own repository, keep changes small
and attributable; do not commit credentials or private recordings.

You can also return to the ball demonstration above. Explain which changes
belong in the shared model and which belong in a renderer. Ask a partner to
predict one change before saving it. An unchanged tutorial example is **not**
an Assignment 3 submission. The supplied 2025 Week 7 PDF, p52, offers a more
involved Ball example; our explicit arguments replace its `**kwargs` and
Processing-specific vectors. Trace on paper if Python is unavailable.

### If AI helps with the change

Ask for one small change, then read and test it. A plausible explanation is not
evidence that the code behaves correctly. Compare the ordinary input and the
edge case. Note the tool/model if known, attempts needed, and elapsed time to a
working result. Do not compare output-token speed with total task completion
time, or treat a single attempt as a benchmark.

## Optional current examples — checked 21 October 2026

These are discussion prompts, not required tools. See the
[companion lecture news brief](https://github.com/sd5913/teaching/blob/2fe0d30d4dcdc7c19665be0e10b568220b53f15f/lessons/week07-news-20261021.md)
for the release context. Performance descriptions come from the vendors;
we have not reproduced their benchmarks.

- **19 October 2026:** [OpenAI's MultiLangBench announcement](https://openai.com/index/low-resource-programming-languages/)
  and [evaluation repository](https://github.com/openai/MultiLangBench)
  concern testing programming tasks across languages. Open evaluation code is
  not the same thing as open model weights. For our exercise: what test would
  show that your changed function works?
- **15 October 2026, fast-mode general availability:** [Anthropic's release notes](https://platform.claude.com/docs/en/release-notes/overview)
  and [fast-mode documentation](https://platform.claude.com/docs/en/build-with-claude/fast-mode)
  describe a faster output mode. Generating tokens faster does not measure
  setup, failed attempts or debugging. For our exercise: measure time to a
  working interaction, including retries.
- **19 October 2026:** [MiniMax's M3.1 Flash announcement](https://www.minimax.io/blog/minimax-m31f)
  describes hosted availability and a later weights release. Do not call it
  open-weight before the weights are released. No signup or paid API is needed
  to take part in this tutorial.

## Keep the two projects separate

The group project is 40%: a shared GitHub repository, everyone's commits,
original/licensed material and scope agreed by Week 8. Follow the actual brief;
this page does not add final deliverables or assessment rules.

Individual Assignment 3 is separate: 15%, due **1 November 2026, 23:59 HKT**.
Use its own brief and Canvas submission instructions.

## Instructor review and sources

The two 20-minute activities follow the
[Week 7 lesson plan](https://github.com/sd5913/teaching/blob/31c675b4085f771da6340878f3a54d7018f1015d/lessons/week07-lesson-plan.md)
in teaching PR #10. The optional tutorial adapts existing 2026 Weeks 4–6;
it is not an activity recovered from last year's slides. The supplied 2025 PDF, “SD5913 - PFAD - Week 7.pdf”, pp15–28 and
41–54, covers agents, state, global variables and creative-code tutorials.
Its old Blackboard, deadline, team-size and preinstalled-software assumptions
are not carried forward. The core class activities still follow the current
2026 plan, not the old assessment logistics.
Before class, check the actual Canvas group route and ClassPoint text/image
activities. Do not reuse last year's response links.
