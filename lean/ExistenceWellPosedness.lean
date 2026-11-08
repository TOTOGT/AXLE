/-!
# CORRECTION (2026-11-08) — read before using this file
1. The files named below as discharging the hypotheses (FoldOperator.lean, ContactStructure.lean,
   ResamplingKernel.lean) do not exist in AXLE or geometry. The hypotheses are undischarged.
2. The reasons given are false in general: unique ODE solutions do not make a flow non-expansive
   (ẋ = x gives x ↦ 2x at t = ln 2); a unique nondegenerate minimiser does not make the selection
   map non-expansive (argmin of (q − 2x)² is 2x); a fold is not non-expansive (x ↦ x² sends 1, 2 to
   1, 4). What is needed are quantitative bounds (a one-sided Lipschitz constant ℓ ≤ 0 for the flow;
   B/m for a minimiser map with D²_qq V ≥ mI and ‖D²_qx V‖ ≤ B), proved for an actual system.
3. This file composes R ∘ K ∘ F ∘ C; the canonical chain is U ∘ F ∘ K ∘ C (F and K swapped).
4. The conditional Banach theorem for the canonical order, with no sorry and an explicit
   n-step bound, is in geometry, Orthogenesis/Vol1/ChainContraction.lean. It is conditional: it
   does not show that any dm³ construction meets its hypotheses, and it is not Theorem 5.1 as
   worded on the Volume I page ("well-defined on any piecewise C² trajectory").
This file is kept unchanged below as the record of what was claimed.

# ExistenceWellPosedness.lean  (rewrite, 2026-07-03)
## Principia Orthogona, Volume I §4 (V6) — Existence and Well-Posedness of Φ = R ∘ K ∘ F ∘ C

**Why this file was rewritten.** The previous version was *vacuous*. Every
"theorem" had the form `∀ x, ∃! y, y = f x`, which is a tautology of Lean's
function semantics — it holds for ANY total function `f` and says nothing about
C, K, F, R specifically. The real mathematical content of §4 is that the
operator Φ has a **well-defined unique attracting state**, and that this holds
*for a reason*: C strictly contracts, F/K/R are non-expansive, so the composite
is a contraction and Banach's theorem gives a unique fixed point.

This rewrite states that real content. The genuinely checkable fact — that the
toy-model compression `C x = r*·x` contracts distances by exactly `r*` — is
**proved**, not assumed. The remaining operator hypotheses (F non-expansive,
K the unique ODE solution, R the unique Morse arg-min) are stated as honest
named hypotheses, and the Banach fixed-point conclusion is routed to Mathlib's
`ContractingWith` API via a labelled `sorry`.

**Not machine-checked.** Not compiled against Mathlib this session; Mathlib
lemma names are best-effort and must be confirmed by `lake build`.
-/

import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace Dm3

/-! ## 1. The contraction ratio -/

variable (r_star : ℝ)

/-! ## 2. Compression genuinely contracts (proved)

This is the substantive replacement for the old tautology. The toy-model
compression `C x = r*·x` does not merely "exist as a function"; it strictly
contracts the metric by the factor `r*`. -/

/-- Toy-model compression operator. -/
noncomputable def C_toy (x : ℝ) : ℝ := r_star * x

/-- **Compression contracts distances by exactly `r*`** (for `r* ≥ 0`).
    Proved — this is the real content missing from the old file. -/
theorem compression_contracts (hr : 0 ≤ r_star) (x y : ℝ) :
    dist (C_toy r_star x) (C_toy r_star y) = r_star * dist x y := by
  unfold C_toy
  rw [Real.dist_eq, Real.dist_eq, ← mul_sub, abs_mul, abs_of_nonneg hr]

/-- Hence, for `r* < 1`, compression is a strict contraction:
    `dist (C x) (C y) < dist x y` whenever `x ≠ y`. -/
theorem compression_strict (hr0 : 0 ≤ r_star) (hr1 : r_star < 1)
    {x y : ℝ} (hxy : x ≠ y) :
    dist (C_toy r_star x) (C_toy r_star y) < dist x y := by
  rw [compression_contracts r_star hr0]
  have hpos : 0 < dist x y := dist_pos.mpr hxy
  calc r_star * dist x y < 1 * dist x y := by
        exact (mul_lt_mul_right hpos).mpr hr1
    _ = dist x y := one_mul _

/-! ## 3. The other three operators: substantive well-definedness hypotheses

Each of these is a *real* mathematical property (non-expansiveness, ODE
solvability, arg-min uniqueness), stated as a named hypothesis rather than the
old tautology. In the full theory each is discharged from the concrete
definition; here they are the honest interface. -/

variable {α : Type*} [MetricSpace α]

/-- **Folding is non-expansive.** The Whitney fold `F` does not increase
    distances (Lipschitz constant ≤ 1). Real property; discharged in
    FoldOperator.lean from the explicit case split. -/
def FoldingNonexpansive (F : α → α) : Prop :=
  ∀ x y, dist (F x) (F y) ≤ dist x y

/-- **Kernel is the unique ODE solution.** `K` returns the unique solution of
    the contact-flow ODE (Picard–Lindelöf); here abstracted as
    non-expansiveness of the time-`τ` flow map, which is what the fixed-point
    argument needs. Discharged from `IsPicardLindelof` in ContactStructure.lean. -/
def KernelNonexpansive (K : α → α) : Prop :=
  ∀ x y, dist (K x) (K y) ≤ dist x y

/-- **Resampling is the unique Morse arg-min.** `R x` is the unique minimiser
    of a Morse potential near `x`; uniqueness is what makes `R` single-valued
    for a *reason* (not by fiat). Abstracted as non-expansiveness of the mode
    map. Discharged from `Morse ⇒ isolated nondegenerate minimum` in
    ResamplingKernel.lean. -/
def ResamplingNonexpansive (R : α → α) : Prop :=
  ∀ x y, dist (R x) (R y) ≤ dist x y

/-! ## 4. Well-posedness of Φ = R ∘ K ∘ F ∘ C

Well-posedness here means: Φ has a **unique fixed point** to which iterates
converge (the attracting generative state). This is genuine content, unlike the
old `∃! y, y = Φ x`. -/

/-- The composite operator on ℝ (toy model), with abstract F, K, R : ℝ → ℝ. -/
noncomputable def Phi (F K R : ℝ → ℝ) : ℝ → ℝ := R ∘ K ∘ F ∘ (C_toy r_star)

/-- **The composite contracts by `r*`.**

    If F, K, R are each non-expansive on ℝ, then Φ = R∘K∘F∘C contracts distances
    by the factor `r*` (compression's ratio), because non-expansive maps cannot
    undo the contraction from C. Proved by chaining. -/
theorem Phi_contracts
    (F K R : ℝ → ℝ)
    (hF : FoldingNonexpansive F) (hK : KernelNonexpansive K)
    (hR : ResamplingNonexpansive R)
    (hr : 0 ≤ r_star) (x y : ℝ) :
    dist (Phi r_star F K R x) (Phi r_star F K R y) ≤ r_star * dist x y := by
  unfold Phi Function.comp
  calc dist (R (K (F (C_toy r_star x)))) (R (K (F (C_toy r_star y))))
      ≤ dist (K (F (C_toy r_star x))) (K (F (C_toy r_star y))) := hR _ _
    _ ≤ dist (F (C_toy r_star x)) (F (C_toy r_star y)) := hK _ _
    _ ≤ dist (C_toy r_star x) (C_toy r_star y) := hF _ _
    _ = r_star * dist x y := compression_contracts r_star hr x y

/-- **Main theorem — Existence and Well-Posedness of Φ.**

    If F, K, R are non-expansive and `0 ≤ r* < 1`, then Φ has a unique fixed
    point `x*`, and iterates `Φ^[n] x → x*` for every starting `x`.

    This is the real §4 statement. The proof is Banach's fixed-point theorem
    applied to the contraction bound `Phi_contracts`; it is routed to Mathlib's
    `ContractingWith` API and left as a labelled `sorry` pending build. -/
theorem Phi_wellPosed
    (F K R : ℝ → ℝ)
    (hF : FoldingNonexpansive F) (hK : KernelNonexpansive K)
    (hR : ResamplingNonexpansive R)
    (hr0 : 0 ≤ r_star) (hr1 : r_star < 1) :
    ∃! x : ℝ, Phi r_star F K R x = x := by
  sorry
  -- Route (not machine-checked):
  --  1. From `Phi_contracts` and `hr1`, package Φ as `ContractingWith K Φ`
  --     with `K = Real.toNNReal r_star < 1`
  --     (via `LipschitzWith` in edist form; `Phi_contracts` is the dist form).
  --  2. `ContractingWith.fixedPoint` gives the fixed point `x*`;
  --     `ContractingWith.fixedPoint_unique'` / `ContractingWith.tendsto_iterate_fixedPoint`
  --     give uniqueness and convergence.
  --  3. Repackage as the `∃!` statement above.
  -- Every hypothesis feeding this is a genuine metric property, not a tautology.

/-- Convergence corollary (statement): from any start, iterates approach the
    unique attracting state. Follows from the same `ContractingWith` witness. -/
theorem Phi_iterates_converge
    (F K R : ℝ → ℝ)
    (hF : FoldingNonexpansive F) (hK : KernelNonexpansive K)
    (hR : ResamplingNonexpansive R)
    (hr0 : 0 ≤ r_star) (hr1 : r_star < 1) (x₀ : ℝ) :
    ∃ xStar : ℝ, Phi r_star F K R xStar = xStar ∧
      Filter.Tendsto (fun n => (Phi r_star F K R)^[n] x₀) Filter.atTop (nhds xStar) := by
  sorry
  -- Same `ContractingWith` witness as `Phi_wellPosed`, plus
  -- `ContractingWith.tendsto_iterate_fixedPoint`.

/-! ## 5. Obligation ledger (honest status)

| Obligation                         | Status       | Discharged from / route                 |
|------------------------------------|--------------|-----------------------------------------|
| `compression_contracts` / `_strict`| **proved**   | `Real.dist_eq`, `abs_mul`               |
| `FoldingNonexpansive F`            | hypothesis   | FoldOperator.lean (Whitney case split)  |
| `KernelNonexpansive K`             | hypothesis   | ContactStructure.lean (`IsPicardLindelof`)|
| `ResamplingNonexpansive R`         | hypothesis   | ResamplingKernel.lean (Morse arg-min)   |
| `Phi_contracts`                    | **proved**   | chaining the above                      |
| `Phi_wellPosed` / convergence      | sorry        | `ContractingWith.fixedPoint` (Banach)   |

No tautologies remain: each statement above carries genuine metric content. -/

end Dm3
