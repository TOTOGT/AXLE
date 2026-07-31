#!/usr/bin/env python3
"""Week 6 full study material page. Importing build_site also regenerates the base site."""
import build_site as bs

body = """
<div class="crumb"><a href="index.html">Home</a> / <a href="week6.html">Week 6</a> / Study material</div>
<article>
<div class="kicker">Week 6 · Study Material</div>
<h1>End-to-End RAG and Multihop Retrieval</h1>
<p class="lede">You have a strong retriever (Week 4) and a machine that measures answers (Week 5). This week the two halves become one system — properly this time, with chunk-level context, engineered prompts, and verifiable citations. Then you attack the questions no single document can answer.</p>

<h2>Part 1 — Prompt construction <em>is</em> context engineering</h2>
<p>Your Week 5 generator was deliberately crude: it dumped 2000-character document prefixes into a prompt. Three things were wrong with that, and fixing them is most of today's quality gain.</p>
<p><b>Retrieve chunks, not documents.</b> You built chunk-level indexes in Week 3, then evaluated at document level so the comparison with BM25 stayed honest. That scaffolding comes down now: the context window should receive the specific passages that matched, not whole-document prefixes that may not even contain them.</p>
<p><b>Position matters — "lost in the middle."</b> Models attend most reliably to the beginning and end of a long context, and least reliably to the middle. The same passage placed at position 1 versus position 5 measurably changes whether the model uses it. Two practical responses: keep the context short (fewer, better chunks beat more chunks), and order deliberately — a common pattern is best-first, or best at the edges with weaker material buried.</p>
<p><b>Format is signal.</b> Delimiters, source labels, and consistent structure help the model tell context from instruction from question. Unlabeled walls of text invite the model to blend everything — including blending your instructions with retrieved content, which is precisely the vulnerability Week 8 exploits.</p>

<h2>Part 2 — Citations that can be verified</h2>
<p>An answer with a source label is not the same as a grounded answer. Models will happily attach a plausible-looking citation to a claim they invented — a <em>citation hallucination</em>, and one of the most damaging failure modes because it manufactures false confidence in exactly the audience least able to check.</p>
<p>Three requirements for citations worth shipping:</p>
<ol>
<li><b>Stable identifiers.</b> Give each chunk a short ID in the prompt (<code>[S1]</code>, <code>[S2]</code>) and require the model to reuse those exact tokens. Free-text citations are unparseable and unverifiable.</li>
<li><b>Per-claim, not per-answer.</b> One citation at the end tells you nothing about which sentence it supports.</li>
<li><b>Programmatic verification.</b> Parse the IDs out, confirm each exists, and — the step almost everyone skips — check that the cited chunk actually supports the claim, using the Week 5 judge. A citation you never verified is decoration.</li>
</ol>

<h2>Part 3 — Multihop: the questions one document can't answer</h2>
<p>"Which of our courses shares a prerequisite with the astrobiology program?" Every retrieval technique so far assumes the answer sits in some passage waiting to be found. Here it doesn't exist anywhere — it must be <em>assembled</em>:</p>
<pre><code>hop 1: what are the astrobiology prerequisites?     → doc A
hop 2: which other courses list those prerequisites? → docs C, F
synthesis: the answer, which appears in no single document</code></pre>
<p>Single-shot retrieval fails these by construction: the query embeds as one blurred point between two topics, and the top-k fills with documents that are partly relevant to everything and sufficient for nothing. Two mechanisms fix it:</p>
<p><b>Decomposition (parallel).</b> Split the question into independent sub-questions, retrieve for each, merge, synthesize. Works when the hops don't depend on each other: "compare X and Y" — retrieve X, retrieve Y, compare.</p>
<p><b>Iterative retrieval (sequential).</b> When hop 2's query depends on hop 1's answer, you must loop: retrieve, read, decide what's still missing, retrieve again. This is genuinely different — the system takes an action based on what it just learned. That loop is the direct bridge to next week's agents.</p>
<div class="box"><div class="label">The routing question</div>
<p>Decomposition costs 2–4× the latency and tokens. Most queries are single-hop and don't need it. So you need a cheap classifier deciding <em>per query</em> whether to decompose — the same "should I retrieve?" decision from Week 1, one level up. Build the simple version today; Week 7 hands the decision to the model itself.</p></div>

<h2>Lab — the real pipeline</h2>

<h3>Step 1 · Chunk-level retrieval</h3>
<p>Create <code>retrieve.py</code> — returns passages with IDs and provenance, not document names:</p>
<pre><code>import vector_index as vi
from bm25_baseline import search as bm25_search
from pathlib import Path

BEST = "titled"
TEXTS = {p.name: p.read_text(errors="ignore")
         for p in Path("corpus").glob("*") if p.suffix in (".txt", ".md")}

def retrieve_chunks(query, k=4, depth=12):
    \"\"\"Vector chunks + top BM25 documents, fused by simple interleaving.\"\"\"
    col = vi.client.get_collection(BEST)
    res = col.query(query_embeddings=vi.embed([query]), n_results=depth)
    chunks = [{"text": t, "doc": m["doc"]}
              for t, m in zip(res["documents"][0], res["metadatas"][0])]

    # keyword safety net: ensure the best BM25 doc is represented
    top_bm25 = [d for d, _ in bm25_search(query, k=2)]
    for d in top_bm25:
        if not any(c["doc"] == d for c in chunks):
            chunks.append({"text": TEXTS[d][:1200], "doc": d})

    out = chunks[:k]
    for i, c in enumerate(out, 1):
        c["id"] = f"S{i}"
    return out</code></pre>

<h3>Step 2 · Prompt with citations</h3>
<p>Create <code>generate.py</code>:</p>
<pre><code>import ollama, re
from retrieve import retrieve_chunks

PROMPT = \"\"\"You answer strictly from the sources below.

Rules:
- Use ONLY information in the sources.
- After EVERY sentence, cite the source(s) it came from, like [S1] or [S1][S3].
- If the sources do not answer the question, reply exactly: I don't know.

Sources:
{sources}

Question: {question}
Answer:\"\"\"

def format_sources(chunks):
    return "\\n\\n".join(f"[{c['id']}] (from {c['doc']})\\n{c['text']}" for c in chunks)

def generate(question, k=4):
    chunks = retrieve_chunks(question, k=k)
    r = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content":
        PROMPT.format(sources=format_sources(chunks), question=question)}])
    return r["message"]["content"].strip(), chunks

def cited_ids(answer_text):
    return set(re.findall(r"\\[(S\\d+)\\]", answer_text))</code></pre>

<h3>Step 3 · Verify the citations</h3>
<p>Create <code>verify_citations.py</code> — reusing the Week 5 judge, because a citation is just a faithfulness claim with an address:</p>
<pre><code>import re
from generate import generate, cited_ids
from judge import ask

def verify(question):
    answer, chunks = generate(question)
    by_id = {c["id"]: c for c in chunks}
    valid_ids = set(by_id)
    used = cited_ids(answer)

    print(f"\\nQ: {question}\\nA: {answer}")
    print(f"  cited: {sorted(used)}  |  invalid: {sorted(used - valid_ids) or 'none'}")

    for sentence in [s.strip() for s in re.split(r"(?&lt;=[.!?])\\s+", answer) if s.strip()]:
        ids = cited_ids(sentence)
        if not ids:
            print(f"  ⚠ uncited: {sentence[:70]}…")
            continue
        for sid in ids &amp; valid_ids:
            v = ask(f"Source:\\n{by_id[sid]['text'][:2000]}\\n\\nClaim: {sentence}\\n\\n"
                    f"Does the source support this claim? Reply YES or NO only.")
            if not v.startswith("YES"):
                print(f"  ✗ [{sid}] does NOT support: {sentence[:70]}…")</code></pre>
<p>Run this on ten golden questions. The uncited sentences and the false citations you find are the honest picture of where your prompt still leaks — and they're excellent material for your capstone defense.</p>

<h3>Step 4 · Context ordering A/B</h3>
<p>Test "lost in the middle" on your own corpus instead of trusting the paper. In <code>generate.py</code>, add a parameter that reverses chunk order (worst-first), then run your Week 5 audit under both settings and compare faithfulness and relevance. Record the delta. If it's small on your corpus, that's a finding too — you now know context length is your lever rather than ordering.</p>

<h3>Step 5 · Decomposition and the router</h3>
<p>Create <code>multihop.py</code>:</p>
<pre><code>import ollama
from retrieve import retrieve_chunks
from generate import PROMPT, format_sources

def needs_decomposition(question):
    r = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content":
        f"Does answering this question require combining information from MULTIPLE "
        f"separate documents? Reply YES or NO only.\\n\\n{question}"}])
    return r["message"]["content"].strip().upper().startswith("YES")

def decompose(question, max_parts=3):
    r = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content":
        f"Break this question into at most {max_parts} simpler sub-questions, each "
        f"answerable from a single document. One per line, no numbering.\\n\\n{question}"}])
    return [q.strip("-• ").strip() for q in r["message"]["content"].splitlines() if len(q.strip()) &gt; 10]

def multihop_answer(question, k=3):
    subs = decompose(question)
    chunks, seen = [], set()
    for sq in subs:
        for c in retrieve_chunks(sq, k=k):
            key = c["text"][:120]
            if key not in seen:
                seen.add(key); chunks.append(c)
    for i, c in enumerate(chunks, 1):
        c["id"] = f"S{i}"
    r = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content":
        PROMPT.format(sources=format_sources(chunks), question=question)}])
    return r["message"]["content"].strip(), subs, chunks

def smart_answer(question):
    \"\"\"Route: only pay for decomposition when the question needs it.\"\"\"
    if needs_decomposition(question):
        ans, subs, chunks = multihop_answer(question)
        return ans, {"mode": "multihop", "sub_questions": subs}
    from generate import generate
    ans, chunks = generate(question)
    return ans, {"mode": "single"}</code></pre>

<h3>Step 6 · Prove it on the multi-source questions</h3>
<p>Remember the multi-source items you deliberately put in <code>golden.json</code> last week. Run each through <code>generate()</code> and through <code>multihop_answer()</code>, and put the two answers side by side. Also check the router: on your full golden set, how often does <code>needs_decomposition</code> fire on simple questions (wasted latency) or miss real multihop ones (wrong answers)? That confusion matrix is your Week 6 headline result.</p>

<div class="box warn"><div class="label">Troubleshooting</div>
<ul>
<li><b>Model ignores the citation format:</b> smaller models drift. Add one worked example to the prompt (one-shot), and keep the rule block short — long rule lists get partially ignored.</li>
<li><b>Everything comes back "I don't know":</b> your k is too small or chunks too narrow. Check the retrieved chunks by hand first — this is a Week 5 retrieval failure, not a prompt problem.</li>
<li><b>Decomposition invents sub-questions unrelated to the corpus:</b> constrain it — mention the domain in the decomposition prompt, and cap at 3 parts.</li>
<li><b>Multihop is slower and worse:</b> genuinely common on single-hop questions. That's the router's whole reason to exist — check it's firing correctly before blaming decomposition.</li>
</ul></div>

<div class="box ok"><div class="label">Week 6 checkpoint — done when</div>
<ul>
<li><code>retrieve.py</code> returns chunk-level context with IDs and provenance</li>
<li><code>generate.py</code> produces per-sentence citations in a parseable format</li>
<li><code>verify_citations.py</code> has been run on 10 questions; invalid and uncited claims counted</li>
<li>Context-ordering A/B delta recorded in the README</li>
<li><code>multihop.py</code> answers your multi-source golden questions that single-shot fails</li>
<li>Router confusion matrix recorded (false decompositions vs. missed multihops)</li>
<li>Committed: <code>git commit -m "Week 6: end-to-end RAG with citations + multihop"</code></li>
</ul></div>

<div class="box warn"><div class="label">This weekend</div>
<p><b><a href="challenge6.html">Challenge 6: The Multihop Gauntlet</a></b> — author 8 genuine multihop questions, demonstrate the single-shot pipeline failing them, then measure the difference. The stretch goal is the automatic router you prototyped in Step 5. Reading and video on the <a href="week6.html">Week 6 page</a>.</p></div>

<div class="pagenav"><a href="week6.html">← Week 6 overview</a><a href="challenge6.html">Challenge 6 →</a></div>
</article>
"""

with open(f"{bs.OUT}/week6-material.html", "w") as f:
    f.write(bs.page("Week 6 Study Material", body))
print("Wrote week6-material.html")
