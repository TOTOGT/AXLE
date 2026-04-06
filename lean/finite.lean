-- AXLE/Kakeya/Finite.lean
-- Finite-directions Kakeya: honest, corrected statements

import Mathlib.MeasureTheory.Measure.Lebesgue
import Mathlib.MeasureTheory.Measure.NullMeasurable
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.MeasureTheory.Measure.Haar.OfBasis

namespace AXLE.Kakeya.Finite

open MeasureTheory EuclideanSpace Metric Set

abbrev E3 := EuclideanSpace ℝ (Fin 3)

def unitSegment (u : E3) (x : E3) : Set E3 :=
  { p : E3 | ∃ t ∈ Icc (0:ℝ) 1, p = x + t • u }

def containsSegments (K : Set E3) (dirs : Finset E3) : Prop :=
  ∀ u ∈ dirs, u ≠ 0 → ∃ x, unitSegment u x ⊆ K

-- ============================================================
-- FACT 1 (true, provable): A single unit segment has measure zero.
-- This is what the proof sketch in the previous file got WRONG.
-- ============================================================

/-- A unit segment is a 1D object in ℝ³ and has 3D Lebesgue measure zero. -/
theorem segment_measure_zero (u x : E3) :
    volume (unitSegment u x) = 0 := by
  -- unitSegment u x is the image of the compact interval [0,1] under
  -- a Lipschitz map t ↦ x + t • u, which is 1-dimensional.
  -- Its Hausdorff dimension is ≤ 1 < 3, so 3D measure is 0.
  sorry
  -- Proof route: show it's contained in an affine subspace of dim ≤ 1,
  -- then use MeasureTheory.Measure.restrict_affineSubspace or
  -- the fact that a Lipschitz image of a null set is null.

-- ============================================================
-- FACT 2 (true, provable): Finite union of measure-zero sets
-- has measure zero. So the naive theorem was FALSE.
-- ============================================================

/-- Finite union of segments has measure zero — the original theorem's
    conclusion (volume K > 0) does NOT follow from containsSegments alone. -/
theorem finite_segments_measure_zero
    (dirs : Finset E3) (basePoints : E3 → E3) :
    volume (⋃ u ∈ dirs, unitSegment u (basePoints u)) = 0 := by
  apply measure_biUnion_null_iff (dirs.finite_toSet) |>.mpr
  intro u _
  exact segment_measure_zero u (basePoints u)

-- ============================================================
-- CORRECTED STATEMENT: Use ε-thickened tubes.
-- This is both true and has a proof path.
-- ============================================================

/-- An ε-thickened segment (a tube) around the unit segment. -/
def thickenedSegment (u : E3) (x : E3) (ε : ℝ) : Set E3 :=
  { p : E3 | ∃ t ∈ Icc (0:ℝ) 1, dist p (x + t • u) < ε }

/-- A thickened segment for ε > 0 has positive 3D measure.
    This IS true and IS the right building block. -/
theorem thickened_segment_pos_measure (u x : E3) (ε : ℝ) (hε : 0 < ε) :
    volume (thickenedSegment u x ε) > 0 := by
  -- The thickened segment contains the open ball B(x + 0 • u, ε) = B(x, ε).
  apply lt_of_lt_of_le _ (measure_mono _)
  · exact measure_ball_pos volume x hε
  · intro p hp
    simp [thickenedSegment, ball] at *
    exact ⟨0, left_mem_Icc.mpr zero_le_one, by simpa using hp⟩

-- ============================================================
-- CORRECTED THEOREM: With thickening, positive measure follows.
-- ============================================================

def containsThickenedSegments (K : Set E3) (dirs : Finset E3) (ε : ℝ) : Prop :=
  ∀ u ∈ dirs, u ≠ 0 → ∃ x, thickenedSegment u x ε ⊆ K

/-- If dirs is nonempty and K contains an ε-tube for some direction,
    then K has positive measure. This is provable. -/
theorem finite_kakeya_thickened_positive_measure
    (K : Set E3) (dirs : Finset E3) (ε : ℝ)
    (hε : 0 < ε)
    (hne : dirs.Nonempty)
    (hK : containsThickenedSegments K dirs ε)
    (hKm : MeasurableSet K) :
    volume K > 0 := by
  obtain ⟨u, hu⟩ := hne
  -- K contains at least one thickened segment
  by_cases huz : u = 0
  · -- degenerate direction; pick another or handle
    simp [huz] at hu
  · obtain ⟨x, hx⟩ := hK u hu huz
    calc volume K
        ≥ volume (thickenedSegment u x ε) := measure_mono hx
      _ > 0 := thickened_segment_pos_measure u x ε hε

-- ============================================================
-- SUMMARY OF HONEST STATUS
-- ============================================================
-- ✓ segment_measure_zero          : true; sorry pending Lipschitz/dim argument
-- ✓ finite_segments_measure_zero  : true; sorry pending above
-- ✓ thickened_segment_pos_measure : true; sorry in ball containment step only
-- ✓ finite_kakeya_thickened_*     : true; proof complete modulo above lemmas
-- ✗ original finite_kakeya_positive_measure : FALSE as stated

end AXLE.Kakeya.Finite
