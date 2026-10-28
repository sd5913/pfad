# Preparing and checking the core

This is the unfinished production acceptance route, not instructions to spend
the student tutorial downloading models. Run from `week10` on a permitted
networked preparation machine. It makes no paid API calls and opens no accounts.

## Source and vectors

```bash
uv run python download_handbook.py
```

Inspect the actual PDF title/year and relevant sections. Record the returned
SHA-256 and actual date. Choose two useful policy sections and one unsupported
question. PDF page numbers mean positions starting at one, not printed labels.
The download helper validates a PDF signature/size; that does not prove its
title or content is the expected edition.

Use an already prepared matching encoder snapshot, or explicitly prepare its
public model download ahead of class. No download is automatic. The encoder
extra selects CPU PyTorch on Linux/Windows; clean installation and package size
still need verification. The original feasibility probe used cached CUDA-build
PyTorch **on CPU**; that is not proof this CPU-package installation succeeds.

```bash
uv run --extra encoder python prepare_index.py \
  --pdf out/Student_Handbook_2026-27_English.pdf \
  --encoder-path /path/to/prepared/snapshot \
  --pages 8,9 --retrieved-on YYYY-MM-DD \
  --query 'First short source-supported question' \
  --query 'Second short source-supported question'
uv run python handbook.py
```

**Replace the example pages/date/questions after inspecting the PDF.** They are
syntax placeholders, not claims about its sections. This writes real vectors
and exact source metadata to `fixtures/handbook.json`, refusing overwrite.
Review each extract, both rankings, IDs, same-space identity and source support.
Keep only the small attributed extract; do not commit the downloaded whole PDF.

## Live model and memory

Prepare and verify a local tool-capable Ollama model without new paid access.
The present `qwen3:4b` default is a candidate; record the actual version/digest,
download size, hardware, cold startup and response time when verified.

```bash
uv run --extra encoder python bot.py --encoder-path /path/to/prepared/snapshot
```

Retain a fictional, redacted acceptance trace covering a supported question,
unsupported question, contextual follow-up, fresh-process reopening, isolated
second conversation and wrong-owner rejection. Inspect actual serialized
history/tool results reaching subsequent model calls. Review claims against
sources, not just citation-ID membership. Do not call protocol doubles live.

## Speech and stop

```bash
uv run python speech.py --play
```

Check live WAV synthesis, hear the exact text, interrupt playback and verify the
player exits. Repeat through an actual cited bot answer. A device error must
preserve visible answer/history and report speech failure. Prepared refusal
audio is a separate prerecorded fallback; it cannot satisfy these live checks.

Finally run the full README route on a clean student machine, time pairing at
minute10, and record precise versions/commands/results. Only after these core
gates pass should the long lecture replacement be produced and rendered.
