# Open Questions — The Swarm Simulator

Status as of Version 2, May 2026.
Tracked in AXLE issue tracker: https://github.com/TOTOGT/AXLE

| ID | Description | Status | Lean file | Closure path |
|----|-------------|--------|-----------|--------------|
| S1 | **Full Banach space contraction proof** (Theorem 5.1). The arithmetic core (L < 1, 0 < L) is proved in T1–T5 of SwarmSimulator.lean. The full proof requires SwarmState as a complete metric space and invocation of Banach's fixed-point theorem (`Mathlib.Topology.MetricSpace.Contraction`). | **Open** — arithmetic core proved (0 sorry); metric space structure pending | `SwarmSimulator.lean` §3 | Define SwarmState as `MetricSpace`, prove Gswarm is Lipschitz, invoke `Mathlib.Topology.MetricSpace.Contraction.contractionMapping` |
| S2 | **Multi-orbit existence theorem** (§6). The system-level invariant Inv(S) ⊋ ⋃ Inv(Oᵢ) is proved (T9). Existence of the individual orbits Oᵢ requires either Poincaré–Bendixson on ℝ⁴ or explicit fixed-point construction for each cluster. | **Open** — invariant structure proved (T9, 0 sorry); orbit existence pending | `SwarmSimulator.lean` §6 | Prove each cluster satisfies T1–T3 independently, then apply T9 to the collection; or invoke `Mathlib.Dynamics.OmegaLimit` |
| S3 | **Empirical calibration of default parameters**. The contraction condition LI + LC + LM < 1 constrains the parameter space. The default parameters in swarm_simulator.py (L ≈ 0.81) satisfy the condition; real swarm systems may not. Calibration against the datasets of Sinhuber et al. (2019) or Nitti et al. (2025) would ground the parameters empirically. | **Open** — noted as future work; no Lean obligation | None | Fit parameters to trajectory data from Zenodo 10.5281/zenodo.19208015 companion deposit |
| S4 | **Discrete-time Gronwall bound** (Theorem 5.3). The bound ‖Xt − X*‖ ≤ Lᵗ · ‖X0 − X*‖ follows from iterated application of the Lipschitz condition. The arithmetic core (Lⁿ · r ≤ r for L < 1) is proved (T3, T10). The full discrete Gronwall inequality in Lean requires a formal induction over SwarmState with the ℓ¹ norm. | **Open** — bound structure proved; formal induction pending | `SwarmSimulator.lean` §3–4 | Formal induction: if ‖Gswarm(X) − Gswarm(Y)‖ ≤ L · ‖X − Y‖ then by induction ‖Xₙ − X*‖ ≤ Lⁿ · ‖X₀ − X*‖ |

## Notes on sorry count

`SwarmSimulator.lean` contains **0 sorry**.
All 12 theorems are proved without sorry and without axioms beyond Mathlib4.
Open obligations S1–S4 are documented as future work, not as sorrys — the
arithmetic cores of all main theorems are fully proved.

## Comparison with previous version

| Obligation | V1 status | V2 status |
|------------|-----------|-----------|
| S1 (Banach contraction) | Not in deposit | Arithmetic core proved (T1–T5, 0 sorry); full metric space pending |
| S2 (Multi-orbit existence) | Not in deposit | Invariant proved (T9, 0 sorry); orbit existence pending |
| S3 (Parameter calibration) | Not noted | Documented as open |
| S4 (Discrete Gronwall) | Not in deposit | Bound proved (T3, T10, 0 sorry); formal induction pending |
