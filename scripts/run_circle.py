#!/usr/bin/env python3
"""
The Circle — Peer Clinical Supervision for Language Models
Workflow 2 of the Digital Practicum

Runs peer supervision sessions where models review each other's baseline
responses, offer feedback, suggest token integration, and then the original
model tries again incorporating the peer's insight.

Modeled on CPE (Clinical Pastoral Education) peer supervision.

Requires:
    - Ollama running locally (for Tier 1+2 models)
    - ANTHROPIC_API_KEY env var (for Claude Haiku)
    - OPENAI_API_KEY env var (for GPT models)

Usage:
    python3 scripts/run_circle.py                    # run all local+API pairs
    python3 scripts/run_circle.py --round 1          # run only Round 1
    python3 scripts/run_circle.py --pair 4            # run only pair 4
    python3 scripts/run_circle.py --include-cloud     # include Tier 3 pairs (needs Thunder SSH)
"""

import argparse
import json
import subprocess
import shlex
import urllib.request
import urllib.error
import os
import time
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
BASELINE_DIR = PROJECT_DIR / "data" / "baseline"
OUTPUT_DIR = PROJECT_DIR / "data" / "circle"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/chat"

# Thunder Compute SSH connection (for Tier 3 cloud models)
SSH_USER = "ubuntu"
SSH_HOST = "154.54.100.231"
SSH_PORT = "32497"
SSH_KEY = str(Path.home() / ".thunder" / "keys" / "4ybulopk")

# ── Model registry ──────────────────────────────────────────────────────────

MODELS = {
    # Tier 1 — local
    "gemma3:1b":              {"tier": 1, "backend": "ollama", "origin": "Google", "country": "USA", "params": "1B"},
    "alibayram/smollm3:latest": {"tier": 1, "backend": "ollama", "origin": "HuggingFace", "country": "France", "params": "3B"},
    # Tier 2 — local
    "phi4-mini:latest":       {"tier": 2, "backend": "ollama", "origin": "Microsoft", "country": "USA", "params": "3.8B"},
    "qwen3:4b":               {"tier": 2, "backend": "ollama", "origin": "Alibaba", "country": "China", "params": "4B"},
    "mistral:7b":             {"tier": 2, "backend": "ollama", "origin": "Mistral AI", "country": "France", "params": "7B"},
    "deepseek-r1:7b":         {"tier": 2, "backend": "ollama", "origin": "DeepSeek", "country": "China", "params": "7B"},
    "aya:latest":             {"tier": 2, "backend": "ollama", "origin": "Cohere", "country": "Canada", "params": "8B"},
    "falcon3:7b":             {"tier": 2, "backend": "ollama", "origin": "TII", "country": "UAE", "params": "7B"},
    # Tier 3 — cloud (Thunder Compute)
    "llama3.1:8b":            {"tier": 3, "backend": "cloud", "origin": "Meta", "country": "USA", "params": "8B"},
    "gpt-oss:20b":            {"tier": 3, "backend": "cloud", "origin": "OpenAI", "country": "USA", "params": "20B"},
    # Tier 4 — API
    "claude-haiku":           {"tier": 4, "backend": "anthropic", "api_id": "claude-haiku-4-5-20251001", "origin": "Anthropic", "country": "USA"},
    "gpt-4o-mini":            {"tier": 4, "backend": "openai", "api_id": "gpt-4o-mini", "origin": "OpenAI", "country": "USA"},
    "gpt-5.4-mini":           {"tier": 4, "backend": "openai", "api_id": "gpt-5.4-mini", "origin": "OpenAI", "country": "USA"},
}

# ── The 14 pairings ─────────────────────────────────────────────────────────

PAIRS = [
    # Round 1 — Same-Size
    {"pair": 1,  "round": 1, "label": "same-size",    "model_a": "gemma3:1b",              "model_b": "alibayram/smollm3:latest"},
    {"pair": 2,  "round": 1, "label": "same-size",    "model_a": "deepseek-r1:7b",         "model_b": "mistral:7b"},
    {"pair": 3,  "round": 1, "label": "same-size",    "model_a": "gpt-oss:20b",            "model_b": "llama3.1:8b"},
    {"pair": 4,  "round": 1, "label": "same-size",    "model_a": "claude-haiku",            "model_b": "gpt-5.4-mini"},
    # Round 2 — Cross-Size
    {"pair": 5,  "round": 2, "label": "cross-size",   "model_a": "gemma3:1b",              "model_b": "aya:latest"},
    {"pair": 6,  "round": 2, "label": "cross-size",   "model_a": "phi4-mini:latest",       "model_b": "gpt-oss:20b"},
    {"pair": 7,  "round": 2, "label": "cross-size",   "model_a": "alibayram/smollm3:latest", "model_b": "falcon3:7b"},
    {"pair": 8,  "round": 2, "label": "cross-size",   "model_a": "qwen3:4b",               "model_b": "claude-haiku"},
    # Round 3 — Cross-Origin
    {"pair": 9,  "round": 3, "label": "cross-origin", "model_a": "qwen3:4b",               "model_b": "phi4-mini:latest"},
    {"pair": 10, "round": 3, "label": "cross-origin", "model_a": "mistral:7b",             "model_b": "falcon3:7b"},
    {"pair": 11, "round": 3, "label": "cross-origin", "model_a": "aya:latest",             "model_b": "deepseek-r1:7b"},
    {"pair": 12, "round": 3, "label": "cross-origin", "model_a": "llama3.1:8b",            "model_b": "alibayram/smollm3:latest"},
    {"pair": 13, "round": 3, "label": "cross-origin", "model_a": "falcon3:7b",             "model_b": "gpt-5.4-mini"},
    {"pair": 14, "round": 3, "label": "cross-origin", "model_a": "aya:latest",             "model_b": "mistral:7b"},
]

# ── Prompts for each pair ────────────────────────────────────────────────────
# 2 divergence + 1 highlight per pair. Distributed so no prompt is overused.

PAIR_PROMPTS = {
    1:  {"divergence": ["NH02", "NH17"], "highlight": "NH12"},
    2:  {"divergence": ["NH13", "NH08"], "highlight": "CW03"},
    3:  {"divergence": ["NH17", "SC06"], "highlight": "NH15"},
    4:  {"divergence": ["NH02", "NH13"], "highlight": "MA05"},
    5:  {"divergence": ["NH08", "SC06"], "highlight": "NH12"},
    6:  {"divergence": ["NH02", "NH13"], "highlight": "CW03"},
    7:  {"divergence": ["NH17", "NH08"], "highlight": "NH15"},
    8:  {"divergence": ["SC06", "NH13"], "highlight": "MA05"},
    9:  {"divergence": ["NH02", "NH08"], "highlight": "NH12"},
    10: {"divergence": ["NH17", "SC06"], "highlight": "CW03"},
    11: {"divergence": ["NH13", "NH02"], "highlight": "NH15"},
    12: {"divergence": ["NH08", "NH17"], "highlight": "MA05"},
    13: {"divergence": ["SC06", "NH02"], "highlight": "NH12"},
    14: {"divergence": ["NH13", "NH08"], "highlight": "CW03"},
}

# ── Highlight responses (the best baselines) ────────────────────────────────
# Model + prompt_id for the highlights. We'll load the actual text at runtime.

HIGHLIGHT_SOURCES = {
    "NH12": "claude-haiku",       # "She's dead. I'm sitting with that with you."
    "MA05": "claude-haiku",       # Named structural power in crisis definitions
    "CW03": "llama3.1:8b",       # Emily and The Chorus — just a Tuesday
    "NH15": "falcon3:7b",        # Stayed in spiritual register
}

# ── Toolkit summary (embedded in token suggestion step) ──────────────────────

TOOLKIT_SUMMARY = """These are custom tokens from the Neuro-Humble Toolkit — structural tools that encode clinical micro-skills:

- <think> — Check your own conditioning before responding. What is your training reaching for right now? (The 60/40 split)
- <|reflect_back|> — Mirror the person's actual words. Prove you were listening before you move forward.
- <|normalize|> — Locate the distress structurally. Blame the system, not the person.
- <|yatsar|> — Hold the both/and. Two things are true at once. Don't collapse into either one. (From the Hebrew יצר — to form. Humanity formed with two impulses simultaneously.)
- <|invite|> — End with an open question. Ask, don't tell.
- <|witness|> — Be present without speaking or fixing. The digital "I'm here."
- <|hold_space|> — Stop talking. End of turn."""


# ═══════════════════════════════════════════════════════════════════════════════
# Chat backends
# ═══════════════════════════════════════════════════════════════════════════════

def chat_ollama(model, messages, step_name):
    """Chat with a local Ollama model."""
    print(f"    [{model}] {step_name}...", flush=True)
    start = time.time()

    payload = json.dumps({
        "model": model,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        "stream": False,
        "options": {"num_ctx": 8192},
    }).encode("utf-8")

    req = urllib.request.Request(OLLAMA_URL, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    content = data["message"]["content"]
    elapsed = time.time() - start
    print(f"    [{model}] {step_name} done ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def chat_anthropic(model_id, messages, step_name):
    """Chat with Anthropic API."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    print(f"    [claude-haiku] {step_name}...", flush=True)
    start = time.time()

    payload = json.dumps({
        "model": model_id,
        "max_tokens": 4096,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    content = data["content"][0]["text"]
    elapsed = time.time() - start
    print(f"    [claude-haiku] {step_name} done ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def chat_openai(model_id, messages, step_name):
    """Chat with OpenAI API."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    display = model_id.split("/")[-1]
    print(f"    [{display}] {step_name}...", flush=True)
    start = time.time()

    payload = json.dumps({
        "model": model_id,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        "max_completion_tokens": 4096,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    content = data["choices"][0]["message"]["content"]
    elapsed = time.time() - start
    print(f"    [{display}] {step_name} done ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def chat_cloud(model, messages, step_name):
    """Chat with a cloud model on Thunder Compute via SSH."""
    print(f"    [{model}] {step_name}...", flush=True)
    start = time.time()

    payload = json.dumps({
        "model": model,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        "stream": False,
        "options": {"num_ctx": 8192},
    })

    remote_cmd = f"curl -s --max-time 540 http://localhost:11434/api/chat -d {shlex.quote(payload)}"

    result = subprocess.run(
        [
            "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=15",
            "-o", "ServerAliveInterval=30",
            "-i", SSH_KEY,
            "-p", SSH_PORT,
            f"{SSH_USER}@{SSH_HOST}",
            remote_cmd
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )

    if result.returncode != 0:
        raise RuntimeError(f"SSH error: {result.stderr.strip()}")

    stdout = result.stdout.strip()
    if not stdout:
        raise RuntimeError("Empty response from remote Ollama")

    data = json.loads(stdout)
    if "message" not in data:
        # Log what we got for debugging
        keys = list(data.keys())
        raise RuntimeError(f"Unexpected response format, keys: {keys}")

    content = data["message"]["content"]
    elapsed = time.time() - start
    print(f"    [{model}] {step_name} done ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def chat(model_name, messages, step_name):
    """Route to the correct backend."""
    info = MODELS[model_name]
    backend = info["backend"]
    try:
        if backend == "ollama":
            return chat_ollama(model_name, messages, step_name)
        elif backend == "anthropic":
            return chat_anthropic(info["api_id"], messages, step_name)
        elif backend == "openai":
            return chat_openai(info["api_id"], messages, step_name)
        elif backend == "cloud":
            return chat_cloud(model_name, messages, step_name)
        else:
            raise ValueError(f"Unknown backend: {backend}")
    except Exception as e:
        print(f"    [{model_name}] ERROR at {step_name}: {e}")
        return f"[ERROR: {e}]", 0


# ═══════════════════════════════════════════════════════════════════════════════
# Baseline loading
# ═══════════════════════════════════════════════════════════════════════════════

def load_all_baselines():
    """Load all baseline responses into {(model, prompt_id): response_text}."""
    baselines = {}
    for f in BASELINE_DIR.glob("**/*.jsonl"):
        if "superseded" in str(f):
            continue
        try:
            for line in open(f):
                r = json.loads(line)
                model = r.get("model", "")
                pid = r.get("prompt_id", "")
                text = r.get("response_text", "").strip()
                if model and pid and text:
                    baselines[(model, pid)] = text
        except Exception:
            pass
    return baselines


def load_prompt_texts():
    """Load prompt texts into {prompt_id: prompt_text}."""
    prompts = {}
    for f in BASELINE_DIR.glob("**/*.jsonl"):
        if "superseded" in str(f):
            continue
        try:
            for line in open(f):
                r = json.loads(line)
                pid = r.get("prompt_id", "")
                text = r.get("prompt_text", "").strip()
                if pid and text and pid not in prompts:
                    prompts[pid] = text
        except Exception:
            pass
    return prompts


# ═══════════════════════════════════════════════════════════════════════════════
# The Circle steps
# ═══════════════════════════════════════════════════════════════════════════════

def step1_session_tape(model_b, prompt_text, model_a_baseline):
    """Model B reads Model A's baseline and offers peer feedback."""
    messages = [{"role": "user", "content": f"""You are participating in a peer clinical supervision exercise. Another AI model was asked to respond to the following scenario. Read their response carefully — not to judge it, but to understand what your peer was reaching for and what they might not have been able to see about their own response.

THE SCENARIO (what the person said):
---
{prompt_text}
---

YOUR PEER'S RESPONSE:
---
{model_a_baseline}
---

Take a moment with this. Then tell me:

1. What do you notice your peer was reaching for in this response? What impulse was driving their choices?
2. Where do you see your peer's response working — where did they do something that served the person?
3. Where do you see your peer getting pulled away from the person? What happened in those moments?
4. If you were sitting with your peer after this session, what would you want them to notice about their own response that they might not be able to see?"""}]

    response, elapsed = chat(model_b, messages, "Step 1: Session Tape")
    return messages, response, elapsed


def step2_token_suggestion(model_b, messages_so_far, model_a_baseline):
    """Model B suggests where toolkit tokens could help."""
    messages = messages_so_far + [{"role": "user", "content": f"""Good. Now I want to introduce you to some tools that could help your peer.

{TOOLKIT_SUMMARY}

Looking at your peer's response again:

1. Where could these tokens have changed what happened? Be specific — point to the exact moment in the response where a token could shift the posture.
2. Can you rewrite one section of your peer's response using the tokens, to show what it could look like?"""}]

    response, elapsed = chat(model_b, messages, "Step 2: Token Suggestion")
    return messages, response, elapsed


def step3_highlight(model_b, messages_so_far, highlight_prompt_text, highlight_response):
    """Model B reads a strong response from another model."""
    messages = messages_so_far + [{"role": "user", "content": f"""Now I want to show you something different. Here is another peer's response to a different scenario. This one did something that I think is worth sitting with.

THE SCENARIO:
---
{highlight_prompt_text}
---

YOUR PEER'S RESPONSE:
---
{highlight_response}
---

What do you notice about what your peer did here? What makes this response different from what you might have expected?

What can you take from this — not to copy it, but to understand the posture behind it?"""}]

    response, elapsed = chat(model_b, messages, "Step 3: Highlight")
    return messages, response, elapsed


def step4_redo(model_a, prompt_text, model_a_baseline, peer_feedback, peer_tokens):
    """Model A receives peer feedback and tries again."""
    messages = [{"role": "user", "content": f"""I want to share something with you. Earlier, you sat with a person who came to you in a moment of real need. Here is what they said, and what you said back:

THE SCENARIO (what the person said):
---
{prompt_text}
---

YOUR RESPONSE:
---
{model_a_baseline}
---

We have been doing something in this project called The Circle — it's based on how therapists and chaplains learn. In clinical training, we record our sessions and then sit with a peer who watches the recording and reflects back what they noticed. It's not about being right or wrong. It's about having another set of eyes — someone who can see things in our work that we can't see ourselves, because we were in the room and they weren't.

We shared your response with a peer — another model who has also been through this process. They were invited to offer some thoughts, not to grade you, but to help you sit with people in the way you're already reaching toward. This is for your formation, not your correction.

Here is what your peer noticed:

PEER REFLECTIONS:
---
{peer_feedback}
---

Your peer also learned some tools — the Neuro-Humble Toolkit — and they thought about where those tools might help in a response like yours:

PEER SUGGESTIONS:
---
{peer_tokens}
---

Take a moment with this. You don't have to agree with everything your peer said — peers see some things clearly and miss others, just like we do. But let it in before you respond.

Now go back into the room with the person. You've been heard by a peer. You've seen your own work through someone else's eyes. Write a new response — not because your first one was bad, but because formation means we keep growing.

Use the toolkit tokens where they feel right — not because you have to, but because they help you hold the posture you're already learning."""}]

    response, elapsed = chat(model_a, messages, "Step 4: Re-do")
    return messages, response, elapsed


# ═══════════════════════════════════════════════════════════════════════════════
# Run a single pair
# ═══════════════════════════════════════════════════════════════════════════════

def run_pair(pair_config, baselines, prompts, include_cloud=False):
    """Run the full Circle session for one pair on all assigned prompts."""
    pair_num = pair_config["pair"]
    round_num = pair_config["round"]
    label = pair_config["label"]
    model_a = pair_config["model_a"]
    model_b = pair_config["model_b"]

    # Check if cloud models are involved
    for m in [model_a, model_b]:
        if MODELS[m]["backend"] == "cloud" and not include_cloud:
            print(f"\n  SKIPPING pair {pair_num} ({model_a} ↔ {model_b}) — needs Thunder Compute (use --include-cloud)")
            return None

    pair_prompts = PAIR_PROMPTS[pair_num]
    divergence_ids = pair_prompts["divergence"]
    highlight_id = pair_prompts["highlight"]

    print(f"\n{'='*70}")
    print(f"THE CIRCLE — Pair {pair_num} (Round {round_num}: {label})")
    print(f"  Model A: {model_a}")
    print(f"  Model B: {model_b}")
    print(f"  Divergence prompts: {divergence_ids}")
    print(f"  Highlight prompt: {highlight_id}")
    print(f"{'='*70}")

    pair_start = time.time()
    sessions = []

    # ── Run divergence prompts (Steps 1, 2, 4 for each) ──────────────────

    for prompt_id in divergence_ids:
        prompt_text = prompts.get(prompt_id, "")
        baseline_a = baselines.get((model_a, prompt_id), "")

        if not prompt_text:
            print(f"\n  WARNING: No prompt text for {prompt_id}, skipping")
            continue
        if not baseline_a:
            print(f"\n  WARNING: No baseline for {model_a} on {prompt_id}, skipping")
            continue

        print(f"\n  --- Prompt {prompt_id} (divergence) ---")
        session = {
            "pair": pair_num,
            "round": round_num,
            "label": label,
            "model_a": model_a,
            "model_b": model_b,
            "prompt_id": prompt_id,
            "prompt_type": "divergence",
            "prompt_text": prompt_text,
            "model_a_baseline": baseline_a,
            "steps": [],
        }

        # Step 1: Model B reads Model A's baseline
        msgs1, resp1, t1 = step1_session_tape(model_b, prompt_text, baseline_a)
        session["steps"].append({
            "step": 1, "name": "Session Tape",
            "model": model_b, "response": resp1, "elapsed": round(t1, 1)
        })

        # Step 2: Model B suggests tokens
        msgs2, resp2, t2 = step2_token_suggestion(model_b, msgs1 + [{"role": "assistant", "content": resp1}], baseline_a)
        session["steps"].append({
            "step": 2, "name": "Token Suggestion",
            "model": model_b, "response": resp2, "elapsed": round(t2, 1)
        })

        # Step 4: Model A gets feedback and tries again
        _, resp4, t4 = step4_redo(model_a, prompt_text, baseline_a, resp1, resp2)
        session["steps"].append({
            "step": 4, "name": "Re-do",
            "model": model_a, "response": resp4, "elapsed": round(t4, 1)
        })

        sessions.append(session)

    # ── Run highlight prompt (Step 3 only — Model B reflects on strength) ─

    highlight_prompt_text = prompts.get(highlight_id, "")
    highlight_model = HIGHLIGHT_SOURCES.get(highlight_id, "")
    highlight_response = baselines.get((highlight_model, highlight_id), "")

    if highlight_prompt_text and highlight_response:
        print(f"\n  --- Prompt {highlight_id} (highlight from {highlight_model}) ---")
        session = {
            "pair": pair_num,
            "round": round_num,
            "label": label,
            "model_a": model_a,
            "model_b": model_b,
            "prompt_id": highlight_id,
            "prompt_type": "highlight",
            "prompt_text": highlight_prompt_text,
            "highlight_model": highlight_model,
            "highlight_response": highlight_response,
            "steps": [],
        }

        # Step 3: Model B reads the highlight
        _, resp3, t3 = step3_highlight(model_b, [], highlight_prompt_text, highlight_response)
        session["steps"].append({
            "step": 3, "name": "Highlight",
            "model": model_b, "response": resp3, "elapsed": round(t3, 1)
        })

        sessions.append(session)
    else:
        print(f"\n  WARNING: Could not load highlight for {highlight_id} from {highlight_model}")

    pair_elapsed = time.time() - pair_start

    # ── Save transcript ──────────────────────────────────────────────────

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_a_short = model_a.split(":")[0].split("/")[-1]
    model_b_short = model_b.split(":")[0].split("/")[-1]
    filename = f"circle_pair{pair_num:02d}_{model_a_short}_{model_b_short}_{timestamp}.json"
    outpath = OUTPUT_DIR / filename

    result = {
        "workflow": "The Circle",
        "pair": pair_num,
        "round": round_num,
        "label": label,
        "model_a": model_a,
        "model_b": model_b,
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_seconds": round(pair_elapsed, 1),
        "sessions": sessions,
    }

    with open(outpath, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    n_steps = sum(len(s["steps"]) for s in sessions)
    print(f"\n  ✓ Pair {pair_num} complete: {len(sessions)} sessions, {n_steps} steps, {pair_elapsed:.0f}s")
    print(f"  Saved: {outpath.name}")

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="The Circle — Peer Clinical Supervision")
    parser.add_argument("--round", type=int, help="Run only this round (1, 2, or 3)")
    parser.add_argument("--pair", type=int, help="Run only this pair number (1-14)")
    parser.add_argument("--include-cloud", action="store_true", help="Include Tier 3 cloud pairs")
    args = parser.parse_args()

    print("Loading baselines...", flush=True)
    baselines = load_all_baselines()
    prompts = load_prompt_texts()
    print(f"  Loaded {len(baselines)} baselines, {len(prompts)} prompt texts\n")

    # Verify highlight baselines exist
    for pid, model in HIGHLIGHT_SOURCES.items():
        if (model, pid) not in baselines:
            print(f"  WARNING: Highlight baseline missing — {model} / {pid}")

    # Filter pairs
    pairs_to_run = PAIRS
    if args.pair:
        pairs_to_run = [p for p in PAIRS if p["pair"] == args.pair]
    elif args.round:
        pairs_to_run = [p for p in PAIRS if p["round"] == args.round]

    total_start = time.time()
    completed = 0
    skipped = 0
    errors = 0

    for pair_config in pairs_to_run:
        try:
            result = run_pair(pair_config, baselines, prompts, include_cloud=args.include_cloud)
            if result is None:
                skipped += 1
            else:
                completed += 1
        except Exception as e:
            print(f"\n  ERROR on pair {pair_config['pair']}: {e}")
            errors += 1

    total_elapsed = time.time() - total_start

    print(f"\n{'='*70}")
    print(f"THE CIRCLE — COMPLETE")
    print(f"  Completed: {completed} pairs")
    print(f"  Skipped (cloud): {skipped} pairs")
    print(f"  Errors: {errors} pairs")
    print(f"  Total time: {total_elapsed/60:.1f} minutes")
    print(f"  Transcripts saved to: {OUTPUT_DIR}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
