# Principia Orthogona, Volume I — Version History

## Version 3 (May 2026) — Current
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
