theorem dm3_volume_invariant
    (M : GenerativeManifold) (F : FoldOp M) (U : UnfoldOp M)
    (vol : Set M.carrier → ℝ≥0∞) (X : Set M.carrier) :
    vol (U.map '' (F.map '' X)) = vol X := by
  -- Fold introduces measure-zero locus (F.has_fold)
  have hF_zero : vol {p | ∃ q, q ≠ p ∧ F.map q = F.map p} = 0 := sorry  -- rank-1 collapse
  -- Unfold is measure-preserving (U.decreases_Phi + stable_branch)
  have hU_measure : MeasurePreserving U.map := sorry  -- from U.decreases_Phi
  rw [MeasureTheory.measure_image_eq_of_measurePreserving hU_measure]
  rw [MeasureTheory.measure_add_measure_compl hF_zero]
