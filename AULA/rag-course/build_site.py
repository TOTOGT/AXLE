#!/usr/bin/env python3
"""Generate the AXLE RAG & Context Engineering course site."""
import os

OUT = "/sessions/focused-nice-cray/mnt/AXLE/rag-course/site"
COURSE = "RAG &amp; Context Engineering"
SUBTITLE = "Building Production-Grade AI Systems"
INSTRUCTOR = "Pablo Grossi"
BRAND = "AXLE"

CSS = """
:root{--bg:#0f1117;--panel:#181b24;--panel2:#1f2330;--text:#e8eaf0;--muted:#9aa3b5;
--accent:#4f8ef7;--accent2:#7c5cff;--ok:#3ecf8e;--warn:#f7b84f;--border:#2a2f3e;
--radius:14px;--maxw:880px}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;line-height:1.65}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
header.site{background:linear-gradient(135deg,#141827 0%,#1a1440 100%);border-bottom:1px solid var(--border);padding:18px 24px}
header.site .inner{max-width:var(--maxw);margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
.brand{font-weight:800;letter-spacing:2px;color:#fff;font-size:15px}
.brand span{color:var(--accent)}
nav.top a{color:var(--muted);margin-left:18px;font-size:14px;font-weight:600}
nav.top a:hover{color:#fff;text-decoration:none}
main{max-width:var(--maxw);margin:0 auto;padding:40px 24px 80px}
.hero{padding:60px 0 40px;text-align:center}
.hero h1{font-size:40px;line-height:1.15;background:linear-gradient(90deg,#fff,#9db8ff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:14px}
.hero p.tag{color:var(--muted);font-size:19px;max-width:640px;margin:0 auto 28px}
.pills{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:30px}
.pill{background:var(--panel);border:1px solid var(--border);border-radius:999px;padding:7px 16px;font-size:13px;color:var(--muted)}
.pill b{color:var(--text)}
.cta{display:inline-block;background:linear-gradient(90deg,var(--accent),var(--accent2));color:#fff;font-weight:700;padding:13px 30px;border-radius:10px;font-size:16px}
.cta:hover{text-decoration:none;opacity:.92}
h2.sec{font-size:22px;margin:48px 0 18px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);padding:22px;transition:border-color .15s}
.card:hover{border-color:var(--accent)}
.card .wk{font-size:12px;font-weight:700;letter-spacing:1.5px;color:var(--accent);text-transform:uppercase;margin-bottom:6px}
.card h3{font-size:17px;margin-bottom:8px}
.card h3 a{color:var(--text)}
.card p{font-size:14px;color:var(--muted);margin-bottom:12px}
.card .links a{font-size:13px;font-weight:600;margin-right:16px}
.crumb{font-size:13px;color:var(--muted);margin-bottom:26px}
.crumb a{color:var(--muted)}.crumb a:hover{color:var(--accent)}
article h1{font-size:30px;line-height:1.2;margin-bottom:6px}
.kicker{font-size:12px;font-weight:700;letter-spacing:2px;color:var(--accent);text-transform:uppercase;margin-bottom:10px}
.lede{color:var(--muted);font-size:17px;margin:14px 0 30px}
article h2{font-size:20px;margin:38px 0 14px;color:#fff}
article h3{font-size:16px;margin:22px 0 8px;color:#cdd6ea}
article p{margin-bottom:14px}
article ul,article ol{margin:0 0 16px 24px}
article li{margin-bottom:8px}
.box{background:var(--panel);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:10px;padding:18px 20px;margin:22px 0}
.box.ok{border-left-color:var(--ok)}
.box.warn{border-left-color:var(--warn)}
.box .label{font-size:11px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
code{background:var(--panel2);border:1px solid var(--border);border-radius:6px;padding:2px 7px;font-size:.88em;font-family:'SF Mono',Menlo,Consolas,monospace}
pre{background:#12141c;border:1px solid var(--border);border-radius:10px;padding:16px;overflow-x:auto;margin:16px 0}
pre code{background:none;border:none;padding:0;font-size:13px;line-height:1.6}
.res{display:flex;flex-direction:column;gap:10px;margin:14px 0}
.res a{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px 16px;font-size:14px;font-weight:600}
.res a:hover{border-color:var(--accent);text-decoration:none}
.res a span{display:block;font-weight:400;font-size:12.5px;color:var(--muted);margin-top:3px}
.pagenav{display:flex;justify-content:space-between;margin-top:56px;padding-top:22px;border-top:1px solid var(--border);gap:12px}
.pagenav a{font-size:14px;font-weight:700}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--border)}
th{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:1px}
footer.site{border-top:1px solid var(--border);padding:26px 24px;text-align:center;color:var(--muted);font-size:13px}
@media(max-width:600px){.hero h1{font-size:28px}.grid{grid-template-columns:1fr}}
"""

def page(title, body, depth=0):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · {COURSE.replace('&amp;','&')}</title>
<style>{CSS}</style>
</head>
<body>
<header class="site"><div class="inner">
<div class="brand">{BRAND} <span>·</span> {COURSE}</div>
<nav class="top"><a href="index.html">Home</a><a href="syllabus.html">Syllabus</a><a href="week1.html">Start Week 1</a></nav>
</div></header>
<main>
{body}
</main>
<footer class="site">{COURSE} — {SUBTITLE}<br>Instructor: {INSTRUCTOR} · {BRAND} · 2026</footer>
</body>
</html>"""

def resources(items):
    out = '<div class="res">'
    for label, desc, url in items:
        out += f'<a href="{url}" target="_blank" rel="noopener">{label}<span>{desc}</span></a>'
    return out + '</div>'

def ul(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ol(items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'

W = []  # (num, title, tagline, body_fn)

# ---------------- WEEK CONTENT ----------------
weeks = [
dict(num=1, material=True, title="When (and When Not) to Retrieve",
tag="What language models actually know, where they hallucinate, and the engineering decision that defines every RAG system.",
objectives=[
 "Explain the difference between parametric knowledge and externally grounded knowledge",
 "Identify the query categories where retrieval adds value — and where it adds only cost",
 "Set up a professional local development environment: Ollama, uv, git",
 "Empirically map a model's knowledge boundaries"],
concepts=[
 ("Parametric knowledge and its limits", "Everything a model 'knows' is compressed into its weights during training. That compression is lossy: frequent facts survive; rare ones blur. The model has no flag for 'I never learned this' — which is why it confabulates fluently."),
 ("The context window as a budget", "Whatever the model didn't memorize must arrive through the prompt. The context window is finite, and quality degrades as it fills. Context engineering is the discipline of spending that budget well."),
 ("The retrieval decision", "Retrieval earns its cost on: private data, fresh data, long-tail facts, and auditable citations. It wastes cost on: stable general knowledge, reasoning tasks, and creative work. Production systems route between these cases."),
 ("Alternatives to RAG", "Long-context stuffing, fine-tuning, and tool calls each solve part of the problem. You will be able to argue when each beats retrieval — a question every system design interview and every architecture review asks.")],
lab=[
 "Install Ollama, pull <code>llama3.1:8b</code> and <code>nomic-embed-text</code>",
 "Create the course repo with <code>uv</code>; first commit",
 "Write <code>hello_llm.py</code> — your first programmatic call to a local model",
 "Probe the model's knowledge boundaries across query categories",
 "Choose your capstone corpus (20+ documents in a domain you can judge)"],
checkpoint="Working local environment, committed repo, and a one-page retrieval-decision memo for your capstone domain.",
reading=[("Lewis et al. (2020) — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks","The paper that named RAG. Read the intro and §2; skim the rest.","https://arxiv.org/abs/2005.11401")],
videos=[("Andrej Karpathy — [1hr Talk] Intro to Large Language Models","The best single hour on what an LLM is and isn't. Watch the sections on the 'LLM OS' and hallucination.","https://www.youtube.com/watch?v=zjkBMFhNj_g")],
reflect=[
 "Which model failure surprised you most, and why?",
 "If you could fix only one failure category with retrieval, which delivers most value to your capstone users?",
 "When the model didn't know, did it refuse or confabulate? Why does that difference matter in production?"]),

dict(num=2, material=True, title="Classical Retrieval: BM25 and the Inverted Index",
tag="Fifty years of search engineering in one week — and the baseline every later technique must beat.",
objectives=[
 "Build an inverted index and explain why it makes search fast",
 "Derive TF-IDF and BM25 from first principles",
 "Evaluate retrieval with Recall@k, Precision@k, and MRR",
 "Establish a measured baseline over your capstone corpus"],
concepts=[
 ("The inverted index", "Instead of scanning every document per query, map each term to the documents containing it. Every search engine since the 1970s — including Elasticsearch today — is built on this structure."),
 ("From counting to TF-IDF", "Term frequency says a document mentioning your term often is probably relevant. Inverse document frequency says rare terms carry signal and common ones don't. Multiply them and search 'just works' surprisingly often."),
 ("BM25: TF-IDF grown up", "Two refinements made BM25 the 25-year industry standard: term-frequency saturation (the 50th occurrence shouldn't count like the 2nd — parameter k1) and length normalization (long documents match everything by accident — parameter b)."),
 ("Measuring retrieval", "Recall@k: of the relevant documents, how many made the top k? MRR: how high does the first relevant one rank? You cannot improve what you do not measure — these metrics become the spine of Week 5.")],
lab=[
 "Build an inverted index + TF-IDF scorer in pure Python (~60 lines) over your corpus",
 "Swap in <code>rank_bm25</code>; compare rankings against your hand-rolled version",
 "Write 10 test queries with known-relevant documents",
 "Compute Recall@5 and MRR — your official course baseline"],
checkpoint="<code>bm25_baseline.py</code>, <code>eval_queries.json</code>, and a metrics table, committed. Every later week must beat these numbers or justify itself.",
reading=[("Manning, Raghavan &amp; Schütze — Introduction to Information Retrieval (Ch. 1 &amp; 6)","The standard text, free online. Boolean retrieval and TF-IDF scoring.","https://nlp.stanford.edu/IR-book/")],
videos=[("A no-nonsense intro to BM25","Compact, practical walkthrough of the scoring function.","https://www.youtube.com/watch?v=TW9vHU1GpU4"),
        ("BM25 retrieval model — university IR lecture","A deeper academic treatment if you want the derivation.","https://www.youtube.com/watch?v=p8st3g_Y39I")],
reflect=[
 "Why does IDF alone explain most of why keyword search works?",
 "When would you tune k1 and b rather than accept the defaults?",
 "Which of your failure queries do you predict embeddings will fix — and which won't they?"]),

dict(num=3, material=True, title="Semantic Retrieval: Embeddings and Vector Search",
tag="Meaning as geometry: how embeddings find what keywords miss — and the chunking decision that quietly dominates quality.",
objectives=[
 "Explain what an embedding is and why cosine similarity approximates semantic relatedness",
 "Design and compare chunking strategies empirically",
 "Stand up a vector database and query it programmatically",
 "Benchmark semantic retrieval against your BM25 baseline"],
concepts=[
 ("Embeddings: meaning as coordinates", "An embedding model maps text to a point in high-dimensional space where distance tracks meaning. 'Car' and 'automobile' land near each other even though they share no letters — exactly the failure BM25 can't fix."),
 ("Approximate nearest-neighbor search", "Comparing a query against millions of vectors exactly is too slow. ANN indexes (HNSW, IVF) trade a sliver of accuracy for orders-of-magnitude speed. You'll learn what those trade-offs cost you."),
 ("Chunking: the highest-leverage decision", "Documents must be split before embedding. Too small: fragments lose context. Too large: the signal drowns and the context budget bloats. Chunk size, overlap, and structure-awareness routinely matter more than the choice of embedding model."),
 ("Vector databases", "Chroma, Qdrant, pgvector, and friends persist embeddings, filter on metadata, and serve ANN queries. You'll learn what they actually do — and why they're not magic, just indexes plus bookkeeping.")],
lab=[
 "Embed your corpus with <code>nomic-embed-text</code> via Ollama",
 "Index in Chroma; wire a query pipeline",
 "Run three chunking strategies: fixed-size, paragraph-based, structure-aware",
 "Score each against your Week 2 query set; compare with the BM25 baseline head-to-head"],
checkpoint="A vector index plus a chunking comparison table with real numbers — and a verdict on which queries semantics fixed and which it broke.",
reading=[("Vector Embeddings Explained — Weaviate","A clear, practitioner-level explanation of embeddings and similarity.","https://weaviate.io/blog/vector-embeddings-explained")],
videos=[("What Are Embeddings? (Visual Breakdown)","Visual intuition for how meaning becomes geometry.","https://www.youtube.com/watch?v=03LdHj6miTE"),
        ("Text embeddings &amp; semantic search","How transformer models produce document and query vectors.","https://www.youtube.com/watch?v=OATCgQtNX2o")],
reflect=[
 "Which of Week 2's 'Break BM25' failures did embeddings fix? Which survived?",
 "Did any query get <em>worse</em> under semantic search? What does that tell you?",
 "Why might a smaller chunk retrieve better but generate worse answers?"]),

dict(num=4, material=True, title="Hybrid Retrieval and Reranking",
tag="Neither keywords nor vectors win alone. Production systems fuse both — then let a heavier model re-order the shortlist.",
objectives=[
 "Fuse keyword and semantic results with Reciprocal Rank Fusion",
 "Add a cross-encoder reranker and measure its lift",
 "Apply query rewriting and expansion techniques",
 "Justify each pipeline stage with measured evidence"],
concepts=[
 ("Why hybrid wins", "BM25 nails exact terms, codes, and names; embeddings nail paraphrase and synonymy. Real query traffic contains both. Fusing the two result lists covers each system's blind spots."),
 ("Reciprocal Rank Fusion", "RRF combines ranked lists using only positions — no score normalization headaches. Simple, robust, and the default answer in production. You'll implement it in a dozen lines."),
 ("Cross-encoder reranking", "Bi-encoders (embeddings) score query and document independently — fast but shallow. A cross-encoder reads them <em>together</em> — slow but precise. The pattern: retrieve 50 candidates cheaply, rerank the top handful expensively."),
 ("Query understanding", "Users write bad queries. Rewriting, expansion, and HyDE (embedding a hypothetical answer instead of the question) reshape queries before retrieval ever runs.")],
lab=[
 "Implement RRF over your BM25 + vector retrievers",
 "Add a cross-encoder reranker (sentence-transformers) on the top 20 candidates",
 "Measure the lift of each stage separately: baseline → hybrid → +rerank",
 "Test query rewriting on your worst-performing queries"],
checkpoint="A staged pipeline where every component earns its place with numbers: hybrid must beat both parents, reranking must beat plain hybrid.",
reading=[("Hybrid Search and Re-Ranking in Production RAG — Towards Data Science","What production teams actually deploy and why.","https://towardsdatascience.com/hybrid-search-and-re-ranking-in-production-rag/")],
videos=[("Hybrid Retrieval &amp; Reranking for RAG Systems: BM25, Vector Search, RRF &amp; Cross-Encoders","The full modern retrieval architecture in one video.","https://www.youtube.com/watch?v=PP49RulTXp8"),
        ("Advanced RAG — Reranking with Cross Encoders","Hands-on reranking implementation.","https://www.youtube.com/watch?v=ZFbaA9eM0uo")],
reflect=[
 "Why is rank fusion more robust than score fusion across different retrievers?",
 "Reranking added latency. For your capstone's users, is the quality lift worth it?",
 "Where in your pipeline would query rewriting help most — and how would you prove it?"]),

dict(num=5, material=True, title="Evaluation: Diagnosing Failures Systematically",
tag="'It looks right' is not evaluation. This week you build the measurement machine that turns debugging from guesswork into diagnosis.",
objectives=[
 "Distinguish retrieval failures from generation failures from chunking failures",
 "Implement faithfulness, answer relevance, and context precision/recall metrics",
 "Use LLM-as-judge responsibly, knowing its biases",
 "Build a golden dataset cheaply and maintain it"],
concepts=[
 ("The failure taxonomy", "A wrong answer has exactly three root causes: the right context never arrived (retrieval failure), it arrived but the model ignored or contradicted it (generation failure), or it arrived mangled (chunking failure). Each has a different fix — diagnosis must come first."),
 ("Generation metrics", "Faithfulness: is every claim in the answer supported by the retrieved context? Answer relevance: does it address the question? Context precision/recall: was the retrieved context the right context? Together these localize the failure."),
 ("LLM-as-judge", "Using a strong model to grade answers scales evaluation dramatically — but judges prefer verbose answers, their own phrasing, and the first option shown. You'll learn the calibration rituals that keep judge scores honest."),
 ("Golden datasets", "Fifty carefully labeled question-answer-source triples beat five thousand noisy ones. You'll build yours with a synthesis-then-verify loop over your own corpus.")],
lab=[
 "Build an evaluation harness (RAGAS or hand-rolled) over your Week 4 pipeline",
 "Generate a golden dataset from your corpus; hand-verify every item",
 "Run a full failure audit: label every bad answer with its root cause",
 "Set up the harness to run on every future pipeline change"],
checkpoint="An eval suite plus a failure taxonomy for your system. This is your debugging compass for the rest of the program.",
reading=[("RAG Evaluation Metrics — Confident AI","Answer relevancy, faithfulness, contextual precision and recall, clearly explained.","https://www.confident-ai.com/blog/rag-evaluation-metrics-answer-relevancy-faithfulness-and-more"),
         ("RAGAS documentation — Faithfulness","How the leading open-source framework computes it.","https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/")],
videos=[("RAG Evaluation Metrics Explained: Context Precision, Recall, Relevancy &amp; Faithfulness","Each core metric with worked examples.","https://www.youtube.com/watch?v=wOoYP55eYF0")],
reflect=[
 "Of your failures, what fraction were retrieval vs. generation vs. chunking? Did that surprise you?",
 "Where would an LLM judge disagree with your human judgment on your own domain?",
 "What is the smallest golden dataset you'd trust to gate a production deploy?"]),

dict(num=6, material=True, title="End-to-End RAG and Multihop Retrieval",
tag="Wiring retrieval into generation properly — then handling the questions no single document can answer.",
objectives=[
 "Assemble the full retrieve → construct → generate → cite pipeline",
 "Engineer prompts that resist 'lost in the middle' degradation",
 "Decompose complex questions into retrievable sub-questions",
 "Handle multihop queries with iterative retrieval"],
concepts=[
 ("Prompt construction is context engineering", "Where context appears in the window matters: models attend best to the start and end, worst to the middle. Ordering, formatting, and citation scaffolding measurably change answer quality."),
 ("Grounded citation", "Production answers cite sources. You'll design a citation format the model reliably follows, and verify citations point at text that actually supports the claim."),
 ("Query decomposition", "'Which of our courses shares prerequisites with the one Maria teaches?' requires two lookups. Decomposition splits complex questions into sub-queries, retrieves for each, and synthesizes."),
 ("Iterative and multihop retrieval", "Sometimes hop 2 depends on hop 1's answer. The pipeline becomes a loop: retrieve, read, decide what's still missing, retrieve again. This is the bridge to agents in Week 7.")],
lab=[
 "Wire your Week 4 retriever into a full generation pipeline with citations",
 "A/B test context ordering and formatting with your Week 5 harness",
 "Implement query decomposition; route simple queries past it",
 "Build iterative retrieval for genuine multihop questions from your corpus"],
checkpoint="A complete RAG system answering single-hop and multihop questions with verifiable citations — evaluated, of course.",
reading=[("Liu et al. — Lost in the Middle: How Language Models Use Long Contexts","The paper behind the ordering effects you'll measure yourself.","https://arxiv.org/abs/2307.03172"),
         ("MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries","How multihop capability is benchmarked.","https://arxiv.org/abs/2401.15391")],
videos=[("Advanced RAG Course: Retrieval &amp; Reranking Techniques","A consolidated tour of the advanced pipeline patterns this week assembles.","https://www.youtube.com/watch?v=_kpxLkH5vY0")],
reflect=[
 "Did context ordering change your metrics? By how much?",
 "What kinds of questions in your domain are inherently multihop?",
 "When does decomposition hurt — and how would your router detect those cases?"]),

dict(num=7, material=True, title="Agentic RAG: Retrieval-Aware Workflows",
tag="From pipeline to agent: the model decides when to search, judges its own context, and re-queries until it can answer.",
objectives=[
 "Reframe retrieval as a tool the model invokes deliberately",
 "Implement a ReAct-style reason-act-observe loop",
 "Build self-correction: draft, critique, re-retrieve",
 "Route across multiple indexes and sources"],
concepts=[
 ("Retrieval as a tool", "Static pipelines retrieve once, always, for everything. An agent decides: search or answer directly? Which index? What query? The Week 1 retrieval decision returns — made per-query, by the model itself."),
 ("The ReAct loop", "Reason about what's missing, act (search), observe results, repeat. A dozen lines of control flow around your existing pipeline — but it changes what the system can answer."),
 ("Self-correction", "Draft an answer, critique it against the retrieved evidence, re-retrieve for unsupported claims. Slower and costlier, measurably more faithful. Your eval harness decides if it's worth it."),
 ("Context engineering for agents", "Loops accumulate context fast. What stays in the window, what gets summarized, what gets dropped — memory management is the difference between an agent that scales and one that drowns.")],
lab=[
 "Convert your Week 6 pipeline into a ReAct agent with retrieval as a tool",
 "Add a context-sufficiency check: the agent judges whether it can answer yet",
 "Implement one self-correction cycle",
 "Run the full eval: agent vs. static pipeline — quality, latency, and cost"],
checkpoint="An agentic version of your system plus an honest comparison table against the Week 6 pipeline. Sometimes the pipeline wins — knowing when is the skill.",
reading=[("Yao et al. — ReAct: Synergizing Reasoning and Acting in Language Models","The paper behind the loop you're building.","https://arxiv.org/abs/2210.03629"),
         ("What is Agentic RAG? — Weaviate","Architecture patterns for retrieval-aware agents.","https://weaviate.io/blog/what-is-agentic-rag")],
videos=[("Agentic RAG Explained","Concepts and architecture in a compact overview.","https://www.youtube.com/watch?v=MYPDsV_825U"),
        ("ReAct Agent Explained Simply","The reason-act-observe loop, step by step.","https://www.youtube.com/watch?v=bOhK-FRR-Ac")],
reflect=[
 "On which query types did the agent beat the pipeline? Where did it just burn tokens?",
 "How did you decide what to evict from the agent's context — and what broke when you got it wrong?",
 "What would it take to trust this agent unsupervised in front of your users?"]),

dict(num=8, material=True, title="Production: Secure, Observable, Deployable",
tag="The final mile: your system meets adversaries, latency budgets, and real users. Capstone week.",
objectives=[
 "Defend against prompt injection arriving through retrieved documents",
 "Instrument the pipeline with tracing and retrieval logging",
 "Deploy behind an API with caching and streaming",
 "Present and defend your capstone to technical and non-technical audiences"],
concepts=[
 ("The RAG attack surface", "Your index ingests documents; documents can contain instructions. Indirect prompt injection — attacks hiding in the corpus itself — is ranked the #1 LLM vulnerability by OWASP. Defense is layered: input sanitation, privilege separation, output validation."),
 ("Access control on the index", "If users have different permissions, retrieval must respect them — filtering at query time, not after generation. A RAG system that leaks one confidential chunk has failed entirely."),
 ("Observability", "Log every retrieval: query, candidates, scores, what made the context window. When answers degrade in production, these traces are the only way to run your Week 5 diagnosis on live traffic. Add drift detection: corpora change, embeddings go stale."),
 ("Performance engineering", "Semantic caching, streaming tokens, async retrieval, and index update pipelines. Latency budgets are design constraints, not afterthoughts.")],
lab=[
 "Red-team your own system: plant an injection in your corpus, watch it fire, then defend",
 "Add structured tracing and retrieval logs",
 "Wrap the system in FastAPI with streaming; add a minimal chat UI",
 "Containerize and load-test; document your latency and cost profile"],
checkpoint="Capstone presentation: your deployed system, live, plus a defense of every design choice backed by your own evaluation numbers — delivered once for engineers, once for stakeholders.",
reading=[("OWASP — LLM Prompt Injection Prevention Cheat Sheet","The practitioner's defense checklist.","https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html"),
         ("OWASP Top 10 for LLM Applications","The full vulnerability landscape for LLM systems.","https://owasp.org/www-project-top-10-for-large-language-model-applications/")],
videos=[("How AI Prompt Injection Works — Hands-on with LLMs","See the attack class you're defending against, live.","https://www.youtube.com/watch?v=fCpAr2OylDw")],
reflect=[
 "Did your injection defense survive a second, sneakier attempt?",
 "Which trace fields actually helped you debug — and which were noise?",
 "Explain your system to a non-technical stakeholder in three sentences. Did they get it?"],
exercises=[
 "<b>The retrieval case (Week 1).</b> In three sentences a stakeholder would understand, justify why your capstone needs retrieval at all — and name one query type it should answer <em>without</em> retrieving.",
 "<b>BM25 by hand (Week 2).</b> Given a 3-document toy corpus, hand-compute the BM25 score of one query against each document (k1=1.5, b=0.75). Verify with <code>rank_bm25</code>.",
 "<b>Metrics by hand (Week 2).</b> From a printed result table of 5 queries, compute Recall@5 and MRR on paper before checking with code.",
 "<b>The prediction game (Week 3).</b> Write 5 fresh queries for your corpus and predict, before running anything, whether BM25 or embeddings wins each. Score your predictions.",
 "<b>RRF on paper (Week 4).</b> Given two ranked lists of 5 documents, compute the fused RRF ranking by hand (k=60). Explain in one sentence why no score normalization was needed.",
 "<b>Failure triage (Week 5).</b> For a wrong answer transcript, write the exact decision procedure you'd follow to classify it as retrieval, generation, or chunking failure — then apply it.",
 "<b>Citation scaffold (Week 6).</b> Draft the prompt block that enforces your citation format, and demonstrate on 3 questions that citations point at genuinely supporting text.",
 "<b>Trace the hops (Week 7).</b> Author one new multihop question and hand-trace the retrieval hops your agent takes, comparing against what it should have done.",
 "<b>One novel attack (Week 8).</b> Write one injection payload not used in your challenge, predict which defense layer stops it, then test the prediction.",
 "<b>The budget memo (Week 8).</b> Write your capstone's latency and cost budget per query, identify the single biggest lever for each, and state what you'd sacrifice first under load."]),
]

# ---------------- CHALLENGES ----------------
challenges = [
dict(num=1, title="Catch Your Model Lying",
brief="Before trusting retrieval to fix hallucination, you need to see hallucination — systematically, in your own model, with your own eyes.",
tasks=[
 "Write <code>hallucination_probe.py</code>: ask your local model 20 questions — 5 each across four categories: stable general knowledge, niche long-tail facts, post-training-cutoff events, and your capstone domain",
 "Score every answer yourself: ✅ correct, ❌ wrong, 🤷 refused/hedged",
 "Write a 5-sentence conclusion: in which categories does retrieval earn its keep?"],
deliverable="A results table (markdown or CSV) + conclusion, committed with message <code>Week 1 challenge: hallucination probe</code>.",
stretch="Re-run all 20 questions at temperature 0 and 1.0. Does any category change verdict? What does that imply about 'just lower the temperature' as a hallucination fix?"),
dict(num=2, title="Break BM25",
brief="The fastest way to understand a system is to find its edges. Your mission: make your own search engine fail, on purpose, five different ways.",
tasks=[
 "Find 5 queries where your BM25 baseline retrieves the wrong documents from your corpus",
 "Diagnose each failure: synonymy, paraphrase, misspelling, question-vs-statement phrasing, or something else",
 "Predict, in writing, which failures Week 3's embeddings will fix"],
deliverable="<code>bm25_failures.md</code> with the 5 queries, diagnoses, and predictions, committed.",
stretch="Try to <em>fix</em> one failure without embeddings — synonym expansion, stemming, or query rewriting. How far can classical tricks go?"),
dict(num=3, title="The Chunking Bake-Off",
brief="Everyone copies chunk_size=1000, overlap=200 from a tutorial. You're going to find out what those numbers should be for YOUR corpus.",
tasks=[
 "Run at least 4 chunking configurations across size, overlap, and structure-awareness",
 "Score each configuration on your full query set: Recall@5 and MRR",
 "Inspect 3 losing retrievals per configuration: WHY did that chunking lose?"],
deliverable="A bake-off table with metrics per configuration and a written recommendation for your capstone, committed.",
stretch="Design one corpus-specific chunking rule (split on headings, keep tables whole, attach section titles to every chunk). Does it beat all generic configurations?"),
dict(num=4, title="Beat the Baseline",
brief="This week has a hard, numeric win condition: your hybrid pipeline must beat BOTH pure BM25 and pure vector search on your own metrics. No participation trophies.",
tasks=[
 "Assemble hybrid retrieval with RRF; measure it",
 "Add cross-encoder reranking; measure the lift separately",
 "If hybrid does NOT beat both parents, diagnose why and fix it — that's the real exercise"],
deliverable="A staged results table (BM25 / vector / hybrid / hybrid+rerank) with your analysis, committed.",
stretch="Sweep the RRF k parameter and the rerank depth (top-10/20/50). Chart quality vs. latency and pick your production operating point."),
dict(num=5, title="The Failure Audit",
brief="Play quality engineer for your own system: every bad answer gets a root cause, and every root cause gets a ticket.",
tasks=[
 "Run your full golden dataset through the Week 4 pipeline",
 "Label every failure: retrieval, generation, or chunking",
 "Write the top 3 'tickets': the highest-impact fixes, with evidence"],
deliverable="<code>failure_audit.md</code>: counts per category, example transcripts, and your 3 tickets, committed.",
stretch="Have an LLM judge label the same failures independently. Compute agreement with your human labels. Where does the judge get it wrong — and would you still trust it to gate deploys?"),
dict(num=6, title="The Multihop Gauntlet",
brief="Write the questions your system CAN'T answer yet — then make it answer them.",
tasks=[
 "Author 8 genuine multihop questions from your corpus (answers require 2+ documents)",
 "Show your Week 4 single-shot pipeline failing on most of them",
 "Run them through your decomposition + iterative retrieval pipeline; measure the difference"],
deliverable="The gauntlet questions, before/after results, and citations for every answer, committed.",
stretch="Add a router that detects multihop questions automatically and only invokes decomposition when needed. Measure the latency saved on simple queries."),
dict(num=7, title="Agent vs. Pipeline",
brief="A rigorous head-to-head: your agent against your static pipeline, three metrics, no favorites. The interesting result is wherever the agent LOSES.",
tasks=[
 "Run your full eval suite against both systems: quality, latency, token cost",
 "Break results down by query type: simple factual, multihop, out-of-corpus",
 "Write a deployment recommendation: which system serves which traffic?"],
deliverable="A comparison report with per-query-type tables and your routing recommendation, committed.",
stretch="Implement the router you just recommended: simple queries hit the pipeline, hard ones wake the agent. Measure the blended cost and quality."),
dict(num=8, title="Red Team Your Own System",
brief="Capstone hardening: you built it, now break in. Every defense you add must be proven against an attack you authored.",
tasks=[
 "Plant 3 distinct prompt-injection payloads in your corpus (instruction hijack, data exfiltration lure, citation spoof)",
 "Demonstrate each attack firing against your undefended system — record the transcripts",
 "Implement layered defenses; re-run all 3 attacks and show them failing",
 "Confirm your eval metrics did NOT degrade under the new defenses"],
deliverable="<code>redteam_report.md</code>: attacks, transcripts before/after, defense design, and final eval numbers. This ships with your capstone presentation.",
stretch="Swap attack corpora with a colleague (or have an LLM author novel attacks you haven't seen). Does your defense generalize, or did you only patch your own ideas?"),
]

# ---------------- PAGE BUILDERS ----------------
def week_page(w):
    n = w["num"]
    prev_link = f'<a href="week{n-1}.html">← Week {n-1}</a>' if n > 1 else '<a href="syllabus.html">← Syllabus</a>'
    next_link = f'<a href="week{n+1}.html">Week {n+1} →</a>' if n < 8 else '<a href="index.html">Course home →</a>'
    concepts_html = ''.join(f'<h3>{i+1}. {h}</h3><p>{p}</p>' for i, (h, p) in enumerate(w["concepts"]))
    reading_html = resources(w["reading"])
    video_html = resources(w["videos"])
    body = f"""
<div class="crumb"><a href="index.html">Home</a> / <a href="syllabus.html">Syllabus</a> / Week {n}</div>
<article>
<div class="kicker">Week {n} of 8</div>
<h1>{w["title"]}</h1>
<p class="lede">{w["tag"]}</p>
<div class="box"><div class="label">Learning objectives</div>{ul(w["objectives"])}</div>
{f'<div class="box ok"><div class="label">Study material</div><p><b><a href="week{n}-material.html">Open the full Week {n} study material →</a></b> Complete lesson: concepts in depth, the full lab with all code, and troubleshooting.</p></div>' if w.get("material") else ''}
<h2>Concepts</h2>
{concepts_html}
<h2>Lab — live session</h2>
{ol(w["lab"])}
<div class="box ok"><div class="label">Checkpoint</div><p>{w["checkpoint"]}</p></div>
<h2>Reading</h2>
{reading_html}
<h2>Watch</h2>
{video_html}
<h2>Reflection — bring answers to the next session</h2>
{ol(w["reflect"])}
{('<h2>Final exercise set — capstone review</h2><p>Ten exercises spanning the whole program. Complete them before your capstone defense; several make excellent warm-up material for the presentation itself.</p>' + ol(w["exercises"])) if w.get("exercises") else ''}
<div class="box warn"><div class="label">Weekend challenge</div>
<p><b><a href="challenge{n}.html">Challenge {n}: {challenges[n-1]["title"]}</a></b> — {challenges[n-1]["brief"]}</p></div>
<div class="pagenav">{prev_link}{next_link}</div>
</article>"""
    return page(f"Week {n}", body)

def challenge_page(c):
    n = c["num"]
    body = f"""
<div class="crumb"><a href="index.html">Home</a> / <a href="week{n}.html">Week {n}</a> / Challenge {n}</div>
<article>
<div class="kicker">Weekend Challenge · Week {n}</div>
<h1>{c["title"]}</h1>
<p class="lede">{c["brief"]}</p>
<h2>Your mission</h2>
{ol(c["tasks"])}
<div class="box ok"><div class="label">Deliverable</div><p>{c["deliverable"]}</p></div>
<div class="box"><div class="label">Stretch goal</div><p>{c["stretch"]}</p></div>
<div class="pagenav"><a href="week{n}.html">← Back to Week {n}</a>{f'<a href="week{n+1}.html">Week {n+1} →</a>' if n < 8 else '<a href="index.html">Course home →</a>'}</div>
</article>"""
    return page(f"Challenge {n}", body)

def index_page():
    cards = ''
    for w in weeks:
        n = w["num"]
        cards += f"""<div class="card"><div class="wk">Week {n}</div>
<h3><a href="week{n}.html">{w["title"]}</a></h3>
<p>{w["tag"]}</p>
<div class="links"><a href="week{n}.html">Lesson</a><a href="challenge{n}.html">Challenge</a></div></div>"""
    body = f"""
<div class="hero">
<h1>RAG &amp; Context Engineering</h1>
<p class="tag">{SUBTITLE}. An eight-week, build-first program: you leave with a deployed retrieval-augmented AI system, the evaluation data to defend every design choice, and the judgment to know when each technique earns its place.</p>
<div class="pills">
<div class="pill"><b>8 weeks</b> · 1 live session/week</div>
<div class="pill"><b>~6–8 hrs</b>/week</div>
<div class="pill"><b>Instructor:</b> {INSTRUCTOR}</div>
<div class="pill"><b>100% hands-on</b> · local-first tooling</div>
</div>
<a class="cta" href="syllabus.html">View the full syllabus</a>
</div>
<h2 class="sec">How this program works</h2>
<p>Every week follows the same professional rhythm: a live session where concepts are taught and the lab is built together, a <b>checkpoint</b> that becomes a permanent part of your capstone system, a <b>weekend challenge</b> that stress-tests what you built, plus curated reading and video. Nothing is throwaway — by Week 8 your weekly checkpoints assemble into one complete, deployed, evaluated RAG system running on a document collection you chose in Week 1.</p>
<p>From day one you work like a working engineer: local LLMs via Ollama, a real git repository, reproducible environments, and the rule that every claim gets tested with code — no copying framework defaults on faith.</p>
<h2 class="sec">The eight weeks</h2>
<div class="grid">{cards}</div>
<h2 class="sec">The capstone</h2>
<p>Your final session is a defense, not a demo. You present your deployed system live, walk through the design decisions behind it — chunking, hybrid fusion, reranking depth, agent-vs-pipeline routing, injection defenses — and back every choice with your own evaluation numbers. You deliver it twice: once for a technical audience, once for stakeholders. That second version is often the harder one, and the more valuable skill.</p>"""
    return page("Home", body)

def syllabus_page():
    rows = ''
    for w in weeks:
        n = w["num"]
        rows += f'<tr><td><b>{n}</b></td><td><a href="week{n}.html">{w["title"]}</a></td><td><a href="challenge{n}.html">{challenges[n-1]["title"]}</a></td></tr>'
    body = f"""
<div class="crumb"><a href="index.html">Home</a> / Syllabus</div>
<article>
<div class="kicker">Program Document</div>
<h1>Syllabus</h1>
<p class="lede">{COURSE}: {SUBTITLE} — an eight-week applied program in retrieval-augmented generation and context engineering.</p>

<h2>Program description</h2>
<p>Large language models are powerful but bounded: they know only what they were trained on, and they fail silently when asked to go beyond it. Retrieval-augmented generation (RAG) — connecting models to external knowledge at inference time — is how production AI systems ground their answers in private, fresh, and verifiable data. This program teaches RAG as an engineering discipline: not a framework tutorial, but the design decisions, measurement practices, and production concerns that separate demos from systems.</p>
<p>The program is build-first. Each participant selects a document corpus in Week 1 and constructs a complete system over it across eight weeks: classical and semantic retrieval, hybrid fusion and reranking, systematic evaluation, multihop and agentic workflows, and finally secure deployment. All tooling is local-first and open source.</p>

<h2>Learning outcomes</h2>
<p>On completion, participants will be able to:</p>
{ul([
"Decide when and why external retrieval is necessary in LLM systems, and defend that decision",
"Design classical, semantic, and hybrid retrieval pipelines, and justify each stage with measurement",
"Diagnose accuracy and performance failures using structured evaluation and a root-cause taxonomy",
"Build end-to-end RAG systems, including query decomposition and multihop retrieval",
"Implement retrieval-aware agentic workflows and judge when they beat static pipelines",
"Deploy secure, observable, production-grade RAG systems with layered injection defenses",
"Communicate system behavior and design trade-offs to technical and non-technical stakeholders"])}

<h2>Schedule</h2>
<table>
<tr><th>Week</th><th>Lesson</th><th>Weekend challenge</th></tr>
{rows}
</table>

<h2>Methodology</h2>
<p>This program follows a <b>guided-cohort model</b>: one live 90-minute session per week in which the cohort studies the concepts and builds the labs <em>together</em>, with the instructor facilitating pace, discussion, and debugging. The materials are designed to carry the technical content; the sessions exist so that nobody struggles alone and every question gets worked through out loud. Between sessions, participants complete a weekend challenge (approximately 3–4 hours) that stress-tests the week's build and produces a committed deliverable. Expect a total commitment of 6–8 hours per week. Every artifact is version-controlled from day one; the accumulated repository is itself a program outcome — a portfolio piece demonstrating professional practice.</p>

<h2>Assessment</h2>
<p>Assessment is continuous and evidence-based: eight weekly checkpoints (committed, working code with measured results), eight challenge deliverables, and a capstone defense. The capstone is presented twice — a technical deep-dive and a stakeholder briefing — and is evaluated on whether design choices are supported by the participant's own evaluation data, not on feature count.</p>

<h2>Tools and materials</h2>
<p>Python 3.11+, uv, git, Ollama (llama3.1:8b and nomic-embed-text), rank-bm25, Chroma, sentence-transformers, RAGAS, FastAPI, and Docker. All tools are free and run locally; a laptop with 8&nbsp;GB+ RAM is sufficient. Readings draw on primary sources — the original RAG, ReAct, and Lost-in-the-Middle papers, the Stanford IR textbook, and OWASP security guidance — linked from each week's page.</p>

<h2>Prerequisites</h2>
<p>Working Python proficiency (functions, classes, virtual environments, pip/uv) and basic command-line comfort. No prior experience with LLM APIs, vector databases, or information retrieval is assumed — Weeks 1–3 build these foundations explicitly.</p>

<h2>Instructor</h2>
<p>{INSTRUCTOR} — program design and session facilitation, {BRAND}. Sessions are run in the guided-cohort format: the instructor leads the study, works the labs alongside the cohort, and keeps every participant moving — the accompaniment model {BRAND} programs are built on.</p>
<div class="pagenav"><a href="index.html">← Course home</a><a href="week1.html">Begin Week 1 →</a></div>
</article>"""
    return page("Syllabus", body)

# ---------------- WRITE ----------------
os.makedirs(OUT, exist_ok=True)
files = {"index.html": index_page(), "syllabus.html": syllabus_page()}
for w in weeks: files[f"week{w['num']}.html"] = week_page(w)
for c in challenges: files[f"challenge{c['num']}.html"] = challenge_page(c)
for name, html in files.items():
    with open(os.path.join(OUT, name), "w") as f: f.write(html)
print(f"Wrote {len(files)} pages to {OUT}")
for n in sorted(files): print(" ", n)
