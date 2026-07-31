# Week 1, Day 1 — Professional Setup

You're setting up the way a RAG engineer does: reproducible environment, version control, local LLM. Run each step in your Mac's Terminal and check it off.

---

## 1. Ollama — your local LLM

Download from https://ollama.com/download (Mac app), or via Homebrew:

```bash
brew install ollama
```

Then pull two models — a generator and an embedder:

```bash
ollama pull llama3.1:8b        # the LLM (≈5 GB, needs ~8 GB RAM)
ollama pull nomic-embed-text   # embedding model for Week 3+
```

**Verify:**

```bash
ollama run llama3.1:8b "Say hello in one sentence."
```

If your Mac has ≤8 GB RAM, use `llama3.2:3b` instead.

## 2. Python environment

Professionals never install into system Python. We'll use `uv` (modern, fast):

```bash
brew install uv
cd ~/Desktop/AXLE/rag-course
uv init ragcourse && cd ragcourse
uv add requests rank-bm25 chromadb ollama
```

**Verify:**

```bash
uv run python -c "import chromadb, rank_bm25; print('environment OK')"
```

## 3. Version control

Every checkpoint gets committed. Your capstone becomes a portfolio repo.

```bash
cd ~/Desktop/AXLE/rag-course/ragcourse
git init
git add . && git commit -m "Day 1: environment setup"
```

Optional but recommended: create a GitHub account (or use existing) and push. This repo is what you'll show people at the end.

## 4. First contact with the API

Ollama exposes a local HTTP API at `http://localhost:11434` — the same pattern as OpenAI/Anthropic APIs. Create `hello_llm.py`:

```python
import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "What is retrieval-augmented generation, in two sentences?"}],
)
print(response["message"]["content"])
```

Run it:

```bash
uv run python hello_llm.py
```

## 5. Pick your capstone corpus

Decide what document collection your capstone RAG system will answer questions about. Good options: your AXLE/AULA course materials, a set of PDFs/manuals you know well, or documentation for a tool you use. Aim for 20+ documents. You know the domain → you can judge answer quality — that matters for evaluation weeks.

---

## Done checklist

- [ ] `ollama run llama3.1:8b` responds
- [ ] `uv run python -c "import chromadb"` works
- [ ] Git repo initialized and first commit made
- [ ] `hello_llm.py` prints an answer
- [ ] Capstone corpus chosen

Report back with your checklist status and your corpus choice — then we start Week 1 concepts: probing what your local model knows and where it hallucinates.
