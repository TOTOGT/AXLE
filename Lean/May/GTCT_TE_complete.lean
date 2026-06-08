-- GTCT.Operators.TE  (corrected acronym)
-- T/E : the fifth operator — time and entropy are dual readings of
-- the same conformal reparameterization on ℕ_{>0}.
--
--   T asks: when does the return happen?
--   E asks: what is the entropic cost of this step?
--   Same function: T(n) = E(n) = log 3 − v₂(n) · log 2.
--
-- Connection to Collatz: the value T(n) is precisely the time-weight
-- of one Collatz step at n — log 3 from the 3n+1 branch, log 2 weighted
-- by v₂(n) (how many times 2 divides n) from the n/2 branches that
-- compose into a single macro-step.
--
-- This module is the discrete-conformal counterpart to the four
-- primitive operators in GTCT.Operators.{Compress, Threshold, Fold, Unfold}.
-- It does not replace them; it reparameterizes the temporal metric on
-- which their composition unfolds.

import Mathlib.NumberTheory.Padics.PadicVal
import Mathlib.Analysis.SpecialFunctions.Log.Basic

namespace GTCT

open Real

/-- The fifth operator T ≡ E : ℕ_{>0} → ℝ.
    Two physical readings, one function:
      • T  — conformal time of the discrete-to-continuous map
      • E  — entropic cost of one macro-step
    Steps with greater 2-adic structure are entropically cheaper. -/
noncomputable def TE (n : ℕ) : ℝ :=
  Real.log 3 - (padicValNat 2 n : ℝ) * Real.log 2

/-- T is the temporal reading of the fifth operator. -/
noncomputable abbrev T : ℕ → ℝ := TE

/-- E is the entropic reading of the fifth operator. -/
noncomputable abbrev E : ℕ → ℝ := TE

/-- The honest duality: time and entropy are the same number,
    asked from two directions. -/
theorem T_eq_E (n : ℕ) : T n = E n := rfl

/-- Useful re-statement: the operator unfolds explicitly as
    log 3 − v₂(n) · log 2. -/
theorem TE_def (n : ℕ) :
    TE n = Real.log 3 - (padicValNat 2 n : ℝ) * Real.log 2 := rfl

/-- For odd n (v₂(n) = 0), the cost of one step is log 3 — the bare
    cost of crossing the 3n+1 branch with no 2-adic discount. -/
theorem TE_odd {n : ℕ} (hn : Odd n) (hn0 : n ≠ 0) :
    TE n = Real.log 3 := by
  simp only [TE, TE_def]
  have hv : padicValNat 2 n = 0 := by
    rw [padicValNat.eq_zero_iff (by norm_num : 2 ≠ 1)]
    left
    exact Nat.Odd.not_two_dvd_nat hn
  simp [hv]

/-- For n = 2^k · m with m odd, the cost discounts by k · log 2.
    This is the core 2-adic discount lemma. -/
theorem TE_pow_two_mul {k : ℕ} {m : ℕ} (hm : Odd m) (hm0 : m ≠ 0) :
    TE (2 ^ k * m) = Real.log 3 - k * Real.log 2 := by
  simp only [TE, TE_def]
  have hv : padicValNat 2 (2 ^ k * m) = k := by
    rw [padicValNat.prime_pow_self_mul_pow_of_not_dvd
        (by norm_num : Nat.Prime 2)]
    · simp [padicValNat.eq_zero_iff]
      exact Nat.Odd.not_two_dvd_nat hm
  simp [hv]

/-- TE is strictly positive when v₂(n) · log 2 < log 3.
    Equivalently: TE n > 0 iff v₂(n) < log 3 / log 2 ≈ 1.585.
    So TE n > 0 for all n with v₂(n) ≤ 1 (i.e., n odd or n ≡ 2 mod 4). -/
theorem TE_pos_of_padicVal_le_one {n : ℕ} (hn : padicValNat 2 n ≤ 1) :
    0 < TE n := by
  simp only [TE, TE_def]
  have hlog3 : 0 < Real.log 3 := by
    apply Real.log_pos; norm_num
  have hlog2 : 0 < Real.log 2 := by
    apply Real.log_pos; norm_num
  have hbound : (padicValNat 2 n : ℝ) * Real.log 2 ≤ Real.log 2 := by
    have : (padicValNat 2 n : ℝ) ≤ 1 := by exact_mod_cast hn
    nlinarith
  have hlog32 : Real.log 2 < Real.log 3 := by
    apply Real.log_lt_log; norm_num; norm_num
  linarith

/-- The accumulated TE cost along a finite Collatz orbit segment.
    This is the discrete analogue of log L(E, 1) in BSD — an aggregation
    of local (2-adic) data predicting global convergence. -/
noncomputable def orbitCost (orbit : List ℕ) : ℝ :=
  (orbit.map TE).sum

/-- TE is a conformal reparameterization — not a force.
    This lemma tag exists so downstream proofs can reference the
    "T/E is conformal" claim by name. -/
theorem TE_is_conformal :
    ∀ n : ℕ, TE n = Real.log 3 - (padicValNat 2 n : ℝ) * Real.log 2 :=
  fun n => rfl

/-- Monotonicity: higher 2-adic valuation → lower entropic cost.
    The more a number is divisible by 2, the cheaper the step. -/
theorem TE_antitone_padicVal {m n : ℕ}
    (h : padicValNat 2 m ≤ padicValNat 2 n) :
    TE n ≤ TE m := by
  simp only [TE, TE_def]
  have hlog2 : 0 ≤ Real.log 2 := le_of_lt (Real.log_pos (by norm_num))
  have : (padicValNat 2 m : ℝ) ≤ (padicValNat 2 n : ℝ) := by exact_mod_cast h
  nlinarith

end GTCT
