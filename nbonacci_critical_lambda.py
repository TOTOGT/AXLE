#!/usr/bin/env python3
"""
nbonacci_critical_lambda.py
===========================
Finds the critical fission strength lambda_c(n) for n-bonacci substitution
chains (n=2..5), and tests whether lambda_c scales with the n-bonacci
constant rho_n (dominant root of x^n = x^(n-1) + ... + 1).

Author: Pablo Nogueira Grossi | G6 LLC | 2026 | MIT
"""

from __future__ import annotations
import numpy as np
from scipy.linalg import eig
from scipy.optimize import brentq

# ---------------------------------------------------------------------------
# 1. n-bonacci substitution words  (general, up to n=5)
# ---------------------------------------------------------------------------

def nbonacci_word(n: int, n_gen: int) -> list[int]:
    """
    General n-bonacci substitution:
        symbol 0 (A) -> [0, 1]
        symbol k (1..n-2) -> [0, k+1]
        symbol n-1 -> [0]
    Symbols: 0=fissile(A), 1..n-1 = absorbers(B,C,D,E)
    """
    rules = {}
    for k in range(n):
        if k == 0:
            rules[k] = [0, 1] if n > 1 else [0]
        elif k < n - 1:
            rules[k] = [0, k + 1]
        else:
            rules[k] = [0]
    word = [0]
    for _ in range(n_gen):
        word = [s for c in word for s in rules[c]]
    return word

# ---------------------------------------------------------------------------
# 2. Parameter map
# ---------------------------------------------------------------------------

# Symbol 0 = fissile: D=1.0, Sr=0.5, Sf=lambda (free)
# Symbol k>0 = absorber: D=1.0, Sr=2.0, Sf=0
D_FISSILE  = 1.0;  SR_FISSILE = 0.5
D_ABSORBER = 1.0;  SR_ABSORBER = 2.0

def site_params(word: list[int], lam: float):
    N = len(word)
    D  = np.where(np.array(word) == 0, D_FISSILE,  D_ABSORBER).astype(float)
    Sr = np.where(np.array(word) == 0, SR_FISSILE, SR_ABSORBER).astype(float)
    Sf = np.where(np.array(word) == 0, lam, 0.0)
    return D, Sr, Sf

# ---------------------------------------------------------------------------
# 3. Matrix assembly + k_eff
# ---------------------------------------------------------------------------

def build_and_solve(word: list[int], lam: float) -> float:
    D, Sr, Sf = site_params(word, lam)
    N = len(D)
    # harmonic-mean interface diffusion
    D_half = np.zeros(N + 1)
    D_half[0] = D[0]
    D_half[N] = D[N-1]
    for i in range(N-1):
        D_half[i+1] = 2*D[i]*D[i+1] / (D[i]+D[i+1])
    # loss matrix
    L = np.zeros((N, N))
    for i in range(N):
        L[i,i] = D_half[i] + D_half[i+1] + Sr[i]
        if i > 0:   L[i,i-1] = -D_half[i]
        if i < N-1: L[i,i+1] = -D_half[i+1]
    F = np.diag(Sf)
    vals, _ = eig(F, L)
    return float(np.max(vals.real))

# ---------------------------------------------------------------------------
# 4. n-bonacci constants (dominant root of x^n = x^(n-1)+...+1)
# ---------------------------------------------------------------------------

def nbonacci_constant(n: int) -> float:
    """Dominant positive real root of x^n - x^(n-1) - ... - 1 = 0."""
    coeffs = [1] + [-1]*n   # x^n - x^(n-1) - ... - x^0
    roots = np.roots(coeffs)
    real_positive = roots[np.isreal(roots) & (roots.real > 1)].real
    return float(np.max(real_positive))

# ---------------------------------------------------------------------------
# 5. Main sweep
# ---------------------------------------------------------------------------

def find_lambda_c(n: int, n_gen: int, lam_lo=0.3, lam_hi=5.0) -> float:
    word = nbonacci_word(n, n_gen)
    f = lambda lam: build_and_solve(word, lam) - 1.0
    if f(lam_lo) > 0:
        return lam_lo   # already supercritical at lower bound
    if f(lam_hi) < 0:
        return np.nan   # never reaches criticality
    return brentq(f, lam_lo, lam_hi, xtol=1e-6)

if __name__ == "__main__":
    # Generation to use per n (keep N ~ 100-200 sites)
    gen_map = {2: 9, 3: 7, 4: 6, 5: 5}

    print(f"\n{'n':>3}  {'gen':>4}  {'N_sites':>8}  {'rho_n':>8}  "
          f"{'lambda_c':>10}  {'lambda_c/rho_n':>14}  {'lambda_c-rho_n':>14}")
    print("-" * 70)

    results = {}
    for n in range(2, 6):
        g = gen_map[n]
        word = nbonacci_word(n, g)
        N = len(word)
        rho = nbonacci_constant(n)
        lc  = find_lambda_c(n, g)
        ratio = lc / rho if not np.isnan(lc) else np.nan
        diff  = lc - rho if not np.isnan(lc) else np.nan
        results[n] = (g, N, rho, lc, ratio, diff)
        print(f"{n:>3}  {g:>4}  {N:>8}  {rho:>8.5f}  "
              f"{lc:>10.5f}  {ratio:>14.5f}  {diff:>14.5f}")

    # --- convergence check: lambda_c vs generation for n=2,3 ---
    print("\nConvergence of lambda_c with generation:")
    print(f"{'n':>3}  {'gen':>4}  {'N':>7}  {'lambda_c':>10}")
    print("-" * 30)
    for n in [2, 3]:
        for g in range(4, gen_map[n]+2):
            try:
                word = nbonacci_word(n, g)
                lc = find_lambda_c(n, g)
                print(f"{n:>3}  {g:>4}  {len(word):>7}  {lc:>10.5f}")
            except Exception as e:
                print(f"{n:>3}  {g:>4}  error: {e}")

def plot_results(results, gen_map):
    import matplotlib.pyplot as plt

    ns = list(results.keys())
    rhos = [results[n][2] for n in ns]
    lcs  = [results[n][3] for n in ns]
    ratios = [results[n][4] for n in ns]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Panel 1: lambda_c and rho_n vs n
    ax = axes[0]
    ax.plot(ns, lcs,  "o-", label=r"$\lambda_c(n)$", color="steelblue")
    ax.plot(ns, rhos, "s--", label=r"$\rho_n$ (n-bonacci const)", color="tomato")
    ax.set_xlabel("n (substitution order)")
    ax.set_ylabel("Value")
    ax.set_title(r"$\lambda_c(n)$ vs n-bonacci constant $\rho_n$")
    ax.legend(); ax.grid(alpha=0.3)
    ax.set_xticks(ns)

    # Panel 2: ratio lambda_c / rho_n
    ax = axes[1]
    ax.plot(ns, ratios, "o-", color="purple")
    ax.axhline(np.mean(ratios), ls="--", color="gray",
               label=f"mean = {np.mean(ratios):.4f}")
    ax.set_xlabel("n")
    ax.set_ylabel(r"$\lambda_c / \rho_n$")
    ax.set_title(r"Ratio $\lambda_c(n) / \rho_n$")
    ax.legend(); ax.grid(alpha=0.3)
    ax.set_xticks(ns)

    # Panel 3: convergence of lambda_c with generation for n=2,3
    ax = axes[2]
    for n, color in [(2, "steelblue"), (3, "tomato")]:
        gens, lcs_g = [], []
        for g in range(4, gen_map[n]+2):
            try:
                word = nbonacci_word(n, g)
                lc = find_lambda_c(n, g)
                gens.append(len(word))
                lcs_g.append(lc)
            except: pass
        ax.plot(gens, lcs_g, "o-", color=color, label=f"n={n}")
        ax.axhline(lcs_g[-1], ls="--", color=color, alpha=0.4)
    ax.set_xlabel("Chain length N")
    ax.set_ylabel(r"$\lambda_c$")
    ax.set_title(r"Convergence of $\lambda_c$ with chain length")
    ax.legend(); ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("/mnt/user-data/outputs/fig_lambda_c.png", dpi=150)
    plt.close()
    print("Saved fig_lambda_c.png")

import numpy as np
plot_results(results, gen_map)
