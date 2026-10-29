# SD5913 — Programming for Artists and Designers

PolyU School of Design · 2026

This repository holds the weekly material for SD5913. It is built as the semester
runs, so expect it to grow week by week — `git pull` before each class.

---

## Start here

1. **Register your GitHub account** against your student ID:
   **<https://pfad.ait4x.org>**. One minute. This is how your work gets matched
   to you, and it is how you get invited to the
   [`sd5913`](https://github.com/sd5913) organisation.
2. **Work through [`week01/README.md`](week01/README.md).** It takes you from
   "no GitHub account" to "my first repository is published".
3. **Read [`assignments/01-why-are-we-here.md`](assignments/01-why-are-we-here.md).**
   Your first assignment is due at the end of week 2. Before you submit, run
   [the check](assignments/check.py) inside your repo — it tells you what is missing.
4. **For the current lesson, go to [Week 7: from an idea to one interaction](week07/README.md).**
   The [weekly content index](#weekly-content) links to the same material.

```bash
git clone https://github.com/sd5913/pfad
cd pfad
```

New to the terminal, to folders and paths, or to files whose names start with a
dot? [`reference/files.md`](reference/files.md) is ten minutes and every week assumes it.

## This repo has two branches, and that is on purpose

```
2026   ← you are here. This year's course. The default branch.
2025   ← last year's complete course. Frozen, kept for reference.
```

Branches are parallel versions of the same repository. They share a name and a
remote, but their contents are independent — you move between them and the files
on disk change under you.

Have a look right now:

```bash
git branch -a          # every branch this clone knows about
git switch 2025        # last year's course, all 13 weeks of it
ls                     # different files entirely
git switch 2026        # back to the present
```

Last year's material is genuinely useful — it is a complete, working course, and
several of this year's assignments have a 2025 ancestor worth reading. It is just
not *this* year's material, so it lives out of the way on its own branch instead
of cluttering the folder you work in.

You will use branches for real later, when your group project has three people
changing code at once and you need to work without standing on each other. For
now, know that they exist and that switching between them is free.

> The 2025 edition also still lives at
> [`venetanji/pfad`](https://github.com/venetanji/pfad) if you would rather browse
> it as its own repository.

## Reference

The [Week 7 activity](week07/README.md) is the current lesson. The draft
[Week 8 companion](week08/README.md) builds on it; earlier
[sound, music and speech](week06/README.md) and
[images and frames](week05/README.md) examples remain available.

Five pages the weekly tutorials assume and do not repeat — index at
[`reference/README.md`](reference/README.md).

- [`reference/files.md`](reference/files.md) — folders, paths, and the names that start with a dot.
- [`reference/git.md`](reference/git.md) — the six git commands you use, branches, and what the check looks at.
- [`reference/uv.md`](reference/uv.md) — what `uv run` does, and the `# /// script` block every script carries.
- [`reference/python.md`](reference/python.md) — every Python construct taught so far, with the slide it came from.
- [`reference/errors.md`](reference/errors.md) — the error message you are looking at, what it means, what to do.

## Assignments

| # | What | Weight | Due |
|---|---|---|---|
| 1 | [Why are we here?](assignments/01-why-are-we-here.md) — a reflection, published as a repository | 5% | Sun 13 Sep 2026, 23:59 |
| 2 | [Data visualisation](assignments/02-data-visualisation.md) — numbers about a natural phenomenon, made into a picture | 10% | Sun 4 Oct 2026, 23:59 |
| 3 | Interactive experience project | 15% | Sun 1 Nov 2026, 23:59 (Hong Kong time) |

Plus participation (10%), a mid-term quiz **in class on Thu 22 Oct 2026**
(10%), the group project (40%), and a final quiz (10%).

The Assignment 3 brief and submission instructions will be provided separately;
this date is a reminder, not the complete assignment specification.

**Everything you submit in this course is a portfolio piece.** Your repositories
are public, your commits carry your name, and they accumulate into something you
can show people. Treat them accordingly.

## Weekly content

| Week | Topic |
|---|---|
| 01 | [Git, GitHub, and your first repository](week01/README.md) |
| 02 | [Your repo passes the check · predict, break, fix](week02/README.md) |
| 03 | [Numbers into pictures — data, loops, functions, matplotlib](week03/README.md) |
| 04 | [One control, one clear response — Streamlit, browser events, FastAPI and a test](week04/README.md) |
| 05 | [Images, frames and representations — 8 October 2026](week05/README.md) |
| 06 | [Sound, music and speech — WAV samples, browser instruments and a local voice bot](week06/README.md) |
| 07 | [From an idea to one interaction — 22 October 2026](week07/README.md) |
| 08 | [Camera interactions — OpenCV, MediaPipe and teamwork (29 October 2026)](week08/README.md) |
| 1 | [Why are we here?](assignments/01-why-are-we-here.md) — a reflection, published as a repository | 5% | Sun 13 Sep 2026, 23:59 |
| 13 | [Final quiz, revision and project support - class date TBC](week13/README.md) |
| 2 | [Data visualisation](assignments/02-data-visualisation.md) — numbers about a natural phenomenon, made into a picture | 10% | Sun 4 Oct 2026, 23:59 |
| 3 | Interactive experience project | 15% | Sun 1 Nov 2026, 23:59 (Hong Kong time) |

More lands each week.
