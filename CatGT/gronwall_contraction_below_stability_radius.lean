theorem gronwall_contraction_below_stability_radius
    (ε : ℝ) (hε : ε < stabilityRadius) :
    (canonicalTriple.mu_max + 3 * ε) * (2 * Real.pi) < 0 := by
  simp [canonicalTriple, stabilityRadius]
  have h1 : canonicalTriple.mu_max = -2 := rfl
  have h2 : ε < 1/3 := hε
  linarith
