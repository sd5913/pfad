# Week 10: persistent objects and a talking handbook agent

**Thursday 12 November 2026. This is a complete 120-minute tutorial, separate
from the 120-minute lecture.** Build on Week 7's classes, Week 8's inspected
programs and Week 9's requests/processes. Trace one system: related saved
conversations supply context to a source-backed handbook bot with spoken replies.

By the end you can explain and inspect:

- A `User`, `Conversation` or `Message` model, an instance, its SQL operation and stored row.
- Stable keys, references, ordinary indexes, owner-scoped queries and a fresh-process reload.
- A real handbook chunk/vector, a compatible query vector and a cited retrieval result.
- Previous turns actually entering a model request, an isolated conversation and a spoken answer.

## Prepare before class

Work in **`pfad/week10`**. You need `uv` and Python 3.12 or newer. The weekly
project and lockfile isolate dependencies from the repository's other examples.
Begin with the small storage dependency; there is no database server, Docker,
account, API key or dedicated GPU:

```bash
cd week10
uv run python storage_demo.py seed
uv run python storage_demo.py inspect
```

A prepared Linux x86_64 machine must have the local model server, public model
weights, pinned sentence encoder, eSpeak NG library/English voice data and
FFmpeg/`ffplay` before the tutorial. Follow [REHEARSAL.md](REHEARSAL.md); this is
preparation, not twenty minutes of surprise model installation. The core
application makes only loopback model requests on **127.0.0.1:11440**. It does
not contact a paid endpoint or download models during a conversation.

Only rebuilding the handbook index additionally needs Poppler's `pdftotext`
system executable (`poppler-utils` on Debian/Ubuntu or Fedora; `poppler` on
Arch). Check `pdftotext -v` before rebuilding; `uv` does not install this tool.
The supplied already-verified `fixtures/handbook.json` can be inspected and
used by the bot without Poppler or rebuilding. See the preparation guide for
the rebuild command and recovery steps.

The verified CPU route uses Qwen3.5-2B Q4_K_M (1.28 GB) and MiniLM (about 90 MB).
Allow roughly 3 GB for weights, runtime and the encoder environment, plus
package caches. On the tested Ryzen 9 5900HS laptop, a clean dependency install
from an empty cache took 12 seconds; re-downloading the chat model took 47
seconds on that connection. Your connection/hardware may be much slower.
The measured model-call timings are recorded in the preparation/evidence files.
No Windows/macOS execution claim is made; those systems can use their matching
llama.cpp release and normal eSpeak/FFmpeg installation, but must rehearse or
use a prepared partner machine. Linux is the verified route.

**At minute 10, pair with a prepared machine if setup is still failing.**
Alternate the keyboard and explanations. The supplied cited vectors can be
inspected without encoder/model downloads. [recorded-run.json](fixtures/recorded-run.json)
and [recorded-answer.wav](fixtures/recorded-answer.wav) are labelled recordings
of an actual local run, useful for inspection when a service is unavailable;
playing them does not establish a new live tool call, memory or synthesis.
A physical listener must check intelligibility/volume on the teaching speakers.

Use fictional profiles/questions only. The trace JSON contains the actual model
prompt; keep personal data out of it. Local names such as Ada are ownership
examples, **not authenticated accounts**.

## The complete 120-minute route

| Minutes | Work and evidence |
| --- | --- |
| 0-10 | Setup; first storage result; check prepared model/index/speech readiness |
| 10-30 | Create/load User, Conversation and Message; methods → SQL → rows |
| 30-50 | Exact history queries, keys/indexes, update/restart, constraints/rollback |
| 50-60 | Break |
| 60-70 | Real handbook vectors, three rankings and inspected cited passages |
| 70-90 | Typed question/follow-up; inspect model context; synthesize/play a reply |
| 90-100 | Reopen/isolate conversations; trigger one failure and recover |
| 100-120 | Tutor review and group-project support |

## 0-10: get a visible storage result

Run the preparation commands. A fresh file prints `user=1 conversation=1` and
two saved messages. The assistant seed explicitly says **prepared storage
example; no model was called**. Read the actual SQL, parameters, rows and index
names printed by `inspect`. IDs may differ in a reused file. Repeating `seed`
reuses an existing seed title; after `rename`, another Handbook conversation
can be created. Use `--db out/experiment.sqlite` for a separate disposable file.

Run the behavioral checks:

```bash
uv run python -m unittest discover -p 'test_*.py'
```

Expect 20 passing checks. Scripted model replies and synthetic coordinates
inside protocol unit tests are doubles; the separate learned-vector fixture
and recorded live model run supply different evidence. Green unit tests alone
do not prove a speaker can be heard or a model's factual claims are supported.

**Check/recover:** point to the database filename before experimenting. Do not
remove a database containing work you need. Use a new filename for a fresh run.

## 10-30: follow a model through a real row

**Predict:** does `Conversation.create(...)` store its methods or its field
values? Does an attribute assignment alone update the database?

Read [models.py](models.py). `Record` inherits Peewee's `Model`, supplying real
persistence/query methods. `User`, `Conversation` and `Message` inherit Record.
Each gets an automatic primary-key `id`. A conversation stores its owner's ID;
a message stores its conversation's ID. A foreign key is a reference, not a
copy of the parent object. No password/login app is required.

```bash
uv run python storage_demo.py inspect
uv run python storage_demo.py rename
uv run python storage_demo.py inspect
```

**Observe/inspect:** `rename` loads a conversation, changes `chat.title`, then
calls `.save()`. The separate inspection process reads the new title with the
same stored ID. Methods remain in Python; SQLite stores values/references.
The previous process's object is gone. Python's `id(chat)` is not this primary key.

**Change:** edit only the title string in [storage_demo.py](storage_demo.py).
Predict the new output, run `rename`, then inspect in a new process.
**Check:** title changes; owner and IDs remain. Now temporarily omit `.save()`
and repeat: another process must still see the previous saved value.
**Recover:** restore `.save()` and the original string; inspect your diff.

Spend the final five minutes explaining the path to a partner: Python method,
SQL operation, affected row and newly loaded object. A notebook printing the
same original object again is insufficient restart evidence.

## 30-50: exact queries, relationships and failure

Read `Store.owned_conversation()`, then `history_query()`. The application checks
the owner before selecting messages for that conversation. Read the actual
`SELECT ... WHERE conversation_id = ? ORDER BY id` and bound parameter list.
A parameter supplies a value; it is not pasted into SQL text.

`history()` selects the newest **four complete user/assistant pairs**, then
restores chronological order. Older pairs remain in SQLite but do not enter
the next model request. This explicit window is not unlimited memory.

```bash
uv run python storage_demo.py invalid
uv run python storage_demo.py inspect
```

**Predict/run/observe:** can a message refer to missing conversation 999999?
SQLite rejects it with `FOREIGN KEY constraint failed`. Inspect the explicit
`foreign_keys` pragma; SQLite does not enforce this by default. Existing rows
remain. Role/nonempty-content checks reject invalid rows too.

**Inspect/change/check:** `append_turn()` puts the user and assistant inserts
inside `db.atomic()`. Temporarily call it with an empty assistant answer in a
disposable experiment, or inspect `test_constraints_and_atomic_rollback`:
the user insert rolls back when the second insert fails. Explain why a
half-turn would damage later context. Restore the valid call afterwards.

Distinguish three jobs using the printed indexes:

- A primary key identifies a row.
- A foreign key refers to a parent and can enforce existence.
- An ordinary `(conversation_id, id)` index helps find/order matching rows; it costs storage and work on writes.

This index does not search semantic meaning. No benchmark is needed to explain
the distinction. Close Python and inspect again in a fresh process. Sketch
User/SaveFile ownership (one-to-many), User/Membership/Team (many-to-many through
a joining row), and Message replying to Message (self-reference). These are
transfer questions, not three additional app implementations.

## 50-60: break

Save your one-file experiment and leave the source/database available.

## 60-70: inspect the handbook before trusting an answer

The bundle contains **six short genuine extracts**, not the full handbook.
Source: Academic Registry's *Student Handbook for Taught Programmes 2026/27*,
July 2026; verified 29 October, 137 PDF pages. PDF positions 20, 25 and 76
correspond to printed pages 9, 14 and 61. The official URL, edition, PDF SHA-256,
section and chunk IDs accompany the text in [chunks.json](fixtures/chunks.json).

```bash
uv run python handbook.py
```

**Predict/run:** choose the relevant section for lost-card procedure, leave
request and card replacement cost. The three exact prepared questions use real
384D vectors generated by the pinned MiniLM encoder. Expect first results
`hb2026-p020-replacement`, `hb2026-p025-leave` and `hb2026-p076-fees` respectively.
The fee query's measured cosine scores are about 0.893 (fee row) and 0.737
(replacement rule). Inspect the printed numeric values and passage text.

**Check:** open the cited PDF sections and neighbouring text. The fee's HK$
heading is retained in section metadata. The leave table had ambiguous flattened
columns; the prepared bundle keeps unambiguous prose instead. Similarity is
approximate, not policy truth or a probability. An unrelated question still
has nearest neighbours. The six extracts cannot answer every handbook question.

**Change/recover:** try `uv run python handbook.py --query 'An unprepared question'`.
It rejects the missing prepared vector. Fixture mode only handles its exact
stored queries; it never substitutes keyword search. Arbitrary new questions
need the live matching encoder. A changed encoder/revision/pooling requires
rebuilding both document and query vectors; matching dimension alone is insufficient.

## 70-90: type, retrieve, inspect, speak

**Terminal 1:** the prepared model server must say it is listening on
`http://127.0.0.1:11440`; exact startup is in REHEARSAL.md. Leave it running.
**Terminal 2**, from `week10`:

```bash
uv run --extra encoder python bot.py
```

The extra installs the verified CPU encoder dependencies. Encoder weights are
loaded locally; missing assets fail rather than silently downloading. Input
above 256 encoder tokens is rejected, not silently truncated. No GPU is used.

Type these questions, one at a time:

```text
What should I do if I lose my student identity card?
If I find the original later, should I keep both?
```

**Predict/observe:** the first answer should direct an online replacement
application, cite the replacement rule and, when retrieved, the HK$150 fee row.
The follow-up should resolve “the original” to the identity card and explain
return/cancellation rather than keeping both. Actual model wording may vary;
compare claims against the returned passages, not the recorded wording alone.

The application requires retrieval on every turn. The **model composes the
query**, Python executes the retriever tool, then a second model call receives
its actual result. The model returns structured `answer` and `source_ids`.
The adapter formats bracketed citations; an empty source list becomes the
canonical `I cannot answer from these sources.` No script supplies policy
answers. This is a bounded RAG/tool workflow, with an explicit retrieval policy,
not an autonomous choice of arbitrary tools. JSON shape and allowed IDs do not
prove factual support; a valid ID can accompany a wrong claim.

Open `out/last-turn.json` after the second question. **Inspect:** the earlier
user/assistant pair must be present in the actual request, followed by the new
question, tool call, source result and final answer. A conversation number alone
is not memory. History helps resolve references; the handbook supplies policy
evidence. The trace is a temporary diagnostic snapshot, separate from SQLite.
Use `--trace out/my-check.json` to retain a particular fictional test.

**Hear/check:** after a validated atomic save, eSpeak NG synthesizes that answer
and `ffplay` plays it. Compare words with the visible answer. WAV creation,
player completion and a listener hearing intelligible speech are separate
checks. `Ctrl+C` during playback stops its player; an empty typed line exits.
A speech error prints `SPEECH FAILED`; the displayed/saved turn remains.

**Change/recover:** change the `history_turns` default in `agent.Bot` from four
to two. After enough turns, compare the selected next prompt with the full
SQLite history. Explain what was excluded, then restore four. Update the CLI's
printed policy too if you keep a different window in your own project.

## 90-100: reopen, isolate and recover

Exit, then run a fresh process with the ID your CLI printed:

```bash
uv run --extra encoder python bot.py --conversation 1
```

Replace `1` with your actual conversation ID. Ask the contextual follow-up.
Inspect the reloaded previous messages and the model-composed query. Then exit
and run a separate profile/conversation:

```bash
uv run --extra encoder python bot.py --user Bo
```

Ask `How do I request leave from class?` and inspect its prompt: Ada's earlier
turns must be absent. Using `--user Bo --conversation ADA_ID` must reject the
wrong owner. An unknown ID gives a recoverable error. Profiles demonstrate
application-level isolation; anybody who controls this local file can change it.

Choose a failure, predict the retained state, run it and recover:

- Ask `What is the Wi-Fi password at the campus cafeteria?` Expect a source-limited refusal; the nearest passage is insufficient.
- Run `uv run python bot.py --bundle out/missing.json`. Missing index: no answer/save/speech; return to the normal command.
- Stop terminal 1's model with Ctrl+C and retry. Connection failure: no new turn; restart the server before continuing.
- Run `uv run python speech.py --text ''`. Invalid speech text: a clear error; previous conversation history remains.

For separate speech testing, `uv run python speech.py --play` speaks a labelled
prepared check, not handbook policy. The prerecorded refusal WAV demonstrates
playback only; `recorded-answer.wav` records a real earlier cited answer.
`--text-only` is an explicitly labelled fallback that skips speech and therefore
cannot verify the spoken-output core. If the service cannot run, inspect the
recorded trace honestly and arrange a prepared-machine run.

## 100-120: tutor review and project support

Use the existing 12 November tutor allocation; exact times follow your assigned
slot. Partners explain the row, source, history and audio evidence in turn.
Show the integrated result, one failure/recovery and one next change. Use this
block to help unfinished setup/code, rather than adding appointments afterwards.

| Representation | Useful question | Limitation |
| --- | --- | --- |
| Related User/Conversation/Message rows | Whose messages, in what order? | Ownership/fields/constraints need a model |
| Nested scene/save document | What is the whole saved configuration? | References across documents need checks |
| Vectors plus source metadata | Which passages resemble this query? | Similarity does not establish truth |

JSON is a representation, not the absence of schema. Document stores can
validate schemas; relational systems can store nested data. SaveFile ownership
is a transfer sketch, not another required app. Optional extensions: alter the
history policy with tests, add carefully sourced chunks, reuse Week 6 microphone
input, or use a saved conversation for a game NPC. No AI feature is required.

Project policy stays **40%**, **25% idea / 50% code / 25% execution**, due
**6 December 2026, 23:59 HKT**. Use one public **sd5913-owned** team repository
with teammate Write access. GitHub Projects is recommended; an equivalent
accessible progress record is valid. Link useful evidence from the team README.
This adds no graded upload, compulsory defence or required technology. Canvas
is the submission system; no ClassPoint or instructor login is needed here.

## Sources and verified limits

Checked 29 October 2026: Python 3.12.15, uv 0.13.6, Peewee 4.5.3,
PyTorch 2.14.1+cpu, Transformers 5.19.0, Sentence Transformers 6.2.0,
llama.cpp build b11972 (`cf24317be`), eSpeak NG 1.52.0.1.
Linux x86_64 CPU storage, actual tool/answer/follow-up/reopen/isolation and player
completion/stop/failure were exercised. Physical speaker audibility and other
OSes need rehearsal. A small local model can still choose a poor query, omit
useful sources, refuse unnecessarily or produce an unsupported claim: inspect
the trace and source rather than treating the program as official advice.

- [Peewee models/SQLite](https://docs.peewee-orm.com/en/latest/peewee/models.html) and [4.5.3 release](https://github.com/coleifer/peewee/releases/tag/4.5.3).
- [MiniLM model and license](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/1110a243fdf4706b3f48f1d95db1a4f5529b4d41), Apache-2.0; [Sentence Transformers documentation](https://sbert.net/).
- [Qwen3.5-2B quantization](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF/tree/f6d5376be1edb4d416d56da11e5397a961aca8ae), Apache-2.0; [llama.cpp tools](https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md).
- [eSpeak NG integration](https://github.com/espeak-ng/espeak-ng/blob/master/docs/integration.md).
- [Official 2026/27 handbook](https://www.polyu.edu.hk/ar/docdrive/polyu-students/student-handbook/Student_Handbook_2026-27_English.pdf); attribution and exact provenance in fixtures.
- Historical [2025 Week 10](https://github.com/sd5913/pfad/tree/2025/week10): persistent models, vectors and retriever retained; unsafe login hashing not reused. Orange/t-SNE removed by explicit instructor decision.
