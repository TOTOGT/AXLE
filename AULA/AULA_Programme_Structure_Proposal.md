# AULA Programme Structure — Proposal

Hour House / Principia Orthogona · TOTOGT/AXLE repo · Drafted 2026-07-07

This is a proposal only — no files have been moved or edited yet. It maps what actually exists in the repo right now against what the live site claims exists, and proposes a 101/102/103 structure to organize it. Review it, then tell me which parts to execute.

## 1. What's actually in AULA/ right now

The `AULA/` folder in TOTOGT/AXLE contains 12 HTML files:

- `index.html` — homepage
- `caela-framework.html` — WIPPEA/CAELA reference page
- `Lesson01_Vitruvian_Approximation.html` — B2–C1, 120 min, 7 stages
- `Lesson02_Cajueiro_Principle.html` — B2–C1, 110–130 min, 6 stages
- `Lesson02b_Galilean_Confluence.html` — B2–C1, 120 min, 7 stages
- `Lesson03_Number33.html` — B2–C1, 100–120 min, 6 stages
- `Lesson03b_Chladni_Plates.html` — B1–B2+, 90–120 min, 5 stages
- `Lesson04_USA_Top10.html` — B1–B2+, 90–110 min, 4 stages
- `Lesson07_Alpha_Submission_v2.html` — B1–B2+, 120 min, 7 stages
- `voynich-caela-lesson.html` — B2–C1, 120 min, final project
- `CropCircles.html` — newest class (per README, added June 25)
- `g6-earth-house.html` — a facilities/site plan, not a lesson
- `README.md`

## 2. What's broken on the live homepage right now

`AULA/index.html` links to three files that don't exist anywhere in the repo:

- `Lesson05_Your_First_Reel.html` — 404
- `Lesson05b_Media_Kit.html` — 404
- `AULA/portal.html` — 404 (a *different* `portal.html` exists at the repo root, but it's the Principia Orthogona A1→D2 research-prompt portal, not an ESL student portal — publishing it under this link would be the wrong content anyway)

Meanwhile, the homepage **undersells what already exists**: Lesson02b, Lesson03, and Lesson03b are fully built (with stages, timing, vocabulary — real content) but aren't linked from `index.html` at all. The homepage still marks "03 — Coming soon." `caela-framework.html` links to all of them correctly, so the homepage is just stale relative to the rest of the site.

There's also a level-label conflict: one draft of Lesson02 (Cajueiro) is tagged B2–C1 in the file itself, but an earlier "coming soon" version embedded in `assignments/lessons/index.html` tags the same lesson A2–B1. Two different difficulty targets for the same lesson — worth resolving before publishing a leveled programme.

## 3. Scattered duplicates elsewhere in the repo (the "48 files" problem)

Across the full repo (175 HTML files total), lesson-shaped content is scattered outside AULA in at least these places:

- `assignments/lessons/index.html` — a single long page that re-embeds the *full text* of Lessons 01–04 inline (a second, older copy of content that now also lives as standalone AULA files)
- `assignments/lessons/Lesson3.html`, `assignments/lessons/Lesson7.html`, `assignments/lessons/lesson2.html`, `assignments/Lesson7.html` — individual orphaned duplicates
- `Lesson07_Alpha_Submission_v2.html` and `Lesson07_Alpha_Submission (1).html` at the repo **root** — duplicates of the AULA version
- `Finance/Lesson4.html`, `a.PolyLaminin/Lesson7.html` — topic-folder duplicates
- `course-16weeks.html` (repo root) — a distinct, more advanced "English for Researchers, C1→D2" 16-week programme built on the same operator framework, but aimed at academic publishing rather than general ESL
- `portal.html` (repo root) — the Principia Orthogona A1→D2 prompt portal (general research-reading levels, not tied to Hour House lesson numbering)

None of this is in `AULA/`. Right now a lesson can exist in two or three places at slightly different revisions, and there's no single source of truth.

## 4. Proposed structure: AULA as the one home, three tiers

Keep `AULA/` as the canonical folder for every Hour House lesson (matches your framework — CAELA/WIPPEA pages already live there, and it's the folder GitHub Pages actually serves lessons from). Retire or redirect the duplicates elsewhere in the repo once content is confirmed current in AULA.

Inside AULA, organize the existing + planned lessons into three tiers, using the CEFR bands the lessons already carry:

**AULA 101 — Foundations (A2–B1)**
Entry point. Shorter, more visual, less text-heavy.
- Lesson 03b — Chladni Plates (B1–B2+, sound/physics, hands-on)
- Lesson 04 — USA Top 10 (B1–B2+, data reading)
- Lesson 03 — Number 33 (resolve which level draft is canonical)
- *Missing:* Lesson 05 — Your First Reel (linked, not written)

**AULA 102 — Intermediate/Upper-Intermediate (B1–B2 / B2–C1)**
- Lesson 02 — Cajueiro Principle (resolve A2–B1 vs B2–C1 conflict)
- Lesson 02b — Galilean Confluence
- Lesson 07 — Your First Alpha (Claude-assisted)
- *Missing:* Lesson 05b — Media Kit (linked, not written)
- CropCircles (new — needs a level tag)

**AULA 103 — Advanced (B2–C1 → D2)**
- Lesson 01 — Vitruvian Approximation
- Voynich Manuscript — final project
- Bridge to `course-16weeks.html` ("English for Researchers, C1→D2") as an optional capstone track for students who want to move from ESL into academic publishing — could be surfaced as "AULA 104" or "Advanced Track" rather than folded into 103, since it's a different commitment (16 weeks, DOI publication) from a single 90–120 min lesson.

## 5. Concrete next steps (pick what you want done)

1. Fix the three broken homepage links — either write Lesson 05 / 05b, or unlink them until they exist, and either build or unlink `AULA/portal.html`.
2. Add Lesson02b, 03, 03b to the homepage lesson grid (they're built, just invisible).
3. Resolve the Lesson02 level conflict (A2–B1 vs B2–C1) — pick one canonical version.
4. Decide what to do with the duplicate/orphaned files outside AULA (delete, redirect, or leave as historical archive).
5. Once the above is settled, I can build the 101/102/103 landing structure into `index.html` and/or as three separate hub pages.
6. Pull the confirmed-canonical AULA files into your local folder so future edits happen locally and sync back to GitHub, rather than editing on the live repo each time.

Nothing above has been executed — this is the map. Tell me which numbered items to act on and I'll start there.
