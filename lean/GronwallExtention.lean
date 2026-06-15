theorem return_map_contraction (ε : ℝ) (hε : ε < stabilityRadius) :
    ∃ κ < 1, ∀ deviations, dist (returnMap deviation) ≤ κ * dist deviation := by
  -- use the gronwall_... lemma + Gronwall inequality + exp bound
  sorry  -- or fill with your existing machinery
