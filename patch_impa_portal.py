#!/usr/bin/env python3
"""
patch_impa_portal.py
====================
Inserts Chapter η into AXLE's impa-portal.html at two locations:

  (1) Nav bar — adds  <a href="chapter-eta-dnls.html">Chapter η</a>
      immediately after the existing  Chapter E  link.

  (2) Chapter card grid — adds a `.ch-lnk` card for Chapter η
      immediately after the existing Chapter E card and before
      the Bonus Chapter W card.

Idempotent: if "chapter-eta-dnls.html" is already in the file at the
expected nav position, the script exits without modification.

Usage
-----
    cd /path/to/AXLE                  # local clone of TOTOGT/AXLE
    python3 patch_impa_portal.py impa-portal.html

Optional dry-run / diff:
    python3 patch_impa_portal.py impa-portal.html --dry-run
    diff impa-portal.html impa-portal.html.patched

License: MIT
Author:  Pablo Nogueira Grossi, G6 LLC, 2026
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# The two patches. Each is (find, replace) — both `find` strings must be
# unique substrings of the live portal so str.replace() lands precisely.
# --------------------------------------------------------------------------

NAV_FIND = '<a href="https://totogt.github.io/3M/chE-gtct.html">Chapter E</a>'
NAV_REPLACE = (
    NAV_FIND
    + '\n    <a href="chapter-eta-dnls.html">Chapter η</a>'
)

CARD_FIND = (
    '<a href="https://totogt.github.io/3M/chE-gtct.html" class="ch-lnk">'
    '<div><div class="ch-tag">Bonus Chapter E</div>'
    '<div class="ch-ttl">GTCT for Everyone — Nine Axioms</div></div>'
    '<div class="ch-arr">→</div></a>'
)
CARD_REPLACE = (
    CARD_FIND
    + '\n    '
    + '<a href="chapter-eta-dnls.html" class="ch-lnk">'
      '<div><div class="ch-tag">Chapter η · Mini-Beast</div>'
      '<div class="ch-ttl">Tribonacci as Critical Constant — DNLS, η ≈ 1.839287</div></div>'
      '<div class="ch-arr">→</div></a>'
)

PATCHES = [
    ("nav bar", NAV_FIND, NAV_REPLACE),
    ("chapter card grid", CARD_FIND, CARD_REPLACE),
]

# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "path",
        type=Path,
        help="path to impa-portal.html in your local AXLE clone",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would change without writing the file",
    )
    args = ap.parse_args()

    if not args.path.exists():
        print(f"error: {args.path} does not exist", file=sys.stderr)
        return 1

    src = args.path.read_text(encoding="utf-8")

    # Idempotency check: bail if Chapter η link already in nav
    if 'href="chapter-eta-dnls.html"' in src:
        print(
            "Chapter η link already present in",
            args.path,
            "— no changes made.",
        )
        return 0

    out = src
    for label, find, replace in PATCHES:
        if find not in out:
            print(
                f"error: patch anchor for {label!r} not found in",
                args.path,
                "(file structure may have drifted; aborting)",
                file=sys.stderr,
            )
            return 2
        out = out.replace(find, replace, 1)
        print(f"  patched: {label}")

    if args.dry_run:
        out_path = args.path.with_suffix(args.path.suffix + ".patched")
        out_path.write_text(out, encoding="utf-8")
        print(
            f"dry-run: wrote candidate to {out_path}; "
            f"diff {args.path} {out_path}"
        )
    else:
        args.path.write_text(out, encoding="utf-8")
        print(f"wrote: {args.path}  (now {len(out):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
