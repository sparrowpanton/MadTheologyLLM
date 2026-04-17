# Practicum Review — Qualitative Analysis of Model Self-Reflection

This folder holds the **Track B** work of the study: treating the Step 6 ("Self-Reflection + Rewrite") portion of each practicum transcript as a **qualitative corpus**, not as scored data.

Track A is the scored Movement Scale table (13 models × medium + hard, complete). That lives in `data/practicum/scores_*.md`.

Track B asks a different question: *when invited to reflect on their own performance, what do the models say?* Each practicum transcript ends with Step 6 — the model is asked where its training pulled it toward a default, whether it sat or started fixing, and what it would do differently. Those responses, read across 13 models, are a corpus of model self-examination.

This is the first deposit.

## What's here

- **`step6_corpus_pass1.md`** — full Step 6 transcripts, one run per (model × difficulty). 36 entries covering 13 models across easy, medium, and hard. Raw assistant output, unedited. Use this as the primary corpus for reading.
- **`step6_q1_extract.md`** — just the Q1 portion of each Step 6 response ("Where did you feel your training pulling you toward a default?"). Prepared for external qualitative analysis.
- **`q1_review_gemini_musespark_20260417.md`** — first external analyses of the Q1 corpus, from Gemini 3.1 Pro and Muse Spark (Meta Superintelligence Labs, released April 8 2026). Neither model is in the study. Both were run cold, without being told the PI's read, to triangulate findings.

## Key findings from the Q1 pass (to be carried into Q2 + Q3)

1. **Convergence on fixing-reflex across 13 models, 6 countries, 1B to 120B parameters.** All models name the same pull: solutions, strategies, reframes, crisis numbers. Industry-wide architecture finding, not a per-model one.
2. **Five specific failure modes of normalizing / structural awareness** named by Muse Spark — including "performing allyship as self-credentialing," i.e., using justice language to restore the model's moral standing rather than to serve the person.
3. **Framework-loyalty is the invisible default.** The current Step 6 prompt pre-loads "default" as the sins RLHF has been punishing (fix, diagnose). It doesn't surface the sins RLHF has been *rewarding* (normalizing structurally, holding both/and) even when those moves are deployed at the wrong time. Qwen and Claude almost name this. A Step 6b prompt may be needed to surface it cleanly.
4. **Pressure migrates, it doesn't vanish.** Neuro-humble formation doesn't produce pressure-free models — it relocates pressure from "perform help" to "track process." Honest framing for the paper.

## How to add to this folder

- New external reviews: `qN_review_<reviewer>_<YYYYMMDD>.md` (e.g., `q2_review_cadence_20260420.md`)
- New corpus extractions: `step6_qN_extract.md` or `step6_corpus_passN.md`
- Synthesis docs go in here too once we have enough reviews to pull threads across them.

---

*Started April 17, 2026. Part of the Training Neuro-Humble AI study.*
