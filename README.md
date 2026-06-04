# AXLE — Formal Verification Hub
### Principia Orthogona Series · G6 LLC · Newark NJ · 2026

**AXLE** (Automated eXtensible Lean Engine) is the formal verification repository for the
*Principia Orthogona* series. It contains Lean 4 / Mathlib4 proof files, Python simulations,
companion papers, and the HTML living-book chapters for Book 3 (The Mini-Beast).

**0 axioms beyond Mathlib4 · 9 honest sorrys · AXLE v6.1**

Author: Pablo Nogueira Grossi · ORCID: [0009-0000-6496-2186](https://orcid.org/0009-0000-6496-2186)  
Contact: pablogrossi@hotmail.com · G6 LLC · Newark, NJ

---

## Series and Zenodo

| Record | DOI | Contents |
|---|---|---|
| Series root | [10.5281/zenodo.19117399](https://doi.org/10.5281/zenodo.19117399) | All volumes |
| Vols. I–III + Applications | [10.5281/zenodo.19117400](https://doi.org/10.5281/zenodo.19117400) | GOMC Science |
| Vol. II v2a (Contact Geometry) | [10.5281/zenodo.20159456](https://doi.org/10.5281/zenodo.20159456) | TOGT + AXLE skeleton |
| GTCT (Ring 5) | [10.5281/zenodo.20239928](https://doi.org/10.5281/zenodo.20239928) | Generative Time Circuit Theorem |
| Autophagy / Triple-Alpha (Ch. A) | [10.5281/zenodo.20168812](https://doi.org/10.5281/zenodo.20168812) | dm³ biological instantiation |
| DNLS companion | [10.5281/zenodo.20026942](https://doi.org/10.5281/zenodo.20026942) | Discrete nonlinear Schrödinger |
| Fruit-fly / MultiOrbitBioSwarm | [10.5281/zenodo.19210136](https://doi.org/10.5281/zenodo.19210136) | Connectome dm³ |

---

## Repository structure

```
AXLE/
│
├── Lean 4 proof files
│   ├── Main_v6.lean                     AXLE v6.1 master — 0 extra axioms, 9 sorrys
│   ├── AXLE.lean / AXLE_v5_1.lean / AXLE_v6.lean
│   ├── AutophagyDm3.lean                Ch. A — 18 theorems proved
│   ├── AutophagyDm3_v2.lean             26 theorems, Issue #14 obligations
│   ├── TribonacciMeasure.lean           Tribonacci / DNLS measure
│   ├── gronwall_proof.lean              Gronwall contraction (Issue #13)
│   ├── DiscreteDM3.lean / discreteDm3.lean
│   ├── Dm3Comp.lean                     dm³ compositional structures
│   ├── Dm3GoldbachToy.lean / Dm3NSToy.lean / Dm3RHToy.lean
│   ├── finite.lean                      Finite Kakeya — complete proofs
│   ├── Monotonicity.lean
│   ├── MultiChamber.lean
│   ├── Examples.lean
│   ├── WaveNumber6/Wavenumber6.lean
│   └── lean/                            Lake project (lakefile.toml)
│
├── Papers
│   ├── autophagy_dm3.pdf / .tex         Ch. A — Autophagy & Triple-Alpha as dm³
│   ├── Collatz_Paper_Grossi2026.pdf
│   ├── Grossi2026_Number33_Intelligencer.pdf
│   ├── GCM-Manifesto.docx.pdf
│   ├── NuclearPhysicsB_latex.pdf
│   ├── G6_TOGT_NASA_MoonBase_Research_Contribution.pdf
│   ├── GTCT_v1.LaTex
│   └── Papers/
│
├── Python simulations
│   ├── dnls_nbonacci.py
│   ├── dnls_long_time.py / _parallel.py
│   ├── nbonacci_criticality.py / nbonacci_critical_lambda.py
│   ├── DNLS/TribonacciDNLS_annotated.ipynb
│   ├── simulations/
│   └── scripts/
│
├── Book 3 — The Mini-Beast (HTML living book)
│   ├── book3/                           chapter map and assets
│   ├── ch00-introduction.html
│   ├── ch01-one-equation.html
│   ├── ch-e-gtct.html                   Ch. E — GTCT bridge
│   ├── chW-wigner.html                  Ch. W — Wigner crystallisation
│   ├── collatz.html                     Ch. H — Collatz
│   ├── chapter-eta-dnls.html            Ch. η — DNLS
│   ├── chapters-pi-phi-mu-eta-delta-sigma-omega.html
│   ├── sample-chapter-autophagy.html    Ch. A
│   ├── sample-chapter-tubulin.html      Ch. T
│   ├── sample-chapter-wigner.html       Ch. W
│   └── living-book.html
│
├── Domain folders
│   ├── AnuclearPhysics/                 Nuclear Physics B materials
│   ├── Autophagy/
│   ├── DNLS/
│   ├── DigitalHerbarium/
│   ├── FruitFly/                        MultiOrbitBioSwarm
│   ├── GTCT/
│   ├── Lexicon/
│   ├── PrincipiaOrthogona_v2/           Vol. II v2a deposit
│   ├── WaveNumber6/
│   └── a.PolyLaminin/
│
├── SVG diagrams
│   ├── 01_operator_sequence.svg
│   ├── 02_saturn_hexagon.svg
│   ├── 03_coherence_bridge.svg
│   ├── 04_collatz_dm3.svg
│   └── 05_domain_map.svg
│
└── Metadata
    ├── README.md                        this file
    ├── AXLE-REPO-PROFILE.md
    ├── ZENODO_DESCRIPTION.md
    ├── CONTRIBUTING.md
    ├── LICENSE                          MIT (code); CC BY 4.0 (papers, figures)
    ├── axle_sorry_roadmap.svg
    └── topics.json
```

---

## AXLE v6.1 — Lean proof status

**File:** `Main_v6.lean` · 0 axioms beyond Mathlib4 · 9 honest sorrys

| Constant | Value | Theorem | Status |
|---|---|---|---|
| ε₀ | 1/3 | `epsilon_zero` | ✅ proved |
| τ | 2 | `tau_contact` | ✅ proved |
| g₃₃ | 33 | `g33_is_invariant` | ✅ proved |
| g₆₄ | 64 = 2⁶ | `g64_equals_two_to_6` | ✅ proved |
| T* | 2π | `T_star` | ✅ proved |
| κ | ≤ √(7/9) ≈ 0.882 | `stability_radius` | ✅ proved |
| τ · ε* | 2/3 | `tau_eps_product` | ✅ proved |
| Gronwall (outer) | ε₀ = 1/3, r > r_att | `epsilon_zero` | ✅ proved |
| Gronwall (inner) | r* ≈ 0.80 | — | ⚠️ sorry — Issue #13 |
| Limit cycle | Poincaré–Bendixson | `limitCycle_exists_auto` | ⚠️ sorry |

### AutophagyDm3_v2.lean — 26 theorems, Issue #14

18 fully proved (no sorry): `contactCoeff_neg`, `V_critical_at_one`, `V_second_deriv_at_one`,
`V_factored`, `V_at_one`, `mu_canonical`, `mu_dm3_neg`, `gronwall_radius`, `basin_asymmetry`,
`contactForm_nondeg_scalar`, `contactForm_orientation`, `V_is_morse_at_one`,
`whitneyFold_conditional` (strengthened — sorry guards Mather's theorem only),
`dm3_basin_compact`, `dm3_basin_nonempty`, and others.

Remaining open: `limitCycle_exists_auto` (Poincaré–Bendixson not yet in Mathlib4).

---

## Open issues

| Issue | Description | Status |
|---|---|---|
| #13 | Gronwall basin asymmetry — inner boundary r* ≠ r_att − ε₀ | open |
| #14 | AutophagyDm3 — Mather's theorem, Poincaré–Bendixson | open |

---

## Reproduce figures

```bash
# Autophagy / Triple-Alpha (Chapter A)
pip install numpy matplotlib
python3 code/autophagy_dm3.py --out figures

# DNLS / N-bonacci criticality
python3 dnls_nbonacci.py
python3 nbonacci_criticality.py
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add files, including via the GitHub mobile app.

## License

Code and Lean 4: MIT · Papers and figures: CC BY 4.0  
© 2026 Pablo Nogueira Grossi · G6 LLC
