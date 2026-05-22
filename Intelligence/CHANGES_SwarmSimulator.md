# The Swarm Simulator — Version History

## Version 2 (May 2026) — Current
**DOI:** 10.5281/zenodo.20230613

### What V2 adds relative to V1:
- `SwarmSimulator.lean` added directly to the deposit: 12 theorems proved
  without sorry, 0 axioms beyond Mathlib4. Covers Theorems 5.1–5.3
  (contraction, unique fixed point, global convergence), the multi-orbit
  invariant (§6), and 6 auxiliary operator lemmas. Two honest open
  obligations (S1: Banach space, S2: multi-orbit existence).
- `swarm_simulator.py` — full runnable simulator with SwarmParams dataclass,
  step() function (as in §7), evolve(), fixed-point detection, multi-orbit
  simulation, and figure generator. Default parameters satisfy L < 1 (≈ 0.81)
  as required by Theorem 5.1.
- Individual figure PDFs: fig1–fig4 (state evolution, convergence,
  contraction region, multi-orbit).
- `CHANGES_SwarmSimulator.md` (this file): explicit version history.
- `OPEN_QUESTIONS.md`: open questions table with status column.
- Contraction parameter note: the default parameters in swarm_simulator.py
  are chosen so that LI + LC + LM ≈ 0.81 < 1, satisfying Theorem 5.1.
  The paper's §7 code snippet shows the step() function only; the full
  parameter constraints are now explicitly documented.

### Files in V2 deposit:
| File | Description |
|------|-------------|
| `swarm_simulator_paper.pdf` | Full paper (V1/V2) |
| `SwarmSimulator.lean` | Lean 4 / Mathlib4 formal proofs (12 facts, 0 sorry) |
| `swarm_simulator.py` | Python simulator and figure generator |
| `fig1_state_evolution.pdf` | I, C, M, F over time (contractive regime) |
| `fig2_convergence.pdf` | ‖Xt − X*‖ → 0 geometric decay (Theorem 5.3) |
| `fig3_contraction_region.pdf` | L = LI+LC+LM parameter space |
| `fig4_multi_orbit.pdf` | Two independent clusters, distinct fixed points (§6) |
| `CHANGES_SwarmSimulator.md` | This version history |
| `OPEN_QUESTIONS.md` | Open questions with status |

---

## Version 1 (March 2026)
**DOI:** 10.5281/zenodo.19208284

### Contents:
- Paper PDF (4 pages): swarm state space (§2), collective operators (§3–4),
  contraction and fixed-point theorems (§5), multi-orbit emergence (§6),
  minimal simulator code snippet (§7).
- No Lean verification file.
- No Python simulation script (only the 9-line step() function in the paper).
- No figures.
- References to prior work: Cucker–Smale [6], Olfati-Saber [5], Rivera-Ortiz [3],
  Leonard [4], Nitti et al. [1], Sar & Ghosh [2], Gray et al. [7].
