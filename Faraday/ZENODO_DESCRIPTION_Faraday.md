# Electromagnetic Unity: From Faraday's Fields to the dm³ Operator Framework

**Pablo Nogueira Grossi** · G6 LLC, Newark NJ · May 2026  
**ORCID:** 0009-0000-6496-2186  
**Contact:** pablogrossi@hotmail.com · g6llc@proton.me  
**Series root:** https://doi.org/10.5281/zenodo.19117399  
**GitHub:** https://github.com/TOTOGT/AXLE  
**License:** CC BY-NC-ND 4.0

---

## What this deposit contains

| File | Description |
|---|---|
| `Faraday_EM_dm3_Grossi2026.pdf` | Complete paper (7 pages, 4 figures, 2 tables) |
| `faraday_figures.py` | Python figure generator (reproduces all 4 figures) |
| `fig1_helix.png` | Helical charged-particle trajectory in magnetic field |
| `fig2_induction.png` | Faraday induction — flux, EMF, Lenz's law |
| `fig3_faraday_effect.png` | Magneto-optical Faraday rotation |
| `fig4_correspondence.png` | dm³ operator ↔ EM correspondence diagram |

## Summary

Michael Faraday established the deep reciprocal unity between electricity,
magnetism, and light. This paper argues that the dm³ contact-geometric operator
chain C→K→F→U→T provides a unified algebraic skeleton for Faraday's three
foundational results and Maxwell's synthesis.

**Four structural correspondences:**

| dm³ Operator | EM Phenomenon | Shared Invariant |
|---|---|---|
| C: Compression | Magnetic confinement (Larmor orbit) | ε₀ = 1/3 |
| K: Curvature | Cyclotron resonance | T* = 2π |
| F: Fold (saturation) | Faraday rotation (non-reciprocal) | g₃₃ = 33 |
| U: Unification | Maxwell synthesis (E, B, c) | μ_max = −2 |
| T: Time circuit | EM wave propagation (helical return) | g₆₄ = 64 |

**Central structural observation:** The Faraday rotation angle θ_F ≈ 33° is
realisable in standard magneto-optic materials (heavy flint glass at λ = 589 nm)
and corresponds to the g₃₃ = 33 invariant formally verified in AXLE
(Main_v6.lean, theorem T8: trace_bound_33).

**Falsifiable prediction:** g₆₄ = 64 should appear in the period-doubling
structure of an electromagnetic resonator in the dm³ T-operator regime.

## Building the figures

```
python faraday_figures.py
# Produces: fig1_helix.png  fig2_induction.png
#           fig3_faraday_effect.png  fig4_correspondence.png
```

Requirements: Python ≥ 3.10, numpy, matplotlib, scipy

## Relation to the series

| Volume / Paper | DOI | Domain |
|---|---|---|
| Vol. I: Operator Algebra | 10.5281/zenodo.20320693 | Abstract mathematics |
| Vol. II: Contact Geometry | 10.5281/zenodo.20159456 | dm³ normal form |
| GTCT (Ring 5) | 10.5281/zenodo.20239928 | Time circuit T |
| Biological Transitions | 10.5281/zenodo.20230612 | Neural, HPA, circadian |
| Multi-Orbit Identity Theory | 10.5281/zenodo.20230614 | Operator-algebraic orbits |
| G6 Crystal | 10.5281/zenodo.19162012 | Architecture / Moon Base |
| **This paper (EM)** | **Preprint, May 2026** | **Electromagnetism** |
| Series root | 10.5281/zenodo.19117399 | All versions |

## Formal verification (AXLE)

The dm³ constants cited in this paper are formally verified in
[TOTOGT/AXLE](https://github.com/TOTOGT/AXLE):

- T* = 2π → `PrincipiaVol1.lean`, T3: `period_is_2pi`
- g₃₃ = 33 → `Main_v6.lean`, T8: `trace_bound_33`
- ε₀ = 1/3 (outer basin) → `Chain_updated.lean`, `gronwall_outer`
- μ_max = −2 → `VolumeTwo.lean`, T7: `lyapunov_exponent`

160+ theorems proved across the series, 0 axioms beyond Mathlib4.

---
Part of the Principia Orthogona / Generative Contact Mechanics series.  
Series root: https://doi.org/10.5281/zenodo.19117399
