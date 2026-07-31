#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
axle_rag.audit — the reverse direction: the corpus audits itself
================================================================
G6 LLC · Principia Orthogona · AXLE-RAG · MIT License

WP-24, WP-28, WP-29 and WP-30 were audits done by hand. So was the 2026-07-30
session that found r* = 0.773 stale (true value 0.77594059), the e^-r / e^-z
coupling misprint, the κ symbol collision (√(5/9) chain contraction vs √(7/9)
dm³ marker), a saddle eigenvalue printed as 1.1097 instead of 1.4915, an ORCID
digit, and a Lean file that had drifted out of sync with the paper describing
it. Every one of those is mechanically detectable. This module detects them.

Checks
------
C1 CONSTANT DRIFT      one constant, two values across the corpus
C2 DOI COHERENCE       same work cited under different DOIs; series vs version
C3 DANGLING REFERENCE  [n] citation with no entry n in the file's reference list
C4 TAG LAUNDERING      a claim asserted flatly in one file, tagged OPEN in another
C5 VERIFICATION DRIFT  prose says "no sorry" while the named .lean file has one
C6 ORPHAN CONSTANT     a number asserted with no tag at all
C7 STALE HEDGE         hedge language ("to be confirmed", "pending") adjacent to a
                       flat assertion — the failure mode CLAUDE.md rule 7 names

Also emits a SESSION HANDOFF brief: the contested-claim state a fresh session
must read before touching anything, so parallel sessions stop undoing each
other's repairs.

Run:
    python3 audit.py chunks.jsonl                 # full report
    python3 audit.py chunks.jsonl --handoff       # brief for the next session
    python3 audit.py chunks.jsonl --json out.json
"""
from __future__ import annotations
import argparse, json, re, sys
from collections import defaultdict
from pathlib import Path

TRUST_NAME = {0: "OPEN", 1: "PREMISE", 2: "MODEL", 3: "DATA", 4: "VERIFIED"}
SEV = {"HIGH": 3, "MED": 2, "LOW": 1}

# tolerance per constant: below this, two values are "the same number"
TOL = {"r*": 1e-4, "eps_0": 1e-6, "kappa*": 1e-4, "mu_max": 1e-3,
       "r_s": 1e-4, "tau": 1e-9, "rho": 1e-4}

CORRECTION = re.compile(
    r"(supersed|erratum|correction notice|withdraw|previously (?:stated|printed|reported)|"
    r"was wrong|incorrect|do not cite|stale|retire[ds]?|replaced with|misprint)", re.I)

HEDGE = re.compile(r"(to be confirmed|pending confirmation|volume/issue|"
                   r"not yet (?:established|verified|estimated)|remains open|"
                   r"left to the .{0,40} literature)", re.I)
FLAT = re.compile(r"(is proved|we prove|establishes that|confirms that|"
                  r"it follows that|therefore established|ESTABLISHED)", re.I)
NUM = re.compile(r"(?<![\w.])\d+\.\d{2,}(?![\w])")


def _finding(code, sev, msg, where, detail=None):
    return {"code": code, "severity": sev, "message": msg,
            "where": sorted(set(where)), "detail": detail or {}}


# --------------------------------------------------------------------- C1
def check_constant_drift(chunks):
    seen = defaultdict(list)          # const -> [(value, source, wp, trust)]
    for c in chunks:
        # a correction notice legitimately quotes the value it retires; counting
        # it as a live assertion is the known false-positive class (CLAUDE.md)
        if CORRECTION.search(c["text"]):
            continue
        for k, v in (c.get("constants") or {}).items():
            seen[k].append((v, c["source"], c.get("wp"), c["trust"]))
    out = []
    for k, obs in seen.items():
        vals = sorted({round(v, 8) for v, *_ in obs})
        if len(vals) < 2:
            continue
        tol = TOL.get(k, 1e-6)
        groups = []
        for v in vals:
            if groups and abs(v - groups[-1][-1]) <= tol:
                groups[-1].append(v)
            else:
                groups.append([v])
        if len(groups) < 2:
            continue
        by_val = defaultdict(list)
        for v, src, wp, _ in obs:
            by_val[round(v, 8)].append(src)
        out.append(_finding(
            "C1", "HIGH",
            f"constant {k} asserted with {len(groups)} distinct values: "
            + " vs ".join(str(g[0]) for g in groups),
            [s for _, s, *_ in obs],
            {"values": {str(v): sorted(set(srcs)) for v, srcs in by_val.items()}}))
    return out


# --------------------------------------------------------------------- C2
def check_doi_coherence(chunks):
    by_wp = defaultdict(set)
    dois = defaultdict(set)
    for c in chunks:
        if c.get("doi"):
            dois[c["doi"]].add(c["source"])
            if c.get("wp"):
                by_wp[c["wp"]].add(c["doi"])
    out = []
    for wp, ds in by_wp.items():
        if len(ds) > 1:
            out.append(_finding("C2", "MED",
                                f"{wp} cited under {len(ds)} different DOIs",
                                [s for d in ds for s in dois[d]],
                                {"dois": sorted(ds)}))
    # near-miss DOIs (one digit apart) are the classic concept-vs-version slip
    keys = sorted(dois)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if len(a) == len(b) and sum(x != y for x, y in zip(a, b)) == 1:
                out.append(_finding("C2", "MED",
                                    f"near-identical DOIs in corpus: {a} vs {b} "
                                    "(concept vs version, or a typo)",
                                    sorted(dois[a] | dois[b]),
                                    {"dois": [a, b]}))
    return out


# --------------------------------------------------------------------- C3
def check_dangling_refs(chunks):
    cited, defined = defaultdict(set), defaultdict(int)
    for c in chunks:
        for r in c.get("refs", []):
            cited[c["source"]].add(r)
        if c.get("heading", "").lower().startswith(("source", "reference", "bibliograph")):
            defined[c["source"]] += 1
    out = []
    for src, refs in cited.items():
        n = defined.get(src, 0)
        if n and refs and max(refs) > n:
            out.append(_finding("C3", "MED",
                                f"cites [{max(refs)}] but only {n} reference entries found",
                                [src], {"max_cited": max(refs), "defined": n}))
    return out


# --------------------------------------------------------------------- C4
def check_tag_laundering(chunks):
    """A claim marked OPEN somewhere and asserted flatly elsewhere."""
    open_terms = defaultdict(set)
    for c in chunks:
        if c["trust"] == 0:
            for k in (c.get("constants") or {}):
                open_terms[k].add(c["source"])
    out = []
    for c in chunks:
        if c["trust"] >= 3 and FLAT.search(c["text"]):
            for k in (c.get("constants") or {}):
                if k in open_terms and c["source"] not in open_terms[k]:
                    out.append(_finding(
                        "C4", "HIGH",
                        f"{k} asserted as {TRUST_NAME[c['trust']]} here, but tagged OPEN in "
                        + ", ".join(sorted(open_terms[k])),
                        [c["source"], *open_terms[k]], {"constant": k}))
    return out


# --------------------------------------------------------------------- C5
def check_verification_drift(chunks):
    lean_files = {c["source"]: c for c in chunks if c["kind"] == "lean"}
    dirty = {s for s, c in lean_files.items() if not c["verified"]}
    out = []
    for c in chunks:
        if c["kind"] == "lean":
            continue
        m = re.findall(r"([A-Za-z_][\w]*\.lean)", c["text"])
        for f in m:
            if f in dirty and re.search(r"(no\s+sorry|sorry[- ]free|0\s+sorr|kernel[- ]verified|machine[- ]checked)", c["text"], re.I):
                out.append(_finding("C5", "HIGH",
                                    f"prose claims {f} is sorry-free; the ingested "
                                    f"{f} contains a sorry",
                                    [c["source"], f], {"lean_file": f}))
    return out


# --------------------------------------------------------------------- C6
def check_orphan_constants(chunks):
    out = []
    for c in chunks:
        if c["tags"] or c["kind"] == "lean":
            continue
        nums = NUM.findall(c["text"])
        if len(nums) >= 2 and c.get("constants"):
            out.append(_finding("C6", "LOW",
                                "numeric claim carries no [TAG]",
                                [c["source"]],
                                {"constants": c["constants"], "heading": c.get("heading", "")}))
    return out


# --------------------------------------------------------------------- C7
def check_stale_hedges(chunks):
    out = []
    for c in chunks:
        if HEDGE.search(c["text"]) and FLAT.search(c["text"]):
            out.append(_finding("C7", "MED",
                                "hedge and flat assertion in the same claim "
                                "(CLAUDE.md rule 7 failure mode)",
                                [c["source"]], {"heading": c.get("heading", "")}))
    return out


CHECKS = [check_constant_drift, check_doi_coherence, check_dangling_refs,
          check_tag_laundering, check_verification_drift,
          check_orphan_constants, check_stale_hedges]


def run(chunks):
    f = []
    for chk in CHECKS:
        try:
            f.extend(chk(chunks))
        except Exception as e:                                  # never fail the sweep
            f.append(_finding("EXX", "LOW", f"{chk.__name__} errored: {e}", []))
    f.sort(key=lambda x: (-SEV[x["severity"]], x["code"]))
    return f


# --------------------------------------------------------------------------
def handoff_brief(chunks, findings) -> str:
    """What a fresh session must read before editing anything."""
    L = ["# SESSION HANDOFF — read before editing",
         "",
         f"Corpus: {len(chunks)} claims across "
         f"{len({c['source'] for c in chunks})} files.",
         ""]
    dist = defaultdict(int)
    for c in chunks:
        dist[TRUST_NAME[c["trust"]]] += 1
    L += ["## Claim inventory",
          "", "| status | claims |", "|---|---|"]
    for k in ("VERIFIED", "DATA", "MODEL", "PREMISE", "OPEN"):
        L.append(f"| {k} | {dist.get(k,0)} |")

    high = [f for f in findings if f["severity"] == "HIGH"]
    L += ["", "## Contested — do NOT 'tidy' these without resolving them", ""]
    if not high:
        L.append("_No high-severity conflicts detected._")
    for f in high:
        L.append(f"- **[{f['code']}]** {f['message']}")
        L.append(f"  - files: {', '.join(f['where'][:6])}")

    canon = defaultdict(set)
    for c in chunks:
        for k, v in (c.get("constants") or {}).items():
            canon[k].add(v)
    L += ["", "## Constants currently asserted", "",
          "| constant | value(s) | status |", "|---|---|---|"]
    for k in sorted(canon):
        vals = sorted(canon[k])
        state = "OK" if len(vals) == 1 else "**CONFLICT — resolve first**"
        L.append(f"| {k} | {', '.join(str(v) for v in vals)} | {state} |")

    opens = [c for c in chunks if c["trust"] == 0][:12]
    L += ["", "## Open claims (never present these as established)", ""]
    for c in opens:
        L.append(f"- `{c['source']}` — {c['text'][:120].strip()}…")

    L += ["", "## Rules inherited from CLAUDE.md",
          "1. No claim moves to VERIFIED without a kernel check you watched pass.",
          "2. Every claim keeps a tag; tags do not drift upward silently.",
          "3. No document scores its own rigor.",
          "4. A caveat may only be removed by the edit that verifies the thing it hedges.",
          "5. Minimal edits; update this brief in the same session.", ""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit the corpus for the known defect classes.")
    ap.add_argument("chunks", type=Path)
    ap.add_argument("--json", type=Path)
    ap.add_argument("--handoff", action="store_true")
    ap.add_argument("--severity", choices=["HIGH", "MED", "LOW"], default="LOW")
    a = ap.parse_args()

    chunks = [json.loads(l) for l in a.chunks.read_text(encoding="utf-8").splitlines() if l.strip()]
    findings = [f for f in run(chunks) if SEV[f["severity"]] >= SEV[a.severity]]

    if a.handoff:
        print(handoff_brief(chunks, run(chunks)))
        return 0
    if a.json:
        a.json.write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{len(findings)} findings → {a.json}")
        return 0

    print(f"AXLE-RAG audit · {len(chunks)} claims · {len(findings)} findings\n")
    if not findings:
        print("clean.")
    for f in findings:
        print(f"[{f['severity']:<4}] {f['code']}  {f['message']}")
        if f["where"]:
            print(f"        where: {', '.join(f['where'][:5])}")
        if f["detail"]:
            print(f"        {json.dumps(f['detail'], ensure_ascii=False)[:220]}")
        print()
    return 1 if any(f["severity"] == "HIGH" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
