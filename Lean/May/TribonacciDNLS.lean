/-!
# TribonacciDNLS.lean
# ==================
# Formally verified analytic lemmas supporting:
#
#   "Differential Nonlinear Robustness of Critical States in
#    Fibonacci and Tribonacci Substitution Chains"
#   Pablo Nogueira Grossi, G6 LLC (2026)
#   Zenodo: https://doi.org/10.5281/zenodo.20026943
#
# What is proved here WITHOUT sorry
# ----------------------------------
# 1. The tribonacci constant η exists as a real root of
#    p(x) = x³ − x² − x − 1 in the interval [1, 2]  (IVT)
# 2. η > 1
# 3. η > 0
# 4. The geometric weight sequence w_k = η^{−k} is strictly antitone:
#    k < l → w_l < w_k
#
# These facts underwrite the amplitude envelope used in Section 3.2
# of the paper:  A_k ~ η^{−k}, well-defined and decaying.
#
# What is NOT claimed here
# ------------------------
# - The dm³ criticality principle (axiom in dm3_Criticality_gtct.lean)
# - GTCT Theorem T1 (carries sorry in gtct_t1.lean)
# - The g₃₃ = 33 stability conjecture (open, tracked in AXLE Issue #13)
# - Any claim that the DNLS results follow from Lean verification
#   (the numerics are independent Python/SciPy computations)
#
# Repository:  https://github.com/TOTOGT/AXLE
# ORCID:       0009-0000-6496-2186
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Topology.Order.IntermediateValue

namespace TribonacciDNLS

/-!
## The tribonacci constant η
-/

/-- The characteristic polynomial p(x) = x³ − x² − x − 1 has a root in [1, 2].
    IVT witnesses: p(1) = 1 − 1 − 1 − 1 = −2 < 0 and p(2) = 8 − 4 − 2 − 1 = 1 > 0. -/
private lemma η_exists : ∃ x : ℝ, 1 ≤ x ∧ x ≤ 2 ∧ x ^ 3 = x ^ 2 + x + 1 := by
  have hcont : ContinuousOn (fun x : ℝ => x ^ 3 - x ^ 2 - x - 1) (Set.Icc 1 2) :=
    ((((continuous_pow 3).sub (continuous_pow 2)).sub continuous_id).sub
      continuous_const).continuousOn
  have hmem : (0 : ℝ) ∈ Set.Icc ((1 : ℝ) ^ 3 - 1 ^ 2 - 1 - 1)
                                   ((2 : ℝ) ^ 3 - 2 ^ 2 - 2 - 1) := by norm_num
  obtain ⟨c, hc, hpc⟩ :=
    intermediate_value_Icc (by norm_num : (1 : ℝ) ≤ 2) hcont hmem
  exact ⟨c, hc.1, hc.2, by linarith⟩

/-- The tribonacci constant η: unique real root of x³ − x² − x − 1 = 0 in [1, 2].
    Constructed via the Intermediate Value Theorem; noncomputable. -/
noncomputable def η : ℝ := η_exists.choose

private lemma η_spec : 1 ≤ η ∧ η ≤ 2 ∧ η ^ 3 = η ^ 2 + η + 1 :=
  η_exists.choose_spec

/-- η satisfies the tribonacci characteristic equation. -/
theorem η_characteristic : η ^ 3 = η ^ 2 + η + 1 := η_spec.2.2

/-- η > 1.
    Proof: η ≥ 1 from the IVT interval; η = 1 is impossible because
    substituting gives 1 = 1 + 1 + 1 = 3, a contradiction. -/
theorem η_gt_one : 1 < η := by
  rcases η_spec.1.eq_or_lt with h | h
  · exfalso
    have hchar := η_spec.2.2
    rw [← h] at hchar
    norm_num at hchar
  · exact h

/-- η > 0 (immediate from η > 1). -/
theorem η_pos : 0 < η := lt_trans one_pos η_gt_one

/-- η ≠ 0. -/
theorem η_ne_zero : η ≠ 0 := ne_of_gt η_pos

/-!
## The geometric weight sequence w_k = η^{−k}

This is the amplitude envelope used in Section 3.2 of the paper:
the tribonacci substitution chain's natural scaling factor η^{−k}
is well-defined (positive for all k) and strictly decreasing.
-/

/-- Geometric weight: w_k = η^{−k} = (η⁻¹)^k. -/
noncomputable def w (k : ℕ) : ℝ := (η⁻¹) ^ k

@[simp] theorem w_zero : w 0 = 1 := by simp [w]

/-- All weights are strictly positive. -/
theorem w_pos (k : ℕ) : 0 < w k :=
  pow_pos (inv_pos.mpr η_pos) k

/-- η⁻¹ ∈ (0, 1) because η > 1. -/
private lemma η_inv_lt_one : η⁻¹ < 1 := inv_lt_one η_gt_one

private lemma η_inv_pos : 0 < η⁻¹ := inv_pos.mpr η_pos

/-- The weight sequence is strictly antitone:
    k < l → w l < w k.
    Proof: η⁻¹ ∈ (0,1), so (η⁻¹)^l < (η⁻¹)^k when k < l. -/
theorem w_strictAnti : StrictAnti w := by
  intro a b hab
  simp only [w]
  exact pow_lt_pow_of_lt_one (le_of_lt η_inv_pos) η_inv_lt_one hab

/-- Corollary: the weight sequence is antitone (k ≤ l → w l ≤ w k). -/
theorem w_antitone : Antitone w := StrictAnti.antitone w_strictAnti

/-- The weights decay to zero: w k → 0 as k → ∞. -/
theorem w_tendsto_zero : Filter.Tendsto w Filter.atTop (nhds 0) := by
  simp only [w]
  exact tendsto_pow_atTop_nhds_zero_of_lt_one
    (le_of_lt η_inv_pos) η_inv_lt_one

/-!
## Tribonacci recurrence

The sequence satisfying the recurrence w(k+3) = w(k+2) + w(k+1) + w(k)
with w(0)=0, w(1)=1, w(2)=1. Growth rate is controlled by η.
-/

def tribonacci : ℕ → ℕ
  | 0       => 0
  | 1       => 1
  | 2       => 1
  | (n + 3) => tribonacci (n + 2) + tribonacci (n + 1) + tribonacci n
termination_by n => n

@[simp] lemma tribonacci_zero : tribonacci 0 = 0 := rfl
@[simp] lemma tribonacci_one  : tribonacci 1 = 1 := rfl
@[simp] lemma tribonacci_two  : tribonacci 2 = 1 := rfl

lemma tribonacci_rec (n : ℕ) :
    tribonacci (n + 3) = tribonacci (n + 2) + tribonacci (n + 1) + tribonacci n := rfl

/-!
## Summary of verified facts for the paper

The following are proved above WITHOUT sorry and support the paper's claims:

  η_gt_one        : 1 < η        ✓
  η_pos           : 0 < η        ✓
  η_characteristic : η³ = η²+η+1  ✓
  w_pos           : ∀ k, 0 < w k  ✓
  w_strictAnti    : StrictAnti w  ✓  (the amplitude envelope is well-defined and decaying)
  w_tendsto_zero  : w k → 0      ✓

Open proof obligations (tracked in AXLE sorry roadmap):
  - dm³ criticality principle (axiom)
  - GTCT Theorem T1 (sorry)
  - g₃₃ stability threshold (conjecture, Issue #13)
-/

end TribonacciDNLS
