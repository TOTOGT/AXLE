# Series impact — stationary-density coefficient 4 → 2 (and the session's other fixes)

**Date:** 2026-07-03 · **Trigger:** correction of the dm³ stationary-density
coefficient from **4** to **2** in `Dm3Arithmetic.lean`.

This is a "where to look" map grounded in the deposit registry descriptions,
**not** a verified diff of each paper's internals. Items marked *check* mean the
dependency is plausible from the description but the actual paper text was not
read line-by-line.

---

## 1. What the fix actually is

The dm³ radial law is `f(r) = r − r³`, attractor at `r = 1`.

- **Drift at the attractor:** `f'(1) = 1 − 3·1² = −2`. So near `r=1`,
  `ṙ ≈ −2(r−1)`. This is the linear relaxation rate / Lyapunov exponent
  `μ_max = −2`.
- **Lyapunov-function rate:** for `V = (r−1)²`, `V̇ = 2(r−1)ṙ ≈ −4(r−1)² = −4V`.
  The `−4` is the decay rate of `V`, i.e. **2 × the drift**. It is *not* the drift.

For the OU stabilisation `dX = −a(X−1)dt + σ dW`, the stationary law is
`N(1, σ²/(2a))` with density `∝ exp(−a(x−1)²/σ²)`. **The density-exponent
coefficient equals the drift rate `a`.** Correct value: `a = 2`, giving

  ρ(x) ∝ exp(−2(x−1)²/σ²),  variance σ²/4,  norm √2/(σ√π).

The earlier `a = 4` used the Lyapunov rate in place of the drift.

**Independent cross-check (strong).** V6's Lean-verified canonical triple is
`(T*, μ_max, τ) = (2π, −2, 2)` with noise tolerance `τ·ε₀ = 2/3`. The eigenvalue
there is `−2`, so the density coefficient *must* be `2`. The fix is consistent
with an already-machine-checked constant; the `4` was the outlier.

---

## 2. The one quantitative consequence that propagates

Coefficient `4 → 2` **doubles the stationary variance** (σ²/8 → σ²/4) and widens
the stabilised-state distribution by **√2 ≈ 1.414** in standard deviation.

So any downstream claim of the form "width / spread / noise-tolerance / fitted
Gaussian σ of the stabilised state" changes by a factor of √2 (in σ) or 2 (in
variance). Everything else in the session's corrections is either a value
transcription (r*, γ*) or a functional-form fix (Bernoulli flow, Invariant 7.5)
that does not touch this width.

---

## 3. Propagation map across the corpus

| # | Deposit | Depends on | What changes | Severity |
|---|---|---|---|---|
| 3 | dm³ Toy Model (source paper) | density, drift, flow | Density coeff 2; flow already Bernoulli; **source of the fix** | **High — fix at source** |
| 26 | Autophagy & Triple-Alpha (Book 3, Ch A) / `AutophagyDm3.lean` | stationary density, basin width, μ_max | If it quotes stabilised-state spread → ×√2 width. μ_max=−2 unchanged. Shared dependency → propagates to #32 and others | **High — check** |
| 32 | Biological Transitions Multi-Agent (V2) | `AutophagyDm3.lean` | Inherits #26 outcome | Med — check |
| 11 | Neurological Recovery (NSCISC/TBIMS/TRACK-TBI) | dm³ sigmoid fit to recovery stats | If a Gaussian spread / relaxation width was fit, refit with σ²/4. Relaxation *rate* (−2) unchanged | **Med–High — check (empirical fit)** |
| 9 | Immune System as Maintenance Engine | dm³ relaxation near attractor | Same: width ×√2 if quoted; rate unchanged | Med — check |
| 6 | Time as an Operator (circadian/DST) | cites r*, ε₀ as established | ε₀=1/3 unchanged; r* → 0.77594059 if it quoted 0.773/0.80; density width if used | Low–Med — check |
| 7 | Gravitational Lensing (sub-halo) | dm³ constants in χ²/n fit | Only if the fit used the stationary width/coefficient; else unaffected | Low — check |
| 2 | Vol II — Contact Realization | γ*, Invariant 7.5 citation | γ* = 2e^{z₀}; Thm 3.4 now cites Invariant 7.5 *unconditional folding part* only | **High — already handled this session** |
| 4/27 | GCM (two deposits) | flow form | Bernoulli flow ṙ=r−r³; reconcile which GCM DOI Vol II ref [2] points to | Med — handled + reconcile |
| 24 | GTCT Ring 5 (V3) | r* ≈ 0.773 (earlier) | Update to certified 0.77594059 | Low — value transcription |
| 1 | Vol I (V6) | assumptions, 5.1/5.4/7.5 | Already updated (V6 + this session's HTML/Lean) | Done |

---

## 4. What does NOT change (guard against overclaiming)

- **μ_max = −2, ε₀ = 1/3, τ = 2, τ·ε₀ = 2/3** — Lean-verified, unaffected. The
  drift/eigenvalue was always −2; only the density coefficient was mis-set to 4.
- **r\* = 0.77594059** — a value-precision item, independent of the 4→2 fix.
  Papers quoting 0.773 or 0.80 are drift/imprecision, not consequences of this fix.
- **γ\* = 2e^{z₀}** — the Hopf reconciliation; independent of the density.
- **Invariant 7.5 / condition (D) / Gerono** — a functional-form + necessity
  result; does not touch the density width.
- **Bernoulli flow ṙ = r − r³** — a functional-form fix; the attractor and rate
  are unchanged, so it does not by itself move any width.
- Non-dm³ deposits (DNLS n-bonacci #38/#39, Law of Monsters #19, Lexical
  Generativity #25, Collatz-geometry #23) — no dependency on the density.

---

## 4b. Repo scan — ground truth (added after connecting `~/geometry`)

A line-by-line grep of the actual site repo changes the picture from the
registry-only estimate above:

- **The coefficient-4 density error did NOT propagate into the series.** Every
  hit for `exp(-4…)`, `4(r-1)`, `variance/8`, etc. is a false positive:
  `ch16-scale.html` (RG scale invariance), `ch2.html` (SVD singular-value
  variance), `ALGEBRAIC_PROOFS_ALL_7_THEOREMS.md` (DRIFTS spectroscopy),
  `prelude.html` (nav card for the scale-invariance chapter). **No repo page
  states the dm³ stationary density with coefficient 4.** The error was confined
  to the draft Lean file, now fixed. Nothing downstream to correct for it.

- **The real propagation surface is r\* precision drift**, in a specific set of
  files:
  - `vol2-toymodel.html:429` — `r* ≈ 0.773` (argued)
  - `hub.html:620` — `r*≈0.773`
  - `dm3-lab-index.html` (lines 172, 229, 241, 305) — `r* ≈ 0.80`, contrasted
    with the symmetric bound `r = 2/3` and `µ → −2`, `ε₀ = 1/3`
  - plus further hits across `book4/`, `HVEH/`, `book7/`, course pages.
  Certified value is **0.77594059 ≈ 0.776**; both `0.773` (superseded GTCT Ring 5
  value) and `0.80` (rounded-up) are drift. **Caution:** several of these are
  pedagogically framed (e.g. dm3-lab-index presents `≈0.80` as a numerical
  observation vs the `2/3` symmetric prediction, as an open exercise) — those
  need per-file judgment, not a blind find-replace, and the distinct constants
  `2/3` (symmetric bound), `1/3` (Gronwall ε₀), and `4/5` (rational bound in the
  Lean inequality `1/3 < 4/5`) must NOT be collapsed into r*.

- **`vol1-mathematics.html` is still the pre-V6 page** in the repo (Second
  Edition, DOI `19117400`, `1/3 < 4/5 ≈ r*`). The V6 refresh exists only in the
  output file `principia_vol1_v6.html` and has not yet been applied to the repo.

## 4c. Blockers / sequencing

- **Rebase must be done by the user.** `.git` is read-only in the sandbox
  (`Operation not permitted` on `.git/objects` and `index.lock`); the tree is
  behind `origin/main`. Editing before rebasing risks conflicts. Order:
  `git fetch origin` → `git rebase origin/main` (or `git pull --rebase origin
  main`); `git stash` first if there are uncommitted local edits, `git stash pop`
  after.

## 5. Net recommendation

1. **One substantive numeric propagation:** the stabilised-state width is √2
   larger everywhere it is quoted. Priority targets: the dm³ toy paper (#3, done),
   `AutophagyDm3.lean` (#26, shared dependency → highest leverage), and any
   empirical-fit paper (#11 neurological recovery, #9 immune, #7 lensing).
2. **Housekeeping, not consequences of this fix:** r* precision (#24, #6),
   GCM DOI reconciliation (#4/#27), γ* and Invariant 7.5 (Vol II, already done).
3. Because `AutophagyDm3.lean` is imported by several deposits, fix and re-`lake
   build` it first — a corrected width there propagates automatically to its
   dependents, and it is the single highest-leverage file to touch next.
