# Copilot agent brief: execute the T=10^5 sweep

Paste the entire body below verbatim into a new Copilot agent task on
`grossi-ops/Atratores`.

---

## Context

`dnls_long_time.py` was reconfigured in commit bf91428 with the T=10^5
defaults (T_END=100000.0, N_CHECKPOINTS=375, all other constants
unchanged). The reconfigured script has **not been executed yet**. This
task is to run the sweep and report results. **It is not a "task already
complete" no-op.** No prior session has produced T=10^5 numbers.

## Tasks

1. From the repo root, install dependencies if needed
   (`pip install numpy scipy matplotlib`).
2. Run the T=10^5 sweep with current defaults:
   ```
   python3 dnls_long_time.py
   ```
   This writes `ipr_vs_time.csv`. Time the wallclock.
3. Run the analysis:
   ```
   python3 analyze_long_time.py
   ```
   This writes `spreading_exponents.csv` and the three figures.
4. If a `ipr_vs_time.csv` from the previous T=10^4 run is still in the
   sandbox or the repo, also run the analysis on it once with
   `--csv <that-csv-path>` so we can compare.

## Deliverable — paste back exactly this

In your reply, paste the **raw text** of the following sections from the
T=10^5 sanity report, in this order, with no editing or summarising:

- Section `[1] Linear-limit (lambda=0) flatness check`
- Section `[2] t = 0 IPR values`
- Section `[3] Norm conservation across all runs`
- Section `[4] Final-time IPR(T) by chain and lambda`
- Section `[5] Spreading-exponent fits`

Then, if you also have the T=10^4 CSV available, paste **only**
section `[4]` from that run, prefixed with `### T=10^4 reference:`.

Then report the actual wallclock of the T=10^5 sweep
(e.g. `wallclock: 14m 22s`), and the worst norm drift across all 12 runs
(this is in section [3], but call it out as a single line so we can scan).

## Do NOT

- Do not edit `dnls_long_time.py` or `analyze_long_time.py`. They are
  configured correctly. If anything looks off, report it but don't change
  it.
- Do not change any defaults (T_END, N_CHECKPOINTS, RTOL, ATOL, LAMBDAS,
  N_SITES, NORM_TOL).
- Do not summarise, interpret, or annotate the section text. Paste the
  raw output verbatim. Interpretation happens elsewhere.
- Do not declare this task "already complete in a previous session."
  The T=10^5 sweep has not been executed; that's the point of the task.
- Do not commit anything to the repo unless the script generated output
  files that already would have been committed (e.g. nothing — the CSV
  and figures are gitignored or not normally committed).

## Acceptance criteria

- A T=10^5 `ipr_vs_time.csv` has been produced and read by
  `analyze_long_time.py` without errors.
- Sections [1] through [5] appear verbatim in the reply.
- Wallclock is reported as a single line.
- Worst norm drift is reported as a single line.
