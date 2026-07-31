#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
axle_rag.flow — what moves between places
=========================================
G6 LLC · Principia Orthogona · AXLE-RAG · MIT License

An index is static and nobody reads a corpus — not a person, not a retriever.
What has to travel is the INVALIDATION SIGNAL.

This is `make` for a body of knowledge. Claims depend on constants, on DOIs, on
Lean files, on other claims. Change one root and the dependent closure is stale
by construction. The flow is: edit → propagate → work order → repair → re-audit.

Concretely, on 2026-07-30 a single edit (r* : 0.773 → 0.77594059) should have
propagated to: the GTCT paper text, four figures, the figure captions, the Lean
constant, FINDINGS.md, three site copies of ch10, the book4 hub blurb, and ch03.
Nine of those were found by hand, one at a time, across sessions. The dependency
closure computes all of them in milliseconds.

Node types
    const:<name>     a tracked numeric constant
    doi:<id>         a deposit identifier
    lean:<file>      a machine-checked artifact
    file:<name>      a source document
    claim:<id>       an individual claim chunk

Edges  claim → the constants/DOIs/lean files it asserts or cites
       file  → its claims

Run:
    python3 flow.py chunks.jsonl --change "const:r*"
    python3 flow.py chunks.jsonl --change "lean:ForcedUrgency.lean" --order
    python3 flow.py chunks.jsonl --graph graph.json
"""
from __future__ import annotations
import argparse, json, re, sys
from collections import defaultdict, deque
from pathlib import Path

TRUST_NAME = {0: "OPEN", 1: "PREMISE", 2: "MODEL", 3: "DATA", 4: "VERIFIED"}
LEAN_MENTION = re.compile(r"([A-Za-z_][\w]*\.lean)")


def build_graph(chunks: list[dict]):
    """deps[node] = set(nodes that depend on it)"""
    deps: dict[str, set[str]] = defaultdict(set)
    meta: dict[str, dict] = {}

    for c in chunks:
        cid = f"claim:{c['id']}"
        fid = f"file:{c['source']}"
        meta[cid] = {"source": c["source"], "trust": c["trust"], "wp": c.get("wp"),
                     "heading": c.get("heading", ""), "text": c["text"][:180],
                     "verified": c.get("verified", False)}
        meta.setdefault(fid, {"source": c["source"], "kind": "file"})

        deps[cid].add(fid)                                  # claim change → file changes

        for k in (c.get("constants") or {}):
            n = f"const:{k}"
            meta.setdefault(n, {"kind": "const", "name": k})
            deps[n].add(cid)                                # const change → claim stale

        if c.get("doi"):
            n = f"doi:{c['doi']}"
            meta.setdefault(n, {"kind": "doi", "id": c["doi"]})
            deps[n].add(cid)

        if c["kind"] == "lean":
            n = f"lean:{c['source']}"
            meta.setdefault(n, {"kind": "lean", "file": c["source"],
                                "verified": c.get("verified", False)})
            deps[n].add(cid)
        else:
            for f in set(LEAN_MENTION.findall(c["text"])):
                n = f"lean:{f}"
                meta.setdefault(n, {"kind": "lean", "file": f})
                deps[n].add(cid)                            # lean change → prose stale

    return deps, meta


def closure(deps, roots: list[str]) -> list[str]:
    seen, q = set(), deque(roots)
    while q:
        n = q.popleft()
        for m in deps.get(n, ()):
            if m not in seen:
                seen.add(m)
                q.append(m)
    return sorted(seen)


def work_order(deps, meta, roots: list[str]) -> str:
    hit = closure(deps, roots)
    files = sorted({meta[n]["source"] for n in hit
                    if n.startswith("claim:") and n in meta})
    claims = [n for n in hit if n.startswith("claim:")]

    L = [f"# WORK ORDER — propagation of {', '.join(roots)}", "",
         f"{len(claims)} claims in {len(files)} files are stale by construction.",
         "", "## Files to touch (in this order)", ""]
    # verified artifacts first: the kernel is the root of trust
    lean = [f for f in files if f.endswith(".lean")]
    docs = [f for f in files if not f.endswith(".lean")]
    for i, f in enumerate(lean + docs, 1):
        n = sum(1 for c in claims if meta[c]["source"] == f)
        L.append(f"{i}. `{f}` — {n} affected claim(s)")

    L += ["", "## Affected claims", ""]
    for c in claims[:40]:
        m = meta[c]
        flag = " ✓kernel" if m.get("verified") else ""
        L.append(f"- **{m['source']}**{flag} · {TRUST_NAME[m['trust']]}"
                 + (f" · {m['wp']}" if m.get("wp") else ""))
        L.append(f"  > {m['text'].strip()[:150]}…")
    if len(claims) > 40:
        L.append(f"- …and {len(claims)-40} more")

    L += ["", "## Completion criteria",
          "- [ ] every file above edited or explicitly ruled out",
          "- [ ] `python3 audit.py chunks.jsonl --severity HIGH` returns clean",
          "- [ ] handoff brief regenerated (`audit.py --handoff`)",
          "- [ ] correction notices added where a published value changed", ""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Propagate a change through the corpus.")
    ap.add_argument("chunks", type=Path)
    ap.add_argument("--change", action="append", default=[],
                    help="root node, e.g. const:r* · doi:10.5281/... · lean:X.lean · file:y.html")
    ap.add_argument("--order", action="store_true", help="emit a markdown work order")
    ap.add_argument("--graph", type=Path, help="dump the dependency graph as JSON")
    ap.add_argument("--roots", action="store_true", help="list available root nodes")
    a = ap.parse_args()

    chunks = [json.loads(l) for l in a.chunks.read_text(encoding="utf-8").splitlines() if l.strip()]
    deps, meta = build_graph(chunks)

    if a.graph:
        a.graph.write_text(json.dumps(
            {"edges": {k: sorted(v) for k, v in deps.items()},
             "nodes": {k: v for k, v in meta.items() if not k.startswith("claim:")}},
            indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"graph → {a.graph} ({len(deps)} nodes with dependents)")
        return 0

    if a.roots or not a.change:
        print("Available roots (change any of these and the closure follows):\n")
        for kind in ("const", "doi", "lean"):
            ns = sorted(n for n in deps if n.startswith(kind + ":"))
            if ns:
                print(f"  {kind}:")
                for n in ns:
                    print(f"    {n:<52} → {len(closure(deps,[n]))} dependent nodes")
        return 0

    if a.order:
        print(work_order(deps, meta, a.change))
        return 0

    hit = closure(deps, a.change)
    files = sorted({meta[n]["source"] for n in hit if n.startswith("claim:")})
    print(f"changing {', '.join(a.change)} invalidates "
          f"{sum(1 for n in hit if n.startswith('claim:'))} claims "
          f"across {len(files)} files:\n")
    for f in files:
        print("  " + f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
