#!/usr/bin/env python3
"""
nbonacci_criticality.py
=======================
Criticality (k-effective) of a 1D slab with diffusion coefficients and
cross-sections modulated by n-bonacci substitution sequences.

Model
-----
One-group diffusion equation on a uniform mesh of N sites:

    -d/dx [D_i d phi/dx] + Sigma_r,i phi = (1/k) nu*Sigma_f,i phi

with vacuum boundary conditions (phi=0 at both ends).

Discretised by standard finite differences:

    L phi = (1/k) F phi

where L is the loss (diffusion + removal) matrix and F is the fission matrix.
k_eff is the dominant eigenvalue of L^{-1} F.

Parameter map (dimensionless)
------------------------------
Symbol A (fissile):    D_A = 1.0,  Sigma_r_A = 0.5,  nu_Sigma_f_A = lambda
Symbol B (moderator):  D_B = 1.5,  Sigma_r_B = 1.2,  nu_Sigma_f_B = 0
Symbol C (absorber,    D_C = 1.2,  Sigma_r_C = 2.0,  nu_Sigma_f_C = 0
          tribonacci
          only):

Author
------
    Pablo Nogueira Grossi  |  ORCID: 0009-0000-6496-2186
    G6 LLC, Newark NJ  |  pablogrossi@hotmail.com

License: MIT
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags, lil_matrix
from scipy.sparse.linalg import eigs
from scipy.linalg import eig


# ---------------------------------------------------------------------------
# 1. Substitution words
# ---------------------------------------------------------------------------

def fibonacci_word(n_gen: int) -> list[int]:
    """Fibonacci substitution: A->AB, B->A. Returns symbol list (0=A,1=B)."""
    word = [0]
    rules = {0: [0, 1], 1: [0]}
    for _ in range(n_gen):
        word = [s for c in word for s in rules[c]]
    return word


def tribonacci_word(n_gen: int) -> list[int]:
    """Tribonacci substitution: A->AB, B->AC, C->A. Returns symbol list."""
    word = [0]
    rules = {0: [0, 1], 1: [0, 2], 2: [0]}
    for _ in range(n_gen):
        word = [s for c in word for s in rules[c]]
    return word


# ---------------------------------------------------------------------------
# 2. Parameter map
# ---------------------------------------------------------------------------

# Each symbol maps to (D, Sigma_r, nu_Sigma_f)
PARAMS = {
    0: (1.0, 0.5, None),   # A: fissile — nu_Sigma_f = lambda (free parameter)
    1: (1.5, 1.2, 0.0),    # B: moderator
    2: (1.2, 2.0, 0.0),    # C: absorber (tribonacci only)
}


def site_params(word: list[int], lam: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Build site-wise parameter arrays from a substitution word.

    Returns D, Sigma_r, nu_Sigma_f arrays of length len(word).
    """
    N = len(word)
    D = np.empty(N)
    Sr = np.empty(N)
    Sf = np.empty(N)
    for i, s in enumerate(word):
        d, sr, sf = PARAMS[s]
        D[i] = d
        Sr[i] = sr
        Sf[i] = sf if sf is not None else lam
    return D, Sr, Sf


# ---------------------------------------------------------------------------
# 3. Diffusion matrix assembly (finite differences, uniform mesh h=1)
# ---------------------------------------------------------------------------

def build_matrices(
    D: np.ndarray, Sr: np.ndarray, Sf: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Assemble loss matrix L and fission matrix F for the 1D diffusion equation.

    Finite difference with mesh spacing h=1 and vacuum BCs (phi_0 = phi_{N+1} = 0).

    L_{ii}   = D_{i-1/2} + D_{i+1/2} + Sigma_r,i
    L_{i,i+1} = -D_{i+1/2}
    L_{i,i-1} = -D_{i-1/2}

    where D_{i+1/2} = 2 D_i D_{i+1} / (D_i + D_{i+1})  (harmonic mean).

    F_{ii}   = nu_Sigma_f,i
    """
    N = len(D)

    # Harmonic-mean interface diffusion coefficients
    D_half = np.zeros(N + 1)          # D_{i+1/2} for i = 0..N-1, plus BCs
    for i in range(N - 1):
        D_half[i + 1] = 2 * D[i] * D[i + 1] / (D[i] + D[i + 1])
    D_half[0] = D[0]                  # left vacuum BC: extrapolation ~ D_0
    D_half[N] = D[N - 1]             # right vacuum BC

    # Loss matrix (dense for small N; sparse wrapper handles large N)
    L = np.zeros((N, N))
    for i in range(N):
        L[i, i] = D_half[i] + D_half[i + 1] + Sr[i]
        if i > 0:
            L[i, i - 1] = -D_half[i]
        if i < N - 1:
            L[i, i + 1] = -D_half[i + 1]

    # Fission matrix (diagonal)
    F = np.diag(Sf)

    return L, F


def k_eff(L: np.ndarray, F: np.ndarray) -> tuple[float, np.ndarray]:
    """
    Compute k_eff as the dominant eigenvalue of L^{-1} F.

    Uses scipy.linalg.eig on the generalised problem F v = k L v.
    Returns (k_eff, fundamental flux mode).
    """
    vals, vecs = eig(F, L)
    vals = vals.real
    # Dominant positive eigenvalue
    idx = np.argmax(vals)
    k = float(vals[idx])
    phi = vecs[:, idx].real
    phi = phi / np.max(np.abs(phi))   # normalise to peak = 1
    return k, phi


# ---------------------------------------------------------------------------
# 4. Sweeps
# ---------------------------------------------------------------------------

def sweep_lambda(
    word_fn,
    n_gen: int,
    lam_values: np.ndarray,
) -> np.ndarray:
    """Compute k_eff vs lambda for a fixed substitution generation."""
    word = word_fn(n_gen)
    k_arr = np.empty(len(lam_values))
    for j, lam in enumerate(lam_values):
        D, Sr, Sf = site_params(word, lam)
        L, F = build_matrices(D, Sr, Sf)
        k_arr[j], _ = k_eff(L, F)
    return k_arr


def sweep_generation(
    word_fn,
    generations: list[int],
    lam: float,
) -> tuple[list[int], np.ndarray, list[np.ndarray]]:
    """Compute k_eff vs substitution generation at fixed lambda."""
    k_arr = np.empty(len(generations))
    fluxes = []
    lengths = []
    for j, g in enumerate(generations):
        word = word_fn(g)
        lengths.append(len(word))
        D, Sr, Sf = site_params(word, lam)
        L, F = build_matrices(D, Sr, Sf)
        k_arr[j], phi = k_eff(L, F)
        fluxes.append(phi)
    return lengths, k_arr, fluxes


# ---------------------------------------------------------------------------
# 5. Plots
# ---------------------------------------------------------------------------

def plot_all(out_prefix: str = "fig") -> None:
    lam_vals = np.linspace(0.5, 3.0, 80)
    generations = [3, 4, 5, 6, 7, 8]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # --- Panel 1: k_eff vs lambda, Fibonacci generations ---
    ax = axes[0]
    for g in [4, 6, 8]:
        k = sweep_lambda(fibonacci_word, g, lam_vals)
        word = fibonacci_word(g)
        ax.plot(lam_vals, k, label=f"gen {g}  (N={len(word)})")
    ax.axhline(1.0, color="k", lw=0.8, ls="--", label="k=1")
    ax.set_xlabel(r"$\lambda$ (fission strength)")
    ax.set_ylabel(r"$k_{\rm eff}$")
    ax.set_title("Fibonacci: $k_{\\rm eff}$ vs $\\lambda$")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # --- Panel 2: k_eff vs generation at fixed lambda ---
    ax = axes[1]
    # Find lambda that gives k~1 for Fibonacci gen 6
    lam_crit = float(lam_vals[np.argmin(np.abs(
        sweep_lambda(fibonacci_word, 6, lam_vals) - 1.0
    ))])

    for chain_name, word_fn in [("Fibonacci", fibonacci_word),
                                  ("Tribonacci", tribonacci_word)]:
        lengths, k_arr, _ = sweep_generation(word_fn, generations, lam_crit)
        ax.plot(generations, k_arr, "o-", label=chain_name)

    ax.axhline(1.0, color="k", lw=0.8, ls="--")
    ax.set_xlabel("Substitution generation")
    ax.set_ylabel(r"$k_{\rm eff}$")
    ax.set_title(f"$k_{{\\rm eff}}$ vs generation ($\\lambda={lam_crit:.2f}$)")
    ax.legend()
    ax.grid(alpha=0.3)

    # --- Panel 3: Flux profiles for Fibonacci at two generations ---
    ax = axes[2]
    for g in [5, 8]:
        word = fibonacci_word(g)
        D, Sr, Sf = site_params(word, lam_crit)
        L, F = build_matrices(D, Sr, Sf)
        _, phi = k_eff(L, F)
        x = np.arange(len(phi))
        ax.plot(x / len(phi), phi, lw=0.8, label=f"gen {g}  (N={len(phi)})")
    ax.set_xlabel("Normalised position $x/L$")
    ax.set_ylabel(r"$\phi$ (normalised flux)")
    ax.set_title(f"Fundamental flux mode ($\\lambda={lam_crit:.2f}$)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{out_prefix}_criticality.png", dpi=150)
    plt.close()
    print(f"Saved {out_prefix}_criticality.png")

    # --- Panel 4: convergence of k_eff to limiting value ---
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    for chain_name, word_fn in [("Fibonacci", fibonacci_word),
                                  ("Tribonacci", tribonacci_word)]:
        lengths, k_arr, _ = sweep_generation(word_fn, generations, lam_crit)
        delta_k = np.abs(k_arr - k_arr[-1])
        # avoid log(0)
        mask = delta_k > 1e-14
        ax2.semilogy(
            np.array(generations)[mask], delta_k[mask], "o-", label=chain_name
        )
    ax2.set_xlabel("Substitution generation")
    ax2.set_ylabel(r"$|k_{\rm eff}(g) - k_{\rm eff}(g_{\rm max})|$")
    ax2.set_title("Convergence of $k_{\\rm eff}$ with substitution generation")
    ax2.legend()
    ax2.grid(alpha=0.3, which="both")
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_convergence.png", dpi=150)
    plt.close()
    print(f"Saved {out_prefix}_convergence.png")


# ---------------------------------------------------------------------------
# 6. Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Running n-bonacci criticality sweep...")
    plot_all(out_prefix="/mnt/user-data/outputs/fig")

    # Print a summary table
    lam_vals = np.linspace(0.5, 3.0, 80)
    lam_crit = float(lam_vals[np.argmin(np.abs(
        sweep_lambda(fibonacci_word, 6, lam_vals) - 1.0
    ))])
    print(f"\nCritical lambda (Fibonacci gen 6): {lam_crit:.3f}")
    print(f"\n{'Gen':>4} {'N_Fib':>8} {'k_Fib':>10} {'N_Tribo':>8} {'k_Tribo':>10}")
    print("-" * 46)
    for g in range(3, 9):
        wf = fibonacci_word(g);  Df,Srf,Sff = site_params(wf, lam_crit)
        kf, _ = k_eff(*build_matrices(Df,Srf,Sff))
        wt = tribonacci_word(g); Dt,Srt,Sft = site_params(wt, lam_crit)
        kt, _ = k_eff(*build_matrices(Dt,Srt,Sft))
        print(f"{g:>4} {len(wf):>8} {kf:>10.6f} {len(wt):>8} {kt:>10.6f}")
