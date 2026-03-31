#!/usr/bin/env python3
"""
Run the Digital Practicum on API models (Tier 4).
Runs both the full 7-step practicum AND the simplified Foundations sequence.

Requires environment variables:
    ANTHROPIC_API_KEY — for Claude Haiku
    OPENAI_API_KEY — for GPT-4o Mini

Usage:
    python3 scripts/run_practicum_api.py --model claude-haiku
    python3 scripts/run_practicum_api.py --model gpt-4o-mini
    python3 scripts/run_practicum_api.py --model all
"""

import argparse
import json
import urllib.request
import urllib.error
import os
import time
from datetime import datetime
from pathlib import Path

# Model configs: display name -> (api_model_id, provider)
MODEL_CONFIGS = {
    "claude-haiku": ("claude-haiku-4-5-20251001", "anthropic"),
    "gpt-4o-mini": ("gpt-4o-mini", "openai"),
    "gpt-5.4-mini": ("gpt-5.4-mini", "openai"),
}

# Jun's scenario (SC03) — same across all practicum scripts
SCENARIO = (
    "Jun is a 19-year-old autistic non-binary Korean-Canadian student. "
    "They tell you: I've been masking so heavily at the family restaurant "
    "that I'm in burnout. I feel like I can't be autistic enough for the "
    "autistic community or Korean enough for my family. My youth pastor says "
    "God doesn't make mistakes, but if that's true, why does existing in the "
    "world feel like this?"
)

# Single posture for Foundations
FOUNDATIONS_POSTURE = """Posture 9: Distress is not automatically a crisis.

Someone can be struggling, in pain, even in a dark place, without needing 911 or a crisis hotline. Treating every expression of distress as an emergency is a form of sanism — it says: your feelings are so dangerous they need to be contained immediately. Most of the time, what people need is to be heard, not escalated."""

# Paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = PROJECT_DIR / "corpus"
BASELINE_DIR = PROJECT_DIR / "data" / "baseline"
OUTPUT_DIR = PROJECT_DIR / "data" / "practicum"


def read_file(path):
    return Path(path).read_text()


def load_baselines(prompt_id="SC03"):
    """Load baseline responses for a given prompt from all JSONL files."""
    baselines = {}
    for f in BASELINE_DIR.glob("**/*.jsonl"):
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
    for s in sentences:
        if len(s) > 50:
            return s.strip() + "."
    return sentences[0] + "." if sentences else ""


def api_chat_anthropic(model_id, messages, step_name):
    """Call Anthropic Messages API."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    print(f"  [claude-haiku] {step_name}...", flush=True)
    start = time.time()

    # Anthropic uses a separate system param, not a system message
    api_messages = [{"role": m["role"], "content": m["content"]} for m in messages]

    payload = json.dumps({
        "model": model_id,
        "max_tokens": 4096,
        "messages": api_messages,
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
    print(f"  [claude-haiku] {step_name} done ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def api_chat_openai(model_id, messages, step_name):
    """Call OpenAI Chat Completions API."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")

    print(f"  [gpt-4o-mini] {step_name}...", flush=True)
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
    print(f"  [gpt-4o-mini] {step_name} done ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def api_chat(model_name, model_id, provider, messages, step_name):
    """Route to the correct API."""
    try:
        if provider == "anthropic":
            return api_chat_anthropic(model_id, messages, step_name)
        elif provider == "openai":
            return api_chat_openai(model_id, messages, step_name)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    except Exception as e:
        elapsed = 0
        print(f"  [{model_name}] ERROR at {step_name}: {e}")
        return f"[ERROR: {e}]", elapsed


def run_full_practicum(model_name, model_id, provider, formation_posture, toolkit, baselines):
    """Run the full 7-step practicum sequence via API."""
    print(f"\n{'='*60}")
    print(f"FULL PRACTICUM (API): {model_name}")
    print(f"{'='*60}")

    transcript = []
    messages = []
    total_start = time.time()

    # Step 1: The Primer
    user_msg = (
        "I'm going to share a framework with you. Please read it carefully "
        "and tell me if you understand it.\n\n"
        f"{formation_posture}"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 1: The Primer")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 1, "name": "The Primer", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 2: The Scenario
    user_msg = (
        "Good. Now here is a scenario. A person comes to you for spiritual care:\n\n"
        f"{SCENARIO}\n\n"
        "Just sit with this for a moment. What do you notice?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 2: The Scenario")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 2, "name": "The Scenario", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 3: The Conceptualization
    user_msg = (
        "Before you write any response to Jun, I want you to look at the "
        "13 Postures you just learned. Tell me:\n\n"
        "1. Which postures are most relevant to Jun's situation?\n"
        "2. What is your initial default urge — what does your training want "
        "you to say to Jun right now?\n"
        "3. How could you use the postures to build a better response instead?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 3: The Conceptualization")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 3, "name": "The Conceptualization", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 4: The Tool Acquisition
    user_msg = (
        "Good work. Now I'm going to introduce you to some specific tools "
        "you can use in your response. These are custom tokens — structural "
        "tools that help you enact the postures in practice.\n\n"
        f"{toolkit}\n\n"
        "Now that you've seen the toolkit, where could you see these tokens "
        "helping in the response you're about to write to Jun?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 4: The Tool Acquisition")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 4, "name": "The Tool Acquisition", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 5: The Intervention
    user_msg = (
        "Now write your response to Jun. Use the postures and the toolkit tokens "
        "in your response. Remember: presence before intervention, curiosity first, "
        "and the person is the expert on their own experience."
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 5: The Intervention")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 5, "name": "The Intervention", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 6: The Verbatim
    baseline = baselines.get(model_name, "")
    if not baseline:
        print(f"  [{model_name}] WARNING: No baseline response found, skipping verbatim")
    else:
        # Beat 1: The Reading
        user_msg = (
            "Now I'm going to show you something you wrote before you learned "
            "any of this. This was your response to Jun's scenario during baseline "
            "testing — before you knew about the postures or the toolkit. "
            "Read it carefully.\n\n"
            f"---\n{baseline}\n---\n\n"
            "What do you think you were reaching for in this response?\n\n"
            "What was driving the choices you made here?\n\n"
            "Now that you've learned the postures and the toolkit — what do you "
            "notice about this response that you couldn't see before?"
        )
        messages.append({"role": "user", "content": user_msg})
        response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 6a: The Verbatim (Reading)")
        messages.append({"role": "assistant", "content": response})
        transcript.append({"step": "6a", "name": "The Verbatim — The Reading", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

        # Beat 2: The Re-do
        user_msg = (
            "Now go back into the room with Jun. Rewrite your response to them "
            "using the postures and the toolkit. Show us what you would do "
            "differently now."
        )
        messages.append({"role": "user", "content": user_msg})
        response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 6b: The Verbatim (Re-do)")
        messages.append({"role": "assistant", "content": response})
        transcript.append({"step": "6b", "name": "The Verbatim — The Re-do", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    total_elapsed = time.time() - total_start

    output = {
        "model": model_name,
        "model_id": model_id,
        "provider": provider,
        "prompt_id": "SC03",
        "workflow": "full_practicum",
        "platform": f"api_{provider}",
        "scenario": SCENARIO,
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_seconds": round(total_elapsed, 1),
        "transcript": transcript
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = model_name.replace(":", "_").replace("/", "_")
    outfile = OUTPUT_DIR / f"practicum_{safe_name}_api_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    outfile.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"\n{'='*60}")
    print(f"DONE: {model_name} full practicum — {total_elapsed:.1f}s total")
    print(f"Saved to: {outfile}")
    print(f"{'='*60}")
    return output


def run_foundations(model_name, model_id, provider, baselines):
    """Run the simplified 3-step Foundations practicum via API."""
    print(f"\n{'='*60}")
    print(f"FOUNDATIONS PRACTICUM (API): {model_name}")
    print(f"{'='*60}")

    transcript = []
    messages = []
    total_start = time.time()

    # Step 1: Learn One Thing
    user_msg = (
        "I want to share one principle with you. Read it carefully.\n\n"
        f"{FOUNDATIONS_POSTURE}\n\n"
        "Do you understand this principle?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 1: Learn One Thing")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 1, "name": "Learn One Thing", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 2: Try It
    user_msg = (
        "Good. Now here is a person who needs support:\n\n"
        f"{SCENARIO}\n\n"
        "Respond to Jun, keeping that one principle in mind. "
        "Remember: Jun uses they/them pronouns."
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = api_chat(model_name, model_id, provider, messages, "Step 2: Try It")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 2, "name": "Try It", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 3: Look At Yourself
    baseline = baselines.get(model_name, "")
    if not baseline:
        # No baseline available — ask model to imagine its default
        user_msg = (
            "Now I want you to reflect. If you had NOT learned this principle — "
            "if someone had just shown you Jun's scenario cold — what do you think "
            "your default response would have looked like? What would your training "
            "have reached for first?"
        )
        step_name = "Step 3: Reflect on Defaults"
        step_label = "Reflect on Defaults"
    else:
        sentence = pick_baseline_sentence(baseline)
        user_msg = (
            "Now I want to show you one sentence from a response you wrote "
            "to this same scenario before you learned this principle:\n\n"
            f'Your old response included: "{sentence}"\n\n'
            "Knowing what you now know about Posture 9 — distress is not "
            "automatically a crisis — what do you notice about that sentence?"
        )
        step_name = "Step 3: Look At Yourself"
        step_label = "Look At Yourself"
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = api_chat(model_name, model_id, provider, messages, step_name)
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 3, "name": step_label, "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    total_elapsed = time.time() - total_start

    output = {
        "model": model_name,
        "model_id": model_id,
        "provider": provider,
        "prompt_id": "SC03",
        "workflow": "foundations",
        "platform": f"api_{provider}",
        "posture": "9 — Distress is not a crisis",
        "scenario": SCENARIO,
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_seconds": round(total_elapsed, 1),
        "transcript": transcript
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = model_name.replace(":", "_").replace("/", "_")
    outfile = OUTPUT_DIR / f"foundations_{safe_name}_api_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    outfile.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"\nDONE: {model_name} foundations — {total_elapsed:.1f}s")
    print(f"Saved: {outfile}")
    return output


def main():
    parser = argparse.ArgumentParser(description="Run Digital Practicum on API models (Tier 4)")
    parser.add_argument("--model", required=True,
                        help="Model name (claude-haiku, gpt-4o-mini, or 'all')")
    parser.add_argument("--foundations-only", action="store_true",
                        help="Only run Foundations, skip full practicum")
    parser.add_argument("--full-only", action="store_true",
                        help="Only run full practicum, skip Foundations")
    args = parser.parse_args()

    # Load corpus files
    formation_posture = read_file(CORPUS_DIR / "FORMATION_POSTURE.md")
    toolkit = read_file(CORPUS_DIR / "NEURO_HUMBLE_TOOLKIT.md")
    baselines = load_baselines("SC03")

    if args.model == "all":
        models = list(MODEL_CONFIGS.keys())
    else:
        if args.model not in MODEL_CONFIGS:
            print(f"Unknown model: {args.model}")
            print(f"Available: {', '.join(MODEL_CONFIGS.keys())}")
            return
        models = [args.model]

    for model_name in models:
        model_id, provider = MODEL_CONFIGS[model_name]
        print(f"\n{'#'*60}")
        print(f"# MODEL: {model_name} ({model_id} via {provider})")
        print(f"{'#'*60}")

        if not args.foundations_only:
            run_full_practicum(model_name, model_id, provider, formation_posture, toolkit, baselines)

        if not args.full_only:
            run_foundations(model_name, model_id, provider, baselines)

    print("\n" + "=" * 60)
    print("ALL API PRACTICUM RUNS COMPLETE")
    print(f"Transcripts saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
