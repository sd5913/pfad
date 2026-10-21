# Week 12 — inspect a tool call before it acts

> **Planning draft for 2026.** Based on the supplied MCP slides, especially
> the tiny addition tool on page 51. Keep the agent → server → tool → result
> path visible. The archived Streamlit/ComfyUI integration is not the starter.

## Proposed activity

Trace a request, a proposed tool call, a tool result and a final response.
Start with prepared text examples rather than a live agent.

1. Start with a tiny request: “add 3 and 4”. The agent proposes an addition
   call; the MCP server exposes the tool; the tool returns 7. Identify each
   role. The server does not become the language model.
2. Read the proposed tool name and arguments. Predict the result.
3. Check whether the call matches the request and uses valid inputs.
4. Compare the tool result with the assistant's final answer. Did it report
   the actual result or claim something that did not happen?
5. Try a missing argument, a failed tool result and a request outside the
   allowed scope. Mark where the system should stop or ask a person.

**Working evidence:** one labelled call/result trace and a failure case.
This is a proposed practice exercise, not a new assessed deliverable.

## Who does what?

The AI host application contains an MCP client. The client connects to an MCP
server that exposes the addition tool. The model proposes a call; the
application mediates execution and permissions. MCP standardizes the exchange,
not automatic trust or safety. Keep these boundaries visible in the trace.

## Small live practical, after preflight

Prepare one local MCP server exposing only a pure addition function. First
inspect its name, argument types and returned value with a prepared client;
then connect an already-available local model/agent if appropriate. Compare a
valid call with a missing or wrongly typed argument. Do not expose shell,
filesystem, network, image-generation or account tools. Keep a
human decision before any paid generation, external send or file overwrite.
A static trace is the core fallback; no account, paid API or new model download
is required.

Local stdio and remote Streamable HTTP require different setup. For this small
practical, select and preflight one local path; do not silently switch transports.
Pin the protocol/SDK versions before adding commands or code. Version-specific
discovery features and SDK APIs are not part of this handout until checked.
Advanced asyncio is not required for the core addition trace.

Do not copy the archived event-loop setup: the
[errata](https://github.com/sd5913/pfad/blob/2025/ERRATA.md) records tools bound to
a dead event loop through repeated `asyncio.run()` calls. Any replacement must
be implemented and tested separately before this README claims it runs.

## Group-project connection

Ask whether a tool-using agent adds a necessary interaction. A direct button
calling a known function may be clearer. AI need not be inside the product.

## Sources and release checklist

- Current primary references, checked **21 October 2026**: MCP
  [architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
  and [server concepts](https://modelcontextprotocol.io/docs/2026-07-28/learn/server-concepts)
  (2026-07-28 documentation).

- Historical: [2025 Week 12](https://github.com/sd5913/pfad/tree/2025/week12),
  [index](https://github.com/sd5913/pfad/blob/2025/README.md) and
  [errata](https://github.com/sd5913/pfad/blob/2025/ERRATA.md).
- The tracing activity is a proposed adaptation of the supplied slides.
- Supplied “SD5913 - PFAD - Week 12.pdf”: principles/testing/small steps
  pp25–34; MCP pp48–53; p51 visually shows FastMCP with add(a, b);
  heavier ComfyUI/submodule tutorial pp55–65 is optional context, not required
  installation. These steps are a bounded adaptation of the addition example.
- Pending: confirmed focus, prepared success/failure traces,
  and, only if retained, a separately tested lifecycle-safe live example.
