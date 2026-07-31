#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
axle_rag.retrieve — claim-gated retrieval
=========================================
G6 LLC · Principia Orthogona · AXLE-RAG · MIT License

BM25 over the ingested chunks, with three things standard RAG does not do:

1. TRUST-AWARE RANKING.  score = bm25 × trust_weight.  A kernel-verified claim
   outranks a prose claim of equal lexical fit. Configurable, and the raw bm25
   is always reported so the reweighting is auditable.

2. GATING.  --min-trust drops claims below a floor. Default keeps everything
   but MARKS it: an [OPEN] claim can be retrieved, never silently.

3. CONTEXT ASSEMBLY WITH A REFUSAL CONTRACT.  build_context() emits a block the
   generator must obey: every retrieved claim arrives with its tag, DOI and
   source, plus explicit instructions never to present OPEN as established and
   never to state a constant not present in the context.

No network, no API keys, no embedding model required — BM25 is exact and
reproducible, which matters more than recall for a corpus that must be citable.
An optional dense reranker can be layered later without changing the contract.

Run:
    python3 retrieve.py chunks.jsonl "what is r*?"
    python3 retrieve.py chunks.jsonl "harvest coefficient" --min-trust 3 --context
"""
from __future__ import annotations
import argparse, json, math, re, sys
from collections import Counter
from pathlib import Path

TRUST_NAME = {0: "OPEN", 1: "PREMISE", 2: "MODEL", 3: "DATA", 4: "VERIFIED"}
# deliberately mild: retrieval must not become an argument from authority
TRUST_WEIGHT = {0: 0.55, 1: 0.80, 2: 1.00, 3: 1.15, 4: 1.30}

_TOKEN = re.compile(r"[A-Za-zÀ-ÿ0-9*★_.\-/]+")
_STOP = set("""a an the of in on for to and or is are was were be been by with as at from that this
these those it its which not no than then so such can may might will would shall should""".split())


def tok(s: str) -> list[str]:
    return [t for t in (w.lower() for w in _TOKEN.findall(s))
            if t not in _STOP and len(t) > 1]


class BM25:
    """Okapi BM25. Pure stdlib, deterministic."""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.N = len(docs)
        self.docs = docs
        self.len = [len(d) for d in docs]
        self.avg = (sum(self.len) / self.N) if self.N else 0.0
        self.tf: list[Counter] = [Counter(d) for d in docs]
        df: Counter = Counter()
        for d in docs:
            df.update(set(d))
        self.idf = {t: math.log(1 + (self.N - n + 0.5) / (n + 0.5)) for t, n in df.items()}

    def score(self, q: list[str], i: int) -> float:
        tf, dl, s = self.tf[i], self.len[i], 0.0
        for t in q:
            f = tf.get(t)
            if not f:
                continue
            s += self.idf.get(t, 0.0) * f * (self.k1 + 1) / (
                f + self.k1 * (1 - self.b + self.b * dl / (self.avg or 1)))
        return s


class Index:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        corpus = [tok(f"{c.get('heading','')} {c['text']} {c.get('wp') or ''} "
                      f"{c.get('source','')}") for c in chunks]
        self.bm25 = BM25(corpus)

    @classmethod
    def load(cls, path: Path) -> "Index":
        return cls([json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()])

    def search(self, query: str, k: int = 6, min_trust: int = 0,
               kinds: set[str] | None = None, trust_boost: bool = True) -> list[dict]:
        q = tok(query)
        hits = []
        for i, c in enumerate(self.chunks):
            if c["trust"] < min_trust:
                continue
            if kinds and c["kind"] not in kinds:
                continue
            raw = self.bm25.score(q, i)
            if raw <= 0:
                continue
            w = TRUST_WEIGHT[c["trust"]] if trust_boost else 1.0
            hits.append({**c, "bm25": round(raw, 3), "score": round(raw * w, 3)})
        hits.sort(key=lambda h: -h["score"])
        return hits[:k]


# --------------------------------------------------------------------------
REFUSAL_CONTRACT = """\
RETRIEVAL CONTRACT — binding on the answer you generate:
1. Cite by [source · tag · DOI] for every factual sentence you write.
2. A claim tagged OPEN is NOT established. If the answer depends on one, say so
   explicitly and do not assert it. Never launder OPEN into DATA.
3. Do not state a numeric constant that does not appear verbatim in the context
   below. If the user asks for one that is absent, say it is not in the corpus.
4. If two context blocks give different values for the same constant, report the
   conflict and its sources; do not silently pick one.
5. VERIFIED means machine-checked by the Lean kernel. Do not apply that word to
   anything else.
"""


def build_context(hits: list[dict], max_chars: int = 6000) -> str:
    out, n = [REFUSAL_CONTRACT, ""], 0
    for h in hits:
        head = (f"[{h['source']} · {TRUST_NAME[h['trust']]}"
                + (f" · {h['doi']}" if h.get("doi") else "")
                + (f" · {h['wp']}" if h.get("wp") else "")
                + (" · KERNEL-VERIFIED" if h.get("verified") else "") + "]")
        body = h["text"]
        if n + len(body) > max_chars:
            body = body[: max(0, max_chars - n)] + " …"
        out += [head, body, ""]
        n += len(body)
        if n >= max_chars:
            break
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Claim-gated retrieval over the corpus.")
    ap.add_argument("chunks", type=Path)
    ap.add_argument("query")
    ap.add_argument("-k", type=int, default=6)
    ap.add_argument("--min-trust", type=int, default=0,
                    help="0 OPEN · 1 PREMISE · 2 MODEL · 3 DATA · 4 VERIFIED")
    ap.add_argument("--kind", action="append", help="html|md|tex|lean (repeatable)")
    ap.add_argument("--no-boost", action="store_true")
    ap.add_argument("--context", action="store_true", help="emit LLM-ready context block")
    a = ap.parse_args()

    idx = Index.load(a.chunks)
    hits = idx.search(a.query, k=a.k, min_trust=a.min_trust,
                      kinds=set(a.kind) if a.kind else None,
                      trust_boost=not a.no_boost)
    if a.context:
        print(build_context(hits))
        return 0

    if not hits:
        print("no matching claims in corpus."); return 0
    for h in hits:
        flag = " ⚠ NOT ESTABLISHED" if h["trust"] == 0 else (" ✓ kernel" if h["verified"] else "")
        print(f"\n[{h['score']:>6}] {TRUST_NAME[h['trust']]:<8}{flag}")
        print(f"  {h['source']}" + (f" · {h['wp']}" if h.get("wp") else "")
              + (f" · {h['doi']}" if h.get("doi") else ""))
        if h.get("constants"):
            print(f"  constants: {h['constants']}")
        print("  " + (h["text"][:260] + ("…" if len(h["text"]) > 260 else "")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
