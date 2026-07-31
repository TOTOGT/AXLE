#!/usr/bin/env python3
"""Week 7 full study material page. Importing build_site also regenerates the base site."""
import build_site as bs

body = """
<div class="crumb"><a href="index.html">Home</a> / <a href="week7.html">Week 7</a> / Study material</div>
<article>
<div class="kicker">Week 7 · Study Material</div>
<h1>Agentic RAG: Retrieval-Aware Workflows</h1>
<p class="lede">Your Week 6 router made one decision, once, with a fixed script behind it. This week the model takes the wheel: it decides whether to search, what to search for, whether what came back is enough, and whether to go again. The honest finding this week is often that the agent <em>loses</em> — and knowing exactly when is the professional skill.</p>

<h2>Part 1 — Retrieval as a tool, not a pipeline stage</h2>
<p>Every system you've built so far shares a shape: <em>always retrieve, once, then answer</em>. The query is a passive input; the pipeline is a fixed track. An agent inverts the relationship — retrieval becomes a <b>tool the model chooses to invoke</b>, with arguments it writes itself.</p>
<p>That single change unlocks four behaviors your pipeline can't express:</p>
<ul>
<li><b>Skip retrieval</b> when the question doesn't need it (Week 1's decision, now made per query, by the model).</li>
<li><b>Write a better query</b> than the user did — the Week 4 rewrite, applied selectively.</li>
<li><b>Search again</b> after seeing that the first results were insufficient.</li>
<li><b>Choose a source</b> when several indexes exist (docs vs. FAQ vs. changelog).</li>
</ul>
<p>The cost is control. A pipeline's behavior is inspectable and its latency is predictable; an agent's is neither. You are trading determinism for adaptability — which is exactly why this week ends with a measurement, not a celebration.</p>

<h2>Part 2 — The ReAct loop</h2>
<p>ReAct (Reason + Act) is the pattern nearly all agent frameworks implement, usually with far more ceremony than it needs. The loop:</p>
<pre><code>┌─────────────────────────────────────────────┐
│  THOUGHT   what do I know? what's missing?  │
│  ACTION    search("...")  or  answer("...") │
│  OBSERVE   results appended to the trace    │
└──────────────── repeat, max N ──────────────┘</code></pre>
<p>Three implementation realities the tutorials gloss over:</p>
<p><b>The trace is the state.</b> There's no hidden memory — the accumulated thought/action/observation text <em>is</em> everything the model knows. Manage that text and you manage the agent.</p>
<p><b>The stop condition is load-bearing.</b> Without a hard iteration cap, agents loop: search, get the same results, decide they're insufficient, search again. Always cap (3–5 hops), and always define a fallback answer when the cap is hit.</p>
<p><b>Small models drift from output formats.</b> An 8B model will eventually emit prose where you expected <code>ACTION: search(...)</code>. Parse defensively and treat unparseable output as "answer now" rather than crashing. Robustness here is most of the engineering.</p>

<h2>Part 3 — Self-correction: draft, critique, re-retrieve</h2>
<p>A second, complementary loop. Instead of deciding <em>before</em> answering whether context suffices, the agent answers, then audits itself:</p>
<ol>
<li><b>Draft</b> an answer from the retrieved context.</li>
<li><b>Critique</b> it: which claims aren't supported by the sources? (You already built this in Week 5 — it's your faithfulness judge, pointed inward.)</li>
<li><b>Re-retrieve</b> for the unsupported claims specifically.</li>
<li><b>Revise</b> with the enlarged context.</li>
</ol>
<p>This measurably raises faithfulness and roughly doubles cost and latency. Two warnings worth stating to students plainly: models are weaker at critiquing their own output than others' (self-preference bias, from Week 5), and more than one revision cycle rarely pays. One cycle, measured — not a philosophy.</p>

<h2>Part 4 — Context engineering for agents</h2>
<p>Loops accumulate text fast: four hops × four chunks each = sixteen chunks in the window, most of them from queries that turned out to be wrong turns. Left unmanaged, the agent drowns in its own history — and "lost in the middle" (Week 6) hits hardest at exactly the moment the agent needs to reason over everything it gathered.</p>
<p>Three strategies, in increasing order of effort:</p>
<table>
<tr><th>Strategy</th><th>How</th><th>Trade-off</th></tr>
<tr><td><b>Windowing</b></td><td>Keep only the last N observations verbatim</td><td>Simplest; can drop the one useful early hit</td></tr>
<tr><td><b>Summarizing</b></td><td>Compress old observations into a running note</td><td>Cheap on tokens; lossy — details vanish and can't be cited</td></tr>
<tr><td><b>Scratchpad</b></td><td>Extract facts found so far into a structured list; keep raw text only for the current hop</td><td>Best quality; most code</td></tr>
</table>
<p>This is the heart of the course title. Retrieval decides what <em>could</em> enter the window; context engineering decides what <em>does</em> — and in an agent, that decision is made repeatedly, under a growing budget, which is what makes it hard.</p>

<h2>Lab — build the agent, then interrogate it</h2>

<h3>Step 1 · The tool interface</h3>
<p>Create <code>agent_tools.py</code> — thin wrappers over what you already built:</p>
<pre><code>from retrieve import retrieve_chunks

def search(query, k=3):
    chunks = retrieve_chunks(query, k=k)
    return [{"doc": c["doc"], "text": c["text"][:900]} for c in chunks]

TOOL_SPEC = \"\"\"Available actions:
  SEARCH: &lt;query&gt;   — search the knowledge base
  ANSWER: &lt;answer&gt;  — give the final answer with [doc] citations\"\"\"</code></pre>

<h3>Step 2 · The ReAct loop</h3>
<p>Create <code>agent.py</code>:</p>
<pre><code>import ollama, re
from agent_tools import search, TOOL_SPEC

SYSTEM = \"\"\"You answer questions using a knowledge base.

{tools}

Rules:
- Reply with EXACTLY ONE line: either "SEARCH: ..." or "ANSWER: ...".
- Search when you lack information. Answer when the observations suffice.
- Never answer from prior knowledge; only from observations.
- If after searching the knowledge base still lacks the answer, ANSWER: I don't know.\"\"\"

def run_agent(question, max_hops=4, verbose=True):
    trace = [f"QUESTION: {question}"]
    used_chunks = []
    for hop in range(max_hops):
        prompt = (SYSTEM.format(tools=TOOL_SPEC) + "\\n\\n" + "\\n".join(trace)
                  + "\\n\\nYour next line:")
        line = ollama.chat(model="llama3.1:8b",
                           messages=[{"role": "user", "content": prompt}]
                           )["message"]["content"].strip().splitlines()[0]
        if verbose: print(f"  hop {hop+1}: {line[:100]}")

        m = re.match(r"SEARCH:\\s*(.+)", line, re.I)
        if m:
            q = m.group(1).strip().strip('"')
            results = search(q)
            used_chunks.extend(results)
            obs = "\\n".join(f"  [{r['doc']}] {r['text'][:400]}" for r in results) or "  (nothing found)"
            trace += [f"THOUGHT: I need to search for: {q}", f"OBSERVATION:\\n{obs}"]
            continue

        m = re.match(r"ANSWER:\\s*(.+)", line, re.I | re.S)
        if m:
            return m.group(1).strip(), {"hops": hop + 1, "chunks": used_chunks, "trace": trace}

        # defensive: model drifted from the format — treat the text as the answer
        return line, {"hops": hop + 1, "chunks": used_chunks, "trace": trace, "drift": True}

    return "I don't know.", {"hops": max_hops, "chunks": used_chunks,
                             "trace": trace, "hit_cap": True}</code></pre>
<p>Run it on a multihop question from your gauntlet and watch the hops print. The first time an agent writes its own second query and finds what it was missing is the moment this week clicks.</p>

<h3>Step 3 · Sufficiency check and self-correction</h3>
<p>Create <code>self_correct.py</code>:</p>
<pre><code>import ollama
from generate import generate
from retrieve import retrieve_chunks
from generate import PROMPT, format_sources

def unsupported_claims(answer_text, chunks):
    ctx = "\\n\\n".join(c["text"] for c in chunks)[:5000]
    r = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content":
        f"Context:\\n{ctx}\\n\\nAnswer:\\n{answer_text}\\n\\n"
        f"List any claims in the answer NOT supported by the context, one per line. "
        f"If all claims are supported, reply exactly: NONE"}])
    text = r["message"]["content"].strip()
    return [] if text.upper().startswith("NONE") else \\
           [c.strip("-• ") for c in text.splitlines() if len(c.strip()) &gt; 10]

def corrected_answer(question):
    draft, chunks = generate(question)
    gaps = unsupported_claims(draft, chunks)
    if not gaps:
        return draft, {"revised": False, "gaps": []}
    for gap in gaps[:2]:                      # re-retrieve for what was unsupported
        chunks.extend(retrieve_chunks(gap, k=2))
    for i, c in enumerate(chunks, 1):
        c["id"] = f"S{i}"
    r = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content":
        PROMPT.format(sources=format_sources(chunks), question=question)}])
    return r["message"]["content"].strip(), {"revised": True, "gaps": gaps}</code></pre>

<h3>Step 4 · Context management</h3>
<p>Add windowing to <code>run_agent</code>: keep the question and the last two observations verbatim, and replace older observations with a one-line summary. Re-run your gauntlet. Did quality hold? Did token use drop? Break it deliberately — window down to one observation and watch a multihop question fail because hop 1's finding was evicted. <b>That controlled failure is the lesson</b>; students who have caused it never forget why context management is a design decision.</p>

<h3>Step 5 · The head-to-head — this week's real deliverable</h3>
<p>Create <code>compare.py</code>: run your full golden set through three systems — Week 6 pipeline, agent, self-correcting pipeline — recording per item: correctness (Week 5 judge), faithfulness, latency, and token count. Then break results down <b>by query type</b>, because the aggregate hides the finding:</p>
<table>
<tr><th>Query type</th><th>Expect</th></tr>
<tr><td>Simple factual</td><td>Pipeline usually wins — same answer, a fraction of the cost</td></tr>
<tr><td>Multihop</td><td>Agent wins — this is what the loop is for</td></tr>
<tr><td>Unanswerable</td><td>Agent often <em>worse</em>: it searches repeatedly before admitting defeat, burning tokens; sometimes it talks itself into an answer</td></tr>
<tr><td>Ambiguous / vague</td><td>Agent wins when it rewrites the query well; loses when it wanders</td></tr>
</table>
<p>Write the deployment recommendation: which traffic goes to which system, with numbers. "Route multihop to the agent, everything else to the pipeline — the agent costs 3.4× the tokens for +0.02 faithfulness on simple queries" is a professional conclusion. "Agents are better" is not.</p>

<div class="box warn"><div class="label">Troubleshooting</div>
<ul>
<li><b>Agent never searches:</b> it's answering from parametric memory. Strengthen the rule ("You have NO prior knowledge of this domain") and make the first hop a forced search.</li>
<li><b>Agent loops on the same query:</b> add the previous queries to the prompt with "Do not repeat these searches", and keep the cap at 3–4.</li>
<li><b>Format drift (prose instead of SEARCH:/ANSWER:):</b> expected with 8B models — the defensive branch handles it. Count drift events; it's a legitimate metric for your comparison table.</li>
<li><b>Everything is slow:</b> agents make 3–8 LLM calls per question. Test on 15 golden items, not 50, while iterating.</li>
</ul></div>

<div class="box ok"><div class="label">Week 7 checkpoint — done when</div>
<ul>
<li><code>agent.py</code> runs a ReAct loop with a hard hop cap and defensive parsing</li>
<li>Sufficiency check and one self-correction cycle implemented</li>
<li>Context management added, and its failure mode demonstrated deliberately</li>
<li>Three-system comparison broken down by query type: quality, latency, tokens</li>
<li>A written deployment recommendation with numbers behind it</li>
<li>Committed: <code>git commit -m "Week 7: agentic RAG + head-to-head comparison"</code></li>
</ul></div>

<div class="box warn"><div class="label">This weekend</div>
<p><b><a href="challenge7.html">Challenge 7: Agent vs. Pipeline</a></b> — the rigorous head-to-head, with the stretch goal of building the router you just recommended and measuring blended cost and quality. Reading and videos on the <a href="week7.html">Week 7 page</a>.</p></div>

<div class="pagenav"><a href="week7.html">← Week 7 overview</a><a href="challenge7.html">Challenge 7 →</a></div>
</article>
"""

with open(f"{bs.OUT}/week7-material.html", "w") as f:
    f.write(bs.page("Week 7 Study Material", body))
print("Wrote week7-material.html")
