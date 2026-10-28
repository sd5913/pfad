# Week 10: persistent objects and a talking handbook agent

**Thursday 12 November 2026. Lecture: 120 minutes; this tutorial: a separate
120 minutes.** Build on Week 7's objects and Week 8's inspected, tested programs.
The new question is what happens when an object must survive a restart and
supply context to a later model call.

> **Production status, 29 October: incomplete core.** The real SQLite/ORM path,
> bounded tool dispatcher, memory plumbing and local speech synthesis have been
> checked. Current handbook extraction/index fixtures, a live model's grounded
> answers and contextual follow-up, and audible playback/stop have not yet passed
> integrated verification. The approved tutorial route is specified here, but
> its second half is **not classroom-ready**. See [bundle status](fixtures/README.md).
> The old artwork JSON example remains supplementary; it does not replace this core.

By the end, explain and inspect:

- `User -> Conversation -> Message`: a Python model, one instance, its row and its stable ID.
- Exact, owner-scoped queries, constraints, ordinary indexes and a fresh-process reload.
- A real handbook chunk, its learned vector, a query in the same space and a cited result.
- A real retriever tool call, the history sent to the next model call, and an isolated second conversation.
- A displayed answer, its source support, synthesis, playback and failure as separate checks.

## Prepare before the session

Clone the current PFAD companion and open a terminal in **`pfad/week10`**:

```bash
cd week10
uv run python storage_demo.py seed
uv run python storage_demo.py inspect
```

Python 3.12 or newer and `uv` are prerequisites. This week has its own
`pyproject.toml`; commands from this directory use Peewee **4.5.3**, the latest
upstream release checked on 29 October. First use needs internet to install the
small Peewee package; no database server, account, Docker or GPU is required for
storage. Linux storage/protocol checks passed on Python 3.14; Python 3.12 was
used for the cached encoder probe. Windows/macOS execution is not yet verified.
Package installation from an empty uv cache is still blocked in production by
network restrictions; no clean-install claim or fabricated lockfile is supplied.

The instructor must prepare the **actual 2026-27 handbook extract/index** and
verify its page references before students start. Full PDF ingestion is an
instructor preparation job, not a tutorial exercise. Students inspect the small
bundle and two prepared real query vectors without downloading a model.
Arbitrary live typed questions require the exact matching encoder, a locally
installed tool-capable model, and a prepared local Ollama service. The proposed
chat model default is `qwen3:4b`; it is **not yet empirically verified here**.
Model downloads and hardware requirements must be timed on a prepared machine
before declaring this route ready. The CLI does not download models or contact
paid endpoints. A generic subscription to a coding assistant does not establish
this local application endpoint.

Speech uses the open-source eSpeak NG shared library and English voice data,
plus FFmpeg's `ffplay` for playback. Install these through the normal platform
package manager before class. The core voice is intentionally simple and local.
A synthesized WAV has been verified; system playback was denied in production.
For a different library location, `ESPEAK_LIBRARY` and `ESPEAK_DATA_PATH` can name
an existing installation. No Steam installation is a student prerequisite.

If setup fails at minute 10, pair with a prepared machine and alternate the
keyboard. Copy only fictional `out/` data if you need to inspect its records.
If no prepared machine has the source/index/model/speech path, the tutor must
record the incomplete core and use the inspection fallbacks explicitly. Paper
and replay can support reasoning but cannot establish live retrieval or memory.

## The complete 120-minute route

| Minutes | Work and evidence |
| --- | --- |
| 0-10 | Setup; first storage run; verify prepared handbook/index/model status |
| 10-30 | Create/load User, Conversation and Message; map methods to SQL and rows |
| 30-50 | Query history, distinguish keys/indexes, update/restart, reject a broken relation |
| 50-60 | Break |
| 60-70 | Inspect real handbook vectors, two query rankings and cited retriever results |
| 70-90 | Typed question and follow-up; inspect actual model context; hear the reply |
| 90-100 | Reopen/isolate conversations; trigger one retrieval or speech failure |
| 100-120 | Integrated-core-experience tutor review and group-project support |

## 0-10: get the first visible result

Run the setup commands. Expect `user=1 conversation=1` on a new database and two
message rows. The assistant seed explicitly says **prepared storage example;
no model was called**. Inspect `out/chat.sqlite` through the printed SQL and
rows. Do not type real passwords or student information. Running `seed` again
while the original title exists reuses that seed; after renaming, a new
Handbook conversation can be created. IDs need not always be 1 in a reused file.
Use `--db out/experiment.sqlite` to start a separate disposable experiment.

Run the behavior checks:

```bash
uv run python -m unittest discover -p 'test_*.py'
```

Protocol tests use explicit scripted model replies and synthetic coordinates
inside unit tests. They prove dispatch/validation, not model understanding or
real handbook embeddings. A green suite does not close the live-core gap.

## 10-30: trace a model through a real row

**Predict:** does `Conversation.create(...)` save its methods, or its field
values? Does changing a Python attribute alone change the stored row?

Read [models.py](models.py). `Record` inherits Peewee's `Model`; `User`,
`Conversation` and `Message` inherit persistence/query methods. The database
adds the primary-key `id`. Each conversation stores its owner's ID, and each
message stores its conversation's ID. A foreign key is a stored reference,
not a copied parent object.

```bash
uv run python storage_demo.py inspect
uv run python storage_demo.py rename
uv run python storage_demo.py inspect
```

**Observe:** `rename` changes a loaded object's `title` then calls `.save()`.
A new `inspect` process sees `My game questions`, with the same conversation ID.
Methods stay in `models.py`; SQLite stores stable values and references.
Read the `SELECT ... WHERE conversation_id = ? ORDER BY id` trace and its
parameter list. The parameter binds a value; it is not pasted into SQL text.

**Change:** edit only `chat.title = 'My game questions'` in
[storage_demo.py](storage_demo.py), predict the next inspection, then run it.
**Check:** the title changes; owner and IDs remain. **Recover:** restore that
one string; do not delete a database that contains work you need.

## 30-50: relationships, exact lookup and recovery

Open `Store.history_query()` and trace the ownership check before the message
query. `history()` returns the most recent **four complete user/assistant pairs**
in chronological order. All older pairs remain in SQLite, but are not sent in
the next model call. This is an explicit context-window policy, not unlimited
memory. Local fictional usernames demonstrate ownership checks; this is not an
authenticated multi-user service.

```bash
uv run python storage_demo.py invalid
uv run python storage_demo.py inspect
```

**Predict:** can a message reference conversation 999999? **Observe:** SQLite
rejects it with `FOREIGN KEY constraint failed`; the existing rows remain.
Inspect the connection's `foreign_keys` pragma and the `role`/nonempty-content
checks in the models. `append_turn()` puts the user and assistant rows in one
transaction: if the second insert fails, the first rolls back too. Do not claim
a failed answer was successfully saved. No password/login implementation is needed.

**Check the three different jobs:** a primary key identifies a row; a foreign
key refers to another row and can enforce existence; an ordinary index makes
matching-row lookup cheaper. Inspect the index names printed by `inspect`.
The `(conversation_id, id)` index supports finding and ordering one history.
Indexes cost storage and work on each write; they are not semantic vectors.
No benchmark is required to explain the distinction.

Close the terminal and reopen it in `pfad/week10`. Run `inspect` again. Explain
why stable IDs survive while the previous Python objects do not. Then make a
short relationship sketch: User/SaveFile is one-to-many; User/Membership/Team
uses a junction record; Message replying to Message is a self-reference. These
are transfer questions, not three extra apps to implement.

## 50-60: break

Leave the source files and database available. Save your one-file edit.

## 60-70: inspect the handbook before trusting an answer

**Blocked until the real bundle is supplied and reviewed.** With that bundle:

```bash
uv run python handbook.py
```

Read the printed official URL, year, PDF SHA-256, one-based PDF page, chunk ID,
encoder/weight identity, dimension and first eight numeric values. Each vector
is a learned representation of that exact short passage. It is not a row ID,
a policy, a truth score or the full PDF. The supplied two queries have actual
vectors from the same encoder and pooling rule.

**Predict:** which source passage should support each query? **Run** the two
prepared queries. **Check:** compare both ranked results with the cited PDF
sections, including neighbouring text that a short chunk may omit. A larger
cosine score means closer directions, not greater policy correctness. A query
about an unrelated subject still has a nearest neighbour.

`handbook.py --query '...'` accepts only an exact prepared question in fixture
mode; it cannot silently invent a new vector. A new question requires the same
live encoder. Changing encoder/weights/tokenization requires rebuilding both
stored chunks and queries. A dimension match alone is insufficient.

## 70-90: type, retrieve, answer, speak

**The live route is implemented but not yet verified end to end.** On the
prepared machine, use its matching cached encoder path; this path is the one
instructor-supplied argument, not a model download command:

```bash
uv run --extra encoder python bot.py --encoder-path /path/to/prepared/snapshot
```

The `--extra encoder` flag supplies the live CLIP dependencies; prepared-vector
inspection needs no extra. For an Ollama-embedded bundle, omit `--encoder-path`; its model name/digest must
match the installed encoder. `bot.py` defaults to local port 11434, a fresh
conversation and four retained turns. The CLI prints the actual conversation
ID to reuse. Type a short source-supported question chosen from the real
bundle; then ask a follow-up referring to it. Keep within CLIP's short-text
limit when this encoder is used; overly long input fails visibly, never silently
truncates. Type an empty line to end the typed loop.

**Observe:** the model chooses `retrieve_handbook`, supplies a query, receives
source IDs/text/pages, and then answers. Inspect `TOOL TRACE` and
`out/last-turn.json`: the second call must contain the first user and assistant
messages, plus actual tool results. The `thread` label is not the proof; the
serialized messages reaching the model are. The trace contains the ephemeral
prompt snapshot for this exercise; it is overwritten by the next successful
turn and is separate from persistent history. Use fictional conversation only.

**Check:** does the follow-up resolve its reference using the previous turn?
Is each factual claim supported by its cited source? The program rejects
unknown citation IDs, but a valid ID can still accompany a wrong claim. Inspect
the source text yourself. Ask something outside the source scope. Expected:
`I cannot answer from these sources.` A scripted unit-test refusal is not live
model evidence; the actual model must be checked on both cases.

The displayed answer is saved atomically before synthesis. Hear the same answer;
compare words/citations with the text. If speech fails, it prints `SPEECH FAILED`
and retains the text/history. `Ctrl+C` during playback stops its player; an
empty typed line ends the session. WAV generation, player completion and a
listener hearing intelligible output are three separate observations.

**Change:** set the `history_turns` default in `agent.Bot` from four to two.
After enough turns, inspect the selected prompt and explain what disappeared
from the next call versus what remains in SQLite. **Recover:** restore four.
The CLI's printed policy must be updated if you keep this as a project change.

## 90-100: restart, isolation and one failure

Close the program and run a fresh process using the printed ID:

```bash
uv run --extra encoder python bot.py --encoder-path /path/to/prepared/snapshot --conversation 1
```

Replace `1` with your actual ID. Ask a follow-up. Inspect the loaded history and
the next request, then start a new conversation by omitting `--conversation`.
Ask the same vague follow-up. It must not receive the other conversation's
messages. Using `--user Bo --conversation 1` for Ada's conversation must fail
ownership checking. This is application-level separation, not secure login.

Choose one failure:

- Run `uv run python bot.py --bundle out/missing.json`: a clear missing-index error; no answer, saved turn or speech claimed.
- Stop the prepared local model server and retry: connection failure; no turn saved. Restart it before continuing.
- Run `uv run python speech.py --text ''`: a visible speech error; existing history remains unchanged.

For speech-only verification:

```bash
uv run python speech.py --play
```

This says **prepared speech check**, not handbook policy. The supplied
[prepared-refusal.wav](fixtures/prepared-refusal.wav) is prerecorded synthesized
fallback audio: 1.777 seconds, 22050 Hz, mono PCM. Its text is `I cannot answer
from these sources.` Playing it demonstrates playback only, not live synthesis,
retrieval, agent memory or a source-supported answer. `--text-only` is an
explicitly labeled bot fallback that skips speech; it cannot pass the spoken core.

## 100-120: tutor review and project support

Use the existing 12 November tutor allocation; the tutor confirms exact meeting
times. Show your integrated core experience, one current risk and one next
change. Partners explain the row, source, history and audio evidence in turn.
A missing live component is a known gap to resolve, not a reason to invent a demo.
Support unfinished setup or code within this twenty-minute block.

Compare storage by the question you ask:

| Representation | Useful question | Limit |
| --- | --- | --- |
| Related User/Conversation/Message rows | Which messages belong to this user's conversation, in order? | Exact fields/relations must be modelled |
| Nested save/config document | What is this scene's whole saved configuration? | Cross-document references need a design/check |
| Handbook vectors plus metadata | Which passages resemble this question semantically? | Similarity does not establish truth or permission |

JSON is a representation, not the opposite of a schema. Document databases may
validate schemas; relational systems can also store nested data. No extra
NoSQL service is required. SaveFile ownership remains a transfer sketch.

These techniques are optional project inspiration. The project remains **40%**,
with **25% idea / 50% code / 25% execution**, due **6 December 2026, 23:59 HKT**.
Use a public **sd5913-owned** team repository with teammate Write access.
GitHub Projects is recommended; an equivalent accessible shared progress record
is valid. Link useful evidence from your team's README. This adds no graded
upload, compulsory defence, AI feature or required technology. Canvas remains
the submission system; this tutorial needs no ClassPoint or instructor login.

## Sources, versions and honest limits

- [Peewee 4.5.3 release, 7 October 2026](https://github.com/coleifer/peewee/releases/tag/4.5.3): checked 29 October; genuine upstream source, commit `e245a01b1f57005e7ae315736da8e6a70e65afba`, used for local tests.
- [Peewee models](https://docs.peewee-orm.com/en/latest/peewee/models.html) and [SQLite pragmas](https://docs.peewee-orm.com/en/latest/peewee/sqlite.html): Context7 checked 29 October.
- [Ollama tool calls](https://docs.ollama.com/capabilities/tool-calling) and [embeddings](https://docs.ollama.com/capabilities/embeddings): current protocol checked through Context7; local endpoint unavailable, default model not verified.
- [Transformers 5.19.0](https://huggingface.co/docs/transformers/v5.19.0/en/model_doc/clip): cached CLIPTextModel CPU probe with PyTorch 2.14.1+cu132 produced 768D vectors. This is not evidence of handbook retrieval until real extracted passages are indexed.
- [Stable Diffusion v1.5 source snapshot](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/tree/451f4fe16113bff5a5d2269ed5ad43b0592e9a14): existing learned text encoder; model license/provenance belongs with preparation. We do not redistribute weights or generate images.
- [eSpeak NG integration](https://github.com/espeak-ng/espeak-ng/blob/master/docs/integration.md): real local eSpeak NG 1.52.0.1 synthesis passed; playback/audibility/stop still require a real machine check.
- [Official current handbook](https://www.polyu.edu.hk/ar/docdrive/polyu-students/student-handbook/Student_Handbook_2026-27_English.pdf): instructor-supplied URL; retrieval/title/pages not yet independently verified.
- Historical [2025 Week 10 examples](https://github.com/sd5913/pfad/tree/2025/week10): ORM classes, retrieval tool and vectors retained; unsafe login hashing is not reused. Orange/t-SNE is removed by instructor decision, not a missing prerequisite.

Storage, protocol and original supplementary artwork tests pass locally.
Scripted model doubles check dispatch/history/citation validation and failure
paths only. Missing current PDF bundle, verified live model reasoning, a clean
student environment and actual heard/stopped speech remain release blockers.
