# Copilot Brief — Brief 5
# Tetrabonacci extension: from quasiperiodic to random

## Goal
Extend the differential-nonlinear-robustness analysis to tetrabonacci substitution chains. The intent is to test whether the fibonacci → tribonacci pattern (more letters → more localized → more nonlinear-robust) continues, and to provide the next data point along the n-bonacci sequence that asymptotes to a random sequence as n → ∞.

This is scoped as a self-contained piece of work that produces enough data to anchor a follow-up paper, not to fold into the current Zenodo paper revision. The current paper closes with fib + trib results; this brief opens the next.

## Repo and branch
- Repo: `grossi-ops/Atratores`
- Branch: `agent/tetrabonacci-extension`
- Open as draft PR titled: "Tetrabonacci substitution chain: T=50, T=10⁴ FSS, and D₂"

## Background — tetrabonacci substitution
Substitution rule: `A → AB`, `B → AC`, `C → AD`, `D → A`, starting from `A`.

Letter-count recurrence (apply substitution to letter counts a, b, c, d):
```
a' = a + b + c + d
b' = a
c' = b
d' = c
length' = a' + b' + c' + d' = 2a + 2b + 2c + d
```

Natural lengths follow the tetrabonacci numbers (OEIS A000078):
```
iter:   0  1  2  3  4   5   6   7    8    9    10   11    12    13
length: 1  2  4  8  15  29  56  108  208  401  773  1490  2872  5536
```

Perron-Frobenius eigenvalue (tetrabonacci constant): largest root of x⁴ − x³ − x² − x − 1 = 0, ≈ 1.92756.

Natural hopping values (geometric series, matching the convention in `dnls_nbonacci.py`):
```
t_A = 1.0
t_B = 0.5
t_C = 0.25
t_D = 0.125
```

## Tasks

### Task A — Add `tetrabonacci_word` to dnls_nbonacci.py
Implement substitution iteratively (no recursion, no nested replace chaining):
```python
def tetrabonacci_word(N):
    """Return the tetrabonacci word truncated to N sites."""
    s = "A"
    while len(s) < N:
        s = "".join({"A": "AB", "B": "AC", "C": "AD", "D": "A"}[ch] for ch in s)
    return s[:N]

def tetrabonacci_word_natural(n_iterations):
    """Return the n-th iteration of the tetrabonacci substitution starting from 'A'."""
    s = "A"
    for _ in range(n_iterations):
        s = "".join({"A": "AB", "B": "AC", "C": "AD", "D": "A"}[ch] for ch in s)
    return s
```

Add a `build_hamiltonian_tetra` (or extend the existing builder) that maps four letters to four hopping values. Match the existing code style.

### Task B — Verify substitution against OEIS A000078
Verify lengths at natural iterations match {1, 2, 4, 8, 15, 29, 56, 108, 208, 401, 773, 1490, 2872, 5536}. Print verbatim output:
```
tetrabonacci_word_natural(0)  length = 1     (expected 1)    OK/FAIL
tetrabonacci_word_natural(1)  length = 2     (expected 2)    OK/FAIL
...
tetrabonacci_word_natural(13) length = 5536  (expected 5536) OK/FAIL
```
Halt the brief and request human review if any length disagrees with the table.

### Task C — Experiment 1: T=50 reproduction at N=500
Run T=50 evolution at N=500 across the standard λ-grid:
```python
LAMBDAS = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]
```
Use the same integrator and tolerances as the original `dnls_nbonacci.py` paper run (RK45, RTOL=1e-6, T_END=50). Output CSV: `data/tetrabonacci_T50_N500.csv` with columns `time, lambda, chain, IPR, norm`.

Required table in the PR description:
```
λ      fib retention   trib retention   tetra retention
0.0    ...             ...              ...
0.5    ...             ...              ...
1.0    ...             ...              ...
...
10.0   ...             ...              ...
```
"Retention" = IPR(T=50) / IPR(t=0). The fib and trib values are already known from the paper; quote them alongside for direct comparison. Hypothesis to test: does tetra retention monotonically beat trib retention at every λ, or only at some?

### Task D — Experiment 2: T=10⁴ FSS at λ=1.5
Run tetrabonacci at λ=1.5, T=10⁴, N ∈ {500, 1000, 2000} with DOP853, RTOL=1e-9, ATOL=1e-11.
Output CSV: `data/tetrabonacci_lambda1p5_T1e4.csv`.

Required table in the PR description (extending the existing FSS table):
```
λ=1.5, T=10⁴:
                N=500    N=1000   N=2000
fib IPR         ...      ...      ...
trib IPR        ...      ...      ...
tetra IPR       ...      ...      ...
fib/trib        ...      ...      ...
trib/tetra      ...      ...      ...
fib/tetra       ...      ...      ...
```
Hypothesis: tetra IPR > trib IPR > fib IPR at all N (tetra most retained), and the differential grows with N as before.

### Task E — Experiment 3: D₂_tetra at natural lengths, λ=0
Run mid-gap eigenstate IPR at λ=0 across natural tetrabonacci lengths N ∈ {208, 401, 773, 1490, 2872}.
Output CSV: `data/tetrabonacci_d2_natural_lengths.csv`.

Apply the same spatial-spread filter from Brief 3 to exclude any compact zero-modes. Report whether such modes are encountered and how many were filtered.

Required output:
```
chain          N      IPR      log10(N)   log10(IPR)
tetrabonacci   208    ...      ...        ...
tetrabonacci   401    ...      ...        ...
...
tetrabonacci   2872   ...      ...        ...

D₂_tetra fit:  D₂ = ____  std_err = ____  R² = ____  n_pts = ____
Comparison:    D₂_fib = 0.65, D₂_trib = 0.28, D₂_tetra = ____
```
Hypothesis: D₂_tetra < D₂_trib < D₂_fib (more multifractal/localized as n grows). If the trend reverses or saturates, that's a discovery.

## Required output (verbatim paste in PR description)

### [1] OEIS A000078 verification (Task B output)

### [2] T=50 retention table across fib, trib, tetra (Task C)

### [3] T=10⁴ FSS table extended with tetra row (Task D)

### [4] Natural-length IPR(N) and D₂ fit (Task E)

### [5] Norm conservation across all runs
Max leak in T=50 runs: ____. Max leak in T=10⁴ runs: ____. Flags raised: ____.

### [6] Three-figure deliverable
- `figures/tetra_T50_retention.png`: bar chart of retention at T=50 for fib/trib/tetra across all λ
- `figures/tetra_FSS_lambda1p5.png`: log-log IPR vs N at T=10⁴ for all three chains
- `figures/tetra_D2_natural.png`: log-log IPR vs N at λ=0 for all three chains, with D₂ fit lines

### [7] One-paragraph summary in PR description
Plain-language summary of: does the trend continue, does it saturate, or does something qualitatively new happen at tetrabonacci?

## Definition of done
- All four CSVs committed under `data/`
- All three figures committed under `figures/`
- All seven verbatim sections in PR description
- PR green
- The summary paragraph in [7] is honest about whether the trend held; do NOT force a conclusion that contradicts the data

## Anti-hallucination guard
The substitution-rule expansion is the highest-risk step. Verify lengths against OEIS A000078 **before** running any DNLS computation — if lengths are wrong, every downstream number is wrong. The dict-based substitution above is the safe pattern; do NOT use chained `.replace()` calls (they are non-commutative and will corrupt the word). The geometric hopping `t_A=1, t_B=0.5, t_C=0.25, t_D=0.125` is a convention choice — flag it explicitly in the docstring and PR description so a referee knows it's not the only possible parameterization.

## Out of scope (do NOT do as part of this PR)
- T=10⁵ runs (only T=50 and T=10⁴)
- α-fits (no late-time spreading-exponent analysis yet)
- Pentabonacci / hexabonacci / further extensions
- Edits to the current `section8_draft.md` (this is for the follow-up paper, not the current one)
