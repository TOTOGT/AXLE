# Open Questions — Principia Orthogona, Volume I

Status as of Version 3, May 2026.
Tracked in AXLE issue tracker: https://github.com/TOTOGT/AXLE

| ID | Description | Status | Lean file | Closure path |
|----|-------------|--------|-----------|--------------|
| O1 | **AXLE Issue #12** — Lipschitz continuity of K; eigenvalue API gap in `separation_theorem` (diagonal sum bound pending Mathlib eigenvalue API for real symmetric matrices) | **Open** — partial: bound structure and exp(−12) < 1/32 proved; 1 scoped sorry | `PrincipiaVol1.lean` §9 | `Mathlib.LinearAlgebra.Matrix.Spectrum` + `Finset.sum` bound |
| O2a | **AXLE Issue #14 Ob.2** — Whitney fold from mTORC1 kinase data: `whitneyFold_conditional` sorry guards Mather's C∞-stability theorem. Algebraic content (`V_factored`, `V_is_morse_at_one`) proved. Antecedent requires constitutive biology data. | **Strengthened** — proper conditional Prop replaces True stub; sorry guards Mather only | `AutophagyDm3_v2.lean` | Mather stability once in Mathlib; biology data gap is domain-side |
| O2b | **AXLE Issue #14 Ob.3** — Limit cycle existence via Poincaré–Bendixson. Compactness content proved (`dm3_basin_compact`, `dm3_basin_nonempty`). Sorry guards only the PB step. | **Partially closed** — topological content (compactness, non-empty ω-limit set) proved; dynamical content (PB conclusion) sorry | `AutophagyDm3_v2.lean` | `Mathlib.Dynamics.OmegaLimit` + Poincaré–Bendixson infrastructure |
| O3 | **AXLE Issue #15 / Theorem T1** — Global monotonicity of z(t) in Gronwall basin. `gronwall_contraction_below_stability_radius` proves the decay exponent sign only. Full ODE integration (‖δxₜ‖ ≤ ‖δx₀‖·exp((μmax+3ε)·t)) pending. | **Partially closed** — exponent sign proved (0 sorry); ODE application open | `PrincipiaVol1.lean` §8 | Define dm³ semiflow formally; invoke `Mathlib.Analysis.ODE.Gronwall` |
| O4 | **Sorry 1** — Discrete dm³ extension to ℤ. Requires DynamicalSystem typeclass for discrete maps. Collatz connection in `discreteDm3.lean` provides structural motivation. | **Open** | `discreteDm3.lean` (AXLE root) | Define `DynSys` typeclass; prove embedding ℕ → PhaseVector and intertwining lemma |
| O5 | **Conjecture 15.1** — Perelman functor 𝒫 : dm³ → RicciFlow. Term-by-term structural correspondence argued in §15 (Table 1). Construction of 𝒫 and functor law verification open. | **Open** — argued, not proved; explicitly stated as conjecture | None (proof sketch in paper §15) | `CategoryTheory.Functor` applied to both categories once RicciFlow is in Mathlib |
| O6 | **Conjecture 16.1** — Dimensional threshold N=3. Identified as minimum dimension for non-trivial contact geometry, connecting to c=3 in Collatz. | **Open** — argued via club filter infrastructure in §16; explicitly stated as conjecture | `PrincipiaVol1.lean` §10 (infrastructure proved) | Full Collatz proof (equivalent to O4 + Collatz conjecture itself) |

## Notes on sorry count

The deposit contains **1 sorry** total, in `PrincipiaVol1.lean`:
- `separation_theorem`: the `h_transverse` sub-goal (O1). The surrounding bound
  structure is proved. This sorry is clearly scoped and labelled.

All other 30+ theorems in `PrincipiaVol1.lean` are proved without sorry.
`AutophagyDm3_v2.lean` contains 2 additional sorry instances (O2a, O2b),
both strengthened from True stubs to proper conditional propositions.

## Comparison with previous version

| Obligation | V1/V2 status | V3 status |
|------------|-------------|-----------|
| O1 (separation_theorem) | Not in deposit | 1 scoped sorry, bound structure proved |
| O2a (Mather) | True stub | Proper conditional; sorry guards Mather only |
| O2b (PB) | True stub | Split: compactness proved; PB sorry |
| O3 (Gronwall T1) | Not in deposit | Exponent sign proved (0 sorry) |
| O4 (discrete dm³) | Not in deposit | Documented stub |
| O5 (Perelman functor) | Stated as conjecture | Stated as conjecture |
| O6 (threshold) | Stated as conjecture | Club filter infrastructure proved |
