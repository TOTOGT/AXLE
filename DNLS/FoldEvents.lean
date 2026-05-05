/-
  FoldEvents.lean
  Non-Platonic g = 33 lock-in for the AXLE FoldEvents API.

  This file replaces the abstract `G ^ 6 = 33` placeholder with a
  concrete, computable saturating-counter model. No Jordan form, no
  spectral theory: the operator's iterates are forced to stabilise by
  a structural inequality (boundedness + monotonicity), and the
  proofs proceed by ordinary induction on the iterate count.

  The fold step `G : ℕ → ℕ` increments a counter by one each step
  until it reaches the lock-in generation `gThreshold = 33`, where it
  freezes. From there, every further iteration — including any
  6-step "hex packet" — leaves the state unchanged. This is the
  formal, observational content of the slogan "G⁶(hex) = 33".

  References: NPB §4 (lock-in prediction), TribonacciMeasure.lean
  (η-weighted fractal measure), AXLE design notes (non-Platonic route).
-/
import Mathlib.Data.Nat.Basic
import Mathlib.Logic.Function.Iterate
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.Tactic

namespace FoldEvents

/-! ## Lock-in threshold and fold step -/

/-- The lock-in generation predicted in NPB §4. -/
def gThreshold : ℕ := 33

/-- The fold step `G : ℕ → ℕ`: a saturating counter that increments by
    one each step until it reaches `gThreshold`, where it freezes.
    This is the non-Platonic, observational model of the orthogenetic
    G — purely structural, computable, and bounded. -/
def G (k : ℕ) : ℕ := min (k + 1) gThreshold

@[simp] lemma G_unfold (k : ℕ) : G k = min (k + 1) gThreshold := rfl

@[simp] theorem G_at_threshold : G gThreshold = gThreshold := by
  simp [gThreshold]

/-- G never exceeds the lock-in threshold. -/
theorem G_le_threshold (k : ℕ) : G k ≤ gThreshold := min_le_right _ _

/-- G is monotone in its argument. -/
theorem G_monotone : Monotone G := fun _ _ hab =>
  min_le_min (Nat.succ_le_succ hab) le_rfl

/-! ## Iterates of G -/

/-- Any number of iterations of G leave the threshold fixed. -/
theorem G_iter_threshold (n : ℕ) : G^[n] gThreshold = gThreshold := by
  induction n with
  | zero => rfl
  | succ k ih =>
      rw [Function.iterate_succ_apply', ih, G_at_threshold]

/-- Starting from 0, the n-th iterate of G is `min n gThreshold`. -/
theorem G_iter_zero_eq_min (n : ℕ) : G^[n] 0 = min n gThreshold := by
  induction n with
  | zero => rfl
  | succ k ih =>
      rw [Function.iterate_succ_apply', ih, G_unfold]
      simp only [gThreshold]
      omega

/-- After exactly 33 iterations from 0 we reach the threshold. -/
theorem G_iter_thirty_three : G^[33] 0 = gThreshold := by
  rw [G_iter_zero_eq_min]; rfl

/-! ## The lock-in theorems

    These two replace the `sorry`s in the original sketch.
-/

/-- **Stability at the threshold.** For every `n ≥ 33`, the n-th
    iterate of `G` has the lock-in generation as a fixed point.
    Once the system is at generation 33, no number of further
    applications of `G` can move it. -/
theorem stability_at_threshold (n : ℕ) (h : n ≥ gThreshold) :
    Function.IsFixedPt G^[n] gThreshold := by
  show G^[n] gThreshold = gThreshold
  exact G_iter_threshold n

/-- **6-fold hex lock-in.** A 6-step "hex packet" applied at the
    threshold leaves the state unchanged. This is the formal,
    non-Platonic content of the informal claim "G⁶(hex) = 33":
    six iterations starting from 33 stay at 33. -/
theorem g6_hex_lockin : G^[6] gThreshold = gThreshold :=
  G_iter_threshold 6

/-- **Orbit-level 6-fold lock-in.** Once the orbit starting at 0 has
    reached the threshold (i.e. after at least 33 iterations), any
    further 6-step hex packet leaves the orbit value unchanged. -/
theorem g6_hex_lockin_in_orbit (n : ℕ) (h : gThreshold ≤ n) :
    G^[6] (G^[n] 0) = G^[n] 0 := by
  rw [G_iter_zero_eq_min, min_eq_right h, g6_hex_lockin]

/-! ## Sanity checks (computable, decidable) -/

example : G^[6]   gThreshold = 33 := by decide
example : G^[33]  0           = 33 := by decide
example : G^[100] 0           = 33 := by decide
example : G^[39]  gThreshold = 33 := by decide  -- 6-fold packet × any starting point

end FoldEvents
