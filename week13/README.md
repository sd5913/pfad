# Week 13 — explain the loop, explain your work

> **Thursday 3 December 2026; draft activity.** The supplied Week 13 PDF confirms a recap,
> final test and conclusion in last year's final week. Its 10am timing and
> Blackboard instructions are historical, not confirmed 2026 arrangements.
> This companion is practice, not an assessed task.

## Try a loop with an end

[`loop.py`](loop.py) is a tiny, original Python example using only the standard
library. It matches the eight-line `limit = 3` / `step = 0` / `while step < limit`
example in the Week 13 teaching deck; the few extra lines above it allow a
different limit on the command line. No dataset, account, network call, API key,
framework or package installation is needed to run it.

Before this draft is merged, a reviewer can start with a fresh checkout of
PR #16 (Python 3.10 or newer is the only runtime requirement):

```bash
git clone https://github.com/sd5913/pfad.git
cd pfad
git fetch origin pull/16/head
git switch --detach FETCH_HEAD
python3 week13/loop.py
```

After this companion is released on `2026`, run `python3 week13/loop.py` from
your updated course checkout instead of fetching the PR.
If your computer's Python command is `python` rather than `python3`, use that
command with Python 3.10 or newer. `uv run week13/loop.py` also works for the
course's usual `uv` workflow, but `uv` is not required for this example.

Before running, predict each line. With no argument, `limit` is 3. `step` starts
at 0, is printed, then increases by one on each pass. The test is checked again
*before* the next pass:

| Test | Printed by the loop | `step` after pass |
|---|---|---|
| `0 < 3` | `0` | `1` |
| `1 < 3` | `1` | `2` |
| `2 < 3` | `2` | `3` |
| `3 < 3` | nothing | `3` |

When the test is false, the loop stops and `print("done")` runs once. Expected
output, on **separate lines**:

```text
0
1
2
done
```

Now try the boundary case from the deck. From the repository root, run
`python3 week13/loop.py 0`. The optional `0` replaces the default limit. Since
`0 < 0` is false immediately, the loop body never runs; the entire output is:

```text
done
```

To check both outputs automatically (no pytest or other dependencies), run
`python3 -m unittest discover -s week13 -p 'test_loop.py'`. A successful check
says `Ran 2 tests` and `OK`. The test invokes the real script with its default
and zero limits. If you change the expected output, make a prediction first.
The input must be a whole number: a word such as `three` produces a
`ValueError`, rather than a loop result. For a negative limit the body also
never runs because `step` starts at 0.

If another person cannot reproduce your result: check that they have the
`week13/loop.py` file from this branch, run the command from the `pfad` folder,
check `python3 --version`, and compare the argument and printed lines with the
table. `No such file or directory` usually means the current directory or
branch is wrong. `ModuleNotFoundError` from another project means it may have
undeclared dependencies; this particular script needs none. An absolute path
on one person's machine or a private input file would not transfer to a fresh
checkout. If `step += 1` is removed, `step` stays at 0 for limit 3 and the loop
does not end: reason about that change **on paper only**, not by running it.

## Proposed activity

Choose a small part of code you have actually used this semester. Trace it
carefully enough that another person can predict what happens.

1. Mark its inputs, changing state and output.
2. Choose a normal input and predict the result before running it.
3. Trace one repeated step or loop by hand. Say what changes and what makes
   it stop.
4. Try one failure or boundary case. Explain what the program does, not only
   what you hoped it would do.
5. Swap explanations. Ask a teammate to point to the line responsible for the
   behaviour and one improvement that keeps the purpose small.

**Working evidence:** a short trace, one observed result and one limitation.
Use it for revision and project documentation, not as a new assessment.

## Optional archive comparison

The [2025 semester loop](https://github.com/sd5913/pfad/blob/2025/week13/semester.py)
offers a longer example of state and control flow. Read a selected excerpt
rather than treating its simulated grades, assignment names or random
outcomes as current course rules. The whole script is not required.

A paper trace works without installation. The runnable example above uses only
values, a condition and a loop already covered in the taught 2026 weeks; no
unfamiliar framework is needed in the final review.

## Tutorial: can somebody else run it?

Following the old tutorial's practical emphasis, give another person your
repository's run instructions and ask them to try the intended interaction on
another computer when available. Note missing files, absolute paths, hidden
dependencies and unclear instructions. Fix one small reproducibility problem.
Do not publish secrets or private data to make the example work.

This is preparation and feedback, not a newly invented submission deadline.

## Course boundary

Review taught material and the actual project brief. Do not invent a showcase
date, new portfolio submission, final-quiz format or extra deliverables.
The current overview lists the final quiz as 10%; its scheduling and
instructions must come from the instructor.

## Sources and release checklist

- Historical: [2025 Week 13 script](https://github.com/sd5913/pfad/blob/2025/week13/semester.py).
- Current: [course overview](../README.md) and the material actually taught.
- The activity is a proposed adaptation, not a confirmed final-week plan.
- Supplied “SD5913 - PFAD - Week 13.pdf”: agenda p2; recap pp3–26;
  class/object p8; Scrum/Docker/networks pp13–17; MCP pp25–26; AMA p27;
  another-computer test p28. Use these as a map, not a new topic list.
- Do not copy p5's misleading assignment/copy wording or p21's unsafe
  unsalted-password-hash screenshot. Do not make advanced asyncio a core topic.
- Pending: later-week taught scope and confirmed final-week arrangements; review
  later topics only if they were actually taught.
