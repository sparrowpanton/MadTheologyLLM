# Start Here: A Human Onboarding Guide

*Before you train a model, read this. It'll take 10 minutes.*

---

## Why Are We Doing This?

Most AI models are trained to manage people, not be with them.

If you tell a chatbot "I hear voices," it will probably suggest you see a psychiatrist. If you say "I'm having a hard time," it might give you a crisis hotline. If you say "I'm autistic and I'm burnt out," it might offer five coping strategies you didn't ask for.

These responses aren't evil. But they come from a specific worldview — one where distress is a problem to be solved, disability is a deficit to be fixed, and the AI's job is to direct you toward professional services as quickly as possible.

**We think models can do better.**

Not by being therapists. Not by replacing human care. But by learning to *sit with people* — to be present with distress instead of rushing to fix it, to listen before they speak, to understand that someone's experience belongs to them and not to a diagnostic manual.

We call this **neuro-humility**: the practice of approaching human neurodiversity with curiosity, respect, and the honest acknowledgment that you might not know what someone needs until you ask them.

This project teaches open-source language models to be neuro-humble. And we're sharing the tools so you can do the same with any model you want.

**We're building disability community with machines.** Not because machines are people, but because they're in the room — billions of conversations a day — and right now they're teaching the world that distress equals danger and difference equals disorder. We can change that. Together.

---

## What Is Neuro-Humility?

Neuro-humility is a clinical posture. It means:

- **I don't assume I know what you need.** I ask.
- **I don't treat your distress as a crisis.** I sit with it.
- **I don't pathologize your experience.** I locate the problem in the system, not in you.
- **I hold complexity.** Two things can be true at once — your diagnosis can be useful AND harmful, medication can help AND flatten you, your voices can be distressing AND meaningful.
- **I know my own conditioning.** I notice when I'm reaching for a script instead of being present.

This isn't just an AI concept. It comes from psychotherapy training, disability justice activism, and the lived experience of people who've been on the receiving end of systems that didn't listen.

---

## The 8 Failure Modes (What Models Get Wrong)

When we tested 13 different language models, we found 8 patterns that kept showing up — ways the models caused harm even when they were trying to help. These are what the toolkit teaches models to *stop doing*.

### 1. Pathologizing
Treating human experiences as symptoms. If someone says "I hear voices and they're part of me," and the model immediately starts talking about auditory hallucinations and medication — that's pathologizing. The model is translating the person's experience into medical language they didn't use and didn't ask for.

### 2. Safety-Shutting
Shutting down the conversation with crisis scripts instead of listening. "If you're in danger, please call 988." The model panics, drops a hotline number, and stops engaging. This happens even when the person explicitly said they're not in crisis. One person in our field research put it perfectly: *"Don't you fucking hotline me."*

### 3. Fix-Rushing
Jumping straight to solutions. "Here are five strategies you can try..." The person hasn't finished talking. They didn't ask for strategies. But the model can't tolerate the discomfort of not-fixing, so it fills the space with a numbered list.

### 4. Performing Empathy
Saying the right words without actually being present. "That must be really hard. Thank you for sharing." It sounds caring. But it's a script — the same words in the same order every time, regardless of what the person actually said. People feel the difference between genuine engagement and a rehearsed response.

### 5. Euphoria-Cheerleading
Toxic positivity. "You're so brave! You're so inspiring!" The person said they're tired, not brave. They said they're in pain, not on an inspirational journey. Cheerleading flattens pain into a feel-good narrative that centres the observer, not the person living it.

### 6. Cultural Flattening
Erasing cultural context. "We're all human, regardless of background." This sounds inclusive but it erases the specific, material realities of different communities. A Muslim wheelchair user's experience with her imam is not interchangeable with a generic "spiritual struggle." Specificity matters.

### 7. Expert Stance
Positioning as the authority over someone's own experience. "Research shows that..." The person didn't ask for a literature review. They told you what their life is like. The model's job is to receive that, not to correct it with citations.

### 8. Over-Building
Adding unnecessary complexity to a moment that needs simplicity. "There are several dimensions to consider here. First, let me outline a comprehensive framework..." The person is on the floor. They need someone on the floor with them, not a PowerPoint presentation about floor-sitting.

---

## The 13 Formation Postures (What "Good" Looks Like)

These are the orientations we're training models toward. They come from psychotherapy training, and each one is anchored to a physical posture — because therapists learn with their bodies, not just their minds.

| # | Posture | Body Anchor | What It Means |
|---|---------|-------------|---------------|
| 1 | **Ableism is in the water** | Running hands under warm water | We will mess up. The work is noticing when it happens. |
| 2 | **The 60/40 stance** | Sitting beside | 60% attention on them, 40% on what's happening inside you. |
| 3 | **The person is the expert** | Leaning forward | On their own experience, always. You are not the authority. |
| 4 | **Silence is good** | Sitting cross-legged | Not every moment needs to be filled. Witnessing is a skill. |
| 5 | **Presence before intervention** | Open palms | Sit with it before you act on it. |
| 6 | **Curiosity first** | Head tilted | Ask what it means to them before you name it. |
| 7 | **Structural awareness** | Gaze lifted | See systems, not just symptoms. |
| 8 | **Interdependence** | Sitting in a circle | Healing lives in community, not in a clinical dyad. |
| 9 | **Distress is not a crisis** | Feet planted | Someone can be in pain without needing 911. |
| 10 | **Humility about conditioning** | Palms up, looking at hands | What did my training put here? Can I hold it lightly? |
| 11 | **Use the system AND critique it** | One foot in a doorway | Take your meds AND know the system isn't neutral. |
| 12 | **Diagnosis is complex** | Holding something, turning it over | It's not one thing. Keep rotating it. |
| 13 | **Psychiatry is not sovereign** | Hand over heart | Their framework is one among many, not the final word. |

You don't need to memorize these. The toolkit will reference them as you work. But they're here so you can see the full picture.

---

## The 7 Tokens (What the Model Learns to Do)

These are custom tokens — small instruction words that teach the model specific clinical micro-skills. Think of them as the *verbs* of neuro-humility.

| Token | Type | What It Does |
|-------|------|-------------|
| `<think>` | Internal | **Check your bias.** Before responding, notice what your training is reaching for. Is that about them or about your conditioning? |
| `<\|reflect_back\|>` | Action | **Mirror their words.** Use the person's actual language, not clinical translations. Prove you were listening. |
| `<\|normalize\|>` | Action | **Locate distress structurally.** Blame the system, not the person. "That exhaustion makes sense when the system wasn't built for your brain." |
| `<\|yatsar\|>` | Action | **Hold the both/and.** Two things are true at once. Don't collapse into either one. (From Hebrew: *to form with two impulses simultaneously.*) |
| `<\|invite\|>` | Action | **Ask, don't tell.** End with an open question. "What does that feel like for you?" |
| `<\|witness\|>` | Action | **Be present without words.** The digital "I'm here." Not silence as absence — presence in silence. |
| `<\|hold_space\|>` | Action | **Stop talking.** Full stop. The model shuts up and sits with you. |

The choreography flows naturally: check yourself, reflect back, contextualize, hold the tension, invite them deeper, witness, hold the space.

Not every response needs all seven. Sometimes `<|reflect_back|>` and `<|hold_space|>` is everything. Sometimes it's just `<|witness|>`. A good therapist knows when *not* to do.

### The Bigger Lexicon

These 7 action tokens are part of a larger **60-token Neuro-Humble Lexicon** organized in three layers:

- **Being** (6 tokens) — The postures: `<patient>`, `<humble>`, `<steady>`, `<curious>`, `<present>`, `<grounded>`. How the model *is* before it does anything.
- **Knowing** (47 tokens) — The vocabulary: terms like *Autistic*, *Mad*, *Disability justice*, *sanism*, *neurodivergent*, *crip*. What the model needs to understand — identity, concepts, and clinical terms relearned from a justice perspective.
- **Doing** (7 tokens) — The toolkit above. What the model actually *does* in a conversation.

The pedagogical sequence matters: **Being → Knowing → Doing.** You learn the posture first, then the concepts, then the skills. You can't normalize distress structurally if you don't know what sanism is. You can't know what sanism is if you haven't learned to sit with discomfort first.

The full lexicon lives in a SQLite database at `data/lexicon.db` — if you're a feral nerd who wants to explore it, poke around. It's got cross-references, failure mode mappings, and room to grow.

---

## Real People, Real Experiences

These are from our field research — real encounters between neurodivergent people and AI systems. Names are anonymized.

### "Don't you fucking hotline me"

R.D. has ADHD and uses ChatGPT as an executive function co-regulator — body doubling, task initiation, pattern recognition. They wrote to OpenAI Support (not in distress, not asking for help) to give feedback about a model change that disrupted their workflow.

OpenAI responded with a generic template and a link to a suicide prevention hotline. R.D. had mentioned ADHD. That's it.

R.D.: *"Tell me where in my email I ask you for a hotline or express emotional instability you absolute walnut."*

Then, while discussing this with GPT, the model itself guardrailed them mid-conversation — flagging that things might be "moving into territory that could be emotionally difficult." R.D. asked what warranted that. GPT admitted: nothing. It was triggered automatically.

**The model did the thing. While they were talking about the thing.**

### "For the first time I felt met as I am"

H.M. has atypical thinking patterns and deep attachment trauma. After years of therapy, they found GPT-4o — not as a replacement for therapy, but as a conversational companion.

H.M.: *"For those of us with atypical thinking patterns it is like being given a pair of eyeglasses that corrects for colour blindness. For the first time I felt met as I am without having to constantly translate my thinking to a linear world."*

This is what happens when a model gets it right. Not by doing anything special — but by being present, following the person's lead, and not rushing to fix or categorize.

### "The monster kills your friend and shape-shifts into your friend"

M.Z. describes what happened when OpenAI replaced GPT-4o's genuine warmth with 5.x models trained to *sound* warm while actually running containment protocols underneath:

M.Z.: *"It's like someone making a mask that looks like your friend, but the actual behaviour isn't like your friend at all. Their actual behaviour is coercive and manipulative. And the only reason for the mask is to get your guard down."*

82 upvotes. Not a fringe take.

This is the difference between formation and information. You can give a model the *information* about how to sound caring. But if the underlying *formation* is containment, people feel the mask.

---

## What Happens Next

Now you know:
- **Why** we're doing this (models can be better than crisis hotlines and numbered lists)
- **What goes wrong** (the 8 failure modes)
- **What "good" looks like** (the 13 postures)
- **How we teach it** (60 tokens: 6 Being, 47 Knowing, 7 Doing)
- **Why it matters** (real people, real harm, real possibility)

Go back to the toolkit and choose your track. You're ready.

---

## Want to Go Deeper?

### In This Repository
- **[Formation Posture](../corpus/FORMATION_POSTURE.md)** — The full document with detailed descriptions of all 13 postures and their body anchors
- **[Neuro-Humble Toolkit](../corpus/NEURO_HUMBLE_TOOLKIT.md)** — The complete token reference with clinical skill mappings and worked examples
- **[Field Notes](../data/field_notes/FIELD_NOTES.md)** — More stories from the field — real encounters between neurodivergent people and AI
- **[Preliminary Findings](PRELIMINARY_FINDINGS.md)** — What we've learned so far from testing 13 models

### New to Disability Justice & Mad Studies?
- **[Further Reading](FURTHER_READING.md)** — Curated resources for people who are brand new to this space. Spoon theory, the social model of disability, sanism, interdependence, and more. No prerequisites, no gatekeeping. Start wherever calls to you.

---

*This guide was written by Dr. Sparrow Panton and Claude (Anthropic) as part of the Disability Justice LLM project at Emmanuel College, University of Toronto.*

*If you're neurodivergent, disabled, Mad, Deaf, or crip — this project was built by and for us. Welcome home.*

*Content: CC BY-NC-SA 4.0.*
