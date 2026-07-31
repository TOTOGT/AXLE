# RAG & Context Engineering: An 8-Week Hands-On Course

**Student:** Pablo · **Instructor:** Claude · **Cost:** $0
**Prerequisites:** Comfortable with Python. No prior RAG experience needed.
**Commitment:** ~5–8 hrs/week (lessons + hands-on labs)
**Capstone:** A production-grade RAG system on documents you choose, deployed and evaluated.

---

## How this works

Each week has three parts:
1. **Concepts** — I teach the theory interactively; you ask questions until it clicks.
2. **Lab** — we write real code together in your environment (Python, a vector DB, an LLM API).
3. **Checkpoint** — a small deliverable that becomes part of your capstone.

By week 8 the weekly checkpoints assemble into one complete system — nothing is throwaway.

---

## Week 1 — When (and When Not) to Retrieve

**Concepts:** What LLMs know vs. what they hallucinate. Context windows as a budget. The retrieval decision: parametric knowledge vs. external grounding. Alternatives to RAG (long context, fine-tuning, tools) and when each wins.

**Lab:** Probe an LLM's knowledge boundaries empirically. Build a "should I retrieve?" classifier for incoming queries.

**Checkpoint:** A one-page decision doc: retrieval criteria for your capstone domain.

## Week 2 — Classical Retrieval: The Foundation Everyone Skips

**Concepts:** Tokenization, inverted indexes, TF-IDF, BM25. Why keyword search still beats embeddings on many queries. Precision, recall, MRR, nDCG.

**Lab:** Build a BM25 search engine from scratch (no libraries first, then `rank_bm25`). Measure it on a labeled query set.

**Checkpoint:** Working BM25 index over your capstone corpus + baseline metrics.

## Week 3 — Semantic Retrieval: Embeddings & Vector Search

**Concepts:** Embedding models, cosine similarity, ANN indexes (HNSW, IVF). Chunking strategies — the single highest-leverage design choice. Vector databases (Chroma, Qdrant, pgvector) and how to pick one.

**Lab:** Embed your corpus with 2–3 chunking strategies; compare retrieval quality head-to-head against your BM25 baseline.

**Checkpoint:** Vector index + a chunking comparison table with real numbers.

## Week 4 — Hybrid Retrieval & Reranking

**Concepts:** Fusing keyword + semantic results (Reciprocal Rank Fusion, weighted scores). Cross-encoder rerankers. Query understanding: expansion, rewriting, HyDE.

**Lab:** Build a hybrid retriever with RRF, add a reranker, measure the lift at each stage.

**Checkpoint:** A retrieval pipeline that measurably beats both pure-keyword and pure-vector.

## Week 5 — Evaluation: Diagnosing Failures Systematically

**Concepts:** Why "it looks right" isn't evaluation. Retrieval metrics vs. generation metrics. Faithfulness, answer relevance, context precision/recall. LLM-as-judge — power and pitfalls. Building golden datasets cheaply.

**Lab:** Build an eval harness (RAGAS or hand-rolled) over your pipeline. Run a failure-mode audit: categorize every bad answer as retrieval failure, generation failure, or chunking failure.

**Checkpoint:** Eval suite + failure taxonomy for your system. This is your debugging compass for the rest of the course.

## Week 6 — End-to-End RAG & Multihop Retrieval

**Concepts:** Prompt construction: context ordering, citation formats, "lost in the middle." Multihop questions and iterative retrieval. Query decomposition. Graph-augmented retrieval basics.

**Lab:** Wire retrieval → prompt → generation → citation into one pipeline. Add query decomposition for multihop questions; verify with your eval suite.

**Checkpoint:** Full RAG system answering both single-hop and multihop questions with citations.

## Week 7 — Agentic RAG: Retrieval-Aware Workflows

**Concepts:** Retrieval as a tool the model decides to call. ReAct loops, self-correction (retrieve → draft → critique → re-retrieve). Routing between multiple indexes/sources. Context engineering for agents: what goes in the window, what stays out, memory management.

**Lab:** Convert your pipeline into an agent that plans retrieval steps, judges its own context sufficiency, and re-queries when needed.

**Checkpoint:** Agentic version of your system + eval comparison against the week-6 static pipeline.

## Week 8 — Production: Secure, Observable, Deployable

**Concepts:** Latency/cost budgets, caching, streaming. Prompt injection via retrieved documents and defenses. Access control on the index. Observability: tracing, logging retrievals, drift detection. Update pipelines for changing corpora.

**Lab:** Add tracing + guardrails, containerize, deploy behind an API, load-test it.

**Checkpoint / Capstone presentation:** Your deployed system + a walkthrough where you defend every design choice with the eval numbers to back it — for both technical and non-technical audiences.

---

## Tooling we'll use (all free/cheap)

Python, `rank_bm25`, an embedding model (local or API), Chroma or Qdrant, an LLM API of your choice, RAGAS or a hand-rolled eval harness, FastAPI + Docker for deployment.

## Ground rules

- Every claim gets tested with code — no cargo-culting framework defaults.
- You type the code (or review every line I write); I explain until it's clear.
- Any week can stretch or compress. The syllabus serves you, not the reverse.

**To start Week 1, just say "start week 1."**
