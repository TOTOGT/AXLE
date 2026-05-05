"""
dnls_nbonacci.py
================
Discrete Nonlinear Schrödinger (DNLS) dynamics on Fibonacci and Tribonacci
substitution chains.

Companion code for:
  "Differential Nonlinear Robustness of Critical States in Fibonacci and
   Tribonacci Substitution Chains"
  Pablo Nogueira Grossi, G6 LLC (2026)
  DOI (this paper): 10.5281/zenodo.20026943
  DOI (Vol. I): 10.5281/zenodo.19117400

Usage
-----
    python dnls_nbonacci.py

Outputs
-------
    results_table.txt   — IPR vs λ table (reproduces Table 1 of the paper)
    ipr_vs_lambda.csv   — machine-readable version of same

Dependencies
------------
    numpy, scipy  (standard scientific Python)

Author
------
    Pablo Nogueira Grossi  |  ORCID: 0009-0000-6496-2186
    G6 LLC, Newark NJ  |  pablogrossi@hotmail.com
    GitHub: https://github.com/TOTOGT/AXLE

License: MIT
"""

import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# 1.  Substitution word generators
# ---------------------------------------------------------------------------

def fibonacci_word(length):
    """
    Fibonacci substitution: A -> AB, B -> A  (letters encoded 0, 1).
    Returns the first `length` symbols of the infinite Fibonacci word.
    """
    word = [0]
    rules = {0: [0, 1], 1: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]


def tribonacci_word(length):
    """
    Rauzy (tribonacci) substitution: 1->12, 2->13, 3->1  (letters 0,1,2).
    Returns the first `length` symbols of the infinite tribonacci word.

    Letter frequencies converge to the left Perron–Frobenius eigenvector of
        M = [[1,1,1],[1,0,0],[0,1,0]]
    giving (f_1, f_2, f_3) ≈ (0.5437, 0.2956, 0.1607).
    """
    word = [0]
    rules = {0: [0, 1], 1: [0, 2], 2: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]


# ---------------------------------------------------------------------------
# 2.  Tight-binding Hamiltonian
# ---------------------------------------------------------------------------

def build_hamiltonian(word, N, t_mod=0.5):
    """
    Tridiagonal tight-binding Hamiltonian on N sites.

    Hopping amplitudes assigned to substitution letters:
        letter 0 -> t_A = 1.0
        letter 1 -> t_B = t_mod
        letter 2 -> t_C = t_mod^2

    H[j, j+1] = H[j+1, j] = t_{word[j]},  diagonal = 0.

    Parameters
    ----------
    word   : list of ints, substitution word (length >= N)
    N      : int, number of sites
    t_mod  : float, modulation parameter (default 0.5, generic incommensurate)

    Returns
    -------
    H : (N, N) ndarray, real symmetric Hamiltonian
    hoppings : (N-1,) ndarray, bond hopping values
    """
    hop_map = {0: 1.0, 1: t_mod, 2: t_mod**2}
    hoppings = np.array([hop_map.get(word[j], t_mod) for j in range(N - 1)])
    H = np.zeros((N, N))
    for j in range(N - 1):
        H[j, j + 1] = hoppings[j]
        H[j + 1, j] = hoppings[j]
    return H, hoppings


def mid_gap_state(H):
    """
    Return the eigenstate of H whose eigenvalue is closest to E = 0
    (the mid-gap critical state), together with that eigenvalue.
    """
    vals, vecs = eigh(H)
    idx = np.argmin(np.abs(vals))
    return vecs[:, idx], vals[idx]


def ipr(psi):
    """Inverse participation ratio: sum |psi_j|^4 / (sum |psi_j|^2)^2."""
    norm2 = np.sum(np.abs(psi)**2)
    return np.sum(np.abs(psi)**4) / norm2**2


# ---------------------------------------------------------------------------
# 3.  DNLS time evolution
# ---------------------------------------------------------------------------

def dnls_rhs(t, z, lam, hoppings):
    """
    Right-hand side of the DNLS equation split into real/imaginary parts.

        i d psi_j / dt = -sum_{<j,k>} t_{jk} psi_k + lam |psi_j|^2 psi_j

    State vector z = [Re(psi), Im(psi)], length 2N.

    Parameters
    ----------
    t        : float, time (not used explicitly, required by solve_ivp)
    z        : (2N,) ndarray
    lam      : float, nonlinear coupling
    hoppings : (N-1,) ndarray, bond hoppings

    Returns
    -------
    dz/dt : (2N,) ndarray
    """
    N = len(z) // 2
    psi = z[:N] + 1j * z[N:]

    dpsi = np.zeros(N, dtype=complex)
    dpsi[:-1] -= hoppings * psi[1:]
    dpsi[1:]  -= hoppings * psi[:-1]
    dpsi      += lam * np.abs(psi)**2 * psi

    dpsi_dt = -1j * dpsi
    return np.concatenate([dpsi_dt.real, dpsi_dt.imag])


def evolve_dnls(psi0, hoppings, lam, T=50.0, rtol=1e-7, atol=1e-9):
    """
    Integrate the DNLS equation from t=0 to t=T.

    Parameters
    ----------
    psi0     : (N,) complex ndarray, initial wavefunction
    hoppings : (N-1,) ndarray
    lam      : float, nonlinear coupling
    T        : float, integration time
    rtol, atol : solver tolerances

    Returns
    -------
    psi_final : (N,) complex ndarray
    norm_final : float  (should be ≈ norm of psi0; checks conservation)
    """
    N = len(psi0)
    z0 = np.concatenate([psi0.real, psi0.imag])
    sol = solve_ivp(
        dnls_rhs, [0, T], z0,
        args=(lam, hoppings),
        method='RK45', rtol=rtol, atol=atol, max_step=0.1
    )
    zf = sol.y[:, -1]
    psi_f = zf[:N] + 1j * zf[N:]
    return psi_f, np.sum(np.abs(psi_f)**2)


# ---------------------------------------------------------------------------
# 4.  Main: bifurcation scan and output
# ---------------------------------------------------------------------------

def main():
    N = 500
    t_mod = 0.5
    T = 50.0
    lambda_vals = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]

    print("Building substitution words and Hamiltonians ...")
    word_fib  = fibonacci_word(N + 1)
    word_trib = tribonacci_word(N + 1)

    H_fib,  hop_fib  = build_hamiltonian(word_fib,  N, t_mod)
    H_trib, hop_trib = build_hamiltonian(word_trib, N, t_mod)

    psi0_fib,  E_fib  = mid_gap_state(H_fib)
    psi0_trib, E_trib = mid_gap_state(H_trib)

    print(f"  Fibonacci  mid-gap eigenvalue: {E_fib:.6f},  IPR: {ipr(psi0_fib):.6f}")
    print(f"  Tribonacci mid-gap eigenvalue: {E_trib:.6f},  IPR: {ipr(psi0_trib):.6f}")
    print()

    # Verify tribonacci constant η as Perron–Frobenius root
    # Characteristic polynomial: x^3 - x^2 - x - 1 = 0
    eta_roots = np.roots([1, -1, -1, -1])
    eta = float(np.max(eta_roots.real))
    print(f"  Tribonacci constant η (Perron–Frobenius root): {eta:.9f}")
    print(f"  Verification: η^3 - η^2 - η - 1 = {eta**3 - eta**2 - eta - 1:.2e}  (should be ~0)")
    print(f"  η > 1: {eta > 1}  (Lean 4-verified in TribonacciMeasure.lean)")
    print()

    rows = []
    header = f"{'lambda':>8} | {'IPR_trib':>10} | {'IPR_fib':>10} | {'ratio':>8} | {'norm_trib':>10} | {'norm_fib':>10}"
    print(header)
    print("-" * len(header))

    for lam in lambda_vals:
        psi_f_trib, norm_trib = evolve_dnls(psi0_trib, hop_trib, lam, T)
        psi_f_fib,  norm_fib  = evolve_dnls(psi0_fib,  hop_fib,  lam, T)

        ipr_trib = ipr(psi_f_trib)
        ipr_fib  = ipr(psi_f_fib)
        ratio    = ipr_trib / ipr_fib

        row = (lam, ipr_trib, ipr_fib, ratio, norm_trib, norm_fib)
        rows.append(row)
        print(f"{lam:>8.1f} | {ipr_trib:>10.6f} | {ipr_fib:>10.6f} | {ratio:>8.4f} | {norm_trib:>10.6f} | {norm_fib:>10.6f}")

    # Write outputs
    with open("results_table.txt", "w") as f:
        f.write("# DNLS on Fibonacci and Tribonacci chains\n")
        f.write(f"# N={N}, t_mod={t_mod}, T={T}\n")
        f.write(f"# {'lambda':>8} {'IPR_trib':>12} {'IPR_fib':>12} {'ratio':>10}\n")
        for lam, ipr_t, ipr_f, ratio, *_ in rows:
            f.write(f"  {lam:>8.1f} {ipr_t:>12.6f} {ipr_f:>12.6f} {ratio:>10.4f}\n")

    with open("ipr_vs_lambda.csv", "w") as f:
        f.write("lambda,IPR_trib,IPR_fib,ratio,norm_trib,norm_fib\n")
        for row in rows:
            f.write(",".join(f"{v:.8f}" for v in row) + "\n")

    print("\nWrote results_table.txt and ipr_vs_lambda.csv")


if __name__ == "__main__":
    main()
