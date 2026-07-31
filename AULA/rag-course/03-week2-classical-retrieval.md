# Week 2 — Classical Retrieval: The Foundation Everyone Skips

Most RAG tutorials jump straight to embeddings. Professionals learn keyword search first — because in production, BM25 is still the baseline to beat, and often it *isn't* beaten.

## Concepts

### 1. The inverted index
Instead of scanning every document per query (slow), we build a map from **term → list of documents containing it**. This is how every search engine since the 1970s works, including Elasticsearch today.

### 2. Scoring: from counting to TF-IDF
- **Term frequency (TF):** a doc mentioning "retrieval" 10× is probably more about retrieval than one mentioning it once.
- **Inverse document frequency (IDF):** "the" appears everywhere → worthless. "multihop" appears in 2 docs → gold. Rare terms carry signal.
- TF-IDF = multiply the two.

### 3. BM25: TF-IDF grown up
Two fixes that made it the 25-year industry standard:
- **Saturation:** the 50th occurrence of a term shouldn't count like the 2nd (parameter k1).
- **Length normalization:** long docs match everything by accident; penalize them fairly (parameter b).

### 4. Measuring retrieval quality
- **Recall@k:** of the relevant docs, how many appear in the top k?
- **Precision@k:** of the top k, how many are relevant?
- **MRR:** how high does the *first* relevant doc rank?
You cannot improve what you don't measure — this becomes the spine of Week 5.

## Lab (we do this together in session)

1. **From scratch:** build an inverted index + TF-IDF scorer in pure Python (~60 lines) over your capstone corpus.
2. **Then the library:** swap in `rank_bm25`, compare rankings.
3. **Evaluate:** write 10 test queries with known-relevant docs; compute Recall@5 and MRR. These numbers are your **baseline** — every later week must beat them or justify itself.

**Checkpoint:** `bm25_baseline.py` + `eval_queries.json` + a metrics table, committed.

## Weekend Challenge

**"Break BM25."** Find 5 queries where BM25 fails on your corpus and diagnose *why* for each. Expected failure modes to hunt for: synonyms ("car" vs "automobile"), paraphrase, misspellings, questions phrased differently than the docs. This failure list is exactly what Week 3's embeddings should fix — we'll test that claim directly.

## Reading

- Manning, Raghavan & Schütze, *Introduction to Information Retrieval* — Ch. 1 (boolean retrieval) and Ch. 6 (scoring & TF-IDF). Free: https://nlp.stanford.edu/IR-book/
- Optional deep-dive: Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond* (skim only).

## Video

- *A no-nonsense intro to BM25*: https://www.youtube.com/watch?v=TW9vHU1GpU4
- *BM25 retrieval model* (university IR lecture): https://www.youtube.com/watch?v=p8st3g_Y39I

## Reflection questions

1. Why does IDF alone explain most of why search "just works"?
2. When would you tune k1 and b rather than accept defaults?
3. Which of your 5 failure queries do you predict embeddings will fix — and which won't they?
