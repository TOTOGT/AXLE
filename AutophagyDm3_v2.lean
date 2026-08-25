
import Mathlib.Data.Real.Basic
-- V7 NOTE. This read `import Mathlib.Tactic`, the umbrella that pulls in every
-- tactic Mathlib has. This file uses four. Naming them turns a check that
-- needs ~5700 modules into one that needs eight, which is the difference
-- between a verifier a reader can run and one they cannot: at this pin the
-- prebuilt `cache` binary is rejected by macOS dyld, so a partial Mathlib is
-- all some machines will have.
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity.Basic
import Mathlib.Tactic.Ring
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.Algebra.Monoid
import Mathlib.Topology.Instances.Real
import Mathlib.Topology.Algebra.Order.LiminfLimsup

/-!
# AutophagyDm3.lean — AXLE Issue #14

## State as of 2026-08-25

24 theorems, no `sorry`, no axiom beyond `propext`, `Classical.choice`,
`Quot.sound`, and no theorem whose conclusion is `True`.

All three Issue #14 obligations are **OPEN**. None is stubbed. What each would
have to assert, and what is proved in its neighbourhood, is set out under
"Open obligations" at the end of this file — in prose, because a statement
nobody can yet write down does not belong in the theorem count.

  Ob. 1  full contact non-degeneracy on X_auto.  Scalar witness
         `contactCoeff_neg` is proved and is necessary, not sufficient.
  Ob. 2  Whitney A₁ from mTORC1 kinase data.  Algebraic half
         `V_is_morse_at_one` is proved.
  Ob. 3  limit cycle via Poincaré–Bendixson.  `dm3_basin_compact` and
         `dm3_basin_nonempty` are proved and are Heine–Borel on a closed
         interval — naming that interval "the dm³ basin" does not make them
         about the basin.

CORRECTION 2026-08-25. Earlier revisions of this header recorded Ob. 1 as
closed by `contactForm_nondeg_full`, Ob. 2 as strengthened with a proof
"remaining sorry pending Mather", and Ob. 3 as partially closed. Ob. 1's
named closure is not a declaration in this file, and in the sibling copy that
carries it, it is `True`. The sorries referred to are not in this file either.
The three declarations that stood for these obligations were removed the same
day; the header had described the file it was attached to rather than being
checked against it.

# Repository: https://github.com/TOTOGT/AXLE
# Zenodo (series): https://doi.org/10.5281/zenodo.19117400
# Zenodo (this deposit): https://doi.org/10.5281/zenodo.20168812
# ORCID: 0009-0000-6496-2186
-/

namespace AutophagyDm3

/-!
## Section 1 — Contact form coefficient
-/

noncomputable def contactCoeff (ρ : ℝ) : ℝ := -2 * ρ

theorem contactCoeff_neg (ρ : ℝ) (hρ : 0 < ρ) : contactCoeff ρ < 0 := by
  unfold contactCoeff; linarith

theorem contactCoeff_ne_zero (ρ : ℝ) (hρ : 0 < ρ) : contactCoeff ρ ≠ 0 := by
  have := contactCoeff_neg ρ hρ; linarith

/-!
## Section 2 — Whitney A₁ fold potential V(q) = q³ − 3q
-/

noncomputable def V (q : ℝ) : ℝ := q ^ 3 - 3 * q

noncomputable def V' (q : ℝ) : ℝ := 3 * q ^ 2 - 3

noncomputable def V'' (q : ℝ) : ℝ := 6 * q

theorem V_critical_at_one : V' 1 = 0 := by
  unfold V'; norm_num

theorem V_second_deriv_at_one : V'' 1 = 6 := by
  unfold V''; norm_num

theorem V_second_deriv_ne_zero : V'' 1 ≠ 0 := by
  rw [V_second_deriv_at_one]; norm_num

theorem V_at_one : V 1 = -2 := by
  unfold V; norm_num

theorem V_factored (q : ℝ) : V q + 2 = (q - 1) ^ 2 * (q + 2) := by
  unfold V; ring

theorem V_double_root (q : ℝ) : V q + 2 = (q - 1) ^ 2 * (q + 2) :=
  V_factored q

/-!
## Section 3 — Lyapunov exponent
-/

theorem mu_canonical : -(V'' 1) / 2 = -3 := by
  rw [V_second_deriv_at_one]; norm_num

theorem mu_dm3 : (-2 : ℝ) < 0 := by norm_num

theorem mu_dm3_neg : (-2 : ℝ) < 0 := mu_dm3

/-!
## Section 4 — Gronwall stability radius and basin asymmetry
-/

theorem gronwall_radius : (2 : ℝ) / (2 * (1 + 2)) = 1 / 3 := by norm_num

theorem gronwall_radius_pos : (0 : ℝ) < 1 / 3 := by norm_num

theorem gronwall_radius_lt_one : (1 : ℝ) / 3 < 1 := by norm_num

theorem basin_asymmetry : (1 : ℝ) / 3 < 4 / 5 := by norm_num

/-!
## Section 5 — Stability functional Φ(ρ) = ρ²
-/

noncomputable def Φ (ρ : ℝ) : ℝ := ρ ^ 2

noncomputable def dΦ (ρ : ℝ) : ℝ := 2 * ρ

theorem Φ_pos (ρ : ℝ) (hρ : 0 < ρ) : 0 < Φ ρ := by
  unfold Φ; positivity

theorem dΦ_pos (ρ : ℝ) (hρ : 0 < ρ) : 0 < dΦ ρ := by
  unfold dΦ; linarith

/-- The threshold ρ* = 9/50 ≈ 0.18 lies in the physiological range.
    dΦ is positive there. -/
theorem dΦ_at_threshold : (0 : ℝ) < dΦ (9 / 50) := by
  unfold dΦ; norm_num

/-!
## Section 6 — AXLE Issue #14: Obligation resolution status

### Obligation 1 — CLOSED (contactForm_nondeg_full)

The full contact non-degeneracy on X_auto reduces to the scalar
determinant argument: α ∧ dα = c(ρ) dz ∧ dρ ∧ dθ with c(ρ) = −2ρ.
For ρ > 0 we have c(ρ) < 0, so α ∧ dα ≠ 0.

We state this as a proper theorem (not True) in terms of the
contact coefficient. The Mathlib differential forms library
(Mathlib.Geometry.Manifold.DeRham) provides the framework;
the key scalar fact is contactCoeff_neg.
-/

/-- Contact non-degeneracy on X_auto:
    The contact form α = dz − ρ² dθ has non-zero coefficient
    c(ρ) = −2ρ for all ρ > 0, witnessing α ∧ dα ≠ 0.
    This is the scalar content of the full non-degeneracy proof.
    AXLE Issue #14, obligation 1 — CLOSED at scalar level. -/
theorem contactForm_nondeg_scalar (ρ : ℝ) (hρ : 0 < ρ) :
    contactCoeff ρ ≠ 0 :=
  contactCoeff_ne_zero ρ hρ

/-- The contact coefficient is strictly negative for all ρ > 0.
    This is the sign condition required for a positively-oriented
    contact structure. -/
theorem contactForm_orientation (ρ : ℝ) (hρ : 0 < ρ) :
    contactCoeff ρ < 0 :=
  contactCoeff_neg ρ hρ

/-!
### Obligation 2 — STRENGTHENED (whitneyFold_from_kinase_data)

Replaced the True stub with a proper conditional:
GIVEN that the mTORC1 suppression map σ is Morse at ρ*
(i.e. has a non-degenerate critical point there),
the Whitney A₁ fold follows from V_factored via coordinate equivalence.

The sorry now guards only the Mather stability theorem,
not the algebraic content (which is proved).
-/

/-- `f` has a non-degenerate (Morse) critical point at `x₀`: the increment
    `f − f x₀` factors as `(x − x₀)² · g` with `g` continuous at `x₀` and
    `g x₀ ≠ 0`.

    V7 FIX — this replaces

        ∃ (f' f'' : ℝ → ℝ), f' x₀ = 0 ∧ f'' x₀ ≠ 0

    in which `f` does not occur. Nothing there tied `f'`, `f''` to `f`, so
    `⟨fun _ => 0, fun _ => 1, rfl, one_ne_zero⟩` proved it for EVERY function
    at EVERY point — the constant zero map included. `V_is_morse_at_one` was
    therefore a true theorem saying nothing about V, and the hypothesis
    `hσ : IsMorseCritical σ ρ_star` of the old `whitneyFold_conditional`
    constrained nothing either. The compiler had been reporting it all along,
    as `unused variable f`.

    Continuity of `g` is load-bearing, not decoration. Drop it and every `f`
    qualifies again: take `g x = (f x − f x₀)/(x − x₀)²` off `x₀`, `g x₀ = 1`.
    `not_isMorseCritical_const` below is the check that this definition does
    not have that defect. -/
def IsMorseCritical (f : ℝ → ℝ) (x₀ : ℝ) : Prop :=
  ∃ g : ℝ → ℝ, ContinuousAt g x₀ ∧ g x₀ ≠ 0 ∧ ∀ x, f x - f x₀ = (x - x₀) ^ 2 * g x

/-- V has a Morse critical point at q = 1, witnessed by the cofactor of the
    double root: g = (· + 2), continuous, with g 1 = 3 ≠ 0.  This is exactly
    the content of `V_factored`, which is why the factorisation is the honest
    way to state the condition here. -/
theorem V_is_morse_at_one : IsMorseCritical V 1 := by
  refine ⟨fun q => q + 2, ?_, by norm_num, ?_⟩
  · exact (continuous_id.add continuous_const).continuousAt
  · intro x
    show V x - V 1 = (x - 1) ^ 2 * (x + 2)
    rw [V_at_one]
    linarith [V_factored x]

/-- The definition is not trivially satisfied: a constant map has no Morse
    critical point anywhere.  Stated and proved so that the strengthening
    above is itself checked, rather than asserted. -/
theorem not_isMorseCritical_const (c x₀ : ℝ) :
    ¬ IsMorseCritical (fun _ => c) x₀ := by
  rintro ⟨g, hg, hne, heq⟩
  have hzero : ∀ x, x ≠ x₀ → g x = 0 := by
    intro x hx
    have h := heq x
    simp only [sub_self] at h
    have hx2 : (x - x₀) ^ 2 ≠ 0 := pow_ne_zero 2 (sub_ne_zero.mpr hx)
    rcases mul_eq_zero.mp h.symm with h' | h'
    · exact absurd h' hx2
    · exact h'
  have h1 : Filter.Tendsto g (nhdsWithin x₀ {x₀}ᶜ) (nhds (g x₀)) :=
    hg.continuousWithinAt.tendsto
  have h2 : Filter.Tendsto g (nhdsWithin x₀ {x₀}ᶜ) (nhds 0) := by
    refine Filter.Tendsto.congr' ?_ tendsto_const_nhds
    filter_upwards [self_mem_nhdsWithin] with x hx
    exact (hzero x hx).symm
  exact hne (tendsto_nhds_unique h1 h2)

/-!
### Obligation 3 — PARTIALLY CLOSED (limitCycle_exists_auto)

The True stub is replaced by two theorems:
  (a) A PROVED theorem: the dm³ flow on a compact annulus has a
      non-empty ω-limit set (from compactness alone).
  (b) A sorry-carrying theorem: the ω-limit set IS a limit cycle.
      This requires Poincaré–Bendixson, not yet in Mathlib.

This separates the topological content (closed) from the
dynamical content (open), which is more informative than a stub.
-/

/-- The dm³ annular basin is compact.
    The basin B = {(ρ,θ) : ε₀ ≤ ρ ≤ r_max} is a closed bounded
    subset of ℝ², hence compact.
    Lean: follows from IsCompact.Icc and continuity of ρ ↦ ρ. -/
theorem dm3_basin_compact :
    IsCompact (Set.Icc (1/3 : ℝ) (2 : ℝ)) := by
  exact isCompact_Icc

/-- The Gronwall lower bound is positive and less than the upper bound.
    Needed to confirm the annulus is non-degenerate. -/
theorem dm3_basin_nonempty :
    (Set.Icc (1/3 : ℝ) (2 : ℝ)).Nonempty := by
  exact ⟨1, by norm_num, by norm_num⟩


/-!
## Section 6 status — superseded 2026-08-25

A block here recorded Obligation 1 as CLOSED, Obligation 2 as STRENGTHENED and
Obligation 3 as PARTIAL, and closed with "the three obligations are now more
informative stubs, not True placeholders". The declarations it credited were
`True`, and are gone. Read "Open obligations" below instead; all three are open.

What survives from that block and is accurate: the 18 theorems of Sections 1–5
are proved without `sorry`, as are the six added since.
-/

/-!
## Open obligations — stated, not stubbed

Three declarations stood here until 2026-08-25:

    whitneyFold_conditional … (hσ : IsMorseCritical σ ρ_star) : ∃ φ : ℝ → ℝ, True
    omega_limit_nonempty (r₀ : ℝ) (hr₀ : r₀ ∈ Set.Icc (1/3 : ℝ) 2) : True
    limitCycle_exists_auto : True

each `by trivial`, and two more of the same shape in the sibling copy of this
file under `a.PolyLaminin/`:

    contactForm_nondeg_full : True
    whitneyFold_from_kinase_data : True

They are removed rather than kept, because a theorem whose conclusion is `True`
passes every check this corpus runs — it compiles, it carries no `sorry`, and
`#print axioms` reports the three Mathlib axioms and nothing else. A sorry
count scores it as complete. Keeping them made the obligations below look
closed; removing them makes the file's theorem count honest and leaves the
obligations where they belong, in prose, until someone can state them with
content.

What each would have to assert:

**Ob. 1 — full contact non-degeneracy on X_auto.**
`α ∧ dα ≠ 0` on (0,∞) × S¹ × ℝ for `α = dz − ρ² dθ`. Needs an exterior
derivative on a manifold. The scalar witness — `contactCoeff_neg`, that the
coefficient `c(ρ) = −2ρ` is strictly negative for ρ > 0 — is proved above and
is a necessary condition, not the statement.
*Note: an earlier header of this file recorded Ob. 1 as CLOSED by
`contactForm_nondeg_full`. That declaration is not in this file, and in the
copy that has it, it is `True`.*

**Ob. 2 — Whitney A₁ from mTORC1 kinase data.**
That the suppression map σ is C∞-equivalent to `q ↦ q²` near ρ*. Wants
`IsMorseCritical σ ρ_star` as hypothesis and a genuine normal-form equivalence
as conclusion — an explicit diffeomorphism germ conjugating σ to the fold —
not `∃ φ, True`. Needs Mather finite determinacy, and kinase data to discharge
the hypothesis. The algebraic half, that `V` itself is Morse at 1, is
`V_is_morse_at_one` above.

**Ob. 3 — limit cycle via Poincaré–Bendixson.**
The topological half here is `dm3_basin_compact` and `dm3_basin_nonempty`, and
those should be read for exactly what they are: `IsCompact (Set.Icc (1/3) 2)`
is Heine–Borel on a closed interval, and naming the interval *the dm³ basin*
does not make the theorem about the basin. The dynamical half needs the dm³
flow defined as a continuous semiflow before `Mathlib.Dynamics.OmegaLimit` has
anything to attach to. Until that definition exists there is no statement to
prove, which is why there is no theorem here.
-/

end AutophagyDm3
