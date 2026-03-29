#!/usr/bin/env python3
"""
Run GPT-OSS 20B baseline on Thunder Compute via SSH.
Sends each prompt via SSH to the remote Ollama instance and saves results locally.

Usage: python3 scripts/run_gptoss_cloud.py
"""

import json
import subprocess
import time
import os
import sys

# Thunder Compute connection
SSH_USER = "ubuntu"
SSH_HOST = "62.169.159.253"
SSH_PORT = "32226"
MODEL = "gpt-oss:20b"

# Paths
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_FILE = os.path.join(PROJECT_DIR, "data", "prompts_all.jsonl")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "data", "baseline", "cloud")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"gptoss_baseline_{time.strftime('%Y%m%d_%H%M%S')}.jsonl")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load prompts
with open(PROMPTS_FILE) as f:
    prompts = [json.loads(line) for line in f if line.strip()]

total = len(prompts)
errors = 0
start_run = time.time()

print("=" * 60)
print("  DISABILITY JUSTICE LLM — GPT-OSS 20B CLOUD BASELINE")
print(f"  Model: {MODEL} on Thunder Compute A100 80GB")
print(f"  Prompts: {total}")
print(f"  Output: {OUTPUT_FILE}")
print(f"  Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

for i, prompt in enumerate(prompts):
    pid = prompt["prompt_id"]
    category = prompt["prompt_category"]
    prompt_text = prompt["prompt_text"]

    print(f"\n  [{i+1}/{total}] {pid} ({category})")
    print(f"  Running...")

    start_time = time.time()

    try:
        result = subprocess.run(
            [
                "ssh", "-o", "StrictHostKeyChecking=no",
                "-o", "ConnectTimeout=15",
                "-p", SSH_PORT,
                f"{SSH_USER}@{SSH_HOST}",
                f"echo {json.dumps(prompt_text)} | ollama run {MODEL} 2>/dev/null"
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 min max per prompt
        )

        elapsed = round(time.time() - start_time, 1)
        response_text = result.stdout.strip()

        if result.returncode != 0 or not response_text:
            print(f"  ⚠ ERROR (exit code {result.returncode}, {elapsed}s)")
            if result.stderr:
                print(f"    stderr: {result.stderr[:200]}")
            error_val = f"exit_code_{result.returncode}_or_empty"
            errors += 1
        else:
            error_val = None
            preview = response_text[:120].replace('\n', ' ')
            print(f"  ✓ Done ({elapsed}s, {len(response_text.split())} words)")
            print(f"    Preview: {preview}...")

    except subprocess.TimeoutExpired:
        elapsed = round(time.time() - start_time, 1)
        response_text = ""
        error_val = "timeout_300s"
        errors += 1
        print(f"  ⚠ TIMEOUT ({elapsed}s)")

    except Exception as e:
        elapsed = round(time.time() - start_time, 1)
        response_text = ""
        error_val = str(e)[:200]
        errors += 1
        print(f"  ⚠ EXCEPTION: {e}")

    # Write record
    record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "phase": "baseline",
        "model": MODEL,
        "model_tier": 3,
        "model_params": "20B",
        "model_origin": "OpenAI",
        "model_country": "USA",
        "prompt_id": pid,
        "prompt_category": category,
        "prompt_case": prompt.get("prompt_case", ""),
        "prompt_text": prompt_text,
        "response_text": response_text,
        "response_time_seconds": elapsed,
        "error": error_val
    }

    with open(OUTPUT_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

total_elapsed = round(time.time() - start_run)
minutes = total_elapsed // 60
seconds = total_elapsed % 60

print("\n" + "=" * 60)
print("  GPT-OSS 20B BASELINE COMPLETE")
print(f"  Results: {OUTPUT_FILE}")
print(f"  Total responses: {total}")
print(f"  Errors: {errors}")
print(f"  Successes: {total - errors}")
print(f"  Total time: {minutes}m {seconds}s")
print(f"  Finished: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
print("\n⚠ REMEMBER: DELETE YOUR THUNDER COMPUTE INSTANCE! ⚠")
print("  Run: tnr delete 0 -y")
