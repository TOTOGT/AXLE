# Volume II · Appendix A, corrected

Generated from `PrincipiaOrthogona_v2/VolumeTwo.lean` on 2026-08-26, after the
first successful build of that file, and checked by
`tools/verify-vol2/probe_vol2.lean` through `tools/axiom_gate.py`:
19/19 declarations kernel-checked, no `sorryAx`, no axiom outside
`[propext, Classical.choice, Quot.sound]` — and two of them on *no axioms at all*.

**This table is a claim about a file. Regenerate it from the file; do not edit
it by hand.** The published V4 table was hand-written and six of its twelve rows
named declarations that have never existed in any version of `VolumeTwo.lean`.

## Where the file is

`github.com/TOTOGT/AXLE` · `PrincipiaOrthogona_v2/VolumeTwo.lean`

The paper says `AXLE/lean/VolumeTwo.lean` in three places. That path does not
exist and returns 404. A second byte-identical copy sits at
`NASA/MoonBase/AXLE_lean_files/VolumeTwo.lean`.

To reproduce:

    git clone https://github.com/TOTOGT/AXLE && cd AXLE
    lake build PrincipiaVol2
    lake env lean tools/verify-vol2/probe_vol2.lean > /tmp/axioms.txt
    python3 tools/axiom_gate.py /tmp/axioms.txt 19

Pinned to Lean v4.14.0, Mathlib v4.14.0. The pin is part of the claim.

## The table

| Theorem / Lemma | Lean name | Status |
|---|---|---|
| τ > 0 (Thm 3.2) | `embodimentThreshold_pos` | proved |
| τ = 2 (Prop. 4.2) | `toyModel_tau` | proved |
| λ(0) = 0 (Prop. 4.2) | `eigenvalue_at_zero` | proved |
| λ(z) < 0 for z > 0 | `eigenvalue_neg_pos_z` | proved |
| λ(z) → μ_max | `eigenvalue_limit` | proved |
| Thm 3.3 stability certificate | `vol2_contact_Theorem_3_3` | proved |
| ε₀ = 1/3 (§4.6) | `toyModel_epsilon0` | proved |
| N_J\|_Γ = 0, Level 1 (Thm 15.2) | `Theorem_15_2_integrability` | proved |
| alternating m-linear form = 0 when m > dim | `alternating_vanishes_beyond_dim` | proved |
| Thm C, unique preimages of A₂ and A₃ | `thm_C_singularity_bijection` | proved — **see note 3** |
| Thm B, μ_max < 0 ⟺ τ > 0 | `thm_B_threshold_equivalence` | **trivial — see note 2** |
| Thm A, fold ↔ contact correction | `thm_A_contact_realization_fold` | **placeholder — see note 1** |
| ε₀ = 1/3, Waddington reading | `epsilon_zero_waddington` | duplicate of `toyModel_epsilon0` |
| μ_max + τ = 0 | `entropy_lyapunov_duality` | arithmetic — see note 4 |
| Gronwall asymmetry, r* = 0.77594059 | — | **no Lean declaration exists** |
| A₁ surjectivity | `thm_C_A1_surjective` | proved — **added V5**; no axioms |
| the map is *not* a bijection | `thm_C_not_bijective` | proved — **added V5**; no axioms |
| Thm A, correction vanishes off the fold | `thm_A_regularization_pointwise` | proved — **added V5** |
| Thm A, correction constant on the fold | `thm_A_regularization_at_fold` | proved — **added V5** |
| τ = \|μ\| iff \|μ\| = 2 | `tau_eq_abs_mu_iff` | proved — **added V5** |
| N_J\|_ξ = 0 (Level 2d) | — | OP4, open, not yet statable |
| N_J\|_M = 0 (Level 2d+t) | — | OP5, open, depends on OP4 |

## Notes that must travel with the table

**1. Theorem A is not a `sorry`; its conclusion is `True`.**

```lean
theorem thm_A_contact_realization_fold (sys : DM3System) (S H_diss : ℝ → ℝ)
    (hS : ...) (hH : ...) : True := by trivial
```

This matters more than a sorry would. A `sorry` reports `sorryAx` and fails a
kernel gate; `True := by trivial` passes every axiom check ever run against it.
The file's own comment says `OPEN: Replace True with actual convergence
statement`. The published table reported this row as `sorry ★★★★`, which
overstates what is there. The obligation itself is real and unchanged:
distributional convergence of `exp(−βz)` to `Θ` as `β → ∞`.

**2. Theorem B's biconditional is proved from assumptions on both sides.**

```lean
  constructor
  · intro _; exact embodimentThreshold_pos c κ_noise hc hk
  · intro _; exact sys.mu_neg
```

Both branches discard the incoming hypothesis. The right-hand side follows from
`hc` and `hk` alone; the left-hand side is `sys.mu_neg`, a *field* of the
`DM3System` structure, so `μ_max < 0` is assumed at declaration. Each half is
independently true and the arrow carries nothing. The published table listed
this content under `thm_B_mu_iff_tau` as ✓ proved and a separate
`thm_B_full_chain` as sorry ★★★★★; neither name exists. The prose proof of the
full chain in §3.3 is unaffected — only the claim that Lean witnesses it.

**3. Theorem C is a surjection, not a bijection.**

`DM3Bifurcation` has four constructors, `WhitneySingularity` three, and
`singularityCorrespondence` sends both `contact_hopf` and `saddle_node` to `A₁`.
A four-element domain mapping onto three elements, two-to-one on A₁, cannot be a
bijection. §5 of the paper states the fact correctly — *"A₁ has two dm³
preimages"* — while the abstract, Theorem C and the Lean name all say
"bijective". `thm_C_singularity_bijection` proves that A₂ and A₃ have unique
preimages, and contains no surjectivity conjunct. The published row
`thm_C_A1_surjective` does not exist. Recommended wording: the correspondence is
**surjective, and injective away from A₁**.

**4. `entropy_lyapunov_duality` reduces to −2 + 2 = 0.**

The `4` in `embodimentThreshold 4 1` is supplied by hand rather than derived
from `toyModel`, so the "duality" relates two independently written constants.
It becomes non-trivial if the drift coefficient is *defined* as `c = 2|μ_max|`,
which is how `Orthogenesis/Architecture/ToyModel.lean` in the `geometry`
repository states the same fact (`toyModel_tau_eq_abs_muMax`).

**5. There are two formalizations of the dm³ toy model, and they do not compete.**

- `AXLE/PrincipiaOrthogona_v2/VolumeTwo.lean` — **abstract**, over a
  `DM3System` whose `mu_neg`, `omega_pos`, `beta_pos` are hypotheses. Lean v4.14.0.
- `geometry/Orthogenesis/Architecture/ToyModel.lean` — **concrete**,
  `transEig z = −2 + 2e^(−z)`, tied to the vector field by
  `transEig_hasDerivAt`, which proves `transEig` *is* ∂ṙ/∂r at r = 1. Lean v4.32.0.

`eigenvalue_neg_pos_z` and `toyModel_tau` exist in both under the same names and
are different theorems. The abstract version assumes the sign of μ_max; the
concrete version derives it from the field. Neither should be merged into the
other, and no CI can compare them — the toolchains are eighteen releases apart.


## Added while preparing V5 (2026-08-26)

Five declarations, all kernel-checked.

**`thm_C_A1_surjective`** and **`thm_C_not_bijective`** close the two rows V4's
Appendix A listed as *proved* under names that existed nowhere. Both report
`does not depend on any axioms` — constructive, no `propext`, no choice. The
second makes the correction a theorem: contact Hopf and saddle-node share the
A₁ preimage, so injectivity fails and the correspondence cannot be a bijection.

**`thm_A_regularization_pointwise`** and **`thm_A_regularization_at_fold`** give
Theorem A real content beside its `True` placeholder, which is left in place with
its `OPEN` comment rather than quietly replaced. Together they state the
concentration: the contact correction vanishes off the fold as β → ∞ and does not
move with β on it. The distributional limit those two skeletonise stays open, and
needs distribution theory Mathlib does not yet carry.

**`tau_eq_abs_mu_iff`** turns the `toyModel_tau` docstring caveat into a theorem:
with c = 2|μ| and κ_noise = 1, the embodiment threshold equals |μ| exactly when
|μ| = 2 (or μ = 0). That is why τ is a *scale* and not a parameter-free relation —
see WP-79 in the geometry repository.

Still open, with reasons rather than silence: Theorem B's real direction
(τ finite ⟹ μ_max < 0) needs Has'minskii-style stochastic stability; the Gronwall
asymmetry needs the DOP853 numerics carried into the kernel; Levels 2d and 2d+t
need Lie brackets of vector fields, which a pointwise model cannot express.
