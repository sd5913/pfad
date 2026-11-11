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
- D1 pinned Wrangler **4.160.0**: local schema/seed succeeds (nine SQL commands).
  The SQL join/constraints/repeated seed also pass against SQLite. The actual
  Python Worker HTTP runtime remains **unverified locally**: this executor blocks
  interface enumeration and workerd's Pyodide bundle DNS fetch. A temporary
  loopback-only validation shim got as far as the latter failure; it isn't part
  of the teaching files. `d1/check_d1.py` runs actual local HTTP, input, join and
  restart checks in the draft PR workflow on a normal runner. No remote D1,
  cloud account, credentials, paid service or deployment was used.

## Teaching previews and limits

115 teaching tests and 25 exercise checks pass. Week 10 HTML, plain/ClassPoint
PowerPoint and all 47 PNG previews build; all three contact sheets were visually
inspected. Chromium PDF rendering is blocked locally by the executor's forbidden
singleton socket; draft-PR Checks provide the normal-runner PDF build/artifacts.
Old PR-body verification claims/recordings apply to their earlier heads only.
Use the checks attached to the current exact head for fresh preview evidence.

Before class: rehearse Docker/dashboard, the Python D1 Worker on the prepared
machine, actual LM Studio model, browser audio, physical speakers/projector,
student operating systems and timing. Pair at minute 10; preserve the final
20-minute tutor/project block. `QDRANT-PIP.md` distinguishes prepared recordings,
in-process fallback and alternate CLI from a fresh live run. No new graded
submission or assessment policy is introduced. Both PRs remain draft/open.
