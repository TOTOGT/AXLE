-- probe_core.lean -- the two AXLE files that actually carry sorry-free content.
--
-- WHY THESE TWO. The verification table of the nuclear-matter paper cites
-- `AXLE_v8.1.lean`: 6 declarations, 0 proved, all six admitted. `lean/AXLE.lean`
-- and `CatGT/AXLE8.lean` have the same shape. The two files below are where the
-- sorry-free content is, and neither appears in that table.
--
-- Generated from the sources, not hand-listed: every declaration named here was
-- read out of its file with comments stripped and a `sorry` check run on its own
-- proof body. Admitted declarations are deliberately NOT named -- the gate exists
-- to punish quiet admission, not disclosure.
--
-- The original imports of both files are pinned to Mathlib v4.14.0 and do not all
-- resolve under the v4.32.0 that geometry has built. `import Mathlib` is the
-- version-independent form and is a cache hit where Mathlib is already built.

import Mathlib


-- PrincipiaOrthogona1/PrincipiaVol1.lean  --  62 sorry-free declarations
#print axioms PrincipiaVol1.V_critical_at_one
#print axioms PrincipiaVol1.V_second_deriv_at_one
#print axioms PrincipiaVol1.V_second_deriv_ne_zero
#print axioms PrincipiaVol1.V_at_one
#print axioms PrincipiaVol1.V_factored
#print axioms PrincipiaVol1.contactCoeff_neg
#print axioms PrincipiaVol1.contactCoeff_ne_zero
#print axioms PrincipiaVol1.gronwall_radius
#print axioms PrincipiaVol1.epsilon0_of_two
#print axioms PrincipiaVol1.epsilon0_of_three
#print axioms PrincipiaVol1.epsilon0_of_eq_third_iff
#print axioms PrincipiaVol1.gronwall_radius_pos
#print axioms PrincipiaVol1.gronwall_radius_lt_one
#print axioms PrincipiaVol1.basin_asymmetry
#print axioms PrincipiaVol1.basin_asymmetry_at_canonical_r_star
#print axioms PrincipiaVol1.mu_canonical
#print axioms PrincipiaVol1.mu_dm3_neg
#print axioms PrincipiaVol1.Phi_pos
#print axioms PrincipiaVol1.dPhi_pos
#print axioms PrincipiaVol1.dPhi_at_threshold
#print axioms PrincipiaVol1.noiseTolerance
#print axioms PrincipiaVol1.gronwall_contraction_below_stability_radius
#print axioms PrincipiaVol1.exp_neg_two_le
#print axioms PrincipiaVol1.exp_neg_twelve_le
#print axioms PrincipiaVol1.transverse_sum_bound
#print axioms PrincipiaVol1.spectral_trace_ne_33
#print axioms PrincipiaVol1.separation_theorem
#print axioms PrincipiaVol1.separation_trace_first
#print axioms PrincipiaVol1.coherent_directions_realise_33
#print axioms PrincipiaVol1.transverse_sum_bound_general
#print axioms PrincipiaVol1.spectral_trace_ne_33_upto
#print axioms PrincipiaVol1.separation_fails_in_high_dimension
#print axioms PrincipiaVol1.dm3_hypothesis_nonvacuous
#print axioms PrincipiaVol1.v6_separation_statement_is_false
#print axioms PrincipiaVol1.v6_statement_false_at_dimension_five
#print axioms PrincipiaVol1.sup_strictMono_isLimit
#print axioms PrincipiaVol1.closurePoints_unbounded
#print axioms PrincipiaVol1.sup_lt_of_regular
#print axioms PrincipiaVol1.pickAbove_spec
#print axioms PrincipiaVol1.chain_bound
#print axioms PrincipiaVol1.chain_mem
#print axioms PrincipiaVol1.chain_strictMono
#print axioms PrincipiaVol1.closurePoints_stationary
#print axioms PrincipiaVol1.nextLevel_layer_count_gt
#print axioms PrincipiaVol1.regeneration_unbounded
#print axioms PrincipiaVol1.ordinalNextLevel_is_closure_point
#print axioms PrincipiaVol1.ordinal_regeneration_unbounded
#print axioms PrincipiaVol1.regeneration_hierarchy_mahlo
#print axioms PrincipiaVol1.crystal_aspect_ratio
#print axioms PrincipiaVol1.aspect_ratio_encodes_invariants
#print axioms PrincipiaVol1.unfold_stable_branch_is_vacuous
#print axioms PrincipiaVol1.foldMap_not_odd
#print axioms PrincipiaVol1.foldMap_branch_subset
#print axioms PrincipiaVol1.foldSym_branch_subset
#print axioms PrincipiaVol1.shrinkMap_sq_le
#print axioms PrincipiaVol1.nonCommutativity_instance
#print axioms PrincipiaVol1.nonCommutativity_nondegenerate
#print axioms PrincipiaVol1.commuting_instance
#print axioms PrincipiaVol1.compression_permits_identity
#print axioms PrincipiaVol1.exists_order_dependent
#print axioms PrincipiaVol1.not_forall_order_dependent
#print axioms PrincipiaVol1.thm_5_3_is_exactly_existential

-- AutophagyDm3_v2.lean  --  24 sorry-free declarations
#print axioms AutophagyDm3.contactCoeff_neg
#print axioms AutophagyDm3.contactCoeff_ne_zero
#print axioms AutophagyDm3.V_critical_at_one
#print axioms AutophagyDm3.V_second_deriv_at_one
#print axioms AutophagyDm3.V_second_deriv_ne_zero
#print axioms AutophagyDm3.V_at_one
#print axioms AutophagyDm3.V_factored
#print axioms AutophagyDm3.V_double_root
#print axioms AutophagyDm3.mu_canonical
#print axioms AutophagyDm3.mu_dm3
#print axioms AutophagyDm3.mu_dm3_neg
#print axioms AutophagyDm3.gronwall_radius
#print axioms AutophagyDm3.gronwall_radius_pos
#print axioms AutophagyDm3.gronwall_radius_lt_one
#print axioms AutophagyDm3.basin_asymmetry
#print axioms AutophagyDm3.Φ_pos
#print axioms AutophagyDm3.dΦ_pos
#print axioms AutophagyDm3.dΦ_at_threshold
#print axioms AutophagyDm3.contactForm_nondeg_scalar
#print axioms AutophagyDm3.contactForm_orientation
#print axioms AutophagyDm3.V_is_morse_at_one
#print axioms AutophagyDm3.not_isMorseCritical_const
#print axioms AutophagyDm3.dm3_basin_compact
#print axioms AutophagyDm3.dm3_basin_nonempty

-- NbonacciLadder.lean  --  13 sorry-free declarations
-- This is the file that backs Sec. 25.4's ceiling claim ("no n-bonacci constant
-- exceeds 2"). `nbonacci_lt_two_pow` proves the INTEGER form: any k-bonacci
-- sequence seeded below powers of two stays strictly below 2^n, for every k.
-- That gives the growth rate eta_k <= 2. It does NOT give strict eta_k < 2 --
-- that needs a limit argument no file here contains -- and it says nothing about
-- the fractal dimension d_n = log(n)/log(eta_n), for which there is no Lean
-- anywhere in the corpus.
#print axioms NbonacciLadder.sumPrev_mono
#print axioms NbonacciLadder.sumPow_succ
#print axioms NbonacciLadder.two_pow_pos
#print axioms NbonacciLadder.sumPow_lt
#print axioms NbonacciLadder.strong_ind
#print axioms NbonacciLadder.nbonacci_le_two_pow
#print axioms NbonacciLadder.nbonacci_lt_two_pow
#print axioms NbonacciLadder.tribonacci_lt_two_pow
#print axioms NbonacciLadder.trib3_seed
#print axioms NbonacciLadder.trib3_rec
#print axioms NbonacciLadder.trib3_lt_two_pow
#print axioms NbonacciLadder.hrec_is_necessary
#print axioms NbonacciLadder.hseed_is_necessary
