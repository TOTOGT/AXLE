# SESSION HANDOFF — 2026-07-30, tank at 90%

**Goal:** GTCT V4 correction → Book 6 WP-35/36/37 → AXLE-RAG toolkit → commits.

> Written before the tank ran out. Next session starts at **RESUME HERE**.

---

## ⚡ RESUME HERE — two commands

```bash
# 1. geometry: committed, needs push only
cd ~/geometry && git push          # commit 61e8289 already made

# 2. AXLE: files placed, stale lock blocked the commit
cd ~/AXLE
rm -f .git/index.lock              # stale; sandbox couldn't remove it
git status                         # confirm branch = aula/rag-course
git add AULA/rag-course/site/reference-implementation.html AULA/index.html \
        AULA/job-nyc.html research/dps research/axle-rag DPSEstimator.lean \
        .github/workflows/lean-verify.yml .github/workflows/corpus-audit.yml \
        .github/workflows/work-order.yml
git commit -F COMMIT_MSG_AXLE.txt  # message saved alongside this file
git push
```

---

## Decisions made (do not re-litigate)

- **Series DOI is 10.5281/zenodo.19117399**, not 19117400 — concept DOI, resolves to latest.
- **r\* = 0.77594059**, certified by bisection to 1e-7. Supersedes 0.7732 from V1–V3.
- **The dm³ coupling is e⁻ᶻ, not e⁻ʳ.** The e⁻ʳ system gives μ = −1.264 and boundary 0.641 — inconsistent with the paper's own claims. Erratum in §1.1.
- **κ is two different constants.** κ_chain ≤ √(5/9) ≈ 0.745 is derived (Vol IV recursion, Pythagorean from σ_min ≥ 2/3 and ‖u w ᵀ‖ ≤ 1/3). κ\* = √(7/9) ≈ 0.882 is an undrived dm³ marker. They cannot be equal since √(5/9) < r\*.
- **Saddle eigenvalues** are λ₊ = 1.4915, λ₋ = −0.2445, Δ = 3.0136. The web-posted 1.1097 / 4.534 were wrong. Closed forms B.1–B.5 verified numerically.
- **AXLE committed on `aula/rag-course`**, not main — course material belongs there and the tree had 10 untracked paths left untouched. Merge when ready.
- **WP-36's ask is acquisition guidance, not legislation** — avoids preemption entirely.
- **Did NOT rename anything to "SHIT"** — that was a joke, correctly not acted on.

## Blocked / needs you

- ⛔ **AXLE stale `.git/index.lock`** — only removable from your machine.
- ⛔ **`git push` on both repos** — sandbox has no GitHub credentials.
- ⛔ **`DPSEstimator.lean` is UNVERIFIED.** Never compiled; no toolchain here. Run `lake build` + `lean-verify.yml`. **No document may call it verified until that CI is green.**
- ⛔ **Zenodo uploads** are manual and irreversible after publish: GTCT_2026_v4.pdf → 21708678; FUG_base_case_v1.pdf → 21710763; FUG v1.1 under concept 21561818 with the canonical certify_rstar.py.
- ⛔ **MIT xPRO enrollment deadline was today** (30 Jul). If missed, ask Baldev to hold the rate — advisors usually can.

## Done this session

| Repo | State |
|---|---|
| geometry | **committed `61e8289`** — WP-35/36/37, book6/policy/ (EO draft, drafting memo, pilot scope, SITE_ERRATA), book4/ch10.html synced to V4. Push pending. |
| AXLE | **files placed, commit blocked by lock** — reference-implementation.html, AULA index + job-nyc, research/dps, research/axle-rag, DPSEstimator.lean, 3 workflows. |
| GTCT | **not mounted** — paper, figures, numerics still need `commit_session.sh --push`. |
| axle-monitor | **repo does not exist yet** — `gh repo create TOTOGT/axle-monitor --public --clone`, then see SETUP.md. |

## Still outstanding (SITE_ERRATA.md)

- book6/index.html + chIV-\*.html footers: DOI 19117400 → 19117399
- book4/index.html hub: r\*≈0.773 blurb; sorry-count strip
- book4/ch03.html: r\*≈0.8 → 0.77594 (4 places)
- GTCT repo root `Chain_updated.lean` is the stale 2026-04-18 draft (2 sorrys, `r_star := 0.8`) — replace with the AXLE registry copy before the V4 deposit ships
- GTCT repo About text still says "Version 2 / zenodo.20360288"

## Rules inherited

1. No claim moves to VERIFIED without a kernel check you watched pass.
2. Every claim keeps a tag; tags do not drift upward silently.
3. No document scores its own rigor.
4. A caveat is removed only by the edit that verifies the thing it hedges.
5. Minimal edits; update this brief in the same session.

---
*Generated 2026-07-30. Paste the RESUME HERE block as the first message of the next session.*
