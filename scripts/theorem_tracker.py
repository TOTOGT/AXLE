#!/usr/bin/env python3
"""
theorem_tracker.py — scans this repo's top-level .lean files (NOT the
.lake/ dependency checkouts, and NOT the sprawl of domain subfolders,
which still contain unresolved duplicate/orphaned copies — see the
pending "diverged filename collisions" / "orphaned GTCT duplicate Lean
files" cleanup tasks) for theorem/lemma declarations, and classifies
each as "proved" or "sorry" (declaration body contains the `sorry`
tactic). Emits a shields.io "endpoint" badge JSON:
https://shields.io/badges/endpoint-badge

CAVEAT (documented on purpose, not discovered later): this is a plain
text/regex heuristic, not a real proof check. It does NOT run Lean, so
it can't tell you a file actually compiles — it can only tell you
which declarations in files that DO compile still contain `sorry`.
The one place this could theoretically misfire is a declaration whose
trailing comment mentions the word "sorry" in prose without an actual
`sorry` tactic in the proof body — in this repo's actual files, that
hasn't happened (comments here always accompany a real `sorry`), but a
stricter future version should parse the `declaration uses 'sorry'`
warnings straight out of `lake build -v` output instead, since those
come directly from the elaborator and can't have false positives.

Usage:
  python3 scripts/theorem_tracker.py [--root .] [--recursive] [--write badges/theorem-status.json]
"""
import re
import json
import argparse
from pathlib import Path

DECL_RE = re.compile(r"^(theorem|lemma)\s+([A-Za-z_][\w.']*)", re.MULTILINE)
BOUNDARY_RE = re.compile(
    r"^(theorem|lemma|def|noncomputable def|instance|abbrev|structure|class|namespace|end|section|variable)\b",
    re.MULTILINE,
)


def find_lean_files(root: Path, recursive: bool):
    if recursive:
        return sorted(p for p in root.rglob("*.lean") if ".lake" not in p.parts)
    return sorted(root.glob("*.lean"))


def split_declarations(text: str):
    """Split a Lean source file into (name, body) chunks, one per
    top-level theorem/lemma, running from its declaration line up to
    (but not including) the next top-level declaration boundary."""
    starts = [m.start() for m in DECL_RE.finditer(text)]
    names = [m.group(2) for m in DECL_RE.finditer(text)]
    bounds = [m.start() for m in BOUNDARY_RE.finditer(text)]
    decls = []
    for name, start in zip(names, starts):
        later = [b for b in bounds if b > start]
        end = later[0] if later else len(text)
        decls.append((name, text[start:end]))
    return decls


def scan(root: Path, recursive: bool):
    proved, sorried = [], []
    for f in find_lean_files(root, recursive):
        text = f.read_text(errors="ignore")
        for name, body in split_declarations(text):
            target = sorried if re.search(r"\bsorry\b", body) else proved
            target.append(f"{f.name}:{name}")
    return proved, sorried


def badge_json(proved, sorried):
    total = len(proved) + len(sorried)
    pct = (len(proved) / total * 100) if total else 0
    color = (
        "brightgreen" if pct >= 95 else
        "green" if pct >= 80 else
        "yellow" if pct >= 50 else
        "orange"
    )
    return {
        "schemaVersion": 1,
        "label": "theorems",
        "message": f"{len(proved)} proved · {len(sorried)} sorry",
        "color": color,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--recursive", action="store_true",
                     help="also scan domain subfolders (currently inflated by known duplicate files)")
    ap.add_argument("--write", default=None, help="path to write the badge JSON")
    args = ap.parse_args()

    root = Path(args.root)
    proved, sorried = scan(root, args.recursive)
    data = badge_json(proved, sorried)

    print(json.dumps(data, indent=2))
    print(f"\nproved ({len(proved)}):")
    for n in sorted(proved):
        print(" ", n)
    print(f"\nsorry ({len(sorried)}):")
    for n in sorted(sorried):
        print(" ", n)

    if args.write:
        out = Path(args.write)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, indent=2))
        print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
