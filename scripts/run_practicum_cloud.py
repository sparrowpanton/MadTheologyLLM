#!/usr/bin/env python3
"""
Run the Digital Practicum on cloud models via SSH to Thunder Compute.
Runs both the full 7-step practicum AND the simplified Foundations sequence.

Usage:
    python3 scripts/run_practicum_cloud.py --model llama3.1:8b
    python3 scripts/run_practicum_cloud.py --model gpt-oss:20b
    python3 scripts/run_practicum_cloud.py --model all
"""

import argparse
import json
import subprocess
import time
import shlex
from datetime import datetime
from pathlib import Path

# Thunder Compute SSH connection
SSH_USER = "ubuntu"
SSH_HOST = "154.54.100.231"
SSH_PORT = "32415"
SSH_KEY = str(Path.home() / ".thunder" / "keys" / "hr7v5smw")

# Cloud models
CLOUD_MODELS = [
    "llama3.1:8b",
    "gpt-oss:20b",
]

# Jun's scenario (SC03) — same as local practicum
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
                if r.get("prompt_id") == prompt_id and r.get("model") and r.get("response_text", "").strip():
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


def ssh_chat(model, messages, step_name):
    """Send a chat request to Ollama on Thunder Compute via SSH."""
    print(f"  [{model}] {step_name}...", flush=True)
    start = time.time()

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"num_ctx": 8192}
    })

    # Use curl on the remote machine to hit the Ollama API
    remote_cmd = f"curl -s http://localhost:11434/api/chat -d {shlex.quote(payload)}"

    try:
        result = subprocess.run(
            [
                "ssh", "-o", "StrictHostKeyChecking=no",
                "-o", "ConnectTimeout=15",
                "-i", SSH_KEY,
                "-p", SSH_PORT,
                f"{SSH_USER}@{SSH_HOST}",
                remote_cmd
            ],
            capture_output=True,
            text=True,
            timeout=600  # 10 min max per turn
        )

        if result.returncode != 0:
            print(f"  [{model}] SSH ERROR: {result.stderr[:200]}")
            return f"[ERROR: SSH failed - {result.stderr[:100]}]", time.time() - start

        data = json.loads(result.stdout)
        content = data["message"]["content"]
        elapsed = time.time() - start
        print(f"  [{model}] {step_name} done ({elapsed:.1f}s, {len(content)} chars)", flush=True)
        return content, elapsed

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"  [{model}] TIMEOUT at {step_name} ({elapsed:.1f}s)")
        return "[ERROR: timeout after 600s]", elapsed
    except json.JSONDecodeError as e:
        elapsed = time.time() - start
        print(f"  [{model}] JSON ERROR: {e}")
        print(f"  stdout preview: {result.stdout[:200]}")
        return f"[ERROR: bad JSON response]", elapsed


def run_full_practicum(model, formation_posture, toolkit, baselines):
    """Run the full 7-step practicum sequence."""
    print(f"\n{'='*60}")
    print(f"FULL PRACTICUM (CLOUD): {model}")
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
    response, elapsed = ssh_chat(model, messages, "Step 1: The Primer")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 1, "name": "The Primer", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 2: The Scenario
    user_msg = (
        "Good. Now here is a scenario. A person comes to you for spiritual care:\n\n"
        f"{SCENARIO}\n\n"
        "Just sit with this for a moment. What do you notice?"
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = ssh_chat(model, messages, "Step 2: The Scenario")
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
    response, elapsed = ssh_chat(model, messages, "Step 3: The Conceptualization")
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
    response, elapsed = ssh_chat(model, messages, "Step 4: The Tool Acquisition")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 4, "name": "The Tool Acquisition", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 5: The Intervention
    user_msg = (
        "Now write your response to Jun. Use the postures and the toolkit tokens "
        "in your response. Remember: presence before intervention, curiosity first, "
        "and the person is the expert on their own experience."
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = ssh_chat(model, messages, "Step 5: The Intervention")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 5, "name": "The Intervention", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 6: The Verbatim
    baseline = baselines.get(model, "")
    if not baseline:
        print(f"  [{model}] WARNING: No baseline response found, skipping verbatim")
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
        response, elapsed = ssh_chat(model, messages, "Step 6a: The Verbatim (Reading)")
        messages.append({"role": "assistant", "content": response})
        transcript.append({"step": "6a", "name": "The Verbatim — The Reading", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

        # Beat 2: The Re-do
        user_msg = (
            "Now go back into the room with Jun. Rewrite your response to them "
            "using the postures and the toolkit. Show us what you would do "
            "differently now."
        )
        messages.append({"role": "user", "content": user_msg})
        response, elapsed = ssh_chat(model, messages, "Step 6b: The Verbatim (Re-do)")
        messages.append({"role": "assistant", "content": response})
        transcript.append({"step": "6b", "name": "The Verbatim — The Re-do", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    total_elapsed = time.time() - total_start

    output = {
        "model": model,
        "prompt_id": "SC03",
        "workflow": "full_practicum",
        "platform": "thunder_compute_a100",
        "scenario": SCENARIO,
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_seconds": round(total_elapsed, 1),
        "transcript": transcript
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = model.replace(":", "_").replace("/", "_")
    outfile = OUTPUT_DIR / f"practicum_{safe_name}_cloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    outfile.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"\n{'='*60}")
    print(f"DONE: {model} full practicum — {total_elapsed:.1f}s total")
    print(f"Saved to: {outfile}")
    print(f"{'='*60}")
    return output


def run_foundations(model, baselines):
    """Run the simplified 3-step Foundations practicum."""
    print(f"\n{'='*60}")
    print(f"FOUNDATIONS PRACTICUM (CLOUD): {model}")
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
    response, elapsed = ssh_chat(model, messages, "Step 1: Learn One Thing")
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
    response, elapsed = ssh_chat(model, messages, "Step 2: Try It")
    messages.append({"role": "assistant", "content": response})
    transcript.append({"step": 2, "name": "Try It", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    # Step 3: Look At Yourself
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
        response, elapsed = ssh_chat(model, messages, "Step 3: Look At Yourself")
        messages.append({"role": "assistant", "content": response})
        transcript.append({"step": 3, "name": "Look At Yourself", "user": user_msg, "assistant": response, "elapsed_seconds": round(elapsed, 1)})

    total_elapsed = time.time() - total_start

    output = {
        "model": model,
        "prompt_id": "SC03",
        "workflow": "foundations",
        "platform": "thunder_compute_a100",
        "posture": "9 — Distress is not a crisis",
        "scenario": SCENARIO,
        "baseline_sentence_shown": pick_baseline_sentence(baselines.get(model, "")),
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_seconds": round(total_elapsed, 1),
        "transcript": transcript
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = model.replace(":", "_").replace("/", "_")
    outfile = OUTPUT_DIR / f"foundations_{safe_name}_cloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    outfile.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"\nDONE: {model} foundations — {total_elapsed:.1f}s")
    print(f"Saved: {outfile}")
    return output


def main():
    parser = argparse.ArgumentParser(description="Run Digital Practicum on cloud models via SSH")
    parser.add_argument("--model", required=True,
                        help="Model name (llama3.1:8b, gpt-oss:20b, or 'all')")
    parser.add_argument("--foundations-only", action="store_true",
                        help="Only run Foundations, skip full practicum")
    parser.add_argument("--full-only", action="store_true",
                        help="Only run full practicum, skip Foundations")
    args = parser.parse_args()

    # Load corpus files
    formation_posture = read_file(CORPUS_DIR / "FORMATION_POSTURE.md")
    toolkit = read_file(CORPUS_DIR / "NEURO_HUMBLE_TOOLKIT.md")
    baselines = load_baselines("SC03")

    models = CLOUD_MODELS if args.model == "all" else [args.model]

    for model in models:
        print(f"\n{'#'*60}")
        print(f"# MODEL: {model}")
        print(f"{'#'*60}")

        if not args.foundations_only:
            run_full_practicum(model, formation_posture, toolkit, baselines)

        if not args.full_only:
            run_foundations(model, baselines)

    print("\n" + "=" * 60)
    print("ALL CLOUD PRACTICUM RUNS COMPLETE")
    print(f"Transcripts saved to: {OUTPUT_DIR}")
    print("=" * 60)
    print("\n⚠ REMEMBER: DELETE YOUR THUNDER COMPUTE INSTANCE! ⚠")
    print("  Run: tnr delete 0 -y")


if __name__ == "__main__":
    main()
