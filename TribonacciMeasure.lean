import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Topology.Order.IntermediateValue

namespace NuclearPhysicsB

/-!
# Tribonacci Recurrence and TOGT Fractal Measure

The dm³ orthogenetic recurrence

  **w(k+3) = w(k+2) + w(k+1) + w(k)**

arises from iterated G-applications along the Reeb flow.  Its dominant
eigenvalue η (Tribonacci constant, η³ = η² + η + 1, η ≈ 1.839286755214161)
defines the universal TOGT scaling.

In the Nuclear Physics B context (NPB §4), the geometric weight η^{−k}
induces the fractal measure μ_η on the curvature distribution ker α of
nuclear matter.  The stability threshold **g = 33** predicts the generation
at which orthogenetic cycles lock into coherent hadronic or collective modes.
-/

-- ============================================================
-- Tribonacci recurrence
-- ============================================================

/-- The Tribonacci sequence: w(0) = 0, w(1) = 1, w(2) = 1,
    w(n+3) = w(n+2) + w(n+1) + w(n). -/
def tribonacci : ℕ → ℕ
  | 0       => 0
  | 1       => 1
  | 2       => 1
  | (n + 3) => tribonacci (n + 2) + tribonacci (n + 1) + tribonacci n
termination_by n => n

@[simp] lemma tribonacci_zero : tribonacci 0 = 0 := rfl
@[simp] lemma tribonacci_one  : tribonacci 1 = 1 := rfl
@[simp] lemma tribonacci_two  : tribonacci 2 = 1 := rfl

lemma tribonacci_succ3 (n : ℕ) :
    tribonacci (n + 3) = tribonacci (n + 2) + tribonacci (n + 1) + tribonacci n := rfl

-- ============================================================
-- Tribonacci constant η
-- ============================================================

/-- The characteristic polynomial p(x) = x³ − x² − x − 1 has a root in [1, 2].
    IVT witnesses: p(1) = −2 < 0 and p(2) = 1 > 0. -/
private lemma η_exists : ∃ x : ℝ, 1 ≤ x ∧ x ≤ 2 ∧ x ^ 3 = x ^ 2 + x + 1 := by
  -- p is continuous on [1, 2]
  have hcont : ContinuousOn (fun x : ℝ => x ^ 3 - x ^ 2 - x - 1) (Set.Icc 1 2) :=
    ((((continuous_pow 3).sub (continuous_pow 2)).sub continuous_id).sub
      continuous_const).continuousOn
  -- 0 lies between p(1) = −2 and p(2) = 1
  have hmem : (0 : ℝ) ∈ Set.Icc ((1 : ℝ) ^ 3 - 1 ^ 2 - 1 - 1)
                                   ((2 : ℝ) ^ 3 - 2 ^ 2 - 2 - 1) := by norm_num
  -- IVT gives a root c ∈ [1, 2]
  obtain ⟨c, hc, hpc⟩ :=
    intermediate_value_Icc (by norm_num : (1 : ℝ) ≤ 2) hcont hmem
  exact ⟨c, hc.1, hc.2, by linarith⟩

/-- The Tribonacci constant η: the real root of x³ − x² − x − 1 = 0 in [1, 2],
    constructed via the Intermediate Value Theorem.
    Satisfies η³ = η² + η + 1 and η > 1 (proved below without axioms beyond Mathlib4). -/
noncomputable def η : ℝ := η_exists.choose

/-- The defining properties of η: it lies in [1, 2] and satisfies the characteristic eq. -/
private lemma η_spec : 1 ≤ η ∧ η ≤ 2 ∧ η ^ 3 = η ^ 2 + η + 1 :=
  η_exists.choose_spec

/-- η satisfies η³ = η² + η + 1 (characteristic equation). -/
theorem η_characteristic : η ^ 3 = η ^ 2 + η + 1 := η_spec.2.2

/-- η > 1.
    Proof: η ≥ 1 from the IVT interval; equality is ruled out because
    substituting η = 1 into the characteristic equation gives 1 = 3. -/
theorem η_gt_one : 1 < η := by
  rcases η_spec.1.eq_or_lt with h | h
  · -- η = 1 leads to 1 = 3 via η_characteristic
    exfalso
    have hchar := η_spec.2.2
    rw [← h] at hchar
    norm_num at hchar
  · exact h

/-- η > 0 (immediate from η > 1). -/
theorem η_pos : 0 < η := lt_trans one_pos η_gt_one

/-- η ≠ 0. -/
theorem η_ne_zero : η ≠ 0 := ne_of_gt η_pos

-- ============================================================
-- Geometric weight and fractal measure
-- ============================================================

/-- Geometric weight w_k = η^{−k} = (η⁻¹)^k.
    The decreasing sequence defining the TOGT fractal density on ker α. -/
noncomputable def weight (k : ℕ) : ℝ := (η⁻¹) ^ k

@[simp] theorem weight_zero : weight 0 = 1 := by simp [weight]

theorem weight_pos (k : ℕ) : 0 < weight k :=
  pow_pos (inv_pos.mpr η_pos) k

/-- The weight sequence is strictly antitone: larger generation k ↝ smaller amplitude.
    Proof: η⁻¹ ∈ (0, 1) because η > 1. -/
theorem weight_strictAnti : StrictAnti weight := by
  intro a b hab
  simp only [weight]
  apply pow_lt_pow_of_lt_one
  · exact le_of_lt (inv_pos.mpr η_pos)
  · exact inv_lt_one η_gt_one
  · exact hab

-- ============================================================
-- Stability threshold
-- ============================================================

/-- The TOGT stability threshold: **g = 33** generations.
    Prediction (NPB §4): hadronic or collective modes lock in at g_threshold
    iterations, consistent with lattice-QCD nuclear binding scales. -/
def g_threshold : ℕ := 33

/-- Weight at the stability threshold (≈ η^{−33}). -/
noncomputable def threshold_weight : ℝ := weight g_threshold

end NuclearPhysicsB
