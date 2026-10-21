# Week 10 — one class, two objects, somewhere to keep them

> **Planning draft for 2026.** Based on the supplied 2025 data-storage slides,
> with classes and objects made explicit before database machinery.

## Activity 1: describe a thing in your project

Choose a player, artwork, note or other simple thing, not a real user account.

1. Name its class and two attributes. Give each attribute a useful type.
2. Describe two separate objects of that class with different attribute values.
3. Give the class one small behaviour. Predict how calling it on one object
   changes that object's state without changing the other.
4. Trace the before/after values on paper, then compare them with a prepared
   small Python example once it has been checked for class use.
5. Have another person explain the difference between the class, an object,
   an attribute and a method using this example.

No inheritance hierarchy, framework or advanced asyncio is needed.

## Activity 2: what must survive closing the program?

1. Decide which attributes you need to save and which can be calculated again.
2. Give each saved object a stable ID. Sketch a tiny table with two records.
3. If two kinds of object are related, show the ID connecting them. A simple
   one-to-many example is enough.
4. Predict what happens if a record refers to an ID that does not exist.
5. Compare the sketch with a prepared local storage example. Restart it and
   check what was saved.

**Working evidence:** two-object trace and a small table/relationship sketch,
not a new assessed submission.

## Optional retrieval extension

If time and the project justify it, use three public passages and ask which
one supports a question. Keep the source label. Try a question the passages
cannot answer. Retrieval returns candidates, not proof that an answer is true.

## Setup and fallback

Use fictional sample data. Paper traces cover both core activities if the
prepared Python/storage example is not ready. Exact scripts and commands need
preflight before this planning README becomes runnable instructions.

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
- Pending: aligned lesson, tiny tested Python/storage example, restart/data
  checks and optional retrieval path only if it serves the lecture.
