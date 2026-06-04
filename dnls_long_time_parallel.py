"""
dnls_long_time_parallel.py
Parallel version of long-time DNLS evolution.
"""

import csv
import time as _time
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp
from joblib import Parallel, delayed
from tqdm import tqdm


# ---------------------------------------------------------------------------
# 1. Same helper functions as before
# ---------------------------------------------------------------------------

def fibonacci_word(length):
    word = [0]
    rules = {0: [0, 1], 1: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]


def tribonacci_word(length):
    word = [0]
    rules = {0: [0, 1], 1: [0, 2], 2: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]


def build_hamiltonian(word, N, t_mod=0.5):
    hop_map = {0: 1.0, 1: t_mod, 2: t_mod**2}
    hoppings = np.array([hop_map.get(word[j], t_mod) for j in range(N - 1)])
    H = np.zeros((N, N))
    for j in range(N - 1):
        H[j, j + 1] = hoppings[j]
        H[j + 1, j] = hoppings[j]
    return H, hoppings


def mid_gap_state(H):
    vals, vecs = eigh(H)
    idx = np.argmin(np.abs(vals))
    return vecs[:, idx], vals[idx]


def ipr(psi):
    norm2 = np.sum(np.abs(psi)**2)
    return np.sum(np.abs(psi)**4) / norm2**2


def dnls_rhs(t, z, lam, hoppings):
    N = len(z) // 2
    psi = z[:N] + 1j * z[N:]

    dpsi = np.zeros(N, dtype=complex)
    dpsi[:-1] -= hoppings * psi[1:]
    dpsi[1:]  -= hoppings * psi[:-1]
    dpsi      += lam * np.abs(psi)**2 * psi

    dpsi_dt = -1j * dpsi
    return np.concatenate([dpsi_dt.real, dpsi_dt.imag])


def evolve_dnls_long(psi0, hoppings, lam, t_eval, rtol=1e-9, atol=1e-12):
    N = len(psi0)
    z0 = np.concatenate([psi0.real, psi0.imag])

    if t_eval[0] != 0.0:
        t_eval = np.concatenate([[0.0], t_eval])

    sol = solve_ivp(
        dnls_rhs,
        [0.0, t_eval[-1]],
        z0,
        args=(lam, hoppings),
        method='DOP853',
        rtol=rtol,
        atol=atol,
        t_eval=t_eval,
    )
    if not sol.success:
        raise RuntimeError(f"DOP853 failed for lam={lam}: {sol.message}")

    iprs = np.empty(len(t_eval))
    norms = np.empty(len(t_eval))
    for k in range(len(t_eval)):
        zk = sol.y[:, k]
        psi_k = zk[:N] + 1j * zk[N:]
        norms[k] = np.sum(np.abs(psi_k)**2)
        iprs[k] = ipr(psi_k)

    return iprs, norms, lam   # return lam for identification


# ---------------------------------------------------------------------------
# 2. Parallel worker
# ---------------------------------------------------------------------------

def run_one_case(lam, chain_name, psi0, hoppings, norm0, t_eval):
    t0 = _time.time()
    try:
        iprs, norms, _ = evolve_dnls_long(psi0, hoppings, lam, t_eval)
        dt = _time.time() - t0

        drift = float(np.max(np.abs(norms - norm0)))
        return {
            "lam": lam,
            "chain": chain_name,
            "iprs": iprs,
            "norms": norms,
            "drift": drift,
            "time": dt,
            "success": True
        }
    except Exception as e:
        return {
            "lam": lam,
            "chain": chain_name,
            "success": False,
            "error": str(e)
        }


# ---------------------------------------------------------------------------
# 3. Main
# ---------------------------------------------------------------------------

def main():
    # --- Configuration ---
    N = 500
    t_mod = 0.5
    T_FINAL = 1000.0
    NORM_TOL = 1.0e-5
    n_jobs = -1                    # -1 = use all CPU cores
    lambda_vals = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]

    n_checkpoints = 16
    t_eval = np.concatenate([
        [0.0],
        np.logspace(0.0, np.log10(T_FINAL), n_checkpoints),
    ])

    print("Building substitution words and Hamiltonians ...")
    word_fib  = fibonacci_word(N + 1)
    word_trib = tribonacci_word(N + 1)

    H_fib,  hop_fib  = build_hamiltonian(word_fib,  N, t_mod)
    H_trib, hop_trib = build_hamiltonian(word_trib, N, t_mod)

    psi0_fib,  _ = mid_gap_state(H_fib)
    psi0_trib, _ = mid_gap_state(H_trib)

    norm0_fib  = float(np.sum(np.abs(psi0_fib)**2))
    norm0_trib = float(np.sum(np.abs(psi0_trib)**2))

    print(f"  Fibonacci  IPR_0: {ipr(psi0_fib):.6f}   norm_0: {norm0_fib:.10f}")
    print(f"  Tribonacci IPR_0: {ipr(psi0_trib):.6f}   norm_0: {norm0_trib:.10f}")
    print(f"  Running {len(lambda_vals)*2} cases on {n_jobs if n_jobs>0 else 'all'} cores...\n")

    # Prepare all tasks
    tasks = []
    for lam in lambda_vals:
        tasks.append((lam, "trib", psi0_trib, hop_trib, norm0_trib, t_eval))
        tasks.append((lam, "fib",  psi0_fib,  hop_fib,  norm0_fib,  t_eval))

    # Run in parallel
    results = Parallel(n_jobs=n_jobs)(
        delayed(run_one_case)(*task) for task in tqdm(tasks, desc="DNLS runs")
    )

    # Collect rows and flags
    rows = []
    flagged = []

    for res in results:
        if not res["success"]:
            print(f"❌ Failed: lam={res['lam']} {res['chain']} → {res['error']}")
            continue

        for tk, ipr_k, norm_k in zip(t_eval, res["iprs"], res["norms"]):
            rows.append((float(tk), float(res["lam"]), res["chain"],
                         float(ipr_k), float(norm_k)))

        if res["drift"] > NORM_TOL:
            flagged.append((res["chain"], res["lam"], res["drift"]))

        status = "  DRIFT!" if res["drift"] > NORM_TOL else "  OK"
        print(f"  lam={res['lam']:>5.2f}  {res['chain']:>4}  "
              f"drift={res['drift']:.2e}  ({res['time']:.1f}s){status}")

    # Write CSV
    with open("ipr_vs_time.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time", "lambda", "chain", "IPR", "norm"])
        for r in rows:
            w.writerow([f"{r[0]:.6f}", f"{r[1]:.4f}", r[2],
                        f"{r[3]:.10f}", f"{r[4]:.12f}"])

    # Write summary
    with open("long_time_results.txt", "w") as f:
        f.write("# Parallel long-time DNLS on Fibonacci and Tribonacci\n")
        f.write(f"# N={N}, t_mod={t_mod}, T_FINAL={T_FINAL}\n")
        f.write(f"# integrator=DOP853, jobs={n_jobs}\n")
        # ... (same as before)
        f.write("\n# Norm-conservation flags\n")
        if not flagged:
            f.write("#   All runs conserved norm to better than {:.0e}\n".format(NORM_TOL))
        else:
            for ch, lam, drift in flagged:
                f.write(f"#   DRIFT: chain={ch}  lambda={lam}  drift={drift:.3e}\n")

    print("\n✅ Done! Files written: ipr_vs_time.csv and long_time_results.txt")


if __name__ == "__main__":
    main()
