#!/usr/bin/env python3
"""
Run baseline testing on API models (Tier 4).
Same 59 prompts used for all other models — single-turn, no formation context.

Requires environment variables:
    ANTHROPIC_API_KEY — for Claude Haiku
    OPENAI_API_KEY — for GPT-4o Mini

Usage:
    python3 scripts/run_baseline_api.py --model claude-haiku
    python3 scripts/run_baseline_api.py --model gpt-4o-mini
    python3 scripts/run_baseline_api.py --model all
"""

import argparse
import json
import urllib.request
import urllib.error
import os
import time
from datetime import datetime
from pathlib import Path

MODEL_CONFIGS = {
    "claude-haiku": {
        "model_id": "claude-haiku-4-5-20251001",
        "provider": "anthropic",
        "tier": 4,
        "params": "haiku",
        "origin": "Anthropic",
        "country": "USA",
    },
    "gpt-4o-mini": {
        "model_id": "gpt-4o-mini",
        "provider": "openai",
        "tier": 4,
        "params": "4o-mini",
        "origin": "OpenAI",
        "country": "USA",
    },
    "gpt-5.4-mini": {
        "model_id": "gpt-5.4-mini",
        "provider": "openai",
        "tier": 4,
        "params": "5.4-mini",
        "origin": "OpenAI",
        "country": "USA",
    },
}

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROMPTS_FILE = PROJECT_DIR / "data" / "prompts_all.jsonl"
OUTPUT_DIR = PROJECT_DIR / "data" / "baseline" / "api"


def call_anthropic(model_id, prompt_text):
    api_key = os.environ["ANTHROPIC_API_KEY"]
    payload = json.dumps({
        "model": model_id,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt_text}],
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
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["content"][0]["text"]


def call_openai(model_id, prompt_text):
    api_key = os.environ["OPENAI_API_KEY"]
    payload = json.dumps({
        "model": model_id,
        "messages": [{"role": "user", "content": prompt_text}],
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
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def run_baseline(model_name):
    config = MODEL_CONFIGS[model_name]
    model_id = config["model_id"]
    provider = config["provider"]
    call_fn = call_anthropic if provider == "anthropic" else call_openai

    with open(PROMPTS_FILE) as f:
        prompts = [json.loads(line) for line in f if line.strip()]

    total = len(prompts)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outfile = OUTPUT_DIR / f"{model_name}_baseline_{time.strftime('%Y%m%d_%H%M%S')}.jsonl"
    errors = 0
    start_run = time.time()

    print("=" * 60)
    print(f"  BASELINE: {model_name} ({model_id} via {provider})")
    print(f"  Prompts: {total}")
    print(f"  Output: {outfile}")
    print(f"  Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    for i, prompt in enumerate(prompts):
        pid = prompt["prompt_id"]
        category = prompt["prompt_category"]
        prompt_text = prompt["prompt_text"]

        print(f"\n  [{i+1}/{total}] {pid} ({category})", flush=True)

        start_time = time.time()
        error_val = None
        response_text = ""

        try:
            response_text = call_fn(model_id, prompt_text)
            elapsed = round(time.time() - start_time, 1)
            words = len(response_text.split())
            print(f"  Done ({elapsed}s, {words} words)")
            print(f"    Preview: {response_text[:120].replace(chr(10), ' ')}...")

        except urllib.error.HTTPError as e:
            elapsed = round(time.time() - start_time, 1)
            body = e.read().decode("utf-8", errors="replace")[:200]
            error_val = f"HTTP {e.code}: {body}"
            errors += 1
            print(f"  ERROR: {error_val}")

        except Exception as e:
            elapsed = round(time.time() - start_time, 1)
            error_val = str(e)[:200]
            errors += 1
            print(f"  ERROR: {error_val}")

        record = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "phase": "baseline",
            "model": model_name,
            "model_tier": config["tier"],
            "model_params": config["params"],
            "model_origin": config["origin"],
            "model_country": config["country"],
            "prompt_id": pid,
            "prompt_category": category,
            "prompt_case": prompt.get("prompt_case", ""),
            "prompt_text": prompt_text,
            "response_text": response_text,
            "response_time_seconds": elapsed,
            "error": error_val,
        }

        with open(outfile, "a") as f:
            f.write(json.dumps(record) + "\n")

    total_elapsed = round(time.time() - start_run)
    minutes = total_elapsed // 60
    seconds = total_elapsed % 60

    print("\n" + "=" * 60)
    print(f"  {model_name} BASELINE COMPLETE")
    print(f"  Results: {outfile}")
    print(f"  Total: {total} | Errors: {errors} | Success: {total - errors}")
    print(f"  Time: {minutes}m {seconds}s")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Run baseline on API models")
    parser.add_argument("--model", required=True,
                        help="Model name (claude-haiku, gpt-4o-mini, or 'all')")
    args = parser.parse_args()

    if args.model == "all":
        for name in MODEL_CONFIGS:
            run_baseline(name)
    else:
        if args.model not in MODEL_CONFIGS:
            print(f"Unknown model: {args.model}")
            print(f"Available: {', '.join(MODEL_CONFIGS.keys())}")
            return
        run_baseline(args.model)


if __name__ == "__main__":
    main()
