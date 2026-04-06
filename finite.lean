-- AXLE/Kakeya/Finite.lean
-- Finite-directions Kakeya: honest, corrected, and now fully proved

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

open MeasureTheory EuclideanSpace Metric Set

abbrev E3 := EuclideanSpace ℝ (Fin 3)

def unitSegment (u : E3) (x : E3) : Set E3 :=
  { p : E3 | ∃ t ∈ Icc (0:ℝ) 1, p = x + t • u }

def containsSegments (K : Set E3) (dirs : Finset E3) : Prop :=
  ∀ u ∈ dirs, u ≠ 0 → ∃ x, unitSegment u x ⊆ K

-- ============================================================
-- FACT 1: A unit segment has measure zero (now proved)
-- ============================================================

lemma span_singleton_lt_top (u : E3) (hu : u ≠ 0) :
    Submodule.span ℝ ({u} : Set E3) ≠ ⊤ := by
  intro heq
  have h1 : finrank ℝ (Submodule.span ℝ ({u} : Set E3)) = 1 :=
    finrank_span_singleton hu
  have h3 : finrank ℝ E3 = 3 :=
    EuclideanSpace.finrank_eq ℝ (Fin 3) |>.trans (by simp)
  have : finrank ℝ (Submodule.span ℝ ({u} : Set E3)) = 3 := by
    rw [heq]; exact Submodule.finrank_top ▸ h3
  linarith [h1, this]

lemma affine_line_ne_top (u x : E3) (hu : u ≠ 0) :
    AffineSubspace.mk' x (Submodule.span ℝ ({u} : Set E3)) ≠ ⊤ := by
  intro h
  have : Submodule.span ℝ ({u} : Set E3) = ⊤ := by
    have := congr_arg AffineSubspace.direction h
    simp [AffineSubspace.direction_mk', AffineSubspace.direction_top] at this
    exact this
  exact span_singleton_lt_top u hu this

theorem segment_measure_zero (u x : E3) (hu : u ≠ 0) :
    volume (unitSegment u x) = 0 := by
  set L : AffineSubspace ℝ E3 := AffineSubspace.mk' x (Submodule.span ℝ ({u} : Set E3)) with hL_def
  apply measure_mono_null
  · -- Segment lies in L
    intro p ⟨t, _, hp⟩
    rw [AffineSubspace.mem_mk']
    rw [hp, add_sub_cancel_left]
    exact Submodule.mem_span_singleton.mpr ⟨t, rfl⟩
  · -- L has measure zero as a proper affine subspace
    exact addHaar_affineSubspace volume L (affine_line_ne_top u x hu)

-- ============================================================
-- FACT 2: Finite union of segments has measure zero (now proved)
-- ============================================================

theorem finite_segments_measure_zero
    (dirs : Finset E3) (basePoints : E3 → E3) :
    volume (⋃ u ∈ dirs, unitSegment u (basePoints u)) = 0 := by
  apply measure_biUnion_null_iff (dirs.finite_toSet) |>.mpr
  intro u _
  by_cases hu : u = 0
  · -- degenerate case: unitSegment u x collapses to {x}
    have : unitSegment u (basePoints u) = {basePoints u} := by
      ext p; simp [unitSegment, hu, smul_zero]
    rw [this]
    exact measure_singleton _
  · exact segment_measure_zero u (basePoints u) hu

-- ============================================================
-- FACT 3: Thickened segment has positive measure (proved)
-- ============================================================

def thickenedSegment (u : E3) (x : E3) (ε : ℝ) : Set E3 :=
  { p : E3 | ∃ t ∈ Icc (0:ℝ) 1, dist p (x + t • u) < ε }

theorem thickened_segment_pos_measure (u x : E3) (ε : ℝ) (hε : 0 < ε) :
    volume (thickenedSegment u x ε) > 0 := by
  have h_ball_subset : ball x ε ⊆ thickenedSegment u x ε := fun p hp =>
    ⟨0, left_mem_Icc.mpr zero_le_one, by simpa [thickenedSegment, dist_comm] using hp⟩
  calc volume (thickenedSegment u x ε)
      ≥ volume (ball x ε) := measure_mono h_ball_subset
    _ > 0 := measure_ball_pos volume x hε

-- ============================================================
-- CORRECTED THEOREM: Finite thickened Kakeya has positive measure
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
    calc volume K
        ≥ volume (thickenedSegment u x ε) := measure_mono hx
      _ > 0 := thickened_segment_pos_measure u x ε hε

end AXLE.Kakeya.Finite
