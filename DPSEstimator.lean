/-
  DPSEstimator.lean — the estimator behind WP-36, formalized
  ===========================================================
  G6 LLC · Principia Orthogona · MIT License

  ⚠ VERIFICATION STATUS: **UNVERIFIED — kernel check not yet run.**

  This file was written where no Lean toolchain was available, so no one has
  watched it compile. Per the corpus rule (no claim moves to VERIFIED without
  a kernel check you watched come back clean), it is tagged UNVERIFIED and must
  stay so until someone runs:

      lake env lean DPSEstimator.lean          -- expect: no errors
      # then, appended to the file or in a scratch:
      #print axioms transfer_headline_conservative
      -- expect: [propext, Classical.choice, Quot.sound]   (no sorryAx)

  Only after that output is observed may WP-36 describe this as verified.

  ---------------------------------------------------------------------------
  WHAT IS AND IS NOT FORMALIZED

  NOT formalized, and not formalizable: whether duplicate provisioning is
  common, what the prevalence is, what anyone spends. Those are empirical and
  belong to the survey. Formalizing them would be theatre.

  Formalized here: that the *reporting rule* cannot overstate. WP-36 commits in
  advance to publishing two prevalence estimates — one from stated attribution,
  one from a revealed-preference tradeoff — and leading with the lower. The
  theorems below establish that this rule yields a transfer figure that is a
  lower bound on both candidate figures, and that the published number is
  monotone and well-posed. That is a claim about arithmetic, and arithmetic is
  what a kernel can settle.

  In short: the kernel cannot tell you the number is true. It can tell you the
  procedure cannot inflate it.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Order.MinMax
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

namespace DPS

/-! ## Prevalence -/

/-- A prevalence is a proportion: a real in `[0,1]`. -/
structure Prevalence where
  val    : ℝ
  nonneg : 0 ≤ val
  le_one : val ≤ 1

namespace Prevalence

/-- The pointwise minimum of two prevalences is a prevalence. -/
def min' (p q : Prevalence) : Prevalence where
  val    := min p.val q.val
  nonneg := le_min p.nonneg q.nonneg
  le_one := le_trans (min_le_left _ _) p.le_one

end Prevalence

/-! ## The transfer estimator -/

/-- Annual incremental spend attributable to duplicate provisioning:
    `prevalence × monthly incremental spend × 12 × population`. -/
noncomputable def transfer (p incrMonthly pop : ℝ) : ℝ :=
  p * incrMonthly * 12 * pop

/-- The estimate is non-negative on non-negative inputs. -/
theorem transfer_nonneg {p incr pop : ℝ}
    (hp : 0 ≤ p) (hi : 0 ≤ incr) (hpop : 0 ≤ pop) :
    0 ≤ transfer p incr pop := by
  unfold transfer
  have h12 : (0:ℝ) ≤ 12 := by norm_num
  exact mul_nonneg (mul_nonneg (mul_nonneg hp hi) h12) hpop

/-- The estimate is monotone in prevalence. This is the property that makes
    "lead with the lower prevalence" equivalent to "publish the smaller
    transfer" — without it the reporting rule would not do what it claims. -/
theorem transfer_mono {p q incr pop : ℝ}
    (h : p ≤ q) (hi : 0 ≤ incr) (hpop : 0 ≤ pop) :
    transfer p incr pop ≤ transfer q incr pop := by
  unfold transfer
  have h1 : p * incr ≤ q * incr := mul_le_mul_of_nonneg_right h hi
  have h2 : p * incr * 12 ≤ q * incr * 12 :=
    mul_le_mul_of_nonneg_right h1 (by norm_num)
  exact mul_le_mul_of_nonneg_right h2 hpop

/-! ## The reporting rule -/

/-- The rule fixed in advance in WP-36 §8: publish both estimates, lead with
    the lower. -/
noncomputable def headline (stated revealed : ℝ) : ℝ := min stated revealed

theorem headline_le_stated (s r : ℝ) : headline s r ≤ s := min_le_left s r

theorem headline_le_revealed (s r : ℝ) : headline s r ≤ r := min_le_right s r

/-- **Conservatism.** The published transfer never exceeds either candidate
    estimate. This is the whole point: the procedure is incapable of producing
    a figure larger than the evidence supports, whichever estimate one prefers.

    It does not say the number is correct. It says the reporting rule cannot be
    the source of an overstatement. -/
theorem transfer_headline_conservative
    (s r incr pop : ℝ) (hi : 0 ≤ incr) (hpop : 0 ≤ pop) :
    transfer (headline s r) incr pop ≤ transfer s incr pop ∧
    transfer (headline s r) incr pop ≤ transfer r incr pop :=
  ⟨transfer_mono (headline_le_stated s r) hi hpop,
   transfer_mono (headline_le_revealed s r) hi hpop⟩

/-- The headline prevalence remains a valid proportion. -/
theorem headline_mem_unit_interval
    {s r : ℝ} (hs : 0 ≤ s) (hr : 0 ≤ r) (hs1 : s ≤ 1) :
    0 ≤ headline s r ∧ headline s r ≤ 1 :=
  ⟨le_min hs hr, le_trans (min_le_left s r) hs1⟩

/-! ## Incremental spend -/

/-- Incremental spend is total subscription spend minus the cost of a single
    subscription — never the full multi-subscription bill, which would
    overstate by counting spend the user would have incurred anyway. -/
noncomputable def incremental (total single : ℝ) : ℝ := total - single

/-- Incremental spend is non-negative exactly when total spend is at least the
    cost of one subscription — the condition that holds whenever the respondent
    holds at least one. -/
theorem incremental_nonneg {total single : ℝ} (h : single ≤ total) :
    0 ≤ incremental total single := by
  unfold incremental; linarith

/-- Using incremental rather than total spend is itself conservative. -/
theorem incremental_le_total {total single : ℝ} (h : 0 ≤ single) :
    incremental total single ≤ total := by
  unfold incremental; linarith

/-- Composing both conservatism results: the published figure is bounded above
    by the naive figure (higher prevalence estimate × total spend). This is the
    formal content of "we cannot have inflated it by construction." -/
theorem published_le_naive
    (s r total single pop : ℝ)
    (hs : 0 ≤ s) (hsingle : 0 ≤ single) (htot : 0 ≤ total) (hpop : 0 ≤ pop) :
    transfer (headline s r) (incremental total single) pop
      ≤ transfer s total pop := by
  have h1 : transfer (headline s r) (incremental total single) pop
          ≤ transfer s (incremental total single) pop :=
    transfer_mono (headline_le_stated s r)
      (by unfold incremental; linarith) hpop
  have h2 : transfer s (incremental total single) pop ≤ transfer s total pop := by
    unfold transfer incremental
    have hstep : s * (total - single) ≤ s * total := by nlinarith [hs, hsingle]
    nlinarith [hstep, hpop, hs, htot]
  exact le_trans h1 h2

end DPS

/-
  ---------------------------------------------------------------------------
  NOTE ON `published_le_naive`

  `0 ≤ s` is an explicit hypothesis, not an assumption smuggled into a tactic:
  the theorem is true only for non-negative prevalence, and a negative
  prevalence is meaningless. Stated rather than hidden.

  ---------------------------------------------------------------------------
  CLAIM TAGS (WP-36 §8)

  [MODEL]  the estimator's algebraic form
  [OPEN]   every empirical quantity: prevalence, incremental spend, population
  [OPEN]   this file's own verification, until the kernel says otherwise
-/
