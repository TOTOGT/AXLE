# Copilot Brief — Brief 1 of 3
# Converge α_fib and α_trib at N=2000, T=10⁵

## Goal
Close PRB referee question (1): "Are the α values converged — do you have T=10⁵ at N=2000?"

The current α-table in `section8_draft.md` quotes α_fib≈0.211, α_trib≈0.155 at N=2000 from a T=10⁴ run. A referee will object that the late-tail regression is not in the asymptotic regime. We need T=10⁵ at N=2000 for both chains to confirm the sign-flip persists.

## Repo and branch
- Repo: `grossi-ops/Atratores`
- Branch: `agent/alpha-N2000-T1e5`
- Open as draft PR titled: "α(N) convergence: N=2000, T=10⁵ run"

## Inputs
- Existing script: `dnls_long_time.py` (already supports N, T_END, LAMBDAS as module-level constants)
- Existing analysis: `analyze_long_time.py` with `fit_alpha()` for late-tail regression

## Exact parameters
Modify `dnls_long_time.py` parameters block to:
```python
N_SITES = 2000
T_END = 100000.0          # 10^5
N_CHECKPOINTS = 500       # log-spaced
LAMBDAS = [0.5, 1.0, 1.5, 2.0]
INTEGRATOR = "DOP853"
RTOL = 1e-9               # tighter than before to clear norm-leak flag
ATOL = 1e-11
NORM_TOL = 5e-5           # accept up to 5×10⁻⁵; flag in log if exceeded
CHAINS = ["fibonacci", "tribonacci"]
```

Output CSV: `data/ipr_N2000_T1e5.csv` with columns `time, lambda, chain, IPR, norm`.

## Wallclock budget
At N=2000, T=10⁵ with DOP853 and RTOL=1e-9, expect roughly 30–60 minutes per (λ, chain) pair on a single core. Eight pairs total → 4–8 hours. Run on a self-hosted runner if available; otherwise split across two PRs (λ ∈ {0.5, 1.0} and λ ∈ {1.5, 2.0}).

## Required output (verbatim paste in PR description)
After the run completes, paste the following sections **verbatim** — do not summarize.

### [1] Sanity report (from analyze_long_time.py)
Run `python analyze_long_time.py --csv data/ipr_N2000_T1e5.csv --report` and paste full output.

### [2] α-fit table
For each (λ, chain) pair, fit α from the late tail (t > 10⁴) and report:
```
λ   chain         α       α_stderr   t_min_fit   R²
0.5 fibonacci     ...     ...        ...         ...
0.5 tribonacci    ...     ...        ...         ...
1.0 fibonacci     ...     ...        ...         ...
...
```

### [3] Comparison to T=10⁴ values
Quote the previously fit α values from `ipr_lambda1p5_N1000_T1e5.csv` and the prior T=10⁴ runs side-by-side with the new N=2000, T=10⁵ values. State whether α_fib remains in [0.20, 0.22] and whether α_trib continues to decrease.

### [4] Norm conservation
Maximum norm leak across all checkpoints: ____. Flag if any single point exceeds 5×10⁻⁵.

### [5] Plot
Generate `figures/alpha_N2000_T1e5.png` showing IPR(t) on log-log for all 8 (λ, chain) pairs, with α-fit lines overlaid in the t > 10⁴ window.

## Definition of done
- PR shows green CI
- All 5 verbatim sections pasted in PR description
- CSV committed under `data/`
- Figure committed under `figures/`
- No silent parameter changes (e.g., do not relax NORM_TOL further than specified above)

## Anti-hallucination guard
Do **NOT** claim the task is "already complete" without producing the CSV. Do **NOT** invent α values. If the run is interrupted, commit partial CSV and report which (λ, chain) pairs completed.
