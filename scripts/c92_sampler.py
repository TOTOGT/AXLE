"""
AXLE — C9.2 Pipeline: Canonical Collatz Sampler
scripts/c92_sampler.py

Graded drift observable per odd residue, dyadic window [N, 2N].

For each odd integer n in [N, 2N] computes:
  drift_obs(n) = stopping_time(n) / log2(n)

and groups results by odd residue class (n mod M).

Outputs:
  c92_sample_N{N}_M{M}.csv     — per-sample data
  c92_summary_N{N}_M{M}.json  — per-residue summary statistics

Usage:
  python c92_sampler.py --N 10000 --M 8  --out outputs/
  python c92_sampler.py --N 100000 --M 12 --out outputs/

G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026
MIT License
"""

import argparse
import csv
import json
import math
import time
from pathlib import Path


# ── COLLATZ STOPPING TIME ─────────────────────────────────────────────────────

def collatz_stopping_time(n: int) -> int:
    """Return the number of steps for n to reach 1 under the Collatz map."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


# ── GRADED DRIFT OBSERVABLE ───────────────────────────────────────────────────

def drift_observable(n: int) -> float:
    """
    Graded drift observable D(n) = stopping_time(n) / log2(n).

    Normalises the stopping time by the natural scale of n so that
    the observable is comparable across the dyadic window [N, 2N].
    """
    return collatz_stopping_time(n) / math.log2(n)


# ── SAMPLER ───────────────────────────────────────────────────────────────────

def sample_dyadic_window(N: int, M: int, out_dir: Path) -> dict:
    """
    Sample all odd integers in the dyadic window [N, 2N].

    Groups results by odd residue class (n mod M) and writes:
      - CSV  with columns: n, stopping_time, drift_obs, odd_residue_mod_M
      - JSON with per-residue summary statistics

    Parameters
    ----------
    N       : lower bound of the dyadic window
    M       : modulus for odd residue grouping
    out_dir : directory where output files are written

    Returns
    -------
    summary dict (also written to JSON)
    """
    t_start = time.time()
    out_dir.mkdir(parents=True, exist_ok=True)

    # All odd integers in [N, 2N]
    first_odd = N if N % 2 == 1 else N + 1
    odds = range(first_odd, 2 * N + 1, 2)

    # Compute drift observable and residue class for every sample
    raw = []
    for n in odds:
        t = collatz_stopping_time(n)
        obs = t / math.log2(n)
        raw.append((n, t, obs, n % M))

    # Global statistics
    all_obs = [obs for _, _, obs, _ in raw]
    global_mean = sum(all_obs) / len(all_obs)

    # Per-residue accumulators
    by_residue: dict[int, list[float]] = {r: [] for r in range(M)}
    for _, _, obs, residue in raw:
        by_residue[residue].append(obs)

    # Write CSV
    csv_path = out_dir / f"c92_sample_N{N}_M{M}.csv"
    with open(csv_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["n", "stopping_time", "drift_obs", "odd_residue_mod_M"])
        writer.writerows(raw)

    # Build residue-level summary (mean-centered)
    residue_stats: dict[str, dict] = {}
    for r in range(M):
        vals = by_residue[r]
        if not vals:
            continue
        r_mean = sum(vals) / len(vals)
        centered = [v - global_mean for v in vals]
        variance = sum(c * c for c in centered) / len(centered)
        residue_stats[str(r)] = {
            "count": len(vals),
            "mean_drift": r_mean,
            "mean_centered_drift": r_mean - global_mean,
            "variance_centered": variance,
        }

    elapsed = time.time() - t_start
    n_samples = len(raw)

    summary = {
        "N": N,
        "M": M,
        "window": [N, 2 * N],
        "n_samples": n_samples,
        "global_mean_drift": global_mean,
        "elapsed_seconds": round(elapsed, 4),
        "residue_stats": residue_stats,
        "csv_path": str(csv_path),
    }

    summary_path = out_dir / f"c92_summary_N{N}_M{M}.json"
    with open(summary_path, "w") as fh:
        json.dump(summary, fh, indent=2)

    print(f"[C9.2 Sampler] N={N}, M={M} | "
          f"sampled {n_samples} odd integers in [{N}, {2*N}] | "
          f"{elapsed:.2f}s")
    print(f"[C9.2 Sampler] Global mean drift : {global_mean:.6f}")
    print(f"[C9.2 Sampler] CSV     → {csv_path}")
    print(f"[C9.2 Sampler] Summary → {summary_path}")

    return summary


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="C9.2 Canonical Collatz Sampler — dyadic window [N, 2N]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--N", type=int, default=10_000,
                        help="Lower bound of dyadic window [N, 2N]")
    parser.add_argument("--M", type=int, default=8,
                        help="Modulus for odd residue grouping (n mod M)")
    parser.add_argument("--out", type=str, default="outputs",
                        help="Output directory for CSV and JSON")
    args = parser.parse_args()

    sample_dyadic_window(args.N, args.M, Path(args.out))
