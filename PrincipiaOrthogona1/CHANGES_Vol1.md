# Principia Orthogona, Volume I — Version History

## Version 7 (August 24, 2026) — Current

**DOI:** 10.5281/zenodo.22084842

### Why V7 exists

V7 is a correction release. It does not change the mathematics of the paper. It
corrects what the deposit said about the machine verification of that mathematics.

**1. The Lean file had never been compiled.** V3 through V6 described
`PrincipiaVol1.lean` as *"30+ facts proved, 1 sorry (clearly scoped), 0 axioms beyond
Mathlib4."* The first real build of it — 24 August 2026, under Lean v4.14.0 and Mathlib
v4.14.0 rev 4bbdccd9c5f8, the toolchain the deposit itself names — reported **81
errors**. The faults were mechanical: structure fields separated by `;` (so `Dm3Triple`
had one field and every `canonicalTriple.mu_max` was an unknown field), a `MetricSpace`
passed where a `Dist` was expected, `(0 : Fin n)` with no `[NeZero n]`, four Ordinal
lemmas that do not exist under those names, a carrier type that never unfolded to `ℤ`.
Mechanical, but the consequence was not: nothing V3–V6 claimed about that file had been
checked by anything.

The verbatim build log ships in this deposit as `v6-build-errors.txt`, and the V6 file
ships unchanged as `PrincipiaVol1-V6-as-deposited.lean.txt`, so the two can be diffed.

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

- `PrincipiaVol1.lean` rebuilt: **49 theorems, 0 sorry**, no axiom beyond `propext`,
  `Classical.choice`, `Quot.sound`. Every mechanical repair is marked `V7 FIX` in place.
- §9 rewritten: nine theorems including the spectral form, the diagonal-matrix form, a
  first-power form carrying the normalisation V6 omitted, a sharpness witness at n = 33,
  a non-vacuity witness, and the refutation of the V6 statement.
- §14 (Theorem 5.3 concrete instances) was labelled "NOT MACHINE-CHECKED". It is now.
- `v6-build-errors.txt` and `PrincipiaVol1-V6-as-deposited.lean.txt` added.
- `OPEN_QUESTIONS.md` rewritten against a kernel run rather than against the file's own
  comments.
- **`vol1-proofs`** published — a small repository holding this one file and a three-stage
  verifier (`lake build` → `#print axioms` over all 49 theorems → a gate that refuses on
  `sorryAx` or an off-allowlist axiom). AXLE is too large to build for one check; this is
  the check.
- `principia_vol1_v7.pdf` / `.tex` — the paper rebuilt. The V3–V6 LaTeX source
  did not compile either: it referenced three figures by names that exist
  nowhere in the deposit or in `figures.py`. Two were misnamed and are
  repointed at `fig1_phase_portrait` and `fig5_coherence_bridge`; the third, a
  Perelman-correspondence diagram, does not exist at all and is **withdrawn**
  rather than replaced by a different figure under its caption — Table 1
  carries that correspondence term by term. The paper now carries a boxed
  correction notice after the abstract, and §17.1 states the toolchain pin,
  the counts, and the one-command verifier.
- Toolchain and Mathlib revision now pinned and stated. "Current stable" is not a
  checkable dependency, and a floating one is how this went unnoticed for four versions.

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
