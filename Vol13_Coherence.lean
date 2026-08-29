-- SPDX-License-Identifier: MIT
-- ============================================================================
/-
  Principia Orthogona · Part II · Volume XIII — Coherence
  Chapter 3 core:  "On the Nose, or Up to Something"

  QUESTION.  The series writes  G = U ∘ F ∘ K ∘ C  unbracketed, across three
  years and (measured 2026-08-29) 76 files.  An unbracketed four-fold composite
  denotes one thing only if composition associates.  Does it?

  ANSWER, IN ADVANCE.  It depends on what the operators are, and Mathlib states
  both cases in its own source:

      Mathlib/CategoryTheory/Functor/Category.lean:192
        protected theorem assoc (F : C ⥤ D) (G : D ⥤ E) (H : E ⥤ E') :
          (F ⋙ G) ⋙ H = F ⋙ G ⋙ H          -- EQUATION.  strict.

      Mathlib/CategoryTheory/Bicategory/Basic.lean:69
        associator (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d) :
          (f ≫ g) ≫ h ≅ f ≫ g ≫ h            -- ISOMORPHISM.  weak.

  So chapter 3 does not have one answer.  It has three, one per level of
  abstraction, and the series has never said which level it is working at.
  That is the finding.  This file makes the kernel state it.

  HOW TO RUN.  From the geometry repository, which has Mathlib built:
      cd ~/Desktop/geometry && lake env lean ~/Desktop/AXLE/Vol13_Coherence.lean

  Import paths checked against
  geometry/.lake/packages/mathlib/Mathlib on 2026-08-29, not assumed.
-/
-- ============================================================================

import Mathlib.CategoryTheory.Functor.Category
import Mathlib.CategoryTheory.Bicategory.Basic

namespace Vol13

open CategoryTheory

-- ============================================================================
-- LEVEL 0 · ENDOFUNCTIONS
--
-- This is what the corpus actually has today.  AXLE defines
--     PhaseVector := Fin 12 → ℝ
--     applyG : PhaseVector → PhaseVector
-- which are plain functions on a type.  At this level associativity is not a
-- theorem worth having: it holds definitionally, and `rfl` closes it.
-- ============================================================================

section Endofunctions

variable {X : Type*}

/-- The chain as the corpus writes it, at the level the corpus writes it. -/
def chain₀ (C K F U : X → X) : X → X := U ∘ F ∘ K ∘ C

/-- Two of the five bracketings agree on the nose. -/
theorem chain₀_assoc (C K F U : X → X) :
    ((U ∘ F) ∘ K) ∘ C = U ∘ (F ∘ (K ∘ C)) := rfl

/-- And so do the rest.  Stated as a conjunction rather than one `rfl` so that
    a reader can see that four distinct expressions are being identified, not
    one expression restated. -/
theorem chain₀_bracketing_free (C K F U : X → X) :
    ((U ∘ F) ∘ K) ∘ C = (U ∘ F) ∘ (K ∘ C)
      ∧ (U ∘ F) ∘ (K ∘ C) = U ∘ (F ∘ (K ∘ C))
      ∧ U ∘ (F ∘ (K ∘ C)) = U ∘ ((F ∘ K) ∘ C) :=
  ⟨rfl, rfl, rfl⟩

end Endofunctions

-- ============================================================================
-- LEVEL 1 · ENDOFUNCTORS OF A CATEGORY
--
-- If the operators are functors, composition is STILL strict.  Mathlib's
-- `Functor.assoc` is an equation, not an isomorphism.  Rung 30 buys nothing
-- here, and Volume XIII would collapse to this section.
-- ============================================================================

section Endofunctors

variable {𝒞 : Type*} [Category 𝒞]

/-- The chain as a composite of endofunctors. -/
def chain₁ (C K F U : 𝒞 ⥤ 𝒞) : 𝒞 ⥤ 𝒞 := C ⋙ K ⋙ F ⋙ U

/-- Associativity via Mathlib's stated equation. -/
theorem chain₁_assoc (C K F U : 𝒞 ⥤ 𝒞) :
    ((C ⋙ K) ⋙ F) ⋙ U = C ⋙ K ⋙ F ⋙ U := by
  rw [Functor.assoc, Functor.assoc]

/-- The same, definitionally.  If this succeeds, functor composition is
    associative by computation and not merely by lemma — a stronger statement
    about how little coherence is needed at this level. -/
theorem chain₁_assoc_rfl (C K F U : 𝒞 ⥤ 𝒞) :
    ((C ⋙ K) ⋙ F) ⋙ U = C ⋙ K ⋙ F ⋙ U := rfl

/-- Iterated composition, the object the series actually cares about.
    `iterate₁ G 33` is the g⁰ → g³³ chain. -/
def iterate₁ (G : 𝒞 ⥤ 𝒞) : ℕ → (𝒞 ⥤ 𝒞)
  | 0     => 𝟭 𝒞
  | n + 1 => G ⋙ iterate₁ G n

/-- The 33-fold composite unfolds.  Non-vacuous: the two sides are
    syntactically different expressions. -/
theorem iterate₁_succ (G : 𝒞 ⥤ 𝒞) (n : ℕ) :
    iterate₁ G (n + 1) = G ⋙ iterate₁ G n := rfl

/-- Regrouping the iterate is free at this level.  This is the statement the
    series needs in order to write `G^[33]` without specifying a bracketing —
    and at level 1 it costs nothing. -/
theorem iterate₁_regroup (G : 𝒞 ⥤ 𝒞) (n : ℕ) :
    (G ⋙ G) ⋙ iterate₁ G n = G ⋙ (G ⋙ iterate₁ G n) :=
  Functor.assoc _ _ _

end Endofunctors

-- ============================================================================
-- LEVEL 2 · 1-ENDOMORPHISMS IN A BICATEGORY
--
-- Here the answer changes.  The two bracketings are NOT equal; they are
-- related by an invertible 2-morphism, the associator.  This is the level at
-- which Volume XIII has content, and the level the series has never claimed
-- to be working at.
-- ============================================================================

section Bicat

open Bicategory

variable {B : Type*} [Bicategory B] {b : B}

/-- The associator for the first three operators of the chain.  Note the type:
    an isomorphism of 1-morphisms, i.e. a 2-morphism together with an inverse.
    Nothing here asserts the two sides are equal. -/
def assoc₂ (C K F : b ⟶ b) : (C ≫ K) ≫ F ≅ C ≫ K ≫ F :=
  α_ C K F

/-- The associator is invertible in one direction … -/
theorem assoc₂_hom_inv (C K F : b ⟶ b) :
    (assoc₂ C K F).hom ≫ (assoc₂ C K F).inv = 𝟙 ((C ≫ K) ≫ F) :=
  (assoc₂ C K F).hom_inv_id

/-- … and in the other.  Together: the bracketings are isomorphic, which is
    strictly weaker than equal, and is exactly the gap Volume XIII is about. -/
theorem assoc₂_inv_hom (C K F : b ⟶ b) :
    (assoc₂ C K F).inv ≫ (assoc₂ C K F).hom = 𝟙 (C ≫ K ≫ F) :=
  (assoc₂ C K F).inv_hom_id

end Bicat

-- ============================================================================
-- FIXTURE
--
-- A gate that has never rejected anything is not known to work.  The axiom
-- probe below is a gate.  This declaration is deliberately contentless and
-- must appear in the report carrying the three permitted axioms and no
-- sorryAx — which is precisely what a real theorem looks like from the
-- outside.  Its presence is the reminder that the probe cannot distinguish
-- content from vacuity, and that reading the statements is still required.
-- ============================================================================

/-- FIXTURE · deliberately vacuous.  Compare its axiom report to the others. -/
theorem vacuity_control : True := trivial

end Vol13

-- ============================================================================
-- KERNEL AUDIT
--
-- Compiling is not proving.  These lines ask the kernel what each declaration
-- actually rests on.
--
-- EXPECTED: [propext, Classical.choice, Quot.sound] or a subset, on all of
-- them, and NO sorryAx anywhere.  This file admits nothing.
--
-- WHAT THE REPORT DOES NOT TELL YOU: whether `vacuity_control` says anything.
-- It does not.  That is the point of including it.
-- ============================================================================

#print axioms Vol13.chain₀_assoc
#print axioms Vol13.chain₀_bracketing_free
#print axioms Vol13.chain₁_assoc
#print axioms Vol13.chain₁_assoc_rfl
#print axioms Vol13.iterate₁_succ
#print axioms Vol13.iterate₁_regroup
#print axioms Vol13.assoc₂_hom_inv
#print axioms Vol13.assoc₂_inv_hom
#print axioms Vol13.vacuity_control
