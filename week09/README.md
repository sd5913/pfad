# Week 9: connected interactions

**Thursday 5 November 2026.** A separate 120-minute tutorial after the lecture.
Two browser tabs see the same scene because one Python server owns its position.
Trace HTTP, change a Python rule, observe WebSocket updates, reject bad input,
and recover from a disconnect. Explain which process owns state, what a message
means, and why sending does not prove processing. Reuse Week 4's tide API and
Week 8's input-to-action mapping; classes are a prerequisite rather than a new topic.

## Before you start

Use one laptop with a current browser, terminal, editor and
[uv](https://docs.astral.sh/uv/getting-started/installation/). First setup needs
internet for Python 3.13 and packages. No account, camera, microphone, GPU,
model, paid API or instructor ClassPoint login is needed. Core commands work
in PowerShell as well as Linux/macOS shells; actual platform limits are listed
under verification. Pair on a prepared laptop if installation is unavailable.

From the **PFAD repository root**:

```bash
cd week09
uv run python server.py
```

Keep terminal **A** running. `uv` selects this folder's `pyproject.toml` and
creates `week09/.venv` separately from the root Worker project. Wait for
`Uvicorn running on http://127.0.0.1:8009`. Open <http://127.0.0.1:8009> in
**two tabs**, A and B. Each is a separate client of the same server. Keep
terminals in `week09` for every command below. **Ctrl+C** stops Python; closing
a tab disconnects only that client.

`127.0.0.1` means this laptop (loopback), `8009` selects the service, `/state`
a route, and `http://` a protocol. The presenter uses **8765**; leave it alone.
If 8009 is occupied, close your earlier copy or choose one other port everywhere:

```bash
uv run python server.py --port 8011
```

Then use `http://127.0.0.1:8011` in both tabs. Do not kill an unknown process
or expose this teaching service to other machines to fix a local exercise.

## The two-hour route

| Minutes | Work and observable result |
| --- | --- |
| 0-15 | Setup; open two tabs; identify server and clients |
| 15-35 | Trace accepted messages and shared state |
| 35-55 | Change a Python validation rule and check it |
| 55-65 | Break |
| 65-85 | Compare two clients, polling and continuing updates |
| 85-100 | Trigger failure, recover and explain the evidence |
| 100-120 | First-working-interaction tutor review and project support |

At minute 15, use a working partner machine if setup is still blocked. Alternate
who predicts, edits and operates. If none can run the service, use the explicit
paper fallback below; it does not establish a working network result.

## 0-15: locate each process

**Predict:** does opening a tab create a new server or another client? Run the
setup. Expect **Connected**, `x = 50 / revision 0` in both tabs after the
first snapshot. A new tab joining an already used server sees its current values.

Draw one server and two clients. Label the server `127.0.0.1:8009` and both
connections `/ws`. Inspect [server.py](server.py): `create_app()` creates one
`Scene`, shared by HTTP and WebSocket handlers. The supplied
[index.html](index.html) draws it; your main edit will be in Python.

Read the server terminal on failure. An occupied port differs from a stopped
listener. A 404 means a server answered but did not know that route. A connection
refusal normally means no listener is present at that address and port.

## 15-35: predict, send, trace

1. In A select **25** and press **Send WebSocket** once. Predict B's result
   first. Both should move to 25 with the same new revision.
2. Read A's **Message trace**: outgoing action, incoming state, acknowledgement.
   B receives state without making another request.
3. Move B's slider without pressing Send. The scene stays unchanged: unsent
   local input differs from server state.
4. Select **80** in A and press **Send HTTP**. One `POST /action` receives a
   response. Both tabs also receive the server's WebSocket broadcast.
5. Open <http://127.0.0.1:8009/state>. This `GET /state` returns JSON. Send a
   new position from B. The plain JSON document needs **Reload** for a fresh
   snapshot; return to the controller afterward.

An outgoing message looks like this; the browser generates a unique ID:

```json
{"id":"a-1","action":"set_x","x":25}
```

The server validates it, changes `Scene.x`, increments `revision`, broadcasts
state, then acknowledges the sender. On a newly started server:

```json
{"type":"state","x":25,"revision":1}
{"type":"ack","id":"a-1","revision":1}
```

The ID matches a receipt to an action; revision orders server changes. This
demo **does not store IDs to deduplicate retries**. `set_x` assigns an absolute
position; retrying a command such as `add_score` would need a different decision.
Rejections echo a usable action ID too. A delayed result for an earlier action
must not finish a different action that is still waiting. An unidentifiable
message error is logged without pretending to resolve a named action.

Inspect `apply()` and `snapshot()` in [scene.py](scene.py), then trace the
action through `updates()` in [server.py](server.py) and the browser's `show()`.
Your partner should identify all three outgoing fields, the matching ack, and
the same revision in both views. A “sent” line alone is insufficient evidence.

## 35-55: make one bounded Python change

**Predict** results for 0, 80 and 101. Press **Try invalid x = 101**. Expect
**Rejected**, with neither position nor revision changed. A slider constrains
ordinary input, but a server still validates messages sent by other clients.

In `Scene.apply()` change the right edge from **100 to 80** in the comparison
and explanatory error message. Read your diff: one boundary is changing, not
the protocol. Keep `type(message["x"]) is int`: a boolean is not a position,
although Python treats `True` as an integer in some contexts.

Stop Python with Ctrl+C; run `uv run python server.py` again. This example
does not automatically reload edits. Press **Connect** in both tabs. The new
process starts with reset memory.

| Input | Expected after your change |
| --- | --- |
| 0 | Accepted; both tabs show 0 and the same new revision |
| 80 | Accepted; both show 80 |
| 81 | Rejected; position and revision unchanged |
| Invalid 101 button | Rejected with the revised boundary in its error |

Inspect the trace and second tab. **Recover:** restore 100 and its error
message, restart Python and reconnect. From terminal **B**, also in `week09`:

```bash
uv run python -m unittest -v test_rules test_asgi
```

These verify rules and actual FastAPI handlers in memory. The baseline checks
expect 100 to be allowed, so they fail if you keep the experimental 80 rule.
Read the case before deciding whether code or specification needs changing.
Restore the original baseline for the next exercise. Green in-memory tests
still require a separate check of the real browser view.

**55-65: break.** Note current position/revision and leave the server running
if practical. No camera or microphone is active.

## 65-85: continuing updates and two clients

1. A sends 20, then B sends 70. Both follow the server's last accepted action.
   Predict what happens if people click nearly together: the last command the
   server processes wins, and each accepted command gets a revision.
2. **Disconnect** A; B sends 35. B updates. A keeps its last known display and
   labels it Disconnected, rather than pretending that data is live.
3. **Connect** A. It reads a fresh snapshot at 35 with B's revision. It neither
   replays the old command nor resumes the old connection.
4. Compare **Read HTTP snapshot** with automatic updates. Polling repeats
   requests; a WebSocket allows either side to send new messages while open.

In `updates()`, inspect:

```python
incoming = await client.receive()
```

While A waits, `await` yields an opportunity for the event loop to run B's
handler. This is cooperative concurrency in one process, not one Python thread
per tab. The lock orders state changes and revision announcements. The small
broadcast loop can be delayed by a slow client; it is not a production hosting
architecture. Restarting the process loses its in-memory state.

HTTP can reuse TCP connections too: the contrast is request/response semantics
versus continuing two-way messages. WebSocket supplies a handshake and message
framing; raw TCP echo is a different protocol.

### Compact byte-stream observation

The lecture's TCP starter remains on a separate port, **8010**. If time remains,
run it in two spare terminals, still in `week09`:

```bash
uv run python echo_server.py
```

```bash
uv run python echo_client.py
```

Expect `received: red`, then blue on one connection, then green after reconnect.
A newline ends each message. TCP delivers ordered **bytes**, so one read may
contain part of a message or several messages. It does not preserve each send
as a separate message. Inspect combined `red\nblue\n` and split `or` /
`ange\n` sends in [test_echo.py](test_echo.py); `readline()` reconstructs them.
Stop this extra server with Ctrl+C. It has no HTTP routes or WebSocket handshake.

## 85-100: failure, recovery, uncertainty

Restore the original rules first; keep both clients connected.

1. **Wrong route:** open `http://127.0.0.1:8009/missing`. Expect HTTP 404 from
   a reachable service, then return to the controller.
2. **Wrong port:** if no exercise service uses 8011, open
   `http://127.0.0.1:8011`. Refusal differs from an HTTP error. If another app
   answers, do not assume that arbitrary port is empty. Return to 8009.
3. **Missing acknowledgement:** in A choose 73 and press **Send, ignore
   replies, disconnect**. This deliberately ignores replies after sending;
   it should show **Unknown**, never fake success. Observe whether B sees 73.
   Connect A again and compare its fresh snapshot. A snapshot reports current
   state, not a receipt for A's particular command.
4. **Stopped server:** Ctrl+C in terminal A. Both tabs become Disconnected;
   WebSocket send controls disable. An HTTP snapshot cannot reach the stopped
   listener. The last known scene remains visible with that label.
5. **Recover:** rerun `uv run python server.py`. Before reconnecting B, press
   **Read HTTP snapshot** there. Expect x = 50, revision 0, while the label
   still says Disconnected and identifies the HTTP snapshot. This reads current
   state once; it does not open a continuing connection or resend an action.
   Then Connect both tabs for live updates. New connections do not restore the
   old process's memory. Week 10 asks what should persist.

The ignore-replies demonstration removes one client observation; it does not
claim the network dropped a packet. In a real unanswered action the server
may have processed it, or may never have received it. There is no automatic
resend here. Decide what duplicates would do before adding retries.

For the real loopback checks, **stop your server first**, then:

```bash
uv run python -m unittest -v test_scene test_echo
```

They start temporary real HTTP/WebSocket/TCP services and clean up. They normally
use free ports. Maintainers can set `WEEK09_TEST_PORT=8009` on Linux/macOS to
check the documented port. A reported host-policy **skip** is not live proof.

## 100-120: tutor review and project support

This week's tutor delivery is the **first working interaction**, in the allocated
tutorial slot on 5 November. The tutor confirms exact team times. Show a usable
increment from your project; networking is inspiration, not a required feature.
Use this time to help a teammate run it and explain input, state, response,
one failure and recovery. Record run/test evidence, feedback and the next goal
in the team's existing accessible progress record. GitHub Projects is
recommended; an equivalent accessible record is valid. No extra Canvas upload,
attendance score or compulsory defence is introduced.

The project remains **40% of the course**, with **25% idea / 50% code /
25% execution**, due **6 December 2026, 23:59 HKT**. Use a shared public
repository owned by `sd5913`, with teammate Write access. Canvas is the submission
system; the [reviewed brief](https://github.com/sd5913/pfad/blob/4358b4e47b874ef40c120e63b2f6329acbe9b7d5/assignments/group-project.md)
controls assessment details.

## Optional bridges

- **MediaPipe:** map Week 8 index-fingertip x to `round(x * 100)`, clamp to
  0-100, and send `set_x` only when the value changes. No hand means no action.
  Send coordinates, not frames. The slider covers this boundary without a camera.
- **OSC:** Open Sound Control defines addresses such as `/scene/x` and typed
  values. An adapter could translate it into our JSON action. OSC commonly uses
  UDP, but OSC, UDP and WebSocket are different things. No second networking
  stack or OSC library is required here.
- **Games:** compare reliable “spend coin” events with frequent position
  snapshots. UDP may favor fresh updates over retransmitting old positions;
  the application must decide how to handle loss and order. Reliable transport
  still does not prove a game applied an action.
- **LAN/mobile:** accessing another machine changes addresses, exposure and
  firewall assumptions. It is an optional separately rehearsed extension; this
  service deliberately stays on loopback.

## Fallback and troubleshooting

Pair on a working laptop and take turns. If no machine can run a server,
draw A, server and B. Give the server `x=50, revision=0`. A writes JSON; the
server validates, changes its card, and writes two state messages and one ack.
Reject 101 without changing the card. Hide A's ack while B receives state;
reconnect A for a new snapshot. Label this **paper simulation**, not live proof.

| Symptom | Inspect and recover |
| --- | --- |
| `No module named fastapi` | Run from `week09` with `uv run`, not a bare system Python |
| Package download fails | Check normal internet access; use a prepared partner laptop |
| Address already in use | Close your earlier server or choose a deliberate alternate port |
| Browser shows a local file | Open the server's HTTP URL, not `index.html` directly |
| 404 on `/statee` | Correct the route; the server did answer |
| One tab seems frozen | Read its connection label; Connect after restarting |
| Edit has no effect | Restart Python and reconnect; inspect your actual file/diff |
| Revision resets to 0 | A new process starts a new in-memory scene; there is no database |

## Sources and verification

Primary documentation checked **29 October 2026** through Context7:
[FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/),
[websockets client](https://websockets.readthedocs.io/en/stable/reference/sync/client.html),
and [uv projects](https://docs.astral.sh/uv/guides/projects/).
[OSC specification](https://opensoundcontrol.stanford.edu/spec-1_0.html) supplies
the creative-protocol comparison, not an implemented OSC integration.

Dependency targets are current upstream releases verified through GitHub on
29 October: **FastAPI 0.162.0** (23 October), **uvicorn 0.54.0** (25 September),
**websockets 17.3** (19 October), on Python 3.13. Exact transitive lock capture
and latest-pin runtime acceptance await normal-network CI.

Linux x86_64 / Python **3.13.16** preparation: four rule and five actual
in-memory ASGI checks pass with cached FastAPI **0.142.2**, Starlette **1.7.0**,
uvicorn **0.54.0**, websockets **17.2**, Pydantic **2.10.6**. This is not
latest-pin acceptance. The authoring host forbids sockets, so both live suites
explicitly skip there. Nine deterministic checks of the production JavaScript
pass with controlled browser boundaries, and syntax checks pass. Real two-browser behavior,
desktop/mobile appearance, default-port coexistence with the presenter, and
Windows/macOS execution still need the separate live checks.

Maintainers: `node test_browser_state.cjs` executes the production inline
JavaScript with controlled DOM/network/timer boundaries. It checks delayed
results and safe manual refresh, but does not prove browser layout or networking.
Manual HTTP reads while disconnected accept the newest fresh response if no
newer state or connection intervened. Older overlapping responses cannot roll
back a newer observation; revision order is still enforced for the live stream.

[check_browser.cjs](check_browser.cjs) owns server startup, shutdown
and restart on 8009; do not start another server for it. With Playwright 1.64.1
and Chromium installed, `node check_browser.cjs` checks two pages and recovery.
`WEEK09_PYTHON` selects this folder's Python; `WEEK09_SCREENSHOT_DIR` optionally
retains desktop/mobile screenshots and a browser trace. These are prepared
checks, not a claim that a browser run passed.
