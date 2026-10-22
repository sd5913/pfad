# Week 9 — connected interactions (Thursday 5 November 2026)

Send a message, see what comes back, and make a missing reply visible. This
exercise needs two terminals on **one computer**, Python 3, and the files in
this folder. No package installation, browser, login, microphone, internet,
API key or personal data is needed. Use only the invented words below.

## Draw it first

Draw two boxes: **client** and **server**. An arrow marked `red` goes from the
client to the server; an arrow marked `red` returns. Which program sends first?
Label the destination `127.0.0.1:8765`: `127.0.0.1` means *this computer*
(loopback), and `8765` selects the listening program (port). They are two
programs on the same computer, not necessarily two computers. Their protocol
is **TCP with one newline (`\n`) ending each message**. A TCP read might
contain half a message or several messages, so the newline tells us where one
ends. This small example handles one client at a time.

## Run it locally

Open both terminals in the `pfad` repository root (the directory containing
`week09`). Leave terminal A running while using terminal B. Use
`python3 --version` to check Python is installed (on Windows, use `py` in place of
`python3` in every command).

**Terminal A — server:**

```bash
python3 week09/echo_server.py
```

It prints `Listening on 127.0.0.1:8765` and waits. It binds **only** to
loopback; do not change the address to `0.0.0.0`, open a firewall port or
share this service with other computers.

**Terminal B — client:**

```bash
python3 week09/echo_client.py
```

Before running it, predict what replies you expect and whether the client
reconnects between `red` and `blue`. Compare your prediction with the output:

```text
connected to 127.0.0.1:8765
sent: red
received: red
sent: blue
received: blue
closed first connection
reconnected to 127.0.0.1:8765
sent: green
received: green
closed second connection
```

`red` and `blue` travel in order over **one** open connection. Closing it is
an explicit disconnect; `green` uses a **new** connection. Sending bytes
alone would not prove that the other program processed them: here each
`received` line is printed only after the matching reply arrives.

## Interrupt an open connection

Keep terminal A (the server) running. In terminal B, use the pause option:

```bash
python3 week09/echo_client.py --pause-before-blue
```

Wait for `received: red` and the `Pause after red` prompt. The client has **not
sent blue yet**. In terminal A, press **Ctrl+C** to stop the server. Only then
press Enter in B. You should see `sent: blue`, followed by `No reply` on
stderr and a nonzero exit, with **no** `received: blue` or `green`. The
connection that carried red has closed; the client does not quietly create a
new one to finish blue. Depending on timing and operating system, the error
details in parentheses can differ.

What should a person see while waiting, after the failure, and when they
choose to retry? Draw these three screen states. For this controlled exercise
we know blue was not sent *before* we stopped the server; in a real
unanswered in-flight request, a missing reply alone cannot tell us whether
the server processed it. Do not automatically repeat actions that could have
side effects.

## Make connection failure visible; reconnect yourself

With the server stopped, run the ordinary client command in terminal B again:

```bash
python3 week09/echo_client.py
```

Expect `No reply` on stderr and a nonzero exit status, **not** a successful
`received` line. A stopped server refuses a new connection. Never display the
last reply as if it were new.

Start terminal A again with `python3 week09/echo_server.py`, then rerun
terminal B with `python3 week09/echo_client.py`. This creates new connections;
it does not resume the old one or automatically resend an unanswered message.
When finished, press **Ctrl+C** in terminal A.

If you see `Address already in use`, stop the earlier copy of this server or
use the *same different port* in **both** terminals, for example:

```bash
python3 week09/echo_server.py --port 8766
```

```bash
python3 week09/echo_client.py --port 8766
```

If the client times out or says `Connection refused`, check that A printed
`Listening` and that both use the same port. The client waits up to three
seconds for each connection/reply; the server closes an idle client after ten
seconds. You can restart and retry manually; there is no automatic retry.

## Connect this to Week 4

In [Week 4](../week04/README.md), the browser made an **HTTP** request such as
`GET /tides?month=9`; the service used the `/tides` route to return JSON, or
an HTTP error such as 404 for an unknown route. The Week 9 demo instead sends
short newline-delimited messages over a continuing raw **TCP** connection.
It has **no HTTP method, route, status code or JSON**. It is **NOT a WebSocket
or HTTP server/client**; a WebSocket has its own handshake and message framing.
HTTP can reuse transport connections too: the difference here is the
application's continuing exchange versus separate HTTP request/response
semantics, not a claim that HTTP always reconnects. A stopped service yields
a connection error, not an HTTP 404 response.

For your project, ask whether a local-only interaction, an HTTP request for
data, or live messages are really needed. Draw `control -> state -> visible
response`; include a waiting state and an honest error when no reply comes.
An ongoing connection adds state and failure cases, not guaranteed delivery.

## If Python or sockets are unavailable

Do the paper trace with a partner. One person is the client, one the server.
Write `connect 127.0.0.1:8765`, `send red`, `receive red`, `send blue`,
`receive blue` along a single line marked *connection 1*. Draw a close mark.
On a second line marked *connection 2*, write `connect`, `send green`,
`receive green`. Now cross out the server and try to connect again: write
`No reply: connection failed` instead of inventing a received message. Note
which program sent first, what stayed open, and what the person should see.
This is the same prediction and failure exercise without a running service.

## Local maintainer smoke test

From the repository root on Linux or macOS (uses Ctrl+C / SIGINT):

```bash
python3 -m unittest discover -s week09 -p 'test_*.py'
```

This starts a server on a free **loopback** port, verifies two ordered
newline-framed replies on one connection, reconnects, runs the example client,
pauses after red and stops the server before blue, and checks both interrupted
and refused connections report failure rather than a fake reply. It uses only
the Python standard library and leaves no listener running. No class
submission or deadline is attached to this practical.

## Verification scope

Independent verification (21 October 2026): the original local loopback smoke test passed on Linux x86_64 with Python 3.12.14, including ordered replies, reconnect, stopped-server failure and process cleanup. The paused disconnect exercise was added later; see the current PR checks for its result. Windows execution has not been independently checked.

The PR workflow checks every available Week 8–12 companion on an Ubuntu 24.04 runner, including the real local MCP smoke when Week 12 is present. It does not deploy or publish the course.
