/-
Theorem53NonCommutativity.lean
===============================
Self-contained Lean 4 / Mathlib4 formal verification of Theorem 5.3
(Non-Commutativity) from:
"Principia Orthogona, Volume I: The Mathematics of Generative Transitions"
Pablo Nogueira Grossi -- G6 LLC, Newark NJ, 2026

This file is intentionally SELF-CONTAINED and separate from PrincipiaVol1.lean.
PrincipiaVol1.lean (the original monolithic file) contains extensive
pre-existing compile errors in unrelated sections (SS6 CompressionOp.contractive
dist/MetricSpace mismatch, SS7 Dm3Triple, SS9 separation_theorem, SS10-11
Ordinal/club-filter deprecated-API breakage) that predate this work and were
never caught because the file was never wired into CI until now. Fixing all
of that is a separate, larger undertaking. This file carries only the
structures needed for Theorem 5.3 (with the CompressionOp field fixed) plus
the Theorem 5.3 proof content itself, so it can be verified in isolation by
the real Lean kernel in CI.

Build: lake build Theorem53
Dependencies: Mathlib4 (current stable)

Sorry count: 0
Axiom count: 0 beyond Mathlib4
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Dynamics.FixedPoints.Basic

namespace Theorem53NonCommutativity

-- ============================================================================
-- OPERATOR CHAIN STRUCTURES
-- Reproduced from PrincipiaVol1.lean section 6, with one fix:
-- CompressionOp.contractive now uses `letI := M.metric` so that `dist`
-- is resolved via ordinary typeclass search through the Dist/PseudoMetricSpace
-- /MetricSpace extends chain, instead of `@dist _ M.metric` which fails
-- because M.metric : MetricSpace M.carrier is not itself a Dist instance.
-- ============================================================================

structure GenerativeManifold where
  carrier : Type*
  [metric : MetricSpace carrier]
  Phi : carrier -> ℝ
  field : carrier -> carrier

structure CompressionOp (M : GenerativeManifold) where
  map : M.carrier -> M.carrier
  contractive : letI := M.metric; ∀ x y, dist (map x) (map y) ≤ dist x y
  injective : Function.Injective map

structure CurvatureOp (M : GenerativeManifold) where
  map : M.carrier -> M.carrier
  kappa_star : ℝ
  drives_threshold : ∀ x, M.Phi (map x) ≤ M.Phi x

structure FoldOp (M : GenerativeManifold) where
  map : M.carrier -> M.carrier
  has_fold : ∃ x y : M.carrier, x ≠ y ∧ map x = map y
  finite_branch : Set.Finite {p : M.carrier | ∃ q, q ≠ p ∧ map q = map p}

structure UnfoldOp (M : GenerativeManifold) where
  map : M.carrier -> M.carrier
  decreases_Phi : ∀ x, M.Phi (map x) ≤ M.Phi x
  stable_branch : ∀ x, ∃ n : ℕ, Function.IsFixedPt (map^[n]) (map x)

def GenerativeOp (M : GenerativeManifold)
    (C : CompressionOp M) (K : CurvatureOp M)
    (F : FoldOp M) (U : UnfoldOp M) : M.carrier -> M.carrier :=
  U.map ∘ F.map ∘ K.map ∘ C.map

-- ============================================================================
-- THEOREM 5.3 NON-COMMUTATIVITY -- CONCRETE INSTANCES
-- Reproduced from PrincipiaVol1.lean section 14 (v4), with fixes:
-- (1) GenerativeManifold pinned to .{0} throughout so the universe-
--     polymorphic forall/exists statements unify with the concrete intManifold.
-- (2) Numeral arguments passed at type `M.carrier` / `intManifold.carrier`
--     are explicitly ascribed `(_ : ℤ)` so elaboration doesn't need to
--     unfold `intManifold` during OfNat/Neg typeclass search.
-- (3) `Set.finite_insert` (unknown constant in current Mathlib) replaced
--     with `Set.Finite.insert`.
-- (4) commuting_instance's proof rewritten as an explicit case split
--     instead of `split_ifs <;> omega`, because `split_ifs` treats
--     `-x = 5` and `x = -5` as syntactically distinct conditions and the
--     resulting spurious branches were not closing automatically.
-- ============================================================================

def idMap : ℤ -> ℤ := fun x => x
def negMap : ℤ -> ℤ := fun x => -x
def shrinkMap : ℤ -> ℤ := fun x => if 0 < x then x - 1 else if x < 0 then x + 1 else 0
def shiftMap : ℤ -> ℤ := fun x => x + 1
def foldMap : ℤ -> ℤ := fun x => if x = 5 then 0 else if x = 6 then 0 else x
def foldSym : ℤ -> ℤ := fun x => if x = 5 then 0 else if x = -5 then 0 else x

theorem foldMap_not_odd : ¬ (∀ x : ℤ, foldMap (-x) = -foldMap x) := by
  intro h
  have h5 := h 5
  norm_num [foldMap] at h5

noncomputable def intManifold : GenerativeManifold where
  carrier := ℤ
  Phi := fun x => (x : ℝ) ^ 2
  field := id

noncomputable def C_ex : CompressionOp intManifold where
  map := idMap
  contractive := fun x y => le_refl (dist x y)
  injective := fun _ _ h => h

noncomputable def K_ex : CurvatureOp intManifold where
  map := negMap
  kappa_star := 0
  drives_threshold := by
    intro x
    have h : ((negMap x : ℤ) : ℝ) ^ 2 = ((x : ℤ) : ℝ) ^ 2 := by
      simp only [negMap]; push_cast; ring
    exact h.le

noncomputable def F_ex : FoldOp intManifold where
  map := foldMap
  has_fold := ⟨(5 : ℤ), (6 : ℤ), by norm_num, by norm_num [foldMap]⟩
  finite_branch := by
    apply Set.Finite.subset
      (Set.Finite.insert (0 : ℤ) (Set.Finite.insert 5 (Set.finite_singleton 6)))
    rintro p ⟨q, hqp, heq⟩
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff]
    simp only [foldMap] at heq
    split_ifs at heq <;> omega

noncomputable def U_ex : UnfoldOp intManifold where
  map := idMap
  decreases_Phi := fun x => le_refl _
  stable_branch := fun x => ⟨0, rfl⟩

noncomputable def C_nd : CompressionOp intManifold where
  map := shiftMap
  contractive := by
    intro x y
    simp [shiftMap, Int.dist_eq]
  injective := by
    intro x y h
    simp only [shiftMap] at h
    omega

noncomputable def K_nd : CurvatureOp intManifold where
  map := shrinkMap
  kappa_star := 0
  drives_threshold := by
    intro x
    have key : (shrinkMap x) ^ 2 ≤ x ^ 2 := by
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
  map := negMap
  decreases_Phi := by
    intro x
    have h : ((negMap x : ℤ) : ℝ) ^ 2 = ((x : ℤ) : ℝ) ^ 2 := by
      simp only [negMap]; push_cast; ring
    exact h.le
  stable_branch := fun x => ⟨0, rfl⟩

noncomputable def F_sym : FoldOp intManifold where
  map := foldSym
  has_fold := ⟨(5 : ℤ), (-5 : ℤ), by norm_num, by norm_num [foldSym]⟩
  finite_branch := by
    apply Set.Finite.subset
      (Set.Finite.insert (0 : ℤ) (Set.Finite.insert 5 (Set.finite_singleton (-5))))
    rintro p ⟨q, hqp, heq⟩
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff]
    simp only [foldSym] at heq
    split_ifs at heq <;> omega

theorem nonCommutativity_instance :
    GenerativeOp intManifold C_ex K_ex F_ex U_ex (5 : ℤ)
      ≠ (U_ex.map ∘ K_ex.map ∘ F_ex.map ∘ C_ex.map) (5 : ℤ) := by
  first
  | norm_num [GenerativeOp, Function.comp_apply, C_ex, K_ex, F_ex, U_ex,
      idMap, negMap, foldMap]
  | (simp only [GenerativeOp, Function.comp_apply, C_ex, K_ex, F_ex, U_ex,
      idMap, negMap, foldMap]
     split_ifs <;> omega)

theorem nonCommutativity_nondegenerate :
    GenerativeOp intManifold C_nd K_nd F_ex U_nd (4 : ℤ)
      ≠ (U_nd.map ∘ K_nd.map ∘ F_ex.map ∘ C_nd.map) (4 : ℤ) := by
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
  rcases eq_or_ne x 5 with h5 | h5
  · subst h5; norm_num
  rcases eq_or_ne x (-5) with hn5 | hn5
  · subst hn5; norm_num
  · have h1 : ¬ (-x = 5) := by omega
    have h2 : ¬ (-x = -5) := by omega
    simp [h1, h2, h5, hn5]

theorem exists_order_dependent :
    ∃ (M : GenerativeManifold.{0}) (C : CompressionOp M) (K : CurvatureOp M)
      (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
      GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x :=
  ⟨intManifold, C_nd, K_nd, F_ex, U_nd, (4 : ℤ), nonCommutativity_nondegenerate⟩

theorem not_forall_order_dependent :
    ¬ (∀ (M : GenerativeManifold.{0}) (C : CompressionOp M) (K : CurvatureOp M)
      (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
      GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x) :=
  fun h => h intManifold C_ex K_ex F_sym U_ex (5 : ℤ) (commuting_instance 5)

theorem thm_5_3_is_exactly_existential :
    (∃ (M : GenerativeManifold.{0}) (C : CompressionOp M) (K : CurvatureOp M)
      (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
      GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x)
    ∧
    ¬ (∀ (M : GenerativeManifold.{0}) (C : CompressionOp M) (K : CurvatureOp M)
      (F : FoldOp M) (U : UnfoldOp M) (x : M.carrier),
      GenerativeOp M C K F U x ≠ (U.map ∘ K.map ∘ F.map ∘ C.map) x) :=
  ⟨exists_order_dependent, not_forall_order_dependent⟩

end Theorem53NonCommutativity
