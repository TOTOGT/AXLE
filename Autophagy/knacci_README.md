# TOTOGT/AXLE/geometry
## Efficient Honeycomb · Polylaminin dm³ Mapping · NASA Homebase

**Author:** Pablo Nogueira Grossi, G6 LLC, Newark NJ  
**ORCID:** 0009-0000-6496-2186  
**Zenodo DOI:** [10.5281/zenodo.19501831](https://doi.org/10.5281/zenodo.19501831)  
**Series:** Principia Orthogona, Volume IV — Deposit 13 | May 2026

---

## What This Deposit Contains

Reproducible geometry, code, Lean 4 proofs, and figures for:

> **Polylaminin, Microtubules, and the k-nacci Spine**  
> Grossi, P.N. (2026). Zenodo. https://doi.org/10.5281/zenodo.19501831

Central object: the **k-nacci spectral radius ladder** — dominant real roots
η_k of P_k(η) = η^k − η^(k−1) − ⋯ − η − 1, governing fractal self-assembly,
resonance selectivity, and multifractal dimension spectra across 12 orders of
magnitude.

---

## Quick Start

```bash
git clone https://github.com/TOTOGT/AXLE
cd AXLE
pip install numpy scipy matplotlib
python python/knacci_spine.py
python python/knacci_laminin_cross.py
pdflatex tex/knacci_spine_v4.tex
```

---

## Key Verified Results [V]

| Quantity | Value |
|---|---|
| η₃ (Tribonacci, critical spine) | 1.839286755 |
| Wavenumber 6 | 2 × 3 = 6 |
| polyLM d_H (1h / 8h / 12h) | 1.55 / 1.62 / 1.70 |
| Cancer resonance ν_c | 221.8 kHz |
| Axonal density ratio C.3 | η₃^0.15 = 1.096 |

---

## Biological Precision Notes

All polylaminin Hausdorff values refer to **acid-induced polymerization
(pH ≈ 4, Ca²⁺-dependent) in vitro** (Hochman-Mendez 2014, Mesquita 2022).
Native basement-membrane laminin is not claimed to be identically fractal.

- **Laminin–MT coupling** is mechanochemical via dystroglycan–integrin axis
  (Hohenester 2018, Sciandra 2023). Direct laminin–tubulin binding is not
  established and not claimed.
- **SCI regeneration** is supported by preclinical data (rats: Menezes 2010;
  dogs: Chize 2025) and early human safety data (Brazil, Anvisa, ReBEC).
  Polylaminin remains **investigational**; Phase III not completed.
- **Cancer corridors C.1, C.2** are theoretical TO/TOGT predictions, stated
  as open falsifiability conditions only.
- **NASA Homebase** module is an engineered analog of polyLN521 parameters —
  not native laminin.

---

## Falsifiability

| Code | Prediction |
|---|---|
| F.1 | f(α) of any hexagonal chiral substrate: peak d_H ∈ [1.50, 1.85] |
| C.1 | ν_c ≈ 221.8 kHz → >50% cancer apoptosis 24 h, <5% healthy |
| C.2 | LC3-II ↑ 6 h; cathepsin B 12 h; cancer cells only |
| C.3 | Axonal density ratio η₃^Δd_H ≈ 1.10, rodent SCI 8 weeks |
| W.1 | Wigner r*_s ∈ [30,40], QMC β ∈ [1.5,1.9] |
| T.1 | FRET coherence 240–280 nm at 37°C, Taxol-suppressible |

---

## Priority Record

First public statement: **28 February 2026**, Threads @brodananda.  
Full contact-geometric derivation: **13 March 2026**, @unitedWeStreamU
(Post ID 2032563730995696073).

---

## Citation

```bibtex
@misc{grossi2026_knacci,
  author = {Grossi, Pablo Nogueira},
  title  = {Polylaminin, Microtubules, and the k-nacci Spine},
  year   = {2026},
  doi    = {10.5281/zenodo.19501831}
}
```

**License:** CC BY 4.0

*Dedicated to Vic, Alice, and Sarah — Giulia, and David. Once tiny, always strong.*
