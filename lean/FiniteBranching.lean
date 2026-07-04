/-!
# FiniteBranching.lean  (kept, 2026-07-03)
## Principia Orthogona, Volume I §5 (V6) — Finite Branching on Compact Intervals

**Status: kept unchanged as the reference honest pattern.** The 2026-07-03 audit
found this file to be the one of the five that was already correct in form:
three explicit, clearly-labelled `sorry`s with a plausible Mathlib route, honestly
incomplete rather than falsely complete or silently wrong. The other four files
were rewritten to match *this* file's discipline. Only this header note was added.

**Mathematical argument.**

Let `g : ℝ → ℝ` be the branching-indicator function of the generative contact
manifold (the function whose zeros are exactly the branching points). Assume:
  1. `g` is real-analytic on an open neighbourhood of `[a, b]`.
  2. `g` is not identically zero on `[a, b]`.

Then by the *isolated zeros theorem* for real-analytic functions, each zero of `g`
in `[a, b]` is isolated. A closed subset of a compact space in which every point is
isolated is finite. Therefore the set of branching points in `[a, b]` is finite.

**Not machine-checked.** Not compiled against Mathlib this session. Note also that
recent Mathlib renamed `AnalyticOn` to `AnalyticOnNhds`; confirm the current name
by `lake build` before trusting the import/lemma references below.
-/

import Mathlib.Analysis.Analytic.Basic
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Topology.Algebra.Order.Compact
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Order.Filter.Basic

namespace Dm3

open Set Filter Topology

/-! ## 1. Abstract finite-branching theorem -/

/-- **Isolated-zeros lemma (real-analytic case).**

    If `g : ℝ → ℝ` is analytic on an open set `U` containing `[a,b]`, and `g ≢ 0`
    on any connected component of `U`, then every zero of `g` in `[a,b]` is isolated.

    sorry closes when:
    · `AnalyticOn.eq_zero_of_frequently_zero` (or the `AnalyticOnNhds` renamed form)
      from `Mathlib.Analysis.Analytic.IsolatedZeros` is invoked with the hypothesis
      that `g` is not identically zero, yielding `¬ AccumulationPoint (g ⁻¹' {0}) x`
      for each `x` in `g ⁻¹' {0} ∩ [a,b]`. -/
lemma analytic_zeros_isolated
    {U : Set ℝ} (hU : IsOpen U)
    (g : ℝ → ℝ) (hg : AnalyticOn ℝ g U)
    (hg_ne : ¬ ∀ x ∈ U, g x = 0) :
    ∀ x ∈ U ∩ g ⁻¹' {0},
      ∃ ε > 0, ∀ y ∈ Metric.ball x ε, y ≠ x → g y ≠ 0 := by
  sorry
  -- Mathlib route:
  -- `AnalyticOn.eq_zero_of_frequently_zero` states:
  --   if g is analytic on a preconnected open set and has a point x where
  --   g x = 0 and x is a limit of zeros, then g ≡ 0.
  -- Contrapositive: g ≢ 0 → every zero is isolated.
  -- This requires: `hg.eq_zero_of_frequently_zero` (preconnected U)
  -- and converting the contrapositive to the ε-witness form above.

/-- **Discrete-closed-in-compact is finite.**

    A subset `S` of a compact space `K` that is both closed and has the discrete
    subspace topology (every point is isolated) is finite.

    sorry closes when:
    · This is assembled from:
        `IsCompact.finite_cover_nhds` : ∃ finite subcover of any open cover of K
        + the fact that isolatedness of each point gives an open cover of S by
          singletons, which pulls back to a finite subcover of K ∩ S.
    · Alternatively, in Mathlib4 `Set.Countable.finite` can be combined with
      `AnalyticOn`'s `countable_zeros` result (if available for ℝ) to give
      countability, then compactness gives finiteness.
    · The cleanest available Mathlib lemma may be:
        `IsCompact.finite` applied to a set that is compact (closed in compact) and
        has `DiscreteTopology` on the subtype. -/
lemma discrete_closed_in_compact_finite
    {K : Set ℝ} (hK : IsCompact K)
    {S : Set ℝ} (hSK : S ⊆ K) (hS_closed : IsClosed S)
    (hS_discrete : ∀ x ∈ S, ∃ ε > 0, S ∩ Metric.ball x ε = {x}) :
    S.Finite := by
  sorry
  -- Mathlib route:
  -- 1. hS_closed + hK gives IsCompact S  [IsCompact.of_isClosed_subset]
  -- 2. hS_discrete gives DiscreteTopology on S as a subtype
  -- 3. IsCompact + DiscreteTopology → Finite  [IsCompact.finite or
  --    finite_of_compact_of_discrete, which is in Mathlib as
  --    `Finite.of_compact_of_discrete` after importing
  --    Mathlib.Topology.Algebra.Order.Compact]

/-! ## 2. Main finite-branching theorem -/

/-- **Finite Branching Theorem.**

    On any compact interval `[a, b]`, the set of branching points of the
    generative contact manifold is finite.

    `g` is the branching-indicator function: a zero of `g` at `x` means
    the manifold branches at state `x`.

    Proof: combine `analytic_zeros_isolated` (zeros are isolated) with
    `discrete_closed_in_compact_finite` (isolated closed ⊆ compact is finite).

    sorry closes when both helper lemmas above are proved. -/
theorem finiteBranching
    {a b : ℝ} (hab : a < b)
    (g : ℝ → ℝ)
    (U : Set ℝ) (hU : IsOpen U) (hIab : Set.Icc a b ⊆ U)
    (hg : AnalyticOn ℝ g U)
    (hg_ne : ¬ ∀ x ∈ U, g x = 0) :
    (g ⁻¹' {0} ∩ Set.Icc a b).Finite := by
  sorry
  -- Proof outline (once helper lemmas are proved):
  -- let S := g ⁻¹' {0} ∩ Icc a b
  -- Step 1: S ⊆ Icc a b ⊆ U  [by hIab]
  -- Step 2: each point of S is isolated in S  [analytic_zeros_isolated]
  -- Step 3: S is closed  [IsClosed.inter (isClosed_singleton.preimage hg.continuous) isClosed_Icc]
  -- Step 4: Icc a b is compact  [isCompact_Icc]
  -- Step 5: S ⊆ compact + S closed → S compact  [IsCompact.of_isClosed_subset]
  -- Step 6: S compact + S discrete → S finite  [discrete_closed_in_compact_finite]

/-! ## 3. Corollary: branching points are enumerable

    A finite set has a surjection from Fin n for some n : ℕ.
    This is the form needed by the transition-counting argument in Volume I. -/

/-- The branching points in `[a, b]` can be indexed by a finite type. -/
noncomputable def branchingIndex
    {a b : ℝ} (hab : a < b)
    (g : ℝ → ℝ)
    (U : Set ℝ) (hU : IsOpen U) (hIab : Set.Icc a b ⊆ U)
    (hg : AnalyticOn ℝ g U)
    (hg_ne : ¬ ∀ x ∈ U, g x = 0) :
    { n : ℕ // ∃ f : Fin n → ℝ, Set.range f = g ⁻¹' {0} ∩ Set.Icc a b } := by
  have hfin := finiteBranching hab g U hU hIab hg hg_ne
  -- The finite set has cardinality n = hfin.toFinset.card.
  -- We need to exhibit a surjection Fin n → (g ⁻¹' {0} ∩ Icc a b).
  -- This is provided by Set.Finite.exists_surjOn (or similar) applied to hfin.
  -- sorry here because finiteBranching itself carries a sorry;
  -- once that sorry is closed, replace this sorry with:
  --   exact ⟨hfin.toFinset.card, (hfin.toFinset.equivFin).symm,
  --          by ext; simp [Set.Finite.mem_toFinset hfin]⟩
  sorry
  -- Mathlib lemma needed: `Set.Finite.surjOn_iff_exists_map_toFin` or
  -- `Finset.equivFin` + `Set.Finite.toFinset` coercion.

end Dm3
