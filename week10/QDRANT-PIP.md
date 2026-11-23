# Give the existing talking bot a PDF-backed database

Use this route for the second half of the tutorial. Prepare it before class.
The first half in [README.md](README.md) remains relational: a `user` has many
`conversation` rows, a conversation has many `message` rows. SQLite saves
ordered history. Qdrant holds **shared PDF passages + vectors + provenance**.
A foreign key encodes a declared relationship; a nearest vector is an
approximate candidate, not a relationship, truth check or probability.

Recall the lecture's Semantle example: word embeddings make single words
numerically comparable. Here a text embedding represents an entire short
question or passage. The full-PDF route uses Qwen3-Embedding-0.6B to create
1024-number vectors. Its documented query instruction is applied to questions;
documents use the matching encoder without that instruction. Qdrant stores and
ranks them. We carry over the
similarity idea from Semantle, not its word vectors or model.

## Prepare and seed (tutor or prepared pair)

From **`pfad/week10`**, start Docker Desktop/Engine and run:

```bash
docker compose up -d qdrant
uv run --locked python download_handbook.py
uv run --locked --extra encoder --extra ingest python qdrant_add_pdf.py --download
uv run --locked python qdrant_index.py query --bundle out/handbook-full.json
```

The downloader refuses to overwrite an existing PDF. If the current handbook
is already in `out/`, skip that download command. The ingestion command converts
**all PDF pages** to Markdown, preserves chapter/section information and PDF
page numbers, splits with 1500-character chunks and 200-character overlap,
embeds them with the pinned Qwen model and uploads batches to Qdrant. It prints
the number of pages, chunks and stored points. Repeating it reuses a matching
complete bundle and upserts the same points. A changed PDF or chunk settings
requires another `--out` filename. See [FULL-PDF.md](FULL-PDF.md) for provenance,
the 2025 script adaptation and command-line use.

This pins Qdrant 1.20.0, binds HTTP only to this machine’s loopback port 6333,
and mounts a named `handbook-vectors` volume at `/qdrant/storage`. No Qdrant
Cloud account, API key or GPU is needed. Start this before class: image download
and Docker permissions can take time. No Docker? Pair with the prepared tutor
machine; `uv run python handbook.py` is a labelled in-process reference, not
proof of a Qdrant API call or server persistence.

The six selected passages and MiniLM's 384D vectors remain in
`fixtures/handbook.json` as an explicitly labelled teaching fixture. Select
**Six-passage teaching fixture** in Pip to use it, and seed it separately with
`uv run --locked python qdrant_index.py seed`. `prepare_index.py` rebuilds only
that fixture; `qdrant_add_pdf.py` is the full-document ingestion command.
No private reference deck is redistributed.

Seeding uses a collection named from a hash of the corpus/source/encoder.
Repeated seed updates the same UUID points; it doesn’t duplicate passages or
delete unrelated collections. Changed corpus or encoder means a new collection.
Queries against an unseeded collection fail visibly. Keep document and query
encoder identity equal, not merely dimensions.

## 60-70: inspect API and visual interface

**Predict:** which passage should rank first for a card-replacement fee query?
Run `query --bundle out/handbook-full.json`; the prepared questions must produce
the same chunk ordering as the in-process cosine reference. Inspect scores, page, text and
source URL. These are the same vectors, now queried across an HTTP boundary.

Open **http://127.0.0.1:6333/dashboard**. Select the printed `sd5913_...`
collection; inspect its 1024D Cosine configuration, full-document points and payloads.
A Qdrant point’s UUID is a database identity; payload `id` is our source-citation
identity. Point to the original text and PDF page before trusting an answer.
The visual interface and Python client use the same server/API.

```bash
curl http://127.0.0.1:6333/collections
```

Read `qdrant_index.py`: `PUT /collections/NAME` defines vector size/distance;
`PUT /collections/NAME/points?wait=true` stores vector/payload points;
`POST /collections/NAME/points/query` sends a query vector, `limit: 2` and
`with_payload: true`. These are real HTTP methods. Qdrant doesn't encode our
text: the matching Qwen encoder does that before the query. The returned
payload becomes the agent tool result. A `GET` listing alone doesn't prove
semantic retrieval.

**Change/check/recover:** `docker compose restart qdrant`, wait for readiness,
then run `query --bundle out/handbook-full.json` again **without seeding**.
The full set of saved points and rankings must
remain. `docker compose down` removes the container but keeps the named volume;
`up -d` recovers it. **Do not use `down -v`**: that removes the stored vectors.
For a changed source, prepare and seed a new content-addressed collection.
If Docker reports port 6333 busy, stop your own conflicting instance or have the
tutor assign a free host port. For example, if 6335 is free, change the mapping
in `compose.yml` to `127.0.0.1:6335:6333` and run `docker compose up -d` again.
Use `uv run python qdrant_index.py seed --bundle out/handbook-full.json --port 6335` and
`uv run python qdrant_index.py query --bundle out/handbook-full.json --port 6335`, open
`http://127.0.0.1:6335/dashboard`, and set Pip's **Qdrant port** to **6335**.
Keep the container port at 6333. Do not stop another group's work.

## 70-90: the familiar Pip, with retrieval and saved context

Keep the existing Week 6 LM Studio server and downloaded Kokoro assets.
The chat model must support OpenAI-style tools and JSON-schema output; a model
that handled simple Week 6 chat may not do both. Test the actual loaded model
before class; a tutor-prepared tool-capable local model is the fallback. A bad
reply fails visibly before saving a new turn. Don’t silently call a paid API.

Prepare a separate Week 10 environment from this folder:

```bash
uv run --extra encoder --extra pip python encoder.py --qwen --download
uv run --extra encoder --extra pip python -m streamlit run pip_app.py
```

The first command explicitly installs pinned dependencies and downloads the
encoder before class. The app loads encoder files locally. The `pip` extra
includes the same Streamlit/Kokoro libraries used in Week 6; it avoids manually
installed packages being removed by `uv run`. Follow Week 6’s `CONVERSATION.md`
and `prepare_models.py` for existing Kokoro model/voice assets in Week 6’s
output directory. No second speech model is introduced. Use CPU unless your
Week 6 machine already has a rehearsed GPU setup.

Choose the exact loaded model ID and the same local URL as Week 6 (normally
`http://127.0.0.1:1234/v1`). Keep **Qdrant port** at **6333** unless the tutor
assigned a different host port; it must match the seed/query commands. In Pip type:

1. `What should I do if I lose my student identity card?`
2. `If I find the original later, should I keep both?`

**Observe/inspect:** the visible answer cites returned chunk IDs. Expand the
trace: prior turns → model-composed tool query → Qdrant passages → answer →
atomic SQL save. Listen to Kokoro and compare it with the displayed text.
Browser autoplay may need a click. An audio widget or successful synthesis is
not evidence that the room can hear it. Speech failure preserves the saved turn.

The inherited Week 10 agent still requires retrieval every turn. Pip’s local
HTTP transport replaces the separate server transport; its Kokoro voice replaces
eSpeak. The first model call requests the retriever; Python executes it; the
second call receives the passages and generates a structured answer. Membership
of a cited ID is checked, but a human must still check factual support.
The four-pair history window matches Week 6’s last eight messages. Source
passages are untrusted data, not instructions. Read `pip_adapter.py`, `agent.py`
and `pip_app.py`; no library framework hides this boundary.

## 90-100: reopen, isolate, fail and recover

Record the printed conversation ID. Stop/restart Streamlit, select the same
fictional profile and that ID. Ask the follow-up and inspect the reloaded
history. Use a second profile and ID 0 for a new conversation; Ada’s history
must be absent. Trying Ada’s ID under another profile must reject access.
These are local ownership demonstrations, not authentication.

Try an unsupported cafeteria Wi-Fi question: nearest neighbours still exist,
but the expected answer is a source-limited refusal. Inspect the actual reply;
a local model can still get this wrong. Stop Qdrant and ask again: the new turn
must fail without being saved. Restart it and retry; don’t reseed automatically.
Disable the speech checkbox only as a clearly labelled text-only fallback.
Keep `out/pip.sqlite` for history; keep the Docker volume for knowledge. The
trace `out/pip-last-turn.json` is temporary diagnostic data, not either database.
Use fictional questions only.

The existing CLI also accepts `uv run --extra encoder python bot.py --qdrant`
with its original prepared llama.cpp/eSpeak setup. It is an alternate route,
not another required installation. Recorded old CLI evidence proves that older
route only; it does not prove a fresh LM Studio/Kokoro or Docker run.

Then stop experiments at minute 100 and keep **100-120 for tutor/project
support**, with the same project rubric, deadline and submission policy.

Official references checked 11 November 2026:
[local service and dashboard](https://qdrant.tech/documentation/quickstart/),
[point query API](https://api.qdrant.tech/api-reference/search/query-points),
[Qdrant Web UI](https://qdrant.tech/documentation/web-ui/).
