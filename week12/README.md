# Week 12 — review, then act (Thu 26 Nov 2026)

First review one small project interaction; then inspect who may run a tool.
This is **practice, not a new assessed deliverable or deadline**. AI is optional
in your group project. You do not need a model account, an API key, a model
download, paid services or permission to edit anyone's files.

## 1. Review one small change

Choose a representative interaction in your own project. What does the person
do, what should they see, and what happens when an input is missing or wrong?
Can another person follow your README to try it? Identify one small fix, one
normal case and one failure case. If a calculation is repeated, a pure function
can make that rule easier to test. For example, `add(3, 4)` should return `7`
and `add(-2, 2)` should return `0`. Test what happens with a string or missing
number too; Python's `+` alone is not a helpful input error.

## 2. Predict the tool call on paper (no execution)

Label the **person**, **model proposal**, **host application with MCP client**,
**MCP server**, **tool implementation**, **tool result** and **final answer**:

```text
Person:            add 3 and 4
Model proposal:    tool=add, arguments={"a": 3, "b": 4}
Host decision:     name allowed? exact inputs? permission to dispatch?
MCP client/server: send call only if checks pass; server exposes add
Hypothetical tool: add(3, 4) -> 7, if dispatched successfully
Expected result:   7, returned to host if the call succeeds
Final answer:      7 only after a successful result is actually observed
```

This whole diagram is **only a paper/static trace**: predicting `7`
does not prove a server ran. The host mediates execution; the model cannot grant
itself permission by naming a tool. MCP describes the exchange, not a security
policy. The server exposes only `add`; its pure function neither reads nor
writes files. The host's separate allowlist permits only `add` with exactly two
integer arguments. Booleans, although Python considers them integers, are
rejected here. Inspect these *proposals* before anything runs:

| Proposal | Decision | Result to report |
|---|---|---|
| `add` with `{"a": 3, "b": 4}` | Allowed | Inspect actual result `7` |
| `overwrite` with `{"path": "work.txt"}` | Blocked by host; never sent | Refusal, not a completed write |
| `add` with `{"a": 3}` | Invalid: missing `b`; never sent | Ask for the missing input |
| `add` with `{"a": "3", "b": 4}` | Invalid: wrong type; never sent | Correct the input |

If a tool reports an error or no result, stop and report that failure; do not
claim the addition succeeded. There is no overwrite implementation in this
exercise, and no arbitrary filesystem, shell, network or account tool. Real
applications need explicit human review before paid generation, external sends
or overwrites, as well as their own host policy and isolation.

## 3. Run the local simulation (no installation)

From the root of this `pfad` checkout, use Python 3.10 or newer:

```bash
python week12/trace.py
python -m unittest discover -s week12 -p 'test_*.py' -v
```

`trace.py` implements the pure `add(a, b)` and a host-like check with the
standard library. It prints the four cases above. It is **not an MCP server**,
not a client and not a model: it calls the local function directly. The tests
check normal/negative addition, rejected non-integers, a blocked name and
missing/extra/wrong arguments. If `python` is not the name of your Python,
use `uv run --no-project week12/trace.py` instead; the empty PEP 723 dependency
block requires no third-party packages. On a machine without either Python or
`uv`, use the paper trace in section 2; it needs no device setup.

## 4. Optional real local MCP smoke test

Only if you have `uv` and can install dependencies, run this from the same root:

```bash
uv run --no-project week12/check_mcp.py
```

This runs a **real MCP client and server over local stdio**. The script's PEP
723 block pins `mcp==1.15.0` and `pydantic==2.11.9`; the matching server script
has the same pins (this is not a full transitive lockfile). First use may
download those Python packages and their transitive dependencies, but no model,
GPU, login, credentials, paid API or
remote MCP service is used. The client starts `add_server.py` in the same
isolated Python environment, initializes MCP, verifies the one advertised tool
and its two integer inputs, then calls it with `3, 4`. It checks the returned
text is `7`. The other three proposals are refused **at the host before
dispatch**; they are not
server-side error responses. The server writes protocol messages to stdout,
never teaching text. No files are overwritten. If dependency installation or
stdio fails on your machine, do section 3 or the paper trace instead; do not
substitute an untested remote transport or claim the live call succeeded.

Verification for a reviewer:

```bash
python -m unittest discover -s week12 -p 'test_*.py' -v
python week12/trace.py
uv run --no-project week12/check_mcp.py
git diff --check
```

The live check raises an error if discovery, the MCP call or the result differs.
This is a local protocol smoke test, not proof that a model selected the tool or
that a general-purpose host is secure. A direct button calling `add` may be a
better project design than an agent choosing an action.

## Sources

- Current MCP [architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
  and [server concepts](https://modelcontextprotocol.io/docs/2026-07-28/learn/server-concepts)
  (2026-07-28 documentation, checked 21 Oct 2026).
- Historical [2025 Week 12](https://github.com/sd5913/pfad/tree/2025/week12)
  and [errata](https://github.com/sd5913/pfad/blob/2025/ERRATA.md). The
  supplied 2025 PDF pp. 25-34 covered small checks and p. 51 showed a tiny
  FastMCP addition example; its ComfyUI/submodule installation is not part of
  this activity. The errata warns against binding tools to a dead event loop
  through repeated `asyncio.run()` calls; the live client uses one session and
  one async lifecycle.
