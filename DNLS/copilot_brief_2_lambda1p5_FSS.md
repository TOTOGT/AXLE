# Copilot Brief — Brief 2 of 3
# Complete the λ=1.5 row in the FSS table at T=10⁴

## Goal
Close PRB referee question (3): "Can you add λ=1.5 to the FSS table to match the original paper's central claim?"

The Zenodo paper's headline result is at λ=1.5. The current FSS table covers λ ∈ {0.5, 1.0, 2.0, 3.0, 4.0, 5.0} at T=10⁴ across N ∈ {500, 1000, 2000} but is missing the λ=1.5 row. The earlier sweep produced `ipr_lambda1p5_T1e4.csv` (showing the non-monotone 1.69 → 4.15 → 3.10 ratio) but that CSV is not yet folded into the canonical FSS table.

## Repo and branch
- Repo: `grossi-ops/Atratores`
- Branch: `agent/fss-lambda1p5-row`
- Open as draft PR titled: "FSS table: add λ=1.5 row at T=10⁴"

## Inputs
- Existing CSV: `data/ipr_lambda1p5_T1e4.csv` (already has N=500, 1000, 2000)
- Existing script: `fss_analyze.py` with `--lambda-sweep` mode
- Existing draft: `section8_draft.md` containing the FSS table

## Tasks

### Task A — Verify the existing CSV is complete
Run `fss_analyze.py --csv data/ipr_lambda1p5_T1e4.csv --report` and confirm:
- Three N values present: 500, 1000, 2000
- Both chains present at each N
- Final-time IPR values are clean (no NaN, no norm violations)

### Task B — Compute the row
For each N ∈ {500, 1000, 2000}, compute at the final time T=10⁴:
- IPR_fib(N), IPR_trib(N), retention ratios, and the differential ratio IPR_fib / IPR_trib
- Quote to 3 significant figures

### Task C — Insert into section8_draft.md
Append the row to the FSS table in Section 8.4 (preserve existing rows). Format must match existing rows exactly.

### Task D — Verification at T=10⁵
The N=1000, λ=1.5, T=10⁵ verification (showing the 4.15× peak collapses to 1.18×) is already in `ipr_lambda1p5_N1000_T1e5.csv`. Do **NOT** re-run it. Instead, in Section 8.4, add a paragraph stating that the N=1000 ratio at T=10⁴ is transient and quoting the T=10⁵ collapse value.

### Task E — Run T=10⁵ at N=2000, λ=1.5 only
This is the missing piece. The N=1000 verification exists; the N=2000 one does not. Run:
```python
N_SITES = 2000
T_END = 100000.0
LAMBDAS = [1.5]   # only λ=1.5
CHAINS = ["fibonacci", "tribonacci"]
RTOL = 1e-9
ATOL = 1e-11
```
Output: `data/ipr_lambda1p5_N2000_T1e5.csv`. Wallclock: ~30–60 min per chain.

In Section 8.4 add the N=2000 ratio at T=10⁵ alongside the N=1000 collapse value. State whether the differential is monotonic across N at T=10⁵ for λ=1.5.

## Required output (verbatim paste in PR description)

### [1] Updated FSS table (full table including λ=1.5 row)
```
λ      N=500    N=1000   N=2000
0.5    ...      ...      ...
1.0    ...      ...      ...
1.5    ...      ...      ...   ← new row at T=10⁴
2.0    ...      ...      ...
...
```

### [2] T=10⁵ comparison
```
λ=1.5, T=10⁵:
  N=1000: ratio = 1.18 (from existing CSV)
  N=2000: ratio = ____ (from new run)
```

### [3] Section 8.4 paragraph (verbatim copy of inserted text)

### [4] Norm conservation across all (N, λ=1.5, T=10⁵) runs
Max leak: ____. Flag if > 5×10⁻⁵.

## Definition of done
- λ=1.5 row in the FSS table at T=10⁴
- N=2000, T=10⁵, λ=1.5 CSV committed
- Section 8.4 paragraph added explaining the T=10⁴ → T=10⁵ collapse story
- PR green

## Anti-hallucination guard
Do **NOT** re-run the N=1000 T=10⁵ verification — that data exists. Do **NOT** invent ratios. If T=10⁵ N=2000 run cannot complete in budget, commit partial data and clearly mark the N=2000 entry as "in progress" rather than fabricating a number.
