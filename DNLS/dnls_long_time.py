#!/usr/bin/env python3
"""
dnls_long_time.py
=================
Long-time DNLS evolution on Fibonacci and Tribonacci substitution chains.

Pilot extension of `dnls_nbonacci.py` addressing open question 1 of
Section 7 of the companion paper:

  "Differential Nonlinear Robustness of Critical States in Fibonacci and
   Tribonacci Substitution Chains"
  Pablo Nogueira Grossi, G6 LLC (2026)
  DOI (this paper): 10.5281/zenodo.20026943

Changes vs. dnls_nbonacci.py
----------------------------
1. Integrator switched from RK45 to DOP853 (8th-order Dormand-Prince).
   At T ~ 10^3 the step count is ~10x lower than RK45 for the same
   accuracy, with much less drift.
2. Logarithmically spaced checkpoints (t_eval) so we capture the spreading
   dynamics, not just the endpoint. This is what you need to fit the
   spreading exponent alpha (open question 3) once the time-series is in
   hand.
3. Norm monitoring at every checkpoint. Flags any chain/lambda whose
   norm leaks more than NORM_TOL.
4. Outputs a tidy long-format CSV (`ipr_vs_time.csv`) with
   columns: time, lambda, chain, IPR, norm.

Pilot scope
-----------
T = 1000 (10^3). Validates the integrator and output format before
committing to the full T = 10^5 run flagged in the paper. Runtime
estimate on a single core: ~1-3 min per (chain, lambda) pair, so the
full sweep should finish in 20-60 min.

Author
------
    Pablo Nogueira Grossi  |  ORCID: 0009-0000-6496-2186
    G6 LLC, Newark NJ  |  pablogrossi@hotmail.com
    GitHub: https://github.com/TOTOGT/AXLE

License: MIT
"""

from __future__ import annotations

import argparse
import csv
import sys
import time as _time
from typing import Callable

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh


# ---------------------------------------------------------------------------
# 1. Substitution words and Hamiltonian (verbatim from dnls_nbonacci.py)
# ---------------------------------------------------------------------------

def fibonacci_word(length: int) -> list[int]:
    word = [0]
    rules = {0: [0, 1], 1: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]


def tribonacci_word(length: int) -> list[int]:
    word = [0]
    rules = {0: [0, 1], 1: [0, 2], 2: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]


def build_hamiltonian(
    word: list[int], N: int, t_mod: float = 0.5
) -> tuple[np.ndarray, np.ndarray]:
    hop_map = {0: 1.0, 1: t_mod, 2: t_mod**2}
    hoppings = np.array([hop_map.get(word[j], t_mod) for j in range(N - 1)])
    H = np.zeros((N, N))
    for j in range(N - 1):
        H[j, j + 1] = hoppings[j]
        H[j + 1, j] = hoppings[j]
    return H, hoppings


def mid_gap_state(H: np.ndarray) -> tuple[np.ndarray, float]:
    vals, vecs = eigh(H)
    idx = np.argmin(np.abs(vals))
    return vecs[:, idx], float(vals[idx])


def ipr(psi: np.ndarray) -> float:
    norm2 = float(np.sum(np.abs(psi) ** 2))
    return float(np.sum(np.abs(psi) ** 4)) / norm2 ** 2


# ---------------------------------------------------------------------------
# 2. DNLS RHS (verbatim) and long-time evolver (DOP853, t_eval, norm check)
# ---------------------------------------------------------------------------

def dnls_rhs(
    t: float,
    state: np.ndarray,
    lam: float,
    hoppings: np.ndarray,
) -> np.ndarray:
    """
    i d psi_j / dt = -sum_{j'} H_{jj'} psi_{j'} + lam |psi_j|^2 psi_j

    Real-valued formulation with state = [Re(psi); Im(psi)] of length 2N.
    Splitting psi = x + i*y gives:

        dx/dt = -H @ y + lam * |psi|^2 * y
        dy/dt =  H @ x - lam * |psi|^2 * x

    where |psi|^2 = x^2 + y^2 element-wise.  The tridiagonal matrix-vector
    products are evaluated with O(N) numpy slice operations (no Python loop).
    """
    N = len(state) >> 1
    x = state[:N]
    y = state[N:]

    # Tridiagonal H @ x  (hoppings are the N-1 off-diagonal entries)
    Hx = np.zeros(N)
    Hx[:-1] += hoppings * x[1:]
    Hx[1:] += hoppings * x[:-1]

    # Tridiagonal H @ y
    Hy = np.zeros(N)
    Hy[:-1] += hoppings * y[1:]
    Hy[1:] += hoppings * y[:-1]

    nl = x * x + y * y          # |psi_j|^2, shape (N,)
    dxdt = -Hy + lam * nl * y
    dydt = Hx - lam * nl * x
    return np.concatenate([dxdt, dydt])


def evolve_dnls(
    psi0: np.ndarray,
    lam: float,
    hoppings: np.ndarray,
    t_end: float = 1000.0,
    n_checkpoints: int = 200,
    norm_tol: float = 1e-5,
    rtol: float = 1e-8,
    atol: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, bool]:
    """
    Evolve DNLS from psi0 to t_end with DOP853.

    Parameters
    ----------
    psi0 : array_like, shape (N,), real
        Initial mid-gap eigenstate (will be L2-normalised internally).
    lam : float
        Nonlinearity strength.
    hoppings : ndarray, shape (N-1,)
        Off-diagonal entries of the hopping Hamiltonian.
    t_end : float
        Final integration time.
    n_checkpoints : int
        Number of logarithmically-spaced checkpoints in (1, t_end].
    norm_tol : float
        Warn if |L2-norm - 1| > norm_tol at any checkpoint.
    rtol, atol : float
        DOP853 tolerances.

    Returns
    -------
    t_arr   : ndarray, shape (n_checkpoints+1,)  - times sampled
    ipr_arr : ndarray, shape (n_checkpoints+1,)  - IPR at each time
    norm_arr: ndarray, shape (n_checkpoints+1,)  - L2-norm at each time
    norm_ok : bool  - True iff max |L2-norm - 1| <= norm_tol
    """
    # Normalise initial condition to unit L2 norm
    psi0 = np.asarray(psi0, dtype=float)
    psi0 = psi0 / np.sqrt(np.dot(psi0, psi0))

    # Real-valued state vector [Re(psi); Im(psi)], imaginary part starts at 0
    state0 = np.concatenate([psi0, np.zeros_like(psi0)])

    # Log-spaced checkpoints; always include t=0
    t_log = np.geomspace(1.0, t_end, n_checkpoints)
    t_eval = np.unique(np.concatenate([[0.0], t_log]))

    sol = solve_ivp(
        dnls_rhs,
        t_span=(0.0, t_end),
        y0=state0,
        method="DOP853",
        t_eval=t_eval,
        args=(lam, hoppings),
        rtol=rtol,
        atol=atol,
        dense_output=False,
    )

    N = len(psi0)
    n_pts = sol.y.shape[1]
    ipr_arr = np.empty(n_pts)
    norm_arr = np.empty(n_pts)

    for k in range(n_pts):
        psi_k = sol.y[:N, k] + 1j * sol.y[N:, k]
        norm_arr[k] = float(np.sqrt(np.sum(np.abs(psi_k) ** 2)))
        ipr_arr[k] = ipr(psi_k)

    norm_ok = bool(np.max(np.abs(norm_arr - 1.0)) <= norm_tol)
    return sol.t, ipr_arr, norm_arr, norm_ok


# ---------------------------------------------------------------------------
# 3. Sweep constants  (defaults match the paper: N=500, lambda includes 0)
# ---------------------------------------------------------------------------

N_SITES = 500         # chain length, matching Table 1 of the paper
T_END = 1000.0        # final time for pilot run (T = 10^3)
N_CHECKPOINTS = 200   # number of log-spaced checkpoints in (1, T_END]
NORM_TOL = 1e-5       # tight threshold; DOP853 at rtol=1e-8 should clear it easily
LAMBDAS = [0.0, 1.0, 2.0, 4.0, 8.0, 10.0]   # lambda=0 is the linear-limit sanity check
RTOL = 1e-8
ATOL = 1e-10
OUT_CSV = "ipr_vs_time.csv"

CHAINS: dict[str, Callable[[int], list[int]]] = {
    "fibonacci": fibonacci_word,
    "tribonacci": tribonacci_word,
}


# ---------------------------------------------------------------------------
# 4. Main sweep
# ---------------------------------------------------------------------------

def run_sweep(
    n: int = N_SITES,
    t_end: float = T_END,
    n_checkpoints: int = N_CHECKPOINTS,
    norm_tol: float = NORM_TOL,
    lambdas: list[float] | None = None,
    out_csv: str = OUT_CSV,
    verbose: bool = True,
) -> None:
    """
    Sweep over chains x lambdas, integrate DNLS to t_end, and write CSV.

    Output CSV columns
    ------------------
    time    - checkpoint time
    lambda  - nonlinearity strength
    chain   - "fibonacci" or "tribonacci"
    IPR     - inverse participation ratio at that time
    norm    - L2-norm at that time (should remain ~ 1.0 if tolerances are met)
    """
    if lambdas is None:
        lambdas = LAMBDAS

    rows: list[dict] = []
    n_runs = len(CHAINS) * len(lambdas)
    run_idx = 0

    for chain_name, word_fn in CHAINS.items():
        word = word_fn(n)
        H, hoppings = build_hamiltonian(word, n)
        psi0, E0 = mid_gap_state(H)

        if verbose:
            print(f"\nchain={chain_name}  N={n}  mid-gap eigenvalue E0={E0:.6f}")

        for lam in lambdas:
            run_idx += 1
            t_wall = _time.perf_counter()

            if verbose:
                print(
                    f"  [{run_idx}/{n_runs}] lambda={lam:.1f}  T={t_end:.0f} ...",
                    end=" ",
                    flush=True,
                )

            t_arr, ipr_arr, norm_arr, norm_ok = evolve_dnls(
                psi0,
                lam,
                hoppings,
                t_end=t_end,
                n_checkpoints=n_checkpoints,
                norm_tol=norm_tol,
                rtol=RTOL,
                atol=ATOL,
            )

            elapsed = _time.perf_counter() - t_wall
            flag = "" if norm_ok else "  *** NORM LEAK ***"

            if verbose:
                print(f"done in {elapsed:.1f}s{flag}")

            for t_k, ipr_k, norm_k in zip(t_arr, ipr_arr, norm_arr):
                rows.append(
                    {
                        "time": t_k,
                        "lambda": lam,
                        "chain": chain_name,
                        "IPR": ipr_k,
                        "norm": norm_k,
                    }
                )

    with open(out_csv, "w", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["time", "lambda", "chain", "IPR", "norm"]
        )
        writer.writeheader()
        writer.writerows(rows)

    if verbose:
        print(f"\nWrote {len(rows)} rows -> {out_csv}")


# ---------------------------------------------------------------------------
# 5. Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Long-time DNLS evolution on Fibonacci/Tribonacci chains. "
            "Outputs a long-format CSV with columns: time, lambda, chain, IPR, norm."
        )
    )
    ap.add_argument(
        "-N", "--sites",
        type=int, default=N_SITES,
        help=f"chain length (default: {N_SITES})",
    )
    ap.add_argument(
        "-T", "--t-end",
        type=float, default=T_END,
        help=f"final integration time (default: {T_END})",
    )
    ap.add_argument(
        "--checkpoints",
        type=int, default=N_CHECKPOINTS,
        help=f"number of log-spaced checkpoints in (1, T] (default: {N_CHECKPOINTS})",
    )
    ap.add_argument(
        "--norm-tol",
        type=float, default=NORM_TOL,
        help=f"norm-leak warning threshold (default: {NORM_TOL})",
    )
    ap.add_argument(
        "--lambdas",
        type=float, nargs="+", default=LAMBDAS,
        help="nonlinearity values to sweep (default: 0.0 1.0 2.0 4.0 8.0 10.0)",
    )
    ap.add_argument(
        "--out",
        default=OUT_CSV,
        help=f"output CSV path (default: {OUT_CSV})",
    )
    ap.add_argument(
        "--quiet",
        action="store_true",
        help="suppress progress output",
    )
    args = ap.parse_args()

    run_sweep(
        n=args.sites,
        t_end=args.t_end,
        n_checkpoints=args.checkpoints,
        norm_tol=args.norm_tol,
        lambdas=args.lambdas,
        out_csv=args.out,
        verbose=not args.quiet,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
