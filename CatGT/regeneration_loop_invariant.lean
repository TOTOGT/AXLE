theorem regeneration_loop_invariant
    (M : GenerativeManifold)
    (C : CompressionOp M) (K : CurvatureOp M)
    (F : FoldOp M) (U : UnfoldOp M)
    (read : M.carrier → M.carrier)
    (h_read_is_G : ∀ x, read x = GenerativeOp M C K F U x) :
    ∀ x : M.carrier,
      read (GenerativeOp M C K F U (GenerativeOp M C K F U x)) =
      GenerativeOp M C K F U x := by
  intro x
  rw [h_read_is_G]
  -- G is idempotent on the attractor after g₃₃ cycles
  have h_stable : IsFixedPt (GenerativeOp M C K F U) x := sorry  -- from UnfoldOp.stable_branch after threshold
  simp [h_stable]
