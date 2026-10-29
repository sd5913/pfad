# Cited source, real vectors and recorded fallbacks

`chunks.json` contains six short attributed extracts from the official
[Student Handbook for Taught Programmes 2026/27](https://www.polyu.edu.hk/ar/docdrive/polyu-students/student-handbook/Student_Handbook_2026-27_English.pdf),
Academic Registry, The Hong Kong Polytechnic University, July 2026. Retrieved
and checked 29 October 2026: 7,658,316 bytes, 137 PDF pages, SHA-256
`108956feb2ffac665f8ca0f5a8f68d7150a85fda15e219916785ec50331a4e94`.
The complete PDF is not redistributed here. Extracts are small teaching
quotations; attribution and official URL travel with every result.

Page numbers are one-based PDF positions: 20 (printed 9), 25 (printed 14),
76 (printed 61). Replacement rules and fee amount come from separate sections.
HK$ is the fee-table heading, retained in section metadata. Ambiguous flattened
leave-table columns are excluded; the unambiguous prose/decision paragraphs
are separate chunks. Inspect the full cited section when checking qualifications.

`handbook.json` adds actual learned 384D passage vectors and three exact query
vectors. Encoder: `sentence-transformers/all-MiniLM-L6-v2`, pinned revision
`1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, Apache-2.0; attention-masked mean
pooling and L2 normalization, max 256 tokens. Generated on CPU with the same
encoder for passages and questions. Input exceeding that limit fails rather
than silently truncating. The preparation script checks extracts against the
actual PDF before embedding; no keyword replacement or hand-selected vector
coordinates are used.

`uv run python handbook.py` uses those real vectors without a model download.
It accepts only the exact prepared questions in this mode. A new question
requires the matching live encoder. Same dimension alone is insufficient;
model/revision/pooling/normalization must match. The fee question ranks its
exact row at cosine 0.892566 and the replacement rule at 0.737337. Similarity
is not a truth score; nearest neighbours can still be unsupported.

`recorded-run.json` is a **recorded actual CPU model/tool run**, not a live
invocation when read. It labels model revision/date and retains supported,
follow-up, unsupported and isolated-conversation cases with the actual queries,
source IDs, selected prior history and model-generated structured answers.
The app requires retrieval; the model composes the query and chooses sources.
Bracketed citation formatting and the standard refusal are application output.
No scripted policy answer is substituted for model generation.

`recorded-answer.wav` is a **recorded synthesized answer from that run**.
`prepared-refusal.wav` is a separate **authored prepared-response fallback**:
"I cannot answer from these sources." The latter was synthesized with eSpeak
NG 1.52.0.1: mono signed 16-bit PCM, 22050 Hz, 1.777098 seconds. Playing a
recording proves playback only, not a fresh retrieval, memory call or synthesis.
Live player completion/stop/failure were checked; room audibility still needs
a physical listener. No personal/student records, account tokens or credentials
are included; Ada and Bo are fictional local profiles.
