# Week 13: final project support

**Final class date and tutorial scheduling TBC.** The final Canvas quiz is
**10:00-10:30 HKT, 30 minutes**. Follow the instructor and actual Canvas
instructions for everything else about that assessment. This page is the
**separate 120-minute final support tutorial**, including help for unfinished
projects. Some tutorials may move; await the confirmed arrangements. It adds
no new technical practical, upload, grade or compulsory defence.

The outcome is a more reproducible project and a short, owned list of final
fixes. You should be able to explain one interaction, diagnose its largest
remaining blocker, and show what another person actually observed. The
lecture's public diagnosis prompts are revision, not graded quiz questions.
Use only material actually delivered when preparing for the quiz. Weeks 9-12
are approved production drafts at this page's preparation on 29 October;
check the instructor's final delivered scope before treating them as coverage.

## Prepare your existing work

Bring your laptop, power, shared repository URL, current README and existing
progress record. Use the setup for **your project**, including its declared
Python/runtime version, permitted sample inputs and any device requirements.
This is not a request to install another engine, database or AI service.
A partner machine is useful; a separate fresh folder on your machine is an
alternative. Windows, macOS and Linux projects may have different setup needs:
state which systems you tested and which remain untested.

Keep uncommitted work safe. Use a fresh folder for a reproduction check; do not
reset or overwrite your working copy. Do not share credentials, student
records, private media or assessment answers. Use fictional sample data. No
instructor account or ClassPoint session is needed. If hardware, accounts or
internet fail, work with a prepared partner or inspect source and logs with
the tutor; record that the corresponding live check remains incomplete.

## The complete two-hour route

| Minutes | Purpose | Useful evidence in your existing record |
| --- | --- | --- |
| 0-15 | Triage every team | Current state, largest blocker, next check and owner |
| 15-45 | Setup/run/core blockers | One normal interaction or smallest reproducible failure |
| 45-60 | Peer fresh run | Source revision, actual command/result, missing instruction |
| 60-70 | Break | Save work; release camera/audio/network resources |
| 70-100 | Final tutor review and targeted fixes | Checked fix or a bounded unresolved issue |
| 100-115 | README/build/access/credits | Delivery checklist with honest remaining limits |
| 115-120 | Final owners/actions | Essential fix, owner, recheck time before deadline |

Tutors can reorder the help queue, keeping the break and support time. Reviews
use the existing progress record and execution criterion. These notes are for
your team, not a new Canvas upload or assessed presentation.

## 0-15: choose a support queue

Open the repository and try the documented run command. Tell the tutor which
state best describes your team:

| State | First task | Tutor/partner help |
| --- | --- | --- |
| Cannot access or start | Check URL, membership, working directory, runtime and first error | Pair with someone who can run the same revision; compare setup |
| Starts, core interaction fails | Choose one input and write expected versus actual response | Trace the smallest failing path before changing code |
| Core works | Give a partner the README and source revision | Fresh run, boundary test, documentation and access checks |

Name one **essential** behavior, such as “press Start, move the character,
reach an ending” or “choose an image, change the filter, save the result”.
Defer optional polish if the main interaction cannot run. A list of technologies
is not an acceptance check. Tell the tutor what you already tried so the next
attempt answers a different question.

## 15-45: resolve the core blocker

Use this small cycle on your own existing code:

1. **Predict:** choose one normal input and one relevant boundary. Write the
   expected visible or audible result and what would count as failure.
2. **Run:** follow your README from its named directory. Keep the exact command,
   first error and source revision; do not paste private logs into public issues.
3. **Inspect:** find the handler/method and the changing state. If another
   process, file, tool or service is involved, inspect both sides of that boundary.
4. **Change:** make one small fix: an incorrect relative path, missing validation,
   state update, undeclared dependency or unclear instruction. Read the diff.
5. **Check:** repeat the original input and boundary. Compare prediction with
   actual result, including restart/reload where persistence is promised.
6. **Recover:** stop the program normally (close its window or Ctrl+C), restore
   the experimental value if unsuitable, and keep the known working revision.
   Do not delete the whole project or database to hide a failure.

For a setup blocker, check directory and filename first, then runtime version,
then declared dependencies and inputs. An import error is different from a
missing asset, device permission or unreachable service. After ten minutes
without a new clue, ask the tutor or move to a prepared partner rather than
spend the whole session downloading a new stack. Keep the unresolved condition
visible in your README.

### Return to a familiar example only when it helps

These are recovery references, **not exercises all teams must finish**. Work
from the PFAD repository root unless the command enters a weekly folder.
Use the earlier README for prerequisites and its complete stop/recovery steps.

| Need | Exact existing route | What to observe and inspect |
| --- | --- | --- |
| State and methods | [Week 7](../week07/README.md): `uv run week07/ball.py` | Before/after coordinates; inspect `Ball.update()` in `week07/ball.py` |
| Local visual input without a camera | [Week 8](../week08/README.md): enter `week08`, then `uv run python hand_tiles.py` | Sample coordinates select a tile; inspect mapping, including missing-hand state |
| Team workflow, PRs, access or progress | [Week 8 teamwork](../week08/teamwork.md) | Trace a local change through review to shared main; compare repository and Project access |
| Messages and connection failures | [Week 9](../week09/README.md) | Follow its delivered server/client setup; inspect accepted/rejected messages and disconnect recovery |
| Models, scoped rows, restart/history or retrieval | [Week 10](../week10/README.md) | Follow its delivered setup; distinguish stored records, source retrieval, model context and audio |
| Creative-app state versus tool result | [Week 11](../week11/README.md) | Check saved scene and actual application result with the installed route |
| Agent choices and stopping evidence | [Week 12](../week12/README.md) | Trace goal, request/result, failed check, adaptation and stop; distinguish replay from live model choice |

Weeks 7/8 are merged course references. Later-week recovery routes must match
the versions actually delivered; they are being revised during preparation.
Do not start their model downloads, app installs or paid calls merely to finish
Week 13. Your own project's working route takes priority.

## 45-60: let a peer try a fresh run

Give the peer your repository URL and README, then let them lead. On another
computer or in a separate new folder, use the source revision intended for
delivery. Clone through the team's normal Git workflow if available; otherwise
record which source copy/revision was used. Avoid a preconfigured environment
that hides missing dependencies.

The peer follows only the written setup/run steps and permitted sample inputs.
Check one ordinary interaction, one boundary/failure and the normal stop.
If the project promises saved state, stop and reopen it to see what survives.
If it produces an output file or build, locate and open that actual artifact.
A screenshot of success on the author's machine is not fresh-run evidence.

Record a short result, for example:

```text
Revision: <actual short commit>
Machine/runtime: <actual system and version>
Starting folder and command: <what the peer used>
Expected: choosing a sample image shows a filtered preview
Observed: preview worked; Save failed because output/ was missing
Next fix: create output directory safely; owner: <teammate>; recheck: <time>
Limit: camera input not checked on this machine
```

Improve one missing instruction or defect and retest it. If there is no second
machine, the new-folder result checks isolation on one system, not portability
across systems. If no run is possible, trace the instructions on paper with a
peer and label it a documentation inspection. Arrange the remaining run with
the tutor or teammate before the deadline.

**60-70: take the ten-minute break.** Save work and stop temporary processes.

## 70-100: final tutor review and targeted fixes

The tutor visits teams with startup/core blockers first; working teams continue
peer checks while waiting. Show one small interaction and evidence in the
existing record, or the smallest reproducible failure if still blocked. This
is support, not a compulsory defence or new graded demo.

Use a concrete report: expected result, actual result, first useful clue,
change tried and next check. Ask the tutor to help choose the smallest finish
that preserves the project's purpose. After feedback, one teammate fixes the
blocker while another improves setup/check instructions. Retest the original
case; also check the change did not break the core interaction.

A working team can inspect one risk instead of adding features: empty input,
missing asset, repeat action, cancellation, reconnect, restart or a clean build.
Choose a case that belongs to the project. If live accounts/devices are
unavailable, test the local behavior you can check and label the remaining
integration honestly. Do not present a fixture, recorded clip or replay as
proof of a live service or agent.

## 100-115: check the delivery

Use the [current group-project brief](../assignments/group-project.md) and the
actual Canvas assignment. Keep final fixes in your existing progress record.

- **Repository/access:** one shared **public repository owned by `sd5913`**.
  Confirm it opens signed out. Confirm each teammate has **Write** access;
  public visibility alone does not grant it. Ask for help if organization
  membership/ownership is missing; do not create a second competing repository.
- **README/run:** state purpose, supported/tested systems, starting directory,
  runtime/dependencies, setup and exact run command, controls, expected result,
  sample inputs and known limits. Try the command from shared source. Record
  unavoidable device/account/model prerequisites without publishing secrets.
- **Build/output:** if the project has a build/export step, follow its real
  documented command and open the result. If it runs as a script/app, check that
  route. A specific engine, app store, video or additional package is not required
  merely by this checklist.
- **Progress:** link usable increments, tests/playtests, feedback and next
  actions. GitHub Projects is recommended; an equivalent accessible shared
  record is valid. Check its access separately from repository access. Raw
  commit/card counts and formal Scrum roles are not the execution criterion.
- **Credits/privacy:** identify reused code/assets, sources and licenses or
  permission, libraries and meaningful AI assistance. Attribution alone does
  not grant a license. Remove private paths, personal recordings and credentials;
  use permitted sample data. Do not publish private model conversations.
- **Canvas:** open the actual submitted repository URL and confirm it points to
  this team's accessible repository. Follow the current assignment instructions;
  do not invent a new upload or hand-in format. Continue working until the
  existing deadline as allowed by the brief.

## 115-120: leave with an owned plan

Choose one essential remaining fix, its owner and a recheck time. Put optional
features after it. If the project is still blocked, name the smallest runnable
path and the next tutor/teammate check; do not describe an unrun idea as finished.
Keep the public README honest about limitations.

The group project remains **40% of the course**, with **25% idea / 50% code /
25% execution** within its mark. The deadline remains **6 December 2026,
23:59 HKT**. Final class date/tutorial arrangements being TBC does not change
that deadline. There is no new attendance mark, upload, compulsory defence,
required technology or new assessment here.

## Optional familiar revision: a bounded loop

Only use this if it helps your own revision; it does not replace project support.
The existing [loop.py](loop.py) uses Python 3.10+ and no packages or accounts.
From the PFAD root:

```bash
cd week13
uv run loop.py
uv run loop.py 0
python3 -m unittest discover -s . -p test_loop.py
```

Predict before running. The first command prints `0`, `1`, `2`, `done` on
separate lines. With limit zero, the initial condition is false and only
`done` prints. The check runs two subprocess-output tests and reports `OK`.
The inline script metadata keeps `uv run loop.py` independent of the root
project's dependencies. If uv is unavailable, `python3 loop.py` works with
Python 3.10+; on systems naming it `python`, use that command. A first uv run
may obtain Python if no suitable interpreter is installed.

Inspect `step += 1`, change the limit to 2 and predict/run/check `0`, `1`,
`done`. Restore the chosen value afterward. Removing the increment would
prevent termination at a positive limit: reason about that **on paper**, not
by running an infinite print loop. A word such as `three` produces a
`ValueError`; use a whole-number argument. If the script is missing, check
your directory and course revision before installing anything.

## Sources and verification limits

Prepared 29 October 2026. Optional loop commands and both existing tests were
checked on Linux with uv 0.13.6 / Python 3.14.8; the script declares Python
3.10+. This does not verify every team's project, Windows/macOS setup, GUI
hardware, Canvas permissions, actual fresh peer run or final support scheduling.
Those checks happen with the team/tutor, with real results recorded.

- [uv script documentation](https://docs.astral.sh/uv/guides/scripts/), checked
  through Context7 on 29 October: inline metadata isolates script dependencies.
- [Week 7 state/methods](../week07/README.md), [Week 8 vision](../week08/README.md)
  and [teamwork](../week08/teamwork.md) are earlier-course recovery references.
- Historical 2025 Week 13 PDF: p2 recap/final, pp3-26 revision, p27 AMA,
  p28 team/repository and another-computer check. Retain the reproduction
  question, update submission to Canvas and current repository policy.
- [2025 semester simulation](https://github.com/sd5913/pfad/blob/2025/week13/semester.py)
  is optional archive reading, not current marks or a required exercise.
- The historical Docker/Orange/projection material and unsafe password example
  are not final revision requirements. Revision covers actually taught concepts,
  not installation commands, port numbers, release trivia or news claims.
