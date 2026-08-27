-- WITHDRAWN 2026-08-26 from PrincipiaOrthogona_v2/VolumeTwo.lean, lines 369-461.
-- Kept because errors are evidence. NOT a build target; do not import.
--
-- Why withdrawn. These two "levels" proved nothing, while their comments recorded
-- both as "done, closed":
--   * NijenhuisTensorξ.domega_zero_implies_N_zero took the hypothesis
--     (∀ X Y Z, (0:ℝ) = 0) -- a tautology -- so the field asserted its own
--     conclusion unconditionally, and integrability_on_contact_distribution
--     discharged N_J = 0 by applying it.
--   * ContactManifoldPoint.N_R_xi_zero was (fun _ => 0) = (fun _ => 0).
--   * The second conjunct of integrability_on_full_contact_manifold was True.
--   * ContactDistributionPoint did not parse: a `where` block after the field
--     list, and nijenhuisEval used in a field type before it was defined.
--     (build error at 391: unexpected token 'where'; expected command)
--
-- The obligation is real and is now recorded as OP4/OP5 in the Open Problems
-- Register. It cannot honestly be stated in this file: the Nijenhuis tensor
-- N_J(X,Y) = [JX,JY] - J[JX,Y] - J[X,JY] - [X,Y] needs Lie brackets of vector
-- fields, which a pointwise model on (Fin 2 -> ℝ) cannot express. A statement
-- that cannot be written is recorded as prose, not as a theorem with a
-- hypothesis chosen to make it come out true.
--
-- Level 1 (Theorem_15_2_integrability) is unaffected and remains in the file:
-- it is proved from bilinearity and alternation on a 1-dimensional tangent
-- space, and it is correct.

-- ── Level 2d: symplectic distribution ξ, N_J = 0 from d² = 0 ───────────────

/-- The contact distribution ξ at a point: a 2-dimensional real symplectic space.
    We model it as ℝ² with a symplectic form Ω (the restriction of dα).
    Axioms needed:
      (J²)     J ∘ J = −id                  (almost complex structure)
      (Compat) Ω(JX, JY) = Ω(X, Y)          (J preserves Ω)
      (Closed) dΩ = 0                        (Ω = dα|_ξ, so d(dα) = 0)
    Key identity (Salamon 1999, Prop 2.53):
      Ω(N_J(X,Y), Z) = (dΩ)^{0,3}(X,Y,Z) + (dΩ)^{3,0}(X,Y,Z)
    Since dΩ = 0, all type components vanish, so N_J = 0. -/
structure ContactDistributionPoint where
  /-- Symplectic form Ω : ξ × ξ → ℝ  (bilinear, alternating, non-degenerate) -/
  omega        : (Fin 2 → ℝ) → (Fin 2 → ℝ) → ℝ
  /-- Almost complex structure J : ξ → ξ -/
  J            : (Fin 2 → ℝ) → (Fin 2 → ℝ)
  /-- The Nijenhuis tensor extracted from the (0,3)-component of dΩ.
      Statement: N_J(X,Y) is proportional to the (0,3)+(3,0) part of dΩ. -/
  nijenhuis_from_domega :
      ∀ (X Y : Fin 2 → ℝ),
        (∀ Z, omega (nijenhuisEval X Y) Z = 0) →
        nijenhuisEval X Y = 0
  where
    nijenhuisEval : (Fin 2 → ℝ) → (Fin 2 → ℝ) → (Fin 2 → ℝ) :=
      fun X Y => (fun _ => 0)  -- placeholder; see below

/-- The Nijenhuis tensor on ξ, axiomatised with its relation to dΩ. -/
structure NijenhuisTensorξ where
  eval         : (Fin 2 → ℝ) → (Fin 2 → ℝ) → (Fin 2 → ℝ)
  alternating  : ∀ X, eval X X = 0
  /-- Key axiom (Salamon Prop 2.53): N_J is determined by the (0,3) part of dΩ.
      When dΩ = 0, this forces N_J = 0. -/
  domega_zero_implies_N_zero :
      (∀ (X Y Z : Fin 2 → ℝ), (0 : ℝ) = 0) →  -- dΩ = 0 (all components)
      ∀ X Y, eval X Y = 0

/-- LEVEL 2d: On the contact distribution ξ = (ℝ², dα|_ξ),
    the Nijenhuis tensor of any compatible J vanishes: N_J|_ξ = 0.

    Proof: Ω = dα|_ξ.  Since d² = 0, dΩ = d(dα)|_ξ = 0.
    By the Salamon identity, N_J is recovered from the (0,3) component of dΩ.
    Hence N_J = 0.  This closes the sorry WITHOUT Newlander–Nirenberg:
    the integrability of J on ξ follows directly from d² = 0 (a tautology). -/
theorem integrability_on_contact_distribution
    (N : NijenhuisTensorξ)
    (domega_closed : ∀ (X Y Z : Fin 2 → ℝ), (0 : ℝ) = 0) :
    ∀ (X Y : Fin 2 → ℝ), N.eval X Y = 0 :=
  N.domega_zero_implies_N_zero domega_closed

-- ── Level 2d+t: full contact 3-manifold M = ξ × ⟨R⟩ ────────────────────────

/-- The Reeb vector field R is the unique vector field satisfying
      α(R) = 1  and  ι_R dα = 0.
    J is extended from ξ to TM by setting J(R) = 0 (R is J-real). -/
structure ContactManifoldPoint where
  /-- Distribution part: inherits from the 2d level -/
  xi           : NijenhuisTensorξ
  /-- Reeb direction: R transverse to ξ -/
  alpha_R      : ℝ                    -- α(R) = 1
  alpha_R_one  : alpha_R = 1
  /-- Mixed Nijenhuis terms N_J(R, X) for X ∈ ξ.
      These vanish by the contact Cartan formula:
        ι_R dα = 0  ⟹  dα(R, JX) = 0  ⟹  N_J(R, X) = 0. -/
  N_R_xi_zero  : ∀ (X : Fin 2 → ℝ), (fun _ : Fin 2 => (0 : ℝ)) = (fun _ => 0)

/-- LEVEL 2d+t: On the full contact 3-manifold M = ξ ⊕ ⟨R⟩,
    the Nijenhuis tensor of J vanishes everywhere: N_J|_M = 0.

    Proof by decomposition of TM = ξ ⊕ ⟨R⟩:
      (a) N_J|_{ξ×ξ} = 0  by Level 2d  (d² = 0)
      (b) N_J(R, X) = 0   by ι_R dα = 0  (Cartan / contact condition)
      (c) N_J(R, R) = 0   by alternating

    All three cases use only d² = 0 and the contact axiom ι_R dα = 0.
    The full Newlander–Nirenberg theorem (analytic, uses ∂̄) is not needed
    because M is 3-real-dimensional (not a complex manifold — J lives on ξ). -/
theorem integrability_on_full_contact_manifold
    (C : ContactManifoldPoint)
    (domega_closed : ∀ (X Y Z : Fin 2 → ℝ), (0 : ℝ) = 0) :
    -- N_J = 0 on all of TM (modelled as ξ-part + Reeb part)
    (∀ (X Y : Fin 2 → ℝ), C.xi.eval X Y = 0) ∧
    (∀ (X : Fin 2 → ℝ), True) := by   -- N_J(R, X) = 0: encoded in C.N_R_xi_zero
  constructor
  · -- Case (a): ξ × ξ — use Level 2d
    exact integrability_on_contact_distribution C.xi domega_closed
  · -- Case (b) + (c): Reeb direction — use contact axiom
    intro _; trivial   -- encoded as axiom in ContactManifoldPoint

-- Summary remark (inline):
-- Level 1  (done, closed):   dim-count on TangentΓ = ℝ
-- Level 2d (done, closed):   d² = 0 forces N_J|_ξ = 0  (symplectic argument)
-- Level 2d+t (done, closed): ι_R dα = 0 kills mixed terms; alt kills R×R
-- ────────────────────────────────────────────────────────────────────────────
