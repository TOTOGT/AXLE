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

## Build & toolchain

AXLE is pinned to **Lean 4.14.0** (`lean-toolchain`) — deliberately older than `geometry` (the
*Principia Orthogona* / CatGT formalization repo, pinned to Lean 4.32). `mathlib` has to track a
revision compatible with 4.14, and it can silently stop doing so.

**Known failure mode.** `lake` can report `manifest out of date: git url of dependency 'mathlib'
changed; use lake update mathlib`. If that's ignored, the checked-out `mathlib` package can end up
on a revision meant for a newer toolchain (observed: one matching `geometry`'s 4.32 line, not
AXLE's 4.14). Two symptoms of this were both seen directly, not inferred: `AXLE_v5_1.lean` failing
on deprecated `Ordinal` APIs and unknown constants that simply don't exist in 4.14-era mathlib; and
`lake env lean` on any file importing `Mathlib.Order.Ordinal.Basic` (e.g. `AXLE_v6.lean`) failing
with `object file '.../Mathlib/Order/Ordinal/Basic.olean' ... does not exist` — a missing build
artifact, not a bug in the file being compiled.

**Fix.** `lake update mathlib` re-resolves the dependency to the toolchain-matching revision —
confirmed here by `cat .lake/packages/mathlib/lean-toolchain` reading back `v4.14.0` after running
it, matching AXLE's own pin. That alone does **not** produce any `.olean` files, though — nothing
compiles until a full `lake build` actually runs afterward, and it should be treated as a cold
build (the old revision's `.olean`s are stale) even though the project has built before.

**Status as of 2026-09-23 (updated after the full rebuild finished): two separate
problems confirmed, not one.**

1. `AXLE_v5_1.lean` has real, pre-existing bugs, unrelated to the mathlib
revision — the exact same errors, at the exact same lines, appear before and
after `lake update mathlib`: deprecated `Ordinal.lt_add_of_pos_right` /
`Ordinal.IsLimit.add_right`, several type mismatches, three literal syntax
errors (`unexpected token ';'`), and references to struct fields (`mu_max`,
`tau`, `triple`, `layer_count`) that don't exist on `Dm3Triple` /
`RegenerationLevel` / `OrdinalRegenerationLevel`. This needs an actual code
fix in that file. Not attempted here — that's a separate task from Theorem
Alpha and isn't done unprompted.

2. `finite.lean` (`AXLE/Kakeya/Finite.lean`, pulled in by `AXLE.lean`) is
**not** a code bug — it's a genuine mathlib-vintage mismatch. The resolved
mathlib commit (`4bbdccd9c5`, 2024-12-02) correctly matches AXLE's declared
Lean 4.14.0 toolchain, but at that commit: `Mathlib.Analysis.NormedSpace.FiniteDimensional`
has been renamed to `Mathlib.Analysis.Normed.Module.FiniteDimension`;
`Mathlib.MeasureTheory.Measure.Lebesgue` is a folder, not an importable leaf
module (needs a specific submodule, e.g. `.Basic`); and
`Mathlib.MeasureTheory.Measure.Haar.AffineSubspace` does not exist anywhere
in that mathlib snapshot at all — confirmed by a full-repo search, zero
matches. `finite.lean` was written against a newer mathlib than the
toolchain this repo is actually pinned to. Fixing it means either updating
its imports to what 4.14-era mathlib actually offers (and finding a
substitute for the Haar/affine-subspace result, if one exists at that
vintage), or bumping the toolchain forward — both real decisions, not made
here.

Disk space is not the cause: 31 GiB free of 228 GiB at the time of this
build.

**Update 2026-09-26 — `AXLE_v6.lean` confirmed.** A direct `lake env lean AXLE_v6.lean`
run on this toolchain gives no errors and no `sorry`, only unused-variable warnings, matching
the v6.2 audit log in the file. Zero `sorry` is not the same as every theorem being
substantive: the file's own FINAL STATUS v6.2 lists which results are real and which are
vacuous (for example, `gtct_t1` returns its own hypothesis). `Dm3Comp.lean`, `Main_v6.lean`
and `TribonacciRatioConvergence.lean` have not been re-run and remain unconfirmed.

This matters beyond `AXLE_v5_1.lean` itself: `AXLE_v6.lean`, `Dm3Comp.lean`, `Main_v6.lean`, and
`TribonacciRatioConvergence.lean` are the live corpus backing the `open_sorry_core` pool for
**Theorem Alpha 50¢** (`~/Desktop/TheoremAlpha50c`), which shells out to `lake env lean` against
this repo for real kernel verification. A broken toolchain here silently breaks that game's
verification pipeline too, with no separate warning on the game's side.

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
