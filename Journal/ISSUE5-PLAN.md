# Imaginary Origin — Issue No. 5 Plan

Audit + editorial plan. Written 12 August 2026.

---

## Fixed already

The footer bug you found was in **all three files**, not just vol3:

| File | Was | Now |
|---|---|---|
| `index.html` (No. 2) | "Vol. Ω No. 1 has not been published yet — this is the inaugural issue" | line removed, replaced with issue nav |
| `vol3.html` | footer said **No. 2**, plus the inaugural line | corrected to **No. 3**, nav added |
| `vol4.html` | footer said **No. 2**, plus the inaugural line | corrected to **No. 4**, nav added |

The colophon had been copy-pasted forward without updating the issue number, so No. 3 and No. 4 were both publicly identifying themselves as No. 2 while carrying a DOI and a false "inaugural issue" note.

---

## ⚠️ Two things to check before we plan No. 5

### 1. There are three issues in the folder, not four

`Journal/` contains `index.html` (No. 2), `vol3.html`, `vol4.html`. **There is no No. 1 file anywhere in the AXLE repo.** So either No. 1 exists somewhere I haven't found, or the numbering starts at 2 and the old footer was describing that. Worth resolving — an issue sequence that begins at No. 2 with no explanation invites the question from exactly the audience you're about to court.

Also note **No. 4 is dated Saturday, August 15, 2026** — three days from now. It's the upcoming issue, not a past one. Cadence is weekly, Saturdays. **No. 5 = Saturday, August 22, 2026.**

### 2. Pages are being recycled verbatim

Content hashes across the three issues:

| Page | No. 2 | No. 3 | No. 4 |
|---|---|---|---|
| 1 — Front | unique | unique | unique |
| 2 — Ledger / Almanac | `e45f93ce` | **`e45f93ce` same** | unique |
| 3 — Catalysis / Gallery | unique | unique | unique |
| **4 — Reading Room** | `fd671e45` | **identical** | **identical** |
| **5 — Natal** | `0d4070c3` | **identical** | **identical** |
| 6 — Wanted | unique | unique | unique |

**Pages 4 and 5 are byte-identical in every issue published.** No. 3 additionally repeats No. 2's entire Ledger page — so No. 3 is three recycled pages out of six.

This matters more than usual now. A casual reader never opens two issues. **A PI you're asking for a job will open all of them.** Repetition reads as thin output, which is the opposite of the impression the journal exists to create. Fix this before No. 5 goes to a professional audience.

---

## What's actually in the four issues

**No. 2 — Aug 1** · *Outside Verification: A Kernel Check on a Field-Defining Disproof*
Independent Lean 4 recompilation of Alpöge & Fable's Jacobian Conjecture disproof — 3,003 of 3,003 jobs passing, zero open `sorry`. Then: erratum (Vol. I → V6) and a self-reported correction; cashew-to-SAF catalysis bet; Reading Room; Natal conferences; Wanted.

**No. 3 — Aug 8** · *The Desk Audits Its Own House*
New front page. Pages 2–6 largely carried over from No. 2.

**No. 4 — Aug 15** · *A Newsletter Opens — and Chladni Plates Go to the Classroom*
New: The Almanac (a clock made of the moon; lunar analemma; the 18.6-year breath) and The Gallery (Primo Levi joins the scientist gallery). Pages 4–6 recycled.

**Recurring furniture:** Reading Room (*Bitter Cargo*, *Three Domains One Operator*), Natal (two conferences, seven sessions), Wanted (bilingual workshops, collaborators).

**DOI note:** every issue cites `10.5281/zenodo.19117399` — the series *concept* DOI. Per your own project rules, that's the generic-citation habit to avoid. If each issue has its own deposit, cite it; if not, the journal arguably needs one.

---

## Issue No. 5 — targeting FAPESP PIs

**Date: Saturday, August 22, 2026.**

### The strategic inversion

Page 6 is currently *"Wanted: Learners and Researchers"* — you recruiting others. For a PI audience that's backwards. **No. 5 should make you the pair of hands.**

And you have the single best possible credential for that audience, already published in No. 2: an independent Lean 4 kernel recompilation of a field-defining disproof, 3,003/3,003, zero `sorry`. That is *checkable* competence — a PI can run the file. It is worth more than any CV claim.

Recall what C4AI's PI said publicly: *"the biggest difficulty we've had all these years has been the lack of properly trained personnel on the academic market."* No. 5 is your answer to that sentence, addressed to the people who said it.

### Proposed six pages

**Page 1 — Front.** Lead with verification capability, not biography. Something like *"What an Independent Kernel Check Actually Proves"* — using the Jacobian recompilation to argue that formal verification is an underused instrument in applied AI research. Ends by noting the desk is available for exactly this work.

**Page 2 — New technical result.** Must be genuinely new. Candidates from your queue: the DNLS continuation analysis you flagged as "queued" in the No. 2 correction, or a Lean port of the three V6 results currently proved only at prose level. Either closes a loop you've publicly committed to — which is itself the argument for your reliability.

**Page 3 — 🇧🇷 The Brazilian AI landscape.** The ten FAPESP Applied Research Centers: 95 PIs, 739 researchers, BRL 1M/year each for ten years, matched privately. Report it as journalism, name the centers and PIs. This does two jobs at once: it's genuinely good content, and it puts their names in your pages before you write to them.

**Page 4 — Reading Room, REFRESHED.** New books. This page has run unchanged three times.

**Page 5 — Natal, REFRESHED or RETIRED.** If the conferences have happened by Aug 22, replace with a report from them. A forward-looking listing that's gone stale is worse than no page.

**Page 6 — "Available: Hands."** The inversion. What you can do, what you've verified, what you're looking for, in plain terms. Include the Lean artifacts, the ORCID, the DOIs, and a direct line to g6llc@proton.me.

### Two hard requirements

1. **Portuguese.** The journal is entirely in English; the PIs are Brazilian. At minimum page 3 and page 6 should be bilingual, or run a full PT edition. This is not decoration — it signals you intend to work *there*, not to be recruited *from* there.

2. **Kill the recycling.** If pages 4 and 5 can't be genuinely refreshed for No. 5, cut the issue to four strong pages. Four new pages beat six with two repeats, especially for a reader who'll open every issue.

### Timing

No. 5 lands **Aug 22**. The FAPESP openings I found close Aug 14–31. So No. 5 arrives after the earliest deadlines but during the later ones, and well before the next wave — the board turns over constantly. Send it as a follow-up to any application, and as the opening move to PIs you approach cold.

---

## Next

I can draft No. 5 in full — it inherits the existing template, so it's a matter of writing six pages into the same structure. Say which of these first:

- Resolve the No. 1 question, so the numbering is defensible
- Draft page 3 (the FAPESP centers report) — I already have the data
- Draft page 6 ("Available: Hands") — the page that does the actual work
- Refresh pages 4 and 5 so the recycling stops
