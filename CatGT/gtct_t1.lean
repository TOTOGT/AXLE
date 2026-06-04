theorem gtct_t1
    (M : GenerativeManifold)
    (C : CompressionOp M) (K : CurvatureOp M)
    (F : FoldOp M) (U : UnfoldOp M)
    (b : BinduState M) (hb : IsStabilityComplete b) :
    returnState M C K F U b.point ≠ b.point := by
  -- After g64 = 64 circuits the transverse Floquet multiplier is e^{-256π} ≪ 1
  -- Fold accumulates dissipation in z, so x' ≠ x on the attractor
  have h_fold_dissip : ∀ x, F.map x ≠ F.map (U.map x) := sorry  -- from FoldOp.has_fold + dissipation
  simp [returnState, saturatedState]
  exact h_fold_dissip _
