#!/usr/bin/env python3
"""Week 4 full study material page. Importing build_site also regenerates the base site."""
import build_site as bs

body = """
<div class="crumb"><a href="index.html">Home</a> / <a href="week4.html">Week 4</a> / Study material</div>
<article>
<div class="kicker">Week 4 · Study Material</div>
<h1>Hybrid Retrieval and Reranking</h1>
<p class="lede">Week 3 ended on an asymmetry: embeddings fixed your paraphrase failures but blurred exact identifiers that BM25 nailed. Neither system wins alone — real query traffic contains both kinds. This week you stop picking a religion and build the architecture production teams actually run: fuse both, then let a heavier model re-order the shortlist. The win condition is numeric: <b>hybrid must beat both parents.</b></p>

<h2>Part 1 — Why fusion beats either parent</h2>
<p>Lay your Week 3 bake-off table next to your Challenge 2 failure list and the pattern is already there:</p>
<table>
<tr><th>Query type</th><th>BM25</th><th>Embeddings</th></tr>
<tr><td>Exact terms: codes, names, error strings, jargon</td><td><b>Strong</b> — literal match</td><td>Weak — blurred into the neighborhood</td></tr>
<tr><td>Paraphrase &amp; synonyms — user's words ≠ document's words</td><td>Weak — zero overlap, zero score</td><td><b>Strong</b> — same direction in space</td></tr>
<tr><td>Misspellings</td><td>Weak</td><td>Mixed — often survives</td></tr>
<tr><td>Short ambiguous queries</td><td>Mixed</td><td>Mixed — different errors</td></tr>
</table>
<p>The two systems fail on <em>different</em> queries. That's the precondition for fusion to work: combine two rankers whose errors are uncorrelated and the union covers both blind spots. This is the same logic as ensemble methods everywhere in ML — and it's why "BM25 + vectors + fusion" is the default retrieval stack at most serious shops.</p>

<h2>Part 2 — Reciprocal Rank Fusion: embarrassingly simple, annoyingly hard to beat</h2>
<p>Problem: BM25 scores live on one scale (unbounded, corpus-dependent), cosine similarities on another (0–1-ish). Averaging them is meaningless. You could normalize — min-max, z-scores — but every normalization scheme has pathological cases.</p>
<p>RRF sidesteps scores entirely and uses only <b>positions</b>:</p>
<pre><code>RRF(doc) = Σ over rankers  1 / (k + rank_in_that_ranker)      # k = 60 by convention</code></pre>
<p>A doc ranked 1st by BM25 and 3rd by vectors gets 1/61 + 1/63. A doc only one ranker found still scores — just less. The constant k=60 damps the difference between rank 1 and rank 5, so one ranker's confidence can't steamroll the other. Ranked #1 in both → top of the fused list; found by only one → still in the running.</p>
<p>Why it's beloved in production: no tuning, no normalization, robust to adding a third or fourth ranker later, and consistently within a hair of much fancier learned fusion. Twelve lines of code — you'll write them today.</p>

<h2>Part 3 — Reranking: spend compute where it counts</h2>
<p>Your embedding search is a <b>bi-encoder</b>: query and document embedded <em>separately</em>, meeting only at a cosine comparison. Fast — documents are pre-embedded — but shallow: the model can't see how query words interact with document words.</p>
<p>A <b>cross-encoder</b> reads query and document <em>together</em>, attention flowing between them, and outputs one relevance score. Far more accurate; far too slow to run against a whole corpus (it can't precompute anything — every query-document pair is a fresh forward pass).</p>
<p>The production pattern resolves the tension with a funnel:</p>
<pre><code>corpus (thousands)
  → cheap retrieval: BM25 + vectors + RRF     → top ~20 candidates
  → expensive rerank: cross-encoder            → top 5 enter the context window</code></pre>
<p>Cheap-and-broad feeds expensive-and-narrow. Recall is decided by the first stage (a doc missed there is gone forever); precision at the top is decided by the second. Typical lift: 5–15 points of ranking quality for ~100–300 ms. Whether that trade is worth it for <em>your</em> users is a measurement, not an opinion — and you'll make it today.</p>

<h2>Part 4 — Query understanding: fix the query before blaming the index</h2>
<p>Some failures aren't the retriever's fault — the query itself is broken: too short, ambiguous, or phrased in vocabulary the corpus never uses. Three practical repairs, all using the LLM you already run:</p>
<ul>
<li><b>Rewriting:</b> ask the LLM to restate the query clearly ("how do i get my $ back" → "refund request process"). Cheap, often surprisingly effective.</li>
<li><b>Expansion:</b> generate synonyms/related terms and append them — a modern, learned version of what search engines did for decades.</li>
<li><b>HyDE:</b> ask the LLM to write a <em>hypothetical answer</em>, then embed that instead of the question. Answers live nearer to answers than questions do in embedding space — a genuinely clever trick that sometimes wins big and sometimes flops. Measure.</li>
</ul>

<h2>Lab — the staged pipeline, every stage earning its keep</h2>

<h3>Step 1 · RRF fusion</h3>
<p>Create <code>hybrid.py</code>. It fuses your two existing retrievers at the document level:</p>
<pre><code>from bm25_baseline import search as bm25_search
import vector_index as vi

BEST = "titled"                      # your winning collection from Week 3

def rrf(ranked_lists, k=60, top=5):
    scores = {}
    for lst in ranked_lists:
        for rank, doc in enumerate(lst, 1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return [d for d, _ in sorted(scores.items(), key=lambda x: -x[1])][:top]

def hybrid_search(query, k=5, depth=20):
    bm25_docs = [d for d, _ in bm25_search(query, k=depth)]
    vec_docs = vi.search(vi.client.get_collection(BEST), query, k=depth)
    return rrf([bm25_docs, vec_docs], top=k)</code></pre>
<p>Note <code>depth=20</code>: fusion needs to see past the top-5 of each parent — a doc ranked 8th by both is exactly the kind hybrid rescues.</p>

<h3>Step 2 · Cross-encoder reranking</h3>
<p>Add the dependency: <code>uv add sentence-transformers</code> (first run downloads the model, ~90 MB). Create <code>rerank.py</code>:</p>
<pre><code>from pathlib import Path
from sentence_transformers import CrossEncoder
from hybrid import hybrid_search

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
TEXTS = {p.name: p.read_text(errors="ignore")[:1500]
         for p in Path("corpus").glob("*") if p.suffix in (".txt", ".md")}

def reranked_search(query, k=5, depth=20):
    candidates = hybrid_search(query, k=depth, depth=depth)
    pairs = [(query, TEXTS[d]) for d in candidates]
    scores = model.predict(pairs)
    ranked = sorted(zip(candidates, scores), key=lambda x: -x[1])
    return [d for d, _ in ranked[:k]]</code></pre>
<p>(We rerank each document's first 1500 characters — a deliberate simplification; from Week 6 you'll rerank the actual retrieved chunks. Say this limitation out loud in session: knowing what your code approximates is half of engineering.)</p>

<h3>Step 3 · The staged table — your win condition</h3>
<p>Extend <code>evaluate_semantic.py</code> to score four systems on your golden queries:</p>
<pre><code>from hybrid import hybrid_search
from rerank import reranked_search

# ... same score() helper as Week 3 ...
# print rows for: bm25 | best-vector | hybrid | hybrid+rerank</code></pre>
<p>Read the table with Week 4's rules:</p>
<ul>
<li><b>Hybrid beats both parents?</b> Win condition met. If not — don't shrug, diagnose: print per-query results and find which queries fusion hurt. Usually a depth problem or one parent flooding the list.</li>
<li><b>Rerank beats hybrid?</b> Then decide, like an engineer: is the lift worth ~200 ms and a new model dependency for your capstone's users? Either answer is fine; <em>unjustified</em> answers are not.</li>
</ul>

<h3>Step 4 · Query rewriting on your worst queries</h3>
<p>Take your 3 worst golden queries by RR. Create <code>rewrite.py</code>:</p>
<pre><code>import ollama
from hybrid import hybrid_search

def rewrite(query):
    r = ollama.chat(model="llama3.1:8b", messages=[{
        "role": "user",
        "content": f"Rewrite this search query to be clear and specific, using likely "
                   f"document vocabulary. Reply with ONLY the rewritten query.\\n\\n{query}"}])
    return r["message"]["content"].strip()

for q in ["&lt;worst query 1&gt;", "&lt;worst query 2&gt;", "&lt;worst query 3&gt;"]:
    rq = rewrite(q)
    print(f"\\noriginal:  {q}\\nrewritten: {rq}")
    print("  original top:", hybrid_search(q, k=3))
    print("  rewritten top:", hybrid_search(rq, k=3))</code></pre>
<p>Sometimes the rewrite rescues the query; sometimes the LLM "clarifies" it into something you didn't ask. Both outcomes belong in your notes — Week 7's agent will make this rewrite decision automatically, and today you're learning when to trust it.</p>

<div class="box warn"><div class="label">Troubleshooting</div>
<ul>
<li><b>sentence-transformers install is heavy:</b> it pulls PyTorch (~2 GB). One-time cost; everything runs on CPU fine at our scale.</li>
<li><b>Hybrid loses to a parent:</b> check both lists at <code>depth=20</code> — if one retriever returns near-duplicates of the same doc family, the other gets outvoted. Try depth 30, or k=20 in RRF to sharpen top ranks.</li>
<li><b>Cross-encoder scores all look negative:</b> normal — this model outputs logits, not probabilities. Order is what matters.</li>
<li><b>HuggingFace download blocked:</b> set <code>HF_HUB_OFFLINE=0</code> and retry on a normal network; the model caches locally afterward.</li>
</ul></div>

<div class="box ok"><div class="label">Week 4 checkpoint — done when</div>
<ul>
<li><code>hybrid.py</code> fuses BM25 + vectors with RRF you wrote yourself</li>
<li><code>rerank.py</code> adds cross-encoder reranking over the fused candidates</li>
<li>The staged table (bm25 / vector / hybrid / +rerank) is in the README with real numbers</li>
<li>Hybrid beats both parents — or your diagnosis of why not is written down</li>
<li>Rewriting experiment run on your 3 worst queries, observations noted</li>
<li>Committed: <code>git commit -m "Week 4: hybrid + rerank — R@5=…, MRR=…"</code></li>
</ul></div>

<div class="box warn"><div class="label">This weekend</div>
<p><b><a href="challenge4.html">Challenge 4: Beat the Baseline</a></b> — the hard numeric win condition, plus the stretch: sweep RRF's k and rerank depth, chart quality vs. latency, and pick your production operating point. Reading and videos on the <a href="week4.html">Week 4 page</a>.</p></div>

<div class="pagenav"><a href="week4.html">← Week 4 overview</a><a href="challenge4.html">Challenge 4 →</a></div>
</article>
"""

with open(f"{bs.OUT}/week4-material.html", "w") as f:
    f.write(bs.page("Week 4 Study Material", body))
print("Wrote week4-material.html")
