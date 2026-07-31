#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
axle_rag.ingest — corpus → provenance-carrying chunks
=====================================================
G6 LLC · Principia Orthogona · AXLE-RAG · MIT License

The premise: in this corpus a chunk is not a paragraph, it is a CLAIM, and every
claim already carries its epistemic status inline — [DATA] / [MODEL] / [OPEN] /
[VALUE PREMISE] / [ASSUMPTION], plus DOIs, plus Lean kernel-verification notes.
Standard RAG throws that away by chunking on token count. This does not.

Reads .html, .md, .tex, .lean; emits JSONL, one record per chunk:

    {
      "id": "...", "text": "...", "source": "wp35-...html",
      "doi": "10.5281/zenodo.21710763", "volume": "VI", "wp": "WP-35",
      "tags": ["MODEL"], "trust": 2, "verified": false,
      "constants": {"r*": 0.77594059}, "refs": [2, 34]
    }

Trust tiers (ascending):
    0  OPEN            — explicitly not established
    1  VALUE PREMISE / ASSUMPTION — normative or planning choice
    2  MODEL           — derived inside the framework
    3  DATA            — observed / cited to external source
    4  VERIFIED        — machine-checked (Lean kernel, clean axioms)

Run:  python3 ingest.py CORPUS_DIR -o chunks.jsonl
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from dataclasses import dataclass, field, asdict
from html.parser import HTMLParser
from pathlib import Path

# --------------------------------------------------------------------------
# claim vocabulary
# --------------------------------------------------------------------------
TAGS = {
    "DATA": 3, "MODEL": 2, "OPEN": 0,
    "VALUE PREMISE": 1, "VALUE": 1, "ASSUMPTION": 1,
    "SIMULATION": 2, "VERIFIED": 4,
}
TRUST_NAME = {0: "OPEN", 1: "PREMISE", 2: "MODEL", 3: "DATA", 4: "VERIFIED"}

TAG_RE   = re.compile(r"\[(DATA|MODEL|OPEN|VALUE PREMISE|ASSUMPTION|SIMULATION|VERIFIED)\]")
DOI_RE   = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
REF_RE   = re.compile(r"\[(\d{1,3})\]")
WP_RE    = re.compile(r"\bWP-(\d{1,3})\b")
VOL_RE   = re.compile(r"\bVol(?:ume)?\.?\s+([IVX]+)\b")

# constants the corpus asserts; drift in these is the #1 defect class
CONSTANT_PATTERNS = {
    "r*":       re.compile(r"r\s*[*★]\s*(?:=|≈|~)\s*([0-9]*\.[0-9]+)"),
    "eps_0":    re.compile(r"(?:ε₀|eps_0|epsilon_0)\s*(?:=|≈)\s*([0-9]*\.?[0-9/]+)"),
    "kappa*":   re.compile(r"κ\s*[*★]?\s*(?:=|≈|≤)\s*(?:√\(?7/9\)?|sqrt\(7/9\))?\s*(?:≈)?\s*([0-9]*\.[0-9]+)?"),
    "mu_max":   re.compile(r"(?:μ(?:_?max|ₘₐˣ)|mu_max)\s*(?:=|≈)\s*(−?-?[0-9]*\.?[0-9]+)"),
    "r_s":      re.compile(r"r[_ ]?s\s*(?:=|≈)\s*([0-9]*\.[0-9]+)"),
    "tau":      re.compile(r"\bτ\s*=\s*([0-9]+)"),
    "rho":      re.compile(r"\bρ\s*(?:=|≈)\s*([0-9]*\.[0-9]+)"),
}

LEAN_CLEAN_RE = re.compile(
    r"(no\s+sorry(?:Ax)?|0\s+sorr(?:y|ys)|sorry-free|kernel-verified|kernel-checked|machine-checked)",
    re.I)
LEAN_DIRTY_RE = re.compile(r"\bsorry\b(?!-free)", re.I)


@dataclass
class Chunk:
    id: str
    text: str
    source: str
    kind: str                       # html | md | tex | lean
    heading: str = ""
    doi: str | None = None
    volume: str | None = None
    wp: str | None = None
    tags: list[str] = field(default_factory=list)
    trust: int = 2
    verified: bool = False
    constants: dict[str, float] = field(default_factory=dict)
    refs: list[int] = field(default_factory=list)

    def trust_name(self) -> str:
        return TRUST_NAME[self.trust]


# --------------------------------------------------------------------------
# HTML → blocks (keeps claim tags, drops chrome)
# --------------------------------------------------------------------------
class _Blocks(HTMLParser):
    """Extract text blocks from p/li/td/h2/h3/div.box, preserving .tag spans."""
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "td", "blockquote"}
    SKIP  = {"script", "style", "nav", "footer"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[str, str]] = []   # (heading_ctx, text)
        self._buf: list[str] = []
        self._depth = 0
        self._skip = 0
        self._heading = ""
        self._in_tag_span = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP:
            self._skip += 1
            return
        if self._skip:
            return
        cls = a.get("class", "")
        if "tag " in cls or cls.startswith("tag"):
            self._in_tag_span = True
            self._buf.append("[")
        if tag in self.BLOCK:
            self._depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
            return
        if self._skip:
            return
        if self._in_tag_span and tag == "span":
            self._buf.append("]")
            self._in_tag_span = False
            return
        if tag in self.BLOCK and self._depth:
            self._depth -= 1
            txt = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            self._buf.clear()
            if len(txt) > 40:
                if tag in ("h1", "h2", "h3", "h4"):
                    self._heading = txt
                else:
                    self.blocks.append((self._heading, txt))

    def handle_data(self, data):
        if not self._skip and self._depth:
            self._buf.append(data)


def _html_blocks(text: str) -> list[tuple[str, str]]:
    p = _Blocks()
    try:
        p.feed(text)
    except Exception:
        pass
    return p.blocks


# --------------------------------------------------------------------------
# other formats
# --------------------------------------------------------------------------
def _md_blocks(text: str) -> list[tuple[str, str]]:
    """Markdown/plain: headings set context; a heading line does not swallow the
    paragraph that follows it (that bug silently dropped whole short files)."""
    out, heading, buf = [], "", []

    def flush():
        if buf:
            t = re.sub(r"\s+", " ", " ".join(buf)).strip()
            if len(t) > 40:
                out.append((heading, t))
            buf.clear()

    for line in text.splitlines():
        ls = line.strip()
        if ls.startswith("#"):
            flush(); heading = ls.lstrip("#").strip(); continue
        if not ls:
            flush(); continue
        buf.append(ls)
    flush()
    return out


def _tex_blocks(text: str) -> list[tuple[str, str]]:
    text = re.sub(r"(?m)^\s*%.*$", "", text)                     # comments
    # tagging macros -> plain markers
    text = re.sub(r"\\tag(data|model|open|value|assume)\b",
                  lambda m: "[" + {"data": "DATA", "model": "MODEL", "open": "OPEN",
                                   "value": "VALUE PREMISE", "assume": "ASSUMPTION"}[m.group(1)] + "]",
                  text)
    out, heading = [], ""
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        m = re.match(r"\\(?:sub)*section\*?\{([^}]*)\}", para)
        if m:
            heading = m.group(1)
        para = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", " ", para)
        para = re.sub(r"[{}\\]", " ", para)
        para = re.sub(r"\s+", " ", para).strip()
        if len(para) > 40:
            out.append((heading, para))
    return out


def _lean_blocks(text: str) -> list[tuple[str, str]]:
    """One block per theorem/lemma/axiom/def, carrying its docstring."""
    out = []
    pat = re.compile(
        r"(?ms)((?:/--.*?-/\s*)?(?:noncomputable\s+)?(?:theorem|lemma|axiom|def|example)\s+[^\n]*"
        r"(?:\n(?![ \t]*(?:/--|theorem|lemma|axiom|def|example|end|namespace)).*)*)")
    for m in pat.finditer(text):
        blk = m.group(1).strip()
        name = re.search(r"(?:theorem|lemma|axiom|def|example)\s+([A-Za-z_][\w'.]*)", blk)
        out.append((name.group(1) if name else "lean", re.sub(r"\s+", " ", blk)[:1200]))
    return out


READERS = {".html": _html_blocks, ".htm": _html_blocks, ".md": _md_blocks,
           ".tex": _tex_blocks, ".lean": _lean_blocks, ".py": _md_blocks,
           ".txt": _md_blocks}


# --------------------------------------------------------------------------
def _numify(s: str) -> float | None:
    if s is None:
        return None
    s = s.replace("−", "-").strip()
    try:
        if "/" in s:
            a, b = s.split("/")
            return float(a) / float(b)
        return float(s)
    except Exception:
        return None


def build_chunk(text: str, heading: str, path: Path, kind: str,
                doc_doi: str | None, doc_vol: str | None, doc_wp: str | None) -> Chunk:
    tags = sorted(set(TAG_RE.findall(text)))
    # a chunk's trust is its WEAKEST tag: one OPEN contaminates the claim
    trust = min((TAGS[t] for t in tags), default=2)

    verified = False
    if kind == "lean":
        verified = not LEAN_DIRTY_RE.search(text)
        if verified:
            trust = 4
    elif LEAN_CLEAN_RE.search(text) and not LEAN_DIRTY_RE.search(text):
        verified = True
        trust = max(trust, 4)

    consts: dict[str, float] = {}
    for name, pat in CONSTANT_PATTERNS.items():
        m = pat.search(text)
        if m and m.lastindex:
            v = _numify(m.group(1))
            if v is not None:
                consts[name] = v

    doi = (DOI_RE.search(text).group(0).rstrip(".,;)") if DOI_RE.search(text) else doc_doi)
    wp = (("WP-" + WP_RE.search(text).group(1)) if WP_RE.search(text) else doc_wp)
    vol = (VOL_RE.search(text).group(1) if VOL_RE.search(text) else doc_vol)
    refs = sorted({int(r) for r in REF_RE.findall(text) if int(r) < 500})

    cid = hashlib.sha1(f"{path.name}|{heading}|{text[:160]}".encode()).hexdigest()[:16]
    return Chunk(id=cid, text=text, source=path.name, kind=kind, heading=heading,
                 doi=doi, volume=vol, wp=wp, tags=tags, trust=trust,
                 verified=verified, constants=consts, refs=refs)


def ingest_file(path: Path) -> list[Chunk]:
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    reader = READERS.get(path.suffix.lower())
    if not reader:
        return []
    kind = path.suffix.lstrip(".").lower()
    kind = "html" if kind in ("htm",) else kind

    head = raw[:4000]
    doc_doi = DOI_RE.search(head).group(0).rstrip(".,;)") if DOI_RE.search(head) else None
    doc_vol = VOL_RE.search(head).group(1) if VOL_RE.search(head) else None
    m = WP_RE.search(path.name) or WP_RE.search(head)
    doc_wp = "WP-" + m.group(1) if m else None

    return [build_chunk(t, h, path, kind, doc_doi, doc_vol, doc_wp)
            for h, t in reader(raw)]


def ingest_dir(root: Path, exts=None) -> list[Chunk]:
    exts = exts or set(READERS)
    out: list[Chunk] = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts:
            out.extend(ingest_file(p))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest the Principia corpus into tagged chunks.")
    ap.add_argument("root", type=Path)
    ap.add_argument("-o", "--out", type=Path, default=Path("chunks.jsonl"))
    a = ap.parse_args()

    chunks = ingest_dir(a.root)
    with a.out.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")

    dist: dict[str, int] = {}
    for c in chunks:
        dist[c.trust_name()] = dist.get(c.trust_name(), 0) + 1
    print(f"ingested {len(chunks)} chunks from {a.root} → {a.out}")
    print("trust distribution:",
          ", ".join(f"{k}={v}" for k, v in sorted(dist.items(), key=lambda kv: -kv[1])))
    n_const = sum(1 for c in chunks if c.constants)
    print(f"chunks asserting a tracked constant: {n_const}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
