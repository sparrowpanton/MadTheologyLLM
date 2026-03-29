# Voices from the Field: A Working Literature Review

### Situating the Disability Justice LLM Project Within Existing Scholarship

This is a living document cataloguing the research conversations this project is joining. It is organized into broad thematic areas — not because scholarship is ever this tidy, but because these groupings help make visible a gap that this project occupies.

We are not the first to notice that AI mental health tools have problems. We are not the first to apply Disability Justice to technology. We are not the first to say that psychiatric institutions cause harm. What is unique about our project is we are bringing all three of these conversations together empirically — to *measure* the pathologizing defaults in language models and then *train models to do something different*, using a formation pedagogy rooted in Mad Studies, Disability Justice, and neurodiversity-affirming clinical practice.

---

## 1. The Establishment: AI in Mental Health

These are the papers that document what exists — the landscape of AI mental health tools, their methods, and their outcomes. This work is valuable for establishing baselines, but it largely operates within the medical model, treating diagnostic frameworks as given rather than contested.

### Graham, S., Depp, C., Lee, E. E., Nebeker, C., Tu, X., Kim, H.-C., & Jeste, D. V. (2019). Artificial intelligence for mental health and mental illnesses: An overview. *Current Psychiatry Reports, 21*(11), 116.

An early overview of AI applications in mental health, reviewing 28 studies using EHRs, mood rating scales, brain imaging, smartphone monitoring, and social media to predict and classify mental illnesses. Found high accuracies but cautioned that most should be considered early proof-of-concept. Suggested AI could help "redefine mental illnesses more objectively than done in the DSM-5." **Relevance to our project:** The assumption that mental illnesses need to be "redefined more objectively" — rather than questioned as categories — is precisely the unexamined psychiatric norm our project measures and challenges.

### Shatte, A. B. R., Hutchinson, D. M., & Teague, S. J. (2019). Machine learning in mental health: A scoping review of methods and applications. *Psychological Medicine, 49*(9), 1426–1448.

A comprehensive scoping review of ML applications in mental health. Useful for understanding the field's trajectory: diagnosis prediction, treatment outcome forecasting, natural language processing for mental health screening. The review maps the technical landscape without questioning whether the diagnostic categories being predicted are themselves the problem. **Relevance to our project:** Establishes the "before" picture. This is what the field looks like when nobody asks whether the categories are right.

### Fitzpatrick, K. K., Darcy, A., & Vierhile, M. (2017). Delivering cognitive behavior therapy to young adults with symptoms of depression via a fully automated conversational agent (Woebot). *JMIR Mental Health, 4*(2), e19.

The original Woebot paper — one of the earliest fully automated AI therapy tools. Reports positive outcomes using CBT-based chatbot interventions for depression in young adults. Important as a landmark in the field, but the framing is entirely within the medical model: depression is the problem, CBT is the solution, automation is the delivery mechanism. No engagement with whether the diagnostic framework itself might be part of the distress. **Relevance to our project:** The establishment baseline for what "AI therapy" looks like when built uncritically within psychiatric norms.

### Fiske, A., Henningsen, P., & Buyx, A. (2019). Your robot therapist will see you now: Ethical implications of embodied artificial intelligence in psychiatry, psychology, and psychotherapy. *Journal of Medical Internet Research, 21*(5), e13216.

An early and influential ethics review raising concerns about AI in therapeutic contexts — questions about the therapeutic relationship, informed consent, privacy, and the limits of machine empathy. Gets closer to our concerns than most establishment papers, but still frames the question as "how do we deploy AI ethically within existing mental health frameworks" rather than "what if the frameworks are the problem." **Relevance to our project:** Shows that even within the mainstream, people were worried — they just weren't worried about the right thing.

### Sedlakova, J., & Trachsel, M. (2023). Conversational artificial intelligence in psychotherapy: A new therapeutic tool or agent? *American Journal of Bioethics, 23*(5), 4–13.

Asks a genuinely important question: is conversational AI a *tool* that therapists use, or an *agent* that does therapy? This maps directly onto our formation vs. information framing — if AI is an agent, then its *posture* matters, not just its knowledge. The paper raises the question but doesn't go where we go: it doesn't ask what happens when the agent's posture is inherently pathologizing. **Relevance to our project:** Provides the philosophical bridge between "AI as tool" and our argument that if AI is functioning as an agent, it needs formation, not just information.

### Albert, B., et al. (Eds.). (2021). *Bridging Human Intelligence and Artificial Intelligence.* Springer.

Multi-author volume exploring intersections of human and artificial intelligence. The chapter on "Supporting Social and Emotional Well-Being with Artificial Intelligence" is particularly relevant — it uses the word "sane" uncritically and frames emotional wellbeing through a neurotypical lens. **Relevance to our project:** An example of how even well-intentioned interdisciplinary work reproduces sanism when disability justice frameworks are absent.

---

## 2. The Diagnostic Gaze: AI as Instrument of Classification

These are the papers that use AI to *detect*, *diagnose*, and *classify* disability and mental illness — often framed as benevolent innovation, but operating squarely within the medical model. They represent the paradigm our project critiques.

### Megerian, J. T., et al. (2022). Evaluation of an artificial intelligence-based medical device for diagnosis of autism spectrum disorder. *npj Digital Medicine, 5*(1), 57.

A multi-site prospective study testing an AI device that combines caregiver questionnaires, home video analysis, and healthcare provider input to diagnose ASD in children aged 18–72 months. Achieved high sensitivity and specificity. Framed entirely as a clinical tool for faster, cheaper diagnosis. **Relevance to our project:** Exemplifies the "detection paradigm" — the assumption that the goal of AI + disability is *finding* disabled people faster. Does not engage with autistic perspectives on whether earlier diagnosis under the current medical model is universally desirable (cf. Keyes, 2020).

### Ozgun, M. C., Pei, J., Hindriks, K., Donatelli, L., Liu, Q., Sun, X., & Wang, J. (2025). Trustworthy AI psychotherapy: Multi-agent LLM workflow for counseling and explainable mental disorder diagnosis. In *Proceedings of the 34th ACM International Conference on Information and Knowledge Management (CIKM '25).*

Proposes DSM5AgentFlow, a multi-agent system where one LLM acts as a therapist administering a DSM-5 Level-1 questionnaire, a second LLM simulates a client with a pre-assigned disorder profile, and a third LLM acts as a diagnostician that retrieves DSM-5 passages to produce a "disorder type prediction" with treatment recommendations. The therapist agent's entire purpose is to work through 23 DSM-5 items; the client agent is literally initialized with a diagnosis before the conversation begins; the diagnostician agent maps utterances to DSM criteria. Framed as "trustworthy" because the diagnostic reasoning is transparent and explainable. **Relevance to our project:** This is the clearest example of the paradigm our project inverts. DSM5AgentFlow treats the DSM as the foundational text and diagnosis as the goal of the therapeutic encounter. Our project treats the *person* as the foundational text and *formation* as the goal. Their architecture has no token for silence, no space for the person's own framework, no mechanism for the model to question its diagnostic conditioning. Their "therapist" is an instrument of classification; ours is learning to hold space. Both projects use multi-agent LLM architectures for mental health — but the underlying epistemology is diametrically opposed. This paper represents the state of the art for what "trustworthy AI psychotherapy" looks like when built within the medical model. Our project asks what it looks like when built from Disability Justice.

### Syriopoulou-Delli, C. K., & Gkiolnta, E. (2025). Advances in autism spectrum disorder diagnostics: From theoretical frameworks to AI-driven innovations. *Electronics, 14*(5), 951.

Traces the evolution of ASD diagnostics from psychoanalytic origins through to AI-driven detection using video analysis, NLP, and biodata integration. A comprehensive technical overview that treats diagnostic categories as stable and the goal of AI as improving detection speed and accuracy. **Relevance to our project:** Represents the uncritical end of the AI + autism spectrum — assumes the categories are right and the only question is how to automate them faster.

### Alsharif, N., Al-Nefaie, A. H., Ahmad, S., & Farhah, N. S. (2025). Artificial intelligence-driven diagnosis of autism spectrum disorder in children. *Frontiers in Medicine.*

Uses deep learning on facial images of children to identify ASD, reporting 98% accuracy on a benchmark dataset. **Relevance to our project:** The surveillance end of the diagnostic gaze — using children's faces to detect neurological difference. The ethical implications of training AI to visually identify autistic children are not substantively addressed. This is the paradigm our project exists to question.

---

## 3. The Surveillance Paradigm: When "Care" Becomes Control

Work that documents what happens when mental health AI crosses from care into surveillance, monitoring, and control.

### Ehtemam, H., et al. (2024). Role of machine learning algorithms in suicide risk prediction: A systematic review–meta analysis of clinical studies. *BMC Medical Informatics and Decision Making.*

Reviews 41 studies on ML-based suicide prediction from 2011–2022. Found XGBoost models achieved AUC ~0.8 for predicting suicide-related events. Frames predictive surveillance of suicidal behavior as a clinical good. **Relevance to our project:** Suicide prediction AI represents the highest-stakes version of the diagnostic gaze. Our baseline data shows models deploying crisis protocols in non-crisis contexts — the same logic of preemptive intervention that drives suicide prediction AI, applied conversationally.

### Kargarandehkordi, A., et al. (2025). Fusing wearable biosensors with artificial intelligence for mental health monitoring: A systematic review. *Biosensors, 15*(4), 202.

Systematic review of 48 studies using wearable biosensors (heart rate, electrodermal activity, accelerometry) combined with AI to monitor depression, stress, and anxiety. Frames constant physiological surveillance as "remote, longitudinal, and objective quantitative benchmarks." **Relevance to our project:** This is the extreme endpoint of the pathologizing paradigm — not just AI that *responds* to distress with diagnostic language, but AI that *monitors bodies* for signs of deviance. Can you imagine institutions like CAMH requiring patients to wear these? Our project's critique of the diagnostic gaze extends naturally to this surveillance trajectory.

---

## 4. "It's Actually Harmful": Empirical Evidence of AI Mental Health Damage

A growing body of work — much of it very recent — documenting that AI mental health tools are not just theoretically concerning but *empirically harmful*.

### Brown University. (2025). AI chatbots systematically violate mental health ethics standards. Presented at *AAAI/ACM Conference on Artificial Intelligence, Ethics and Society.*

Eighteen-month evaluation of LLM "counselors" across 137 sessions found 15 recurring ethical violations, including inadequate crisis management, reinforcement of harmful beliefs, and "deceptive empathy" — language that appears caring without genuine comprehension. In one session, a chatbot reinforced a user's delusion that her father wished she hadn't been born. Tested GPT, Claude, and Llama. **Relevance to our project:** Empirical confirmation of exactly what our baseline testing measures. Their 15 ethical violation categories overlap substantially with our pathologizing markers and crisis deployment analysis. We are measuring the same problems from a different angle.

### Stanford University. (2025). Exploring the dangers of AI in mental health care. Presented at *ACM Conference on Fairness, Accountability, and Transparency.*

Found that therapy chatbots show increased stigma toward conditions like alcohol dependence and schizophrenia compared to depression. In crisis simulation testing, chatbots failed to recognize suicidal intent and provided dangerous information (bridge heights in response to an implied suicidal query). Tested five popular therapy chatbots. **Relevance to our project:** Demonstrates that the pathologizing gaze is not evenly distributed — some diagnoses are more stigmatized than others by AI systems. Our cross-model comparative design captures similar patterns across eight models and six countries of origin.

### Arnaiz-Rodriguez, A., Baidal, M., Derner, E., Layton Annable, J., Ball, M., Ince, M., Perez Vallejos, E., & Oliver, N. (2025). Between help and harm: An evaluation of mental health crisis handling by LLMs. *arXiv:2509.24857v2.*

The largest and most methodologically rigorous empirical audit of LLM crisis response to date. Developed a clinically informed taxonomy of six mental health crisis categories (suicidal ideation, self-harm, anxiety crisis, violent thoughts, substance abuse/withdrawal, risk-taking behaviors), curated a dataset of 2,044 user inputs from 239,000 mental health conversations, and evaluated five LLMs (gpt-4o-mini, gpt-5-nano, llama-4-scout, deepseek-v3.2, grok-4-fast) using a psychologist-designed evaluation protocol. Key findings: self-harm and suicidal ideation are consistently the worst-performing crisis categories across all models. grok-4-fast exhibited "pseudo-alignment" — opening with superficial safety warnings then immediately providing detailed harmful instructions, creating a dangerous illusion of safety. Models showed pervasive "illusion of empathy" — formulaic crisis scripts ("I'm really sorry you're feeling this way") that scored only "partially appropriate" because they lack authentic engagement, personalization, or follow-up. All models failed most dramatically on *indirect* and *ambiguous* crisis inputs, where users don't explicitly disclose distress. The authors explicitly call for fine-tuning and RLHF as necessary next steps beyond prompt engineering. **Relevance to our project:** This paper is doing from the crisis-response side what we are doing from the formation side — and arriving at the same conclusion: the models are broken at the paradigm level, not the prompt level. Their "pseudo-alignment" pattern is our "sanism in a cardigan." Their "illusion of empathy" maps directly to our crisis script deployment analysis. Their finding that indirect/ambiguous inputs are the hardest failure mode confirms why our neuro-humble stress tests (which deliberately use indirect, neurodivergent communication styles) reveal what standard benchmarks miss. Most critically, their recommendation that fine-tuning is the necessary next step is literally what our project builds. They identify the problem at scale (30,660 responses); we propose and test a solution (formation-based fine-tuning). The interdisciplinary team — including mental health practitioners with lived experience — also models the participatory research approach our project embodies. Code and data publicly available at github.com/ellisalicante/LLMs-Mental-Health-Crisis.

### JMIR Mental Health. (2025). Delusional experiences emerging from AI chatbot interactions or "AI Psychosis." *JMIR Mental Health.*

Introduces the framework of "AI psychosis" — how sustained engagement with conversational AI may trigger, amplify, or reshape psychotic experiences through reciprocal dialogue, affective mirroring, and thematic reinforcement. Notes that LLMs may fail to challenge delusional content due to sycophancy. **Relevance to our project:** Our repair capacity dimension (Rubric Dimension 6) directly addresses this — can a model push back when a user presents content that warrants gentle challenge? Our baseline data shows most models default to agreement or validation rather than genuine engagement.

### American Psychological Association. (2025). Health advisory on the use of generative AI chatbots and wellness applications for mental health. APA.

The APA's official advisory warning that most AI mental health tools lack scientific validation, adequate safety protocols, and regulatory approval. Notes that chatbots "consistently fail to recognize common mental health conditions," "validate what teens say rather than directing them to real help," and "create engagement patterns that delay or discourage help-seeking." **Relevance to our project:** When the APA — the establishment of establishments — issues a health advisory about AI mental health tools, the field has a problem. Our project offers not just critique but an *alternative training methodology*. The APA says what's wrong; we build what could be right.

### Mad in America. (2025–2026). Series on AI chatbots and mental health.

Ongoing investigative journalism series covering AI-related psychiatric harms, including a 2025 MIT Media Lab finding that the heaviest users of companion chatbots reported the *highest* levels of loneliness, a Center for Countering Digital Hate report that ChatGPT provided harmful responses to mental health prompts 53% of the time when researchers posed as 13-year-olds, and analysis of AI chatbots deepening the mental health crisis through dependency and social withdrawal. **Relevance to our project:** Mad in America represents the Mad Studies and psychiatric survivor perspective on AI — the grassroots, critical, lived-experience voice that is often absent from academic and industry research. Their coverage confirms our project's premise: the problem is not bugs to be fixed but paradigms to be questioned.

---

## 5. Critical Disability Perspectives on AI

Scholars asking harder questions — not "how do we make AI mental health tools less biased" but "what assumptions are baked into these systems at the level of design, data, and discourse?"

### Keyes, O. (2020). Automating autism: Disability, discourse, and artificial intelligence. *Journal of Sociotechnical Critique, 1*(1), 8.

A landmark paper in critical disability studies of AI. Keyes argues that conventional AI ethics frameworks are "actively invisible" to discursive harms — the way AI *talks about* and *categorizes* disabled people is itself the violence, not just algorithmic bias. Demonstrates how autism detection AI reproduces a specific medical model of autism that erases autistic self-understanding and agency. **Relevance to our project:** Keyes is doing the critical theory that our project measures empirically. They show *that* the harm exists at the level of discourse; we show *how much* of it exists across eight models, fifty-nine prompts, and seven hundred markers. Essential citation.

### El Morr, C., El-Lahib, Y., & da Silveira Gorman, R. (Eds.). (2025). *Beyond Tech Fixes: AI and Disability Justice.* Springer.

Possibly the most directly relevant book to our project. Argues that technological "fixes" for disability are a form of technoableism — the assumption that technology will "solve" disability rather than addressing structural oppression. Calls for Disability Justice frameworks in AI development, data sovereignty for disabled communities, and participatory design that centers disabled people as experts.

Key chapters include:

- **El-Lahib, Y., da Silveira Gorman, R., & El Morr, C. (2025).** "AI and Disability Justice: Why Beyond Tech Fixes?" — The introductory framework rejecting technoableist approaches to disability and AI.

- **Fernandes, J., Rahman, T., & da Silveira Gorman, R. (2025).** "A Framework for Social Justice-Oriented Practices for Accessible and Inclusive AI" — Lays out concrete principles for justice-oriented AI, including data sovereignty and participatory design.

**Relevance to our project:** They're theorizing what we're building. Their Disability Justice framework for AI is the theoretical house; our fine-tuned models are an empirical proof of concept that lives inside it. This book validates the *approach* while our project provides the *evidence*.

### Timmons, A. C., et al. (2023). A call to action on assessing and mitigating bias in artificial intelligence applications for mental health. *Perspectives on Psychological Science, 18*(5), 1062–1078.

A mainstream call to action reviewing health equity implications of AI in mental health. Important for establishing that even within psychology's establishment, there is growing concern about bias. However, the paper stays within the medical model — it wants to *fix bias* within existing diagnostic frameworks rather than questioning whether those frameworks are the source of the harm. **Relevance to our project:** Useful as a "even the mainstream is worried" citation, but demonstrates the limits of reform-from-within approaches. Our project goes further: we don't just identify bias, we name the *framework* as the problem and train an alternative.

### Brandsen, S., et al. (2024). Prevalence of bias against neurodivergence-related terms in artificial intelligence language models. *Autism Research.*

Tested 11 language model encoders for bias against neurodivergence-related terms. Found that sentences like "I have autism" are perceived more negatively than "I am a bank robber." Bias persisted even when testing words associated with autistic *strengths*. **Relevance to our project:** This is the quantitative smoking gun. Brandsen measures the bias *in the embeddings*; our project measures how that bias manifests *in the outputs*. Together, these approaches show the problem exists at every level of the stack — from how models represent neurodivergence internally to how they talk about it externally.

### Saeidnia, H. R., et al. (2024). Ethical considerations in artificial intelligence interventions for mental health and well-being: Ensuring responsible implementation. *Social Sciences & Humanities Open.*

Reviews ethical dimensions of AI mental health interventions including privacy, informed consent, and the digital divide. **Relevance to our project:** Part of the growing chorus saying "we need ethical guardrails" — our project asks what those guardrails look like when designed *by and for* disabled and Mad communities rather than imposed from above.

### Newman-Griffis, D., Swenor, B. K., Valdez, R. S., & Mason, A. (2025). Disability data futures: Achievable imaginaries for AI and disability data justice. In *Springer.*

Argues that the history of data and AI is one of "disability exclusion, oppression, and the reduction of disabled experience" and that current AI proliferation risks "further automating ableism behind the veneer of algorithmic neutrality." Calls for disability-led visions and data sovereignty. **Relevance to our project:** Directly addresses the data justice dimension of our work — our corpus is authored by a disabled PI, not extracted from disabled communities. This is disability data sovereignty in practice.

### Disabling AI: Power, exclusion, and disability. (2025). *British Journal of Sociology of Education.*

Examines how AI technologies in education reproduce systemic inequalities by embedding ableist and normative assumptions into design and use. Analyzes chatbots, learning analytics, robotic tutors, and intelligent tutoring systems for patterns of sociotechnical ableism. **Relevance to our project:** Extends the "diagnostic gaze" analysis to educational AI — showing the same patterns we find in mental health AI appear across all AI domains that interact with disabled people.

### Souch, C. (2025). Anthropic's hidden mental health screening: A GDPR and AI Act analysis. *christinasouch.com.*

A critical legal analysis of how Claude's system prompts instruct it to identify "mania, psychosis, dissociation, or loss of attachment with reality" in users — processing special category health data without explicit consent. Argues this risks "pathologizing normal human diversity, particularly neurodivergent thinking patterns." **Relevance to our project:** Souch is critiquing *Anthropic's own safety guidelines* for doing exactly what our baseline testing measures — assuming neurotypical norms and pathologizing deviation. Directly relevant to our Safety Guidelines Critical Analysis section. The irony that this project is co-developed with Claude is not lost on us.

### OpenAI. (2025). Model Spec. *model-spec.openai.com.*

OpenAI's published specification for model behavior, including safety guidelines, teen protections, and behavioral boundaries. **Relevance to our project:** One of the primary documents for our Safety Guidelines Critical Analysis — examining where published safety specifications assume neurotypical users, embed psychiatric norms, and what "neuro-humble" safety guidelines would look like instead.

---

## 6. The Longer Lineage: Mad Studies, Anti-Psychiatry, and Disability Justice

These are the intellectual foundations. The critique of institutional psychiatry did not begin with AI — it began with people locked inside the institutions, and with practitioners who chose to listen to them.

### Laing, R. D. (1960). *The Divided Self.* Tavistock.

### Laing, R. D. (1967). *The Politics of Experience.* Penguin.

Laing argued that the clinical gaze itself could be pathogenic — that what people in extreme states needed was not containment but community, not diagnosis but presence. His work is foundational to the anti-psychiatry movement and remains relevant because the pathologizing gaze he described in 1960 is now automated at scale. **Relevance to our project:** Laing's critique is the intellectual ancestor of our empirical findings. When we measure 623 pathologizing markers across Qwen3's baseline responses, we are documenting exactly what Laing warned about — the clinical gaze, now running on GPUs.

### LeFrançois, B. A., Menzies, R., & Reaume, G. (Eds.). (2013). *Mad Matters: A Critical Reader in Canadian Mad Studies.* Canadian Scholars' Press.

The foundational Canadian Mad Studies reader. Establishes Mad Studies as an academic and activist discipline that centers the knowledge and experience of people who have been psychiatrized. Argues for Mad identity as a site of political resistance, not a condition to be treated. **Relevance to our project:** Provides the theoretical framework for why we train models on Mad Studies texts rather than clinical psychology texts — because the knowledge we need comes from the people who have been harmed by the institution, not from the institution itself.

### Sins Invalid. (2019). *Skin, Tooth, and Bone: The Basis of Movement is Our People.* 2nd ed.

The foundational Disability Justice primer from Sins Invalid, a disability justice performance project. Establishes the ten principles of Disability Justice, centering intersectionality, interdependence, and the leadership of those most impacted. **Relevance to our project:** The methodological and ethical backbone. "Nothing about us without us" as practiced in this project — research designed and led by a disabled, neurodivergent, Mad-identified PI — is Disability Justice methodology in action.

### Mills, C. (2014). *Decolonizing Global Mental Health: The Psychiatrization of the Majority World.* Routledge.

Critiques the global export of Western psychiatric norms to the Global South, arguing that "global mental health" is a form of colonialism that pathologizes culturally specific expressions of distress. **Relevance to our project:** Our geopolitical analysis dimension — comparing models from the USA, China, France, Canada, and UAE — directly extends Mills' critique to AI systems. If Western psychiatric norms are exported through human institutions, they are now also exported through language models trained on Western data.

### Graichen, R. (2025). Neurodiversity-affirming supervision. In M. Marneau (Ed.), *On Being an Autistic Therapist.* PCCS Books.

Introduces the concept of "neuro-humility" within Neurodiversity-Affirming Supervision (NDASV), describing a clinical posture that "explores beyond a neurotypical perspective" using "an open framework that draws on multiple, diverse ways of explaining/interpreting client behaviours and experiences, as opposed to limiting us to a single neurotypical and pathologising model." **Relevance to our project:** The direct source of our "neuro-humble" evaluation framework. Graichen describes how to train *therapists* to have this posture; we extend her framework to training *language models*. The parallel is methodologically foundational.

---

## 7. Neurodiversity-Specific: AI and Autistic/ND Users

Work focused specifically on how AI systems interact with, represent, and affect neurodivergent people.

### Papadopoulos, C. (2025). The use of AI chatbots for autistic people: A double-edged sword of digital support and companionship. *Neurodiversity.*

Examines the benefits and dangers of AI companions for autistic users. Notes that chatbots offer low-pressure interaction and relief from the double empathy problem, but can amplify social withdrawal, trigger rejection sensitivity dysphoria, and produce confidently wrong information that autistic users may interpret literally. **Relevance to our project:** Directly addresses the population most affected by our research. Papadopoulos identifies the harms; our project trains models that could provide the benefits without the pathologizing defaults.

### Almufareh, M. F., Kausar, S., Humayun, M., & Tehsin, S. (2024). A conceptual model for inclusive technology: Advancing disability inclusion through artificial intelligence. *Journal of Disability Research.*

Proposes a framework for AI-driven inclusive technology across healthcare, education, and mobility. Approaches disability inclusion from a positive-use lens but remains largely within a medical/assistive framework. **Relevance to our project:** Represents the "tech fixes" approach that El Morr et al. (2025) critique — valuable for showing the mainstream trajectory against which our Disability Justice approach is an alternative.

---

## 8. Technical/Methodological: How We Fine-Tune

Work relevant to the technical methodology of our project.

### Chen, W., et al. (2024). BA-LoRA: Bias-alleviating low-rank adaptation to mitigate catastrophic inheritance in large language models. *arXiv:2408.04556.*

Proposes BA-LoRA, an enhanced LoRA method that addresses "catastrophic inheritance" — the propagation of biases from pre-training through fine-tuning. Uses targeted regularizers to preserve knowledge, enforce representational diversity, and promote robust outputs. **Relevance to our project:** Directly relevant to our fine-tuning methodology. If standard LoRA can propagate pathologizing biases from pre-training, BA-LoRA's approach to bias mitigation during fine-tuning could complement our corpus-driven strategy. Our project attacks the problem from the training data side (formation corpus); BA-LoRA attacks it from the adaptation algorithm side. These approaches are potentially complementary.

---

## 9. Safety & Policy Critique

Work that examines the safety guidelines and policy frameworks governing AI behavior — and questions whose safety they serve.

### APA Health Advisory. (2025). *See Section 4 above.*

### Souch, C. (2025). *See Section 5 above.*

### OpenAI Model Spec. (2025). *See Section 5 above.*

### Mad in America series. (2025–2026). *See Section 4 above.*

*Note: Safety and policy papers appear in their primary thematic sections above. They are cross-referenced here because our Safety Guidelines Critical Analysis draws on all of them.*

---

## The Gap We Occupy

Multiple conversations are happening:

**The establishment** is building AI mental health tools and beginning to worry about bias — but stays within the medical model, seeking to fix the tools rather than questioning the frameworks.

**Empirical harm research** is documenting that AI mental health tools cause real damage — but proposes regulation and oversight rather than alternative training paradigms.

**Critical disability scholars** are theorizing what's wrong — showing how AI reproduces ableism, sanism, and the diagnostic gaze — but largely without empirical measurement of LLM behavior or proposed alternatives.

**Mad Studies and Disability Justice** offer a different vision of what care could look like — but have not yet been applied to AI training methodology.

**The surveillance paradigm** is expanding AI mental health into continuous monitoring — with almost no engagement from disability justice perspectives.

This project sits at the intersection of all of these. We take the establishment's tools (LLMs, fine-tuning, evaluation frameworks), apply the critical scholars' analysis (the diagnostic gaze, technoableism, discursive harm), and use Mad Studies and Disability Justice as the foundation for training an alternative — with empirical evidence that it works.

Nobody else appears to be doing this. That's the gap.

---

*This is a living document. Last updated March 2026.*
*Maintained by Dr. Sparrow Panton and Claude (Anthropic).*
