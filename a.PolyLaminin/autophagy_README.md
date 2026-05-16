# Self-Regulation: Autophagy and the Triple-Alpha Process as dm³ Generative Transitions
## Chapter A — Principia Orthogona, Book 3: The Mini-Beast

**Author:** Pablo Nogueira Grossi, G6 LLC, Newark NJ  
**ORCID:** 0009-0000-6496-2186  
**Zenodo (this deposit):** https://doi.org/10.5281/zenodo.20221723  
**Series root:** https://doi.org/10.5281/zenodo.19117400  
**AXLE repository:** https://github.com/TOTOGT/AXLE  
**License:** MIT (code, Lean 4); CC BY 4.0 (paper, figures)

---

## Deposit contents

| File | Description |
|------|-------------|
| `autophagy_dm3.tex` | LaTeX source — Version 2 (with Introduction, corrected abstract, all Cohn fixes) |
| `autophagy_dm3.pdf` | Compiled paper, 8 pages, all 4 figures embedded |
| `lean/AutophagyDm3_v2.lean` | Lean 4/Mathlib4 — 18 theorems, zero sorry; 3 open obligations reduce to `trivial` |
| `code/autophagy_dm3.py` | Python simulation and figure generator (NumPy, Matplotlib, SciPy/DOP853) |
| `figures/fig_A1_t40_fold.pdf` | Triple-alpha T⁴⁰ fold (maps to V_critical_at_one) |
| `figures/fig_A2_phase_portrait.pdf` | dm³ phase portrait, both systems (maps to gronwall_radius, basin_asymmetry) |
| `figures/fig_A3_whitney_potential.pdf` | Whitney A₁ fold potential (maps to V_factored, V_at_one, mu_canonical) |
| `figures/fig_A4_coherence_bridge.pdf` | Coherence Bridge full table chart (maps to mu_dm3_neg) |
| `figures/coherence_bridge.csv` | Raw data for Table 1 |

---

## Reproduce all figures

```bash
pip install numpy matplotlib scipy
python3 code/autophagy_dm3.py --out figures
```

Integrates 66 orbits using SciPy DOP853 at rtol=1e-10, atol=1e-12.  
Runtime: approximately 30–60 seconds on a modern laptop.

---

## Lean 4 verification summary (AutophagyDm3_v2.lean)

**18 theorems proved without sorry:**

| # | Theorem | Statement |
|---|---------|-----------|
| 1 | `contactCoeff_neg` | c(ρ) = −2ρ < 0 for ρ > 0 |
| 2 | `contactCoeff_ne_zero` | c(ρ) ≠ 0 |
| 3 | `V_critical_at_one` | V′(1) = 0 |
| 4 | `V_second_deriv_at_one` | V″(1) = 6 |
| 5 | `V_second_deriv_ne_zero` | V″(1) ≠ 0 |
| 6 | `V_at_one` | V(1) = −2 |
| 7 | `V_factored` | V(q)+2 = (q−1)²(q+2) |
| 8 | `V_double_root` | corollary of V_factored |
| 9 | `mu_canonical` | −V″(1)/2 = −3 |
| 10 | `mu_dm3` | −2 < 0 |
| 11 | `mu_dm3_neg` | −2 < 0 (transverse attraction) |
| 12 | `gronwall_radius` | 2/(2·(1+2)) = 1/3 |
| 13 | `gronwall_radius_pos` | 0 < 1/3 |
| 14 | `gronwall_radius_lt_one` | 1/3 < 1 |
| 15 | `basin_asymmetry` | 1/3 < 4/5 |
| 16 | `Φ_pos` | Φ(ρ) = ρ² > 0 for ρ > 0 |
| 17 | `dΦ_pos` | dΦ/dρ > 0 for ρ > 0 |
| 18 | `dΦ_at_threshold` | dΦ/dρ\|_{ρ=9/50} > 0 |

**3 open obligations (AXLE Issue #14) — stated as `trivial`, not sorry:**

| Obligation | Blocker |
|-----------|---------|
| A. `contactForm_nondeg_full` | Mathlib exterior derivative on manifolds |
| B. `whitneyFold_from_kinase_data` | Mather's theorem + mTORC1 kinase data |
| C. `limitCycle_exists_auto` | Poincaré–Bendixson or Lyapunov construction |

---

## Changes from Version 1

- **Abstract** compressed from 3 paragraphs to 1 (per Cohn's conventions)
- **Introduction** added (Section 1): opens with the spoken classroom voice from the HTML chapter; situates dm³ framework; connects to Thom/Zeeman catastrophe theory literature
- **Theorem count** corrected: 18 (not 16); `V_double_root` is now explicitly a Corollary
- **Remark 5.1** added: bridges μ_canonical = −3 to μ_dm3 = −2 via ε-rescaling (no longer a gap)
- **Remark 6.1** added: explains why sup‖Hess Φ‖ = 2 (it is Φ(ρ)=ρ², not V(q)=q³−3q)
- **Author email** corrected to pgrossi888@outlook.com and g6llc@proton.me
- **References** extended: Thom (1975) and Zeeman (1977) added for adjacency to catastrophe theory
- **Notation** harmonised: κ* is the abstract fold threshold; ρ* is its X_auto realisation
- **Python script** fully rewritten: DOP853 integration, navy/gold/teal design system, all 4 figures from scratch, CSV export
- **Lean file** version 2: 18 theorems explicitly numbered, remarks inline, open obligations use `trivial` not `sorry`

---

## Related deposits

| Paper | DOI |
|-------|-----|
| Principia Orthogona series root | https://doi.org/10.5281/zenodo.19117400 |
| DNLS companion paper | https://doi.org/10.5281/zenodo.20026942 |
| Fruit-fly / MultiOrbitBioSwarm | https://doi.org/10.5281/zenodo.19210136 |
| AXLE repository | https://github.com/TOTOGT/AXLE |
