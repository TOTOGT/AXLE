# Open Questions — Principia Orthogona, Volume I

Status as of **Version 7, 24 August 2026**.
Tracked in AXLE issue tracker: https://github.com/TOTOGT/AXLE
Deposit: https://doi.org/10.5281/zenodo.22084842 (V7)
Verifier: https://github.com/TOTOGT/vol1-proofs — `bash tools/run.sh`

## What V7 changed in this table

Before V7, `PrincipiaVol1.lean` had never been elaborated by Lean. Its first
real build reported **81 errors** (log: `v6-build-errors.txt`). Every "proved
— 0 sorry" line in the V3 table below was therefore an unverified claim about
a file that did not compile. The file compiles now, and every status here has
been re-derived from a kernel run rather than from the file's own comments.

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

## Sorry count

**0** in `PrincipiaVol1.lean`, verified by `#print axioms` over all 49
theorems. No `sorryAx`. No axiom beyond `propext`, `Classical.choice`,
`Quot.sound`.

The V3–V6 note in this position read: *"The deposit contains 1 sorry total …
All other 30+ theorems in `PrincipiaVol1.lean` are proved without sorry."*
Neither half of that had been checked. The file did not compile, so it had no
theorems at all in the kernel's view.

`AutophagyDm3_v2.lean` is reported to contain 2 sorry instances (O2a, O2b).
**That file has not been built either.** Until it is, treat the number as
unverified. The same applies to every "— 0 sorry" provenance line that used to
appear in the Lean file's section banners; those lines have been removed and
will be restored per file, as each one goes green.

## What is verified, precisely

| Section | Theorems | Content |
|---|---|---|
| §1 P1 | 5 | Whitney A₁ conditions on V(q) = q³−3q at q = 1 |
| §2 P2 | 2 | Contact non-degeneracy c(ρ) = −2ρ < 0 |
| §3 P3–P4 | 4 | Gronwall radius ε₀ = 1/3; basin asymmetry 1/3 < 4/5 |
| §4 P5 | 2 | Lyapunov exponents −V''(1)/2 = −3; μmax = −2 < 0 |
| §5 P6 | 3 | Stability functional Φ(ρ) = ρ², Φ′ > 0 |
| §7 | 1 | Noise tolerance τ·ε₀ = 2/3 |
| §8 | 1 | Gronwall contraction exponent sign |
| §9 | 9 | Separation theorem, V7 form (see O1) |
| §10 | 4 | Club filter, stationary sets, uncountable cofinality |
| §11 | 5 | Regeneration hierarchy, Mahlo-like levels |
| §12 | 3 | Crystal aspect ratio 66 = 33·τ |
| §14 | 9 | Theorem 5.3 non-commutativity, concrete ℤ instances |
| **total** | **49** | |

§14 was labelled "NOT MACHINE-CHECKED" in V6. It is now.

## Comparison across versions

| Obligation | V1/V2 | V3–V6 (claimed) | V7 (verified) |
|------------|-------|-----------------|---------------|
| The Lean file itself | not in deposit | "30+ facts, 1 sorry, 0 axioms" | **did not compile in V3–V6**; compiles now, 49 theorems, 0 sorry |
| O1 (separation) | not in deposit | 1 scoped sorry, "eigenvalue API gap" | statement was false; restated and proved; real gap is the spectral reduction |
| O2a (Mather) | True stub | proper conditional | unverified — host file never built |
| O2b (PB) | True stub | compactness proved | unverified — host file never built |
| O3 (Gronwall T1) | not in deposit | exponent sign proved | exponent sign **verified**; integration open |
| O4 (discrete dm³) | not in deposit | documented stub | unchanged |
| O5 (Perelman) | conjecture | conjecture | unchanged |
| O6 (threshold) | conjecture | infrastructure proved | infrastructure **verified** (4 theorems); conjecture open |
