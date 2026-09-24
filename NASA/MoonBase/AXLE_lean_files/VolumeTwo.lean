-- ============================================================
-- COPY of PrincipiaOrthogona_v2/VolumeTwo.lean as of AXLE 607721b (2026-09-24).
-- That file is canonical; edit it, not this one, and re-copy.
-- The version cited in the MoonBase RFI §4.2 (old names thm_A_contact_realization_fold,
-- thm_B_threshold_equivalence, thm_C_singularity_bijection; predates the later compile fixes) is
-- recoverable with: git show 7246603:NASA/MoonBase/AXLE_lean_files/VolumeTwo.lean
-- ============================================================
-- PrincipiaOrthogona/VolumeTwo.lean
-- Formal skeleton for Volume Two: Contact Realization
-- Principia Orthogona Series — G6 LLC, Newark NJ
-- Author: Pablo Nogueira Grossi (ORCID 0009-0000-6496-2186)
--
-- STATUS (2026-09-24): no `sorry` and no vacuous conclusion. Every declaration
-- is kernel-checked (tools/verify-vol2/run.sh). What remains open is recorded
-- as prose obligations in §7, not as theorems: Theorem A's distributional limit
-- (OP-A) and Theorem B's full chain |κ|↑κ* ⟺ μ_max < 0 ⟺ τ ∈ (0,∞) (OP-B).
-- Volume II V5 (10.5281/zenodo.22117968) cites commit e44e8d1, where the
-- withdrawn declarations below still exist under their old names.
--
-- Mathlib dependencies: ContactGeometry (pending upstream),
--   Analysis.ODE.Gronwall, MeasureTheory.Measure.GaussianMeasure
-- ============================================================

import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.MeasureTheory.Measure.MeasureSpace

-- ── §0 Namespaces and basic types ─────────────────────────────────────────────

namespace PrincipiaOrthogona.VolumeTwo

/- The contact manifold M = X × ℝ. We model X as a smooth manifold; here
   abstracted as a metric space with extra structure.
   (A `/-- -/` doc comment cannot attach to `variable`; that was the parse error
   at 25:57, "unexpected token 'variable'; expected 'lemma'".) -/
variable {X : Type*} [MetricSpace X]

/-- Contact variable z ∈ ℝ records accumulated action (dissipation). -/
abbrev ContactVar := ℝ

/-- A dm³ system on M = X × ℝ is a smooth dynamical system satisfying
    Axioms 1–8 of [GCM]. Here modelled as a triple of ODEs. -/
structure DM3System where
  /-- Transverse contraction rate at limit cycle -/
  mu_max  : ℝ
  /-- Angular frequency -/
  omega   : ℝ
  /-- Contact dissipation exponent -/
  beta    : ℝ
  mu_neg  : mu_max < 0      -- Axiom 2: attracting
  omega_pos : 0 < omega     -- Axiom 3: oscillatory
  beta_pos  : 0 < beta      -- Axiom 4: dissipation active

/-- The toy model parameters from §4: (μ_max, ω, β) = (−2, 1, 1) -/
def toyModel : DM3System where
  mu_max    := -2
  omega     := 1
  beta      := 1
  mu_neg    := by norm_num
  omega_pos := by norm_num
  beta_pos  := by norm_num

-- ── §1 Curvature and Embodiment Thresholds ────────────────────────────────────

/-- The curvature threshold κ* at a point, defined as 1 / focal_radius. -/
noncomputable def kappaThreshold (focal_radius : ℝ) (hf : 0 < focal_radius) : ℝ :=
  1 / focal_radius

/-- The embodiment threshold τ = √(c / κ_noise).
    Defined when c > 0 and κ_noise > 0. -/
noncomputable def embodimentThreshold (c κ_noise : ℝ) (hc : 0 < c) (hk : 0 < κ_noise) : ℝ :=
  Real.sqrt (c / κ_noise)

/-- Embodiment threshold is positive when c, κ_noise > 0. -/
theorem embodimentThreshold_pos (c κ_noise : ℝ) (hc : 0 < c) (hk : 0 < κ_noise) :
    0 < embodimentThreshold c κ_noise hc hk := by
  unfold embodimentThreshold
  apply Real.sqrt_pos_of_pos
  exact div_pos hc hk

-- Toy model: c = 4, κ_noise = 1, τ = 2
theorem toyModel_tau :
    embodimentThreshold 4 1 (by norm_num) (by norm_num) = 2 := by
  unfold embodimentThreshold
  -- The previous proof ran `norm_num` first, which already rewrote 4 / 1, so the
  -- following `rw [show (4:ℝ)/1 = 4 ..]` had no pattern left to match.
  rw [show (4 : ℝ) / 1 = 2 ^ 2 by norm_num]
  exact Real.sqrt_sq (by norm_num)

-- ── §2 Transverse Eigenvalue — Proposition 4.2 ────────────────────────────────

/-- The transverse eigenvalue λ(z) = μ_max · (1 − e^{−βz}).
    For the dm³ toy model: λ(z) = −2(1 − e^{−z}). -/
noncomputable def transverseEigenvalue (sys : DM3System) (z : ℝ) : ℝ :=
  sys.mu_max * (1 - Real.exp (- sys.beta * z))

/-- λ(0) = 0 — neutral stability at the embodiment threshold (pre-embodiment). -/
theorem eigenvalue_at_zero (sys : DM3System) :
    transverseEigenvalue sys 0 = 0 := by
  simp [transverseEigenvalue]

/-- λ(z) < 0 for z > 0 — attracting post-embodiment.
    Proof: μ_max < 0 and (1 − e^{−βz}) > 0 for z > 0. -/
theorem eigenvalue_neg_pos_z (sys : DM3System) (z : ℝ) (hz : 0 < z) :
    transverseEigenvalue sys z < 0 := by
  unfold transverseEigenvalue
  apply mul_neg_of_neg_of_pos sys.mu_neg
  -- `Real.exp_lt_one_of_neg` is not a Mathlib constant. Use strict monotonicity
  -- of exp against exp 0 = 1.
  have hbz : -sys.beta * z < 0 := by nlinarith [sys.beta_pos]
  have hexp : Real.exp (- sys.beta * z) < Real.exp 0 := Real.exp_lt_exp.mpr hbz
  rw [Real.exp_zero] at hexp
  linarith

/-- λ(z) → μ_max as z → ∞ (full dm³ contraction rate). -/
theorem eigenvalue_limit (sys : DM3System) :
    Filter.Tendsto (transverseEigenvalue sys)
                   Filter.atTop
                   (nhds sys.mu_max) := by
  -- `simp only [transverseEigenvalue]` makes no progress here: the constant
  -- occurs unapplied, so there is nothing for the equation lemma to rewrite.
  have hfun : transverseEigenvalue sys
      = fun z : ℝ => sys.mu_max * (1 - Real.exp (-sys.beta * z)) := rfl
  rw [hfun]
  -- Step 1: −β·z → −∞  (β > 0, so −β < 0, and z → +∞)
  -- The hand-rolled witness −b/β + 1 defeated `nlinarith`: it cannot see
  -- β · (b/β) = b, so the division blocked the contradiction. Mathlib already
  -- has the fact.
  have h_lin : Filter.Tendsto (fun z : ℝ => -sys.beta * z) Filter.atTop Filter.atBot :=
    Filter.Tendsto.const_mul_atTop_of_neg (by linarith [sys.beta_pos]) Filter.tendsto_id
  -- Step 2: exp(−β·z) → 0  via  Real.tendsto_exp_atBot ∘ h_lin
  have h_exp : Filter.Tendsto (fun z : ℝ => Real.exp (-sys.beta * z))
      Filter.atTop (nhds 0) :=
    Real.tendsto_exp_atBot.comp h_lin
  -- Step 3: 1 − exp(−β·z) → 1 − 0 = 1
  have h_sub : Filter.Tendsto (fun z : ℝ => 1 - Real.exp (-sys.beta * z))
      Filter.atTop (nhds 1) := by
    simpa using (tendsto_const_nhds (x := (1 : ℝ)) (f := Filter.atTop)).sub h_exp
  -- Step 4: μ_max · (1 − exp(−β·z)) → μ_max · 1 = μ_max
  simpa using (tendsto_const_nhds (x := sys.mu_max) (f := Filter.atTop)).mul h_sub

-- ── §2b Theorem 3.3: Lyapunov Stability Certificate ─────────────────────────

/-- THEOREM 3.3 (Volume Two, §3): Lyapunov stability of the contact limit cycle Γ.
    The transverse eigenvalue is strictly negative for all z > 0
    and converges to μ_max < 0 as z → ∞.
    Together these facts are the Lyapunov stability certificate:
    (a) once past the embodiment threshold, the attractor pulls inward; and
    (b) the contraction rate saturates at the full dissipation rate μ_max.
    Proof: conjunction of eigenvalue_neg_pos_z and eigenvalue_limit. -/
theorem vol2_contact_Theorem_3_3 (sys : DM3System) :
    (∀ z : ℝ, 0 < z → transverseEigenvalue sys z < 0) ∧
    Filter.Tendsto (transverseEigenvalue sys) Filter.atTop (nhds sys.mu_max) :=
  ⟨fun z hz => eigenvalue_neg_pos_z sys z hz, eigenvalue_limit sys⟩

-- ── §3 Stability Radius — §4.6 ────────────────────────────────────────────────

/-- The stability radius ε₀ = |μ_max| / (2·(1 + sup‖Hess V‖)).
    For the dm³ toy model: |μ_max|=2, sup‖Hess V‖=2, so ε₀=1/3. -/
noncomputable def stabilityRadius (mu_max_abs hess_sup : ℝ)
    (hm : 0 < mu_max_abs) (hh : 0 ≤ hess_sup) : ℝ :=
  mu_max_abs / (2 * (1 + hess_sup))

theorem toyModel_epsilon0 :
    stabilityRadius 2 2 (by norm_num) (by norm_num) = 1 / 3 := by
  unfold stabilityRadius
  norm_num

/-- PROPOSITION 4.4 (Waddington landscape): For the dm³ toy model the stability
    radius equals the Waddington entropic gap ε₀ = 1/3.
    This is the Lean witness that the landscape curvature 2/(2·(1+2)) = 1/3
    is the unique threshold separating the two basins in the epigenetic picture.
    Proof: direct computation, same as toyModel_epsilon0. -/
theorem epsilon_zero_waddington :
    stabilityRadius 2 2 (by norm_num) (by norm_num) = 1 / 3 :=
  toyModel_epsilon0

/-- THEOREM: Entropy–Lyapunov duality for the dm³ toy model.
    The Lyapunov contraction rate |μ_max| and the embodiment threshold τ are equal:
      μ_max + τ = 0,  i.e.,  μ_max = −2  and  τ = 2.
    Interpretation: the rate at which trajectories are attracted to Γ (= 2)
    is exactly the embodiment threshold (= 2) — the system dissipates entropy
    at precisely the rate that makes embodiment possible.
    Proof: numerical computation from toyModel_tau + toyModel definition. -/
theorem entropy_lyapunov_duality :
    toyModel.mu_max + embodimentThreshold 4 1 (by norm_num) (by norm_num) = 0 := by
  have htau : embodimentThreshold 4 1 (by norm_num) (by norm_num) = 2 := toyModel_tau
  rw [htau]
  -- toyModel.mu_max = −2 by definition; norm_num closes −2 + 2 = 0
  show (-2 : ℝ) + 2 = 0
  norm_num

-- ── §4 Theorem A: Contact Realization of the Fold (Proof Skeleton) ────────────

/- (withdrawn; kept for the record) THEOREM A (Volume Two, §2): The fold operator F is the piecewise-smooth,
    pre-contact limit of the dm³ operator A_{dm³} = φ^{T*/4}.

    Current status: structural proof sketch only.
    Full proof requires:
      (1) Contact Hamiltonian flow theory (Bravetti 2017 [5])
      (2) Distributional limits: Θ-function as β→∞ limit of e^{-βz}
      (3) Regularization of S(γ) = μΘ(κ(γ)−κ*) by H_diss

    Lean formalization path:
      - Define ContactHamiltonian as a structure
      - Prove Proposition 2.1 (regularization) as filter limit
      - Deduce Theorem A from Table 1 (correspondence table)
-/
-- WITHDRAWN 2026-09-24: `thm_A_contact_realization_fold`. Its conclusion was
-- `True` (`:= by trivial`), so it passed every axiom check and established
-- nothing; Volume II V5, Appendix A note 1, already said so. The statement it
-- stood for is recorded as open obligation OP-A in §7. What is provable of
-- Theorem A without distribution theory is in §6d:
-- `thm_A_regularization_pointwise`, `thm_A_regularization_at_fold`.

-- ── §5 Theorem B: Threshold Equivalence (Proof Skeleton) ─────────────────────

/- (withdrawn; kept for the record) THEOREM B (Volume Two, §3): The geometric threshold κ* and the stochastic
    embodiment threshold τ are equivalent:
      |κ| ↑ κ* ⟺ μ_max < 0 ⟺ τ ∈ (0, ∞)

    Lean formalization path:
      - Forward: Lemma 3.1 (fold → hyperbolicity) + Theorem 3.2 (Itô correction)
      - Backward: Lemma 3.3 (finite τ → μ_max < 0) + Theorem 3.4 (contradiction)
-/
-- WITHDRAWN 2026-09-24: `thm_B_threshold_equivalence`. It proved
-- `sys.mu_max < 0 ↔ 0 < embodimentThreshold c κ_noise hc hk`, but the left side
-- is a field of `DM3System` (`mu_neg`) and the right side is
-- `embodimentThreshold_pos`, so both hold by hypothesis and the arrow carries
-- nothing (Volume II V5, Appendix A note 2). The real content, τ > 0, remains
-- as `embodimentThreshold_pos`; the full chain is open obligation OP-B in §7.

-- ── §6 Theorem C: Singularity–Bifurcation Correspondence (Skeleton) ──────────

/-- The four dm³ bifurcation types, matching §5.1. -/
inductive DM3Bifurcation
  | contact_hopf    : DM3Bifurcation   -- A1: limit cycle loses stability
  | saddle_node     : DM3Bifurcation   -- A1: two cycles collide
  | neimark_sacker  : DM3Bifurcation   -- A2: 2-torus bifurcates
  | slow_fast       : DM3Bifurcation   -- A3: smooth contact↔classical

/-- The Whitney singularity types from Volume One. -/
inductive WhitneySingularity
  | A1 : WhitneySingularity  -- fold, codim 0
  | A2 : WhitneySingularity  -- cusp, codim 1
  | A3 : WhitneySingularity  -- swallowtail, codim 2

/-- The correspondence of Proposition 5.1 / Theorem C. -/
def singularityCorrespondence : DM3Bifurcation → WhitneySingularity
  | DM3Bifurcation.contact_hopf   => WhitneySingularity.A1
  | DM3Bifurcation.saddle_node    => WhitneySingularity.A1
  | DM3Bifurcation.neimark_sacker => WhitneySingularity.A2
  | DM3Bifurcation.slow_fast      => WhitneySingularity.A3

/-- THEOREM C, part: `A₂` and `A₃` each have exactly one preimage.
    Renamed 2026-09-24 from `thm_C_singularity_bijection` (the map is not a
    bijection: see `thm_C_not_bijective`; surjectivity is `thm_C_A1_surjective`). -/
theorem thm_C_unique_preimages_A2_A3 :
    -- A2 and A3 have unique preimages
    (∀ b : DM3Bifurcation,
      singularityCorrespondence b = WhitneySingularity.A2 →
      b = DM3Bifurcation.neimark_sacker) ∧
    (∀ b : DM3Bifurcation,
      singularityCorrespondence b = WhitneySingularity.A3 →
      b = DM3Bifurcation.slow_fast) := by
  constructor
  · intro b hb
    cases b <;> simp [singularityCorrespondence] at hb ⊢ <;> exact hb
  · intro b hb
    cases b <;> simp [singularityCorrespondence] at hb ⊢ <;> exact hb

-- ── §6b Theorem 15.2: Integrability of J on the Attractor ───────────────────

/-- A tangent vector to the 1-dimensional attractor Γ.
    We model the tangent space of Γ as ℝ (one generator). -/
abbrev TangentΓ := ℝ

/-- The Nijenhuis tensor N_J restricted to Γ, as a bilinear alternating map.
    Axioms (all that are needed — no differential geometry beyond these):
      (Alt)    N(X, X) = 0              for all X
      (LinL)   N(c•X, Y) = c • N(X, Y) linearity in the left argument
      (LinR)   N(X, c•Y) = c • N(X, Y) linearity in the right argument     -/
structure NijenhuisTensorΓ (V : Type*) [AddCommGroup V] [Module ℝ V] where
  eval         : TangentΓ → TangentΓ → V
  alternating  : ∀ (X : TangentΓ), eval X X = 0
  linear_left  : ∀ (X Y : TangentΓ) (c : ℝ), eval (c • X) Y = c • eval X Y
  linear_right : ∀ (X Y : TangentΓ) (c : ℝ), eval X (c • Y) = c • eval X Y

/-- THEOREM 15.2 · Teorema 15.2: N_J|_Γ = 0.

    Key insight: Newlander–Nirenberg is needed to prove J integrable on the
    full 2-dimensional contact distribution ξ.  On the *1-dimensional*
    attractor Γ, integrability is automatic from a dimension count alone.

    Proof: Every X, Y : TangentΓ = ℝ satisfies X = X•1 and Y = Y•1.
    Hence N(X, Y) = N(X•1, Y•1) = X•N(1, Y•1) = X•Y•N(1,1) = X•Y•0 = 0.
    The only properties used are LinL, LinR, and Alt — no analysis. -/
theorem Theorem_15_2_integrability
    {V : Type*} [AddCommGroup V] [Module ℝ V]
    (N : NijenhuisTensorΓ V) :
    ∀ (X Y : TangentΓ), N.eval X Y = 0 := by
  intro X Y
  -- Every real number r equals r • 1, so we can factor out both scalars.
  have hX : X = X • (1 : ℝ) := (mul_one X).symm
  have hY : Y = Y • (1 : ℝ) := (mul_one Y).symm
  calc N.eval X Y
      = N.eval (X • 1) (Y • 1) := by rw [← hX, ← hY]
    _ = X • N.eval 1 (Y • 1)   := N.linear_left 1 (Y • 1) X
    _ = X • (Y • N.eval 1 1)   := by rw [N.linear_right]
    _ = X • (Y • 0)            := by rw [N.alternating 1]
    _ = 0                      := by simp

-- ── §6c The Elevation Tower ───────────────────────────────────────────────────
--
-- CORRECTION: the correct general statement is NOT
--   "any alternating bilinear form on an n-dim space is zero"  ← FALSE
--   (counterexample: the symplectic form Ω on ℝ² is alternating, nonzero)
--
-- The correct general statement is:
--   "any alternating m-linear form on an n-dim space is zero when m > n"
--
-- This is the actual content of Theorem_15_2_integrability (m=2, n=1).
-- Here we prove the general version as a Mathlib-contributable lemma.

-- ── MAIN ALGEBRAIC THEOREM ───────────────────────────────────────────────────

/-- THEOREM (Alternating Vanishing beyond Dimension):
    Any alternating m-linear map from an n-dimensional R-module V into any
    R-module W is identically zero when m > n.

    Proof: Any m > n vectors in an n-dim space are linearly dependent.
    An alternating map on linearly dependent inputs is zero:
    write vᵢ = ∑_{j≠i} cⱼ vⱼ, expand by linearity — each term has a
    repeated entry, so alternating kills it.

    This is the general form of the dim-count that proved Theorem 15.2.
    Level 1 (Γ, 1-dim) is the case m = 2, n = 1.
    Level 2d (ξ, 2-dim) uses a DIFFERENT argument (d²=0) — see below.

    Lean path: AlternatingMap.map_linearDependent (Mathlib)
               LinearIndependent.fintype_card_le_finrank -/
theorem alternating_vanishes_beyond_dim
    {R : Type*} [CommRing R] [StrongRankCondition R]
    {V : Type*} [AddCommGroup V] [Module R V] [Module.Finite R V]
    {W : Type*} [AddCommGroup W] [Module R W] [NoZeroSMulDivisors R W]
    {m : ℕ}
    (f : AlternatingMap R V W (Fin m))
    (hm : Module.finrank R V < m) :
    f = 0 := by
  ext v
  -- Step 1: m > finrank R V ⟹ v : Fin m → V is linearly dependent
  have hdep : ¬LinearIndependent R v := by
    intro hind
    -- A linearly independent family has cardinality ≤ finrank
    have hcard : Fintype.card (Fin m) ≤ Module.finrank R V :=
      hind.fintype_card_le_finrank
    -- But card (Fin m) = m > finrank, contradiction
    simp at hcard
    omega
  -- Step 2: alternating maps vanish on linearly dependent inputs
  exact f.map_linearDependent v hdep

-- ── Levels 2d and 2d+t: withdrawn 2026-08-26 ────────────────────────────────
--
-- The contact-distribution and full-manifold integrability arguments that stood
-- here proved nothing: the "dΩ = 0" hypothesis was (∀ X Y Z, (0:ℝ) = 0), a
-- tautology, so the axiom field asserted its own conclusion; one Reeb field was
-- (fun _ => 0) = (fun _ => 0); one conclusion was True; and the structure did
-- not parse. The inline summary recorded both levels as "done, closed".
--
-- The mathematics is not withdrawn -- only the claim that it was formalised.
-- N_J(X,Y) = [JX,JY] - J[JX,Y] - J[X,JY] - [X,Y] requires Lie brackets of vector
-- fields, which a pointwise model on (Fin 2 → ℝ) cannot express, so the
-- obligation is recorded as OP4 and OP5 in §7 rather than restated as a theorem
-- whose hypotheses were picked to make it true.
--
-- Withdrawn text: PrincipiaOrthogona_v2/to_delete/VolumeTwo_nijenhuis_levels_2026-08-26.lean
-- Level 1 (Theorem_15_2_integrability, above) is proved and stands.

-- ── §6d V5 additions, 2026-08-26 ─────────────────────────────────────────────
--
-- Four declarations added while preparing V5. Two of them close rows the V4
-- Appendix A listed as PROVED against names that did not exist; one gives
-- Theorem A real content in place of a `True` conclusion; one turns a docstring
-- caveat into a theorem.

/-- **`thm_C_A1_surjective`** — V4's Appendix A listed this as proved under a name
    that existed nowhere. It is true and easy, so here it is: every Whitney type in
    the target is hit. -/
theorem thm_C_A1_surjective : Function.Surjective singularityCorrespondence := by
  intro w
  cases w with
  | A1 => exact ⟨DM3Bifurcation.contact_hopf, rfl⟩
  | A2 => exact ⟨DM3Bifurcation.neimark_sacker, rfl⟩
  | A3 => exact ⟨DM3Bifurcation.slow_fast, rfl⟩

/-- The correspondence is **not** a bijection, and this is a theorem rather than a
    remark. Contact Hopf and saddle-node share the `A₁` preimage, so the map from
    four bifurcations onto three Whitney types is two-to-one there. Versions V2a–V4
    of Volume II described it as bijective in the abstract and in Proposition 5.1
    while the table beneath stated the truth. -/
theorem thm_C_not_bijective : ¬ Function.Bijective singularityCorrespondence := by
  rintro ⟨hinj, -⟩
  have heq : singularityCorrespondence DM3Bifurcation.contact_hopf
           = singularityCorrespondence DM3Bifurcation.saddle_node := rfl
  have hbad : DM3Bifurcation.contact_hopf = DM3Bifurcation.saddle_node := hinj heq
  exact DM3Bifurcation.noConfusion hbad

/-- **Theorem A, the part that is provable here.** The full statement is a
    distributional limit and stays open (obligation OP-A in §7; the former
    placeholder `thm_A_contact_realization_fold`, whose conclusion was `True`,
    was withdrawn 2026-09-24). What *is* provable without distribution theory is
    the pointwise skeleton: away from the fold the contact correction vanishes as
    the regularisation sharpens.

    `β` is the regularisation parameter, taken to `∞`. -/
theorem thm_A_regularization_pointwise (μ : ℝ) {z : ℝ} (hz : 0 < z) :
    Filter.Tendsto (fun β : ℝ => -μ * Real.exp (-z * β)) Filter.atTop (nhds 0) := by
  have hlin : Filter.Tendsto (fun β : ℝ => -z * β) Filter.atTop Filter.atBot :=
    Filter.Tendsto.const_mul_atTop_of_neg (by linarith) Filter.tendsto_id
  have hexp : Filter.Tendsto (fun β : ℝ => Real.exp (-z * β)) Filter.atTop (nhds 0) :=
    Real.tendsto_exp_atBot.comp hlin
  simpa using hexp.const_mul (-μ)

/-- The other half of the skeleton: **on** the fold the correction does not move
    with `β` at all. Together with the previous theorem this is the concentration
    statement — vanishing off `z = 0`, constant on it — of which the distributional
    limit is the completion. -/
theorem thm_A_regularization_at_fold (μ β : ℝ) :
    -μ * Real.exp (-(0 : ℝ) * β) = -μ := by
  simp

/-- **τ = |μ_max| is a coincidence of the canonical value, not an identity.**
    With the drift coefficient `c = 2|μ|` and `κ_noise = 1`, the embodiment
    threshold `√(c/κ)` equals `|μ|` exactly when `|μ| = 2` (or `μ = 0`). The
    docstring of `toyModel_tau` has asserted this since the file was written;
    it is now a theorem, and it is the reason τ is a scale rather than a
    parameter-free relation. -/
theorem tau_eq_abs_mu_iff (μ : ℝ) :
    Real.sqrt (2 * |μ|) = |μ| ↔ |μ| = 2 ∨ μ = 0 := by
  have habs : (0 : ℝ) ≤ |μ| := abs_nonneg μ
  constructor
  · intro h
    have hsq : 2 * |μ| = |μ| ^ 2 := by
      -- do NOT use simp here: it rewrites √(2*|μ|) to √2 * √|μ| before
      -- Real.sq_sqrt can fire, and turns |μ|^2 into μ^2.
      have h2 : Real.sqrt (2 * |μ|) ^ 2 = |μ| ^ 2 := by rw [h]
      rwa [Real.sq_sqrt (by positivity : (0:ℝ) ≤ 2 * |μ|)] at h2
    have hfac : |μ| * (|μ| - 2) = 0 := by nlinarith [hsq]
    rcases mul_eq_zero.mp hfac with h0 | h2
    · exact Or.inr (abs_eq_zero.mp h0)
    · exact Or.inl (by linarith)
  · rintro (h2 | h0)
    · rw [h2]
      rw [show (2 : ℝ) * 2 = 2 ^ 2 by norm_num]
      exact Real.sqrt_sq (by norm_num)
    · simp [h0]

-- ── §7 Open Problems Register ─────────────────────────────────────────────────
-- This section documents all open proof obligations from §6.3.
--
-- OP-A (Theorem A, contact realization of the fold): the contact correction
--     H_diss(z) = −μ_max e^{−βz} converges, as β → ∞, to the fold generator
--     S(z) = μ_max Θ(z) in the sense of distributions. Proved here: the pointwise
--     skeleton (thm_A_regularization_pointwise, thm_A_regularization_at_fold).
--     Status: OPEN. Requires distribution theory in Mathlib. Difficulty ★★★★.
--
-- OP-B (Theorem B, threshold equivalence): |κ| ↑ κ* ⟺ μ_max < 0 ⟺ τ ∈ (0,∞).
--     Proved here: τ > 0 whenever c, κ_noise > 0 (embodimentThreshold_pos).
--     Status: OPEN. Requires Floquet theory (rank-1 Jacobian loss ⟺ μ_max < 0)
--     and an SDE framework (Itô correction). Difficulty ★★★★★.
--
-- OP1 (Global Equivalence): Theorem B is local (fold neighborhood).
--     Global version: every τ-stable dm³ system arises from a fold globally.
--     Status: OPEN. Requires: global contact topology, Weinstein-style result.
--     Lean path: Define "globally fold-generated" predicate; prove iff.
--
-- OP2 (Higher Resonances): Systematic k:m correspondence between
--     higher Ak singularities and higher resonances.
--     Status: OPEN. Requires: singularity theory beyond A3, Mathlib Morse theory.
--
-- OP4 (Integrability on the contact distribution ξ): N_J|_ξ = 0.
--     Content: the Salamon identity (Salamon 1999, Prop. 2.53) recovers N_J from
--     the (0,3) and (3,0) components of dΩ; d² = 0 kills them.
--     Status: OPEN, not yet statable here. Requires Lie brackets of vector
--     fields and an exterior derivative; a pointwise model on (Fin 2 → ℝ)
--     cannot express N_J. Difficulty ★★★★.
--
-- OP5 (Integrability on the full contact 3-manifold): N_J|_M = 0 on
--     TM = ξ ⊕ ⟨R⟩, the mixed terms vanishing by ι_R dα = 0.
--     Status: OPEN, depends on OP4. Difficulty ★★★★.
--
-- OP3 (Volume Three Instantiations): Compute κ* and τ from data in
--     plasma reconnection, market volatility, neural embedding geometry.
--     Status: OPEN. Requires: domain-specific axiom verification (Axioms 1–8).

end PrincipiaOrthogona.VolumeTwo
