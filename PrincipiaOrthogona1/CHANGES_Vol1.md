# Principia Orthogona, Volume I — Version History

## Version 7 (August 24, 2026) — Current

**DOI:** 10.5281/zenodo.22084842

### Why V7 exists

V7 is a correction release. It does not change the mathematics of the paper. It
corrects what the deposit said about the machine verification of that mathematics.

**1. The Lean file had drifted off its own Mathlib pin.** V3 through V6
described `PrincipiaVol1.lean` as *"30+ facts proved, 1 sorry (clearly scoped),
0 axioms beyond Mathlib4."* Built in August 2026 against the revision
`lake-manifest.json` names — Mathlib v4.14.0, December 2024 — it produced 81
errors.

The profile is version drift, not neglect: `Ordinal.sup` and `Ordinal.lt_sup`
were deprecated 2024-08-27, `Ordinal.IsLimit.add_right` renamed `isLimit_add`
2024-10-11, `Set.finite_insert` is the Mathlib-3 spelling of
`Set.Finite.insert`. Those are the names the file uses — current when it was
written and run. Mathlib moved, the pin was advanced past the code, one later
hand-edit (three structure fields on one line separated by `;`) was never
rebuilt, and with no CI nothing re-ran the build.

V7 brings the file to the pin and ships a runner, so the next drift surfaces
the day it happens. Build log included as `v6-build-errors.txt`; the V6 file
unchanged as `PrincipiaVol1-V6-as-deposited.lean.txt`.

**2. The separation theorem was false as stated.** V3–V6 carried it with one `sorry`
attributed to a missing Mathlib eigenvalue API (O1, AXLE issue #12). The deposited
hypothesis `IsDm3Stable` bounds only the transverse diagonal and says nothing about
`M 0 0`; at `n = 1` it is vacuous and the 1×1 matrix `(33)` has trace 33. The refutation
is now proved in Lean and kept in the file as `v6_separation_statement_is_false`.

The underlying result is real. Book 2 Theorem 12.2 and both ancestor files in AXLE state
**Tr(M⁶) ≠ 33** — the sixth power, which the deposit had dropped. At the first power the
intended bound is numerically false (31·e⁻² ≈ 4.195, not < 1); at the sixth it holds with
wide margin (31·e⁻¹² ≈ 1.9·10⁻⁴). O1 has been re-diagnosed accordingly: what is genuinely
open is the spectral reduction Tr(M⁶) = Σ λᵢ⁶ for a general real M, not an API gap.

### What V7 adds

- `PrincipiaVol1.lean` rebuilt: **58 theorems, 0 sorry**, no axiom beyond `propext`,
  `Classical.choice`, `Quot.sound`. Every mechanical repair is marked `V7 FIX` in place.
- §9 rewritten: nine theorems including the spectral form, the diagonal-matrix form, a
  first-power form carrying the normalisation V6 omitted, a sharpness witness at n = 33,
  a non-vacuity witness, and the refutation of the V6 statement.
- §14 (Theorem 5.3 concrete instances) was labelled "NOT MACHINE-CHECKED". It is now.
- `v6-build-errors.txt` and `PrincipiaVol1-V6-as-deposited.lean.txt` added.
- `OPEN_QUESTIONS.md` rewritten against a kernel run rather than against the file's own
  comments.
- **`vol1-proofs`** published — a small repository holding this one file and a three-stage
  verifier (`lake build` → `#print axioms` over all 58 theorems → a gate that refuses on
  `sorryAx` or an off-allowlist axiom). AXLE is too large to build for one check; this is
  the check.
- `principia_vol1_v7.pdf` / `.tex` — the paper rebuilt from the V6 source
  (47 pp). It carries a boxed correction notice after the abstract; §17.1
  states the toolchain pin, the counts, and the one-command verifier; §22
  prints the Lean listing that the verifier actually builds, in place of a
  listing whose last entry did not compile.

  *Retraction inside this changelog.* A first draft of this entry stated that
  the V3–V6 LaTeX source "did not compile either" and that a
  Perelman-correspondence figure "does not exist at all and is withdrawn."
  **That was wrong.** It described `a.PolyLaminin/principia_vol1_v2_full.tex`,
  an 18-page V2-era file, mistaken for the current source. The real V6 source
  is 2,322 lines, 42 pages, uses `fig1_phase_portrait`,
  `fig6_operator_sequence` and `fig5_coherence_bridge` — all present — and
  compiles on the first pass. No figure was missing and none is withdrawn.
- Toolchain and Mathlib revision now pinned and stated. "Current stable" is not a
  checkable dependency, and a floating one is how this went unnoticed for four versions.

### Also found in the V7 editorial pass

- **O7 — the ε₀ instantiation does not close.** §22 states
  ε₀ = |μmax|/[2(1 + sup‖Hess V‖)], sets sup‖Hess V‖ = |L₂| = 3, and computes
  2/(2·3) = 1/3. The formula at H = 3 gives 1/4; the printed arithmetic and
  the Lean line both correspond to H = 2. `epsilon0_of_eq_third_iff` proves
  that under this formula ε₀ = 1/3 **iff** H = 2, so exactly one of the three
  lines is wrong. Not decided in V7 — deciding it is a question about which
  Hessian bound enters the Gronwall estimate. Opened as O7.
- **Theorems A–D are structures, not theorems.** V6's abstract said so
  correctly; the machine-checked list did not. Corrected.
- **Two structure fields are weaker than their names, now proved.**
  `UnfoldOp.stable_branch` holds for every map on every type
  (`unfold_stable_branch_is_vacuous`); `CompressionOp.contractive` is
  non-expansive and the identity satisfies it
  (`compression_permits_identity`).
- **The Factor-of-3 Prediction was reported as machine-checked**, citing
  `basin_asymmetry : 1/3 < 4/5` — an inequality between two rationals — as
  verification of a bound on gravitational decoherence. Withdrawn.
- **`1/3 < 4/5 ≈ r*`** — the corpus's canonical inner boundary is
  r★ = 0.77594059; 4/5 is 3% above it. A second theorem states the comparison
  against the canonical value, and the text says which number is numerical
  input rather than proved.
- **`V(1) + 2 = (q−1)²(q+2)`** in §19 — a number equated to a function of q.
  The Lean says `V q + 2`. Fixed.
- **`10.5281/zenodo.19117400` was labelled the "series root"** in Data and
  Software Availability. It is the version DOI of V1. The concept DOI is
  `19117399`.
- **A sharpness claim of V7's own was withdrawn.** A draft shipped
  `separation_sharp_at_33` as proof that `n < 33` is load-bearing. Its witness
  violates the theorem's transverse hypothesis. The bound in fact carries to
  n = 131072, and fails only around 1.7·10⁷; both are now theorems.

### Withdrawn in V7

- Every provenance line of the form *"Source: `X.lean` — 0 sorry"* in the Lean file's
  section banners. Those files have not been built either. The claim returns per file, as
  each one goes green.
- The sorry-count sentence in the deposit description. The correct figure is 0, and the
  earlier figure of 1 was not a measurement.

---

## Version 3 (May 2026)
**DOI:** 10.5281/zenodo.20237688 (concept, resolves to latest)

### What V3 adds relative to V2:
- `PrincipiaVol1.lean` added directly to the deposit (previously only linked via AXLE).
  Consolidates 30+ proved facts from `AutophagyDm3_v2.lean`, `AXLE_v5_1.lean`,
  `gronwall_proof.lean` (v6.1 closure), and `main_v7.lean` into a single
  self-contained file with explicit source provenance for every theorem.
- `figures.py` added directly to the deposit (previously only in AXLE repo).
  Generates all 7 figures reproducibly from scratch (numpy/matplotlib only).
- Individual figure PDFs added: `fig1_phase_portrait.pdf` through `fig7_contact_3d.pdf`.
- `CHANGES_Vol1.md` (this file): explicit version history narrative.
- `OPEN_QUESTIONS.md`: open questions table with status column,
  matching the format of the Fibonacci/Tribonacci deposit (10.5281/zenodo.20075822).
- Sorry count clarification: 1 sorry in `separation_theorem` (eigenvalue API gap,
  O1, AXLE Issue #12), clearly scoped. All other 30+ theorems are sorry-free.
- Gronwall closure note: `gronwall_contraction_below_stability_radius` proves
  the sign of the decay exponent only; the full ODE integration is O3.

### Files in V3 deposit:
| File | Description |
|------|-------------|
| `principia_vol1_v2_full.pdf` | Full paper, Second Edition |
| `principia_vol1_v2_full.tex` | LaTeX source (reproducible) |
| `PrincipiaVol1.lean` | Lean 4 / Mathlib4 formal proofs (30+ facts, 1 scoped sorry) |
| `figures.py` | Python figure generator (all 7 figures) |
| `fig1_phase_portrait.pdf` | dm³ phase portrait with Gronwall basin |
| `fig2_threshold_equivalence.pdf` | Threshold equivalence diagram |
| `fig3_bifurcation.pdf` | Bifurcation diagram near κ* |
| `fig4_stability_radius.pdf` | Stability radius ε₀ = 1/3 illustration |
| `fig5_coherence_bridge.pdf` | Coherence Bridge (μmax, β across domains) |
| `fig6_operator_sequence.pdf` | Operator sequence G = U∘F∘K∘C∘E |
| `fig7_contact_3d.pdf` | Contact 3-manifold with limit cycle Γ |
| `CHANGES_Vol1.md` | This version history |
| `OPEN_QUESTIONS.md` | Open questions table with status |
| `VolumeTwo.lean` | Vol II Lean file (companion) |
| `Principia Orthogona Volume One (V1).pdf` | Original V1 PDF (preserved) |

---

## Version 2 (May 16, 2026)
**DOI:** 10.5281/zenodo.20221723

### What V2 added relative to V1:
- `principia_vol1_v2_full.pdf`: complete Second Edition paper with:
  - Fifth operator E (Generative Time Circuit, ż ≥ 0)
  - Perelman structural correspondence (Conjecture 15.1, Table 1)
  - Dimensional threshold N=3 conjecture (Conjecture 16.1)
  - §16 club filter / stationary sets infrastructure
  - Coherence Bridge extended to 7 domains (autophagy + triple-alpha)
- `principia_vol1_v2_full.tex`: LaTeX source
- Companion PDFs bundled: Vol II, GCM paper, dm³ operator toy model
- HTML version (`principia_vol1.html`)
- Lean verification linked via AXLE (not yet directly in deposit)

---

## Version 1 (March 17, 2026)
**DOI:** 10.5281/zenodo.19117400

### Contents:
- Original paper PDF: four-operator framework G = U∘F∘K∘C
- Six minimal assumptions
- Five structural theorems (Theorems A–D + non-commutativity)
- Seven analytical invariants
- Four normal forms (Whitney A₁–A₃ hierarchy)
- Free-discontinuity variational principle
- Symplectic Hamiltonian structure with distributional generator
- Lean 4 verification of Theorems A–D (linked via AXLE)
- No Python code or individual figures in deposit

---

## Version 6 (July 2026)
**DOI:** 10.5281/zenodo.21146416

Closed three previously unproved or hand-waved results found in a line-by-line
audit, and added two explicitly stated assumptions the proofs require:
Existence and Well-Posedness (Theorem 5.1) proved as a corollary; Finite
Branching (Theorem 5.4) proved from the new Transverse Crossing assumption;
Compression Regularity added, with a bi-Lipschitz counterexample showing it is
necessary; Argument V of the classification corrected; and Invariant 7.5
(Injectivity Before Threshold) proved in a companion note, with a Gerono
lemniscate counterexample confirming the unqualified global statement was false
as originally written.

## Version 5 (July 2026)
**DOI:** 10.5281/zenodo.21121980

Hand-verified correction pass on §§18–22: the derivative in Proof IV corrected
to f′(ρ) = −2 − 6ρ − 3ρ²; Proof VI rewritten in Darboux coordinates; P5 made to
distinguish the Lyapunov exponent μmax from the quadratic coefficient L₂; and
the zero-sorry claim scoped explicitly to `PrincipiaVol1.lean`.

*V7 note:* the scoping was right; what was missing was anything that re-ran
the build after Mathlib moved.

## Version 4 (June 21, 2026)
**DOI:** 10.5281/zenodo.20784030

Seven-proof template extended to all five structural theorems; precision and
completeness pass.
