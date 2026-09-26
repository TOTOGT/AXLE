/-
PositionalDominanceThreshold.lean

UPDATED against `Grossi_2026_Positional_Dominance_v2.pdf` (v2, DOI 10.5281/zenodo.21753025,
supersedes v1 10.5281/zenodo.21013066).

v2's own version note retracts the exact claim this file originally formalized. v1 Section 3
stated Delta_V(sigma) ~ a*sigma^2 - b (quadratic, no linear term); v1 Appendix A separately
derived a linear-only form. v2 Section 3.1 shows both were partial truncations of the paper's
own value-function ansatz Vi(s) ~ alpha_i + beta_i*|IA-IB| + gamma_i*sigma^2, whose correct
term-by-term difference is

    Delta_V(sigma) = a*sigma^2 + m*sigma - b        (a, m, b > 0 under the calibrated model)

-- a FULL quadratic with a linear term m that v1 dropped. v2's Proposition 1' (replacing v1's
Proposition 1) gives the corrected root

    sigma* = (-m + sqrt(m^2 + 4*a*b)) / (2*a)

proved unique via Descartes' rule of signs (exactly one sign change in the coefficient
sequence (a, m, -b)), and v2 states explicitly that setting m = 0 recovers v1's sqrt(b/a),
and that since m > 0 the true root is STRICTLY BELOW sqrt(b/a) -- v1's analytical value is an
upper bound, not an approximation. v2 also withdraws the correction factor psi ~ 0.50 as an
attribution: the gap between 0.665 and 0.33 is now attributed to the omitted linear term
itself, pending the direct measurement of m described in v2 Section 3.3.

Hand-derivation for `valueGapFull_sign`'s factoring (done before writing the Lean, per this
corpus's standing rule): given a*sigmastar^2 + m*sigmastar - b = 0, i.e.
a*sigmastar^2 + m*sigmastar = b, expand (sigma-sigmastar)*(a*(sigma+sigmastar)+m):

  = a*sigma^2 + a*sigma*sigmastar + m*sigma - a*sigma*sigmastar - a*sigmastar^2 - m*sigmastar
  = a*sigma^2 + m*sigma - (a*sigmastar^2 + m*sigmastar)
  = a*sigma^2 + m*sigma - b

which is exactly the value gap. Unlike the old m=0 file, only ONE factor's sign needs casing
(a*(sigma+sigmastar)+m is strictly positive whenever a>0, m>0, sigma,sigmastar>=0 -- the m>0
term alone guarantees this), so the sign-reversal argument is actually simpler than the
retracted special case below.

Hand-derivation for `sigmaStarFull_exists` (quadratic formula, checked by hand against v2's
closed form): let D = m^2+4ab, s = sqrt(D). Since a,b>0, D > m^2, and since s,m >= 0 with
D > m^2 this gives s > m, so sigmastar = (s-m)/(2a) >= 0 (in fact > 0). For the threshold
equation, multiply through by (2a)^2: a*(s-m)^2 + 2am(s-m) - 4a^2 b
  = a[(s-m)^2 + 2m(s-m)] - 4a^2 b = a(s-m)(s+m) - 4a^2 b = a(s^2-m^2) - 4a^2 b.
Using s^2 = D = m^2+4ab: = a*m^2 + 4a^2 b - a*m^2 - 4a^2 b = 0. Confirmed by hand.

NOT done here (same scope discipline as before): v2's Theorem 3.0/3.0.1 result -- existence
and uniqueness of sigma* for the actual equilibrium value functions, WITHOUT the ansatz, via
IVT (Lemma 3.2-3.4) and a Bellman convexity-preservation argument (Lemma 3.5-3.6) under
condition (C) -- is substantially harder (needs a formalized Bellman contraction operator,
Berge's theorem, convexity-of-fixed-point argument) and is not attempted here. Also not
touched: MPE existence itself (Fink 1964 / Takahashi 1964), the numerical calibration, the
identification test of Section 3.3, and the "recurrent 1/3" companion note -- whose own
cross-domain evidence table v2 now downgrades for the same reason this corpus's own theorems
get checked (see v2 Appendix A.1/A.2: the four cited Lean theorems are `rfl`-definitional or
vacuous with respect to the value 1/3, not derivations of it).

KERNEL RUN 2026-09-26: `lake env lean` against AXLE (Lean v4.14.0, Mathlib v4.14.0):
no errors, no sorry, two unused-variable warnings (`hb`, lines 87 and 128). The note below was written before that run and is kept as written.

UNTESTED: no local Lean/Mathlib toolchain in this environment. `valueGapFull_sign` is checked
by hand above and structurally simpler than the retracted version below, so it is the lower-
risk theorem. `sigmaStarFull_exists`'s existence proof (the `hs_gt_m` step deriving s > m from
s^2 > m^2, and the final cleared-denominator identity) is the highest-risk spot -- the exact
Mathlib lemma names for sqrt monotonicity and the `linear_combination` coefficient after
`field_simp` are both guesses pending a real `lake env lean` run. Report the actual output and
this gets corrected against that, not guessed at further from here.
-/

-- Mathlib.Algebra.Order.Ring.Lemmas does not exist at the pinned Mathlib (v4.14.0);
-- that was the "object file ... does not exist" error. Replaced with the tactic
-- modules this file actually uses.
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace PositionalDominance

/-! ### Retracted special case (m = 0), kept for reference only

v2 states explicitly that setting `m = 0` in the corrected ansatz recovers v1's `sqrt(b/a)`,
and that the true root is strictly below it once `m > 0`. The two theorems below are the
original formalization of v1's Proposition 1 -- they remain mathematically TRUE statements
about the `m = 0` degenerate case, but v1's Proposition 1 itself is retracted by v2 as the
paper's derivation of `Delta_V`. Do not cite these as formalizing the paper's current claim;
see `valueGapFull_sign` / `sigmaStarFull_exists` below for v2's Proposition 1'. -/

theorem valueGap_sign (a b σstar : ℝ) (ha : 0 < a) (hb : 0 < b) (hσstar : 0 ≤ σstar)
    (hthresh : a * σstar ^ 2 = b) (σ : ℝ) (hσ : 0 ≤ σ) :
    (σ > σstar → a * σ ^ 2 - b > 0) ∧
    (σ < σstar → a * σ ^ 2 - b < 0) ∧
    (σ = σstar → a * σ ^ 2 - b = 0) := by
  have hfactor : a * σ ^ 2 - b = a * (σ - σstar) * (σ + σstar) := by
    rw [← hthresh]; ring
  refine ⟨?_, ?_, ?_⟩
  · intro hgt
    rw [hfactor]
    have h1 : 0 < σ - σstar := sub_pos.mpr hgt
    have h2 : 0 < σ + σstar := by linarith
    exact mul_pos (mul_pos ha h1) h2
  · intro hlt
    rw [hfactor]
    have h1 : σ - σstar < 0 := sub_neg.mpr hlt
    have h2 : 0 < σ + σstar := by linarith
    have hneg1 : a * (σ - σstar) < 0 := mul_neg_of_pos_of_neg ha h1
    exact mul_neg_of_neg_of_pos hneg1 h2
  · intro heq
    rw [hfactor, heq]; ring

theorem sigmaStar_exists (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    0 ≤ Real.sqrt (b / a) ∧ a * (Real.sqrt (b / a)) ^ 2 = b := by
  have hba : 0 ≤ b / a := le_of_lt (div_pos hb ha)
  refine ⟨Real.sqrt_nonneg _, ?_⟩
  rw [Real.sq_sqrt hba]
  field_simp

/-! ### v2 Proposition 1' -- the corrected claim

`Delta_V(sigma) = a*sigma^2 + m*sigma - b`, with `a, m, b > 0`. This is what v2 actually
derives from the paper's own value-function ansatz (Section 3.1), replacing v1's Proposition 1
above. -/

/-- **Sign-reversal, corrected (v2 Proposition 1').** Given `a, m, b > 0` and a candidate
threshold `σstar ≥ 0` with `a*σstar^2 + m*σstar - b = 0`, the full value gap
`a*σ^2 + m*σ - b` is positive above the threshold, negative below it, zero exactly at it, for
every nonnegative `σ`. Only one factor needs sign-casing here (`a*(σ+σstar)+m` is always
strictly positive given `a,m > 0` and `σ,σstar ≥ 0`), unlike the retracted `m = 0` case above
which needed both factors cased. -/
theorem valueGapFull_sign (a m b σstar : ℝ) (ha : 0 < a) (hm : 0 < m) (hb : 0 < b)
    (hσstar : 0 ≤ σstar) (hthresh : a * σstar ^ 2 + m * σstar - b = 0) (σ : ℝ) (hσ : 0 ≤ σ) :
    (σ > σstar → a * σ ^ 2 + m * σ - b > 0) ∧
    (σ < σstar → a * σ ^ 2 + m * σ - b < 0) ∧
    (σ = σstar → a * σ ^ 2 + m * σ - b = 0) := by
  have hthresh' : a * σstar ^ 2 + m * σstar = b := by linarith
  have hfactor : a * σ ^ 2 + m * σ - b = (σ - σstar) * (a * (σ + σstar) + m) := by
    rw [← hthresh']; ring
  have hpos2 : 0 < a * (σ + σstar) + m := by
    have : 0 ≤ a * (σ + σstar) := mul_nonneg ha.le (by linarith)
    linarith
  refine ⟨?_, ?_, ?_⟩
  · intro hgt
    rw [hfactor]
    exact mul_pos (sub_pos.mpr hgt) hpos2
  · intro hlt
    rw [hfactor]
    exact mul_neg_of_neg_of_pos (sub_neg.mpr hlt) hpos2
  · intro heq
    rw [hfactor, heq]; ring

/-- **Existence, corrected (v2 Proposition 1').** `σstar = (-m + sqrt(m^2+4ab)) / (2a)` really
does satisfy `valueGapFull_sign`'s hypothesis, matching v2's closed form for the corrected
root. Highest-risk theorem in this file (see file docstring): the `hs_gt_m` step and the final
`linear_combination` coefficient are hand-derived but not kernel-checked. -/
theorem sigmaStarFull_exists (a m b : ℝ) (ha : 0 < a) (hm : 0 < m) (hb : 0 < b) :
    0 ≤ (-m + Real.sqrt (m ^ 2 + 4 * a * b)) / (2 * a) ∧
    a * ((-m + Real.sqrt (m ^ 2 + 4 * a * b)) / (2 * a)) ^ 2 +
      m * ((-m + Real.sqrt (m ^ 2 + 4 * a * b)) / (2 * a)) - b = 0 := by
  set D := m ^ 2 + 4 * a * b with hD_def
  set s := Real.sqrt D with hs_def
  have hD_nonneg : 0 ≤ D := by positivity
  have hs_nonneg : 0 ≤ s := Real.sqrt_nonneg _
  have hs_sq : s ^ 2 = D := Real.sq_sqrt hD_nonneg
  have hs_gt_m : m < s := by
    nlinarith [hs_sq, hs_nonneg, sq_nonneg (s - m), sq_nonneg (s + m)]
  have ha' : a ≠ 0 := ha.ne'
  -- `positivity` cannot see 0 ≤ -m + s (it needs hs_gt_m), so give the pieces directly.
  refine ⟨div_nonneg (by linarith) (by linarith), ?_⟩
  have key : a * ((-m + s) / (2 * a)) ^ 2 + m * ((-m + s) / (2 * a)) - b = 0 := by
    field_simp
    nlinarith [hs_sq, hD_def]
  linarith [key]

end PositionalDominance
