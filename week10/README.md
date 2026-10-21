# Week 10 — one class, two objects, somewhere to keep them

**Thu 12 Nov 2026.** This companion starts with classes and objects before
database machinery. Run from the `pfad` repository root with Python 3; only
the standard library is needed (no install, account, API key or Docker).

## Run the fictional example

Read [artworks.py](artworks.py) first. `Artwork` is one class; `amber` and
`blue` are separate objects. Predict their `views` after `amber.view()` before
running this command:

```bash
python week10/artworks.py save --file week10/out/artworks.json
```

It prints `a1=3, a2=7` and writes **only** the explicit, disposable
`week10/out/artworks.json` file. Look at the JSON: exhibition `e1` is linked
to artworks `a1` and `a2` by `exhibition_id`. IDs stay the same even if a
title changes. The file contains values, not the `view` method or Python
objects. The `week10/out/` folder is git-ignored; do not add real student
records, passwords or credentials. Save refuses to overwrite an existing file;
use a new path if you want another trial.

**Restart test:** close your Python session or terminal, open a new one in the
same repository root, then run:

```bash
python week10/artworks.py load --file week10/out/artworks.json
```

The new process reconstructs both artworks from JSON, checks their exhibition
link, and calls `view()` on the reloaded `a1`. It prints `a1=4 (not saved)`:
loading and changing an in-memory object does **not** change the file. Run
`load` again to see the stored `a1` count is still 3.

Try a missing file and a broken ID. Both `load` commands should report an
error; a JSON file alone cannot enforce a relationship:

```bash
python week10/artworks.py load --file week10/out/missing.json
python week10/artworks.py save --file week10/out/broken.json --broken-link
python week10/artworks.py load --file week10/out/broken.json
```

The last command reads valid JSON, but `a2` points to nonexistent exhibition
`e99`. `missing.json` should not exist for the first failure; choose a new
unused name if you already created it. These failures are deliberate. To
check the example automatically, run:

```bash
python -m unittest discover -s week10 -p 'test_*.py'
```

## Activity 1: describe a thing in your project

Choose a player, artwork, note or other simple thing, not a real user account.

1. Name its class and two attributes. Give each attribute a useful type.
2. Describe two separate objects of that class with different attribute values.
3. Give the class one small behaviour. Predict how calling it on one object
   changes that object's state without changing the other.
4. Trace the before/after values on paper, then compare them with the
   `save` output and the class in `artworks.py`.
5. Have another person explain the difference between the class, an object,
   an attribute and a method using this example.

No inheritance hierarchy, framework or advanced asyncio is needed.

## Activity 2: what must survive closing the program?

1. Decide which attributes you need to save and which can be calculated again.
2. Give each saved object a stable ID. Sketch a tiny table with two records.
3. If two kinds of object are related, show the ID connecting them. A simple
   one-to-many example is enough.
4. Predict what happens if a record refers to an ID that does not exist.
5. Compare the sketch with `week10/out/artworks.json`. Run `load` in a fresh
   process and check what survived.

**Working evidence:** two-object trace and a small table/relationship sketch,
not a new assessed submission.

## Optional retrieval extension

If time and the project justify it, use three public passages and ask which
one supports a question. Keep the source label. Try a question the passages
cannot answer. Retrieval returns candidates, not proof that an answer is true.

## Setup and fallback

Use fictional sample data. If Python is unavailable, draw the two objects and
the JSON records on paper. Increase only Amber's views from 2 to 3, keep Blue
at 7, then imagine closing the program and reconstructing both from the
saved records. Draw exhibition `e1` and its two `exhibition_id` links; change
one link to `e99` and explain why it cannot be resolved.

Do not copy the archived login app: its unsalted SHA-256 password hashing is
known unsafe. Authentication and real credentials are outside this activity.
Docker/Qdrant and embedding models are optional, not a prerequisite for learning
what an object or a saved record is.

## Sources and release checklist

- Supplied “SD5913 - PFAD - Week 10.pdf”: pp13–30 objects, relationships,
  IDs, schema and SQL/Peewee; pp32–38 database choices; pp44–55 retrieval;
  pp56–67 tutorial. The pp39–43 login example must not be copied.
- Related class/object recap: supplied Week 13 PDF, p8.
- Historical [Week 10 code](https://github.com/sd5913/pfad/tree/2025/week10)
  and [known errata](https://github.com/sd5913/pfad/blob/2025/ERRATA.md).
- Proposed adaptation: the two-object trace and fictional records simplify the
  source material in line with the current focus on accessible classes.
- The optional retrieval exercise needs no downloads or separate service.
