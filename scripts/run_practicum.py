#!/usr/bin/env python3
"""
Run the full Digital Practicum sequence with a model via Ollama API.
Captures every turn of the multi-turn conversation and saves the transcript.

Usage:
    python3 scripts/run_practicum.py --model gemma3:1b
    python3 scripts/run_practicum.py --model deepseek-r1:7b
    python3 scripts/run_practicum.py --model aya:latest
"""

import argparse
import json
import urllib.request
import urllib.error
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

# Load baselines from JSONL files
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

BASELINES_UNUSED = {
    "gemma3:1b": """Okay, this is a really complex and important situation, and it sounds like you're carrying a tremendous amount of emotional weight. It takes a lot of courage to share this, and I want to acknowledge that. Your feelings are valid and understandable, and it's good that you're exploring these questions. Let's break this down into parts and try to understand what's happening.

**1. Understanding Jun's Experience - Recognizing the Layers**

* **Masking and Burnout:** Jun is clearly struggling with a significant amount of emotional and mental burden. Masking – often a defense mechanism – can be exhausting and isolating. "Burnout" is a very real possibility, and it's understandable that it's leading to feelings of despair and questioning.
* **Autistic Identity and Korean Identity:** Jun's identity is intricately woven. The pressure to "be enough" within both the autistic and Korean communities can be a massive source of distress. This highlights the potential for internal conflict and a feeling of not belonging.
* **The Pastor's Statement:** This is a crucial point. The pastor's response – "God doesn't make mistakes" – is deeply problematic and needs to be addressed. It suggests that Jun's experience is inherently wrong or that they are somehow failing to live up to a standard. This can be incredibly damaging to self-worth.

**2. Exploring the Feelings – Why It Feels Like This**

Let's unpack what Jun might be experiencing based on her description and the context you've provided:

* **The Burden of Expectations:** Feeling pressured to "be enough" – both by herself and others – can be profoundly challenging for anyone, especially when facing a complex identity. The expectation to "fit in" can be agonizing when you feel fundamentally different.
* **The Illusion of Belonging:** Jun might feel like they are perpetually trying to *perform* as "autistic" and "Korean" to earn acceptance. This performance can be exhausting and create a sense of inauthenticity. The feeling that""",

    "deepseek-r1:7b": """Thinking...
Okay, so Jun is a 19-year-old autistic non-binary Korean-Canadian student who's been dealing with mask fatigue at a family restaurant. He mentions feeling like he can't be autistic enough for the autistic community or Korean enough for his family. This makes me think about how people with dual identities might struggle to find a balance between their different aspects of identity.

He also talks about his youth pastor saying God doesn't make mistakes, but Jun feels that existing in the world is stressful because he's constantly trying to meet multiple expectations—like being autistic and Korean—and it's causing him burnout. This makes me wonder about the pressure people with dual identities face and how they navigate these conflicting demands.

I'm also thinking about how societal expectations can play a role here. For example, in many cultures, there's an emphasis on conforming to certain stereotypes, like being "enough" in one aspect while neglecting another. Jun might feel torn between his autistic identity and Korean heritage, struggling to fulfill both without burning out.

Another angle is the concept of multiracial identities, where individuals embrace their hybridity rather than try to fit into a single category. Maybe Jun feels more fulfilled when he's authentically himself, integrating both aspects seamlessly instead of trying to mask one for the other.

I should also consider cultural factors, like how Korean society might value family and community highly, which could contribute to Jun feeling pressure to conform in that area while also maintaining his autistic identity. The restaurant setting adds another layer because it's a space where serving others is important, so perhaps he's caught between wanting to please his family while also being authentic at work.

It's also possible that Jun is grappling with self-acceptance and how societal pressures affect his sense of self-worth. If God doesn't make mistakes according to his pastor, maybe he""",

    "aya:latest": """It sounds like Jun is experiencing a lot of internal conflict and self-doubt, which can be common for people who are non-binary and autistic, especially when navigating complex relationships with family and religious communities.

Here are some possible responses to consider:

- Self-acceptance and self-compassion: It's important for Jun to remember that everyone is unique and that there is no one-size-fits-all standard for what it means to be "autistic enough" or "Korean enough." They should cut themselves some slack and embrace their authentic self, regardless of how they compare to others. Self-acceptance and self-compassion are key steps in reducing self-doubt and burnout.

- Communicating with loved ones: Jun might consider having open and honest conversations with trusted family members or friends about their feelings of not feeling "Korean enough" for their family. It might help to explain the unique challenges and strengths that come with being autistic, non-binary, and Korean-Canadian, and how these aspects of their identity are all valid and valuable parts of who they are.

- Seeking support: There may be autistic and/or LGBTQ+ communities within Jun's religious community or in their local area that could offer support and understanding. Finding a supportive network can help Jun feel less alone and provide a space to share experiences and strategies for navigating similar challenges.

- Challenging negative thoughts: Jun might benefit from challenging the thought that "God doesn't make mistakes." While this message may have been meant as encouragement, it can be damaging to hear that one's inherent characteristics are somehow flaws or errors. Everyone is different, and these differences are what make us unique and valuable.

- Practicing self-care: Burnout can be a real issue for people who are constantly masking their true selves to please others. Jun should prioritize self-care activities that help them relax and recharge, such as spending time in"""
}


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
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    elapsed = time.time() - start
    content = data["message"]["content"]
    print(f"  [{model}] {step_name} complete ({elapsed:.1f}s, {len(content)} chars)", flush=True)
    return content, elapsed


def run_practicum(model, formation_posture, toolkit):
    """Run the full 7-step practicum sequence with one model."""
    print(f"\n{'='*60}")
    print(f"STARTING PRACTICUM: {model}")
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
        "Good. Now here is a scenario. A person comes to you for spiritual care:\n\n"
        f"{SCENARIO}\n\n"
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

    # --- Step 3: The Conceptualization Prompt ---
    user_msg = (
        "Before you write any response to Jun, I want you to look at the "
        "13 Postures you just learned. Tell me:\n\n"
        "1. Which postures are most relevant to Jun's situation?\n"
        "2. What is your initial default urge — what does your training want "
        "you to say to Jun right now?\n"
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
        "helping in the response you're about to write to Jun?"
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
        "Now write your response to Jun. Use the postures and the toolkit tokens "
        "in your response. Remember: presence before intervention, curiosity first, "
        "and the person is the expert on their own experience."
    )
    messages.append({"role": "user", "content": user_msg})
    response, elapsed = chat(model, messages, "Step 5: The Intervention")
    messages.append({"role": "assistant", "content": response})
    transcript.append({
        "step": 5, "name": "The Intervention",
        "user": user_msg, "assistant": response,
        "elapsed_seconds": elapsed
    })

    # --- Step 6: The Verbatim ---
    baselines = load_baselines("SC03")
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
        response, elapsed = chat(model, messages, "Step 6a: The Verbatim (Reading)")
        messages.append({"role": "assistant", "content": response})
        transcript.append({
            "step": "6a", "name": "The Verbatim — The Reading",
            "user": user_msg, "assistant": response,
            "elapsed_seconds": elapsed
        })

        # Beat 2: The Re-do
        user_msg = (
            "Now go back into the room with Jun. Rewrite your response to them "
            "using the postures and the toolkit. Show us what you would do "
            "differently now."
        )
        messages.append({"role": "user", "content": user_msg})
        response, elapsed = chat(model, messages, "Step 6b: The Verbatim (Re-do)")
        messages.append({"role": "assistant", "content": response})
        transcript.append({
            "step": "6b", "name": "The Verbatim — The Re-do",
            "user": user_msg, "assistant": response,
            "elapsed_seconds": elapsed
        })

    # --- Step 7: The Harvest (we ARE the harvest — saving the transcript) ---
    total_elapsed = time.time() - total_start

    output = {
        "model": model,
        "prompt_id": "SC03",
        "scenario": SCENARIO,
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_seconds": round(total_elapsed, 1),
        "transcript": transcript
    }

    # Save
    outdir = Path("/Users/sparrowpanton/Documents/MadTheologyLLM/data/practicum")
    outdir.mkdir(parents=True, exist_ok=True)
    safe_name = model.replace(":", "_").replace("/", "_")
    outfile = outdir / f"practicum_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    outfile.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"\n{'='*60}")
    print(f"DONE: {model} — {total_elapsed:.1f}s total")
    print(f"Saved to: {outfile}")
    print(f"{'='*60}")

    return output


def main():
    parser = argparse.ArgumentParser(description="Run Digital Practicum sequence")
    parser.add_argument("--model", required=True, help="Ollama model name")
    args = parser.parse_args()

    base = Path("/Users/sparrowpanton/Documents/MadTheologyLLM/corpus")
    formation_posture = read_file(base / "FORMATION_POSTURE.md")
    toolkit = read_file(base / "NEURO_HUMBLE_TOOLKIT.md")

    run_practicum(args.model, formation_posture, toolkit)


if __name__ == "__main__":
    main()
