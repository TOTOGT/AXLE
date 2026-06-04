# Follow-up PR brief: align dnls_long_time.py defaults with the paper

Paste the body below verbatim into a new Copilot agent task on
`grossi-ops/Atratores`. The task should produce a single small commit on a
new branch and open a PR against `main`.

---

## Task

Open a follow-up PR titled **"align dnls_long_time.py defaults with the
paper"** that makes a three-line change to `dnls_long_time.py` at the repo
root. No other files. No refactors. No new features. Just align the
defaults with what the merged PR description claimed.

### Branch

`copilot/align-long-time-dnls-defaults`

### File: `dnls_long_time.py`

In Section 3 ("Sweep constants"), change exactly three constants:

```diff
-N_SITES = 89          # chain length (13th Fibonacci number)
+N_SITES = 500         # chain length, matching Table 1 of the paper
```

```diff
-NORM_TOL = 1e-3       # flag if |‖ψ‖₂ − 1| > NORM_TOL at any checkpoint
+NORM_TOL = 1e-5       # tight threshold; DOP853 at rtol=1e-8 should clear it easily
```

```diff
-LAMBDAS = [1.0, 2.0, 4.0, 8.0]   # nonlinearity strengths to sweep
+LAMBDAS = [0.0, 1.0, 2.0, 4.0, 8.0, 10.0]   # lambda=0 is the linear-limit sanity check
```

Also update the corresponding default in the `--lambdas` argparse help
string to read `default: 0.0 1.0 2.0 4.0 8.0 10.0`.

### Why these specific values

- **N=500**: the paper's Table 1 and the differential-IPR figure are at
  N=500. N=89 (F_11) was a regression introduced in the original PR.
- **lambda=0**: provides the linear-limit sanity check. At lambda=0 the
  DNLS reduces to linear evolution of an eigenstate, so IPR(t) must be
  flat at the t=0 value to within integration error. Without it we have
  no way to confirm the integrator is correct.
- **NORM_TOL=1e-5**: at T=10^3 with DOP853 at rtol=1e-8, expected norm
  drift is on the order of 10^-7 to 10^-9. A 10^-3 threshold only fires
  on catastrophic failure; a 10^-5 threshold is the right diagnostic for
  the slow drift that would actually disqualify a long-time run.

### Acceptance criteria

- The diff is exactly the three constant changes plus the help-string
  update. No other lines should be touched.
- `python dnls_long_time.py --help` still works.
- `python dnls_long_time.py -N 8 -T 1.0 --checkpoints 4` still runs
  (smoke test for the CLI; do not commit any output CSV).
- PR description quotes the three lines being changed and explains *why*
  each default is changing, in one sentence each.

### Do NOT

- Do not change the RHS, integrator, tolerances, or output format.
- Do not "while you're there" any other refactors.
- Do not add docs, READMEs, or tests in this PR.
