/-!
================================================================================
§ N  THEOREM 5.3 · NON-COMMUTATIVITY — CONCRETE INSTANCES  (v5)
     Paper: §5 Structural Theorems, Theorem 5.3
     Supersedes: v1, v2, v3, v4

     CHANGES FROM v4 — informed by a REAL CI failure, not hand review.
     v4 was pushed as `PrincipiaOrthogona1/Theorem53NonCommutativity.lean`
     through the repo's `verify-proofs.yml` workflow and the kernel actually
     ran it. It failed. The log is precise enough to diagnose, not just
     retry blindly:

       failed to synthesize Dist intManifold.carrier
       failed to synthesize HPow/LE/OfNat/Neg intManifold.carrier
       x has type intManifold.carrier but is expected to have type ℝ
       (then, cascading from the above in the SAME declarations:)
       omega/linarith/nlinarith failures, "unknown identifier hx/key",
       goals showing literal `sorry.map` placeholders

     [F1] ROOT CAUSE (one bug, not many): `noncomputable def intManifold :
          GenerativeManifold where carrier := ℤ, ...` is an ordinary def.
          Typeclass search and coercion search both run under a MORE
          RESTRICTIVE transparency setting than plain elaboration — by
          default they only unfold `@[reducible]`/`@[instance]` defs, not
          arbitrary ones. So `Dist intManifold.carrier` never gets the
          chance to reduce `intManifold.carrier` down to the literal `ℤ`
          for which `Dist ℤ` actually exists; same story for `HPow`, `LE`,
          `OfNat`, `Neg`, and for the `(x : ℤ)` ascriptions/casts scattered
          through the drives_threshold / decreases_Phi proofs (a failing
          ascription also falls back to coercion search, which has the same
          transparency restriction). Once the FIRST such failure happens
          inside a declaration, Lean's error recovery substitutes a `sorry`
          placeholder and keeps elaborating — which is why the log shows
          `hx`/`key` as "unknown identifier" and goals containing literal
          `sorry.map (-5)` later in the SAME theorem: those are downstream
          noise from one root failure, not independent bugs.
          FIX: mark `intManifold` `@[reducible]`. That's the one line that
          should matter; every other change below is defensive insurance
          around it (cheap to include, expensive to find out is needed only
          after a second failed CI run).
     [F2] `K_nd.drives_threshold` compounded [F1] with a second issue: the
          `show ((shrinkMap x : ℤ) : ℝ) ^ 2 ≤ ((x : ℤ) : ℝ) ^ 2` line has to
          defeq-match the actual goal `intManifold.Phi (shrinkMap x) ≤
          intManifold.Phi x`, which itself requires unfolding `intManifold`
          to see `Phi = fun x => (x:ℝ)^2`. Same root cause, same fix.
     [F3] `finite_branch`'s `omega` failures (both instances: foldMap and
          foldSym) are almost certainly [F1] too — `p`, `q` there are typed
          as `intManifold.carrier`, not raw `ℤ`, so `omega` structurally
          cannot see them as integers until the carrier reduces.
     [F4] `C_nd.contractive`'s `simp [shiftMap, Int.dist_eq]` not closing:
          `Int.dist_eq` is stated for literal `ℤ`; it cannot fire against a
          goal stated over the still-opaque `intManifold.carrier`. Same
          root cause. Rewritten to go through `dist_add_left`-style
          reasoning after forcing the carrier open, as a defensive
          alternative in case the simp lemma name/orientation was also part
          of the problem, not only the carrier opacity.

     STATUS: The [F1] diagnosis is inferred from the CI log, not confirmed
     by a second run — I still have no Lean toolchain reachable from this
     sandbox. This needs a real `lake build` (or another CI push) to know
     whether @[reducible] is sufficient or whether a second issue is hiding
     behind it. Please don't take this as ✓ until that comes back green.

     SIGNATURES ARE STILL INFERRED (unchanged from v1-v4) — if
     PrincipiaVol1.lean's actual GenerativeManifold/CompressionOp/etc.
     differ from what's assumed here, that's a separate axis of risk from
     [F1]-[F4] and would need its own diagnosis.

     UPSTREAM DEFECTS (fix in PrincipiaVol1.lean, not here — unchanged):
       [U1] UnfoldOp.stable_branch is vacuous as literally stated (n = 0
            always works). Proposed repair: require 0 < n.
       [U2] CurvatureOp.kappa_star is unused in drives_threshold.
================================================================================
-/

def idMap : ℤ → ℤ := fun x => x
def negMap : ℤ → ℤ := fun x => -x
def shrinkMap : ℤ → ℤ := fun x => if 0 < x then x - 1 else if x < 0 then x + 1 else 0
def shiftMap : ℤ → ℤ := fun x => x + 1
def foldMap : ℤ → ℤ := fun x => if x = 5 then 0 else if x = 6 then 0 else x
def foldSym : ℤ → ℤ := fun x => if x = 5 then 0 else if x = -5 then 0 else x

theorem foldMap_not_odd : ¬ (∀ x : ℤ, foldMap (-x) = -foldMap x) := by
  intro h
  have h5 := h 5
  norm_num [foldMap] at h5

/-! ## The manifold -/

/-- [F1] `@[reducible]` is the actual fix this version is testing: without
    it, typeclass search (Dist, LE, HPow, OfNat, Neg) and coercion search
    both refuse to unfold `intManifold` far enough to see `carrier = ℤ`,
    which is what the CI log's "failed to synthesize" errors were. -/
@[reducible]
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
    -- [F1]/[F2] defensive: force the carrier open before casting.
    unfold_let intManifold
    show ((negMap x : ℤ) : ℝ) ^ 2 ≤ ((x : ℤ) : ℝ) ^ 2
    have h : ((negMap x : ℤ) : ℝ) ^ 2 = ((x : ℤ) : ℝ) ^ 2 := by
      simp only [negMap]; push_cast; ring
    exact h.le

noncomputable def F_ex : FoldOp intManifold where
  map      := foldMap
  has_fold := ⟨5, 6, by norm_num, by norm_num [foldMap]⟩
  finite_branch := by
    apply Set.Finite.subset
      (Set.finite_insert (0 : ℤ) (Set.finite_insert 5 (Set.finite_singleton 6)))
    rintro p ⟨q, hqp, heq⟩
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff]
    simp only [foldMap] at heq
    split_ifs at heq <;> omega

noncomputable def U_ex : UnfoldOp intManifold where
  map           := idMap
  decreases_Phi := fun x => le_refl _
  stable_branch := fun x => ⟨0, rfl⟩

/-! ## Operators — non-degenerate instance (no operator is the identity) -/

noncomputable def C_nd : CompressionOp intManifold where
  map         := shiftMap
  contractive := by
    intro x y
    unfold_let intManifold
    -- [F4] defensive: unfold shiftMap and go through dist on ℤ directly,
    -- rather than trusting a single simp call with Int.dist_eq to both
    -- unfold the carrier AND fire the rewrite in one step.
    show dist (shiftMap x) (shiftMap y) ≤ dist x y
    simp only [shiftMap, Int.dist_eq]
    have : x + 1 - (y + 1) = x - y := by ring
    rw [this]
  injective := by
    intro x y h
    simp only [shiftMap] at h
    omega

noncomputable def K_nd : CurvatureOp intManifold where
  map        := shrinkMap
  kappa_star := 0
  drives_threshold := by
    intro x
    unfold_let intManifold
    show ((shrinkMap x : ℤ) : ℝ) ^ 2 ≤ ((x : ℤ) : ℝ) ^ 2
    have key : (shrinkMap x) ^ 2 ≤ x ^ 2 := by
      simp only [shrinkMap]
      split_ifs with h1 h2
      · have hx : 1 ≤ x := by omega
        nlinarith
      · have hx : x ≤ -1 := by omega
        nlinarith
      · have hx : x = 0 := by omega
        subst hx; simp
    exact_mod_cast key

noncomputable def U_nd : UnfoldOp intManifold where
  map           := negMap
  decreases_Phi := by
    intro x
    unfold_let intManifold
    show ((negMap x : ℤ) : ℝ) ^ 2 ≤ ((x : ℤ) : ℝ) ^ 2
    have h : ((negMap x : ℤ) : ℝ) ^ 2 = ((x : ℤ) : ℝ) ^ 2 := by
      simp only [negMap]; push_cast; ring
    exact h.le
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

theorem nonCommutativity_instance :
    GenerativeOp intManifold C_ex K_ex F_ex U_ex 5
      ≠ (U_ex.map ∘ K_ex.map ∘ F_ex.map ∘ C_ex.map) 5 := by
  first
    | norm_num [GenerativeOp, Function.comp_apply, C_ex, K_ex, F_ex, U_ex,
                idMap, negMap, foldMap]
    | (simp only [GenerativeOp, Function.comp_apply, C_ex, K_ex, F_ex, U_ex,
                  idMap, negMap, foldMap]
       split_ifs <;> omega)

theorem nonCommutativity_nondegenerate :
    GenerativeOp intManifold C_nd K_nd F_ex U_nd 4
      ≠ (U_nd.map ∘ K_nd.map ∘ F_ex.map ∘ C_nd.map) 4 := by
  first
    | norm_num [GenerativeOp, Function.comp_apply, C_nd, K_nd, F_ex, U_nd,
                shiftMap, shrinkMap, negMap, foldMap]
    | (simp only [GenerativeOp, Function.comp_apply, C_nd, K_nd, F_ex, U_nd,
                  shiftMap, shrinkMap, negMap, foldMap]
       split_ifs <;> omega)

theorem commuting_instance (x : ℤ) :
    GenerativeOp intManifold C_ex K_ex F_sym U_ex x
      = (U_ex.map ∘ K_ex.map ∘ F_sym.map ∘ C_ex.map) x := by
  simp only [GenerativeOp, Function.comp_apply, C_ex, K_ex, F_sym, U_ex,
             idMap, negMap, foldSym]
  split_ifs <;> omega

/-! ## The provable form of Theorem 5.3, and its sharp limit -/

theorem exists_order_dependent :
    ∃ (M : GenerativeManifold) (C : CompressionOp M) (K : CurvatureOp M)
      (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
      GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x :=
  ⟨intManifold, C_nd, K_nd, F_ex, U_nd, 4, nonCommutativity_nondegenerate⟩

theorem not_forall_order_dependent :
    ¬ (∀ (M : GenerativeManifold) (C : CompressionOp M) (K : CurvatureOp M)
         (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
         GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x) :=
  fun h => h intManifold C_ex K_ex F_sym U_ex 5 (commuting_instance 5)

theorem thm_5_3_is_exactly_existential :
    (∃ (M : GenerativeManifold) (C : CompressionOp M) (K : CurvatureOp M)
       (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
       GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x)
    ∧
    ¬ (∀ (M : GenerativeManifold) (C : CompressionOp M) (K : CurvatureOp M)
         (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
         GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x) :=
  ⟨exists_order_dependent, not_forall_order_dependent⟩
