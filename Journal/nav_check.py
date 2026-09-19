#!/usr/bin/env python3
"""Walk the journal from the first issue to the last and fail on any break.

Usage:  python3 Journal/nav_check.py          (from the AXLE repo root or Journal/)

The run is not named the way the files are. `index.html` IS No. 2 -- it is both
the journal's landing page and an issue -- and the numbered files start at
`vol3.html`. A reader who wants to go from the beginning to the end therefore
walks index.html -> vol3 -> ... -> vol10, and every hop is a link in a colophon
that somebody typed.

This script does the walk. For each issue it checks:

  1. the file exists;
  2. its <title> carries the issue number the walk expects;
  3. its colophon links BACK to the previous issue;
  4. its colophon links FORWARD to the next issue -- except the last, which
     must instead say it is the last and point at the archive;
  5. every local href in the file resolves.

It also reports, without failing, the issues that exist on disk but are held
back from the public chain. Vol. 11 is one: its Reading Room page carries
"do not publish this page", so nothing in the published run links to it, and a
script that "helpfully" wired it in would publish an unfinished issue.

WHY THE FORWARD LINK IS THE ONE THAT ROTS
Back-links get written when an issue is made, because the previous issue is
sitting there. The forward link has to be added to the PREVIOUS issue after the
new one exists, which means going back into a file that already looked
finished. On 2026-09-19 both No. 9 and No. 10 were missing theirs: a reader
walking forward from No. 2 stopped at No. 9, and No. 10 was reachable only by
typing its URL.
"""
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent

# issue number -> filename, and the strapline the run list uses
RUN = [
    (2,  "index.html",  "Outside Verification"),
    (3,  "vol3.html",   "The Desk Audits Its Own House"),
    (4,  "vol4.html",   "Chladni Plates in the Classroom"),
    (5,  "vol5.html",   "Where the Money Is"),
    (6,  "vol6.html",   "Seven Ways a Proof Can Be True and Useless"),
    (7,  "vol7.html",   "Thirteen Months on the Same Stream"),
    (8,  "vol8.html",   "The One Instrument Ever Pointed at Nepal"),
    (9,  "vol9.html",   "Two Instruments, Thirty Years, Neither Quoted"),
    (10, "vol10.html",  "The Identity That Is Not in the Library"),
]
HELD_BACK = [(11, "vol11.html", "The Graph He Never Drew")]


def colophon(t):
    i = t.find('<div class="colophon">')
    return t[i:i + 2000] if i >= 0 else ""


def main():
    fail, note = [], []
    n = len(RUN)

    for idx, (num, fname, strap) in enumerate(RUN):
        p = HERE / fname
        if not p.exists():
            fail.append("No. %d: %s does not exist" % (num, fname))
            continue
        t = p.read_text(encoding="utf-8", errors="replace")

        m = re.search(r"<title>(.*?)</title>", t, re.S)
        title = " ".join(m.group(1).split()) if m else ""
        if ("No. %d " % num) not in title and ("No. %d" % num) not in title:
            fail.append("No. %d: %s titles itself %r" % (num, fname, title[:70]))

        col = colophon(t)
        if idx > 0:
            prev_file = RUN[idx - 1][1]
            if ('href="%s"' % prev_file) not in col:
                fail.append("No. %d: no back-link to %s in the colophon" % (num, prev_file))
        if idx < n - 1:
            next_file = RUN[idx + 1][1]
            if ('href="%s"' % next_file) not in col:
                fail.append("No. %d: NO FORWARD LINK to %s -- the walk stops here"
                            % (num, next_file))
        else:
            if "Latest issue" not in col:
                fail.append("No. %d is the last issue and does not say so" % num)
            if 'href="index.html"' not in col:
                fail.append("No. %d is the last issue and does not point back at the archive" % num)

        bad = [h for h in re.findall(r'href="([^"#?]+)"', t)
               if not h.startswith(("http", "mailto", "/")) and not (HERE / h).exists()]
        if bad:
            fail.append("No. %d: unresolved local links %s" % (num, sorted(set(bad))))

        pages = t.count('<section class="pg')
        print("  No. %-3d %-12s pages %-2d  %s" % (num, fname, pages, strap))

    for num, fname, strap in HELD_BACK:
        p = HERE / fname
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        held = "do not publish this page" in t.lower()
        linked = [f for _, f, _ in RUN
                  if ('href="%s"' % fname) in (HERE / f).read_text(encoding="utf-8", errors="replace")]
        print("  No. %-3d %-12s HELD BACK  (%s)" % (num, fname,
              "carries a do-not-publish marker" if held else "no marker"))
        if held and linked:
            fail.append("No. %d carries a do-not-publish marker and is linked from %s"
                        % (num, linked))
        if not held and not linked:
            note.append("No. %d no longer carries a do-not-publish marker and is still "
                        "outside the run -- add it to RUN when it ships" % num)

    if not (HERE / "vol1.html").exists() and not (HERE / "vol2.html").exists():
        note.append("There is no file for No. 1. The run as published begins at No. 2, "
                    "which is index.html. Searched: filenames, page titles, git history "
                    "for an added vol1/vol2, and the live site. Reported, not invented.")

    print()
    for x in note:
        print("  NOTE  " + x)
    for f in fail:
        print("::error::" + f)
    if fail:
        return 1
    print("the walk runs No. 2 to No. %d without a break." % RUN[-1][0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
