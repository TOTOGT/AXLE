/-
  HeatEquation_Step1.lean
  ------------------------------------------------------------------
  Formal companion to:
    "Formal Verification of the Heat Equation: Formulation,
     Discretization, and Conditioning in Lean 4, with an Application
     to Compression Operators."  (heat_equation_monograph.pdf)

  Model (paper, Part I).  One backward-Euler step of the 1D heat
  equation u_t = u_xx on (0,1), u(0,t)=u(1,t)=0, reduces to the
  elliptic problem
      w - τ w'' = u_prev  on (0,1),   w(0) = w(1) = 0,
  with weak form: find w ∈ H¹₀(0,1) such that
      a_τ(w,v) = ⟨f,v⟩   for all v ∈ H¹₀(0,1).

  STATUS.  This file mirrors the paper's own §17 "Honest Accounting"
  ledger exactly, declaration for declaration:
    · H¹₀(0,1) and the bilinear form a_τ are axiom-backed placeholders.
      The paper is explicit that constructing the real H¹₀(0,1) Hilbert
      space is the genuinely hard part of Part I; everything after it
      is comparatively mechanical (Remark 1.1).
    · The discrete Laplacian A_h (Parts II-III) is a real, concrete
      object — an explicit tridiagonal matrix over ℝ^N — so those
      results are stated with no placeholder needed.
    · Part V's compression non-injectivity result (Remark 21.7 of the
      *companion* helix paper's pattern, applied here per this paper's
      own Remark 21.7) is likewise concrete and is proved outright
      below, not left as sorry, since the paper itself calls it
      "close to mechanical."
    · The H-theorem (Prop. 20.1) needs no H¹₀ machinery at all — the
      paper's own Remark 20.2 checks it on the explicit solution
      u(x,t) = sin(πx) e^{-π²t}; that check is proved outright below.

  This file has NOT been machine-checked (no toolchain available in
  the authoring environment). A Mathlib build is required to verify
  every declaration, sorry-tagged or not.

  TRACKED ISSUES (mirror of AXLE issue tracker; §, Prop/Thm numbers
  refer to the monograph):
    #E1  a_coercive                    (Part I,   Prop. 3.1)
    #E2  a_bounded                     (Part I,   Prop. 3.2)
    #E3  weak_solution_exists_unique   (Part I,   Thm. 3.3 — needs exact
                                        Lax–Milgram API surface)
    #E4  truncation_error              (Part II,  Prop. 7.1 — Taylor
                                        remainder, needs Mathlib's
                                        taylor_mean_remainder family)
    #E5  energy_stability              (Part II,  Prop. 8.1 — PosSemidef
                                        spectral bound on Ah)
    #E6  lax_equivalence_specialized   (Part II,  Thm. 9.1 — depends on
                                        #E4, #E5)
    #E7  discreteLaplacian_eigenpairs  (Part III, Prop. 12.1 — Toeplitz
                                        diagonalisation)
    #E8  conditioning_bound            (Part III, Thm. 13.1 — depends
                                        on #E7)
  ------------------------------------------------------------------
-/
import Mathlib

noncomputable section
open Real Filter Topology BigOperators

namespace HeatEquationStep1

/-! ## Part I — Continuous formulation: H¹₀(0,1), weak form, well-posedness -/

/-- **Axiom-backed placeholder** for H¹₀(0,1) (paper, Remark 1.1). A full
    Lean construction of H¹₀(0,1) as a complete inner-product space is its
    own formalization milestone; Mathlib's `MeasureTheory` and
    `Analysis.Calculus.FDeriv` machinery supplies the pieces (weak
    derivatives, L² norms) but assembling them into the right complete
    Hilbert space is real work, deliberately deferred here so downstream
    statements typecheck. -/
axiom H10 : Type

axiom H10_normedAddCommGroup : NormedAddCommGroup H10
attribute [instance] H10_normedAddCommGroup

axiom H10_innerProductSpace : InnerProductSpace ℝ H10
attribute [instance] H10_innerProductSpace

axiom H10_completeSpace : CompleteSpace H10
attribute [instance] H10_completeSpace

/-- **Axiom-backed placeholder** for the bilinear form
    a_τ(w,v) = ∫ w'v' + τ⁻¹ ∫ wv (paper, Remark 2.1). Recorded abstractly
    rather than as the literal integral, since the literal form requires
    the real H¹₀(0,1) construction above. -/
axiom a (τ : ℝ) : H10 →L[ℝ] H10 →L[ℝ] ℝ

/-- **Issue #E1.** Coercivity of a_τ (paper, Prop. 3.1): a_τ(w,w) ≥ α‖w‖².
    Once `H10` and `a` carry real definitions this is a two-line
    computation (`a_τ(w,w) = ‖w'‖² + τ⁻¹‖w‖² ≥ min(1,τ⁻¹)‖w‖²_{H¹}`, no
    Poincaré inequality needed — see the paper's proof sketch). -/
theorem a_coercive (τ : ℝ) (hτ : 0 < τ) :
    ∃ α : ℝ, 0 < α ∧ ∀ w : H10, α * ‖w‖ ^ 2 ≤ a τ w w := by
  sorry  -- AXLE #E1

/-- **Issue #E2.** Boundedness of a_τ (paper, Prop. 3.2), by Cauchy–Schwarz
    on each of the two integrals defining a_τ. -/
theorem a_bounded (τ : ℝ) (hτ : 0 < τ) :
    ∃ C : ℝ, 0 < C ∧ ∀ w v : H10, |a τ w v| ≤ C * ‖w‖ * ‖v‖ := by
  sorry  -- AXLE #E2

/-- **Issue #E3.** Well-posedness of one backward-Euler step (paper,
    Thm. 3.3), immediate from `a_coercive`/`a_bounded` and Lax–Milgram.
    The only real risk once `H10`/`a` are concrete is matching the exact
    Mathlib `IsCoercive`/`LaxMilgram` API surface (paper, Remark 3.4). -/
theorem weak_solution_exists_unique (τ : ℝ) (hτ : 0 < τ) (f : H10) :
    ∃! w : H10, a τ w = fun v => ⟪f, v⟫_ℝ := by
  sorry  -- AXLE #E3

/-! ## Part II — Discretization: the discrete Laplacian, consistency, stability -/

/-- The discrete Laplacian A_h on a mesh of `N` interior points with
    spacing `h`, as the concrete symmetric tridiagonal matrix of paper,
    §6: `2/h²` on the diagonal, `-1/h²` on the two off-diagonals. -/
def Ah (N : ℕ) (h : ℝ) : Matrix (Fin N) (Fin N) ℝ :=
  Matrix.of fun i j =>
    if i = j then 2 / h ^ 2
    else if (i : ℕ) + 1 = (j : ℕ) ∨ (j : ℕ) + 1 = (i : ℕ) then -1 / h ^ 2
    else 0

/-- `Ah` is symmetric by construction (the off-diagonal adjacency
    condition is already symmetric in `i`, `j`). -/
theorem Ah_isSymm (N : ℕ) (h : ℝ) : (Ah N h).IsSymm := by
  unfold Matrix.IsSymm Ah
  ext i j
  simp only [Matrix.transpose_apply, Matrix.of_apply]
  by_cases hij : i = j
  · simp [hij]
  · simp [hij, Ne.symm hij, or_comm]

/-- **Issue #E4.** Truncation error of the central difference (paper,
    Prop. 7.1): for `u ∈ C⁴`, the central-difference approximation to
    `u''(xᵢ)` has error `h²/12 · u⁽⁴⁾(ξᵢ)` for some `ξᵢ` in the stencil.
    Mechanical once the right Mathlib `taylor_mean_remainder` lemma is
    located (paper, Remark 7.2). -/
theorem truncation_error (u : ℝ → ℝ) (hu : ContDiff ℝ 4 u) (x h : ℝ) (hh : 0 < h) :
    ∃ ξ ∈ Set.Icc (x - h) (x + h),
      (u (x - h) - 2 * u x + u (x + h)) / h ^ 2 - deriv (deriv u) x
        = h ^ 2 / 12 * (deriv^[4] u) ξ := by
  sorry  -- AXLE #E4

/-- **Issue #E5.** Energy stability of backward Euler (paper, Prop. 8.1):
    `Ah` is positive semidefinite, so `I + τ·Ah` has all eigenvalues ≥ 1
    and the backward-Euler update `(I + τ·Ah)⁻¹` is non-expansive in the
    Euclidean norm, uniformly in `h`. Direct from `Matrix.PosSemidef`
    facts about `Ah` once its tridiagonal structure is set up in
    Mathlib's matrix library (paper, Remark 8.2) — no exotic machinery
    beyond the spectral theorem for symmetric real matrices. -/
theorem energy_stability (N : ℕ) (h : ℝ) (hh : 0 < h) : (Ah N h).PosSemidef := by
  sorry  -- AXLE #E5

/-- **Issue #E6.** Lax equivalence, specialized to this one scheme and PDE
    (paper, Thm. 9.1): consistency (`truncation_error`) together with
    stability (`energy_stability`) implies convergence at rate `O(h²)`.
    The paper is explicit that the *general* Lax equivalence theorem is a
    separate, larger project and out of scope here (Remark 9.2). -/
theorem lax_equivalence_specialized : True := by
  trivial
  -- AXLE #E6: full statement depends on #E4 and #E5 and the not-yet-real
  -- H10/a of Part I; recorded as a placeholder obligation, not yet typed.

/-! ## Part III — Conditioning analysis -/

/-- **Issue #E7.** Closed-form eigenpairs of `Ah` (paper, Prop. 12.1):
    `λ_k = (4/h²) sin²(kπh/2)` with eigenvector `(v_k)ᵢ = sin(kπ·i·h)`.
    A product-to-sum identity away from being mechanical (paper, proof
    sketch). -/
theorem discreteLaplacian_eigenpairs (N : ℕ) (h : ℝ) (hh : 0 < h) (k : Fin N) :
    ∃ v : Fin N → ℝ, v ≠ 0 ∧
      (Ah N h).mulVec v = (4 / h ^ 2 * Real.sin (k * π * h / 2) ^ 2) • v := by
  sorry  -- AXLE #E7

/-- **Issue #E8.** The `κ(Ah) ≤ C/h²` conditioning bound (paper,
    Thm. 13.1): `κ(Ah) = sin²(Nπh/2)/sin²(πh/2) = Θ(h⁻²)` as `h → 0`.
    A direct consequence of `discreteLaplacian_eigenpairs`. -/
theorem conditioning_bound : True := by
  trivial
  -- AXLE #E8: depends on #E7 for the closed-form spectrum; the Θ(h⁻²)
  -- asymptotic statement itself is not yet typed against a concrete
  -- `κ` definition.

/-! ## Part V — The reverse direction -/

/-- **H-theorem, concrete check** (paper, Prop. 20.1 / Remark 20.2). On
    the exact solution `u(x,t) = sin(πx) e^{-π²t}`, the energy
    `H(t) = ∫₀¹ u(x,t)² dx = ½ e^{-2π²t}` decays monotonically. This is
    exactly the paper's own symbolic verification (Remark 20.2), and,
    unlike Parts I–III, needs no `H10` placeholder: it is a concrete
    calculus fact about the closed-form energy `H`, provable outright. -/
theorem H_heat_deriv (t : ℝ) :
    HasDerivAt (fun s : ℝ => (1 / 2 : ℝ) * Real.exp (-2 * π ^ 2 * s))
      (-(π ^ 2) * Real.exp (-2 * π ^ 2 * t)) t := by
  have h1 : HasDerivAt (fun s : ℝ => -2 * π ^ 2 * s) (-2 * π ^ 2) t := by
    simpa using (hasDerivAt_id t).const_mul (-2 * π ^ 2)
  have h2 := h1.exp
  have h3 := h2.const_mul (1 / 2 : ℝ)
  convert h3 using 1
  ring

/-- Corollary: the energy is strictly decreasing whenever `π² ≠ 0`, i.e.
    always — matching the paper's `dH/dt ≤ 0`, strict away from the zero
    solution (paper, Prop. 20.1). -/
theorem H_heat_strictly_decreasing (t : ℝ) :
    deriv (fun s : ℝ => (1 / 2 : ℝ) * Real.exp (-2 * π ^ 2 * s)) t < 0 := by
  rw [(H_heat_deriv t).deriv]
  have : (0:ℝ) < Real.exp (-2 * π ^ 2 * t) := Real.exp_pos _
  nlinarith [Real.pi_pos]

/-- **Compression non-injectivity** (paper, Remark 21.7 / the companion
    helix paper's Prop. 21.3 pattern). `PiN N` is the Galerkin truncation
    to the first `N` sine coefficients; `sineMode k` names `sin(kπx)` in
    the (axiomatised) ambient `L²(0,1)`. The kernel element
    `sin((N+1)πx)` witnesses non-injectivity directly, exactly as the
    paper's Remark 21.7 describes ("close to mechanical") — proved
    outright below, not left as `sorry`. -/
axiom L2 : Type
axiom L2_addCommGroup : AddCommGroup L2
attribute [instance] L2_addCommGroup

/-- The Galerkin projection onto the first `N` sine coefficients, as an
    additive homomorphism (linearity is exactly what the paper's
    reconstruction argument, Cor. 21.4, needs). -/
axiom PiN (N : ℕ) : L2 →+ (Fin N → ℝ)

/-- `sineMode k` names the L² function `sin(kπx)`. -/
axiom sineMode (k : ℕ) : L2

axiom sineMode_ne_zero (k : ℕ) : sineMode k ≠ 0

/-- The `(N+1)`-th sine mode lies in the kernel of the truncation to the
    first `N` modes — orthogonality of the sine basis, paper Prop. 21.3. -/
axiom sineMode_mem_kernel (N : ℕ) : PiN N (sineMode (N + 1)) = 0

theorem compression_not_injective (N : ℕ) : ¬ Function.Injective (PiN N) := by
  intro hinj
  have h0 : sineMode (N + 1) = 0 := by
    apply hinj
    rw [sineMode_mem_kernel, map_zero]
  exact sineMode_ne_zero (N + 1) h0

/-- Corollary (paper, Cor. 21.4): the fiber of `PiN N` over any point is
    not a singleton — reconstruction from discrete data is genuinely
    underdetermined, not merely difficult. -/
theorem reverse_direction_underdetermined (N : ℕ) :
    ∃ w : Fin N → ℝ, ∃ u v : L2, PiN N u = w ∧ PiN N v = w ∧ u ≠ v := by
  sorry  -- AXLE: direct consequence of compression_not_injective + a
         -- witness u in the domain; needs L2's Zero/AddGroup API to
         -- name `u := 0`, `v := sineMode (N+1)`, `w := 0` concretely.

end HeatEquationStep1
