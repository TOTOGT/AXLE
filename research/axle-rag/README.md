# AXLE-RAG — a build system for a body of knowledge

**G6 LLC · Principia Orthogona · MIT License · v0.1 (2026-07-30)**

Not a search box. The corpus is static; what has to **flow** is the
invalidation signal. Change one constant and every downstream claim goes stale
by construction — like `make`, for a science.

## Why this corpus and not another

Almost no corpus is provenance-labeled. This one already is:

- every claim carries `[DATA]` / `[MODEL]` / `[OPEN]` / `[VALUE PREMISE]` / `[ASSUMPTION]`
- deposits carry DOIs; some claims are **kernel-verified** in Lean 4
- WP-24/28/29/30 established an audit standard *inside* the corpus

So the retrieval layer can do something ordinary RAG cannot: **return a claim
together with its epistemic status**, and refuse to launder an `[OPEN]` claim
into an established one.

## The two directions

```
corpus ──ingest──▶ tagged claims ──retrieve──▶ answers that cite status
   ▲                     │
   └──── repair ◀── work order ◀── flow ◀── audit ◀────┘
```

1. **Corpus → LLM.** Claim-gated retrieval; the generator is bound by a
   refusal contract it cannot satisfy without citing tag + DOI.
2. **LLM → corpus.** Automated versions of the hand audits: constant drift,
   DOI incoherence, dangling refs, tag laundering, verification drift, stale
   hedges. Then propagation: what else must change.

## Modules

| file | role |
|---|---|
| `ingest.py` | `.html/.md/.tex/.lean` → JSONL claims with tags, DOIs, constants, trust tier |
| `retrieve.py` | BM25 + trust weighting + gating; emits an LLM context block with a refusal contract |
| `audit.py` | C1–C7 defect sweep; `--handoff` writes the brief a fresh session must read first |
| `flow.py` | dependency graph; `--change const:r*` → the closure of everything now stale; `--order` → a work order |

Pure stdlib. No API key, no embedding model, no network. BM25 is exact and
reproducible, which for a citable corpus matters more than recall.

## Quick start

```bash
python3 ingest.py  ~/geometry           -o chunks.jsonl
python3 audit.py   chunks.jsonl --severity HIGH      # what is broken
python3 audit.py   chunks.jsonl --handoff > HANDOFF.md
python3 flow.py    chunks.jsonl --change "const:r*" --order > WORK_ORDER.md
python3 retrieve.py chunks.jsonl "inner basin boundary" --context   # feed to any LLM
```

## Validated against real defects

Run on a 240-claim slice of the corpus (2026-07-30), with two defects planted
to confirm detection. It found, unprompted:

- **C1** `r*` asserted at 0.773 / 0.7732 / 0.77594059 / 0.8 across four files —
  the exact drift that took a full session to chase by hand
- **C5** prose asserting `ForcedUrgency.lean` is sorry-free while the ingested
  file contains a `sorry`
- **C2** two DOIs attached to the same working paper

Correction notices are suppressed from C1 by design: a repaired file quotes the
value it retires, and counting that as a live assertion is the documented
false-positive class.

## The three-account problem

Parallel sessions undo each other because none of them knows what the last one
decided. `audit.py --handoff` is the fix: a generated brief — claim inventory,
contested constants, open claims that must never be stated as established, and
the inherited editing rules — regenerated from the corpus itself rather than
maintained by hand. Read it first, write it last.

## Limits (stated, not hidden)

- BM25 is lexical; synonym-heavy queries will miss. A dense reranker can be
  added without touching the refusal contract. `[OPEN]`
- Constant extraction is regex-based and covers seven tracked constants;
  broadening it is the obvious next increment. `[OPEN]`
- The trust tier is *inherited from the author's own tags*. It measures
  labeling discipline, not truth. A mislabeled claim retrieves as mislabeled.
  `[MODEL]`
- `verified` for non-Lean files is a prose-pattern match, and is therefore a
  claim about the text, not about the kernel. Only `kind == "lean"` chunks are
  checked structurally. `[MODEL]`
