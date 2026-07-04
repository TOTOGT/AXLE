/-!
# ContactHopf.lean  (rewrite, 2026-07-03)
## Principia Orthogona, Volume II §3 (V4) — Contact Hopf Coefficient Correction

**Why this file was rewritten.** The previous version explained the γ*
correction by inventing a geometric mechanism — "the Reeb-direction projection
of the Sasakian structure contributes a factor of 2." That mechanism is **not**
what the session found and is not in the hand computation. Asserting it would
have injected a *false mathematical claim* into the paper's Lean record under
the banner of a fix, which is worse than the original prose-only gap.

**What the correction actually is.** A plain algebra step in the linearization
of the Hopf term. Writing the term as `−2·(1 − y·e^(−z₀))` expands to
`2·y·e^(−z₀) − 2`, whereas the intended linearization is `y·e^(−z₀) − 2`.
The two differ by a factor of 2 on the `y·e^(−z₀)` coefficient. That algebraic
discrepancy — not any Reeb/Sasakian projection — is the origin of the factor 2.

**Reconciliation (RESOLVED and independently re-derived, 2026-07-03).** An
earlier draft flagged an apparent direction conflict: the Vol II V4 changelog
records `γ* : e^(z₀) → 2·e^(z₀)` (an *increase*), while the linearization slip
above, read as raw algebra, *removes* a spurious factor of 2 (a *decrease*).
There is no contradiction. Both are true simultaneously, at two different points
of the same derivation:

  · The **coefficient on γ** in the eigenvalue (zero-crossing) equation goes
    DOWN, from 2 (erroneous `2·γ·e^(−z₀) − 2`) to 1 (correct `γ·e^(−z₀) − 2`).
  · Solving each equation for its root `γ*` puts that coefficient in the
    DENOMINATOR (`γ* = 2·e^(z₀) / coefficient`), so the root goes UP:
        erroneous:  `2·γ·e^(−z₀) − 2 = 0  ⇒  γ* = e^(z₀)`
        correct:    `γ·e^(−z₀) − 2 = 0    ⇒  γ* = 2·e^(z₀)`.

So the changelog value (`γ* = 2·e^(z₀)`) and the raw-algebra "factor of 2
removed" reading are the SAME fix described at different stages — the coefficient
falls 2→1, and because it sits in the denominator of the root, `γ*` rises
`e^(z₀) → 2·e^(z₀)`. See CONTACTHOPF_RECONCILIATION.md for the full derivation.
The §2 lemmas below capture the coefficient step; §1 records the resulting root.

**Not machine-checked.** Not compiled against Mathlib this session.
-/

import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Topology.MetricSpace.Basic

namespace Dm3

open Real

/-! ## 1. The coefficient values -/

/-- The bifurcation base point `z₀ ∈ ℝ`. In the toy model `z₀ = log r*`. -/
variable (z₀ : ℝ)

/-- **Value used in V3 (superseded).** `γ*_old = exp z₀`. Retained only to
    state the correction relationship. -/
@[deprecated (since := "2026-07-03")]
noncomputable def gammaStar_old : ℝ := Real.exp z₀

/-- **Corrected coefficient value as recorded in the Vol II V4 changelog.**
    `γ* = 2·exp z₀`.

    NOTE: the *value* is the root of the corrected eigenvalue equation
    `γ·e^(−z₀) − 2 = 0`, i.e. `γ* = 2·e^(z₀)`. The factor of 2 comes from the
    linearization algebra in §2 (coefficient 2→1), NOT the Reeb-projection story
    from the previous version. See the resolved reconciliation in the header. -/
noncomputable def gammaStar : ℝ := 2 * Real.exp z₀

/-- Arithmetic relationship between the two recorded values (checkable). -/
@[simp]
theorem gammaStar_eq_two_mul_old : gammaStar z₀ = 2 * gammaStar_old z₀ := by
  simp [gammaStar, gammaStar_old]

theorem gammaStar_pos : 0 < gammaStar z₀ := by unfold gammaStar; positivity

theorem gammaStar_ne_zero : gammaStar z₀ ≠ 0 := ne_of_gt (gammaStar_pos z₀)

/-! ## 2. The actual algebraic origin of the factor of 2

The Hopf term, before linearization, involves `1 − y·e^(−z₀)`. The correction
concerns how this is linearized. The lemma below is a pure `ring` identity
exhibiting the erroneous expansion; it is the honest locus of the fix,
replacing the fabricated geometric mechanism. -/

/-- **Erroneous linearization (as an algebraic identity).**

    `−2·(1 − y·e^(−z₀)) = 2·y·e^(−z₀) − 2`.

    This is a true `ring` identity — the point is that the RIGHT-hand side
    carries a coefficient `2` on `y·e^(−z₀)`, which is the doubling that the
    correction is about. -/
theorem linearization_erroneous_expansion (y : ℝ) :
    -2 * (1 - y * Real.exp (-z₀)) = 2 * (y * Real.exp (-z₀)) - 2 := by ring

/-- **Intended linearization coefficient (as recorded in the session notes).**

    `y·e^(−z₀) − 2` — coefficient `1` on `y·e^(−z₀)`.

    Stated as a definition so downstream proofs reference the intended form
    rather than the erroneous expansion above. -/
noncomputable def linearizedHopfTerm (y : ℝ) : ℝ := y * Real.exp (-z₀) - 2

/-- The erroneous expansion and the intended term differ by exactly one extra
    copy of `y·e^(−z₀)` — i.e. by the factor-of-2 discrepancy (checkable). -/
theorem linearization_discrepancy (y : ℝ) :
    (2 * (y * Real.exp (-z₀)) - 2) - linearizedHopfTerm z₀ y = y * Real.exp (-z₀) := by
  unfold linearizedHopfTerm; ring

/-! ### The resolution, encoded as two proved root computations

These make the header reconciliation machine-statable: each γ* value is exactly
the root of its own eigenvalue equation. The coefficient falls 2→1; because it
sits in the denominator of the root, γ* rises `e^(z₀) → 2·e^(z₀)`. -/

/-- **Erroneous root.** `γ = e^(z₀)` solves the erroneous equation
    `2·γ·e^(−z₀) − 2 = 0`. Proved. -/
theorem erroneous_root_is_exp :
    2 * (Real.exp z₀ * Real.exp (-z₀)) - 2 = 0 := by
  rw [← Real.exp_add]; simp

/-- **Correct root.** `γ* = 2·e^(z₀)` solves the corrected equation
    `γ·e^(−z₀) − 2 = 0`, i.e. `linearizedHopfTerm z₀ (γ*) = 0`. Proved.
    This is the Lean witness that the changelog value and the corrected algebra
    agree. -/
theorem gammaStar_is_root : linearizedHopfTerm z₀ (gammaStar z₀) = 0 := by
  unfold linearizedHopfTerm gammaStar
  rw [mul_assoc, ← Real.exp_add]; simp

/-! ## 3. Contact Hopf normal form (corrected statement)

The full bifurcation statement. Its geometric content — reducing the contact
flow to a 2D normal form and reading off the limit-cycle radius — is a genuine
proof obligation, recorded as an honest `sorry` with a route, NOT closed by a
fabricated one-line justification. -/

/-- **Contact Hopf Bifurcation Theorem (statement).**

    For the contact-structure flow family `Γ_λ` with normal-form coefficient
    `γ*`, for small `λ > 0` a limit cycle of radius `≈ √(λ / γ*)` bifurcates
    from the fixed point.

    Obligations (both genuine, both `sorry`):
    · the reduction of the contact flow to the 2D Hopf normal form with
      coefficient `γ*` — the geometric core of Vol II §3;
    · the limit-cycle existence/uniqueness for that normal form (no general
      Hopf theorem in Mathlib yet; would be a bespoke `IsPicardLindelof`
      construction). -/
theorem contactHopf_bifurcation
    (hγ : gammaStar z₀ = 2 * Real.exp z₀)
    (lam : ℝ) (hlam : 0 < lam) :
    ∃ ρ : ℝ, 0 < ρ ∧ |ρ - Real.sqrt (lam / gammaStar z₀)| < lam := by
  sorry
  -- Route (not machine-checked):
  --  1. Reduce Γ_λ to the 2D Hopf normal form (Vol II §3 geometric computation).
  --  2. Apply the planar Hopf bifurcation result to obtain the limit cycle.
  --  3. Radius estimate ρ ≈ √(λ/γ*) via `Real.sqrt` monotonicity + error bound.
  -- The coefficient γ* enters at step 1; its value 2·e^(z₀) is the root of the
  -- corrected eigenvalue equation (reconciliation resolved in the header).

/-! ## 4. Theorem 3.4 citation (prose note)

Vol II V4 corrects the Theorem 3.4 citation from "Invariant 7.5" to
"Invariant 7.5, Companion Corollary 1". That corollary is the real
compression–folding sub-result; see Invariant75.lean, which no longer
formalizes a generic Lyapunov inequality in its place. No Lean statement is
asserted here beyond this cross-reference. -/

end Dm3
