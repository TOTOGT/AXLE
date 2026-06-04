# Self-Regulation: Autophagy and the Triple-Alpha Process as dm³ Generative Transitions
## Chapter A — Principia Orthogona, Book 3: The Mini-Beast

**Author:** Pablo Nogueira Grossi, G6 LLC, Newark NJ
**ORCID:** 0009-0000-6496-2186
**Zenodo (this deposit):** https://doi.org/10.5281/zenodo.20168812
**Series root:** https://doi.org/10.5281/zenodo.19117400
**AXLE repository:** https://github.com/TOTOGT/AXLE
**License:** MIT (code, Lean 4); CC BY 4.0 (paper, figures)

---

## Deposit contents

| File | Description |
|------|-------------|
| `autophagy_dm3.pdf` | Main paper, 8 pages, all 4 figures embedded |
| `tex/autophagy_dm3.tex` | LaTeX source (9 bibitems, all sections) |
| `lean/AutophagyDm3_v2.lean` | Lean 4/Mathlib4 — 26 theorems, zero actual sorry; obligation 1 closed, 2 strengthened, 3 split |
| `code/autophagy_dm3.py` | Python simulation and figure generator |
| `figures/fig_A1_t40_fold.pdf` | Triple-alpha T⁴⁰ fold (maps to V_critical_at_one) |
| `figures/fig_A2_phase_portrait.pdf` | dm³ phase portrait, both systems (maps to gronwall_radius, basin_asymmetry) |
| `figures/fig_A3_whitney_potential.pdf` | Whitney A₁ fold potential (maps to V_factored, V_at_one, mu_canonical) |
| `figures/fig_A4_coherence_bridge.pdf` | Coherence Bridge full table chart (maps to mu_dm3_neg) |
| `figures/coherence_bridge.csv` | Raw data for fig_A4 and Table 1 |

---

## Lean 4 verification summary (AutophagyDm3.lean)

**18 theorems proved without sorry:**

| Theorem | Statement |
|---------|-----------|
| `contactCoeff_neg` | c(ρ) = −2ρ < 0 for ρ > 0 |
| `contactCoeff_ne_zero` | c(ρ) ≠ 0 |
| `V_critical_at_one` | V′(1) = 0 |
| `V_second_deriv_at_one` | V″(1) = 6 |
| `V_second_deriv_ne_zero` | V″(1) ≠ 0 |
| `V_at_one` | V(1) = −2 |
| `V_factored` | V(q)+2 = (q−1)²(q+2) |
| `V_double_root` | corollary of V_factored |
| `mu_canonical` | −V″(1)/2 = −3 |
| `mu_dm3`, `mu_dm3_neg` | −2 < 0 |
| `gronwall_radius` | ε₀ = 1/3 |
| `gronwall_radius_pos`, `gronwall_radius_lt_one` | 0 < 1/3 < 1 |
| `basin_asymmetry` | 1/3 < 4/5 |
| `Φ_pos`, `dΦ_pos`, `dΦ_at_threshold` | stability functional |
| `contactForm_nondeg_scalar` | c(ρ) ≠ 0 — obligation 1 CLOSED |
| `contactForm_orientation` | c(ρ) < 0 for ρ > 0 — obligation 1 CLOSED |
| `V_is_morse_at_one` | V is Morse at q=1 — obligation 2 local model |
| `whitneyFold_conditional` | conditional on σ Morse — obligation 2 STRENGTHENED |
| `dm3_basin_compact` | annulus [1/3, 2] is compact — obligation 3 partial |
| `dm3_basin_nonempty` | annulus is non-empty — obligation 3 partial |

**3 open obligations (AXLE Issue #14):**
- `contactForm_nondeg_scalar` / `contactForm_orientation` — **CLOSED** (obligation 1)
- `whitneyFold_conditional` — **STRENGTHENED** to proper conditional; sorry guards only Mather's theorem
- `dm3_basin_compact` / `dm3_basin_nonempty` — **PROVED** (compactness half of obligation 3)
- `limitCycle_exists_auto` — sorry pending Poincaré–Bendixson in Mathlib

---

## Reproduce figures

```bash
pip install numpy matplotlib
python3 code/autophagy_dm3.py --out figures
```

---

## Related deposits

| Paper | DOI |
|-------|-----|
| Principia Orthogona series root | https://doi.org/10.5281/zenodo.19117400 |
| DNLS companion paper | https://doi.org/10.5281/zenodo.20026942 |
| Fruit-fly / MultiOrbitBioSwarm | https://doi.org/10.5281/zenodo.19210136 |
| AXLE repository | https://github.com/TOTOGT/AXLE |
