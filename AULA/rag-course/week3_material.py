#!/usr/bin/env python3
"""Week 3 full study material page. Importing build_site also regenerates the base site."""
import build_site as bs

body = """
<div class="crumb"><a href="index.html">Home</a> / <a href="week3.html">Week 3</a> / Study material</div>
<article>
<div class="kicker">Week 3 · Study Material</div>
<h1>Semantic Retrieval: Embeddings and Vector Search</h1>
<p class="lede">Last week you caught BM25 failing on synonyms and paraphrase — words that mean the same thing but share no letters. This week's tool attacks exactly that gap: meaning as geometry. And you'll test your Challenge 2 predictions against reality.</p>

<h2>Part 1 — Embeddings: meaning as coordinates</h2>
<p>An embedding model is a neural network that maps a piece of text to a list of numbers — a point in a high-dimensional space (768 dimensions for the model we'll use). The training objective forces one property: <b>texts with similar meaning land near each other</b>. "Car" and "automobile" sit close together; "car" and "carpet" don't, despite sharing more letters.</p>
<p>Where BM25 asks <em>"do the same words appear?"</em>, embedding search asks <em>"do these texts point in the same semantic direction?"</em> The standard measure is <b>cosine similarity</b> — the angle between the two vectors: 1.0 for identical direction, near 0 for unrelated. Search becomes: embed the query, embed every chunk (once, in advance), return the chunks with the smallest angle.</p>
<div class="box"><div class="label">See it with your own model</div>
<pre><code>import ollama, math

def emb(text):
    return ollama.embed(model="nomic-embed-text", input=text)["embeddings"][0]

def cos(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x*x for x in a)) * math.sqrt(sum(y*y for y in b)))

pairs = [("car", "automobile"), ("car", "carpet"), ("refund policy", "getting my money back")]
for a, b in pairs:
    print(f"{a!r} vs {b!r}: {cos(emb(a), emb(b)):.3f}")</code></pre>
<p>That last pair is the whole reason this week exists: zero shared words, high similarity. BM25 scores it 0.</p></div>

<h2>Part 2 — Making it fast: approximate nearest neighbors</h2>
<p>Exact search compares the query against every stored vector — O(N) per query, the same wall the inverted index solved for keywords. The vector answer is <b>ANN indexes</b>: data structures that find <em>almost certainly</em> the nearest vectors while examining a tiny fraction of them.</p>
<p>The dominant one, <b>HNSW</b> (Hierarchical Navigable Small World), builds a layered graph — sparse express layers on top, dense local layers below. A query enters at the top, greedily hops toward its target, and descends. Think: fly to the right country, drive to the right city, walk to the right door. The price of the speed is the word <em>approximate</em>: recall of ~0.95–0.99 against exact search, tunable. For our corpus sizes exactness is cheap; for millions of vectors, ANN is the only game — and knowing the trade-off exists is what matters at design reviews.</p>

<h2>Part 3 — Chunking: the decision that quietly dominates quality</h2>
<p>You can't embed a 40-page document as one vector — its meaning averages into mush, and you couldn't fit it in the context window anyway. Documents must be split into <b>chunks</b>, and this unglamorous choice routinely moves retrieval quality more than switching embedding models:</p>
<table>
<tr><th>Strategy</th><th>How</th><th>Wins when</th><th>Fails when</th></tr>
<tr><td>Fixed-size</td><td>Every ~800 chars, with overlap</td><td>Uniform prose; dead simple</td><td>Cuts sentences and ideas mid-thought</td></tr>
<tr><td>Paragraph/structure</td><td>Split on blank lines, headings</td><td>Well-formatted docs; keeps ideas whole</td><td>Wildly uneven sizes; giant sections</td></tr>
<tr><td>Structure-aware +</td><td>Attach section title to every chunk</td><td>Chunks carry their own context</td><td>Needs per-corpus rules</td></tr>
</table>
<p>The core tension: <b>small chunks retrieve precisely but may lack context to answer with; big chunks carry context but blur into noise and eat the token budget.</b> There is no universal answer — which is why the lab measures, on <em>your</em> corpus, instead of copying a tutorial's <code>chunk_size=1000</code>.</p>

<h2>Part 4 — Vector databases: indexes plus bookkeeping</h2>
<p>A vector DB (we'll use <b>Chroma</b> — embedded, zero-config, pure local) stores chunk texts, their vectors, and metadata; serves ANN queries; and handles persistence and filtering. That's it. The category is heavily marketed, so keep the deflationary view: <em>a vector database is an ANN index with bookkeeping</em>. Postgres with pgvector, Qdrant, or a NumPy array all occupy the same seat at different scales. Choosing one is a Week 8 ops question, not a Week 3 intelligence question.</p>

<h2>Lab — semantic search over your corpus, three chunkings, verdict by numbers</h2>

<h3>Step 1 · Chunkers</h3>
<p>Create <code>chunkers.py</code>:</p>
<pre><code>def fixed(text, size=800, overlap=150):
    chunks, i = [], 0
    while i &lt; len(text):
        chunks.append(text[i:i+size])
        i += size - overlap
    return chunks

def paragraphs(text, max_len=1200):
    paras, out, cur = [p.strip() for p in text.split("\\n\\n") if p.strip()], [], ""
    for p in paras:
        if len(cur) + len(p) &lt; max_len:
            cur = cur + "\\n\\n" + p if cur else p
        else:
            if cur: out.append(cur)
            cur = p
    if cur: out.append(cur)
    return out

def titled(text, max_len=1200):
    \"\"\"Paragraph chunks, but every chunk carries the last seen heading.\"\"\"
    title, out = "", []
    for chunk in paragraphs(text, max_len):
        first = chunk.splitlines()[0]
        if first.startswith("#"): title = first.lstrip("# ")
        out.append((f"[{title}] " if title else "") + chunk)
    return out</code></pre>

<h3>Step 2 · Embed and index</h3>
<p>Create <code>vector_index.py</code>. One Chroma collection per chunking strategy, so they compete side by side:</p>
<pre><code>from pathlib import Path
import ollama, chromadb
import chunkers

client = chromadb.PersistentClient(path="chroma_db")

def embed(texts):
    return ollama.embed(model="nomic-embed-text", input=texts)["embeddings"]

def build(strategy_name, chunk_fn):
    col = client.get_or_create_collection(strategy_name)
    if col.count(): return col                    # already built
    for p in Path("corpus").glob("*"):
        if p.suffix not in (".txt", ".md"): continue
        chunks = chunk_fn(p.read_text(errors="ignore"))
        col.add(ids=[f"{p.name}::{i}" for i in range(len(chunks))],
                documents=chunks,
                embeddings=embed(chunks),
                metadatas=[{"doc": p.name}] * len(chunks))
    print(f"{strategy_name}: {col.count()} chunks")
    return col

def search(col, query, k=5):
    \"\"\"Chunk-level hits, mapped back to parent documents for fair comparison
    with the Week 2 baseline (which ranks whole documents).\"\"\"
    res = col.query(query_embeddings=embed([query]), n_results=k*3)
    docs, seen = [], set()
    for m in res["metadatas"][0]:
        if m["doc"] not in seen:
            seen.add(m["doc"]); docs.append(m["doc"])
        if len(docs) == k: break
    return docs

STRATEGIES = {"fixed": chunkers.fixed, "paras": chunkers.paragraphs, "titled": chunkers.titled}

if __name__ == "__main__":
    for name, fn in STRATEGIES.items():
        build(name, fn)</code></pre>
<p>Note the mapping step: your golden queries label <em>documents</em>, but this index retrieves <em>chunks</em>. Mapping chunk hits to parent docs keeps the comparison honest. (From Week 6 on, chunks themselves go into the context window — this is just for like-for-like scoring.)</p>

<h3>Step 3 · The bake-off</h3>
<p>Create <code>evaluate_semantic.py</code>, reusing your golden queries:</p>
<pre><code>import json
import vector_index as vi
from bm25_baseline import search as bm25_search

queries = json.load(open("eval_queries.json"))
K = 5

def score(get_top):
    recalls, rrs = [], []
    for item in queries:
        top, rel = get_top(item["query"]), set(item["relevant"])
        recalls.append(len(rel &amp; set(top)) / len(rel))
        rrs.append(next((1/r for r, d in enumerate(top, 1) if d in rel), 0.0))
    return sum(recalls)/len(recalls), sum(rrs)/len(rrs)

print(f"{'system':&lt;12}{'Recall@5':&gt;10}{'MRR':&gt;8}")
r, m = score(lambda q: [d for d, _ in bm25_search(q, k=K)])
print(f"{'bm25':&lt;12}{r:&gt;10.3f}{m:&gt;8.3f}")
for name in vi.STRATEGIES:
    col = vi.client.get_collection(name)
    r, m = score(lambda q, c=col: vi.search(c, q, k=K))
    print(f"{name:&lt;12}{r:&gt;10.3f}{m:&gt;8.3f}")</code></pre>
<p>Run it. One table, four systems, your corpus. Record the winner in your README — and don't be shocked if BM25 still wins some rows. That result is <em>normal</em>, it's corpus-dependent, and it's exactly why Week 4 fuses the two instead of picking a religion.</p>

<h3>Step 4 · Judgment day for Challenge 2</h3>
<p>Run your five "Break BM25" queries through the best semantic collection. For each: did embeddings fix it, as you predicted? Write the scorecard into <code>bm25_failures.md</code> — predictions vs. reality. Typical pattern: synonym and paraphrase failures fixed; exact identifiers (course codes, names, error strings) now <em>worse</em>, because embeddings blur precisely what keywords nail. Keep that asymmetry in mind all next week.</p>

<div class="box warn"><div class="label">Troubleshooting</div>
<ul>
<li><b>Embedding calls slow:</b> first run embeds the whole corpus — normal. Chroma persists; re-runs skip built collections. Batch inputs (the code already passes lists).</li>
<li><b>"collection already exists" after changing a chunker:</b> delete the old one: <code>client.delete_collection("fixed")</code> — or bump the name (<code>fixed_v2</code>).</li>
<li><b>All similarities look high (0.7+):</b> normal for this model family — <em>relative</em> order is what matters, not absolute values.</li>
<li><b>Out of memory with both models loaded:</b> Ollama swaps models per call; if your machine struggles, close other apps or use <code>llama3.2:3b</code> as generator.</li>
</ul></div>

<div class="box ok"><div class="label">Week 3 checkpoint — done when</div>
<ul>
<li>Three Chroma collections built over your corpus — fixed, paragraph, titled</li>
<li>The bake-off table exists with real numbers: BM25 vs three chunkings, Recall@5 and MRR</li>
<li>Challenge 2 predictions scored against reality in <code>bm25_failures.md</code></li>
<li>A written verdict in the README: which chunking your capstone uses, and why</li>
<li>All committed: <code>git commit -m "Week 3: semantic baseline + chunking bake-off"</code></li>
</ul></div>

<div class="box warn"><div class="label">This weekend</div>
<p><b><a href="challenge3.html">Challenge 3: The Chunking Bake-Off</a></b> — extend today's three-way comparison to at least four configurations, inspect the losers, and design one corpus-specific chunking rule. Reading and videos on the <a href="week3.html">Week 3 page</a>.</p></div>

<div class="pagenav"><a href="week3.html">← Week 3 overview</a><a href="challenge3.html">Challenge 3 →</a></div>
</article>
"""

with open(f"{bs.OUT}/week3-material.html", "w") as f:
    f.write(bs.page("Week 3 Study Material", body))
print("Wrote week3-material.html")
