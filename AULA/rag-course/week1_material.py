#!/usr/bin/env python3
"""Week 1 full study material page. Importing build_site also regenerates the base site."""
import build_site as bs

body = """
<div class="crumb"><a href="index.html">Home</a> / <a href="week1.html">Week 1</a> / Study material</div>
<article>
<div class="kicker">Week 1 · Study Material</div>
<h1>When (and When Not) to Retrieve</h1>
<p class="lede">This is the complete Week 1 lesson. In the live session we work through it together; between sessions it's your reference. By the end you'll have a professional environment running a local LLM — and a measured map of exactly where that model can't be trusted.</p>

<h2>Part 1 — How a language model "knows" things</h2>
<p>During training, a model reads a vast snapshot of text and compresses statistical patterns from it into billions of numeric weights. Two properties of that process explain almost everything this course exists to fix:</p>
<p><b>The compression is lossy.</b> Facts that appear thousands of times in training data (the capital of France, the boiling point of water) survive compression with high fidelity. Facts that appear rarely — the prerequisites of a specific AULA course, clause 7 of your supplier contract, anything published last month — blur or vanish. The model didn't choose what to forget; frequency chose for it.</p>
<p><b>There is no "I don't know" flag.</b> The model's only operation is: given the text so far, produce a plausible continuation. When the underlying knowledge is missing, the <em>mechanism doesn't change</em> — it still produces a plausible continuation. That's a hallucination: not a malfunction, but the normal mechanism running without data. This is why hallucinations are fluent, confident, and formatted exactly like correct answers.</p>
<div class="box"><div class="label">Try it now</div>
<p>Ask your local model something it certainly knows, then something it almost certainly doesn't:</p>
<pre><code>ollama run llama3.1:8b "What is the capital of Australia?"
ollama run llama3.1:8b "What were the exact enrollment requirements of AULA's 2025 astrobiology program?"</code></pre>
<p>Watch <em>how</em> it fails the second one. Does it refuse, hedge, or invent? All three happen — and only one of them is safe.</p></div>

<h2>Part 2 — The context window: knowledge that arrives at runtime</h2>
<p>Everything the model didn't memorize must arrive through the prompt — the <b>context window</b>. Think of it as the model's working memory: whatever text you place there, the model can attend to when generating. This is the escape hatch from the limits of Part 1: the model doesn't need to <em>know</em> your document if you <em>show</em> it your document.</p>
<p>But the window is a budget, measured in tokens (a token ≈ ¾ of an English word). Three budget rules govern everything we build in this course:</p>
<ol>
<li><b>It's finite.</b> Your corpus won't fit. Something must choose which fragments enter — that chooser is the retriever, and its quality bounds the whole system.</li>
<li><b>Quality degrades as it fills.</b> Models attend unevenly across long contexts; stuffing the window hurts both cost and accuracy. More context is not more better.</li>
<li><b>Every token costs.</b> Latency and (with hosted models) money scale with context length. Production systems are engineered around this line item.</li>
</ol>
<p><b>Context engineering</b> — the second noun in this course's title — is the discipline of spending that budget deliberately: what gets in, in what order, in what format, and what stays out.</p>

<h2>Part 3 — The retrieval decision</h2>
<p>Retrieval-augmented generation adds a step before generation: search an external knowledge store, place the best findings in the context window, then generate. It is an engineering trade — you buy grounding and pay in latency, complexity, and new failure modes. The professional skill is knowing when the trade is worth it.</p>
<table>
<tr><th>Query relies on…</th><th>Example</th><th>Retrieve?</th><th>Why</th></tr>
<tr><td>Stable, common knowledge</td><td>"Explain photosynthesis"</td><td>No</td><td>Weights already reliable; retrieval adds cost and can even inject noise</td></tr>
<tr><td>Reasoning over given text</td><td>"Summarize this paragraph"</td><td>No</td><td>Everything needed is already in the window</td></tr>
<tr><td>Private data</td><td>"What does our refund policy say?"</td><td><b>Yes</b></td><td>Never in training data — without retrieval the model can only invent</td></tr>
<tr><td>Fresh data</td><td>"What changed in the v3 release?"</td><td><b>Yes</b></td><td>Post-cutoff; weights are frozen in the past</td></tr>
<tr><td>Long-tail facts</td><td>"Dosage note in study NCT0482…"</td><td><b>Yes</b></td><td>Too rare to survive compression; highest hallucination risk</td></tr>
<tr><td>Auditable answers</td><td>"…and cite the source clause"</td><td><b>Yes</b></td><td>Citations require retrieved text; weights can't be cited</td></tr>
</table>
<p>Real systems receive all six kinds of traffic. That's why mature architectures <em>route</em>: a cheap decision layer classifies each query and only invokes retrieval when it pays. You'll build exactly this intuition in the lab — and by Week 7, your agent will make this decision by itself, per query.</p>

<h2>Part 4 — The alternatives, honestly compared</h2>
<p>RAG is not the only way to close a knowledge gap. You should be able to argue all four options — this table is a favorite architecture-review and interview question:</p>
<table>
<tr><th>Approach</th><th>Best when</th><th>Breaks down when</th></tr>
<tr><td><b>Long-context stuffing</b><br>paste everything into the prompt</td><td>Corpus is small (a handful of docs) and queries touch most of it</td><td>Corpus grows past the window; cost per query balloons; attention degrades mid-context</td></tr>
<tr><td><b>Fine-tuning</b><br>continue training on your data</td><td>Teaching <em>style, format, or skills</em> (tone, schema-following)</td><td>Teaching <em>facts</em>: expensive to update, can't cite, still hallucinates, stale on every data change</td></tr>
<tr><td><b>Tool calls</b><br>model queries an API/database</td><td>Answers live in structured systems (inventory, calendar, SQL)</td><td>Knowledge is unstructured prose — you need search over documents, which is… retrieval</td></tr>
<tr><td><b>RAG</b><br>search, then generate</td><td>Large, changing, unstructured corpus; need citations; need freshness</td><td>Corpus is tiny (just stuff it), or the task is pure reasoning/creativity</td></tr>
</table>
<p>Note the pattern: these compose rather than compete. Production systems routinely fine-tune for format, retrieve for facts, and call tools for structured lookups — in the same request.</p>

<h2>Lab — your professional setup</h2>
<p>From day one you work like a working engineer: local model, reproducible environment, version control. Every command below runs in your Mac's Terminal.</p>

<h3>Step 1 · Ollama and models</h3>
<pre><code>brew install ollama          # or download the app from ollama.com
ollama pull llama3.1:8b      # generator (~5 GB, needs ~8 GB RAM)
ollama pull nomic-embed-text # embedder — we'll need it from Week 3</code></pre>
<p>Verify: <code>ollama run llama3.1:8b "Say hello in one sentence."</code></p>
<div class="box warn"><div class="label">Troubleshooting</div>
<ul>
<li><b>≤8 GB RAM or very slow responses:</b> use <code>llama3.2:3b</code> everywhere instead — every lab in this course works with it.</li>
<li><b>"connection refused":</b> the Ollama server isn't running — launch the Ollama app, or run <code>ollama serve</code> in a separate terminal tab.</li>
<li><b>Download stalls:</b> re-run the pull; it resumes where it stopped.</li>
</ul></div>

<h3>Step 2 · Python environment with uv</h3>
<p>Professionals never install into system Python — environments are isolated and reproducible, so "works on my machine" means it works on every machine.</p>
<pre><code>brew install uv
mkdir -p ~/Desktop/AXLE/rag-course &amp;&amp; cd ~/Desktop/AXLE/rag-course
uv init ragcourse &amp;&amp; cd ragcourse
uv add requests rank-bm25 chromadb ollama</code></pre>
<p>Verify: <code>uv run python -c "import chromadb, rank_bm25; print('environment OK')"</code></p>

<h3>Step 3 · Version control</h3>
<pre><code>git init
git add . &amp;&amp; git commit -m "Week 1: environment setup"</code></pre>
<p>Every checkpoint in this course ends in a commit. By Week 8 this repository <em>is</em> your portfolio.</p>

<h3>Step 4 · First programmatic call</h3>
<p>Ollama exposes a local HTTP API on <code>localhost:11434</code> — the same request/response pattern as the OpenAI and Anthropic APIs, so everything you learn transfers. Create <code>hello_llm.py</code>:</p>
<pre><code>import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role": "user",
               "content": "What is retrieval-augmented generation, in two sentences?"}],
)
print(response["message"]["content"])</code></pre>
<p>Run it: <code>uv run python hello_llm.py</code> — then commit.</p>

<h3>Step 5 · Probe the knowledge boundary</h3>
<p>Now we measure Part 1 instead of taking it on faith. Create <code>probe.py</code>:</p>
<pre><code>import ollama

QUESTIONS = {
    "stable":    ["What year did World War II end?"],          # add 4 more
    "long_tail": ["Who founded the first bakery in Ushuaia?"], # add 4 more
    "post_cutoff": ["What happened in tech news last month?"], # add 4 more
    "capstone":  ["&lt;a question only YOUR corpus can answer&gt;"], # add 4 more
}

for category, questions in QUESTIONS.items():
    print(f"\\n=== {category.upper()} ===")
    for q in questions:
        r = ollama.chat(model="llama3.1:8b",
                        messages=[{"role": "user", "content": q + " Answer briefly."}])
        print(f"\\nQ: {q}\\nA: {r['message']['content'][:300]}")</code></pre>
<p>Fill in five questions per category, run it, and score every answer yourself: ✅ correct, ❌ wrong, 🤷 refused. In session we compare maps: the pattern — reliable on stable knowledge, degrading on long-tail, inventing on private — will be visible in <em>everyone's</em> results, on different questions. That shared pattern is the empirical case for this entire course.</p>

<h3>Step 6 · Choose your capstone corpus</h3>
<p>Pick the document collection your system will serve all eight weeks. Criteria:</p>
<ul>
<li><b>You can judge answers.</b> You'll be the ground truth in evaluation weeks — pick a domain you know cold.</li>
<li><b>20+ documents</b>, mostly text (PDF, markdown, HTML all fine). Enough that "just paste it all in" visibly fails.</li>
<li><b>Real questions exist.</b> Someone — you, colleagues, students — actually wants answers from this corpus.</li>
</ul>
<p>Good picks from past cohorts: your own course materials, a product's documentation, a set of research papers, internal process docs.</p>

<div class="box ok"><div class="label">Week 1 checkpoint — done when</div>
<ul>
<li><code>ollama run llama3.1:8b</code> responds</li>
<li><code>uv run python -c "import chromadb"</code> works</li>
<li>Repo initialized, <code>hello_llm.py</code> and <code>probe.py</code> committed</li>
<li>Probe results scored, corpus chosen</li>
<li>One-page retrieval-decision memo: for your corpus, which query categories need retrieval and why</li>
</ul></div>

<div class="box warn"><div class="label">This weekend</div>
<p><b><a href="challenge1.html">Challenge 1: Catch Your Model Lying</a></b> extends Step 5 into the full 20-question probe with a written conclusion — and the stretch goal tests whether temperature changes anything. Reading and video for the week are on the <a href="week1.html">Week 1 page</a>.</p></div>

<div class="pagenav"><a href="week1.html">← Week 1 overview</a><a href="challenge1.html">Challenge 1 →</a></div>
</article>
"""

with open(f"{bs.OUT}/week1-material.html", "w") as f:
    f.write(bs.page("Week 1 Study Material", body))
print("Wrote week1-material.html")
