# Copilot Brief — Brief 4
# T=10⁶ verification: does fib catch up to trib?

## Goal
Brief 1 found α_fib(λ=1.5) ≈ 0.487, α_trib(λ=1.5) ≈ 0.778 at N=2000, T=10⁵. Brief 2 found that at T=10⁵ the IPR ratio trib/fib is 1.24× (N=1000) → 1.38× (N=2000) — tribonacci is still more retained, but the differential is shrinking. Naive α-extrapolation predicts the cross-over (fib > trib) around T ~ 1.4×10⁶.

This brief tests that prediction directly. If the cross-over happens, Section 8 closes with a clean two-regime story: trib wins at finite time, fib wins asymptotically. If the cross-over does not happen, the α-extrapolation is wrong (probably because α slows down further between 10⁵ and 10⁶) and the paper's narrative becomes "trib wins throughout the studied range; whether it wins asymptotically is open."

Either outcome is publishable. We just need to know which.

## Repo and branch
- Repo: `grossi-ops/Atratores`
- Branch: `agent/T1e6-verification`
- Open as draft PR titled: "T=10⁶ verification at N=1000, λ=1.5: does fib catch up?"

## Inputs
- Existing script: `dnls_long_time.py` (already supports module-level constants for N_SITES, T_END, LAMBDAS, RTOL, ATOL)
- Existing analysis: `analyze_long_time.py` with `fit_alpha_full()` and `--report` mode
- Existing CSV (T=10⁵, N=1000, λ=1.5): `data/ipr_lambda1p5_N1000_T1e5.csv`
- Existing CSV (T=10⁵, N=2000, λ=1.5): `data/ipr_lambda1p5_N2000_T1e5.csv`

## Exact parameters
Modify `dnls_long_time.py` parameters block to:
```python
N_SITES = 1000
T_END = 1000000.0         # 10^6
N_CHECKPOINTS = 600        # log-spaced; ~100/decade over 6 decades
LAMBDAS = [1.5]            # single λ — this is a verification run, not a sweep
INTEGRATOR = "DOP853"
RTOL = 1e-9
ATOL = 1e-11
NORM_TOL = 1e-4            # accept up to 1×10⁻⁴ at T=10⁶ (longer integration ⇒ more drift)
CHAINS = ["fibonacci", "tribonacci"]
```

Output CSV: `data/ipr_lambda1p5_N1000_T1e6.csv` with columns `time, lambda, chain, IPR, norm`.

## Wallclock budget
At N=1000, T=10⁶ with DOP853 and RTOL=1e-9, expect roughly 15–30 minutes per chain. Two chains → ~30–60 minutes total. If wallclock exceeds 2 hours, abort and commit partial CSV with a note.

## Required output (verbatim paste in PR description — do not summarize)

### [1] Final-time IPR comparison
```
λ=1.5, N=1000:
  T=10⁴ : IPR_fib = ____, IPR_trib = ____, ratio fib/trib = ____, trib/fib = ____×
  T=10⁵ : IPR_fib = ____, IPR_trib = ____, ratio fib/trib = ____, trib/fib = ____×
  T=10⁶ : IPR_fib = ____, IPR_trib = ____, ratio fib/trib = ____, trib/fib = ____×

Cross-over (trib/fib < 1):  YES at t = ____  /  NO (trib still > fib at T=10⁶)
```
The T=10⁴ and T=10⁵ values come from the existing CSVs. The T=10⁶ value is the new run.

### [2] α-fit table at three time windows
Run `analyze_long_time.py` on `data/ipr_lambda1p5_N1000_T1e6.csv` with `fit_alpha_full()` over three windows:
```
t > 10⁴   (matches Brief 1 window — should reproduce α_fib≈0.49, α_trib≈0.78)
t > 10⁵   (new asymptotic window — tells us whether α slows or holds)
t > 3×10⁵ (last half-decade — most asymptotic estimate available)
```
Report each as:
```
window       chain        α       α_stderr   R²       n_pts
t > 10⁴      fibonacci    ...     ...        ...      ...
t > 10⁴      tribonacci   ...     ...        ...      ...
t > 10⁵      fibonacci    ...     ...        ...      ...
...
```

### [3] Cross-over prediction
From the t > 10⁵ window α-fit, extrapolate when the ratio trib/fib reaches 1.0:
```
t_cross_predicted = T × (current_ratio)^(1 / (α_trib - α_fib))
                  = 10⁶ × (trib/fib at T=10⁶)^(1 / (α_trib - α_fib at t>10⁵))
                  = ____
```
State whether this is consistent with Brief 1's prediction (≈1.4×10⁶) or significantly different.

### [4] Norm conservation
Maximum norm leak across all checkpoints: ____. Flag if any single point exceeds 1×10⁻⁴.

### [5] Plot
Generate `figures/T1e6_lambda1p5_N1000.png` showing:
- Top panel: log-log IPR(t) for both chains over t ∈ [1, 10⁶], with α-fit lines for each window
- Bottom panel: ratio trib/fib vs t on log-x, linear-y, with horizontal line at 1.0 and vertical line at predicted t_cross

### [6] Section 8 update
Add a one-paragraph subsection (Section 8.7 or extension to 8.6) titled "Cross-over verification at T=10⁶" stating the result. If cross-over happened: quote the time and ratio. If not: state how far the ratio fell and what α-fit gives for the asymptotic prediction. Either way, the paper's narrative gets one of two clean sentences:
- "Tribonacci dominates retention up to T=10⁶, after which fibonacci surpasses it; the cross-over is consistent with the spreading-exponent extrapolation α_trib > α_fib."
- "Tribonacci retains higher IPR throughout T ∈ [50, 10⁶]. While the spreading exponents satisfy α_trib > α_fib, indicating the differential continues to shrink with time, the cross-over is not reached within the integration window."

## Definition of done
- CSV committed at `data/ipr_lambda1p5_N1000_T1e6.csv`
- Figure committed at `figures/T1e6_lambda1p5_N1000.png`
- All 6 verbatim sections in PR description
- Section 8 paragraph appended to `section8_draft.md`
- PR green

## Anti-hallucination guard
Do **NOT** invent the cross-over time. Compute it from the data. If the ratio at T=10⁶ is still > 1, do not paper over it; state it directly. Do **NOT** claim the α-fit "matches Brief 1" without showing the numbers side-by-side. The reproduction in window [1] (t > 10⁴) is the integrity check — if α_fib at t > 10⁴ in this run differs from Brief 1's 0.487 by more than 5%, something is wrong with the integration setup; investigate before committing.
