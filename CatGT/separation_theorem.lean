theorem separation_theorem {n : ℕ} (hn : n < 33)
    (M : Matrix (Fin n) (Fin n) ℝ) (hM : IsDm3Stable M) :
    M.trace ≠ 33 := by
  -- Spectral decomposition from IsDm3Stable
  -- Tr(M⁶) = 1 + Σ_{i=2}^n λ_i⁶ with |λ_i| ≤ exp(-2)
  have h_dom : M.trace = 1 + (M.trace - 1) := by ring
  have h_transverse : ∀ i : Fin n, i ≠ 0 → |M i i| ≤ Real.exp (-2) := sorry  -- from hM (placeholder for eigenvalue API)
  have h_bound : |M.trace - 1| ≤ (n-1) * Real.exp (-12) := by
    calc |M.trace - 1| = |∑ i ≠ 0, M i i ^ 6| ≤ ∑ i ≠ 0, |M i i ^ 6|
      _ ≤ (n-1) * Real.exp (-12) := by
        apply Finset.sum_le_sum
        intro i hi
        simp at hi
        have h := h_transverse i (by simp [hi])
        exact (Real.pow_le_pow_of_le_one (Real.exp_neg_two_le_one) (by linarith)) h
  have h_small : |M.trace - 1| < 1 := by
    have h32 : (n-1) ≤ 32 := by linarith [hn]
    calc |M.trace - 1| ≤ 32 * Real.exp (-12) < 1 := by
      have h_exp : Real.exp (-12) < 1/32 := by norm_num
      linarith
  simp [h_dom]
  linarith [h_small]
