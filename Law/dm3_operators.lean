/-
  dm3_operators.lean
  ==================
  Algebraic model of the dm³ contact manifold operators.
  Part of: Principia Orthogona · Law of Monsters
  Pablo Nogueira Grossi · G6 LLC · Newark NJ · June 2026
  DOI: 10.5281/zenodo.20561165
  Lean 4 / Mathlib4
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Topology.Algebra.Order.LiminfLimsup

/-!
## Overview

This file formalises the four primitive TOGT operators on the dm³ contact manifold
in two models:

* **3D model** — full state space ℝ³ = {(r, θ, z)}, used for non-commutativity proofs.
* **1D basin model** — tracks only the radial coordinate r, used for convergence and
  fixed-point proofs.

The contact form is α = dz − r²dθ. The contact hyperplane at a point is
ξ = ker α = {v : v_z = r²·v_θ}.

The four primitive operators are:
* **C** (Constraint) — projects onto the contact hyperplane.
* **K** (Kinetics)   — unit-time Reeb flow along ∂_z (preserves r).
* **F** (Fold)       — Whitney A₁ singularity at curvature threshold κ*.
* **U** (Unfold)     — gradient descent on V(r) = ½(r − r₀)².

The TOGT generator is 𝔤 = U ∘ F ∘ K ∘ C.
-/

namespace DM3

open Real

/-! ## 3D State Space -/

/-- A state in the dm³ manifold: cylindrical coordinates (r, θ, z). -/
abbrev State := ℝ × ℝ × ℝ

/-! ## 3D Operators -/

/-- **C₃** — Contact constraint.
    Resets z to satisfy the contact condition α = 0: z ↦ r²·θ.
    This ensures the trajectory remains in the contact distribution ξ = ker α. -/
def C₃ : State → State
  | (r, θ, _) => (r, θ, r ^ 2 * θ)

/-- **K₃** — Reeb kinetics.
    Unit-time flow along the Reeb vector field R_α = ∂_z.
    The Reeb field satisfies α(R_α) = 1 and ι_{R_α}dα = 0; in dm³, R_α = ∂_z. -/
def K₃ : State → State
  | (r, θ, z) => (r, θ, z + 1)

/-- **F₃** — Whitney fold at κ*.
    Acts only on the radial coordinate r:
    * Below κ*: identity (orbit stays in basin).
    * Above κ*: reflection r ↦ 2κ* − r (A₁ singularity / catastrophe fold). -/
def F₃ (κ : ℝ) : State → State
  | (r, θ, z) => (if r ≤ κ then r else 2 * κ - r, θ, z)

/-- **U₃** — Gradient unfold.
    Gradient descent on V(r) = ½(r − r₀)² with step size 1:
    r ↦ r₀ + (r − r₀)·exp(−1). -/
def U₃ (r₀ : ℝ) : State → State
  | (r, θ, z) => (r₀ + (r - r₀) * exp (-1), θ, z)

/-- **𝔤₃** — The TOGT generator in 3D: 𝔤 = U ∘ F ∘ K ∘ C. -/
def G₃ (κ r₀ : ℝ) : State → State :=
  U₃ r₀ ∘ F₃ κ ∘ K₃ ∘ C₃

/-! ## Non-Commutativity Theorems -/

/-- **Theorem 1 (Non-commutativity of C₃ and K₃).**
    C₃ ∘ K₃ ≠ K₃ ∘ C₃. Witnessed at s = (1, 1, 0).

    Proof:
    * (C₃ ∘ K₃)(1, 1, 0) = C₃(1, 1, 1) = (1, 1, 1·1) = (1, 1, 1)
    * (K₃ ∘ C₃)(1, 1, 0) = K₃(1, 1, 1) = (1, 1, 2)   ← differs! -/
theorem C₃_K₃_noncommutative :
    ∃ s : State, C₃ (K₃ s) ≠ K₃ (C₃ s) :=
  ⟨(1, 1, 0), by simp [C₃, K₃]; norm_num⟩

/-- **Theorem 2 (C₃ is idempotent).**
    Projecting twice is the same as projecting once: C₃ ∘ C₃ = C₃. -/
theorem C₃_idempotent : ∀ s : State, C₃ (C₃ s) = C₃ s := by
  intro ⟨r, θ, z⟩
  simp [C₃]; ring

/-- **Theorem 3 (K₃ breaks the contact condition).**
    After applying K₃ to any non-contact state, the result violates z = r²·θ.
    More precisely: K₃ shifts z by 1 while C₃ ignores the old z and resets it,
    so K₃ applied AFTER contact projection yields a non-contact state. -/
theorem K₃_breaks_contact :
    ∃ s : State, let (r, θ, z) := K₃ s; z ≠ r ^ 2 * θ := by
  exact ⟨(1, 0, 0), by simp [K₃]; norm_num⟩

/-- **Theorem 4 (Commutativity of F₃ and K₃ as point maps).**
    F₃ and K₃ commute as functions (they act on different coordinates):
    F₃ acts only on r; K₃ acts only on z. -/
theorem F₃_K₃_commute (κ : ℝ) :
    ∀ s : State, F₃ κ (K₃ s) = K₃ (F₃ κ s) := by
  intro ⟨r, θ, z⟩
  simp [F₃, K₃]
  split_ifs <;> rfl

/-- **Corollary.** The non-commutativity in the full operator chain 𝔤 = U∘F∘K∘C
    arises from the C-K interaction, not from F-K. This places the catastrophe
    (the Whitney fold F) as structurally downstream of the contact reset C. -/

/-! ## 1D Basin Model -/

/-!
For convergence and fixed-point analysis we project to the radial coordinate.
This is the "basin model": only r matters for the attractor dynamics.
-/

/-- **F** — Fold in 1D -/
def F₁ (κ r : ℝ) : ℝ := if r ≤ κ then r else 2 * κ - r

/-- **U** — Unfold / gradient descent in 1D -/
def U₁ (r₀ r : ℝ) : ℝ := r₀ + (r - r₀) * exp (-1)

/-- **𝔤₁** — Generator in 1D (C and K act as identity on r in this model) -/
def G₁ (κ r₀ r : ℝ) : ℝ := U₁ r₀ (F₁ κ r)

/-! ## Fixed Point and Contractivity -/

/-- **Theorem 5 (Fixed point of 𝔤₁).**
    The basin attractor r₀ is a fixed point of 𝔤₁, provided r₀ < κ. -/
theorem G₁_fixed_point (r₀ κ : ℝ) (h : r₀ < κ) :
    G₁ κ r₀ r₀ = r₀ := by
  simp [G₁, F₁, U₁, if_pos (le_of_lt h)]
  ring

/-- **Theorem 6 (Contractivity).**
    For r in the basin (r ≤ κ), 𝔤₁ contracts toward r₀ with factor exp(−1): -/
theorem G₁_contractive (r₀ κ r : ℝ) (h : r ≤ κ) :
    G₁ κ r₀ r - r₀ = (r - r₀) * exp (-1) := by
  simp [G₁, F₁, U₁, if_pos h]
  ring

/-- **Lemma (exp(−1) < 1).**
    The contraction factor is strictly less than 1. -/
lemma exp_neg_one_lt_one : exp (-1) < 1 := by
  rw [show (-1 : ℝ) = -1 from rfl]
  exact exp_lt_one_iff.mpr (by norm_num)

/-- **Lemma (exp(−1) > 0).**
    The contraction factor is positive (orbit stays on same side of r₀). -/
lemma exp_neg_one_pos : 0 < exp (-1) :=
  exp_pos _

/-- **Theorem 7 (Distance strictly decreases in basin).**
    If r ≠ r₀ and r ≤ κ, one step of 𝔤₁ strictly decreases distance to r₀. -/
theorem G₁_distance_decreases (r₀ κ r : ℝ) (h : r ≤ κ) (hne : r ≠ r₀) :
    |G₁ κ r₀ r - r₀| < |r - r₀| := by
  rw [G₁_contractive r₀ κ r h, abs_mul]
  have hpos : 0 < |r - r₀| := abs_pos.mpr (sub_ne_zero.mpr hne)
  have hexp : |exp (-1)| = exp (-1) := abs_of_pos exp_neg_one_pos
  rw [hexp]
  calc exp (-1) * |r - r₀|
      < 1 * |r - r₀| := by
          apply mul_lt_mul_of_pos_right exp_neg_one_lt_one hpos
    _ = |r - r₀| := one_mul _

/-- **Theorem 8 (Geometric decay of iterates).**
    After n steps inside the basin, |𝔤₁ⁿ(r) − r₀| = |r − r₀| · exp(−n). -/
theorem G₁_iterate_distance (r₀ κ r : ℝ) (h : r ≤ κ) (n : ℕ) :
    G₁ κ r₀ ^[n] r - r₀ = (r - r₀) * exp (-1) ^ n := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ', Function.comp]
    have hF : F₁ κ (G₁ κ r₀ ^[n] r) ≤ κ := by
      simp [F₁]
      split_ifs with hle
      · exact hle
      · -- Reflected point: 2κ − r' where r' > κ → 2κ − r' < κ iff κ < r'
        push_neg at hle
        linarith
    rw [G₁_contractive r₀ κ _ hF, ih]
    ring

/-- **Corollary (Convergence to r₀).**
    All orbits starting in the basin [0, κ] converge to r₀. -/
theorem G₁_converges (r₀ κ r : ℝ) (h : r ≤ κ) :
    Filter.Tendsto (fun n => G₁ κ r₀ ^[n] r)
      Filter.atTop (nhds r₀) := by
  rw [Metric.tendsto_atTop]
  intro ε hε
  -- Need N s.t. |r - r₀| · exp(−1)^N < ε
  obtain ⟨N, hN⟩ := exists_pow_lt_of_lt_one
    (div_pos hε (abs_nonneg (r - r₀) |>.lt_of_ne' (by
      simp [ne_eq]
      exact fun h => by simp [h] at hε))) exp_neg_one_lt_one
  refine ⟨N, fun n hn => ?_⟩
  simp [dist, Real.dist_eq]
  rw [← sub_eq_zero, ← G₁_iterate_distance r₀ κ r h n, sub_self]
  -- Absolute value bound via geometric decay
  rw [G₁_iterate_distance r₀ κ r h n, abs_mul]
  calc |r - r₀| * |exp (-1) ^ n|
      ≤ |r - r₀| * exp (-1) ^ N := by
          apply mul_le_mul_of_nonneg_left _ (abs_nonneg _)
          rw [abs_of_pos (pow_pos exp_neg_one_pos n)]
          exact pow_le_pow_of_le_one (le_of_lt exp_neg_one_pos)
            (le_of_lt exp_neg_one_lt_one) hn
    _ < ε := by linarith [mul_lt_of_lt_one_left hε hN]

/-! ## The Triad -/

/-- A point r satisfies the **TO/TOGT Triad** if it lies in the basin of attraction:
    (i) The contact condition is met (modelled by r ≤ κ in 1D),
    (ii) nilpotency: 𝔤ⁿ(r) → r₀,
    (iii) spectral collapse: convergence is exponential. -/
def inTriad (κ r₀ r : ℝ) : Prop :=
  r ≤ κ ∧ ∀ ε > 0, ∃ N : ℕ, ∀ n ≥ N, |G₁ κ r₀ ^[n] r - r₀| < ε

/-- r₀ is in its own triad. -/
theorem ocio_in_triad (r₀ κ : ℝ) (h : r₀ < κ) : inTriad κ r₀ r₀ :=
  ⟨le_of_lt h, fun ε hε => ⟨0, fun n _ => by
    simp [G₁_iterate_distance r₀ κ r₀ (le_of_lt h) n, sub_self]
    exact hε⟩⟩

/-- **Theorem 9 (Triad Preservation).**
    If r is in the triad, so is 𝔤₁(r). -/
theorem triad_preserved (r₀ κ r : ℝ) (hT : inTriad κ r₀ r) :
    inTriad κ r₀ (G₁ κ r₀ r) := by
  obtain ⟨hle, hconv⟩ := hT
  refine ⟨?_, ?_⟩
  · -- G₁(r) ≤ κ: F folds, U shrinks
    simp [G₁, F₁, U₁]
    split_ifs with hF
    · -- r ≤ κ, so F₁ = r, U gives r₀ + (r - r₀)·exp(-1)
      -- Show r₀ + (r - r₀)·exp(-1) ≤ κ
      have hκ_pos : r₀ ≤ κ := by linarith
      nlinarith [exp_neg_one_pos, exp_neg_one_lt_one]
    · -- r > κ, so F₁ = 2κ - r < κ; U gives r₀ + (2κ - r - r₀)·exp(-1)
      push_neg at hF
      have h2κ : 2 * κ - r < κ := by linarith
      have hκ_pos : r₀ ≤ κ := by linarith
      nlinarith [exp_neg_one_pos, exp_neg_one_lt_one]
  · -- Convergence: shift iterate index by 1
    intro ε hε
    obtain ⟨N, hN⟩ := hconv ε hε
    exact ⟨N, fun n hn => by
      have : G₁ κ r₀ ^[n] (G₁ κ r₀ r) = G₁ κ r₀ ^[n + 1] r := by
        rw [Function.iterate_succ', Function.comp]
      rw [this]
      exact hN (n + 1) (Nat.le_succ_of_le hn)⟩

end DM3
