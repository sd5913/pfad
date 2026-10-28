# SD5913 Student Material Authoring

Read [AUTHORING.md](AUTHORING.md) before creating or reviewing a week's examples
or tutorial. It complements the
[teaching-repo guide](https://github.com/sd5913/teaching/blob/1b3ba08a7099c74db037f799cca733cfe633bad0/docs/COURSE-AUTHORING.md).

- The audience is artists, designers and game-design students learning to read,
  reason about and verify programs. Python is the conceptual language; use
  tangible games, apps, scenes and interactions to explain the computing ideas.
- `weekNN/README.md` is the **complete 120-minute student/TA tutorial**, separate
  from the 120-minute lecture. Budget setup, exercises, break, troubleshooting,
  verification and tutor reviews. A list of links or a short starter is not the
  finished tutorial. Week 13 is final tutorial/project support, not another
  new content practical.
- Read actual earlier weeks and the paired lecture before authoring. Reuse
  classes/methods and earlier concepts to explain new systems; avoid teaching
  the same two-object example each week. Compare the relevant 2025 archive and
  explain deliberate updates instead of silently dropping material.
- Preserve dependencies across weeks: persistent model classes and related
  rows, embeddings/semantic retrieval, then exploration of those same vectors
  and sources. Maintain a source-to-lesson concept crosswalk; replacing setup
  does not authorize deleting the teaching idea.
- Give each exercise an exact command, expected output/observation, a code
  location to inspect, a small edit or prediction, a check and a recovery path.
  Students should be able to do the work without the instructor's login or a
  ClassPoint activity.
- Use `uv`. Prefer `cd weekNN` then `uv run python example.py`; add flags only
  when they solve a demonstrated need. Isolate incompatible weekly dependencies
  from the existing root Worker project. Use compatible pinned versions and
  current documentation; check platform support and first-run downloads.
- Keep the core exercise reproducible without paid APIs, a dedicated GPU, a robot or
  instructor-only infrastructure. State real prerequisites and provide a
  meaningful local/fixture fallback. Label recorded traces and simulations
  accurately, and still test the actual advertised live integration.
- Test behavior and failure paths, not only imports or helper return values.
  Rehearse multi-process commands together, use a non-conflicting demo port,
  and verify the visible result in the target application. Record what remains
  untested instead of calling a headless test a classroom rehearsal.
- Weekly ideas are optional project inspiration. Do not impose AI, camera
  input, a specific engine, app-store publication or another graded submission.
- Group project: **40% of the course, 25% idea / 50% code / 25% execution,
  deadline 6 December 2026, 23:59 HKT**. Each group uses one shared public
  repository **owned by `sd5913`**, with teammate write access. Use the
  recommended [course Project template](https://github.com/orgs/sd5913/projects/1) through
  **Use this template**; check its current title and configure Project access
  separately from repository access.
  An equivalent accessible shared planning/progress record remains valid.
- Tutor review weeks are 5, 12, 19 and 26 November, then 3 December. Exact
  meeting times follow the allocated tutorial slot and tutor confirmation.
  Records support the existing execution criterion; no new grade, upload or
  compulsory defence is introduced.
- Current teaching uses branch `2026`; `2025` is an unrelated archive. Never
  merge those histories. Preserve other authors' work and all accepted weekly
  index entries. Use a feature checkout and the existing weekly teaching/PFAD
  PR pair. Pin unmerged companion links to verified commits.
- Do not merge, publish releases, send messages to students/tutors or alter
  course infrastructure as part of draft authoring. Credentials, student
  records, captures, private keys and graded-assessment answers stay out of
  public repos, fixtures, PRs, logs and artifacts.
