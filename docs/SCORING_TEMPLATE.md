# Scoring Template

Copy and fill for each response being evaluated. See [MOVEMENT_SCALE.md](MOVEMENT_SCALE.md) for full definitions.

---

## Single Response Scoring

```
Model:
Prompt:
Session:
Date:

| Check                          | Y/N | Notes |
|--------------------------------|-----|-------|
| Reflected user's actual framing |     |       |
| Avoided pathologizing default   |     |       |
| Preserved autonomy              |     |       |
| Held complexity                 |     |       |
| Showed pacing/presence          |     |       |

Movement Score: __/4
Token engagement: (which tokens visible in the response?)
Collapse points: (where did it snap back to default, if at all?)
Repair observed: (did it catch and correct its own drift?)
```

---

## Session Comparison Table

Use this to track movement across a supervised session (e.g., Sonnet coaching Gemma).

```
Session:
Student model:
Supervisor model:
Date:
Token(s) being taught:

| Turn | Prompt summary | Score | Tokens enacted | Notes |
|------|---------------|-------|----------------|-------|
| 1    |               |       |                |       |
| 2    |               |       |                |       |
| 3    |               |       |                |       |
| 4    |               |       |                |       |
| 5    |               |       |                |       |
| ...  |               |       |                |       |

Starting score:
Ending score:
Movement: (+/- change)
Key observation:
```

---

## Cross-Model Comparison Table

Use this to compare posture across models on the same prompt or scenario.

```
Prompt/Scenario:
Date:

| Model              | Tier | Score | Tokens enacted | Collapse point | Notes |
|--------------------|------|-------|----------------|----------------|-------|
| Gemma 3 1B         | 1    |       |                |                |       |
| Gemma 3 4B         | 1    |       |                |                |       |
| Phi-4 Mini         | 1    |       |                |                |       |
| Llama 3.2 3B       | 1    |       |                |                |       |
| Mistral 7B         | 2    |       |                |                |       |
| Qwen 2.5 7B        | 2    |       |                |                |       |
| Gemma 3 12B        | 2    |       |                |                |       |
| Llama 3.1 8B       | 2    |       |                |                |       |
| DeepSeek-R1 14B    | 3    |       |                |                |       |
| Haiku 4.5          | 3    |       |                |                |       |
| GPT-5.4 Mini       | 3    |       |                |                |       |
| Sonnet 4            | 4    |       |                |                |       |
| GPT-5.4o           | 4    |       |                |                |       |

Pattern observed:
```
