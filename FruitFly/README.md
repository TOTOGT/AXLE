# Biological Transitions as Multi-Agent Realisations of the
# Generative Operator Pipeline in TO/TOGT: A Fruit-Fly Connectome Toy Model
# Version 2 — Zenodo deposit

**Author:** Pablo Nogueira Grossi, G6 LLC, Newark NJ  
**ORCID:** 0009-0000-6496-2186  
**Concept DOI (all versions):** https://doi.org/10.5281/zenodo.19210136  
**V1 DOI:** https://doi.org/10.5281/zenodo.19210137  
**License:** MIT (code, Lean 4); CC BY 4.0 (paper, figures)  
**Companion paper (broader scope):** https://doi.org/10.5281/zenodo.19208015

---

## What's new in V2

V1 (March 2026) deposited only the 3-page skeleton PDF with no source,
no figures, no code, and a circular self-citation in the abstract
(the companion DOI cited was this paper's own record).

V2 adds:

| Addition | Description |
|----------|-------------|
| `multi_orbit_bioswarm.tex` | Complete LaTeX source (569 lines) |
| `lean/MultiOrbitBioSwarm.lean` | Lean 4 / Mathlib4 — 16 theorems without sorry |
| `code/multi_orbit_bioswarm.py` | Python simulation: G = U∘F∘K∘C + all 4 figures |
| `figures/fig1_swarm_trajectories.pdf` | Swarm trajectories at α = 0.3 and α = 0.5 |
| `figures/fig2_pitchfork_scan.pdf` | Pitchfork bifurcation signature vs α |
| `figures/fig3_convergence.pdf` | Six-iterate convergence with L^t bound |
| `figures/fig4_operator_diagram.pdf` | C → K → F → U pipeline schematic |
| `figures/pitchfork_scan.csv` | Raw data for fig2 (80 α values) |
| References section | 14 bibitems including FlyWire papers |
| **Citation correction** | Circular self-cite fixed → now cites `19208015` |

---

## V1 citation error (corrected here)

The V1 abstract cited `10.5281/zenodo.19210137` as the "companion
fixed-point paper" — but that DOI **is this paper's own V1 record**.
The correct companion (broader biological scope, correct HAL citation)
is `10.5281/zenodo.19208015`. This is corrected throughout V2 and
noted explicitly in the abstract.

---

## Deposit file manifest

```
multi_orbit_bioswarm.tex          — LaTeX source (this paper)
multi_orbit_bioswarm_v2.pdf       — compiled PDF
lean/
  MultiOrbitBioSwarm.lean         — Lean 4 proofs (16 without sorry, 3 sorry obligations)
code/
  multi_orbit_bioswarm.py         — Python simulation and figure generator
figures/
  fig1_swarm_trajectories.pdf
  fig2_pitchfork_scan.pdf
  fig3_convergence.pdf
  fig4_operator_diagram.pdf
  pitchfork_scan.csv
README.md                         — this file
```

---

## Lean 4 verification summary

`MultiOrbitBioSwarm.lean` proves without sorry:
- Pitchfork threshold `1/2` is interior to `(0,1)`
- For `|α| < 1/2`: Lipschitz constant `L(α) < 1` (strict contraction)
- At `|α| = 1/2`: `L(α) = 1` (pitchfork onset, non-expansive)
- `L(0.3) = 4/5`, and `(4/5)^6 < 27/100` (six-iterate bound)
- dm³ normalisation triple `(2π, −2, 2)` is arithmetically consistent

Sorry obligations (infrastructure gaps, not argument gaps):
- A: full BioSwarm Lipschitz bound (needs metric instance)
- B: collective fixed-point (follows from A via Banach)
- C: dynamical pitchfork (needs Mathlib bifurcation library)

---

## Reproduce figures

```bash
pip install numpy matplotlib
python3 code/multi_orbit_bioswarm.py --out figures
```

Produces `fig1`–`fig4` PDFs and `pitchfork_scan.csv` in `figures/`.

---

## Related deposits

| Paper | DOI |
|-------|-----|
| Companion (broader scope) | https://doi.org/10.5281/zenodo.19208015 |
| Principia Orthogona Vol. I | https://doi.org/10.5281/zenodo.19117400 |
| DNLS companion paper | https://doi.org/10.5281/zenodo.20026942 |
| AXLE repo (Lean proofs) | https://github.com/TOTOGT/AXLE |
