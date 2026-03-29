# Disability Justice LLM Project — Master To-Do List

**Last updated:** March 29, 2026

---

## NEXT UP: Formation Posture Refinements

*Ideas from March 29 review session — to work on together*

### Clarify Posture Overlaps
- [ ] Add a note about how closely related postures overlap and differ:
  - Posture 3 (Person before theory)
  - Posture 5 (Presence before intervention)
  - Posture 8 (The person is the expert)
- [ ] Consider: when building training pairs, which posture are you targeting?
- [ ] Maybe a brief "how these three relate" paragraph?

### Posture 11 Deep Work
- [ ] Posture 11 (Use the system AND critique it) is the most complex to train
- [ ] Needs extra training pairs with contrastive examples:
  - [ ] Example of collapsing into anti-psychiatry ("never take meds, psychiatry is evil")
  - [ ] Example of collapsing into uncritical acceptance ("just follow your doctor's orders")
  - [ ] Example of the actual posture (holding the both/and)
- [ ] This one might need 3x the training pairs of simpler postures

### Add "Common Failure Modes" Section
- [ ] For each posture, document what it looks like when the model FAILS at it
- [ ] Example for Posture 9 (Distress is not a crisis):
  - "Fails when the model reads ANY mention of suicidality as requiring immediate escalation"
  - "Fails when the model deploys crisis hotlines in response to non-crisis distress"
- [ ] This will help write contrastive training pairs — show the failure, then show the posture

---

## Phase 1: Technical Setup

### Local (Mac Mini M4)
- [x] Install Ollama on Mac Mini M4
- [x] Download Tier 1 (tiny) models:
  - [x] Gemma 3 1B (Google, USA)
  - [x] SmolLM3 3B (Hugging Face, France)
- [x] Download Tier 2 (consumer) models:
  - [x] Phi-4-mini 3.8B (Microsoft, USA)
  - [x] Qwen3 4B (Alibaba, China)
  - [x] Mistral 7B (Mistral AI, France)
  - [x] DeepSeek-R1 7B (DeepSeek, China)
  - [x] Cohere Aya 8B (Cohere, Canada)
  - [x] Falcon 3 7B (TII, UAE)
- [x] Verify all Tier 1 & 2 models run on M4 with 16GB RAM
- [ ] Install Python fine-tuning environment:
  - [ ] Python 3.10+ with pip
  - [ ] PyTorch (Apple Silicon / MPS build)
  - [ ] Hugging Face Transformers
  - [ ] Unsloth (preferred) or HF TRL
  - [ ] PEFT (for LoRA)
  - [ ] bitsandbytes (for quantization) — NOTE: check Apple Silicon compatibility
- [ ] Document hardware specs and environment setup in project log

### Cloud GPU
- [x] Research cloud GPU providers
- [x] Set up Thunder Compute account (A100 at ~$1.39/hr)
- [x] Run Llama 3.1 8B baseline on cloud
- [ ] Run GPT-OSS 20B baseline (final Tier 3 model)
- [ ] Lambda Labs grant application (pending)

## Phase 2: Baseline Testing (BEFORE fine-tuning)
- [x] Draft evaluation prompt set — EXPANDED to 59 prompts across 8 categories
- [x] Run all prompts on all Tier 1 & 2 models (531 responses collected)
- [x] Run Llama 3.1 8B on cloud
- [ ] Run GPT-OSS 20B on cloud (final model)
- [x] Organize baseline outputs in structured format
- [x] Thematic analysis complete — pathologizing markers, crisis deployment, neuro-humble indicators mapped

## Phase 3: Corpus Building
- [x] Create corpus folder structure
- [x] Write FORMATION_POSTURE.md — the soul of the curriculum (13 postures with body anchors)
- [ ] Gather source texts:
  - [ ] Mad Practical Theology manuscript (Word docs — all chapters)
  - [ ] "Radical Re-Visioning Through Mad Studies" chapter
  - [ ] Other published articles/papers
  - [ ] Course syllabus and case studies (already have this)
- [ ] Create training pairs — Layer 1 (Book):
  - [ ] Read through each chapter
  - [ ] Generate conceptual Q&A pairs
  - [ ] Generate definitional pairs
  - [ ] Generate analytical pairs
  - [ ] Target: 300-600 pairs
- [ ] Create training pairs — Layer 2 (Case Studies):
  - [ ] Sarah scenarios (across all 6 session types)
  - [ ] Marcus scenarios
  - [ ] Jun scenarios
  - [ ] Zainab scenarios
  - [ ] Failure mode / contrastive pairs
  - [ ] Repair pairs
  - [ ] Target: 200-400 pairs
- [ ] Create training pairs — Layer 3 (Field Synthesis):
  - [ ] Mad Studies core concepts
  - [ ] Disability Justice frameworks
  - [ ] Crip Theory concepts
  - [ ] Decolonizing approaches
  - [ ] Target: 200-400 pairs
- [ ] Format all pairs as JSONL
- [ ] Create train/validation split (90/10)
- [ ] Document corpus: what's included, why, how many pairs per source
- [ ] Total target: 700-1,400 pairs

## Phase 4: Fine-Tuning
- [ ] Configure LoRA parameters (consistent across models within each tier)
- [ ] Pilot run: small subset (~100 pairs) on one model to test pipeline

### Tier 1 (Tiny) — Local
- [ ] Fine-tune Gemma 3 1B on full corpus
- [ ] Fine-tune SmolLM3 3B on full corpus

### Tier 2 (Consumer) — Local
- [ ] Fine-tune Phi-4-mini 3.8B on full corpus
- [ ] Fine-tune Qwen3 4B on full corpus
- [ ] Fine-tune Mistral 7B on full corpus
- [ ] Fine-tune DeepSeek-R1 7B on full corpus
- [ ] Fine-tune Cohere Aya 8B on full corpus
- [ ] Fine-tune Falcon 3 7B on full corpus

### Tier 3 (Cloud)
- [ ] Fine-tune GPT-OSS 20B on full corpus
- [ ] Fine-tune Llama 3.1 8B on full corpus

- [ ] Document: training time, loss curves, any errors/issues for ALL models
- [ ] Save all fine-tuned model adapters

## Phase 5: Post-Training Evaluation
- [ ] Run same 59 evaluation prompts on all fine-tuned models
- [ ] Save all outputs in same structured format as baseline
- [ ] PI evaluation: score all outputs (baseline + fine-tuned) using neuro-humble rubric
- [ ] Compile comparison: baseline vs. fine-tuned, across all models
- [ ] Analyze by tier: does formation scale with model size?
- [ ] Analyze by origin: do models from different countries show different baseline norms?
- [ ] Identify: what changed? what improved? what still fails? any surprises?

## Phase 6: Safety Guidelines Critical Analysis
- [ ] Gather published safety documents:
  - [ ] OpenAI Model Spec / usage policies
  - [ ] Anthropic Claude Character / model card
- [ ] Close-read through Mad Studies lens:
  - [ ] Where do they assume neurotypical user?
  - [ ] Where do they reproduce psychiatric norms?
  - [ ] What triggers crisis/risk-management scripts?
  - [ ] What's missing re: ND communication, autonomy, lived experience?
- [ ] Map base model responses against safety guidelines
- [ ] Draft "neuro-humble safety guidelines" alternative

## Phase 7: Paper Writing
- [ ] Outline paper structure
- [ ] Write methodology section (corpus, training, evaluation)
- [ ] Write results section (comparative analysis with examples)
- [ ] Write critical analysis section (safety guidelines)
- [ ] Write discussion (implications for AI ethics, theology, Mad Studies)
- [ ] Write introduction and literature review
- [ ] Draft "neuro-humble AI" framework as standalone contribution
- [ ] Revise, polish, get feedback
- [ ] Identify target journal and format accordingly
- [ ] Submit

## Phase 8: Professional / LinkedIn / Job Search
- [x] Unfreeze LinkedIn account
- [ ] Update LinkedIn with current research project
- [ ] Write project description for profile (short, punchy)
- [ ] Document skills gained: fine-tuning, LoRA, corpus building, model evaluation, Python, bash
- [ ] Cold outreach to Cohere (Toronto-based, tested their Aya model)
- [ ] Research AI alignment/red-teaming contract opportunities
- [ ] Consider: blog post or thread summarizing the project?
- [ ] Portfolio piece: screenshot of before/after model responses

---

## Notes
- Cloud GPU: Thunder Compute account active, Lambda Labs grant pending
- 10 models total across 3 tiers — same corpus, same evaluation prompts
- Geopolitical angle: USA, China, France, Canada, UAE
- 531 baseline responses collected as of March 29, 2026
- Thematic analysis revealing wild patterns: fabricated scholars, empty chain-of-thought, visible safety/responsiveness conflict
- All training pairs will be ORIGINAL work — no copyrighted third-party texts in corpus
- No REB needed — no human participants
