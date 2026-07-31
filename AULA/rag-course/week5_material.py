#!/usr/bin/env python3
"""Week 5 full study material page. Importing build_site also regenerates the base site."""
import build_site as bs

body = """
<div class="crumb"><a href="index.html">Home</a> / <a href="week5.html">Week 5</a> / Study material</div>
<article>
<div class="kicker">Week 5 · Study Material</div>
<h1>Evaluation: Diagnosing Failures Systematically</h1>
<p class="lede">Until now you've measured <em>retrieval</em>. This week you measure <b>answers</b> — and build the machine that tells you <em>why</em> a bad answer was bad. This is the week that separates people who tinker with RAG from people who ship it: without diagnosis, every fix is a guess, and guesses that happen to work are indistinguishable from guesses that don't.</p>

<h2>Part 1 — The failure taxonomy: three root causes, three different fixes</h2>
<p>A user reports: "the answer was wrong." That report is useless until you localize it. Every wrong RAG answer has exactly one of three root causes, and the fixes share nothing:</p>
<table>
<tr><th>Failure</th><th>What happened</th><th>Where to look</th><th>Fix lives in</th></tr>
<tr><td><b>Retrieval</b></td><td>The supporting text never reached the context window</td><td>Is the right chunk in the retrieved set at all?</td><td>Weeks 2–4: fusion, depth, query rewriting</td></tr>
<tr><td><b>Chunking</b></td><td>It reached the window, but mangled — cut mid-idea, or stripped of the context needed to interpret it</td><td>Read the retrieved chunk cold: could <em>you</em> answer from it?</td><td>Week 3: chunk size, boundaries, titles</td></tr>
<tr><td><b>Generation</b></td><td>Correct, complete context arrived — the model ignored it, contradicted it, or padded with invented detail</td><td>Compare each claim in the answer against the context</td><td>Week 6: prompting, ordering, citations</td></tr>
</table>
<p>The diagnostic order is fixed and non-negotiable: <b>check retrieval first, chunking second, generation last</b>. Most teams debug backwards — they rewrite prompts for hours to fix what was a retrieval miss. The prompt was never the problem.</p>
<div class="box"><div class="label">The one-minute triage</div>
<p>For any bad answer, in order: (1) Is the supporting text in the retrieved set? No → retrieval failure, stop. (2) Is the retrieved chunk self-sufficient — readable and interpretable on its own? No → chunking failure, stop. (3) Then it's generation. Three questions, minutes not hours, and the answer tells you which week's material to revisit.</p></div>

<h2>Part 2 — Metrics for the generation half</h2>
<p>Recall@k and MRR say nothing about the text the user actually reads. Four metrics complete the picture — note how each isolates a different stage:</p>
<table>
<tr><th>Metric</th><th>Question</th><th>Low score means</th></tr>
<tr><td><b>Faithfulness</b></td><td>Is every claim in the answer supported by the retrieved context?</td><td>Generation failure — the model is inventing (the metric that most directly tracks hallucination)</td></tr>
<tr><td><b>Answer relevance</b></td><td>Does the answer actually address the question asked?</td><td>Generation failure — often over-retrieval dragging the model off-topic</td></tr>
<tr><td><b>Context precision</b></td><td>Of what was retrieved, how much was actually needed?</td><td>Noisy retrieval — wasted budget, and a distraction risk</td></tr>
<tr><td><b>Context recall</b></td><td>Of what was needed, how much was retrieved?</td><td>Retrieval failure — the ceiling on everything downstream</td></tr>
</table>
<p>The pairing to internalize: <b>context recall bounds what's possible; faithfulness measures whether the model honored it.</b> High recall + low faithfulness = a prompting problem. Low recall + high faithfulness = a model faithfully answering from the wrong evidence — the most dangerous quadrant, because the answer will be confidently, citably wrong.</p>

<h2>Part 3 — LLM-as-judge, and its biases</h2>
<p>Human grading doesn't scale past a few dozen answers. The standard workaround is to have a strong model grade the output — and it works, provided you know what the judge is bad at:</p>
<ul>
<li><b>Verbosity bias:</b> longer answers score higher, whether or not they're better.</li>
<li><b>Self-preference:</b> judges favor text in their own style — a real problem when the judge and generator are the same model.</li>
<li><b>Position bias:</b> in A/B comparisons, whichever is shown first tends to win. Always test both orders.</li>
<li><b>Poor calibration:</b> ask for 1–10 and you'll get 7s and 8s forever. Binary or 3-point scales are far more reliable.</li>
</ul>
<p>The practical rules: judge <em>one narrow question at a time</em> (never "rate this answer overall"), decompose the answer into claims and check each against the context, use binary verdicts, and — the discipline everyone skips — <b>calibrate against 20 hand-labeled examples</b>. If the judge agrees with you less than ~80% of the time on your own domain, its scores are decoration.</p>

<h2>Part 4 — The golden dataset</h2>
<p>Fifty carefully labeled questions beat five thousand noisy ones. Build yours with a <b>synthesize-then-verify</b> loop: have the LLM draft candidate questions from each document (cheap, gets coverage), then <em>you</em> verify and fix every one (slow, gets truth). Never ship a golden item you haven't read.</p>
<p>Deliberately include the hard cases — the ones that catch regressions no happy-path set will:</p>
<ul>
<li><b>Unanswerable questions</b> your corpus genuinely cannot answer. The correct behavior is refusal; measuring it is how you catch a system that never says "I don't know."</li>
<li><b>Multi-source questions</b> needing two or more documents (they'll matter enormously next week).</li>
<li><b>Near-miss questions</b> whose vocabulary matches a <em>wrong</em> document — the trap your retriever is most likely to fall into.</li>
</ul>

<h2>Lab — build the measurement machine</h2>

<h3>Step 1 · A generation step to evaluate</h3>
<p>You need answers before you can grade them. Create <code>answer.py</code> — a deliberately minimal RAG generator (Week 6 does this properly):</p>
<pre><code>import ollama
from pathlib import Path
from rerank import reranked_search

TEXTS = {p.name: p.read_text(errors="ignore")
         for p in Path("corpus").glob("*") if p.suffix in (".txt", ".md")}

PROMPT = \"\"\"Answer the question using ONLY the context below.
If the context does not contain the answer, say exactly: I don't know.

Context:
{context}

Question: {question}
Answer:\"\"\"

def answer(question, k=3):
    docs = reranked_search(question, k=k)
    context = "\\n\\n---\\n\\n".join(f"[{d}]\\n{TEXTS[d][:2000]}" for d in docs)
    r = ollama.chat(model="llama3.1:8b", messages=[
        {"role": "user", "content": PROMPT.format(context=context, question=question)}])
    return r["message"]["content"].strip(), docs, context</code></pre>

<h3>Step 2 · Golden dataset, synthesized then verified</h3>
<p>Create <code>make_golden.py</code> to draft candidates:</p>
<pre><code>import json, ollama
from pathlib import Path

items = []
for p in list(Path("corpus").glob("*"))[:25]:
    if p.suffix not in (".txt", ".md"): continue
    r = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content":
        "Read the document and write 2 specific questions a real user would ask that "
        "THIS document answers. One question per line, no numbering.\\n\\n"
        + p.read_text(errors="ignore")[:3000]}])
    for q in r["message"]["content"].strip().splitlines():
        q = q.strip("-• ").strip()
        if len(q) &gt; 10:
            items.append({"question": q, "source": p.name, "ground_truth": "", "verified": False})

json.dump(items, open("golden_draft.json", "w"), indent=2, ensure_ascii=False)
print(f"{len(items)} candidates drafted — now verify them by hand")</code></pre>
<p>Then do the unglamorous part: open <code>golden_draft.json</code>, keep ~40 good items, write the correct <code>ground_truth</code> for each, fix wrong <code>source</code> labels, delete nonsense, and hand-add 5 unanswerable + 3 multi-source + 3 near-miss questions. Save as <code>golden.json</code> with <code>verified: true</code>. <b>This file is the most valuable artifact you build this week</b> — it gates every change you make for the rest of the course.</p>

<h3>Step 3 · The judge</h3>
<p>Create <code>judge.py</code> — claim-level faithfulness plus relevance, both binary:</p>
<pre><code>import ollama

def ask(prompt):
    r = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": prompt}])
    return r["message"]["content"].strip().upper()

def faithfulness(answer_text, context):
    claims = [c.strip() for c in answer_text.split(".") if len(c.strip()) &gt; 15]
    if not claims: return 1.0
    supported = 0
    for c in claims:
        v = ask(f"Context:\\n{context[:4000]}\\n\\nClaim: {c}\\n\\n"
                f"Is this claim fully supported by the context? Reply YES or NO only.")
        supported += v.startswith("YES")
    return supported / len(claims)

def relevance(question, answer_text):
    v = ask(f"Question: {question}\\nAnswer: {answer_text}\\n\\n"
            f"Does the answer address the question asked? Reply YES or NO only.")
    return 1.0 if v.startswith("YES") else 0.0</code></pre>

<h3>Step 4 · Calibrate the judge before trusting it</h3>
<p>Non-negotiable. Run 20 golden items, record the judge's verdicts, then grade the same 20 yourself and compute agreement:</p>
<pre><code>agreement = matching_verdicts / 20
# ≥0.8  → usable for bulk evaluation
# &lt;0.8  → tighten the prompt (shorter claims, stricter wording) and re-calibrate</code></pre>
<p>Write the agreement number in your README next to every judge-derived metric. A metric without its calibration is a rumor.</p>

<h3>Step 5 · The failure audit</h3>
<p>Create <code>audit.py</code> — run the full golden set and auto-classify every failure by the Part 1 taxonomy:</p>
<pre><code>import json
from answer import answer
from judge import faithfulness, relevance

golden = json.load(open("golden.json"))
rows = []
for item in golden:
    ans, docs, ctx = answer(item["question"])
    retrieved_ok = item["source"] in docs                 # was the right doc retrieved?
    f = faithfulness(ans, ctx)
    r = relevance(item["question"], ans)
    if not retrieved_ok:            cause = "retrieval"
    elif f &lt; 0.7:                   cause = "generation"
    elif r == 0:                    cause = "generation"
    else:                           cause = "ok"
    rows.append({**item, "answer": ans, "docs": docs,
                 "faithfulness": f, "relevance": r, "cause": cause})

json.dump(rows, open("audit_results.json", "w"), indent=2, ensure_ascii=False)
from collections import Counter
print(Counter(r["cause"] for r in rows))</code></pre>
<p>The script separates retrieval from generation automatically. <b>Chunking failures it cannot see</b> — those need your eyes: pull 5 cases labeled "generation", read the retrieved chunk cold, and ask whether a careful human could have answered from it. If not, relabel: chunking. That's the manual step no framework does for you.</p>

<h3>Step 6 · Write the three tickets</h3>
<p>Turn the audit into <code>failure_audit.md</code>: counts per cause, two example transcripts each, and the three highest-impact fixes with evidence. Not "improve retrieval" — <b>"9 of 14 retrieval failures were paraphrase queries; add query rewriting (Week 4, measured +0.2 R@5 on 3 test queries)."</b> That is what an engineering ticket looks like.</p>

<div class="box warn"><div class="label">Troubleshooting</div>
<ul>
<li><b>Judging is slow:</b> every claim is an LLM call. Start with 20 golden items; use <code>llama3.2:3b</code> for judging while iterating, then re-run the final audit on the 8b model.</li>
<li><b>Judge always says YES:</b> classic leniency. Add "Be strict. If the context only partially supports the claim, answer NO." Re-calibrate after any prompt change.</li>
<li><b>Faithfulness is 1.0 everywhere:</b> your sentence-splitter is producing fragments too short to falsify. Filter to claims &gt;15 characters (as above) or split on sentence boundaries properly.</li>
<li><b>Unanswerable questions scored as failures:</b> they need inverted grading — the correct answer is "I don't know". Handle them as a separate section of the report.</li>
</ul></div>

<div class="box ok"><div class="label">Week 5 checkpoint — done when</div>
<ul>
<li><code>golden.json</code> exists: ~50 hand-verified items including unanswerable, multi-source, and near-miss cases</li>
<li><code>judge.py</code> is calibrated against your own labels, agreement recorded in the README</li>
<li><code>audit_results.json</code> classifies every failure; 5 "generation" cases manually re-checked for chunking</li>
<li><code>failure_audit.md</code> has counts, transcripts, and 3 evidence-backed tickets</li>
<li>Committed: <code>git commit -m "Week 5: eval harness, golden set, failure audit"</code></li>
</ul></div>

<div class="box warn"><div class="label">This weekend</div>
<p><b><a href="challenge5.html">Challenge 5: The Failure Audit</a></b> — the full audit plus the stretch: have the judge label the same failures independently, compute agreement with your labels, and decide whether you'd trust it to gate a deploy. Reading and video on the <a href="week5.html">Week 5 page</a>.</p></div>

<div class="pagenav"><a href="week5.html">← Week 5 overview</a><a href="challenge5.html">Challenge 5 →</a></div>
</article>
"""

with open(f"{bs.OUT}/week5-material.html", "w") as f:
    f.write(bs.page("Week 5 Study Material", body))
print("Wrote week5-material.html")
