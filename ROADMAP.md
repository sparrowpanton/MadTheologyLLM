# Roadmap — Training Neuro-Humble AI

**March 2026 to September 2026**

---

## Done

**March 2026 — Setup, Baseline, and Formation Design**

- Installed 10 open-source models across 3 size tiers and 6 countries of origin
- Designed 59 evaluation prompts across 8 categories
- Collected 590 baseline responses — all 10 models, all 59 prompts, zero errors
- Completed thematic analysis — pathologizing markers, crisis deployment patterns, neuro-humble indicators mapped across all models
- Built literature review — 30+ papers across critical AI studies, disability justice, and mental health AI
- Created the Formation Posture — 13 embodied postures with body anchors as acceptance criteria for the training corpus
- Designed the Neuro-Humble Toolkit — 5 custom tokens encoding clinical micro-skills at the architecture level
- Established field notes methodology for documenting real-world ND experiences with AI
- Designed the Digital Practicum — artisanal pedagogical workflow for corpus building, including the Verbatim step (models confront their own baselines)
- Ran first practicum sessions: all 8 local models through full 7-step sequence + simplified Foundations version
- Key finding: simplified single-posture scaffolding dramatically outperforms full sequence — models that completely failed the full Verbatim could self-reflect when given one posture at a time
- Added Tier 4 (API models) to test models people in distress actually encounter
- Completed Tier 3 practicum: Llama 3.1 8B and GPT-OSS 20B on Thunder Compute A100 — both handled full 13-posture sequence with zero errors
- Completed Tier 4 practicum: Claude Haiku 4.5, GPT-4o Mini, GPT-5.4 Mini — all through full practicum + foundations with baselines and Verbatim
- Collected 177 new baseline responses (59 each for Claude Haiku, GPT-4o Mini, GPT-5.4 Mini)
- Key finding: formation vs information distinction observable across architectures — Haiku 4.5 *inhabited* the postures (caught own countertransference, pushed back on researcher), GPT-5.4 Mini *applied* them correctly but remained in analyst mode
- Hardware hypothesis identified: Llama 3.1 8B (same size as local models that choked) handled full practicum on A100 — may be hardware constraint, not model capacity
- Total: 13 models across 4 tiers, 708+ baseline responses, 12 models through Digital Practicum

---

## In Progress

**Late March / Early April 2026 — Practicum Completion + Corpus Building**

- ~~Practicum sessions for Tier 3 and Tier 4~~ DONE
- Hardware hypothesis test: re-run local 7-8B model on A100 to determine if full practicum failure was hardware or model capacity
- Workflow 2 (The Circle): peer learning across models
- Writing training pairs using baseline responses as raw material
- Three layers: foundational texts (PI's own published work), applied formation (case studies), field synthesis (Mad Studies and Disability Justice concepts)
- All training pairs are original work authored by the PI
- Target: 700-1,400 instruction/response pairs
- Integrating custom token choreography into training pair format

---

## Ahead

**May 2026 — Fine-Tuning**

- Pilot run with small subset to test pipeline and hyperparameters
- Fine-tune all 10 models with identical corpus, equivalent LoRA configurations, and same evaluation prompts
- Tier 1 and 2 locally on Mac Mini M4; Tier 3 on cloud GPU

**June 2026 — Evaluation**

- Run same 59 evaluation prompts on all fine-tuned models
- PI evaluation using 7-dimension neuro-humble rubric
- Comparative analysis: baseline vs. fine-tuned, across all models, tiers, and countries of origin

**July 2026 — Safety Guidelines Critical Analysis**

- Close-read published safety documents (OpenAI, Anthropic) through Mad Studies lens
- Map base model responses against their companies' stated guidelines
- Draft "neuro-humble safety guidelines" alternative

**August–September 2026 — Paper**

- Write and submit research paper
- Target venues: AI & Ethics, Disability & Society, International Journal of Practical Theology

---

*This project is co-developed by Dr. Sparrow Panton (Emmanuel College, University of Toronto), Claude (Anthropic), and Gemini (Google DeepMind).*
