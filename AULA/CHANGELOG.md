# AULA reorganization — 2026-07-07

Executed the structure proposed in `AULA_Programme_Structure_Proposal.md`, using only content that already existed in the repo. No new lesson content was written.

## Moved

- `101/` created — Lesson03_Number33.html, Lesson03b_Chladni_Plates.html, Lesson04_USA_Top10.html
- `102/` created — Lesson02_Cajueiro_Principle.html, Lesson02b_Galilean_Confluence.html, CropCircles.html (+ its 4 glyph images), Lesson07_Alpha_Submission_v2.html
- `103/` created — Lesson01_Vitruvian_Approximation.html, voynich-caela-lesson.html
- `assets/` created — 2 unreferenced screenshots + autopost_pipeline.zip (kept, not currently linked from anywhere)
- `index.html`, `caela-framework.html`, `g6-earth-house.html`, `README.md` stayed at AULA root

## Fixed

- Rewrote every internal `href` in the 9 moved lesson files so cross-lesson links, links back to `index.html`/`caela-framework.html`, and `#anchor` links to homepage sections resolve correctly from the new subfolder depth.
- Removed a vestigial second `<nav>` block inside Lesson 07 that pointed to `../../index.html`, `../../portal.html`, and a nonexistent `Lesson06_WorldQuant_Top10.html` — all three were broken. The lesson's real nav (which already worked) was left in place.
- `index.html`: removed the "Student Portal" nav/footer/enroll links, since `AULA/portal.html` doesn't exist (a different, unrelated `portal.html` lives at the repo root — see proposal doc, item 2).
- `index.html`: removed the two homepage cards linking to `Lesson05_Your_First_Reel.html` and `Lesson05b_Media_Kit.html` (files don't exist) and replaced them with `coming-soon` cards, matching the site's existing convention for unwritten lessons — so the plan is still visible but nothing 404s.
- `index.html`: rebuilt the lessons section into three tier blocks (AULA 101/102/103) and added cards for Lesson02b, Lesson03 (was wrongly marked "coming soon" — it's fully built), Lesson03b, and CropCircles, none of which were previously linked from the homepage.
- `index.html`: added a card linking to `../course-16weeks.html` (the "English for Researchers" 16-week track) as an optional 104 capstone.
- `caela-framework.html`: updated its 8 lesson links to the new subfolder paths.

## Not done (needs a decision from you)

- Lesson02 (Cajueiro) level conflict: the current file is tagged B2–C1. An older A2–B1 draft exists only inside `assignments/lessons/index.html` at the repo root (not moved/touched). Left as-is — current AULA version treated as canonical.
- Duplicate/orphaned files elsewhere in the repo (`assignments/`, root-level `Lesson07_Alpha_Submission_v2.html`, `Finance/Lesson4.html`, `a.PolyLaminin/Lesson7.html`, etc.) were **not** deleted — this reorg only touched `AULA/`. Say the word if you want those retired too.
- Lesson 05, Lesson 05b, and an ESL-specific Student Portal still don't exist as content — homepage now says so honestly instead of 404ing.

## How to publish this

This was rebuilt in a local scratch folder from a fresh clone of `TOTOGT/AXLE`, not by editing the live repo directly (no GitHub write access from here). To publish: copy the contents of this AULA folder over the `AULA/` folder in your local git checkout of TOTOGT/AXLE, review the diff, commit, and push.

---

# Update — 2026-07-07, later same day

## New: The Preemie Manual (`day-by-day/preemie-manual.html`)

First chapter of "Day by Day — A Parent's Science Guide to the First Years." Car-manual conceit: specs (prematurity classification), the odometer (corrected vs. chronological age), dashboard warning lights (red/amber symptom tiers), a maintenance schedule (ROP exam, hearing screen, vaccines-by-chronological-age, well-checks), an equipment chapter (oxygen concentrator filter care, apnea monitor, feeding pump), troubleshooting, and a day-by-day conception-to-birth timeline starting at Day 21 (heart begins beating). Linked from the homepage "Day by Day" book card, which was previously "Coming soon."

Includes an interactive planner: enter conception date and/or due date and/or actual birth date, get live corrected age, prematurity classification, an auto-generated maintenance-schedule checklist, and a growth tracker with a real percentile chart. Growth percentiles are computed from the official WHO Child Growth Standards LMS reference tables (weight/length/head-circumference-for-age, birth to 2 years), pulled from the WHO org's own GitHub `anthro` package — not approximated. All dates are stored only in the browser (localStorage), nothing is sent anywhere. Sources are cited at the bottom of the page.

One caveat worth knowing: the WHO LMS data I embedded produced a materially different **L** (skew) parameter than the example CDC publishes on its own site for the same age/sex, even though the **M** (median) values agree closely with independent sources at several checkpoints (birth, 6mo, 12mo). Medians/round numbers on the tool should be solid; percentiles in the tails (very low/very high) may drift somewhat from what your pediatrician's exact chart shows. The page already says to treat this as educational and defer to your care team's official chart — flagging it here too so you know the shape of the uncertainty.

## Fixed: the dm³ 101/102/103 course (48 weekly pages + 3 course landing pages + series hub)

You moved this content into `AULA/101/`, `102/`, `103/` — the same folder names I'd just used for the ESL lesson tiers. To avoid burying one under the other, I renamed the ESL tier folders to `esl-101/`, `esl-102/`, `esl-103/` (updated every reference in `index.html`, `caela-framework.html`, and the 9 ESL lesson files — no broken links introduced). `101/`, `102/`, `103/` are now exclusively the dm³ course weekly files, matching your original "using the 101, 102, 103 course" instruction.

Then fixed the dm³ course itself — it had 671 broken links across 56 files. Breakdown:
- Path-depth bugs (links to `course-dm3-10X.html`, `classroom-index.html`, week-to-week links, etc. missing `../` or a tier prefix): fixed, same category of bug as the ESL lessons.
- Links to `living-book.html`, `Sportal.html`, `impa-portal.html`, `ch-turing-morphogenesis.html`, `ch-lorenz-chaos.html`, `ch-mandelbrot-fractals.html`: these files aren't in this local AULA folder but do exist in the real `TOTOGT/AXLE` repo, one or two levels above `AULA/` (repo root and `book3/`). Pointed the links there with correct relative paths — they'll resolve once this folder is placed back into an actual checkout of the repo.
- `hub.html` → repointed to `classroom-index.html` (the "Book 3 Classroom" page — best match for what a course-wide hub should be).
- `series-hub.html` → repointed to `103/dm3-courses-101-102-103.html` (the page that actually lists all 48 weeks across all three courses).
- `chPI-recurrence.html`, `ch9-phi.html`, `chOmega-hexabonacci.html`, `chT-tubulin.html`, and about a dozen `course-16weeks.html` chapter links (`ch1.html`, `prelude.html`, etc.): these don't exist anywhere in the repo — genuinely unwritten. Grayed out into non-clickable labels ("Not yet published" on hover) instead of leaving them as dead links. Full list is searchable in the files by the inline `opacity:.4` style if you want to find every instance later.

Also surfaced the dm³ track on the homepage — it wasn't linked from `index.html` at all before. Added a new section with cards for dm³ 101/102/103 and the series hub.

## Also noticed, not touched

`course-16weeks.html` and `course-16weeks-source.html` are near-duplicates (identical opening content) sitting side by side in this folder, and there's a third "English for Researchers" variant at `103/dm3-course-landing.html`. Didn't merge or delete anything — just flagging the duplication for whenever you're ready to consolidate.

---

# Update — 2026-07-07, third pass

## Scrubbed: UCEDA School of Elizabeth

Removed every reference to the third-party "UCEDA School of Elizabeth" across the site — this is now a fully independent Hour House programme. Touched 11 files: `index.html`, `caela-framework.html`, `g6-earth-house.html`, `esl-102/Lesson07_Alpha_Submission_v2.html`, `esl-103/voynich-caela-lesson.html`, and 6 more lesson files carrying the small promotional card. In each case the UCEDA promo card/section was removed (grids collapsed to single-column where UCEDA was the second card), CSS classes renamed `uceda-*` → `enroll-*`, and prose mentioning "Hour House and UCEDA" rephrased to reference Hour House alone. Verified with a div-tag balance check after each pass (`esl-102/Lesson07_Alpha_Submission_v2.html` needed a manual fix after a regex left an orphaned `enroll-footer` fragment — caught by the balance check, fixed by hand).

Two orphaned UCEDA image files remain in `assets/` (`Screen Shot 2026-05-28 at 6.20.49 PM.png` — UCEDA QR code, `Screen Shot 2026-05-28 at 6.23.03 PM.png` — UCEDA logo). Deletion was requested and declined — left in place; delete manually or ask again if you change your mind.

## Documented: CAELA to plan, WPPPW to deliver

Added a callout to `caela-framework.html` explaining the real Hour House methodology: lessons are *planned* against the full CAELA/WIPPEA standard, but *delivered* as a leaner five-beat flow — **Warm-Up → Presentation → Practice → Production → Wrap-Up (WPPPW)** — with a self-study quiz built into Wrap-Up so a student working alone still gets a check on what they produced. This is the format used going forward for new lessons (see below).

## New: Lessons 05, 05b, 06 — the first WPPPW-format lessons

Built the three "coming soon" placeholders into full lessons, all delivered in WPPPW with an embedded Wrap-Up quiz:

- **`esl-101/Lesson05_Your_First_Reel.html`** (B1–B2, 120 min) — using Gemini to summarize/translate a public video, remixing it in the standalone Instagram Edits app (watermark-free export, "Add Yours" remix sticker), and building a 7-day posting plan. Production stage has students storyboard, write a bilingual caption, and draft a posting cadence — no video is actually required to complete the lesson's graded language output.
- **`esl-102/Lesson05b_Media_Kit.html`** (B1–B2, 120 min) — the five parts of a creator media kit, Gemini-assisted bio drafting, building a one-page PDF in Canva, and an affiliate-program submission checklist (Shopee's own affiliate program, or a general network like impact.com). Explicitly flags — in Production and in the quiz — that payment/payout details are never entered into a form during class.
- **`esl-102/Lesson06_WorldQuant_Top10.html`** (B1–B2, 90 min) — a companion to Lesson 04, reusing the same May 2026 IQC leaderboard dataset but adding a new derived statistic (score per participant) so students can compare "scale" vs. "efficiency" strategies across the ten countries. All ratios are freshly computed from Lesson 04's published numbers, not fabricated — e.g. China's is an outlier at ~2,191 points/participant vs. the USA's ~290, which reframes the USA's problem as partly an efficiency gap, not only a participation gap.

Wired all three into `index.html` (replaced the `coming-soon` cards with live links, matching the site's existing card markup) and into `caela-framework.html`'s lesson-links grid (between Lesson 04 and Lesson 07, tagged "5 stages · WPPPW"). Verified with the standard div-tag balance check (all 5 touched files balanced) and a full-tree link scan (0 new broken links from any of this work — the pre-existing broken-looking links to `living-book.html`, `Sportal.html`, `book3/ch-*.html` etc. are expected: per the previous update, those resolve once this folder sits inside the real repo checkout, one level above where this local mirror can see).
