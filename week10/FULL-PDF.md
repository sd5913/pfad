# Embed the entire handbook into Qdrant

`qdrant_add_pdf.py` indexes the complete PDF using **Qwen3-Embedding-0.6B**,
the model family used by the 2025 example. Pip defaults to this full-document
index. The six hand-selected MiniLM passages remain a separate teaching fixture.

## Run

From `pfad/week10`, prepare the public handbook if it is not already downloaded:

```bash
uv run --locked python download_handbook.py
```

Then start Qdrant and run full ingestion:

```bash
docker compose up -d qdrant
uv run --locked --extra encoder --extra ingest python qdrant_add_pdf.py --download
```

The script extracts every PDF page as Markdown with PyMuPDF4LLM, converts the
original bold section headings, and uses LangChain's Markdown splitters with
1500-character chunks and 200-character overlap. Each chunk retains its PDF
page, section, source file, source URL and PDF SHA-256. Short passages are
retained. Extraction and chunking check page coverage before publishing a bundle.
Empty pages are reported explicitly. Scanned PDFs need OCR; this text-PDF route
does not turn diagrams or pictures into text.

The pinned Qwen encoder produces normalized 1024-dimensional embeddings.
Questions use its published retrieval instruction; document chunks have no
query instruction. Both ingestion and Pip load the same revision, pooling,
normalization and float32 configuration. Model downloads happen only during
explicit preparation, never during a conversation.

The complete local bundle is `out/handbook-full.json`. Qdrant receives batches
of 64 points in a separate content-addressed collection. The script verifies
the stored point count and prints the collection name. An interrupted upload
can be retried with the same command; it reuses the completed local embeddings.
Repeat runs upsert the same point IDs. A changed PDF, encoder or chunk settings
requires another `--out` path and produces another collection.

Inspect prepared full-document queries and the dashboard:

```bash
uv run --locked python qdrant_index.py query --bundle out/handbook-full.json
```

Open <http://127.0.0.1:6333/dashboard/> and select the printed collection.

## Use in Pip or the CLI

Keep your tool-capable local chat server running, then:

```bash
uv run --locked --extra encoder --extra pip python -m streamlit run pip_app.py \
  --server.address 127.0.0.1
```

Leave **Handbook** set to **Full PDF**. Use your exact local chat-model ID and
URL. The embedding model is separate from the chat model. On the prepared
laptop, the chat URL is `http://127.0.0.1:11440/v1` and model ID is
`handbook-local`. Kokoro and conversation persistence work as before.

The existing CLI accepts the same full-document bundle:

```bash
uv run --locked --extra encoder python bot.py --qdrant --bundle out/handbook-full.json
```

Prepare eSpeak/FFmpeg for spoken CLI replies as described in `REHEARSAL.md`.
Pip uses the existing Week 6 Kokoro assets. Inspect retrieved pages and claims;
embedding the whole document does not guarantee that every answer is supported.

## Reused 2025 source and compatibility

Source: `week10/handbook_app/qdrant_add_pdf.py` and `qdrant_store.py` on
`origin/2025`, observed revision
`512edb07927c5d77cacc7279ba6be601b33dc601` on 12 November 2026.
The original extracts the whole PDF, preprocesses Markdown section headings,
splits by chapter/section and uses 1500/200 size-based splitting. Those parts
are adapted directly here. The 2026 extraction additionally retains page
provenance and does not discard passages merely because they are short.

The original embedding transport expected `qwen3-embedding:0.6b` from an
Ollama-compatible service on port 11434. This laptop has no Ollama installation
or service. The installed Sentence Transformers runtime can run the same Qwen
model family directly, so the adaptation uses its official full-precision
weights instead of introducing another model server. These vectors are not
claimed to be byte-identical to embeddings from a quantized Ollama model.

Pinned model: `Qwen/Qwen3-Embedding-0.6B`, Apache-2.0, revision
`97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3` (upstream HEAD observed on
12 November 2026). The older MiniLM pin and six-point fixture remain available
for the original small teaching checks. PyMuPDF4LLM/PyMuPDF and the Markdown
splitters retain their upstream licenses and notices in their distributions.

## Checks

```bash
uv run --locked --extra encoder --extra pip --extra ingest python -m unittest discover -p 'test_*.py'
```

Coverage checks include real PDF extraction, first/middle/last page inclusion,
retention of short passages, long-section tails, deterministic IDs and batched
HTTP uploads. Unit tests check behavior; a full-document ingestion and live
Pip run are required to establish actual model, Qdrant and speech operation.
