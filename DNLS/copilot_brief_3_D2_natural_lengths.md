# Copilot Brief — Brief 3 of 3
# Resolve the D₂_trib anomaly using natural Rauzy substitution lengths

## Goal
Close PRB referee question (2): "Is the trib D₂ anomaly at N=1000 a finite-size effect of the non-natural chain length, or something physical?"

The current D₂_trib estimate (≈0.37) is a fit through non-monotone IPR(N) data: 0.0969 → 0.0820 → 0.0410 → 0.0484 (N=200, 500, 1000, 2000). The N=1000 → N=2000 reversal is the smoking gun. Hypothesis: arbitrary truncation of the tribonacci word at N=1000 destroys the self-similar boundary that the Rauzy fixed-point chain lengths preserve. Test: re-compute D₂_trib only at natural Rauzy lengths.

## Repo and branch
- Repo: `grossi-ops/Atratores`
- Branch: `agent/d2-rauzy-lengths`
- Open as draft PR titled: "D₂_trib at natural Rauzy substitution lengths"

## Background — Rauzy lengths
The tribonacci word satisfies length recurrence T_n = T_{n-1} + T_{n-2} + T_{n-3} with T_1=1, T_2=2, T_3=4. The natural lengths grow as the Tribonacci numbers:
```
T_8  = 81
T_9  = 149
T_10 = 274
T_11 = 504
T_12 = 927
T_13 = 1705
T_14 = 3136
```
At each T_n, the chain is the n-th iteration of A → AB, B → AC, C → A starting from A. This preserves the self-similar boundary structure.

For comparison, **also** run Fibonacci at natural Fibonacci lengths F_n: 89, 144, 233, 377, 610, 987, 1597, 2584. F_n is what the existing chain at N=500 already approximates (between F_14=377 and F_15=610), but doing the matched comparison cleans up Fig A.

## Repo and branch
Same as above.

## Tasks

### Task A — Add a `--natural-lengths` flag to the chain builder
In whatever module currently houses `tribonacci_word(N)` (likely `dnls_nbonacci.py` or `dnls_long_time.py`), add:
```python
def tribonacci_word_natural(n_iterations):
    """Return the n-th Rauzy iteration of A → AB, B → AC, C → A starting at 'A'."""
    s = "A"
    for _ in range(n_iterations):
        s = s.replace("A", "1").replace("B", "2").replace("C", "3")
        s = s.replace("1", "AB").replace("2", "AC").replace("3", "A")
    return s

def fibonacci_word_natural(n_iterations):
    """Return the n-th iteration of A → AB, B → A starting at 'A'."""
    ...
```

The `replace` chaining is wrong as written — it will recurse. Use a proper non-recursive substitution (e.g., build via list comprehension over the previous string). Test that `tribonacci_word_natural(3)` has length 4, `(4)` has length 7, `(5)` has length 13, `(6)` has length 24. Match against OEIS A000073.

### Task B — Compute IPR at λ=0 across natural lengths
For each (n, chain) build the Hamiltonian, find the mid-gap eigenstate, compute IPR. Use:
```python
TRIB_LENGTHS = [274, 504, 927, 1705, 3136]   # n=10..14
FIB_LENGTHS  = [233, 377, 610, 987, 1597, 2584]  # F_13..F_18
```
N=3136 may be slow; if it does not finish in 30 min, drop it and report.

Output CSV: `data/d2_natural_lengths.csv` with columns `N, chain, IPR, n_iterations`.

### Task C — Fit D₂
Linear regression of `log(IPR)` on `log(N)` for each chain. Quote slope, std err, R², and number of points. Compare to the existing arbitrary-length D₂ values.

### Task D — Update Fig A and Section 8.2
- Regenerate Fig A from `data/d2_natural_lengths.csv` with two panels (or two color groups): "natural lengths" overlay vs the existing arbitrary-length scatter
- In Section 8.2, replace the D₂_trib value with the natural-length fit and add a sentence about the boundary-truncation hypothesis

## Required output (verbatim paste)

### [1] Verification of natural-length builder
```
tribonacci_word_natural(3)  length = 4   (expected 4)
tribonacci_word_natural(4)  length = 7   (expected 7)
tribonacci_word_natural(5)  length = 13  (expected 13)
tribonacci_word_natural(6)  length = 24  (expected 24)
tribonacci_word_natural(10) length = 274 (expected 274)
```
plus the same for Fibonacci.

### [2] IPR table
```
chain         N      IPR        log10(N)   log10(IPR)
fibonacci     233    ...        ...        ...
fibonacci     377    ...        ...        ...
...
tribonacci    274    ...        ...        ...
tribonacci    504    ...        ...        ...
...
```

### [3] D₂ fit
```
chain        D₂        std_err     R²       n_points
fibonacci    ...       ...         ...      ...
tribonacci   ...       ...         ...      ...
```

### [4] Comparison to arbitrary-length values
```
                arbitrary-length D₂   natural-length D₂
fibonacci       0.578                 ...
tribonacci      0.37 (anomalous)      ...
```

### [5] Updated Section 8.2 paragraph
Verbatim copy of the inserted/replaced text.

### [6] Regenerated Fig A
Path: `figures/d2_natural_lengths.png`. Show both arbitrary-length scatter (faded) and natural-length fit (solid) on one plot.

## Definition of done
- New CSV at `data/d2_natural_lengths.csv`
- Updated Fig A
- Section 8.2 reflects the natural-length D₂_trib
- PR green

## Anti-hallucination guard
The substitution rule expansion is the most error-prone step. Verify lengths against OEIS A000073 (tribonacci) and A000045 (Fibonacci) **before** running any DNLS computation. If lengths are wrong, every downstream number is wrong.
