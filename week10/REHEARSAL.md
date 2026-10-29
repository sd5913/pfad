# Prepare and rehearse the local CPU route

Run from `week10`. Prepare this before class; the tutorial pairs with a ready
machine at minute 10. Downloads below are public files, not paid inference.
The bot itself never downloads weights or connects to a paid endpoint.

## Dependencies and source

```bash
uv sync --extra encoder
uv run python download_handbook.py
uv run --extra encoder python encoder.py --download
```

The clean Linux x86_64 CPU environment was installed from an empty uv cache in
12.05 seconds on 29 October. This is a connection-specific observation, not a
promise. Python 3.12.15, uv 0.13.6, Peewee 4.5.3, Torch 2.14.1+cpu,
Transformers 5.19.0, Sentence Transformers 6.2.0. The encoder's pinned public
revision is loaded locally in subsequent runs. About 90 MB of encoder files
are cached in ignored `out/models/`; the complete installed environment used
about 1.2 GB, plus a similarly sized package cache.

The official PDF is 7,658,316 bytes, 137 pages. Its SHA-256 is
`108956feb2ffac665f8ca0f5a8f68d7150a85fda15e219916785ec50331a4e94`.
Title: *Student Handbook for Taught Programmes 2026/27*, Academic Registry,
July 2026; PDF metadata modified 29 July. Retrieved/inspected 29 October 2026.
The downloader validates signature/size and prints its hash; human inspection
establishes title/year/page meaning. Rebuild into a separate file:

```bash
uv run --extra encoder python prepare_index.py --out out/rebuilt-handbook.json
uv run python handbook.py
```

`prepare_index.py` verifies every supplied extract against the actual cited
PDF page, then generates six passage and three query vectors with the same
pinned encoder. It refuses an existing output. Compare the rebuilt bundle with
`fixtures/handbook.json`; do not silently overwrite the reviewed fixture.
Full PDF ingestion is not a class activity.

## Chat model and local server

The tested public model is [Unsloth's Qwen3.5-2B Q4_K_M GGUF](https://huggingface.co/unsloth/Qwen3.5-2B-GGUF/resolve/f6d5376be1edb4d416d56da11e5397a961aca8ae/Qwen3.5-2B-Q4_K_M.gguf),
revision `f6d5376be1edb4d416d56da11e5397a961aca8ae`, Apache-2.0.
Download it to `out/Qwen3.5-2B-Q4_K_M.gguf` ahead of time: 1,280,835,840 bytes,
SHA-256 `aaf42c8b7c3cab2bf3d69c355048d4a0ee9973d48f16c731c0520ee914699223`.
A fresh download and hash check took **46.50 seconds** on the preparation
connection; slower networks need substantially longer.

Use the verified [llama.cpp b11972 CPU release](https://github.com/ggml-org/llama.cpp/releases/tag/b11972),
built from `cf24317be`, published 28 October 2026. The Linux x86_64 archive is
[llama-b11972-bin-ubuntu-x64.tar.gz](https://github.com/ggml-org/llama.cpp/releases/download/b11972/llama-b11972-bin-ubuntu-x64.tar.gz),
22,692,140 bytes, SHA-256
`24519b79152045d6b8b8844ee44ffd96e59a0e1d52a023aa28a1ddc55a3c30e6`.
Extract its directory into `out/llama/`. Keep the adjacent shared libraries with
the executable. Other OS/architecture assets are on that release; their startup
and audio have not been verified here. The release's `v0.8.0` tag is a tracking
release; the concrete tested binary is build b11972, not an invented stable binary.

**Terminal 1**, from `week10`:

```bash
out/llama/llama-b11972/llama-server \
  -m out/Qwen3.5-2B-Q4_K_M.gguf \
  --host 127.0.0.1 --port 11440 --alias handbook-local \
  -ngl 0 -t 6 -c 8192 --jinja --reasoning off
```

Wait for `listening on http://127.0.0.1:11440`. Keep this terminal open.
`-ngl 0` means CPU, six threads; no dedicated GPU was used. The tested laptop is
AMD Ryzen 9 5900HS (8 cores/16 threads), approximately 40 GB RAM. Server startup
reached listening after 2.26 seconds from the prepared files. This measures
that hardware/cache condition, not a low-memory laptop guarantee. Allow about
3 GB for the model, runtime and Python environment plus download caches.

**Terminal 2**:

```bash
uv run --extra encoder python bot.py
```

The application requires a native retrieval tool call; the model composes the
query. After Python executes retrieval, the answer phase uses a JSON schema
with `answer` and `source_ids`. Empty IDs mean refusal. The app formats citations
from the model-generated IDs and validates membership before saving. This is a
bounded retrieval workflow, not an autonomous decision to use arbitrary tools.
Schema validity is not factual correctness. Inspect the raw `structured_answer`
in the trace and compare every claim to the returned passages.

Measured complete CLI runs (encoder/model startup included): supported answer
38.67 seconds including 18.76 seconds of audio, reopened follow-up 18.80 seconds,
unsupported question 17.18 seconds, isolated leave question 18.76 seconds.
These are teaching-laptop observations, not model-only benchmarks.

The small model initially omitted natural-language citations and sometimes
ignored a requested tool. Those runs were rejected without saving. The final
route explicitly requires retrieval and uses structured source selection;
it does not paste a prepared policy answer into model output. A boolean support
field was also removed after it confused a negative answer with missing
support. These observations explain the final interface choice.

## Actual acceptance route

Use fictional data and retain each result with `--trace out/check-name.json`.
Default SQLite file is `out/chat.sqlite`; use a fresh `--db` name to avoid the
prepared storage seed. Record the actual printed conversation ID, not a guessed
number.

1. Ask `What should I do if I lose my student identity card?` Inspect the real tool query, replacement/fee sources, answer and spoken reply.
2. Exit; start a fresh process with `--conversation ID` and the same `--db`. Ask `If I find the original later, should I keep both?` Check the retained pair actually reaches the model and resolves the reference.
3. Ask `What is the Wi-Fi password at the campus cafeteria?` Check the source-limited refusal rather than trusting its nearest neighbour.
4. Start `--user Bo` without a conversation ID and ask about leave. Inspect that Ada's messages are absent; then try Bo with Ada's ID and expect ownership rejection.
5. Stop terminal 1 with Ctrl+C, retry and inspect unchanged message count. Restart it and recover. Ending the bot does not stop the model server; stop both when finished.

The labelled public `fixtures/recorded-run.json` retains actual model answers,
retrieval queries, source IDs and selected prior history from a real CPU run.
It is an inspection fallback, never presented as a fresh live invocation.
The associated `recorded-answer.wav` was synthesized from that actual answer.

## Speech, device failure and stop

Install the normal eSpeak NG shared library/English data and FFmpeg for your OS.
Linux package names are usually `espeak-ng` and `ffmpeg`. No Steam installation
is required. The preparation host's existing library was loaded using explicit
`ESPEAK_LIBRARY` and `ESPEAK_DATA_PATH`; students should normally use the system
installation. Do not copy private environment configuration.

```bash
uv run python speech.py --play
uv run python speech.py --text ''
```

First: live synthesis and player completion; second: expected invalid-text
error. Stop a longer live reply with Ctrl+C and verify `stopped` and no remaining
player. Linux can deliberately select an invalid audio driver for a separate
failure check:

```bash
SDL_AUDIODRIVER=invalid uv run python speech.py --play
```

Expected playback failure. Test the same condition through `bot.py`: it must
print `SPEECH FAILED` after displaying/saving the answer; source/history are
retained. Restore the environment by omitting that assignment. A generated WAV
or player completion is not evidence that room speakers were intelligible:
a physical listener must verify audibility, volume and stop before class.

The prerecorded refusal and recorded cited answer are separate audio fallbacks.
`--text-only` explicitly skips speech. Neither fallback proves live spoken output.
