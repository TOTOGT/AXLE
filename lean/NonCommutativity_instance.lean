/-!
================================================================================
§ N  THEOREM 5.3 · NON-COMMUTATIVITY — CONCRETE INSTANCE (DRAFT)
     Paper: §5 Structural Theorems, Theorem 5.3
     Status: hand-verified, NOT machine-checked — no Lean toolchain was
     reachable in the sandbox this was drafted in (elan/lake install blocked
     by network proxy: only `git clone` to github.com works, not release-
     asset downloads via objects.githubusercontent.com). Paste this at the
     end of PrincipiaVol1.lean and run `lake build` to get the real verdict.
     If anything fails to compile, the likely trouble spots are flagged
     inline below — send back the error and it can be patched.

     WHAT THIS PROVES, AND WHAT IT DOESN'T:
     Theorem 5.3 as stated in the paper ("the operators do not commute; the
     sequence is order-dependent") is a claim about *generic* behavior, not
     a universal law — it cannot be a ∀-statement over all valid instances
     of C, K, F, U, because e.g. any instance where one operator is the
     identity commutes trivially with its neighbour. The provable and
     physically meaningful form is the ∃-form: there exist valid instances,
     satisfying every axiom already in this file (CompressionOp,
     CurvatureOp, FoldOp, UnfoldOp), for which reordering two operators in
     the chain changes the result. That is also precisely the form CatGT's
     ZSM-5-vs-MCM-22 firing-order argument needs — it never claims all
     orderings differ, only that these two specific ones do.
================================================================================
-/

/-- A concrete GenerativeManifold on ℤ with potential Φ(x) = x².
    ℤ is used (rather than ℝ, as elsewhere in this file) purely to keep the
    case-analysis tactics (`omega`, `decide`) simple and low-risk to compile
    without a toolchain to test against. -/
noncomputable def intManifold : GenerativeManifold where
  carrier := ℤ
  Phi     := fun x => (x : ℝ) ^ 2
  field   := id  -- unused by any operator below; any choice satisfies the structure

/-- C := identity. Contractive (as `≤`, non-strict) and injective — both
    hold trivially, and nothing in CompressionOp's axioms forbids C = id. -/
noncomputable def C_ex : CompressionOp intManifold where
  map         := id
  contractive := fun x y => le_refl (dist x y)
  injective   := fun _ _ h => h

/-- K := negation. Φ(Kx) = Φ(x) exactly (equality satisfies the ≤ required
    by drives_threshold), since (−x)² = x². -/
noncomputable def K_ex : CurvatureOp intManifold where
  map              := fun x => -x
  kappa_star       := 0
  drives_threshold := by
    intro x
    show ((-x : ℤ) : ℝ) ^ 2 ≤ (x : ℝ) ^ 2
    push_cast
    ring_nf
    -- Goal after ring_nf should reduce to `x^2 ≤ x^2`, closed by `le_refl`.
    -- If ring_nf normalizes the goal shape differently, replace the last
    -- two lines with: `simp [neg_sq]` — that alone should also close it.

/-- F: collapses 5 and 6 to 0, identity everywhere else. Not injective
    (has_fold witnessed by 5 ≠ 6, F 5 = F 6 = 0); branch set is exactly
    {0, 5, 6}, finite. Deliberately NOT symmetric under negation (unlike a
    first draft using ±5, which accidentally commuted with K = negation —
    an odd function always commutes with negation, so the fold set here is
    asymmetric on purpose). -/
noncomputable def F_ex : FoldOp intManifold where
  map := fun x => if x = 5 then 0 else if x = 6 then 0 else x
  has_fold := by
    refine ⟨5, 6, by decide, ?_⟩
    decide
  finite_branch := by
    apply Set.Finite.subset (Set.finite_insert (0:ℤ) (Set.finite_insert 5 (Set.finite_singleton 6)))
    intro p hp
    obtain ⟨q, hqp, heq⟩ := hp
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff]
    -- Case split on which branch of the if-then-else fired for p and q,
    -- then omega closes each resulting linear/equality case over ℤ.
    by_cases hp5 : p = 5
    · left; right; exact hp5
    · by_cases hp6 : p = 6
      · right; exact hp6
      · by_cases hq5 : q = 5
        · left; left
          simp only [hq5, if_pos rfl] at heq
          by_cases hp5' : p = 5
          · exact absurd hp5' hp5
          · by_cases hp6' : p = 6
            · exact absurd hp6' hp6
            · simp only [if_neg hp5', if_neg hp6'] at heq; omega
        · by_cases hq6 : q = 6
          · left; left
            simp only [hq6] at heq
            simp only [if_neg (by omega : (6:ℤ) ≠ 5), if_pos rfl] at heq
            by_cases hp5' : p = 5
            · exact absurd hp5' hp5
            · by_cases hp6' : p = 6
              · exact absurd hp6' hp6
              · simp only [if_neg hp5', if_neg hp6'] at heq; omega
          · exfalso
            simp only [if_neg hq5, if_neg hq6] at heq
            simp only [if_neg hp5, if_neg hp6] at heq
            exact hqp heq

/-- U := identity. decreases_Phi and stable_branch both hold trivially
    (stable_branch is in fact trivially true for *any* map, for any x, via
    n = 0: `map^[0] = id`, so `IsFixedPt (map^[0]) (map x)` unfolds to
    `map x = map x`. Worth flagging upstream — as literally stated,
    UnfoldOp.stable_branch constrains nothing.) -/
noncomputable def U_ex : UnfoldOp intManifold where
  map           := id
  decreases_Phi := fun x => le_refl _
  stable_branch := fun x => ⟨0, rfl⟩

/-- **Theorem 5.3, concrete instance.** Swapping K and F in the firing
    order changes the result: G = U∘F∘K∘C disagrees with U∘K∘F∘C at x = 5.
    G(5)  = U(F(K(C(5))))  = F(K(5))  = F(−5) = −5   (−5 ∉ {5,6})
    G'(5) = U(K(F(C(5))))  = K(F(5))  = K(0)  =  0   (F 5 = 0 by definition)
    −5 ≠ 0, so G ≠ G' at this point: firing order determines the output. -/
theorem nonCommutativity_instance :
    GenerativeOp intManifold C_ex K_ex F_ex U_ex 5
      ≠ (U_ex.map ∘ K_ex.map ∘ F_ex.map ∘ C_ex.map) 5 := by
  show F_ex.map (K_ex.map (C_ex.map 5)) ≠ K_ex.map (F_ex.map (C_ex.map 5))
  simp only [C_ex, K_ex, F_ex, id]
  decide
