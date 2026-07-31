#!/usr/bin/env python3
"""Week 2 full study material page. Importing build_site also regenerates the base site."""
import build_site as bs

body = """
<div class="crumb"><a href="index.html">Home</a> / <a href="week2.html">Week 2</a> / Study material</div>
<article>
<div class="kicker">Week 2 · Study Material</div>
<h1>Classical Retrieval: BM25 and the Inverted Index</h1>
<p class="lede">Fifty years of search engineering, built by hand over your own corpus. By the end you'll have a working search engine, understand every number it computes, and — most importantly — have a <b>measured baseline</b> that every later technique in this course must beat.</p>

<h2>Part 1 — The inverted index: why search is fast</h2>
<p>The naive way to search: for each query, scan every document. That's O(corpus size) per query — fine for 20 documents, absurd for 20 million. The fix, unchanged since the 1970s, is to do the scanning <em>once, in advance</em>, and flip the direction of the map:</p>
<pre><code>Forward:  doc1 → ["retrieval", "systems", "need", "evaluation", ...]
Inverted: "retrieval" → [doc1, doc4, doc9]
          "evaluation" → [doc1, doc7]</code></pre>
<p>At query time you look up each query term — a hash-table hit — and intersect or union the document lists. Query cost now scales with the number of <em>matching</em> documents, not the corpus. Elasticsearch, Lucene, and every web search engine are, at their core, this data structure plus decades of engineering around it.</p>

<h2>Part 2 — Scoring: from counting to TF-IDF</h2>
<p>The index finds candidates; scoring ranks them. Two intuitions, each one formula:</p>
<p><b>Term frequency (TF).</b> A document that mentions "chunking" ten times is more likely about chunking than one that mentions it once. Count occurrences.</p>
<p><b>Inverse document frequency (IDF).</b> Not all terms are equal. "The" appears in every document — matching it carries zero information. "Multihop" appears in two — matching it is gold. Weight each term by how rare it is: <code>idf(t) = log(N / df(t))</code>, where N is total documents and df(t) is how many contain t.</p>
<p>TF-IDF multiplies the two. It's crude — and it's the reason search "just worked" for decades. The deep insight to keep: <b>rarity is signal</b>. Most of what feels like intelligence in a search engine is IDF quietly ignoring the noise words.</p>

<h2>Part 3 — BM25: TF-IDF grown up</h2>
<p>BM25 (Best Matching 25, from the Okapi system) fixes TF-IDF's two blind spots and has been the industry-standard lexical ranker for ~25 years:</p>
<p><b>Saturation (parameter k1, default ≈1.5).</b> Under raw TF, a document saying "chunking" 50 times scores 5× one saying it 10 times. Really 5× more relevant? No — after a few occurrences, you're convinced. BM25 makes the TF contribution level off: <code>tf·(k1+1)/(tf+k1)</code> approaches a ceiling instead of growing forever. Low k1 → saturates fast; high k1 → closer to raw counting.</p>
<p><b>Length normalization (parameter b, default ≈0.75).</b> Long documents mention everything eventually — raw counting systematically favors them. BM25 scales the score by document length relative to the corpus average. b=1 fully normalizes, b=0 ignores length. The default 0.75 says: penalize length, but not completely.</p>
<p>Together, per term, per document:</p>
<pre><code>score(t, d) = idf(t) · tf(t,d)·(k1+1) / ( tf(t,d) + k1·(1 − b + b·|d|/avg_len) )</code></pre>
<p>Sum over query terms. That one line — readable now, piece by piece — powers more production search than any neural model yet deployed.</p>

<h2>Part 4 — Measuring retrieval: the numbers that rule this course</h2>
<p>From this week on, no retrieval claim is accepted without measurement. Three metrics, all computed against queries whose relevant documents you've labeled by hand:</p>
<table>
<tr><th>Metric</th><th>Question it answers</th><th>Computed as</th></tr>
<tr><td><b>Recall@k</b></td><td>Of the truly relevant docs, how many made the top k?</td><td>relevant found in top-k ÷ total relevant</td></tr>
<tr><td><b>Precision@k</b></td><td>Of the top k results, how many are relevant?</td><td>relevant in top-k ÷ k</td></tr>
<tr><td><b>MRR</b></td><td>How high does the <em>first</em> relevant doc rank?</td><td>average of 1/rank of first relevant hit</td></tr>
</table>
<p>For RAG, <b>Recall@k is usually king</b>: if the right chunk isn't in the top-k that enters the context window, nothing downstream can save the answer. MRR matters when the window is tight and order counts. In Week 5 these three grow into a full evaluation discipline — this week they just need to become reflexes.</p>

<h2>Lab — build the baseline</h2>
<p>All files go in your <code>ragcourse</code> repo from Week 1. We assume your corpus is a folder of <code>.txt</code>/<code>.md</code> files at <code>corpus/</code> — export/convert your documents into that shape first (plain text is fine; PDFs can wait for a later week).</p>

<h3>Step 1 · An inverted index + TF-IDF, from scratch</h3>
<p>Create <code>classic_search.py</code>. No libraries — the point is that there's no magic:</p>
<pre><code>import math, re
from pathlib import Path
from collections import Counter, defaultdict

def tokenize(text):
    return re.findall(r"[a-záéíóúüñ0-9]+", text.lower())

class TfIdfIndex:
    def __init__(self, docs):                 # docs: {name: text}
        self.docs = {n: tokenize(t) for n, t in docs.items()}
        self.N = len(self.docs)
        self.index = defaultdict(set)         # term -> {doc names}
        self.tf = {}                          # doc -> Counter(term)
        for name, toks in self.docs.items():
            self.tf[name] = Counter(toks)
            for t in set(toks):
                self.index[t].add(name)

    def idf(self, term):
        df = len(self.index.get(term, ()))
        return math.log(self.N / df) if df else 0.0

    def search(self, query, k=5):
        scores = Counter()
        for t in tokenize(query):
            for doc in self.index.get(t, ()):
                scores[doc] += self.tf[doc][t] * self.idf(t)
        return scores.most_common(k)

if __name__ == "__main__":
    docs = {p.name: p.read_text(errors="ignore")
            for p in Path("corpus").glob("*") if p.suffix in (".txt", ".md")}
    print(f"Indexed {len(docs)} documents")
    ix = TfIdfIndex(docs)
    while True:
        q = input("\\nquery> ").strip()
        if not q: break
        for doc, score in ix.search(q):
            print(f"  {score:7.2f}  {doc}")</code></pre>
<p>Run <code>uv run python classic_search.py</code> and interrogate your corpus. Watch the scores: search for a rare domain term, then for a common word, and see IDF doing the work.</p>

<h3>Step 2 · Swap in BM25</h3>
<p>Create <code>bm25_baseline.py</code> using the library version (which implements the full formula from Part 3):</p>
<pre><code>from pathlib import Path
from rank_bm25 import BM25Okapi
from classic_search import tokenize

docs = {p.name: p.read_text(errors="ignore")
        for p in Path("corpus").glob("*") if p.suffix in (".txt", ".md")}
names = list(docs)
bm25 = BM25Okapi([tokenize(docs[n]) for n in names])

def search(query, k=5):
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(zip(names, scores), key=lambda x: -x[1])
    return ranked[:k]

if __name__ == "__main__":
    while True:
        q = input("\\nquery> ").strip()
        if not q: break
        for doc, score in search(q):
            print(f"  {score:7.2f}  {doc}")</code></pre>
<p>Run the same queries against both engines. Where do the rankings differ? Long documents are the usual culprits — that's length normalization visibly earning its keep.</p>

<h3>Step 3 · The golden queries</h3>
<p>Create <code>eval_queries.json</code>: 10 realistic queries against your corpus, each with the documents you judge relevant (this hand-labeling is real evaluation work — it will feel slow; it's the most valuable artifact of the week):</p>
<pre><code>[
  {"query": "how do I enroll in the program",
   "relevant": ["enrollment.md", "faq.md"]},
  {"query": "refund and cancellation policy",
   "relevant": ["terms.md"]}
]</code></pre>
<p>Mix easy queries (exact vocabulary from the docs) with hard ones (your own words for the same idea). The hard ones are tomorrow's ammunition.</p>

<h3>Step 4 · Score the baseline</h3>
<p>Create <code>evaluate.py</code>:</p>
<pre><code>import json
from bm25_baseline import search

queries = json.load(open("eval_queries.json"))
K = 5
recalls, rrs = [], []
for item in queries:
    top = [doc for doc, _ in search(item["query"], k=K)]
    rel = set(item["relevant"])
    recalls.append(len(rel &amp; set(top)) / len(rel))
    rr = 0.0
    for rank, doc in enumerate(top, 1):
        if doc in rel:
            rr = 1 / rank
            break
    rrs.append(rr)
    flag = "  ⚠" if rr == 0 else ""
    print(f"R@{K}={recalls[-1]:.2f}  RR={rr:.2f}  {item['query']}{flag}")

print(f"\\nBASELINE — Recall@{K}: {sum(recalls)/len(recalls):.3f}   MRR: {sum(rrs)/len(rrs):.3f}")</code></pre>
<p>Run it, record the two numbers in your README, and commit everything: <code>git commit -m "Week 2: BM25 baseline — R@5=…, MRR=…"</code>. <b>These are the numbers to beat for the next six weeks.</b></p>

<div class="box warn"><div class="label">Troubleshooting</div>
<ul>
<li><b>Recall looks too perfect (1.0 everywhere):</b> your queries reuse exact document vocabulary. Add queries phrased in your own words — watch it drop.</li>
<li><b>One doc dominates every query:</b> it's probably much longer than the rest. Compare TF-IDF vs BM25 rankings for it — then try <code>BM25Okapi(..., b=1.0)</code>.</li>
<li><b>Accented text matching badly:</b> the tokenizer above keeps áéíóúüñ; if your corpus mixes accents inconsistently, normalize with <code>unicodedata</code> before tokenizing.</li>
</ul></div>

<div class="box ok"><div class="label">Week 2 checkpoint — done when</div>
<ul>
<li><code>classic_search.py</code> works and you can explain every line</li>
<li><code>bm25_baseline.py</code> ranks your corpus; you can say what k1 and b do without looking</li>
<li><code>eval_queries.json</code> has 10 hand-labeled queries, easy and hard mixed</li>
<li>Recall@5 and MRR recorded in the README and committed</li>
</ul></div>

<div class="box warn"><div class="label">This weekend</div>
<p><b><a href="challenge2.html">Challenge 2: Break BM25</a></b> — find five queries where your baseline fails, diagnose each, and predict which failures embeddings will fix. Those predictions get tested against reality next week. Reading and videos on the <a href="week2.html">Week 2 page</a>.</p></div>

<div class="pagenav"><a href="week2.html">← Week 2 overview</a><a href="challenge2.html">Challenge 2 →</a></div>
</article>
"""

with open(f"{bs.OUT}/week2-material.html", "w") as f:
    f.write(bs.page("Week 2 Study Material", body))
print("Wrote week2-material.html")
