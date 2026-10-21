# Week 9 — send a message and see what comes back

> **Planning draft, not the confirmed 2026 tutorial.** Adapted from the supplied 2025 network/API slides.
> Confirm current lecture alignment and preflight the small starter.
> Week 4 already introduced APIs; build on it rather than repeating it.

## Proposed activity

Trace one message between a local client and an echo server.

1. Draw the two programs and label who sends first. Identify the address,
   port and protocol. Separate the program's role from the machine it runs on.
2. With a prepared localhost starter, send a short message and predict the
   reply. Change the message; check whether the reply matches it.
3. Send two messages on the same connection. Record their order.
4. Stop the server. What does the client show? Restart and reconnect explicitly.
5. Explain how this differs from asking for a fresh month of tide data in
   [Week 4](../week04/README.md).

**Working evidence:** a short sent/received trace and one disconnect observation,
not a new assessed submission.

## Setup and fallback

Keep the first exercise on localhost. Use made-up text, not personal data.
A two-person paper trace can show the same send/receive/disconnect sequence if
the environment is not ready. Network sharing between classmates is an
instructor-approved extension only; do not open firewall ports, bind publicly
or publish a server as a setup shortcut.

The archival examples need a compatibility check before exact commands become
2026 instructions. Microphone transcription is not required for this exercise.

## Group-project connection

Ask whether your interaction needs an immediate pushed update or a normal
request and response. A persistent connection adds state and failure cases;
choose it for a reason, not because it appears more advanced.

## Sources and release checklist

- Historical: [2025 Week 9 README](https://github.com/sd5913/pfad/blob/2025/week09/README.md)
  and [echo examples](https://github.com/sd5913/pfad/tree/2025/week09).
- Current: [Week 4](../week04/README.md), already-taught API foundation.
- The activity is a proposed adaptation. Old LAN and firewall instructions
  are not requirements for this version.
- Supplied “SD5913 - PFAD - Week 9.pdf”: pp23–35 layers, addresses,
  ports and transport; pp36–45 APIs/WebSockets; pp46–58 speech/async examples.
  Keep advanced asyncio and microphone streaming out of the core practical.
- Pending: confirmed focus, tested dependency versions,
  localhost starter, clean shutdown/reconnection and failure output.
