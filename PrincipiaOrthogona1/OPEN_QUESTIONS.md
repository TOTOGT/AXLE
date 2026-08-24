# Open Questions — Principia Orthogona, Volume I

Status as of **Version 7, 24 August 2026**.
Tracked in AXLE issue tracker: https://github.com/TOTOGT/AXLE
Deposit: https://doi.org/10.5281/zenodo.22084842 (V7) · concept DOI 10.5281/zenodo.19117399
Verifier: https://github.com/TOTOGT/vol1-proofs — `bash tools/run.sh`

## What V7 changed in this table

Before V7, `PrincipiaVol1.lean` did not build against the Mathlib revision
this repository pins: 81 errors (log: `v6-build-errors.txt`). The error
profile is Mathlib drift — `Ordinal.sup` deprecated 2024-08-27,
`IsLimit.add_right` renamed 2024-10-11, `Set.finite_insert` a Mathlib-3
spelling — against code written when those names were current, plus later
hand-edits that were never rebuilt. Nothing re-ran the build, so it went
unnoticed. Every status below has now been re-derived from a kernel run
rather than from the file's own comments.

O1 in particular was mis-diagnosed. It was recorded as a Mathlib eigenvalue
API gap. It was not: the deposited statement of `separation_theorem` was
**false**, and the intended argument was about `M⁶`, not `M`. See the row
below and §9 of the Lean file.

| ID | Description | Status (V7) | Lean file | Closure path |
|----|-------------|-------------|-----------|--------------|
| O1 | **Re-diagnosed.** V3–V6 recorded this as "eigenvalue API gap in `separation_theorem`, 1 scoped sorry". Two corrections: (a) the deposited statement is *false* — `IsDm3Stable` bounds only the transverse diagonal, so at `n = 1` it is vacuous and `(33)` is a counterexample; (b) the intended bound is the **sixth** power (`\|Tr − 1\| ≤ 31·e⁻¹²`), as in Book 2 Thm 12.2 and both ancestor files; at the first power it is numerically false (`31·e⁻² ≈ 4.195`). What is actually open is the **spectral reduction** `Tr(M⁶) = Σ λᵢ⁶` for a general real `M`. | **Open, restated** — 0 sorry. V7 proves the theorem on the eigenvalue list and on a diagonal matrix, where the reduction is an identity. The refutation of the old statement is proved and kept (`v6_separation_statement_is_false`). | `PrincipiaVol1.lean` §9 | Diagonalisability over ℝ, or Jordan form over ℂ; `Mathlib.LinearAlgebra.Matrix.Spectrum` |
| O2a | **AXLE Issue #14 Ob.2** — Whitney fold from mTORC1 kinase data: `whitneyFold_conditional` sorry guards Mather's C∞-stability theorem. Antecedent requires constitutive biology data. | **Open** — the algebraic content (`V_factored`) is kernel-checked in `PrincipiaVol1.lean`; the conditional Prop lives in `AutophagyDm3_v2.lean`, **which has not been built**. Its status is claimed, not verified. | `AutophagyDm3_v2.lean` | Mather stability once in Mathlib; biology data gap is domain-side |
| O2b | **AXLE Issue #14 Ob.3** — Limit cycle existence via Poincaré–Bendixson. Compactness content claimed proved (`dm3_basin_compact`). | **Open** — same caveat: `AutophagyDm3_v2.lean` has not been built. | `AutophagyDm3_v2.lean` | `Mathlib.Dynamics.OmegaLimit` + Poincaré–Bendixson |
| O3 | **AXLE Issue #15 / Theorem T1** — Global monotonicity of z(t) in the Gronwall basin. Full ODE integration `‖δxₜ‖ ≤ ‖δx₀‖·exp((μmax+3ε)t)` pending. | **Partially closed, now verified** — `gronwall_contraction_below_stability_radius` is kernel-checked: it proves the *sign* of the decay exponent and nothing more. The ODE application is open. | `PrincipiaVol1.lean` §8 | Define the dm³ semiflow formally; invoke `Mathlib.Analysis.ODE.Gronwall` |
| O4 | **Discrete dm³ extension to ℤ.** Requires a DynamicalSystem typeclass for discrete maps. | **Open** | `discreteDm3.lean` (AXLE root, not built) | Define `DynSys`; prove the embedding ℕ → PhaseVector and the intertwining lemma |
| O5 | **Conjecture 15.1** — Perelman functor 𝒫 : dm³ → RicciFlow. | **Open** — argued in §15, explicitly a conjecture | none | `CategoryTheory.Functor`, once RicciFlow is in Mathlib |
| O6 | **Conjecture 16.1** — Dimensional threshold N = 3, connecting to c = 3 in Collatz. | **Open** — the club-filter infrastructure in §10 is now kernel-checked (4 theorems); the conjecture is not | `PrincipiaVol1.lean` §10 | Full Collatz proof (O4 + Collatz itself) |
| O7 | **NEW IN V7 — the ε₀ instantiation.** §22 states ε₀ = \|μmax\|/[2(1+sup‖Hess V‖)], sets sup‖Hess V‖ = \|L₂\| = 3, and computes 2/(2·3) = 1/3. The formula at H = 3 gives 1/4; the printed arithmetic and the Lean both use H = 2. | **Open** — `epsilon0_of_eq_third_iff` proves that under this formula ε₀ = 1/3 **iff** H = 2, so exactly one of the three lines is wrong. Not decided here. | `PrincipiaVol1.lean` §3 | Decide, in the paper, which Hessian bound enters the Gronwall estimate. Not a Lean question. |

## Sorry count

**0** in `PrincipiaVol1.lean`, verified by `#print axioms` over all 58
theorems. No `sorryAx`. No axiom beyond `propext`, `Classical.choice`,
`Quot.sound`.

The V3–V6 figure in this position was 1 sorry against 30+ theorems. It is
now 0 against 58, checked at a stated pin.

`AutophagyDm3_v2.lean` is reported to contain 2 sorry instances (O2a, O2b).
That file has no runner yet, so its count is carried rather than re-checked
here — the same caveat that applied to this file before V7, and the reason
each file gets a runner rather than a claim.

## What is verified, precisely

| Section | Theorems | Content |
|---|---|---|
| §1 P1 | 5 | Whitney A₁ conditions on V(q) = q³−3q at q = 1 |
| §2 P2 | 2 | Contact non-degeneracy c(ρ) = −2ρ < 0 |
| §3 P3–P4 | 8 | Gronwall radius ε₀ = 1/3, what forces it (O7), basin asymmetry |
| §4 P5 | 2 | μmax = −2 < 0; L₂ = −V''(1)/2 = −3 |
| §5 P6 | 3 | Stability functional Φ(ρ) = ρ², Φ′ > 0 |
| §7 | 1 | Noise tolerance τ·ε₀ = 2/3 |
| §8 | 1 | Gronwall contraction exponent sign |
| §9 | 13 | Separation theorem, V7 form (see O1) |
| §10 | 4 | Club filter, stationary sets, uncountable cofinality |
| §11 | 5 | Regeneration hierarchy, Mahlo-like levels |
| §12 | 2 | Crystal aspect ratio 66 = 33·τ |
| §14 | 12 | Theorem 5.3 instances, and two vacuity witnesses |
| **total** | **58** | |

Counts produced by `tools/counts.py`, not typed. An earlier draft of this
table summed to 48 while claiming 49.

§14 was labelled "NOT MACHINE-CHECKED" in V6. It is now.
§12 lost one: `g6_equals_schumann` was `33 = 33` by `rfl` and is withdrawn.

## Comparison across versions

| Obligation | V1/V2 | V3–V6 (claimed) | V7 (verified) |
|------------|-------|-----------------|---------------|
| The Lean file itself | not in deposit | "30+ facts, 1 sorry, 0 axioms" | drifted off the pinned Mathlib; rebuilt to the pin, 58 theorems, 0 sorry, with a runner |
| O1 (separation) | not in deposit | 1 scoped sorry, "eigenvalue API gap" | statement was false; restated and proved; real gap is the spectral reduction |
| O2a (Mather) | True stub | proper conditional | unverified — host file never built |
| O2b (PB) | True stub | compactness proved | unverified — host file never built |
| O3 (Gronwall T1) | not in deposit | exponent sign proved | exponent sign **verified**; integration open |
| O4 (discrete dm³) | not in deposit | documented stub | unchanged |
| O5 (Perelman) | conjecture | conjecture | unchanged |
| O6 (threshold) | conjecture | infrastructure proved | infrastructure **verified** (4 theorems); conjecture open |
