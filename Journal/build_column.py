#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Pablo Nogueira Grossi / G6 LLC
"""
build_column.py — render one story into an Imaginary Origin page block.

THE PROBLEM THIS SOLVES
-----------------------
The Reading Room page ran byte-identical in No. 2, No. 3 and No. 4. Nobody was
tracking what had already been printed, so the page repeated by default. No. 5
dropped it rather than refresh it.

This script keeps a ledger (column_ledger.json) of which story ran in which
issue, refuses to print the same story twice, and tells you what is left. The
column cannot silently recycle, because repeating requires overriding a refusal.

USAGE
    # what's available, what has run
    python3 build_column.py --status

    # render the next unrun story for issue 6
    python3 build_column.py --issue 6

    # or name one explicitly
    python3 build_column.py --issue 6 --story fermat_opening.md

    # once the issue actually ships, record it
    python3 build_column.py --issue 6 --story fermat_opening.md --commit

Output is an HTML block to paste into volN.html as the Reading Room page.
Nothing is written to the journal automatically — you place it.

The stories live in the book3-starter working copy (a different repo), so the
path is configurable and checked before use.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "column_ledger.json"

DEFAULT_STORY_DIRS = [
    Path.home() / "Desktop" / "b3s" / "assignments" / "literature",
    Path.home() / "Desktop" / "book3-starter" / "assignments" / "literature",
]

# Not stories: apparatus, notes, superseded drafts, Finder duplicates.
EXCLUDE = {
    "FACT_AND_FICTION.md", "RECONCILIATION.md", "COPRODUCTION_AND_FUNDING.md",
    "README.md", "Fermat.md", "ISSUE5-PLAN.md",
    "what_the_shore_was_called.md",              # superseded
    "the_man_who_could_not_be_interesting.md",   # superseded
    "the_small_colorful_demons (1).md",
    "what_the_plague_made_easy (1).md",
}

# Suggested running order. Anything present but unlisted is offered after these.
ORDER = [
    "fermat_opening.md", "fermat_commission.md", "the_unfinished_cage.md",
    "marie_flight.md", "what_the_plague_made_easy.md",
    "the_boy_who_carried_nothing.md", "the_clerk_who_never_bathed.md",
    "what_the_sea_already_knew.md", "the_small_colorful_demons.md",
    "what_the_cat_wanted.md", "the_ceiling.md",
    "what_the_name_was_still_doing_there.md", "we_built_it_last_week.md",
    "the_children_of_the_sea.md", "o_conselheiro.md",
    "what_the_margin_was_for.md", "what_arrived_without_its_head.md",
    "what_he_had_no_idea_he_had_done.md",
]

ISSUE_ONE_DATE = date(2026, 8, 22)   # No. 5. Issues run weekly, Saturdays.
ISSUE_ONE_NUM = 5


def issue_date(n: int) -> date:
    return ISSUE_ONE_DATE + timedelta(weeks=(n - ISSUE_ONE_NUM))


def story_dir(override: str | None) -> Path:
    if override:
        p = Path(override).expanduser()
        if not p.is_dir():
            sys.exit(f"not a directory: {p}")
        return p
    for p in DEFAULT_STORY_DIRS:
        if p.is_dir():
            return p
    sys.exit("no story directory found; pass --dir")


def load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {"_note": "Which story ran in which issue. Prevents the Reading Room "
                     "from recycling, which it did in No. 2-4.", "printed": {}}


def available(d: Path) -> list[str]:
    have = {f for f in os.listdir(d) if f.endswith(".md")} - EXCLUDE
    ordered = [f for f in ORDER if f in have]
    return ordered + sorted(have - set(ordered))


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_to_html(text: str) -> tuple[str, str, str]:
    """Return (title, dateline, body_html). Deliberately minimal markdown."""
    lines = text.strip().split("\n")
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("#") else "Untitled"
    rest = lines[1:] if lines and lines[0].startswith("#") else lines

    # A short non-empty second line with a comma and a year reads as a dateline.
    dateline = ""
    for ln in rest:
        if ln.strip():
            if len(ln.strip()) < 60 and re.search(r"1[5-9]\d\d|20\d\d", ln):
                dateline = ln.strip()
                rest = rest[rest.index(ln) + 1:]
            break

    paras, buf = [], []
    for ln in rest:
        st = ln.strip()
        # A line of only dashes/asterisks is a scene break, not an em-dash.
        if re.fullmatch(r"[-*_]{3,}", st):
            if buf:
                paras.append(" ".join(buf))
                buf = []
            paras.append("\x00BREAK")
            continue
        if st:
            buf.append(st)
        elif buf:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))

    out = []
    for p in paras:
        if p == "\x00BREAK":
            out.append('          <div style="text-align:center;margin:11px 0;'
                       'color:#3a3a40;font-size:12px;letter-spacing:.3em;">&#8258;</div>')
            continue
        p = esc(p)
        p = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", p)
        p = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", p)
        p = p.replace("---", "&#8212;").replace("--", "&#8212;")
        p = _smarten(p)
        out.append(f'          <p>{p}</p>')
    return title, dateline, "\n".join(out)


def _smarten(p: str) -> str:
    """Straight quotes to typographic ones. This is a typeset publication."""
    p = re.sub(r'"(?=[^\s])', "&#8220;", p)          # opening double
    p = p.replace('"', "&#8221;")                     # the rest close
    p = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "&#8217;", p)   # don't, I'm
    p = re.sub(r"'(?=[^\s])", "&#8216;", p)          # opening single
    p = p.replace("'", "&#8217;")
    return p


# Idiom: the American Weekly Sunday supplement, and specifically Henry Clive's
# "Pin-Up Girls of History" series (No. 5, Pompadour, week of Sept 15 1946).
# The conceit there is deliberate anachronism — a 1940s magazine rendering an
# 18th-century subject — which is exactly what this serial does with Fermat's
# Toulouse, and it sits inside a journal that is already a broadsheet pastiche.
#
# Clive's signature device is the flat orange-red disc behind the head. That is
# rebuilt here in CSS as an empty tondo: the layout anticipates a portrait
# without borrowing one.
#
# NOTHING IS EMBEDDED. The 1946 plate may well be public domain — US works of
# that year required renewal at 28 years and much magazine art was never renewed
# — but that is a records question (Catalog of Copyright Entries), not an
# assumption to publish on. This journal carries a DOI and a CC BY-NC-ND notice.
DISC, INK, PAPER = "#d4552a", "#221a14", "#f0e6d2"
GOWN, ROSE, DIM = "#3d5a80", "#b5321f", "#6f6455"


def _supplement_rule() -> str:
    """The double rule a supplement sets under its section line."""
    return (f'<div aria-hidden="true" style="border-top:2px solid {INK};'
            f'border-bottom:1px solid {INK};height:3px;margin:0 0 10px;"></div>')


def render(story: str, path: Path, n: int, seq: int, total: int) -> str:
    raw = path.read_text(encoding="utf-8")
    title, dateline, body = md_to_html(raw)
    words = len(raw.split())

    # Drop cap, as the supplement set its opening paragraph.
    m = re.search(r"<p>(&#\d+;|\w)", body)
    if m:
        ch = m.group(1)
        body = body.replace(
            f"<p>{ch}",
            f'<p><span style="float:left;font-family:Georgia,serif;font-size:46px;'
            f'line-height:.8;padding:3px 7px 0 0;color:{ROSE};">{ch}</span>', 1)

    dl = (f'<div style="font-family:Georgia,serif;font-style:italic;font-size:12px;'
          f'color:{DIM};margin:0 0 2px;">{esc(dateline)}</div>' if dateline else "")

    return f'''<!-- THE READING ROOM · No. {n} · {issue_date(n).strftime("%B %-d, %Y")}
     story: {story} ({words} words) · part {seq} of {total}
     Built in the American Weekly idiom — Henry Clive's "Pin-Up Girls of History"
     ran as a numbered series with a banner naming the part ("No. 5 Pompadour").
     The coral ground and the tondo are CSS. NO PLATE IS EMBEDDED: this page
     carries a DOI and a CC BY-NC-ND notice, and the 1946 art's renewal status
     is unverified. Do not paste a found scan in here.
     generated by build_column.py — record it with --commit once the issue ships -->
<div class="pg" style="background:{PAPER};">

  <!-- section masthead, after the supplement's own -->
  <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:10px;
       padding:12px 18px 0;">
    <div style="font-family:Georgia,'Iowan Old Style',serif;line-height:.86;color:{INK};">
      <span style="font-size:12px;letter-spacing:.02em;">The</span>
      <span style="font-size:30px;letter-spacing:-.02em;">Reading Room</span>
    </div>
    <div style="font-family:Georgia,serif;font-size:10px;color:{ROSE};text-align:right;
         letter-spacing:.04em;padding-bottom:3px;white-space:nowrap;">
      A Serial in 18 Parts &#183; {"Begins Here" if seq==1 else f"No.&#8202;{seq}"}<br>{issue_date(n).strftime("Week of %B %-d, %Y")}
    </div>
  </div>
  <div style="padding:0 18px;">{_supplement_rule()}</div>

  <!-- coral ground with an empty tondo where the plate would sit -->
  <div style="position:relative;margin:0 18px;padding:16px 18px;overflow:hidden;
       background:linear-gradient(150deg,#ef8a5f 0%,{DISC} 55%,#c2461f 100%);">
    <div aria-hidden="true" style="position:absolute;top:-34px;right:-30px;width:172px;height:172px;
         border-radius:50%;background:rgba(255,238,214,.16);
         border:1px solid rgba(255,238,214,.34);"></div>
    <div style="position:relative;max-width:72%;">
      {dl}
      <div style="font-family:Georgia,'Iowan Old Style',serif;font-size:clamp(24px,3.8vw,34px);
           line-height:1.04;color:#fff6e8;text-shadow:0 1px 0 rgba(0,0,0,.18);">{esc(title)}</div>
    </div>
  </div>

  <!-- The three-zone banner. Clive's ran:
         No.14 Lola Montez        Pin-Up Girls of History        by Henry Clive
        (Posed by Gene Tierney)                     See John Erskine's Story on Page 2
       Left: numbered part and subject, with a parenthetical credit.
       Centre: the series. Right: byline and cross-reference. -->
  <div style="margin:0 18px;padding:10px 16px;background:{INK};color:{PAPER};
       display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:14px;">

    <div style="font-family:Georgia,serif;line-height:1.15;">
      <div style="font-size:14px;">No.&#8202;{seq}&#8194;{esc(title)}</div>
      <div style="font-size:9.5px;color:#f0b49a;font-style:italic;">{esc(dateline) or "a serial in parts"}</div>
    </div>

    <div style="font-family:Georgia,serif;font-style:italic;font-size:clamp(17px,2.6vw,23px);
         white-space:nowrap;letter-spacing:.01em;">Pierre et Mademoiselle</div>

    <div style="font-family:Georgia,serif;text-align:right;line-height:1.15;">
      <div style="font-size:12px;font-style:italic;">by Pablo Nogueira Grossi</div>
      <div style="font-size:9px;color:#f0b49a;">See the note on fact &amp; fiction</div>
    </div>
  </div>

  <div style="padding:13px 18px 0;column-count:2;column-gap:22px;font-size:12.5px;
       line-height:1.56;color:{INK};text-align:justify;hyphens:auto;">
{body}
  </div>

  <div style="margin:13px 18px 0;padding-top:8px;border-top:1px solid rgba(34,26,20,.2);
       font-size:9.5px;color:{DIM};line-height:1.5;">
    <span style="color:{ROSE};letter-spacing:.14em;text-transform:uppercase;">Part {seq} of {total}</span>
    &#8194;&#183;&#8194; Fiction, drawn from the documented record; what is invented and what is
    not is set out in the series&#8217; own note on fact and fiction.
    &#169; 2026 Pablo Nogueira Grossi &#183; G6 LLC.
  </div>
</div>'''


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", type=int, help="issue number, e.g. 6")
    ap.add_argument("--story", help="filename; default is the next unrun one")
    ap.add_argument("--dir", help="path to the literature folder")
    ap.add_argument("--commit", action="store_true", help="record it as printed")
    ap.add_argument("--status", action="store_true", help="show what has run")
    a = ap.parse_args()

    d = story_dir(a.dir)
    led = load_ledger()
    printed = led["printed"]
    avail = available(d)
    unrun = [s for s in avail if s not in printed]

    if a.status or not a.issue:
        print(f"stories in {d}: {len(avail)}   printed: {len(printed)}   remaining: {len(unrun)}")
        if printed:
            print("\n  already printed:")
            for s, n in sorted(printed.items(), key=lambda kv: kv[1]):
                print(f"    No. {n:<3} {s}")
        print("\n  next up:")
        for s in unrun[:6]:
            print(f"    {s}")
        if not unrun:
            print("    (none — the serial has run its course)")
        return

    story = a.story or (unrun[0] if unrun else None)
    if not story:
        sys.exit("no unrun stories left; pass --story to reprint deliberately")
    if story in printed and not a.story:
        sys.exit(f"{story} already ran in No. {printed[story]}")
    if story in printed:
        print(f"  WARNING: {story} already ran in No. {printed[story]}. "
              f"Recycling is what this script exists to prevent.", file=sys.stderr)
    p = d / story
    if not p.exists():
        sys.exit(f"not found: {p}")

    seq = len(printed) + 1
    if a.commit:
        printed[story] = a.issue
        LEDGER.write_text(json.dumps(led, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"recorded: {story} -> No. {a.issue}", file=sys.stderr)
    else:
        print(f"(preview — not recorded; add --commit once No. {a.issue} ships)", file=sys.stderr)
    print(render(story, p, a.issue, seq, len(avail)))


if __name__ == "__main__":
    main()
