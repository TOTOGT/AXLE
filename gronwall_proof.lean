-- ============================================================================
-- GRONWALL PROOF CLOSURE — AXLE v6.1
-- Replaces the sorry in gronwall_contraction_below_stability_radius
-- ============================================================================

-- This proof closes the sorry in Main_v6.lean at line 658.
-- The theorem statement is:
--   (canonicalTriple.mu_max + 3 * ε) * (2 * Real.pi) < 0
-- given ε < stabilityRadius = 1/3.
--
-- The proof does NOT require the full Gronwall ODE integration.
-- It only proves the sign of the decay exponent — which is pure arithmetic
-- plus Real.pi_pos. The ODE integration itself remains in the books;
-- what Lean verifies here is that the exponent is negative, which is the
-- necessary condition for contraction.
--
-- This is an honest distinction: we are not claiming to have verified
-- the full Gronwall lemma in Lean. We are verifying that the decay
-- exponent (μmax + 3ε) · T* is negative whenever ε < ε₀ = 1/3.

theorem gronwall_contraction_below_stability_radius
    (ε : ℝ) (hε : ε < stabilityRadius) :
    (canonicalTriple.mu_max + 3 * ε) * (2 * Real.pi) < 0 := by
  -- Unfold definitions
  simp only [canonicalTriple, stabilityRadius] at *
  -- Now: mu_max = -2, stabilityRadius = 1/3
  -- Goal: (-2 + 3 * ε) * (2 * Real.pi) < 0
  -- Step 1: Show -2 + 3 * ε < 0
  have h1 : -2 + 3 * ε < 0 := by linarith
  -- Step 2: Show 2 * Real.pi > 0
  have h2 : (0 : ℝ) < 2 * Real.pi := by positivity
  -- Step 3: Negative times positive is negative
  exact mul_neg_of_neg_of_pos h1 h2

-- ============================================================================
-- AUDIT NOTE (v6.1 → v6.2):
--
-- What this closes:
--   The sorry at line 658 of Main_v6.lean.
--   The decay exponent (μmax + 3ε) · T* < 0 for all ε < 1/3 is now proved.
--
-- What this does NOT close:
--   The full Gronwall ODE integration (that the contraction bound follows
--   from the exponent sign). That remains in the book proofs (GTCT-2026-001 §5).
--   The sorry comment should be updated to reflect this distinction:
--   the exponent sign is proved; the ODE application is in the books.
--
-- Sorry count after this closure: 8 (down from 9)
-- Axiom count: unchanged — 0 beyond Mathlib
--
-- Remaining open:
--   dm3_euler_preservation          → Mathlib simplicial homology (not in 4.28.0)
--   dm3_volume_invariant            → Mathlib measure theory for fold maps
--   g6_lattice_invariant            → Crystal.G6 module pending
--   g6_symmetry_preservation        → Crystal.G6 module pending
--   separation_theorem              → Issue 6
--   regeneration_loop_invariant     → Issue 6
--   regeneration_hierarchy_mahlo_unconditional → Issue 6
--   gtct_t1                         → Issue 6 + Floquet theory
--
-- Pablo Nogueira Grossi · G6 LLC · Newark NJ · 2026
-- ============================================================================
