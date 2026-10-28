# Writing a complete PFAD tutorial

This repository is what students clone. Branch `2026` is the current course;
the unrelated `2025` branch is an archive. The lecture slides live in the
[teaching repository](https://github.com/sd5913/teaching). A weekly lecture and
its tutorial have different jobs: the lecture explains concepts and demonstrates
a system; the tutorial lets students inspect, change and verify it themselves.

The 2026 Week 7 Ball example and Week 8 vision README demonstrate the desired
concreteness. Use the latest instructor-reviewed versions when those weeks
are still in PRs. Their topics and exact example counts are not templates to
repeat in later weeks.

## Before writing code

Agree the high-level weekly outline with the instructor. Read the paired
lecture, earlier taught examples, current assignment brief and relevant 2025
examples. Record which concepts are new and which are prerequisites. The
current instructor's request overrides historical assessment or platform
choices. An old test that enforces a paper-only lesson is not a reason to
reject an approved hands-on revision; update obsolete assertions deliberately.

Keep a concept crosswalk from the original slide/page/example to its proposed
destination. Read adjacent weeks for dependencies, not only the matching week's
title. Preserve the progression from classes to persistent relational models,
from embeddings to semantic retrieval/RAG, and from those same vectors to
visual exploration and later tool/agent use. Modernize the installation or
framework while retaining the idea. Explain substantive removals in the agreed
outline; an audit recommendation or missing draft example is not authorization
to remove the concept.

Choose a small, observable outcome. For a game-design student, a color echo is
a useful networking starter; a connected interface that reacts to a message,
survives a disconnect and can be tested is a stronger complete tutorial.
Similarly, naming SQLite is not teaching persistence: students need to create,
query and change records, then observe what survives a restart.
Use meaningful model classes such as User, Account, Message and SaveFile;
trace a model method to stored rows/relationships and a reloaded object. Keep
SQL visible enough to explain the mapping. Data persists; method bodies remain
part of the program. One implemented relationship plus short modelling drills
is more achievable than several complete applications.

For embeddings, students need real model-derived numerical vectors, ranked
similarity results and source IDs/text/metadata. Compare exact lookup with
semantic retrieval and inspect sources before an answer is generated. Supply
the same corpus/vectors, encoder identity/version and dimension to any later
visualization exercise. Use sourced real-vector/query fixtures when downloads
are unavailable; do not label keyword matching as an embedding demonstration.

## README contract

Each `weekNN/README.md` must contain:

1. The date, learning outcomes and relation to the lecture.
2. Exact prerequisites, supported platforms, first-run setup and working directory.
3. A complete 120-minute route, including a break and recovery time.
4. Runnable exercises with expected observations and inspection/edit/check steps.
5. Failure handling and a meaningful fallback for unavailable services/devices.
6. A final result students can explain and reproduce.
7. Optional extensions and project inspiration, clearly separated from the core.
8. Relevant source links, tested versions and honest verification limits.

Use a timing table such as this one, adapting it to the actual exercises:

| Minutes | Activity |
| --- | --- |
| 0-15 | Setup and first successful run |
| 15-35 | Trace the smallest complete example |
| 35-55 | Make a focused change and verify it |
| 55-65 | Break |
| 65-85 | Add or inspect the second concept |
| 85-100 | Trigger a failure, diagnose and recover |
| 100-120 | Tutor review/project support and extensions |

When a tutor needs longer for the week's allocated deliveries, budget it
explicitly rather than placing it after two hours of exercises. The outcome
must remain achievable for beginners. No tutorial depends on the instructor
starting a ClassPoint activity or providing a private login.

## Exercise shape

Use a consistent sequence:

- **Predict:** what should happen, including one boundary or missing-input case?
- **Run:** an exact command from the stated directory, including all processes.
- **Observe:** describe a visible result, trace, response or saved record.
- **Inspect:** point to the relevant function, method, data shape or configuration.
- **Change:** one small, purposeful edit rather than an unexplained full rewrite.
- **Check:** compare against an explicit expected result or acceptance rule.
- **Recover:** show how to stop, reset or undo the experimental change safely.

Commands must name files supplied by the PR. Link to the actual examples, not
only the companion PR. Say which terminal starts the server, how readiness is
known, which terminal runs the client, and how to stop both. Use a demo port
that does not collide with the presenter or other required services. Local
tests using a free port do not prove the README's default port is available.

Explain technical concepts in plain language while retaining correct terms.
Have students inspect existing code before asking them to generate new code.
An AI-assisted change still needs a stated behavior, visible diff and evidence.

## Environments and assets

Use `uv` for Python. Prefer simple student commands:

```bash
cd weekNN
uv run python example.py
```

Use the exact command appropriate to the supplied project; this is the shape,
not a claim that an `example.py` exists in every week. Add `--project`,
`--locked`, groups and other flags only when required and explained. CI can use
stricter reproducibility options without making the student workflow verbose.

The root Python project also serves an earlier Worker example. Use a separate
weekly `pyproject.toml` and lockfile when dependencies/runtime requirements
conflict. Check that documented commands discover the intended environment.
Do not alter a shared environment or all old examples to accommodate one week.

Fetch current primary documentation for library/API/CLI use. Pin a compatible
tested set; latest should mean verified and supported. State OS/architecture
limits and the time/size of substantial first-run downloads when known. Keep
downloaded models, build outputs, camera frames and local caches ignored.
Document asset provenance and licenses.

## Services, creative software and agents

Distinguish a local demonstration from a deployed service. Check connectivity,
addresses, process lifetime, cleanup and data persistence. Use sample secrets
and environment-variable names; never commit real tokens. Do not require a
publicly reachable local tool server.

For Blender, Godot or another external application, provide a minimal project
or scene, installation/startup instructions, the exact application/bridge
versions and a visible acceptance check. Identify third-party MCP servers
accurately. Check both the protocol and the application outcome. A stubbed
tool test or discovery response cannot prove the scene changed or the game ran.

For an agent exercise, expose the goal, available actions, observations,
state, stopping condition and limits. Show where the agent decides the next
action. Distinguish that loop from a fixed rendering workflow, and label a
recorded/replayed trace as such. Keep account/model requirements explicit.
Provide a local tool/replay route when students cannot run the live model;
explain what this fallback does and does not demonstrate.

Paid generation, specialist GPUs and robot hardware can support optional
instructor demos. They are not silently required equipment for a normal
tutorial. Do not generate media or incur API charges merely to prepare a plan.

## Group-project connection

Use [the current reviewed brief](https://github.com/sd5913/pfad/blob/4358b4e47b874ef40c120e63b2f6329acbe9b7d5/assignments/group-project.md)
for assessment policy. This source is pinned while its PR is open; refresh it
to the accepted live-branch version after authorized integration.
Current project: 40% of the course, 25% idea / 50% code / 25% execution, due
6 December 2026 at 23:59 HKT. Each group uses a shared public repository
owned by `sd5913`, with teammate write access. The
[Project template](https://github.com/orgs/sd5913/projects/1) starts through
**Use this template**. Its name may change; verify the actual page. Project and
repository access are separate settings.
This is the recommended route; an equivalent accessible shared planning and
progress record remains valid. The choice of board is not a grading criterion.

Tutor review weeks are 5, 12, 19 and 26 November and 3 December; the tutor
confirms exact times in allocated tutorial slots. Weekly goals, usable work,
tests/playtests, feedback and next actions support the existing execution
criterion. Link evidence from the team's README. This adds no Canvas upload,
attendance score, formal Scrum-role requirement or compulsory defence.

Ask whether a technique could inspire the team's project. Do not require
computer vision, AI, a particular framework or an app-store release. Week 13
is final tutorial/project help, including support for unfinished work; it does
not introduce another technical stack or assessment requirement.

## Verification and PR handoff

Run the README's core commands from a clean environment and test meaningful
behavior: boundaries, malformed input, restart persistence, disconnects and
cleanup as relevant. Keep automated tests independent of live accounts and
hardware where possible. Separately rehearse advertised live integrations.
Documentation-only changes usually need a diff/link/content check, not tests
that mirror their prose.

Keep each week in its existing PFAD PR paired with the corresponding teaching
PR. Describe the final outcome, core commands, platforms/versions checked,
failure paths and remaining classroom rehearsal needs. Use precise companion
commit links while unmerged. Preserve the union of accepted weekly index
entries and CI coverage during authorized integration. Keep private student
data and assessment keys outside this public repo. Do not merge or release a
draft just because its tests are green.
