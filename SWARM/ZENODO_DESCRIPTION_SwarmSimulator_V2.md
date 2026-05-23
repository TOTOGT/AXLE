# ZENODO_DESCRIPTION_SwarmSimulator_V2.md
# Paste this into the Zenodo description field for the V2 upload.

---

## The Swarm Simulator: A Dynamical Systems Model of Collective Intelligence Using the TO/TOGT Operator Pipeline
### Version 2 — May 2026

**Pablo Nogueira Grossi · G6 LLC, Newark NJ · ORCID: 0009-0000-6496-2186**
Zenodo V2 DOI: 10.5281/zenodo.20230613
V1 DOI: 10.5281/zenodo.19208284
Series root: https://doi.org/10.5281/zenodo.19117399
AXLE: https://github.com/TOTOGT/AXLE

---

### What this paper does

We introduce the Swarm Simulator, a multi-agent dynamical system based on the generative operator pipeline G = U ∘ F ∘ K ∘ C from Topographical Orthogonal Generative Theory (TO/TOGT). Each agent undergoes local compression, curvature intensification, loss of injectivity, and stabilisation. At the collective level, four operators — shared-intent stability I_t, coordination efficiency C_t, type-propagation multiplier M_t, and diffusion factor F_t — govern the swarm's evolution.

All mathematical results follow directly from previously proved theorems in the Principia Orthogona series: fixed-point theory, contraction mapping, saturated pitchfork bifurcation, and the algebraic separation theorem. No empirical claims, numerical simulations, or unverifiable assertions are made in V1. Version 2 adds reproducible simulation code and formal Lean 4 verification.

---

### What V2 adds

**1. `SwarmSimulator.lean` — Lean 4 / Mathlib4 formal verification**
12 theorems proved without sorry, 0 axioms beyond Mathlib4:
- T1: Contraction arithmetic core (L = LI+LC+LM < 1 ∧ L > 0)
- T2: Unique fixed point arithmetic core (1 − L > 0)
- T3: Global convergence (Lⁿ · r ≤ r for L < 1)
- T4: L_total > 0
- T5: L_total < 1 under hypothesis
- T6: Stabilising operator decreases I (when η > 0, factors ≤ 1)
- T7: Coordination operator decreases C (when I_new ≤ 1)
- T8: Diffusion operator strictly increasing in t (α > 0)
- T9: System invariant strictly exceeds every orbit invariant (§6)
- T10: Lⁿ ≤ L for n ≥ 1 (convergence rate)
- T11: Composition of contractions is a contraction
- T12: State space dimension = 4

Two honest open obligations: S1 (full Banach space proof); S2 (multi-orbit existence via Poincaré–Bendixson).

**2. `swarm_simulator.py` — Full Python simulator**
- SwarmParams dataclass with derived Lipschitz constants LI, LC, LM, L
- step() function from §7 (minimal simulator)
- evolve(): full T-step time evolution
- find_fixedpoint(): approximate fixed point by long-run iteration
- Multi-orbit simulation (two independent clusters, §6)
- Figure generator: all 4 figures
- Default parameters satisfy L ≈ 0.81 < 1 (Theorem 5.1)

Dependencies: numpy, matplotlib. Run: `python swarm_simulator.py`

**3. Individual figure PDFs**
- `fig1_state_evolution.pdf` — I, C, M, F over time (contractive regime)
- `fig2_convergence.pdf` — ‖Xt − X*‖₁ geometric decay (Theorem 5.3)
- `fig3_contraction_region.pdf` — L = LI+LC+LM parameter space map
- `fig4_multi_orbit.pdf` — Two independent clusters, distinct fixed points (§6)

**4. `CHANGES_SwarmSimulator.md`** — V1 → V2 version history

**5. `OPEN_QUESTIONS_SwarmSimulator.md`** — 4-row table with status and closure paths

---

### Proved without sorry (12 facts)

T1 Contraction arithmetic core · T2 Unique fixed point · T3 Global convergence ·
T4 L > 0 · T5 L < 1 · T6 Stabilising operator monotonicity ·
T7 Coordination operator monotonicity · T8 Diffusion strictly increasing ·
T9 Multi-orbit system invariant · T10 Convergence rate (Lⁿ ≤ L) ·
T11 Contraction composability · T12 State space dimension = 4

### Open obligations (2)

| ID | Description | Status |
|----|-------------|--------|
| S1 | Full Banach space contraction (MetricSpace + Banach theorem) | Open — arithmetic core proved |
| S2 | Multi-orbit existence (Poincaré–Bendixson on ℝ⁴) | Open — invariant proved (T9) |

---

### Build instructions

**Lean 4:**
```
lake update && lake build SwarmSimulator
```
Dependencies: Mathlib4 (current stable)

**Python:**
```
pip install numpy matplotlib
python swarm_simulator.py
```
Outputs: fig1–fig4 as PDF and PNG in ./figures/

---

### Relation to prior work

Classical models (Cucker–Smale, Olfati-Saber, Langevin-based cooperation) demonstrate
global order from simple local rules. Bifurcation analyses (Leonard, Gray et al.) show
multi-stable states from symmetry-breaking. The Swarm Simulator recovers these
qualitative behaviours through a single algebraic operator pipeline from TO/TOGT,
yielding contraction, fixed-point, and multi-orbit guarantees across all four collective
quantities. All results follow from previously proved theorems; no new empirical
predictions are made.

---

### Series context

| Role | DOI |
|------|-----|
| Series root | 10.5281/zenodo.19117399 |
| Volume I (mathematics) | 10.5281/zenodo.19117400 |
| Multi-agent biology companion | 10.5281/zenodo.19208015 |
| Multi-Orbit Identity Theory | 10.5281/zenodo.20230614 |
| This deposit (V2) | 10.5281/zenodo.20230613 |
| AXLE formal verification hub | github.com/TOTOGT/AXLE |

**MSC codes:** 37C25, 37D10, 37G10, 47H10, 68T99

**Keywords:** swarm simulator · collective intelligence · TO/TOGT ·
operator pipeline · contraction mapping · fixed point · multi-orbit ·
Lean 4 formal verification · Principia Orthogona · G6 LLC

**License:** CC BY-NC-ND 4.0 (paper) · MIT (code)
**Copyright:** © 2026 Pablo Nogueira Grossi, G6 LLC
**Contact:** pgrossi888@outlook.com · g6llc@proton.me
