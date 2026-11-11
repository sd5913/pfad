# Week 10 revision checks — 11 November 2026

This revision keeps relational models/SQL/persistence as the first half and adds
D1, a real Qdrant HTTP store and a route reusing Week 6 Pip/Kokoro. Both draft
PRs integrate their current base histories, including merged Week 9. Historical
private PDF and PPTX references were each materialized/inspected (67 slides);
neither is included in the repositories.

## Checked in this revision

- 23 isolated Week 10 tests pass, including real-loopback HTTP protocol tests
  through the Week 6 client, actual saved history, source results entering the
  next call, failure before save, encoder mismatch and relational schema checks.
  The protocol tests use a labelled model double, not inference evidence.
- Qdrant **1.20.0** native Linux service: all three real learned-vector fixture
  rankings/near-equal scores match the in-process cosine reference. Repeated
  seed retains six points. Stop/restart without reseeding retains points and
  rankings. Docker itself is unavailable here, so Compose startup/volume mounting
  still needs a prepared-machine check. The committed Compose file pins the same
  server version and named persistent volume with loopback HTTP.
- **Live CPU inference** using the documented Qwen3.5-2B GGUF (checked hash) and
  llama.cpp b11972 as an OpenAI-compatible local server: Pip's existing
  `local_reply.call` transport → bounded retrieval tool → real Qdrant query →
  cited answer → related SQLite save. Lost-card answer gave online application,
  HK$150 and return/cancellation, with replacement/fee source IDs. Follow-up
  explicitly rejected keeping both cards, citing the returned replacement rule.
  Unsupported cafeteria Wi-Fi question produced the source-limited refusal.
- Actual prior pair entered the follow-up prompt. Closing/reopening the SQLite
  store retained six messages; a second profile had empty history; wrong-owner
  access failed. Stopping Qdrant made a new question fail without adding rows.
- Week 6's actual `synthesise_onnx.synthesise_reply` generated the supported
  answer as a 999,468-byte WAV, **20.82 seconds**. This checks Kokoro synthesis,
  not browser autoplay, speaker audibility or a room listening test.
- Locked encoder/Pip dependencies install. Real Streamlit AppTest initial render
  has no exceptions and exposes the model URL/model ID/profile controls. The
  exact LM Studio application and a browser/audio device are unavailable here:
  the live inference check uses its compatible API protocol, not an asserted
  LM Studio GUI run. Rehearse the exact loaded model's tool/schema support.
- D1 pinned Wrangler **4.160.0**, workers-py **1.17.4** and runtime SDK **1.9.0**:
  local schema/seed succeeds (nine SQL commands). The normal GitHub runner also
  passes the **actual Python Worker HTTP/restart check**: bound JOIN, invalid
  input, empty result and changed title surviving restart, in
  [practical checks](https://github.com/sd5913/pfad/actions/runs/42964215984)
  at code head `303aa24a4f2e08fffa64f955043fad1efb7aab0c`.
  The first run found the missing SDK in raw Wrangler startup; the corrected
  example uses the same Pywrangler package-bundling route as Week 4.
  This executor itself cannot run workerd's Pyodide fetch because of its DNS
  restrictions. No remote D1, cloud account, credentials or deployment is used.
- Preserved Week 6 local HTTP-client checks: seven pass. Preserved Week 9:
  15 Python socket/state tests and ten browser-state regressions pass locally.

## Teaching previews and limits

115 teaching tests and 25 exercise checks pass. All ten registered decks build
locally to HTML, plain/ClassPoint PowerPoint and PNG previews. The normal-runner
[teaching preview build](https://github.com/sd5913/teaching/actions/runs/42963660375)
also passes at `3ecda5062caa65dcfd99c16a3712a3cc91f210de`, with downloadable
artifacts. Its actual Chromium PDF has 47 pages; all were rendered/visually
reviewed. Both PowerPoint archives have 47 slides and 47 speaker-note records.
Native Microsoft PowerPoint/ClassPoint operation was not tested.
The executor's local Chromium singleton socket is restricted, so the normal
runner supplies browser-PDF evidence. Later metadata-only pins use the same
reviewed slide content. Old PR-body runs/recordings apply to their earlier heads.

Before class: rehearse Docker/dashboard, the prepared D1 machine, actual LM Studio model, browser audio, physical speakers/projector,
student operating systems and timing. Pair at minute 10; preserve the final
20-minute tutor/project block. `QDRANT-PIP.md` distinguishes prepared recordings,
in-process fallback and alternate CLI from a fresh live run. No new graded
submission or assessment policy is introduced. Both PRs remain draft/open.
