/-!
# Dm3Arithmetic.lean  (rewrite, 2026-07-03)
## The dm³ Operator: Explicit Toy Model (V3) — Three Arithmetic Corrections

**Why this file was rewritten.** The previous version of this file did not
formalize the three corrections it claimed to. Its `flow` was a plain
exponential decay `x·exp(-r*·t)`; its stationary density was a textbook
`N(0, σ²)` Gaussian centered at 0. Neither matches the actual dm³ toy model:

  · the real flow is the **Bernoulli solution** of `ṙ = r − r³`, and
  · the real stationary density is a Gaussian **centered at r = 1** with a
    coefficient of 2, coming from the drift `F ≈ −2(r − 1)`.

This rewrite states the correct objects. Facts that are checkable by
`ring`/`norm_num`/`positivity` are proved; the genuinely hard obligations
(the ODE-satisfaction derivative computation, the normalising integral, the
Fokker–Planck stationarity) are left as **clearly labelled `sorry`s** with a
correct proof route — following the honest pattern of FiniteBranching.lean,
NOT fabricating a proof that has not been machine-checked.

**Not machine-checked.** These files have not been compiled against Mathlib
in this session. Line references to Mathlib lemmas are best-effort and must be
verified by `lake build` before being trusted.

  Fix 1 — Flow formula:
    old:  φ_t(r) = r · exp(−r*·t)                         (simple decay — wrong)
    new:  r(t)   = [1 + (r₀⁻² − 1)·exp(−2t)]^(−1/2)        (Bernoulli sol. of ṙ = r − r³)

  Fix 2 — Hopf bifurcation coefficient factor of 2:
    old:  μ = exp(z₀)
    new:  μ = 2·exp(z₀)
    (The value is corrected here; the *justification* lives in ContactHopf.lean,
     which no longer claims a spurious "Reeb projection" mechanism.)

  Fix 3 — Stationary density:
    old:  ρ(x) ∝ exp(−x² / σ²)          centered at 0, coefficient 1  (wrong)
    new:  ρ(x) ∝ exp(−2(x − 1)² / σ²)   centered at 1, coefficient 2  (from drift −2(r−1))

Note on the coefficient. The drift of the *radial variable* is F'(1) = −2:
f(r) = r − r³ has f'(1) = 1 − 3 = −2, so F ≈ −2(r − 1). The value −4 is the
decay rate of the Lyapunov function V = (r−1)² (V̇ = 2(r−1)·(−2(r−1)) = −4V),
which is twice the drift rate and must not be used as the drift in the density.
(Corrected 2026-07-03: an earlier draft used −4 here.)

r_star value: 0.77594059 (certified; see RStarCertification.lean).
-/

import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.MeasureTheory.Measure.MeasureSpace
import Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral

namespace Dm3

open Real MeasureTheory

/-! ## Parameters -/

/-- The contraction ratio r* (certified value; see RStarCertification.lean). -/
noncomputable def r_star : ℝ := 0.77594059

/-- The bifurcation base point z₀ = log r*. -/
noncomputable def z₀ : ℝ := Real.log r_star

lemma r_star_pos : 0 < r_star := by norm_num [r_star]
lemma r_star_lt_one : r_star < 1 := by norm_num [r_star]

lemma r_star_mem_Ioo : r_star ∈ Set.Ioo (0 : ℝ) 1 := ⟨r_star_pos, r_star_lt_one⟩

lemma z₀_neg : z₀ < 0 := by
  unfold z₀; exact Real.log_neg r_star_pos r_star_lt_one

/-! ## Fix 1: Flow Formula — the Bernoulli solution of ṙ = r − r³

The dm³ radial dynamics near the generative transition are `ṙ = r − r³ = r(1 − r²)`,
a logistic-type (Bernoulli) equation with attracting fixed point at r = 1.
Substituting `u = r⁻²` linearises it to `u̇ = −2(u − 1)`, whose solution
`u(t) = 1 + (r₀⁻² − 1)·e^(−2t)` gives

    r(t) = [1 + (r₀⁻² − 1)·e^(−2t)]^(−1/2).

The old `x·exp(−t)` / `x·exp(−r*·t)` is the solution of the *linearised*
equation `ṙ = −r`, a different (and incorrect) model of the flow. -/

section FlowFormula

/-- **OLD flow (deprecated, incorrect).** Simple exponential decay. Retained
    only to state the correction; do not use. -/
@[deprecated (since := "2026-07-03")]
noncomputable def flow_old (r₀ t : ℝ) : ℝ := r₀ * Real.exp (-(r_star * t))

/-- **Corrected dm³ flow: the Bernoulli solution of `ṙ = r − r³`.**

    `r(t) = [1 + (r₀⁻² − 1)·e^(−2t)]^(−1/2)`

    with `r(0) = r₀` and `r(t) → 1` as `t → ∞`. -/
noncomputable def flow (r₀ t : ℝ) : ℝ :=
  (1 + (r₀ ^ (-2 : ℤ) - 1) * Real.exp (-(2 * t))) ^ (-(1 : ℝ) / 2)

/-- The auxiliary linearising variable `u(t) = r(t)⁻² = 1 + (r₀⁻² − 1)e^(−2t)`,
    which satisfies the *linear* ODE `u̇ = −2(u − 1)`. This is the honest
    engine behind the Bernoulli solution. -/
noncomputable def flowAux (r₀ t : ℝ) : ℝ := 1 + (r₀ ^ (-2 : ℤ) - 1) * Real.exp (-(2 * t))

/-- **Initial condition** `flow r₀ 0 = r₀` (checkable), assuming `r₀ > 0`. -/
theorem flow_zero (r₀ : ℝ) (hr₀ : 0 < r₀) : flow r₀ 0 = r₀ := by
  unfold flow
  have hexp : Real.exp (-(2 * (0 : ℝ))) = 1 := by simp
  rw [hexp]
  have hbase : (1 : ℝ) + (r₀ ^ (-2 : ℤ) - 1) * 1 = r₀ ^ (-2 : ℤ) := by ring
  rw [hbase]
  sorry
  -- Goal after `rw [hbase]`:  (r₀ ^ (-2 : ℤ)) ^ (−1/2 : ℝ) = r₀.
  -- Route: rewrite the ℤ-power as an rpow via `Real.rpow_intCast r₀ (-2)`,
  -- then `Real.rpow_natCast`/`Real.rpow_mul (le_of_lt hr₀)` with the exponent
  -- product (−2)·(−1/2) = 1 and `Real.rpow_one`. Elementary; left as sorry
  -- only because exact Mathlib coercion lemma names must be confirmed by build.

/-- The linearising variable satisfies its linear ODE `u̇ = −2(u − 1)`. -/
theorem flowAux_ode (r₀ t : ℝ) :
    HasDerivAt (flowAux r₀) (-(2 * (flowAux r₀ t - 1))) t := by
  unfold flowAux
  have h : HasDerivAt (fun t => 1 + (r₀ ^ (-2 : ℤ) - 1) * Real.exp (-(2 * t)))
      ((r₀ ^ (-2 : ℤ) - 1) * (Real.exp (-(2 * t)) * (-2))) t := by
    apply HasDerivAt.const_add
    apply HasDerivAt.const_mul
    apply HasDerivAt.exp
    have : HasDerivAt (fun t => -(2 * t)) (-2 : ℝ) t := by
      simpa using ((hasDerivAt_id t).const_mul (2 : ℝ)).neg
    simpa using this
  convert h using 1
  ring

/-- **ODE-satisfaction of the corrected flow: `ṙ = r − r³`.**

    This is the mathematical heart of Fix 1: the corrected `flow` solves the
    dm³ radial equation, whereas the old exponential did not. -/
theorem flow_ode (r₀ t : ℝ) (hpos : 0 < flowAux r₀ t) :
    HasDerivAt (flow r₀) (flow r₀ t - (flow r₀ t) ^ 3) t := by
  sorry
  -- Route (verified by hand this session; not yet machine-checked):
  --   flow r₀ = (flowAux r₀) ^ (−1/2).
  --   d/dt (u^(−1/2)) = (−1/2)·u^(−3/2)·u̇       [Real.rpow, HasDerivAt.rpow]
  --                   = (−1/2)·u^(−3/2)·(−2(u−1)) [flowAux_ode]
  --                   = u^(−3/2)·(u − 1)
  --                   = u^(−1/2) − u^(−3/2)
  --                   = r − r³.
  -- Needs `HasDerivAt.rpow_const` with `hpos`, then `flowAux_ode`, then `ring`
  -- on the rpow exponents (−1/2, −3/2). Left as sorry pending `lake build`.

/-- The fixed point of the corrected flow is r = 1 (not 0): `ṙ = 0 ↔ r ∈ {0, ±1}`,
    and r = 1 is the attractor. Checkable statement of the equilibrium. -/
theorem flow_equilibrium_at_one : (1 : ℝ) - (1 : ℝ) ^ 3 = 0 := by ring

end FlowFormula

/-! ## Fix 2: Hopf Bifurcation Factor of 2 -/

section HopfFactor

/-- **OLD Hopf coefficient (deprecated, incorrect).** -/
@[deprecated (since := "2026-07-03")]
noncomputable def μ_hopf_old : ℝ := Real.exp z₀

/-- **Corrected Hopf coefficient** `μ = 2·exp(z₀) = 2·r*`.
    The correction to the *value* is recorded here; the corrected *derivation*
    (a linearization step, not a geometric projection) is in ContactHopf.lean. -/
noncomputable def μ_hopf : ℝ := 2 * Real.exp z₀

theorem μ_hopf_eq_two_rStar : μ_hopf = 2 * r_star := by
  unfold μ_hopf z₀; rw [Real.exp_log r_star_pos]

theorem μ_hopf_eq_two_old : μ_hopf = 2 * μ_hopf_old := by
  simp [μ_hopf, μ_hopf_old]

theorem μ_hopf_pos : 0 < μ_hopf := by unfold μ_hopf; positivity

/-- Numerical sanity check: μ ≈ 1.5519. -/
theorem μ_hopf_approx : 1.55 < μ_hopf ∧ μ_hopf < 1.56 := by
  have h : μ_hopf = 2 * r_star := μ_hopf_eq_two_rStar
  rw [h]; constructor <;> norm_num [r_star]

end HopfFactor

/-! ## Fix 3: Stationary Density — centered at r = 1, coefficient 2

The dm³ stationary density is the invariant measure of
`dX_t = F(X_t) dt + σ dW_t` with drift `F(r) ≈ −2(r − 1)` near the attractor
`r = 1`. The Ornstein–Uhlenbeck stationary law is Gaussian with

    mean = 1,   variance = σ² / (2·2) = σ² / 4,

so the density is `ρ(x) ∝ exp(−2(x − 1)² / σ²)`. The old file used
`exp(−x²/σ²)`: **wrong center (0 vs 1), wrong coefficient (1 vs 2), wrong drift.** -/

section StationaryDensity

variable (σ : ℝ)

/-- **OLD density (deprecated, incorrect).** Centered at 0, coefficient 1. -/
@[deprecated (since := "2026-07-03")]
noncomputable def ρ_old (C x : ℝ) : ℝ := C * Real.exp (-(x ^ 2 / σ ^ 2))

/-- **Corrected stationary density.**

    `ρ(x) = (√2 / (σ·√π)) · exp(−2(x − 1)² / σ²)`

    Gaussian with mean 1 and variance σ²/4; normalising constant
    `√2/(σ√π) = 1 / ∫ exp(−2(x−1)²/σ²) dx`. -/
noncomputable def ρ (x : ℝ) : ℝ :=
  (Real.sqrt 2 / (σ * Real.sqrt Real.pi)) * Real.exp (-(2 * (x - 1) ^ 2 / σ ^ 2))

/-- The density is peaked at the attractor r = 1: the exponent vanishes there. -/
theorem ρ_peak_at_one : (2 * ((1 : ℝ) - 1) ^ 2 / σ ^ 2) = 0 := by ring

/-- ρ is non-negative everywhere (checkable), for σ > 0. -/
theorem ρ_nonneg (hσ : 0 < σ) (x : ℝ) : 0 ≤ ρ σ x := by
  unfold ρ
  apply mul_nonneg
  · apply div_nonneg (Real.sqrt_nonneg 2)
    exact mul_nonneg (le_of_lt hσ) (Real.sqrt_nonneg _)
  · exact le_of_lt (Real.exp_pos _)

/-- **Normalisation** `∫ ρ = 1` (Gaussian integral). -/
theorem ρ_normalised (hσ : 0 < σ) : ∫ x : ℝ, ρ σ x = 1 := by
  sorry
  -- Route: substitute y = √2(x−1)/σ so ∫ exp(−2(x−1)²/σ²) dx = (σ/√2)·∫ exp(−y²) dy
  --        = (σ/√2)·√π   [Mathlib `integral_gaussian` / `Real.integral_exp_neg_sq`].
  -- Multiply by prefactor √2/(σ√π) ⇒ 1. Left as sorry pending exact lemma name.

/-- **Fokker–Planck stationarity** of ρ for the dm³ OU model
    `dX = −2(X−1)dt + σ dW`. Expected to stay open until Mathlib has SDE
    machinery; recorded honestly rather than asserted. -/
theorem ρ_is_stationary_of_dm3_flow : True := by trivial
  -- No content claimed. When Mathlib gains Fokker–Planck support, replace
  -- `True` with the statement that ρ is the stationary density of the OU
  -- generator L*ρ = 0 for drift −2(x−1), diffusion σ²/2.

end StationaryDensity

/-! ## Sorry ledger (honest status)

| # | Obligation                    | Status        | Route                                   |
|---|-------------------------------|---------------|-----------------------------------------|
| 1 | `flow_zero` rpow identity     | sorry (easy)  | `Real.rpow_mul`, coercion lemma names   |
| 2 | `flow_ode` (ṙ = r − r³)       | sorry (core)  | `HasDerivAt.rpow_const` + `flowAux_ode` |
| 3 | `ρ_normalised`                | sorry         | Gaussian integral, u-substitution       |
| 4 | `ρ_is_stationary_of_dm3_flow` | open (no SDE) | future Mathlib Fokker–Planck            |

Proved without sorry: `r_star_*`, `z₀_neg`, `flowAux_ode`, `flow_equilibrium_at_one`,
`μ_hopf_*`, `ρ_peak_at_one`, `ρ_nonneg`. -/

end Dm3
