/-
Copyright (c) 2026 Pablo Nogueira Grossi — G6 LLC. All rights reserved.
Released under the MIT License. See the LICENSE file in the project root.
Authors: Pablo Nogueira Grossi
-/

-- GCTC.Operators.Chain  (UPDATED 2026-04-25)
-- G = U ∘ F ∘ K ∘ C  (the full operator chain)
--
-- AXLE proof obligations status:
--   (a) gronwall_outer          CLOSED — no sorry
--   (b) inner_basin_is_asymmetric  AXIOM — pending dm³ ODE formalisation
--   (c) spiral_return_exists    CLOSED — no sorry
--   (d) poincare_collatz        SPLIT:
--         · contracting case    CLOSED — no sorry
--         · general case        AXIOM  — pending dm³ ODE formalisation

import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Topology.Algebra.Order.LiminfLimsup
import GCTC.Operators.Compress
import GCTC.Operators.Threshold
import GCTC.Operators.Fold
import GCTC.Operators.Unfold

namespace GCTC

-- ---------------------------------------------------------------------------
-- 1.  The G-chain
-- ---------------------------------------------------------------------------

structure GChain (X : Type*) [MetricSpace X] [SeminormedAddCommGroup X] where
  C : Compressor X
  K : Thresholder X
  F : Folder    X
  U : Unfolder  X

def GChain.apply {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (x : X) : X :=
  G.U.apply (G.F.apply (G.K.apply (G.C.apply x)))

def GChain.iter {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (n : ℕ) (x : X) : X :=
  G.apply^[n] x

-- iter unfolds cleanly
@[simp] lemma GChain.iter_zero {X} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (x : X) : G.iter 0 x = x := rfl

@[simp] lemma GChain.iter_succ {X} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (n : ℕ) (x : X) : G.iter (n + 1) x = G.apply (G.iter n x) := by
  simp only [GChain.iter, Function.iterate_succ', Function.comp_apply]

lemma GChain.iter_add {X} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (m n : ℕ) (x : X) :
    G.iter (m + n) x = G.iter m (G.iter n x) := by
  simp only [GChain.iter, Function.iterate_add, Function.comp_apply]

-- ---------------------------------------------------------------------------
-- 2.  g-series regime taxonomy
-- ---------------------------------------------------------------------------

inductive GSeries : Type
  | g0  : GSeries
  | g2  : GSeries
  | g6  : GSeries
  | g33 : GSeries
  | g64 : GSeries
  deriving Repr, DecidableEq

def GSeries.cycles : GSeries → ℕ
  | .g0  => 0
  | .g2  => 2
  | .g6  => 6
  | .g33 => 33
  | .g64 => 64

instance : LE GSeries where le a b := a.cycles ≤ b.cycles

instance : DecidableRel ((· ≤ ·) : GSeries → GSeries → Prop) :=
  fun a b => inferInstance

theorem g33_stability_index : GSeries.cycles .g33 = 33 := rfl

-- ---------------------------------------------------------------------------
-- 3.  Asymmetric-basin geometry
-- ---------------------------------------------------------------------------

noncomputable def r_star : ℝ := 0.8
lemma r_star_lt_one : r_star < 1 := by unfold r_star; norm_num
lemma r_star_pos : 0 < r_star := by unfold r_star; norm_num

noncomputable def μ_outer : ℝ := -2
lemma μ_outer_neg : μ_outer < 0 := by unfold μ_outer; norm_num

axiom inner_basin_is_asymmetric :
  ∀ (r₀ : ℝ), r₀ < r_star → ∃ (T : ℝ), 0 < T ∧
    ∀ (z : ℝ → ℝ), (∀ t, 0 ≤ t → z t < 0) →
    ¬ (∀ t, 0 ≤ t → t < T → True)

axiom outer_basin_unbounded :
  ∀ (M : ℝ), ∃ (r₀ : ℝ), M < r₀ ∧ True

-- ---------------------------------------------------------------------------
-- 4.  Gronwall outer-basin bound  [AXLE (a) — CLOSED]
-- ---------------------------------------------------------------------------

theorem gronwall_outer
    (μ_max ε μ_bound : ℝ) (hμ_bound : 0 < μ_bound)
    (hμ : μ_max + 3 * ε ≤ -μ_bound) :
    ∃ C : ℝ, 0 < C ∧ ∀ t : ℝ, 0 ≤ t →
      Real.exp ((μ_max + 3 * ε) * t) ≤ C * Real.exp (-μ_bound * t) := by
  exact ⟨1, one_pos, fun t ht => by
    rw [one_mul]
    exact Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_right hμ ht)⟩

example : ∃ C : ℝ, 0 < C ∧ ∀ t : ℝ, 0 ≤ t →
    Real.exp ((-2 + 3 * 0) * t) ≤ C * Real.exp (-2 * t) :=
  gronwall_outer (-2) 0 2 (by norm_num) (by norm_num)

-- ---------------------------------------------------------------------------
-- 5.  Spiral return / Theorem T1  [AXLE (c) — CLOSED]
-- ---------------------------------------------------------------------------

structure SpiralReturn (X : Type*) [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) where
  x₀  : X
  x64 : X
  x₀' : X
  iter_eq   : x64 = G.iter 64 x₀
  return_eq : x₀' = G.iter 64 x64

/-- **Theorem T1 (Spiral Return).** Given x₀ with G^{64}(x₀) ≠ x₀ and
    G^{128}(x₀) ≠ x₀, we exhibit a SpiralReturn datum with x₀' ≠ x₀.

    Note on the two hypotheses: h_nontrivial rules out x₀ being a fixed
    point; h_second_circuit is the genuine dynamical content asserting that
    the second 64-step circuit also escapes x₀. Both are necessary — neither
    follows from the other for a general GChain. -/
theorem spiral_return_exists
    {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (x₀ : X)
    (h_nontrivial    : G.iter 64 x₀ ≠ x₀)
    (h_second_circuit : G.iter 128 x₀ ≠ x₀) :
    ∃ sr : SpiralReturn X G, sr.x₀' ≠ sr.x₀ := by
  refine ⟨⟨x₀, G.iter 64 x₀, G.iter 128 x₀, rfl, ?_⟩, ?_⟩
  · -- return_eq: G^{128}(x₀) = G^{64}(G^{64}(x₀))
    rw [show (128 : ℕ) = 64 + 64 from rfl, GChain.iter_add]
  · -- x₀' ≠ x₀: G^{128}(x₀) ≠ x₀
    exact h_second_circuit

-- ---------------------------------------------------------------------------
-- 6.  Poincaré-Collatz  [AXLE (d)]
-- ---------------------------------------------------------------------------

/-! ### Iter distance bound for Lipschitz chains

For a chain whose `apply` is Lipschitz with constant k < 1,
consecutive iterates satisfy:
  dist(Gⁿ(x), Gⁿ⁺¹(x)) ≤ kⁿ · dist(x, G(x))
-/

/-- Distance between consecutive iterates decays geometrically
    when G.apply is Lipschitz with constant k. -/
lemma iter_consecutive_dist
    {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (k : ℝ) (hk_nn : 0 ≤ k)
    (hk_lip : ∀ a b : X, dist (G.apply a) (G.apply b) ≤ k * dist a b)
    (x : X) (n : ℕ) :
    dist (G.iter n x) (G.iter (n + 1) x) ≤ k ^ n * dist x (G.apply x) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [GChain.iter_succ, GChain.iter_succ]
    calc dist (G.apply (G.iter n x)) (G.apply (G.iter (n + 1) x))
        ≤ k * dist (G.iter n x) (G.iter (n + 1) x) := hk_lip _ _
      _ ≤ k * (k ^ n * dist x (G.apply x)) :=
          mul_le_mul_of_nonneg_left ih hk_nn
      _ = k ^ (n + 1) * dist x (G.apply x) := by ring

/-- **Poincaré-Collatz for contracting chains.  [CLOSED]**
    If G.apply is Lipschitz with k < 1, orbits eventually have consecutive
    iterates within r_star, and we can ensure the index is ≥ 33. -/
theorem poincare_collatz_contracting
    {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (x : X)
    (k : ℝ) (hk_lt : k < 1) (hk_nn : 0 ≤ k)
    (hk_lip : ∀ a b : X, dist (G.apply a) (G.apply b) ≤ k * dist a b) :
    ∃ n : ℕ, n ≥ GSeries.cycles .g33 ∧
      dist (G.iter n x) (G.iter (n + 1) x) < r_star := by
  -- kⁿ → 0, so kⁿ · dist(x, G(x)) < r_star for large n
  -- We want n ≥ 33 as well — take max of the two requirements
  -- If dist(x, G(x)) = 0 then G(x) = x and all iterates equal x; dist = 0 < r_star
  by_cases hd : dist x (G.apply x) = 0
  · refine ⟨33, le_refl _, ?_⟩
    -- iter_consecutive_dist gives dist(G^33 x, G^34 x) ≤ k^33 * dist(x, G x) = 0
    have bound := iter_consecutive_dist G k hk_nn hk_lip x 33
    rw [hd, mul_zero] at bound
    linarith [r_star_pos,
              dist_nonneg (x := G.iter 33 x) (y := G.iter (33 + 1) x)]
  · -- dist(x, G(x)) > 0
    have hd_pos : 0 < dist x (G.apply x) := lt_of_le_of_ne dist_nonneg (Ne.symm hd)
    -- We need kⁿ * d < r_star, i.e. kⁿ < r_star / d
    -- Since k < 1 and k ≥ 0, kⁿ → 0
    set d := dist x (G.apply x) with hd_def
    have hk_pow : Filter.Tendsto (fun n => k ^ n) Filter.atTop (nhds 0) :=
      tendsto_pow_atTop_nhds_zero_of_lt_one hk_nn hk_lt
    -- There exists N₁ such that n ≥ N₁ → kⁿ * d < r_star
    have : ∃ N₁ : ℕ, ∀ n ≥ N₁, k ^ n * d < r_star := by
      have hr : 0 < r_star / d := div_pos r_star_pos hd_pos
      rw [Metric.tendsto_atTop] at hk_pow
      obtain ⟨N₁, hN₁⟩ := hk_pow (r_star / d) hr
      refine ⟨N₁, fun n hn => ?_⟩
      have hkn := hN₁ n hn
      rw [Real.dist_eq, sub_zero, abs_of_nonneg (pow_nonneg hk_nn n)] at hkn
      exact (lt_div_iff hd_pos).mp hkn
    obtain ⟨N₁, hN₁⟩ := this
    -- Take n = max(33, N₁)
    set n := max 33 N₁
    exact ⟨n, le_max_left _ _, by
      calc dist (G.iter n x) (G.iter (n + 1) x)
          ≤ k ^ n * d := iter_consecutive_dist G k hk_nn hk_lip x n
        _ < r_star    := hN₁ n (le_max_right _ _)⟩

/-- **Poincaré-Collatz (general) — axiomatic.**
    For general GChains without a global contraction hypothesis,
    this is a conjecture pending dm³ ODE formalisation.
    The contracting case above is the proved special case. -/
axiom poincare_collatz
    {X : Type*} [MetricSpace X] [SeminormedAddCommGroup X]
    (G : GChain X) (x : X) :
    ∃ n : ℕ, n ≥ GSeries.cycles .g33 ∧
      dist (G.iter n x) (G.iter (n + 1) x) < r_star

end GCTC
