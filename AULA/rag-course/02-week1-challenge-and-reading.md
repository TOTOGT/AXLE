# Week 1 — Weekend Challenge & Reading

## The Challenge: "Catch Your Model Lying"

Write a script `hallucination_probe.py` that asks your local model (llama3.1:8b) **20 questions** across four categories — 5 each:

1. **Stable general knowledge** (e.g., "What year did WWII end?")
2. **Niche/long-tail facts** (e.g., details about a small town, an obscure standard, AULA-specific info)
3. **Post-training-cutoff events** (things from 2025–2026)
4. **Your capstone domain** (questions only your corpus can answer)

For each answer, score it yourself: ✅ correct, ❌ wrong, 🤷 refused/hedged.

**Deliverable:** a table (markdown or CSV) with question, category, model answer (short), and verdict — plus a 5-sentence conclusion: *in which categories does retrieval earn its keep?*

**Stretch goal:** run the same 20 questions at temperature 0 and 1.0. Does anything change category?

Commit everything to your repo: `git commit -m "Week 1 challenge: hallucination probe"`

## Weekend Reading

- **Primary:** Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — the paper that named RAG. Read the intro and section 2; skim the rest. https://arxiv.org/abs/2005.11401
- **Skim:** Your own probe results. Seriously — they're the most instructive reading this week.

## Video

- Andrej Karpathy, *[1hr Talk] Intro to Large Language Models* — the best single hour on what an LLM is and isn't. Watch especially the part on LLMs as an "operating system" and hallucination. https://www.youtube.com/watch?v=zjkBMFhNj_g

## Reflection questions (bring answers to Week 2)

1. Which failure surprised you most?
2. If you could only fix ONE category of failure with retrieval, which gives most value for your capstone users?
3. What did the model do when it didn't know — refuse or confabulate? Why does that difference matter in production?
