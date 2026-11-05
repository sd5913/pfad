# Week 9: connected interactions

**Thursday 5 November 2026.** A separate 120-minute tutorial after the lecture:
**30 minutes of WebSocket work, 30 minutes observing Multiboxes, and 40 minutes
for group work and TA feedback**, plus setup and a break.

Use a small shared scene to trace a message and change one Python rule. Then
observe the same client/server ideas in a multiplayer physics game. Keep the
last 40 minutes for your own project, including teams still getting started.
Networking is inspiration for the project, not a required feature.

## The two-hour route

| Minutes | Activity | What you should be able to show |
| --- | --- | --- |
| 0-10 | Setup or pair on a prepared laptop | Two tabs connected to one local server |
| 10-40 | WebSockets: send, change one rule, reconnect | One action, shared state, rejection and a fresh snapshot |
| 40-50 | Break | Take the full ten minutes |
| 50-80 | Observe Multiboxes | Input, Python-owned physics and two views of the same world |
| 80-120 | Group work and TA feedback | A usable project increment, one blocker and the next fix |

Move to a prepared partner machine at minute 10 if setup is still blocked.
Alternate who predicts, edits and operates. Do not let installation or extra
exercises consume the group/TA block. The longer linked Multiboxes study guide
is a reference; this tutorial selects a **30-minute observation**, not its full
separate two-hour route.

## 0-10: prepare two views

Use a browser, terminal, editor and
[uv](https://docs.astral.sh/uv/getting-started/installation/). The small scene
needs Python 3.13 and packages, which uv selects automatically. First setup
needs internet. No account, camera, GPU, paid API or ClassPoint login is needed.

From the **PFAD repository root**:

```bash
cd week09
uv run python server.py
```

Keep the terminal running. Wait for
`Uvicorn running on http://127.0.0.1:8009`, then open
**<http://127.0.0.1:8009> in two tabs**, A and B. Expect **Connected** and
`x = 50 / revision 0` after a fresh start. Tabs joining an already used server
see its current values.

**127.0.0.1** means this laptop; **8009** selects the service. uv uses this
folder's `pyproject.toml` and environment, separate from the root Worker project.
Keep terminals in `week09` for the scene commands. **Ctrl+C** stops Python;
closing one tab disconnects only that client. Leave presenter port **8765** alone.
If 8009 is occupied, close your earlier copy or use
`uv run python server.py --port 8011` and change both browser URLs to 8011.

**Before the tutorial, the tutor also prepares Multiboxes:** use its
[setup guide][multiboxes-setup] on a prepared machine or rehearse an available
classroom endpoint. Students can observe two local tabs, pair at that machine,
or follow the tutor's demonstration. Multiboxes is a separate project; running
`server.py` above does not start it. No second installation is required during
the observation block. Its documented local browser address is
**http://localhost:8000**; the small scene remains on **8009**.

## 10-40: WebSockets, one rule and one recovery

### 10-20: send one action

1. Predict B's result. In A choose **25** and press **Send WebSocket**.
   Both dots should move to 25 with the same revision.
2. Read A's **Message trace**: outgoing action, incoming state, then an
   acknowledgement. B receives state without requesting it again.
3. Move B's slider without pressing Send. Its local input changes; the shared
   scene does not. Which process owns the scene?

An action and its results look like this after a fresh start:

```json
{"id":"a-1","action":"set_x","x":25}
{"type":"state","x":25,"revision":1}
{"type":"ack","id":"a-1","revision":1}
```

The browser generates the actual ID. **State** describes the scene;
**ack** names the action that was applied. The revision orders accepted changes
in this process. An ID correlates a reply; this example does not deduplicate
repeated commands. A "sent" line alone does not prove processing.

Open <http://127.0.0.1:8009/state> once to see an HTTP snapshot. Reload is needed
for a later snapshot; the WebSocket tabs receive continuing updates.

### 20-30: change one Python rule

Open [scene.py](scene.py), find `Scene.apply()`, and predict results at **80** and
**81**. Change the allowed maximum from **100 to 80**, including its error message.
Keep the integer check and the rest of the message contract.

Stop Python with Ctrl+C, rerun `uv run python server.py`, and press **Connect**
in both tabs. Edits do not reload automatically; a new process resets its memory.

| Input after the change | Expected result |
| --- | --- |
| 80 | Accepted; both tabs show 80 with the same revision |
| 81 | Rejected; neither position nor revision changes |

Use the slider and **Send WebSocket** to check both values. **Restore 100** and
its error message, restart and reconnect before continuing. A browser slider
alone cannot enforce a server rule.

### 30-40: disconnect and recover

1. Disconnect A. Send **35** from B. A keeps its last known display and labels
   it **Disconnected**.
2. Connect A again. It receives a fresh snapshot at 35; it does not replay its
   previous action.
3. Explain the difference between local input, the shared scene and an observed
   action result. Point to `Scene.apply()` in [scene.py](scene.py) and
   `updates()` in [server.py](server.py).

**Checkpoint:** show your partner the accepted change, one rejected value and
one recovered view. Finish at minute 40, even if some optional details remain.

## 40-50: break

Take ten minutes. The tutor can leave the prepared Multiboxes view ready for
the next block. There is no new installation task during the break.

## 50-80: observe Multiboxes

[Multiboxes][multiboxes] is a shared physics and territory-painting game. Python
and Pymunk own the world; browser Canvas clients draw it. Its
[study guide][multiboxes-guide] explains the complete starter. Use the three
observations below for today's **30 minutes**.

### 50-60: two clients, one game

Use the tutor's prepared instance or two tabs on the prepared local machine.
Choose nicknames and connect. Move, jump, and paint while descending. Find the
pink **YOU** outline in each tab and compare the shared world and coverage scores.

**Predict:** if you move in A, which square should B see moving? Closing A should
remove that player from B. Reconnecting creates a new temporary identity and
receives the current world.

### 60-70: follow one input to a shared result

Observe the tutor's browser Network/WS panel, or inspect the labeled examples
in the [protocol reference][multiboxes-protocol]. A client sends buttons:

```json
{"type":"input","seq":12,"left":false,"right":true,"jump":false,"down":false}
```

Follow **input -> Python physics -> state snapshot -> browser drawing**.
The client requests movement; the server decides positions, teams and score.

Current Multiboxes sends **JSON input and metadata**, then **complete binary
state snapshots**. The supplied decoder turns those frames into readable state.
Observe the tutor's decoded example or the protocol tables; you do not need to
write a decoder. This differs from the small scene's JSON state messages.
Label a source example as a trace if no live capture is available.

### 70-80: separate rules from rendering

Compare two source locations:

- [simulation.py][multiboxes-simulation]: Python rules such as gravity and jump
  speed affect the shared world.
- [app.mjs][multiboxes-client]: the browser renders the world and marks your
  local player. Changing a local outline would not change the shared score.

Point out where input is checked in [protocol.py][multiboxes-validation].
Explain why a client should request an action rather than choose its own score.
No second code-edit exercise, engine implementation or database setup is
required. Finish at minute 80 and return to your own project.

A shared campus session needs a prepared, reachable endpoint. If Wi-Fi or a
client fails, observe the prepared local two-tab world instead. If no runtime is
available, trace the linked source and sample messages and say which behavior
has not been observed. Hosted HTTPS clients need WSS; follow the project's
setup rather than changing browser security settings.

## 80-120: group work and TA feedback

Protect these **40 minutes** for group work and TA feedback on your team's
**first working interaction**. The TA confirms exact team times within the tutorial.
Networking, Multiboxes, AI and a camera are not required project features.

1. **Show the current increment.** Help a teammate run it. Explain one input,
   state change and visible response. Teams still blocked on setup should show
   the blocker and get help reaching one runnable interaction.
2. **Ask for focused feedback.** Show one failure or confusing result. Record
   what was expected, what happened and the TA's advice.
3. **Make the next change small.** Use the remaining time to fix or test it.
   Record the next owner, action and observable check in the team's existing
   accessible progress record. GitHub Projects is recommended; an equivalent
   record is valid.

There is no extra Canvas upload, attendance score or compulsory defence. The
project remains **40% of the course**, with **25% idea / 50% code / 25% execution**,
due **6 December 2026, 23:59 HKT**. Use a shared public `sd5913` repository with
teammate Write access. Canvas is the submission system; the
[reviewed brief](https://github.com/sd5913/pfad/blob/4358b4e47b874ef40c120e63b2f6329acbe9b7d5/assignments/group-project.md)
controls assessment details.

## Recovery and optional reference

| Symptom | Inspect and recover |
| --- | --- |
| `No module named fastapi` | Run from `week09` with `uv run` |
| Package download fails | Pair on a prepared machine at minute 10 |
| Address already in use | Stop your earlier server or choose another port deliberately |
| Browser opens a local file | Use the server's HTTP URL |
| `crypto.randomUUID is not a function` over a LAN IP | Use the updated `index.html` and reload: its action-ID fallback uses `crypto.getRandomValues()`, which works over LAN HTTP. `randomUUID()` requires HTTPS or a trusted local address such as `localhost` |
| A tab seems frozen | Read its connection label and reconnect |
| A rule edit has no effect | Restart Python; reconnect both tabs |
| Revision resets to 0 | A new process has fresh RAM; no database was loaded |
| Multiboxes is unavailable | Observe the prepared two-tab demo or a labeled source trace |

If no scene can run, draw A, server and B. Start the server card at
`x=50, revision=0`; apply 25, reject 101, and write state and ack cards.
Label this **paper simulation**. It does not establish working networking.

For later reading, inspect `await`, the lock and the sequential broadcast in
[server.py](server.py). A slow scene client can delay the small broadcast loop.
The supplied **Send, ignore replies, disconnect** control demonstrates an unknown
outcome by suppressing an observation; it does not prove random packet loss.
The optional [raw TCP server](echo_server.py) and [client](echo_client.py) use
port 8010 and newline framing. These are references, not extra tasks in the
protected group/TA time.

After restoring the original 100 boundary, maintainers can run:

```bash
uv run python -m unittest discover -p 'test_*.py' -v
node test_browser_state.cjs
```

The suites start temporary socket services; stop your manual scene server first.
A host-policy skip is not live proof. [check_browser.cjs](check_browser.cjs) owns
its own service on 8009; with the documented Playwright/Chromium environment it
checks two real pages and restart recovery. See that file for maintainer options.

## Sources and verification

The scene's unchanged code was checked on Linux on **29 October 2026**: 15 Python
tests, nine production-JavaScript checks and the real two-page browser check
passed. Installed versions were Python 3.13.16, FastAPI 0.162.0, uvicorn 0.54.0,
websockets 17.3 and Playwright 1.64.1. [Public practical CI](https://github.com/sd5913/pfad/actions/runs/40796663469)
records that earlier run; it is not a classroom or Windows/macOS rehearsal.
Primary references: [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
and [uv projects](https://docs.astral.sh/uv/guides/projects/).

LAN action-ID compatibility checked against MDN through Context7 on
**5 November 2026**: [`randomUUID()`](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/randomUUID)
requires a secure context, while [`getRandomValues()`](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/getRandomValues)
also works over plain HTTP. The fallback creates a random 32-character action
ID within the server's 48-character limit; it is used to correlate replies.

The revised allocation and Multiboxes references were checked **4 November**.
The links below pin source commit `2977be17b35790dd7b31f1f242b0dc86113d5350`.
Reading its source/docs verifies the referenced design and task descriptions;
it does not establish a new Multiboxes runtime or campus-device test.

[multiboxes]: https://github.com/venetanji/multiboxes/tree/2977be17b35790dd7b31f1f242b0dc86113d5350
[multiboxes-setup]: https://github.com/venetanji/multiboxes/blob/2977be17b35790dd7b31f1f242b0dc86113d5350/README.md
[multiboxes-guide]: https://github.com/venetanji/multiboxes/blob/2977be17b35790dd7b31f1f242b0dc86113d5350/STUDY_GUIDE.md
[multiboxes-protocol]: https://github.com/venetanji/multiboxes/blob/2977be17b35790dd7b31f1f242b0dc86113d5350/docs/protocol.md
[multiboxes-simulation]: https://github.com/venetanji/multiboxes/blob/2977be17b35790dd7b31f1f242b0dc86113d5350/src/multibox/simulation.py
[multiboxes-client]: https://github.com/venetanji/multiboxes/blob/2977be17b35790dd7b31f1f242b0dc86113d5350/src/multibox/static/app.mjs
[multiboxes-validation]: https://github.com/venetanji/multiboxes/blob/2977be17b35790dd7b31f1f242b0dc86113d5350/src/multibox/protocol.py
