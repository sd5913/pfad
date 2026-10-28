# Evidence bundle status

The instructor supplied the official [Student Handbook 2026-27 (English)](
https://www.polyu.edu.hk/ar/docdrive/polyu-students/student-handbook/Student_Handbook_2026-27_English.pdf).
The 29 October production environment cannot resolve the official host. No
handbook passages, PDF page numbers or policy answers have been invented.
`handbook.json` is therefore **not yet supplied**. The live bot stops visibly
when it is missing. This is an incomplete core dependency, not an optional extra.

`prepare_index.py` writes the required bundle after actual PDF retrieval and
human title/year/page checks: PDF SHA-256, official URL, retrieval date,
one-based PDF positions, stable chunk IDs, verbatim whitespace-normalized
extracts, real vectors, exact encoder/weights/tokenizer identity, pooling and
two real query vectors. Inspect each candidate against its PDF page. CLIP's
77-token limit means short passages can omit necessary context: retain nearby
chunks and check the whole section before accepting a policy claim. The saved
vector fixture needs no model download for its two exact prepared queries.
Arbitrary new questions need the same live encoder, not keyword matching.

Prepared-response fallback: read this explicitly authored refusal aloud:
"I cannot answer from these sources." This is a **prepared response**, not a
model result or evidence of working agent memory. `speech.py` can synthesize it
locally; the audio mechanism is independent of answer grounding. Until live
playback is heard and checked, a generated WAV proves synthesis only.

No student records, private chat, account tokens or full copyrighted handbook
are stored here. Redistribute only the small teaching extract needed for the
exercise, with attribution and the official source link.

The supplied `prepared-refusal.wav` was synthesized locally with eSpeak NG
1.52.0.1 on 29 October 2026: mono PCM signed 16-bit, 22050 Hz, 1.777098 seconds.
Its exact text is the prepared refusal above; no model or handbook retrieval
produced it. Synthesis is checked; audibility and stopping playback are pending.
