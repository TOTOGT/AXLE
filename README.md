# AXLE — Formal Verification Hub
### Principia Orthogona Series · G6 LLC · Newark NJ · 2026

**AXLE** (Algebraic eXpression Language for Evaluation) is the formal verification repository for the
*Principia Orthogona* series. It contains Lean 4 / Mathlib4 proof files, Python simulations,
companion papers, and the HTML living-book chapters for Book 3 (The Mini-Beast).

**0 axioms beyond Mathlib4 · 9 honest sorrys · AXLE v6.1**

Author: Pablo Nogueira Grossi · ORCID: [0009-0000-6496-2186](https://orcid.org/0009-0000-6496-2186)
Contact: g6llc@proton.me · G6 LLC · Newark, NJ

---

## Applied lines — economics, finance, and AI systems

The framework is not confined to mathematical physics. Several lines apply it directly to markets,
credit, and multi-agent AI, under the same discipline as the rest of the repository: reproducible
pipelines, machine-checked constants, and open problems stated rather than hidden.

### Economics and finance

| Work | Location | What it is |
|---|---|---|
| **The Response Gap** | [`Economics/`](Economics) | Algorithmic credit and automated liquidation treated as an auditable governance object; proposes response-time budgets and epistemic-disclosure standards for underwriting models. [doi:10.5281/zenodo.21752834](https://doi.org/10.5281/zenodo.21752834) |
| **The Forced Urgency Gap** (WP-32) | [`Economics/`](Economics) | Non-identification of loss aversion under latent liquidity constraints. Reproducible FRED / Federal Reserve Z.1 pipeline (Python, 1971–2026) with the 2020 and 2022 liquidity shocks as natural experiments. Six-theorem Lean core, kernel-verified, no `sorryAx`. |
| **The Banking Butterfly** | [`Economics/`](Economics) | Precision asymmetry in Brazilian retail banking: the spread between rates for borrowers with alternatives and borrowers without. |
| **Positional Dominance under Non-Contestability** | [`NetworkGamesJOMO/`](NetworkGamesJOMO) | Two-player stochastic network game: hub control dominates velocity investment above a threshold σ\* ≈ 1/3. Associated constants machine-checked in Lean 4. |
| **The One-Third Invariant** (companion) | [`NetworkGamesJOMO/`](NetworkGamesJOMO) | Companion paper on the 1/3 threshold shared with the dm³ stability radius ε₀. |
| **WorldQuant International Quant Championship 2026** | [`NetworkGamesJOMO/`](NetworkGamesJOMO) | Gold, Silver, and Bronze certificates. |
| **CapitalGuard Trader** | [`Finance/`](Finance) | Risk-first single-name trading system — ATR trailing stops, 0.75% max risk per trade, hard daily loss limit — with backtests, a paper-trading bot, and live setup dashboards. |
| **Grid-bot backtest (BTC/ETH)** | [`Finance/`](Finance) | Backtest of a grid strategy across two crypto pairs. |
| **Ponte Nova** | [`Finance/fednow-margin.html`](Finance/fednow-margin.html) | Instant-payments concept built on FedNow settlement timing, aimed at users underserved by existing rails. |

### AI and multi-agent systems

| Work | Location | What it is |
|---|---|---|
| **SwarmSimulator** | [`Intelligence/`](Intelligence) · [`SWARM/`](SWARM) | Multi-agent convergence under the dm³ operators — Lean 4 formalization, Python simulator, contraction-region and convergence figures, and a standing open-questions log. |
| **Multi-Agent TOGT** | [`BioPhysics/`](BioPhysics) · [`FruitFly/`](FruitFly) | Multi-agent instantiation with a Lean companion (`MultiAgentTogt.lean`), simulation code, and agent-trajectory figures. |
| **Contact No-Go API** | [`nogo-api/`](nogo-api) | Flask service exposing transverse-stability and cosmological no-go results as HTTP endpoints. Every route computes something backed by a named theorem — a thin numeric wrapper over proved math, not a black box. |
| **RAG & Context Engineering** | [`AULA/rag-course/`](AULA/rag-course) | Full eight-week course worked end to end: retrieval decisions, classical retrieval, evaluation, and a production RAG capstone, with per-week labs and build scripts. |

**Why these sit in a formal-verification repository.** A margin call, a liquidation cascade, and a
swarm of agents settling into consensus are one object at different scales: a system iterating under
constraint toward a fixed point, with a threshold separating stable from degenerate behaviour. That
threshold is ε₀ = 1/3 in the dm³ core and σ\* ≈ 1/3 in the network game. The economics lines are
where the framework meets data that fights back.

---

## Series and Zenodo

| Record | DOI | Contents |
|---|---|---|
| Series root | [10.5281/zenodo.19117399](https://doi.org/10.5281/zenodo.19117399) | All volumes |
| Vols. I–III + Applications | [10.5281/zenodo.19117400](https://doi.org/10.5281/zenodo.19117400) | GOMC Science |
| Vol. II v2a (Contact Geometry) | [10.5281/zenodo.21148424](https://doi.org/10.5281/zenodo.21148424) | TOGT + AXLE skeleton |
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
│ ├── Main_v6.lean AXLE v6.1 master — 0 extra axioms, 9 sorrys
│ ├── AXLE.lean / AXLE_v5_1.lean / AXLE_v6.lean
│ ├── AutophagyDm3.lean Ch. A — 18 theorems proved
│ ├── AutophagyDm3_v2.lean 26 theorems, Issue #14 obligations
│ ├── TribonacciMeasure.lean Tribonacci / DNLS measure
│ ├── gronwall_proof.lean Gronwall contraction (Issue #13)
│ ├── DiscreteDM3.lean / discreteDm3.lean
│ ├── Dm3Comp.lean dm³ compositional structures
│ ├── Dm3GoldbachToy.lean / Dm3NSToy.lean / Dm3RHToy.lean
│ ├── finite.lean Finite Kakeya — complete proofs
│ ├── Monotonicity.lean
│ ├── MultiChamber.lean
│ ├── Examples.lean
│ ├── WaveNumber6/Wavenumber6.lean
│ └── lean/ Lake project (lakefile.toml)
│
├── Papers
│ ├── autophagy_dm3.pdf / .tex Ch. A — Autophagy & Triple-Alpha as dm³
│ ├── Collatz_Paper_Grossi2026.pdf
│ ├── Grossi2026_Number33_Intelligencer.pdf
│ ├── GCM-Manifesto.docx.pdf
│ ├── NuclearPhysicsB_latex.pdf
│ ├── G6_TOGT_NASA_MoonBase_Research_Contribution.pdf
│ ├── GTCT_v1.LaTex
│ └── Papers/
│
├── Python simulations
│ ├── dnls_nbonacci.py
│ ├── dnls_long_time.py / _parallel.py
│ ├── nbonacci_criticality.py / nbonacci_critical_lambda.py
│ ├── DNLS/TribonacciDNLS_annotated.ipynb
│ ├── simulations/
│ └── scripts/
│
├── Book 3 — The Mini-Beast (HTML living book)
│ ├── book3/ chapter map and assets
│ ├── ch00-introduction.html
│ ├── ch01-one-equation.html
│ ├── ch-e-gtct.html Ch. E — GTCT bridge
│ ├── chW-wigner.html Ch. W — Wigner crystallisation
│ ├── collatz.html Ch. H — Collatz
│ ├── chapter-eta-dnls.html Ch. η — DNLS
│ ├── chapters-pi-phi-mu-eta-delta-sigma-omega.html
│ ├── sample-chapter-autophagy.html Ch. A
│ ├── sample-chapter-tubulin.html Ch. T
│ ├── sample-chapter-wigner.html Ch. W
│ └── living-book.html
│
├── Applied lines
│ ├── Economics/ Response Gap, Forced Urgency (WP-32), Banking Butterfly
│ ├── NetworkGamesJOMO/ Positional dominance, one-third invariant, IQC certificates
│ ├── Finance/ CapitalGuard Trader, backtests, dashboards, Ponte Nova
│ ├── Intelligence/ · SWARM/ SwarmSimulator — multi-agent convergence
│ ├── BioPhysics/ Multi-Agent TOGT (Lean + simulation)
│ ├── AULA/rag-course/ RAG and context-engineering course
│ └── nogo-api/ Contact No-Go API (Flask, theorem-backed endpoints)
│
├── Domain folders
│ ├── AnuclearPhysics/ Nuclear Physics B materials
│ ├── Autophagy/
│ ├── DNLS/
│ ├── DigitalHerbarium/
│ ├── FruitFly/ MultiOrbitBioSwarm
│ ├── GTCT/
│ ├── Lexicon/
│ ├── PrincipiaOrthogona_v2/ Vol. II v2a deposit
│ ├── WaveNumber6/
│ └── a.PolyLaminin/
│
├── SVG diagrams
│ ├── 01_operator_sequence.svg
│ ├── 02_saturn_hexagon.svg
│ ├── 03_coherence_bridge.svg
│ ├── 04_collatz_dm3.svg
│ └── 05_domain_map.svg
│
└── Metadata
├── README.md this file
├── AXLE-REPO-PROFILE.md
├── ZENODO_DESCRIPTION.md
├── CONTRIBUTING.md
├── LICENSE MIT (code); CC BY 4.0 (papers, figures)
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
