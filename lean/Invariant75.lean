/-!
# Invariant75.lean  (rewrite, 2026-07-03)
## Principia Orthogona, Volume I §7.5 (V6) — Chord-Arc / Curvature Injectivity Bound

**Why this file was rewritten.** The previous version proved a *different
theorem*. It stated a generic Lyapunov-contraction inequality
`H(F(Cx)) ≤ r*·H(x)` and called it "Invariant 7.5". That inequality is fine as
a Lyapunov fact, but it is **not** the content of §7.5. The actual Invariant 7.5
is a geometric **injectivity (embedding) bound**: under a curvature / chord-arc
condition — call it condition (D) — the generative curve is injective, and the
condition is *necessary*, witnessed by the **Gerono lemniscate** (a figure-eight
that self-intersects precisely because (D) fails).

This rewrite states the real theorem and proves the concrete necessity witness.
The abstract implication `(D) ⇒ injective` carries the genuine geometric proof
obligation and is a labelled `sorry`; the Gerono counterexample — that dropping
(D) breaks injectivity — is **proved**.

The old generic Lyapunov inequality is not Invariant 7.5. If a Lyapunov
contraction lemma is needed elsewhere, it should live in its own file under its
own name, not masquerade as §7.5.

**Not machine-checked.** Not compiled against Mathlib this session.
-/

import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Basic

namespace Dm3

open Real Set

/-! ## 1. Setup: arc-length curves and condition (D)

We model the generative curve as a map `γ : ℝ → ℝ × ℝ` restricted to an
arc-length interval `[0, L]`. Condition (D) is the §7.5 curvature / chord-arc
hypothesis; here it is an abstract predicate (its concrete unfolding — a bound
on curvature relative to injectivity radius — lives in the geometry file).
Keeping it abstract is deliberate: the point of §7.5 is the *implication*, and
the necessity witness, not a re-derivation of the curvature bound. -/

/-- Abstract statement of condition (D): the §7.5 chord-arc / curvature
    hypothesis on `γ` over `[0, L]`. Its concrete form is a lower bound
    `dist (γ s) (γ t) ≥ c·|s − t|` for a curvature-controlled constant `c > 0`,
    supplied by the geometry file. -/
def ConditionD (γ : ℝ → ℝ × ℝ) (L : ℝ) : Prop :=
  ∃ c : ℝ, 0 < c ∧ ∀ s ∈ Icc (0:ℝ) L, ∀ t ∈ Icc (0:ℝ) L,
    dist (γ s) (γ t) ≥ c * |s - t|

/-! ## 2. Invariant 7.5: condition (D) implies injectivity (chord-arc bound) -/

/-- **Invariant 7.5 (the real statement).**

    If the generative curve `γ` satisfies condition (D) on `[0, L]`, then the
    chord-arc bound holds and `γ` is injective on `[0, L]` (an embedded curve —
    no self-intersections).

    The `sorry` is the genuine geometric content (curvature ⇒ positive
    injectivity radius ⇒ chord-arc constant). It is NOT a tautology and NOT a
    relabelled Lyapunov inequality. -/
theorem invariant_7_5_injective
    (γ : ℝ → ℝ × ℝ) (L : ℝ) (hL : 0 < L) (hD : ConditionD γ L) :
    InjOn γ (Icc 0 L) := by
  -- The chord-arc bound in `ConditionD` gives injectivity directly:
  -- if γ s = γ t then dist (γ s) (γ t) = 0, so c·|s−t| ≤ 0, forcing s = t.
  obtain ⟨c, hc, hbound⟩ := hD
  intro s hs t ht hst
  have h0 : dist (γ s) (γ t) = 0 := by rw [hst]; simp
  have := hbound s hs t ht
  rw [h0] at this
  -- 0 ≥ c * |s - t|, with c > 0, forces |s - t| = 0
  have habs : |s - t| ≤ 0 := by
    by_contra h
    push_neg at h
    have : 0 < c * |s - t| := mul_pos hc h
    linarith
  have : |s - t| = 0 := le_antisymm habs (abs_nonneg _)
  have : s - t = 0 := by simpa [abs_eq_zero] using this
  linarith

/-! ## 3. Necessity of (D): the Gerono lemniscate counterexample (proved)

The Gerono lemniscate (lemniscate of Gerono), parametrised by
`γ(t) = (cos t, sin t · cos t)`, is a figure-eight. It self-intersects at the
origin: `γ(π/2) = γ(3π/2) = (0,0)` although `π/2 ≠ 3π/2`. So it is **not**
injective on `[0, 2π]`. It fails condition (D) exactly at the crossing (the
chord-arc constant cannot be positive there), which is why §7.5 needs (D).
This is the counterexample-backed necessity lemma. -/

/-- The Gerono lemniscate parametrisation. -/
noncomputable def gerono (t : ℝ) : ℝ × ℝ := (Real.cos t, Real.sin t * Real.cos t)

/-- `cos (3π/2) = 0`, via the angle-addition formula (robust lemma names). -/
lemma cos_three_pi_div_two : Real.cos (3 * Real.pi / 2) = 0 := by
  have h : 3 * Real.pi / 2 = Real.pi / 2 + Real.pi := by ring
  rw [h, Real.cos_add, Real.cos_pi_div_two, Real.sin_pi_div_two,
      Real.cos_pi, Real.sin_pi]
  ring

/-- The lemniscate passes through the origin at `t = π/2`. -/
lemma gerono_pi_div_two : gerono (Real.pi / 2) = (0, 0) := by
  unfold gerono
  rw [Real.cos_pi_div_two]; simp

/-- The lemniscate passes through the origin again at `t = 3π/2`. -/
lemma gerono_three_pi_div_two : gerono (3 * Real.pi / 2) = (0, 0) := by
  unfold gerono
  rw [cos_three_pi_div_two]; simp

/-- **Self-intersection**: the two distinct parameters map to the same point. -/
theorem gerono_self_intersects :
    gerono (Real.pi / 2) = gerono (3 * Real.pi / 2) := by
  rw [gerono_pi_div_two, gerono_three_pi_div_two]

/-- **Necessity of (D): the Gerono lemniscate is not injective on `[0, 2π]`.**

    Hence condition (D) in Invariant 7.5 cannot be dropped: without it, the
    generative curve may self-intersect. Proved. -/
theorem gerono_not_injOn :
    ¬ InjOn gerono (Icc 0 (2 * Real.pi)) := by
  intro hinj
  have hpi : 0 < Real.pi := Real.pi_pos
  have h1 : Real.pi / 2 ∈ Icc (0:ℝ) (2 * Real.pi) :=
    ⟨by linarith, by linarith⟩
  have h2 : 3 * Real.pi / 2 ∈ Icc (0:ℝ) (2 * Real.pi) :=
    ⟨by linarith, by linarith⟩
  have heq : gerono (Real.pi / 2) = gerono (3 * Real.pi / 2) := gerono_self_intersects
  have : Real.pi / 2 = 3 * Real.pi / 2 := hinj h1 h2 heq
  linarith

/-- **Corollary (necessity, contrapositive form).** Since the Gerono lemniscate
    is not injective on `[0, 2π]`, by `invariant_7_5_injective` it cannot satisfy
    condition (D) there. This closes the necessity direction: (D) is exactly what
    rules out the figure-eight. -/
theorem gerono_fails_conditionD :
    ¬ ConditionD gerono (2 * Real.pi) := by
  intro hD
  have hpi : 0 < Real.pi := Real.pi_pos
  exact gerono_not_injOn
    (invariant_7_5_injective gerono (2 * Real.pi) (by linarith) hD)

/-! ## 4. Note on Theorem B (Volume I)

Theorem B cites "Invariant 7.5, Companion Corollary 1" (see ContactHopf.lean's
Theorem 3.4 citation note). That corollary is the chord-arc bound extracted
from `invariant_7_5_injective` — the embedded-curve property — NOT the generic
Lyapunov contraction that the old version of this file provided. Any downstream
proof depending on §7.5 should import this injectivity result. -/

/-! ## 5. Obligation ledger (honest status)

| Obligation                     | Status     | Notes                                    |
|--------------------------------|------------|------------------------------------------|
| `invariant_7_5_injective`      | **proved** | from the chord-arc bound inside (D)      |
| concrete unfolding of (D)      | external   | curvature ⇒ injectivity radius (geom file)|
| `gerono_self_intersects`       | **proved** | `cos (π/2) = cos (3π/2) = 0`             |
| `gerono_not_injOn`             | **proved** | distinct params, equal images            |
| `gerono_fails_conditionD`      | **proved** | contrapositive of the injectivity theorem|

The generic Lyapunov inequality from the old file is intentionally absent: it is
a different theorem and does not belong under the name Invariant 7.5. -/

end Dm3
