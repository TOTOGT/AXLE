-- probe_vol2.lean — Principia Orthogona Volume II, kernel axiom report.
--
-- Asks the Lean KERNEL which axioms each named theorem actually depends on.
-- A theorem proved with `sorry` reports sorryAx here even though it compiled
-- without error, which is the point: compilation is not verification.
--
-- WHAT THIS PROBE CANNOT SEE, and why it is not the whole check.
-- `thm_A_contact_realization_fold` has conclusion `True`, and
-- `thm_B_threshold_equivalence` proves its biconditional from assumptions on
-- both sides. Both will appear below on the permitted axioms, because a
-- vacuous theorem is a true theorem. The axiom gate is necessary and not
-- sufficient; see tools/conclusion_scan.lean in the geometry repository.
--
-- Run:  lake env lean tools/verify-vol2/probe_vol2.lean

import PrincipiaOrthogona_v2.VolumeTwo

open PrincipiaOrthogona.VolumeTwo

-- §1 thresholds
#print axioms PrincipiaOrthogona.VolumeTwo.embodimentThreshold_pos
#print axioms PrincipiaOrthogona.VolumeTwo.toyModel_tau

-- §2 transverse eigenvalue (Proposition 4.2)
#print axioms PrincipiaOrthogona.VolumeTwo.eigenvalue_at_zero
#print axioms PrincipiaOrthogona.VolumeTwo.eigenvalue_neg_pos_z
#print axioms PrincipiaOrthogona.VolumeTwo.eigenvalue_limit
#print axioms PrincipiaOrthogona.VolumeTwo.vol2_contact_Theorem_3_3

-- §3 stability radius
#print axioms PrincipiaOrthogona.VolumeTwo.toyModel_epsilon0
#print axioms PrincipiaOrthogona.VolumeTwo.epsilon_zero_waddington
#print axioms PrincipiaOrthogona.VolumeTwo.entropy_lyapunov_duality

-- §4-§6 the three named theorems
#print axioms PrincipiaOrthogona.VolumeTwo.thm_A_contact_realization_fold
#print axioms PrincipiaOrthogona.VolumeTwo.thm_B_threshold_equivalence
#print axioms PrincipiaOrthogona.VolumeTwo.thm_C_singularity_bijection

-- §6b integrability, Level 1 only
#print axioms PrincipiaOrthogona.VolumeTwo.Theorem_15_2_integrability
#print axioms PrincipiaOrthogona.VolumeTwo.alternating_vanishes_beyond_dim

-- §6d added for V5, 2026-08-26. The first two close rows the V4 Appendix A
-- listed as PROVED against names that did not exist; the next two give
-- Theorem A real content beside its `True` placeholder; the last turns the
-- toyModel_tau docstring caveat into a theorem.
#print axioms PrincipiaOrthogona.VolumeTwo.thm_C_A1_surjective
#print axioms PrincipiaOrthogona.VolumeTwo.thm_C_not_bijective
#print axioms PrincipiaOrthogona.VolumeTwo.thm_A_regularization_pointwise
#print axioms PrincipiaOrthogona.VolumeTwo.thm_A_regularization_at_fold
#print axioms PrincipiaOrthogona.VolumeTwo.tau_eq_abs_mu_iff
