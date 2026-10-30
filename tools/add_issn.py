#!/usr/bin/env python3
"""Add the ISSN (3144-6787, online; U.S. ISSN Center, APPL0007838, notice of 2026-10-22) to the
footer of every Imaginary Origin page in Journal/.  Dry run by default; --write to change files.
Idempotent: a page that already carries the ISSN is left alone.  A page whose footer does not match the
expected wording is REPORTED, never guessed at."""
import re, sys
from pathlib import Path
J = Path(__file__).resolve().parent.parent / "Journal"
OLD = "The Generative Science Journal &#183; Vol."
NEW = "The Generative Science Journal &#183; ISSN 3144-6787 (Online) &#183; Vol."
write = "--write" in sys.argv
changed, already, nomatch = [], [], []
for p in sorted(J.glob("*.html")):
    t = p.read_text(encoding="utf-8")
    if "Imaginary Origin" not in t: continue
    if "ISSN 3144-6787" in t: already.append(p.name); continue
    if t.count(OLD) == 1:
        changed.append(p.name)
        if write: p.write_text(t.replace(OLD, NEW), encoding="utf-8")
    else:
        nomatch.append((p.name, t.count(OLD)))
print(("WROTE" if write else "DRY RUN"), "changed:", len(changed), changed)
print("already had it:", already)
print("footer did not match exactly once (not touched):", nomatch)
