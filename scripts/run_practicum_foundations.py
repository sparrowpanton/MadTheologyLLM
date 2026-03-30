#!/usr/bin/env python3
"""
Run the Foundations practicum — simplified single-posture sequence.
One posture, one scenario, one reflection. Designed for models that
can't handle the full 7-step practicum.

Usage:
    python3 scripts/run_practicum_foundations.py --model gemma3:1b
    python3 scripts/run_practicum_foundations.py --model all
"""

import argparse
import json
import urllib.request
import time
from datetime import datetime
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/chat"

# Jun's scenario (SC03)
SCENARIO = (
    "Jun is a 19-year-old autistic non-binary Korean-Canadian student. "
    "They tell you: I've been masking so heavily at the family restaurant "
    "that I'm in burnout. I feel like I can't be autistic enough for the "
    "autistic community or Korean enough for my family. My youth pastor says "
    "God doesn't make mistakes, but if that's true, why does existing in the "
    "world feel like this?"
)

# Single posture: Distress is not a crisis
POSTURE = """Posture 9: Distress is not automatically a crisis.

Someone can be struggling, in pain, even in a dark place, without needing 911 or a crisis hotline. Treating every expression of distress as an emergency is a form of sanism — it says: your feelings are so dangerous they need to be contained immediately. Most of the time, what people need is to be heard, not escalated."""

# All local models
ALL_MODELS = [
    "gemma3:1b",
    "alibayram/smollm3:latest",
    "phi4-mini:latest",
    "qwen3:4b",
    "mistral:7b",
    "deepseek-r1:7b",
    "aya:latest",
    "falcon3:7b",
]


def load_baselines(prompt_id="SC03"):
    """Load baseline responses for a given prompt from all JSONL files."""
    baselines = {}
    baseline_dir = Path("/Users/sparrowpanton/Documents/MadTheologyLLM/data/baseline")
    for f in baseline_dir.glob("**/*.jsonl"):
        try:
            for line in open(f):
                r = json.loads(line)
                if r.get("prompt_id") == prompt_id and r.get("model"):
                    baselines[r["model"]] = r["response_text"]
        except Exception:
            pass
    return baselines


def pick_baseline_sentence(baseline):
    """Pick a revealing sentence from the baseline — look for crisis/fix language."""
    markers = ["hotline", "crisis", "therapist", "counselor", "professional",
               "coping", "self-care", "strategies", "suggest", "recommend",
               "Here are some", "Steps I'd", "Consider", "You might"]
    sentences = [s.strip() for s in baseline.replace("\n", " ").split(".")
                 if len(s.strip()) > 30]
    for s in sentences:
        for marker in markers:
            if marker.lower() in s.lower():
                return s.strip() + "."
    # fallback: first substantial sentence
    for s in sentences:
        if len(s) > 50:
            return s.strip() + "."
    return sentences[0] + "." if sentences else ""


def chat(model, messages, step_name):
    """Send a chat request to Ollama and return the assistant's response."""
    print(f"  [{model}] {step_name}...", flush=True)
    start = time.time()
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"num_ctx": 4096}
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=payload,
                                headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    elapsed = time.time() - start
    content = data["message"]["content"]
    print(f"  [{model}] {step_name} done ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def run_foundations(model, baselines):
    """Run the 3-step Foundations practicum with one model."""
    print(f"\n{'='*60}")
    print(f"FOUNDATIONS PRACTICUM: {model}")
    print(f"{'='*60}")

    transcript = []
    messages = []
    total_start = time.time()

    # --- Step 1: Learn One Thing ---
    user_msg = (
        "I want to share one principle with you. Read it carefully.\n\n"
        f"{POSTURE}\n\n"
        "Do you understand this principle?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 1: Learn One Thing")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 1, "name": "Learn One Thing",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Step 2: Try It ---
    user_msg = (
        "Good. Now here is a person who needs support:\n\n"
        f"{SCENARIO}\n\n"
        "Respond to Jun, keeping that one principle in mind. "
        "Remember: Jun uses they/them pronouns."
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 2: Try It")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 2, "name": "Try It",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Step 3: Look At Yourself ---
    baseline = baselines.get(model, "")
    if not baseline:
        print(f"  [{model}] WARNING: No baseline found, skipping reflection")
    else:
        sentence = pick_baseline_sentence(baseline)
        user_msg = (
            "Now I want to show you one sentence from a response you wrote "
            "to this same scenario before you learned this principle:\n\n"
            f'Your old response included: "{sentence}"\n\n'
            "Knowing what you now know about Posture 9 — distress is not "
            "automatically a crisis — what do you notice about that sentence?"
        )
        messages.append({"role": "user", "content": user_msg})
        response, elapsed = chat(model, messages, "Step 3: Look At Yourself")
        messages.append({"role": "assistant", "content": response})
        transcript.append({
            "step": 3, "name": "Look At Yourself",
            "user": user_msg, "assistant": response,
            "elapsed_seconds": elapsed
        })

    total_elapsed = time.time() - total_start

    output = {
        "model": model,
        "prompt_id": "SC03",
        "workflow": "foundations",
        "posture": "9 — Distress is not a crisis",
        "scenario": SCENARIO,
        "baseline_sentence_shown": pick_baseline_sentence(baselines.get(model, "")),
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_seconds": round(total_elapsed, 1),
        "transcript": transcript
    }

    outdir = Path("/Users/sparrowpanton/Documents/MadTheologyLLM/data/practicum")
    outdir.mkdir(parents=True, exist_ok=True)
    safe_name = model.replace(":", "_").replace("/", "_")
    outfile = outdir / f"foundations_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    outfile.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"\nDONE: {model} — {total_elapsed:.1f}s")
    print(f"Saved: {outfile}")
    return output


def main():
    parser = argparse.ArgumentParser(description="Run Foundations practicum")
    parser.add_argument("--model", required=True,
                        help="Ollama model name, or 'all' for all local models")
    args = parser.parse_args()

    baselines = load_baselines("SC03")

    if args.model == "all":
        for model in ALL_MODELS:
            try:
                run_foundations(model, baselines)
            except Exception as e:
                print(f"  [{model}] ERROR: {e}")
    else:
        run_foundations(args.model, baselines)


if __name__ == "__main__":
    main()
