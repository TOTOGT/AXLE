/-
  The Forced Urgency Gap — Lean 4 formalization sketch.

  Kernel-checkable core of §4 (Amplification). The cumulative displacement of a
  unit urgency shock, when a fraction `ρ` of forced supply is harvested and
  re-forced each round, is the geometric sum of the cascade:

        A(ρ) = ∑ₖ ρᵏ = 1/(1-ρ),   for 0 ≤ ρ < 1.

  This file certifies: (1) the cascade actually sums to A(ρ); (2) A(ρ) ≥ 1;
  (3) A(ρ) = 1 iff ρ = 0; (4) A is strictly increasing in ρ; (5) A is unbounded
  as ρ → 1⁻; (6) a policy corollary — anything that strictly lowers ρ strictly
  lowers cumulative displacement.

  DESIGN RULE (inherited from the TOTOGT/io corpus, non-negotiable):
  only NON-VACUOUS, kernel-certifiable statements live here. The paper's
  empirical content is NOT theorems and is deliberately NOT encoded — see the
  [OPEN] block at the bottom. Encoding an empirical claim as a trivially-true
  Lean statement would be exactly the defect the corpus exists to prevent.

  Run:  lake env lean ForcedUrgency.lean     (against a built Mathlib, e.g. the
        `orthogenesis` project used for SaturnHexagon.lean / SmokeBox.lean)
  Then read #print axioms: every theorem must show only
  [propext, Classical.choice, Quot.sound] — no sorryAx.

  KERNEL STATUS: VERIFIED 2026-07-25 — run with `lake env lean` against the
  orthogenesis project (Lean v4.33.0-rc1, Mathlib built). All six theorems:
  #print axioms → [propext, Classical.choice, Quot.sound], no sorryAx.
  (One cosmetic linter warning: unused hypothesis h0 in A_strictMono — the
  monotonicity holds without ρ₁ ≥ 0; harmless, not an error.)
-/
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic

namespace ForcedUrgency

/-- Amplification factor: cumulative displacement from a unit urgency shock when
    a fraction `ρ` of forced supply is harvested (absorbed and held) and thereby
    tightens the constraint that produces the next round. -/
noncomputable def A (ρ : ℝ) : ℝ := 1 / (1 - ρ)

/-! ## 1. The amplification factor IS the geometric sum of the cascade

This is the real content of "A = 1/(1-ρ)": not the definition restated, but the
claim that the round-by-round reallocation actually accumulates to it. -/

/-- If the lemma name errors on your Mathlib version, it is `tsum_geometric_of_lt_1`. -/
theorem cascade_sum (ρ : ℝ) (h0 : 0 ≤ ρ) (h1 : ρ < 1) :
    ∑' k : ℕ, ρ ^ k = A ρ := by
  rw [tsum_geometric_of_lt_one h0 h1]
  simp [A, one_div]

/-! ## 2. Order and comparative statics -/

/-- The cascade never dampens: a unit shock is displaced by at least a unit. -/
theorem A_ge_one (ρ : ℝ) (h0 : 0 ≤ ρ) (h1 : ρ < 1) : 1 ≤ A ρ := by
  have hpos : 0 < 1 - ρ := by linarith
  have hle  : 1 - ρ ≤ 1 := by linarith
  rw [A]
  have h := one_div_le_one_div_of_le hpos hle   -- 1/1 ≤ 1/(1-ρ)
  simpa using h

/-- No amplification exactly when nothing is harvested. -/
theorem A_eq_one_iff (ρ : ℝ) (h1 : ρ < 1) : A ρ = 1 ↔ ρ = 0 := by
  have hpos : 0 < 1 - ρ := by linarith
  rw [A, div_eq_one_iff_eq (ne_of_gt hpos)]
  constructor <;> intro h <;> linarith

/-- The ratchet is monotone in the harvest coefficient: a higher `ρ` strictly
    increases cumulative displacement. -/
theorem A_strictMono {ρ₁ ρ₂ : ℝ} (h0 : 0 ≤ ρ₁) (hlt : ρ₁ < ρ₂) (h1 : ρ₂ < 1) :
    A ρ₁ < A ρ₂ := by
  have hp2 : 0 < 1 - ρ₂ := by linarith
  have hle : 1 - ρ₂ < 1 - ρ₁ := by linarith
  rw [A, A]
  exact one_div_lt_one_div_of_lt hp2 hle

/-! ## 3. Divergence as ρ → 1 (filter-free, elementary form)

`A → ∞ as ρ → 1⁻` stated so the kernel certifies unboundedness without topology:
for any target `M`, some admissible `ρ` produces displacement exceeding `M`. -/

theorem A_unbounded (M : ℝ) : ∃ ρ : ℝ, 0 ≤ ρ ∧ ρ < 1 ∧ M < A ρ := by
  have hMpos : 0 < |M| + 2 := by positivity
  set c : ℝ := 1 / (|M| + 2) with hc
  have hcpos : 0 < c := by rw [hc]; positivity
  have hcle1 : c ≤ 1 := by
    rw [hc, div_le_one hMpos]; have := abs_nonneg M; linarith
  refine ⟨1 - c, by linarith, by linarith, ?_⟩
  have h1c : (1 : ℝ) - (1 - c) = c := by ring
  rw [A, h1c, hc, one_div_one_div]
  have hM : M ≤ |M| := le_abs_self M
  linarith

/-! ## 4. Policy comparative-statics -/

/-- Any intervention (e.g. bridge liquidity, foreclosure-timing regulation,
    limits on distressed-asset purchase) that strictly lowers the harvest
    coefficient strictly lowers cumulative displacement. Direct corollary of
    `A_strictMono` — the model's one clean, machine-checked policy statement. -/
theorem policy_lowers_displacement {ρ ρ' : ℝ}
    (h0 : 0 ≤ ρ') (hlt : ρ' < ρ) (h1 : ρ < 1) : A ρ' < A ρ :=
  A_strictMono h0 hlt h1

#print axioms cascade_sum
#print axioms A_ge_one
#print axioms A_eq_one_iff
#print axioms A_strictMono
#print axioms A_unbounded
#print axioms policy_lowers_displacement

end ForcedUrgency

/-
  ============================================================================
  [OPEN] — NOT formalized here, and must NOT be encoded as Lean theorems.
  These are empirical / econometric claims; the kernel cannot certify them and
  a trivially-true encoding would misrepresent their status.

  FUG-OPEN-1  The identification failure (§1). "Loss aversion is not identified
              under latent liquidity" is a statement about an econometric model's
              identifiability, contingent on data-generating assumptions — an
              econometrics theorem at best, not this arithmetic core.
  FUG-OPEN-2  The buffer-depletion lag (§3). A claim about real time-series
              (FRED/Z.1); [DATA], not [MODEL]. Its magnitude [N] is measured,
              not derived.
  FUG-OPEN-3  The values of ρ and the contract share (Appendix A). Empirical
              coefficients to be estimated from housing/foreclosure data; ρ is
              [OPEN] until estimated with a stated identification strategy. What
              is proved above is only how A depends on ρ *given* ρ — never what
              ρ is.
  FUG-OPEN-4  The AI-displacement mapping (§5) is an interpretation of the same
              coefficients, not a separate theorem.

  Full credit — in the didactic sense of CONTRIBUTING.md — for formalizing
  FUG-OPEN-1 as a genuine identification result, OR for a proof that it fails
  as stated.
  ============================================================================
-/
