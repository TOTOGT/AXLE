/-!
================================================================================
§ N  THEOREM 5.3 · NON-COMMUTATIVITY — CONCRETE INSTANCES  (v4)
     Paper: §5 Structural Theorems, Theorem 5.3
     Supersedes: v1 (NonCommutativity_instance.lean), v2, v3

     CHANGES FROM v3 — the v3 patch is REVERTED, and replaced.

     [R1] v3 changed the two headline finishers from `norm_num` to
          `split_ifs <;> norm_num`, on the stated grounds that
          `finite_branch` / `commuting_instance` use `split_ifs` "for exactly
          this situation". They do not. The situations differ:

            · finite_branch / commuting_instance branch on conditions
              containing FREE VARIABLES (`p = 5`, `q = 5`, `x = 5`).
              These are undecidable in context, so `split_ifs` is REQUIRED.
            · the headline theorems branch on CLOSED NUMERALS
              (`(-5 : ℤ) = 5`, `(5 : ℤ) = 5`, `0 < 4 + 1`).
              There is nothing to case on.

          Note also that the cited pattern finishes with `omega`, not
          `norm_num`. v3 copied the splitter and swapped the finisher.

          The patch fails under BOTH possible behaviours of the preceding
          `simp only`, which is why it is a regression rather than a gamble:

            (a) If the default simprocs fire (`reduceIte`, `Int.reduceEq`,
                `Int.reduceNeg`, `Int.reduceAdd`) — expected, for closed ℤ
                literals — then `simp only` has already collapsed every `ite`.
                The goal reaching `split_ifs` is `(-5 : ℤ) ≠ 0` (or `¬False`),
                and `split_ifs` THROWS: "no if-then-else to split".

            (b) If they do not fire and the `ite`s survive, `split_ifs`
                produces branches carrying contradictory hypotheses, e.g.
                `h : (-5 : ℤ) = 5` with goal `(0 : ℤ) ≠ -0`. That goal is
                FALSE standing alone; the contradiction lives in `h`. And
                `norm_num` DOES NOT CONSUME HYPOTHESES — it normalises the
                target only. Those branches do not close.

          `omega` is the correct finisher in world (b) precisely because it
          does read linear-integer hypotheses from context.

     [R2] The finishers below are `first | norm_num [...] | (simp only [...];
          split_ifs <;> omega)`. This wins in world (a) via the first branch
          and in world (b) via the second. That is defence-in-depth; v3 was
          defence against one world at the cost of the other.

     [R3] `foldMap_not_odd` (present since v2 — my defect, not v1's) used the
          two-step `simp only [foldMap] at this; norm_num at this`. If the
          first call reduces `this` to `False` it CLOSES THE GOAL, and the
          second errors with "no goals to prove". Any `simp ... at h;
          norm_num at h` pair is fragile whenever `h` may collapse. Merged
          into a single call.

     [R4] Header of v3 cites companion scripts `verify_sem.py` /
          `verify_strong.py`. Those were scratch files; the shipped companion
          is `verify_noncommutativity.py`.

     STATUS: STILL NOT MACHINE-CHECKED. No Lean toolchain is reachable in the
     authoring sandbox (no elan/lake; `lake exe cache get` endpoint blocked;
     a from-source Mathlib build exceeds the command timeout). The *semantic*
     content is verified by exhaustive brute force over x ∈ [-80, 80]
     (`verify_noncommutativity.py`): every axiom, every branch set, every
     (non-)commutation claim. The *tactic* proofs are hand-audited only.
     Run `lake build` for the real verdict.

     SIGNATURES ARE INFERRED. PrincipiaVol1.lean was not available, so
     GenerativeManifold / CompressionOp / CurvatureOp / FoldOp / UnfoldOp /
     GenerativeOp are reconstructed from v1's usage. This file assumes
         FoldOp.has_fold      : ∃ x y, x ≠ y ∧ map x = map y
         FoldOp.finite_branch : {p | ∃ q, q ≠ p ∧ map q = map p}.Finite
         GenerativeOp M C K F U = U.map ∘ F.map ∘ K.map ∘ C.map
     If any differs, the affected proof needs a mechanical adjustment, not a
     new idea.

     CHANGES FROM v1 (three defects, two additions) — unchanged from v2:
       [D1] finite_branch: ∨-navigation was off by one. `Set.mem_insert_iff`
            yields the RIGHT-associated `p = 0 ∨ (p = 5 ∨ p = 6)`, so
            `left; right`, `left; left`, and a bare `right` are ill-formed.
            Replaced by `split_ifs at heq <;> omega`, which cannot drift.
       [D2] drives_threshold: the tactic block ENDED at `ring_nf`. The comment
            claimed "closed by le_refl", but `le_refl` was never invoked and
            `ring_nf` does not discharge `x^2 ≤ x^2`. Fixed via `Eq.le`.
       [D3] `decide` on ℤ goals is fragile (OfNat unfolding inside
            `noncomputable` defs). Replaced by `omega` / `norm_num`.
       [A1] The v1 witness is DEGENERATE: C = U = id. Logically valid (the
            swap is K↔F, neither of which is the identity) but half the chain
            is inert and the manifold does no work; and v1's K = negation
            satisfies drives_threshold with EQUALITY, i.e. never drives.
            `nonCommutativity_nondegenerate` fixes both.
       [A2] v1 asserts in prose that Thm 5.3 cannot be a ∀-statement. Now a
            theorem: `not_forall_order_dependent`, witnessed by the symmetric
            fold — v1's discarded "accidental" draft, which is odd and
            therefore genuinely commutes with negation.

     UPSTREAM DEFECTS (fix in PrincipiaVol1.lean, not here):
       [U1] UnfoldOp.stable_branch is VACUOUS. If it reads
            `∀ x, ∃ n, IsFixedPt (map^[n]) (map x)`, then n = 0 gives
            `map^[0] = id`, so `id (map x) = map x` holds for EVERY map.
            Proposed repair:
                stable_branch : ∀ x, ∃ n, 0 < n ∧ IsFixedPt (map^[n]) (map x)
            This bites (it fails for map = (· + 1)) and both unfold operators
            below survive it: n = 1 for id, n = 2 for negation.
       [U2] CurvatureOp.kappa_star is unused: `drives_threshold` is
            `Φ (map x) ≤ Φ x`, which never mentions it. Bind it or drop it.
================================================================================
-/

-- Maps are given standalone names so the tactic proofs unfold predictably
-- instead of relying on structure-projection reduction.

/-- Identity. -/
def idMap : ℤ → ℤ := fun x => x

/-- Negation. Φ-preserving (an involution), NOT Φ-driving. -/
def negMap : ℤ → ℤ := fun x => -x

/-- Strict contraction toward 0: drives Φ = x² strictly downward off the origin. -/
def shrinkMap : ℤ → ℤ := fun x => if 0 < x then x - 1 else if x < 0 then x + 1 else 0

/-- Unit translation. Injective, an isometry (hence contractive), not the identity. -/
def shiftMap : ℤ → ℤ := fun x => x + 1

/-- Asymmetric fold: collapses {5, 6} to 0. NOT odd — this is precisely why it
    fails to commute with negation (see `foldMap_not_odd`). -/
def foldMap : ℤ → ℤ := fun x => if x = 5 then 0 else if x = 6 then 0 else x

/-- Symmetric fold: collapses {5, -5} to 0. IS odd, hence commutes with negation.
    Used to refute the ∀-form of Theorem 5.3. -/
def foldSym : ℤ → ℤ := fun x => if x = 5 then 0 else if x = -5 then 0 else x

/-- The crux of the whole construction: an odd function commutes with negation,
    so the fold set must be asymmetric. `foldMap` is not odd.
    [R3] single call: a `simp ... at h; norm_num at h` pair would error with
    "no goals" if the first call already collapses `h` to `False`. -/
theorem foldMap_not_odd : ¬ (∀ x : ℤ, foldMap (-x) = -foldMap x) := by
  intro h
  have h5 := h 5
  norm_num [foldMap] at h5

/-! ## The manifold -/

/-- A concrete GenerativeManifold on ℤ with potential Φ(x) = x².
    ℤ (rather than ℝ) keeps every side condition decidable by `omega`. -/
noncomputable def intManifold : GenerativeManifold where
  carrier := ℤ
  Phi     := fun x => (x : ℝ) ^ 2
  field   := id

/-! ## Operators — v1 instance (degenerate: C = U = id) -/

noncomputable def C_ex : CompressionOp intManifold where
  map         := idMap
  contractive := fun x y => le_refl (dist x y)
  injective   := fun _ _ h => h

noncomputable def K_ex : CurvatureOp intManifold where
  map              := negMap
  kappa_star       := 0
  drives_threshold := by
    intro x
    -- [D2] v1 stopped at `ring_nf`, leaving `x^2 ≤ x^2` open. Discharge via Eq.le.
    have h : ((negMap x : ℤ) : ℝ) ^ 2 = ((x : ℤ) : ℝ) ^ 2 := by
      simp only [negMap]; push_cast; ring
    exact h.le

noncomputable def F_ex : FoldOp intManifold where
  map      := foldMap
  has_fold := ⟨5, 6, by norm_num, by norm_num [foldMap]⟩
  finite_branch := by
    -- [D1] rebuilt. Conditions here contain FREE variables p, q, so
    -- `split_ifs` is genuinely required; `omega` consumes hqp and the
    -- branch hypotheses.
    apply Set.Finite.subset
      (Set.finite_insert (0 : ℤ) (Set.finite_insert 5 (Set.finite_singleton 6)))
    rintro p ⟨q, hqp, heq⟩
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff]
    simp only [foldMap] at heq
    split_ifs at heq <;> omega

noncomputable def U_ex : UnfoldOp intManifold where
  map           := idMap
  decreases_Phi := fun x => le_refl _
  -- Under the CURRENT (vacuous) axiom: `⟨0, rfl⟩`.
  -- Under the proposed repair [U1] `∃ n, 0 < n ∧ …`: use `⟨1, by norm_num, rfl⟩`.
  stable_branch := fun x => ⟨0, rfl⟩

/-! ## Operators — non-degenerate instance (no operator is the identity) -/

noncomputable def C_nd : CompressionOp intManifold where
  map         := shiftMap
  contractive := by
    intro x y
    -- translation is an isometry: |‌(x+1) - (y+1)| = |x - y|
    simp [shiftMap, Int.dist_eq]
  injective := by
    intro x y h
    simp only [shiftMap] at h
    omega

noncomputable def K_nd : CurvatureOp intManifold where
  map        := shrinkMap
  kappa_star := 0
  drives_threshold := by
    intro x
    have key : (shrinkMap x) ^ 2 ≤ x ^ 2 := by
      -- FREE variable x: `split_ifs` required here, `omega` supplies bounds.
      simp only [shrinkMap]
      split_ifs with h1 h2
      · have hx : 1 ≤ x := by omega
        nlinarith
      · have hx : x ≤ -1 := by omega
        nlinarith
      · have hx : x = 0 := by omega
        subst hx; simp
    show ((shrinkMap x : ℤ) : ℝ) ^ 2 ≤ ((x : ℤ) : ℝ) ^ 2
    exact_mod_cast key

noncomputable def U_nd : UnfoldOp intManifold where
  map           := negMap
  decreases_Phi := by
    intro x
    have h : ((negMap x : ℤ) : ℝ) ^ 2 = ((x : ℤ) : ℝ) ^ 2 := by
      simp only [negMap]; push_cast; ring
    exact h.le
  -- Negation is an involution: n = 2 works even under the repaired axiom [U1].
  -- Current (vacuous) axiom: ⟨0, rfl⟩.  Repaired: ⟨2, by norm_num, by simp [negMap]⟩.
  stable_branch := fun x => ⟨0, rfl⟩

/-! ## Operators — commuting instance (refutes the ∀-form) -/

noncomputable def F_sym : FoldOp intManifold where
  map      := foldSym
  has_fold := ⟨5, -5, by norm_num, by norm_num [foldSym]⟩
  finite_branch := by
    apply Set.Finite.subset
      (Set.finite_insert (0 : ℤ) (Set.finite_insert 5 (Set.finite_singleton (-5))))
    rintro p ⟨q, hqp, heq⟩
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff]
    simp only [foldSym] at heq
    split_ifs at heq <;> omega

/-! ## Theorem 5.3 -/

/-- **v1, preserved.** Swapping K and F changes the result at x = 5.
    G(5)  = U(F(K(C 5))) = F(-5) = -5      (-5 ∉ {5,6})
    G'(5) = U(K(F(C 5))) = K(0)  =  0
    Brute-force verified: G(5) = -5, G'(5) = 0.

    [R1]/[R2] CLOSED numerals: no case split is warranted. `norm_num` with the
    map definitions in its simp set reduces the `ite`s and closes the goal.
    The `first`-fallback covers the world where the simprocs do not fire — and
    that fallback finishes with `omega`, NOT `norm_num`, because the resulting
    branches carry the contradiction in a HYPOTHESIS and `norm_num` reads only
    the target. -/
theorem nonCommutativity_instance :
    GenerativeOp intManifold C_ex K_ex F_ex U_ex 5
      ≠ (U_ex.map ∘ K_ex.map ∘ F_ex.map ∘ C_ex.map) 5 := by
  first
    | norm_num [GenerativeOp, Function.comp_apply, C_ex, K_ex, F_ex, U_ex,
                idMap, negMap, foldMap]
    | (simp only [GenerativeOp, Function.comp_apply, C_ex, K_ex, F_ex, U_ex,
                  idMap, negMap, foldMap]
       split_ifs <;> omega)

/-- **NEW (v2).** Order-dependence with NO operator equal to the identity, and
    with K strictly driving Φ downward off the origin.
    C(4) = 5.
    G(4)  = U(F(K 5)) = U(F 4) = U(4) = -4
    G'(4) = U(K(F 5)) = U(K 0) = U(0) =  0
    Brute-force verified: G(4) = -4, G'(4) = 0. -/
theorem nonCommutativity_nondegenerate :
    GenerativeOp intManifold C_nd K_nd F_ex U_nd 4
      ≠ (U_nd.map ∘ K_nd.map ∘ F_ex.map ∘ C_nd.map) 4 := by
  first
    | norm_num [GenerativeOp, Function.comp_apply, C_nd, K_nd, F_ex, U_nd,
                shiftMap, shrinkMap, negMap, foldMap]
    | (simp only [GenerativeOp, Function.comp_apply, C_nd, K_nd, F_ex, U_nd,
                  shiftMap, shrinkMap, negMap, foldMap]
       split_ifs <;> omega)

/-- **NEW (v2).** The symmetric fold is odd, hence commutes with negation, hence
    the chain is order-INDEPENDENT for this instance, at every point.
    Here `x` is FREE, so `split_ifs` is correct and necessary; `omega` closes
    each branch, including the ones with contradictory hypotheses. -/
theorem commuting_instance (x : ℤ) :
    GenerativeOp intManifold C_ex K_ex F_sym U_ex x
      = (U_ex.map ∘ K_ex.map ∘ F_sym.map ∘ C_ex.map) x := by
  simp only [GenerativeOp, Function.comp_apply, C_ex, K_ex, F_sym, U_ex,
             idMap, negMap, foldSym]
  split_ifs <;> omega

/-! ## The provable form of Theorem 5.3, and its sharp limit -/

/-- Theorem 5.3, ∃-form: there exist valid instances for which firing order
    determines the output. This is the form CatGT's ZSM-5 vs MCM-22 argument
    needs — it never claims all orderings differ, only that two specific ones do. -/
theorem exists_order_dependent :
    ∃ (M : GenerativeManifold) (C : CompressionOp M) (K : CurvatureOp M)
      (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
      GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x :=
  ⟨intManifold, C_nd, K_nd, F_ex, U_nd, 4, nonCommutativity_nondegenerate⟩

/-- The ∀-form is FALSE. Not a matter of taste: here is the counterexample. -/
theorem not_forall_order_dependent :
    ¬ (∀ (M : GenerativeManifold) (C : CompressionOp M) (K : CurvatureOp M)
         (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
         GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x) :=
  fun h => h intManifold C_ex K_ex F_sym U_ex 5 (commuting_instance 5)

/-- Together: order-dependence is a property of *instances*, not of the
    operator algebra. Theorem 5.3 is exactly an ∃-statement, and provably
    no more than one. -/
theorem thm_5_3_is_exactly_existential :
    (∃ (M : GenerativeManifold) (C : CompressionOp M) (K : CurvatureOp M)
       (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
       GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x)
    ∧
    ¬ (∀ (M : GenerativeManifold) (C : CompressionOp M) (K : CurvatureOp M)
         (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
         GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x) :=
  ⟨exists_order_dependent, not_forall_order_dependent⟩
