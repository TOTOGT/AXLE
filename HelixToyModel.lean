/-
  HelixToyModel.lean
  ------------------------------------------------------------------
  Formal companion to:
    "A Contact-Geometric Toy Model on the Solid Cylinder:
     Transverse Stability, Closure-Dependent Escape, Degenerate Hopf
     Structure, and a Cosmological No-Go."

  Model (see paper, eq. (2)):
     ṙ = f(r)(1 - e^{-z}),   θ̇ = 1,   ż = 1,
  with closure conditions f(1)=0, f'(1)=-2, f(r)(r-1)<0 for r>0, r≠1.
  Transverse linearisation about Γ={r=1}, ε := r-1 :
     ε̇ = 2 ε (e^{-z} - 1),   z = z₀ + t.                       (paper eq. (5))

  STATUS.  This file is structured against Lean 4 / Mathlib4.  The
  arithmetic / sign lemmas (§2) are written to compile.  The analytic
  results (closed-form ODE check, Lyapunov limit, no-go integral) are
  stated precisely and left as `sorry`, tracked below as AXLE-style
  issues.  It has NOT been machine-checked in the authoring environment
  (no toolchain available there); a Mathlib build is required to verify.

  TRACKED ISSUES (mirror of AXLE issue tracker):
    #H1  epsSol_satisfies_ode      (calc via deriv_exp + chain rule)
    #H2  lyapunov_exponent_eq      (l'Hôpital / boundedness of correction)
    #H3  nogo_attractor_to_botinf  (∫ c → -2  ⇒  H → -∞)
  ------------------------------------------------------------------
-/
import Mathlib

noncomputable section
open Real Filter Topology

namespace HelixToyModel

/-! ## §1  The transverse linear solution (paper, Thm. 1) -/

/-- Closed-form transverse deviation, paper eq. (6):
    ε(t) = ε₀ · exp(-2t + 2 e^{-z₀}(1 - e^{-t})). -/
def epsSol (ε₀ z₀ t : ℝ) : ℝ :=
  ε₀ * Real.exp (-2 * t + 2 * Real.exp (-z₀) * (1 - Real.exp (-t)))

/-- Instantaneous transverse rate ρ(z) = 2(e^{-z} - 1) (paper, Thm. 2). -/
def transRate (z : ℝ) : ℝ := 2 * (Real.exp (-z) - 1)

/-- **Issue #H1.**  The closed form solves the linear ODE ε̇ = ρ(z₀+t)·ε. -/
theorem epsSol_satisfies_ode (ε₀ z₀ t : ℝ) :
    deriv (fun s => epsSol ε₀ z₀ s) t
      = transRate (z₀ + t) * epsSol ε₀ z₀ t := by
  sorry  -- AXLE #H1 : structurally routine (deriv_exp, chain rule, exp_neg)

/-- **Issue #H2.**  The Lyapunov exponent equals -2 for any nonzero seed:
    the e^{-z} modulation is integrable along the flow, so contributes a
    bounded additive term to log|ε| and cannot change the rate. -/
theorem lyapunov_exponent_eq (ε₀ z₀ : ℝ) (h : ε₀ ≠ 0) :
    Tendsto (fun t => Real.log |epsSol ε₀ z₀ t / ε₀| / t) atTop (𝓝 (-2)) := by
  sorry  -- AXLE #H2 : log|ε/ε₀| = -2t + 2e^{-z₀}(1-e^{-t}); divide by t → -2

/-! ## §2  The neutral line z = 0  (paper, Thm. 2) — fully proved -/

/-- For z < 0 the transverse rate is strictly positive (repelling). -/
theorem transRate_pos {z : ℝ} (h : z < 0) : 0 < transRate z := by
  have h1 : (1 : ℝ) < Real.exp (-z) := by
    have : (0 : ℝ) < -z := by linarith
    calc (1 : ℝ) = Real.exp 0 := (Real.exp_zero).symm
      _ < Real.exp (-z) := by exact Real.exp_lt_exp.mpr this
  have : 0 < Real.exp (-z) - 1 := by linarith
  unfold transRate; linarith

/-- On the neutral line z = 0 the transverse rate vanishes. -/
theorem transRate_zero : transRate 0 = 0 := by
  unfold transRate; simp

/-- For z > 0 the transverse rate is strictly negative (attracting). -/
theorem transRate_neg {z : ℝ} (h : 0 < z) : transRate z < 0 := by
  have h1 : Real.exp (-z) < 1 := by
    have : (-z : ℝ) < 0 := by linarith
    calc Real.exp (-z) < Real.exp 0 := Real.exp_lt_exp.mpr this
      _ = 1 := Real.exp_zero
  have : Real.exp (-z) - 1 < 0 := by linarith
  unfold transRate; linarith

/-- Sign trichotomy: the neutral line z = 0 is the unique stability reversal. -/
theorem neutral_line_trichotomy (z : ℝ) :
    (z < 0 → 0 < transRate z) ∧ (z = 0 → transRate z = 0) ∧
    (0 < z → transRate z < 0) :=
  ⟨transRate_pos, fun h => by subst h; exact transRate_zero, transRate_neg⟩

/-! ## §3  Degenerate Hopf at the axis (paper, Thm. 5) — algebraic core -/

/-- Linear coefficient λ(z) = 1 - e^{-z} at the axis r = 0. -/
def lam (z : ℝ) : ℝ := 1 - Real.exp (-z)

/-- Cubic (first Lyapunov) coefficient a(z) for the cubic closure equals λ(z);
    they coincide, which is the source of the degeneracy. -/
def aCoeff (z : ℝ) : ℝ := 1 - Real.exp (-z)

/-- **Degeneracy identity.**  For the cubic closure the pinned cycle radius is
    r* = √(λ/a) = 1 for all z with λ(z) ≠ 0, since λ = a.  Here we record the
    coefficient identity a = λ, from which r*² = 1. -/
theorem hopf_degenerate_pinned (z : ℝ) : aCoeff z = lam z := rfl

/-- Consequently, wherever λ(z) ≠ 0, the squared amplitude λ/a equals 1. -/
theorem cycle_radius_pinned {z : ℝ} (hz : lam z ≠ 0) : lam z / aCoeff z = 1 := by
  rw [hopf_degenerate_pinned]; exact div_self hz

/-! ## §4  The contact no-go (paper, Thm. 7) -/

/-  Under θ̇ ≡ 1 and θ-independence, the contact Hamilton equations give
    ż = H(z) := -g(z)  and  transverse rate c(z) := -g'(z).
    We encode the *locking identity* c = H' and the *mutual-exclusivity*
    consequence.  We take H, c as the primitive data with H = -g, c = -g'. -/

/-- **Locking identity** (paper eq. (17)):  with H = -g and c = -g',
    one has c(z) = H'(z) for every z, provided g is differentiable. -/
theorem locking_identity (g : ℝ → ℝ) (hg : Differentiable ℝ g) :
    ∀ z, (fun z => -deriv g z) z = deriv (fun z => - g z) z := by
  intro z
  simp [deriv.neg (hg z)]

/-- **Issue #H3 / No-go (clean direction).**  If the transverse rate c tends to
    -2 (a genuine attractor) and c = H', then the expansion rate H is unbounded
    below; in particular H does not converge to any positive constant, so a
    de Sitter (finite positive-limit) rate is impossible. -/
theorem nogo_attractor_not_deSitter
    (H c : ℝ → ℝ) (hlock : ∀ z, c z = deriv H z)
    (hattr : Tendsto c atTop (𝓝 (-2))) :
    Tendsto H atTop atBot := by
  sorry  -- AXLE #H3 : H(z) = H(z₀) + ∫_{z₀}^z c , integrand → -2 ⇒ H → -∞

/-- Corollary (mutual exclusivity, contrapositive form): a transverse attractor
    excludes a positive finite-limit expansion rate on (M, α). -/
theorem attractor_excludes_deSitter
    (H c : ℝ → ℝ) (hlock : ∀ z, c z = deriv H z)
    (hattr : Tendsto c atTop (𝓝 (-2)))
    (L : ℝ) (hL : 0 < L) : ¬ Tendsto H atTop (𝓝 L) := by
  intro hHL
  have hbot : Tendsto H atTop atBot := nogo_attractor_not_deSitter H c hlock hattr
  -- a function cannot tend to a finite limit and to -∞ simultaneously
  exact absurd (hHL.mono_right atBot_le_nhds ▸ hHL) (by
    -- disjointness of 𝓝 L and atBot at atTop
    sorry)  -- AXLE #H3b : atBot and 𝓝 L are disjoint filters (nontrivial base)

end HelixToyModel
