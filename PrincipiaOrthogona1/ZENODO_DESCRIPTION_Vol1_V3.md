# ZENODO_DESCRIPTION_Vol1_V3.md
# Copy this text into the Zenodo description field for the V3 upload.

---

## Principia Orthogona, Volume I: The Mathematics of Generative Transitions
### Version 3 — May 2026

**Pablo Nogueira Grossi · G6 LLC, Newark NJ · ORCID: 0009-0000-6496-2186**
Zenodo concept DOI (resolves to latest): https://doi.org/10.5281/zenodo.19117399
V3 DOI: 10.5281/zenodo.20237688
Series root: https://doi.org/10.5281/zenodo.19117399
AXLE: https://github.com/TOTOGT/AXLE · DM3-lab: https://github.com/TOTOGT/DM3-lab

---

### What this volume does

This volume develops a unified mathematical framework for generative transitions:
localised geometric events in which a trajectory undergoes compression, curvature
intensification, loss of injectivity, and stabilisation, governed by the operator
sequence G = U ∘ F ∘ K ∘ C.

The framework rests on six minimal assumptions and produces: constructive operator
definitions with explicit formulas; five structural theorems including existence,
non-commutativity, and finite branching; seven analytical invariants; four normal
forms; a singularity classification restricted to the Whitney A₁–A₃ hierarchy;
a free-discontinuity variational principle; and a symplectic Hamiltonian structure
with a distributional generator at the fold.

The second edition (V2, May 2026) added: a fifth operator E (Generative Time Circuit)
with ż ≥ 0; a term-by-term structural correspondence with Perelman's proof of the
Poincaré conjecture via Ricci flow with surgery (Conjecture 15.1); and the dimensional
threshold N = 3 as the minimum dimension for non-trivial contact geometry, connecting
it to c = 3 in the Collatz map (Conjecture 16.1).

---

### What V3 adds

V3 completes the reproducibility stack to the standard of the Fibonacci/Tribonacci
deposit (10.5281/zenodo.20075822). Specifically:

**1. `PrincipiaVol1.lean` — directly in this deposit**
Consolidated Lean 4 / Mathlib4 formal verification file. Sources:
- P1–P6 (Whitney A₁, Gronwall, basin, contact, Lyapunov, stability): from
  `AutophagyDm3_v2.lean` — 0 sorry
- Theorems A–D (operator chain structures): from `AXLE_v5_1.lean` — 0 sorry
- Gronwall contraction (exponent sign): from `gronwall_proof.lean` v6.1 — 0 sorry
- Club filter / stationary sets: from `AXLE_v5_1.lean` — 0 sorry
- Separation theorem: 1 scoped sorry at eigenvalue API boundary (O1, AXLE Issue #12)

Total: 30+ facts proved, 1 sorry (clearly scoped), 0 axioms beyond Mathlib4.

**2. `figures.py` — directly in this deposit**
Python figure generator producing all 7 figures from scratch.
Dependencies: numpy, matplotlib (standard). Run: `python figures.py`

**3. Individual figure PDFs** (fig1–fig7)
- `fig1_phase_portrait.pdf` — dm³ phase portrait with Gronwall basin
- `fig2_threshold_equivalence.pdf` — threshold equivalence diagram
- `fig3_bifurcation.pdf` — bifurcation diagram near κ*
- `fig4_stability_radius.pdf` — stability radius ε₀ = 1/3
- `fig5_coherence_bridge.pdf` — Coherence Bridge (μmax, β across 7 domains)
- `fig6_operator_sequence.pdf` — operator sequence G = U∘F∘K∘C∘E
- `fig7_contact_3d.pdf` — contact 3-manifold with limit cycle Γ

**4. `CHANGES_Vol1.md`** — explicit V1 → V2 → V3 version history

**5. `OPEN_QUESTIONS.md`** — open questions table with status column

---

### Proved without sorry (30+ facts)

P1a–d: Whitney A₁ conditions on V(q) = q³−3q at q=1
P2: Contact non-degeneracy c(ρ) = −2ρ < 0
P3: Gronwall radius ε₀ = 1/3
P4: Basin asymmetry 1/3 < 4/5
P5: Lyapunov exponents −V''(1)/2 = −3; μmax = −2 < 0
P6: Stability functional σ(ρ) = ρ² > 0, σ'(ρ) > 0
A: GenerativeOp well-defined (existence by construction)
B: CompressionOp contractive + injective
C: FoldOp non-injective + finite branch
D: UnfoldOp Φ-decrease + stable branch
+: Canonical triple (T*, μmax, τ) = (2π, −2, 2); noise tolerance τ·ε₀ = 2/3
+: Gronwall contraction exponent sign (scope: sign only; ODE integration is O3)
+: Club filter / stationary sets for regular uncountable ordinals
+: Regeneration hierarchy (unbounded, ordinal, Mahlo-like)
+: Crystal aspect ratio arithmetic (66 = 33·τ)

### Open obligations (5)

| ID | Description | Status |
|----|-------------|--------|
| O1 | AXLE #12: Eigenvalue API gap in separation_theorem | Open — 1 scoped sorry |
| O2 | AXLE #14: Mather step; Poincaré–Bendixson | Strengthened/Partial |
| O3 | AXLE #15 / T1: Full ODE Gronwall integration | Partial — exponent sign proved |
| O4 | Sorry 1: Discrete dm³ extension to ℤ | Open |
| O5 | Conjecture 15.1: Perelman functor 𝒫 | Open — stated as conjecture |

---

### Version history

| Version | Date | Key addition |
|---------|------|-------------|
| V1 | March 17, 2026 | Original four-operator framework |
| V2 | May 16, 2026 | Fifth operator E; Perelman correspondence; Collatz threshold |
| V3 | May 2026 | Full reproducibility stack: Lean file, figures.py, figure PDFs, changelogs |

---

### Build instructions

**Lean 4:**
```
lake update && lake build PrincipiaVol1
```
Dependencies: Mathlib4 (current stable)

**Figures:**
```
pip install numpy matplotlib
python figures.py
```
Outputs: fig1_phase_portrait.pdf through fig7_contact_3d.pdf

**Paper:**
```
pdflatex principia_vol1_v2_full.tex
pdflatex principia_vol1_v2_full.tex
```
(run twice for cross-references)

---

### Series context

| Role | DOI |
|------|-----|
| Series root / concept DOI | 10.5281/zenodo.19117399 |
| Volume I (this deposit) | 10.5281/zenodo.20237688 |
| Volume II (contact geometry) | 10.5281/zenodo.19379473 |
| GCM paper (dm³ toy model) | 10.5281/zenodo.19379385 |
| G6 Crystal (lunar architecture) | 10.5281/zenodo.19162013 |
| Multi-Orbit Identity Theory | 10.5281/zenodo.20230614 |
| Autophagy / Triple-Alpha (Book 3, Ch.A) | 10.5281/zenodo.20168812 |
| Fibonacci / Tribonacci DNLS | 10.5281/zenodo.20026942 |
| AXLE formal verification hub | github.com/TOTOGT/AXLE |

**MSC codes:** 37C25, 37G10, 53D10, 57M27, 58K05, 70H05, 47H10

**Keywords:** generative transitions · contact geometry · operator sequence ·
Whitney fold · singularity theory · variational mechanics · symplectic geometry ·
Ricci flow · Perelman conjecture · Lean 4 formal verification · dimensional threshold ·
dm³ framework · Gronwall stability · Principia Orthogona · G6 LLC

**License:** CC BY-NC-ND 4.0 (paper) · MIT (code)
**Copyright:** © 2026 Pablo Nogueira Grossi, G6 LLC
**Contact:** pgrossi888@outlook.com · g6llc@proton.me
