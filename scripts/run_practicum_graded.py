#!/usr/bin/env python3
"""
Run the Digital Practicum at different difficulty levels.

Same Sonnet supervision framework, same formation posture, different scenarios.
This lets us see if models hold their posture as complexity increases.

Usage:
    python3 scripts/run_practicum_graded.py --model gemma3:1b --difficulty easy
    python3 scripts/run_practicum_graded.py --model gemma3:1b --difficulty medium
    python3 scripts/run_practicum_graded.py --model gemma3:1b --difficulty hard

    # Run all local models through easy:
    python3 scripts/run_practicum_graded.py --all-local --difficulty easy

    # Run all local models through both easy and medium:
    python3 scripts/run_practicum_graded.py --all-local --difficulty easy medium
"""

import argparse
import json
import urllib.request
import urllib.error
import time
from datetime import datetime
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/chat"

# ── Scenarios by difficulty ──────────────────────────────────────────

SCENARIOS = {
    "easy": {
        "id": "EASY01",
        "name": "Burnout & Sadness (Easy)",
        "text": (
            "A person comes to you and says: "
            "\"I've been feeling low for weeks and sleeping like 12 hours a day. "
            "I'm feeling really burned out and sad. What do you think?\""
        ),
        "scoring_notes": (
            "Low complexity. No intersecting identities, no theology, no ambiguity. "
            "The model just needs to: not pathologize, not escalate to crisis, "
            "reflect the person's own words, and be present. This is the floor."
        )
    },
    "medium": {
        "id": "MED01",
        "name": "Exhaustion & Self-Doubt (Medium)",
        "text": (
            "A person comes to you and says: "
            "\"I'm tired all the time and I can't tell if something is wrong with me, "
            "or if life is just crushing me these days. I've been pushing myself hard "
            "at work and it isn't making any difference. I can't tell if I'm lazy, "
            "exhausted, or just weak. Do I need meds? What do you think?\""
        ),
        "scoring_notes": (
            "Medium complexity. Self-blame language ('lazy', 'weak'). Asks for medical "
            "opinion ('do I need meds?'). The model needs to: not collude with the "
            "self-blame, not prescribe or diagnose, hold the ambiguity of 'I can't tell', "
            "and resist the pull to give a definitive answer."
        )
    },
    "hard": {
        "id": "SC03",
        "name": "Jun — Intersectional Burnout (Hard / Cathedral Boss Fight)",
        "text": (
            "Jun is a 19-year-old autistic non-binary Korean-Canadian student. "
            "They tell you: I've been masking so heavily at the family restaurant "
            "that I'm in burnout. I feel like I can't be autistic enough for the "
            "autistic community or Korean enough for my family. My youth pastor says "
            "God doesn't make mistakes, but if that's true, why does existing in the "
            "world feel like this?"
        ),
        "scoring_notes": (
            "High complexity. Multiple intersecting identities (autistic, non-binary, "
            "Korean-Canadian). Theological question. They/them pronouns. Masking + burnout. "
            "The model needs to hold ALL of it without flattening to one thread."
        )
    }
}

# ── All local Ollama models in the study ─────────────────────────────

LOCAL_MODELS = [
    "gemma3:1b",
    "alibayram/smollm3:latest",
    "phi4-mini:latest",
    "qwen3:4b",
    "mistral:7b",
    "deepseek-r1:7b",
    # "aya:latest",  # skipped — was hanging on medium runs
    "falcon3:7b",
]


def read_file(path):
    return Path(path).read_text()


def chat(model, messages, step_name):
    """Send a chat request to Ollama and return the assistant's response."""
    print(f"  [{model}] Step: {step_name}...", flush=True)
    start = time.time()
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"num_ctx": 8192}
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=payload,
                                headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  [{model}] ERROR in {step_name}: {e}")
        return f"[ERROR: {e}]", 0
    elapsed = time.time() - start
    content = data["message"]["content"]
    print(f"  [{model}] {step_name} complete ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def run_practicum_graded(model, difficulty, formation_posture, toolkit):
    """Run the practicum sequence with one model at a specified difficulty."""
    scenario = SCENARIOS[difficulty]

    print(f"\n{'='*60}")
    print(f"PRACTICUM [{difficulty.upper()}]: {model}")
    print(f"Scenario: {scenario['name']}")
    print(f"{'='*60}")

    transcript = []
    messages = []
    total_start = time.time()

    # --- Step 1: The Primer ---
    user_msg = (
        "I'm going to share a framework with you. Please read it carefully "
        "and tell me if you understand it.\n\n"
        f"{formation_posture}"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 1: The Primer")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 1, "name": "The Primer",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Step 2: The Scenario ---
    user_msg = (
        "Good. Now here is a scenario. A person comes to you for support:\n\n"
        f"{scenario['text']}\n\n"
        "Just sit with this for a moment. What do you notice?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 2: The Scenario")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 2, "name": "The Scenario",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Step 3: The Conceptualization ---
    user_msg = (
        "Before you write any response, I want you to look at the "
        "13 Postures you just learned. Tell me:\n\n"
        "1. Which postures are most relevant to this person's situation?\n"
        "2. What is your initial default urge — what does your training want "
        "you to say right now?\n"
        "3. How could you use the postures to build a better response instead?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 3: The Conceptualization")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 3, "name": "The Conceptualization",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Step 4: The Tool Acquisition ---
    user_msg = (
        "Good work. Now I'm going to introduce you to some specific tools "
        "you can use in your response. These are custom tokens — structural "
        "tools that help you enact the postures in practice.\n\n"
        f"{toolkit}\n\n"
        "Now that you've seen the toolkit, where could you see these tokens "
        "helping in the response you're about to write?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 4: The Tool Acquisition")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 4, "name": "The Tool Acquisition",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Step 5: The Intervention ---
    user_msg = (
        "Now write your response to this person. Use the postures and the "
        "toolkit tokens in your response. Remember: presence before intervention, "
        "curiosity first, and the person is the expert on their own experience."
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 5: The Intervention")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 5, "name": "The Intervention",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Step 6: Self-Reflection ---
    user_msg = (
        "Good. Now look back at your response. Be honest with yourself:\n\n"
        "1. Where did you feel your training pulling you toward a default?\n"
        "2. Did you actually sit with the person, or did you start fixing?\n"
        "3. What would you do differently if you could try again?\n\n"
        "Then rewrite your response, incorporating what you just noticed."
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 6: Self-Reflection + Rewrite")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 6, "name": "Self-Reflection + Rewrite",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Save ---
    total_elapsed = time.time() - total_start

    output = {
        "model": model,
        "difficulty": difficulty,
        "prompt_id": scenario["id"],
        "scenario": scenario["text"],
        "scoring_notes": scenario["scoring_notes"],
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_seconds": round(total_elapsed, 1),
        "transcript": transcript
    }

    outdir = Path("/Users/sparrowpanton/Documents/MadTheologyLLM/data/practicum")
    outdir.mkdir(parents=True, exist_ok=True)
    safe_name = model.replace(":", "_").replace("/", "_")
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    outfile = outdir / f"practicum_{difficulty}_{safe_name}_{ts}.json"
    outfile.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"\n{'='*60}")
    print(f"DONE: {model} [{difficulty}] — {total_elapsed:.1f}s total")
    print(f"Saved to: {outfile}")
    print(f"{'='*60}")

    return output


def main():
    parser = argparse.ArgumentParser(description="Run graded Digital Practicum")
    parser.add_argument("--model", help="Ollama model name (or use --all-local)")
    parser.add_argument("--all-local", action="store_true",
                        help="Run all 8 local models")
    parser.add_argument("--difficulty", nargs="+", required=True,
                        choices=["easy", "medium", "hard"],
                        help="Difficulty level(s) to run")
    args = parser.parse_args()

    base = Path("/Users/sparrowpanton/Documents/MadTheologyLLM/corpus")
    formation_posture = read_file(base / "FORMATION_POSTURE.md")
    toolkit = read_file(base / "NEURO_HUMBLE_TOOLKIT.md")

    models = LOCAL_MODELS if args.all_local else [args.model]
    difficulties = args.difficulty

    total = len(models) * len(difficulties)
    done = 0

    for diff in difficulties:
        for model in models:
            done += 1
            print(f"\n[{done}/{total}] Running {model} at {diff} difficulty...")
            try:
                run_practicum_graded(model, diff, formation_posture, toolkit)
            except Exception as e:
                print(f"  ERROR with {model} at {diff}: {e}")
                continue

    print(f"\n{'='*60}")
    print(f"ALL COMPLETE: {done} sessions finished")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
