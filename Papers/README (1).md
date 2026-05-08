# Criticality Thresholds in One-Dimensional Multiplying Media with n-Bonacci Aperiodic Modulation

**Author:** Pablo Nogueira Grossi  
**Affiliation:** G6 LLC, Newark, New Jersey, USA  
**ORCID:** 0009-0000-6496-2186  
**Contact:** pablogrossi@hotmail.com  
**Year:** 2026  
**License:** MIT (code), CC BY 4.0 (text and figures)

---

## Overview

This deposit contains all code, figures, and manuscript files for the paper:

> Nogueira Grossi, P. (2026). *Criticality Thresholds in One-Dimensional
> Multiplying Media with n-Bonacci Aperiodic Modulation: Spectral Gap
> Control of k-effective in Substitution-Sequence Diffusion Operators.*

The paper studies the one-group neutron diffusion equation on a uniform
1D slab whose material coefficients vary site-by-site according to the
n-bonacci substitution sequence for n = 2, 3, 4, 5 (Fibonacci,
Tribonacci, Tetranacci, Pentanacci). The central result is that the
critical fission strength λ_c(n) is governed by the spectral gap of the
substitution transfer matrix, not by the n-bonacci constant alone, and
that λ_c(n) → 7/6 exactly for n ≥ 4.

This work is a companion to:

> Nogueira Grossi, P. (2026). *Differential Nonlinear Robustness of
> Critical States in Fibonacci and Tribonacci Substitution Chains.*
> Zenodo. https://doi.org/10.5281/zenodo.20026942 (concept DOI, always latest)

---

## Repository structure

```
deposit/
├── README.md                      — this file
│
├── nbonacci_criticality.py        — pilot sweep: k_eff vs lambda,
│                                    Fibonacci and Tribonacci, generates
│                                    early diagnostic figures
│
├── nbonacci_critical_lambda.py    — main sweep: finds λ_c(n) for n=2..5
│                                    by bisection (Brent's method),
│                                    computes spectral gaps and convergence
│                                    tables, generates fig_lambda_c_v2.png
│
├── generate_all_figures.py        — generates all 5 paper figures
│                                    (Fig 1–5) from scratch; single entry
│                                    point for full reproduction
│
├── nbonacci_diffusion_draft.tex   — LaTeX source of the manuscript
├── nbonacci_diffusion_draft.pdf   — compiled PDF of the manuscript
│
├── fig1_chain_structure.png       — Fig 1: substitution word visualization
├── fig2_keff_vs_lambda.png        — Fig 2: k_eff vs lambda, gen 4/6/8
├── fig3_lambda_c_gap.png          — Fig 3: λ_c(n) vs spectral gap Δ_n
├── fig4_convergence.png           — Fig 4: convergence with generation
└── fig5_flux_profiles.png         — Fig 5: fundamental flux modes
```

---

## Reproducing all results

### Requirements

- Python ≥ 3.10
- numpy, scipy, matplotlib

Install dependencies:

```bash
pip install numpy scipy matplotlib
```

### Run the full figure pipeline

```bash
python generate_all_figures.py
```

This reproduces Figures 1–5 exactly as they appear in the paper.
Runtime: under 5 minutes on a single core.

### Run the critical lambda sweep (main numerical result)

```bash
python nbonacci_critical_lambda.py
```

Prints the λ_c(n) table, spectral gap data, and convergence tables
for n = 2, 3, 4, 5 and saves `fig_lambda_c_v2.png`.

### Compile the manuscript

```bash
pdflatex nbonacci_diffusion_draft.tex
pdflatex nbonacci_diffusion_draft.tex   # second pass for references
```

Requires a standard LaTeX distribution (TeX Live, MiKTeX) with the
packages: amsmath, amssymb, amsthm, geometry, hyperref, graphicx,
booktabs, xcolor, authblk.

---

## Key numerical results (summary)

| n | Chain        | ρ_n    | Δ_n    | λ_c(n)   | vs 7/6         |
|---|--------------|--------|--------|----------|----------------|
| 2 | Fibonacci    | 1.6180 | 1.0000 | 1.06419  | outlier        |
| 3 | Tribonacci   | 1.8393 | 1.1019 | 1.15626  | ≈ 37/32        |
| 4 | Tetranacci   | 1.9276 | 1.1093 | 1.16667  | → 7/6 exactly  |
| 5 | Pentanacci   | 1.9660 | 1.0949 | 1.16667  | = 7/6 (machine)|

Linear fit: λ_c ≈ 0.958 · Δ_n + 0.107 (r = 0.989)

---

## Parameter map (dimensionless model)

| Symbol | Role      | D   | Σ_r | νΣ_f |
|--------|-----------|-----|-----|------|
| A (0)  | Fissile   | 1.0 | 0.5 | λ    |
| B,C,.. | Absorber  | 1.0 | 2.0 | 0    |

Vacuum boundary conditions (φ = 0) at both ends.
Uniform mesh, h = 1. Harmonic-mean interface diffusion coefficients.
Eigenvalue problem solved via `scipy.linalg.eig`; λ_c found by
Brent's method (`scipy.optimize.brentq`, tolerance 10⁻⁹).

---

## Relation to companion deposit

The DNLS companion paper (concept DOI: doi:10.5281/zenodo.20026942, V4: doi:10.5281/zenodo.20075822) studies
nonlinear dynamics on the same Fibonacci and Tribonacci chains using
the discrete nonlinear Schrödinger equation. The present deposit extends
that spectral framework to classical neutron transport, replacing the
DNLS nonlinearity parameter with the fission production strength λ
and replacing IPR with k_eff as the central observable.

Code for the DNLS companion is available at:
https://github.com/grossi-ops/Atratores/tree/main/DNLS

---

## Citation

If you use this code or data, please cite:

```
Nogueira Grossi, P. (2026). Criticality Thresholds in One-Dimensional
Multiplying Media with n-Bonacci Aperiodic Modulation [Data and code].
Zenodo. https://doi.org/10.5281/zenodo.20077205

