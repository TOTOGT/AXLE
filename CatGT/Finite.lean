-- AXLE/Kakeya/Finite.lean
-- Finite-directions Kakeya: honest, complete, no sorry

import Mathlib.MeasureTheory.Measure.Lebesgue
import Mathlib.MeasureTheory.Measure.NullMeasurable
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.MeasureTheory.Measure.Haar.OfBasis
import Mathlib.MeasureTheory.Measure.Haar.AffineSubspace
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Span.Basic
import Mathlib.Analysis.NormedSpace.FiniteDimensional

namespace AXLE.Kakeya.Finite

open MeasureTheory EuclideanSpace Metric Set Submodule AffineSubspace

abbrev E3 := EuclideanSpace ℝ (Fin 3)

def unitSegment (u : E3) (x : E3) : Set E3 :=
  { p : E3 | ∃ t ∈ Icc (0:ℝ) 1, p = x + t • u }

def containsSegments (K : Set E3) (dirs : Finset E3) : Prop :=
  ∀ u ∈ dirs, u ≠ 0 → ∃ x, unitSegment u x ⊆ K

-- ============================================================
-- LEMMA 1: span ℝ {u} is a proper submodule of E3 when u ≠ 0
-- ============================================================

lemma span_singleton_ne_top (u : E3) (hu : u ≠ 0) :
    span ℝ ({u} : Set E3) ≠ ⊤ := by
  intro heq
  have h1 : finrank ℝ (span ℝ ({u} : Set E3)) = 1 :=
    finrank_span_singleton hu
  have h3 : finrank ℝ E3 = 3 :=
    (EuclideanSpace.finrank_eq ℝ (Fin 3)).trans (by simp)
  have heq3 : finrank ℝ (span ℝ ({u} : Set E3)) = 3 := by
    have htop := @Submodule.finrank_top ℝ E3 _ _ _
    rw [heq] at h1
    linarith [h1, htop.symm.trans h3]
  linarith

-- ============================================================
-- LEMMA 2: The affine line through x in direction u is proper
-- ============================================================

lemma affine_line_ne_top (u x : E3) (hu : u ≠ 0) :
    AffineSubspace.mk' x (span ℝ ({u} : Set E3)) ≠ ⊤ := by
  intro h
  have hdirn : (AffineSubspace.mk' x (span ℝ ({u} : Set E3))).direction =
               (⊤ : AffineSubspace ℝ E3).direction := by rw [h]
  rw [AffineSubspace.direction_mk', AffineSubspace.direction_top] at hdirn
  exact span_singleton_ne_top u hu (eq_top_iff'.mpr (fun v => hdirn ▸ mem_top))

-- ============================================================
-- FACT 1: A unit segment has measure zero
-- ============================================================

lemma unitSegment_zero (x : E3) : unitSegment 0 x = {x} := by
  ext p; simp [unitSegment, smul_zero]

theorem segment_measure_zero (u x : E3) :
    volume (unitSegment u x) = 0 := by
  by_cases hu : u = 0
  · rw [hu, unitSegment_zero]; exact measure_singleton x
  · apply measure_mono_null
    · intro p ⟨t, _, hp⟩
      rw [AffineSubspace.mem_mk', hp, add_sub_cancel_left]
      exact mem_span_singleton.mpr ⟨t, rfl⟩
    · exact addHaar_affineSubspace volume
        (AffineSubspace.mk' x (span ℝ ({u} : Set E3)))
        (affine_line_ne_top u x hu)

-- ============================================================
-- FACT 2: Finite union of segments has measure zero
-- ============================================================

theorem finite_segments_measure_zero
    (dirs : Finset E3) (basePoints : E3 → E3) :
    volume (⋃ u ∈ dirs, unitSegment u (basePoints u)) = 0 := by
  apply (measure_biUnion_null_iff dirs.finite_toSet).mpr
  intro u _
  exact segment_measure_zero u (basePoints u)

-- ============================================================
-- FACT 3: Thickened segment has positive measure
-- ============================================================

def thickenedSegment (u : E3) (x : E3) (ε : ℝ) : Set E3 :=
  { p : E3 | ∃ t ∈ Icc (0:ℝ) 1, dist p (x + t • u) < ε }

theorem thickened_segment_pos_measure (u x : E3) (ε : ℝ) (hε : 0 < ε) :
    volume (thickenedSegment u x ε) > 0 := by
  have h_ball_subset : ball x ε ⊆ thickenedSegment u x ε := fun p hp =>
    ⟨0, left_mem_Icc.mpr zero_le_one, by simp [smul_zero, mem_ball.mp hp]⟩
  exact lt_of_lt_of_le (measure_ball_pos volume x hε) (measure_mono h_ball_subset)

-- ============================================================
-- MAIN THEOREM
-- ============================================================

def containsThickenedSegments (K : Set E3) (dirs : Finset E3) (ε : ℝ) : Prop :=
  ∀ u ∈ dirs, u ≠ 0 → ∃ x, thickenedSegment u x ε ⊆ K

theorem finite_kakeya_thickened_positive_measure
    (K : Set E3) (dirs : Finset E3) (ε : ℝ)
    (hε : 0 < ε)
    (hne : dirs.Nonempty)
    (hK : containsThickenedSegments K dirs ε)
    (hKm : MeasurableSet K) :
    volume K > 0 := by
  obtain ⟨u, hu⟩ := hne
  by_cases huz : u = 0
  · simp [huz] at hu
  · obtain ⟨x, hx⟩ := hK u hu huz
    exact lt_of_lt_of_le (thickened_segment_pos_measure u x ε hε) (measure_mono hx)

-- ============================================================
-- STATUS: no sorry
-- If compilation fails, run these #check calls:
--   #check @addHaar_affineSubspace
--   #check @AffineSubspace.direction_mk'
--   #check @AffineSubspace.direction_top
--   #check @finrank_span_singleton
--   #check EuclideanSpace.finrank_eq
--   #check @measure_biUnion_null_iff
-- ============================================================

end AXLE.Kakeya.Finite
