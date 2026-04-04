"""
AXLE — C9.2 Pipeline: Fourier Analysis of Collatz Drift
scripts/c92_fourier.py

Reads the sample CSV produced by c92_sampler.py and computes:
  1. Mean-centered drift vector across M residue classes
  2. DFT spectrum of that vector
  3. Mean-centered sparsity metrics

Outputs:
  c92_fourier_N{N}_M{M}.json — spectrum, sparsity, and dominant frequency

Usage:
  python c92_fourier.py --N 10000 --M 8  --out outputs/
  python c92_fourier.py --N 100000 --M 12 --out outputs/

Dependency: only Python standard library (no numpy/scipy required).

G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026
MIT License
"""

import argparse
import cmath
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _std(values: list[float], mean: float) -> float:
    if len(values) < 2:
        return 0.0
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


# ── DFT ───────────────────────────────────────────────────────────────────────

def dft(values: list[float]) -> list[dict]:
    """
    Compute the (unnormalised) Discrete Fourier Transform of a real sequence.

    Returns a list of dicts with keys:
      freq_idx  — frequency bin index k (0 … N-1)
      magnitude — |X[k]| / N  (amplitude, normalised)
      phase_rad — arg(X[k])   (phase in radians)
      re, im    — real and imaginary parts of X[k] / N
    """
    N = len(values)
    if N == 0:
        return []

    spectrum = []
    for k in range(N):
        coef = sum(
            values[j] * cmath.exp(-2j * math.pi * k * j / N)
            for j in range(N)
        )
        magnitude = abs(coef) / N
        spectrum.append({
            "freq_idx": k,
            "magnitude": round(magnitude, 10),
            "phase_rad": round(cmath.phase(coef), 10),
            "re": round(coef.real / N, 10),
            "im": round(coef.imag / N, 10),
        })
    return spectrum


# ── MEAN-CENTERED SPARSITY ────────────────────────────────────────────────────

def mean_centered_sparsity(values: list[float]) -> dict:
    """
    Compute mean-centered sparsity metrics for a population of drift
    observables.

    All statistics are computed on the mean-centered (zero-mean) version
    of the input.  The sparsity index is the fraction of centered values
    whose absolute value falls below 10 % of the maximum absolute value
    (threshold-sparsity definition, robust to scale).

    Returns a dict with:
      mean            — global mean of the raw values
      std             — standard deviation of the raw values
      l1_norm         — ‖x - mean‖₁  (sum of absolute centered values)
      l0_count        — count of non-negligible centered coefficients
      sparsity        — fraction of centered values below threshold
      max_abs_centered — max |xᵢ - mean|
    """
    if not values:
        return {
            "mean": 0.0, "std": 0.0,
            "l1_norm": 0.0, "l0_count": 0,
            "sparsity": 0.0, "max_abs_centered": 0.0,
        }

    mean = _mean(values)
    std = _std(values, mean)
    centered = [v - mean for v in values]

    l1 = sum(abs(c) for c in centered)
    # L0: non-negligible (above floating-point noise floor)
    l0 = sum(1 for c in centered if abs(c) > 1e-12)

    max_abs = max(abs(c) for c in centered) if centered else 0.0
    threshold = 0.10 * max_abs if max_abs > 0 else 1e-12
    sparse_count = sum(1 for c in centered if abs(c) < threshold)
    sparsity = sparse_count / len(centered)

    return {
        "mean": round(mean, 10),
        "std": round(std, 10),
        "l1_norm": round(l1, 10),
        "l0_count": l0,
        "sparsity": round(sparsity, 10),
        "max_abs_centered": round(max_abs, 10),
    }


# ── FOURIER ANALYSIS ──────────────────────────────────────────────────────────

def run_fourier_analysis(N: int, M: int, in_dir: Path, out_dir: Path) -> dict:
    """
    Load the sample CSV produced by c92_sampler.py, run Fourier analysis,
    and write c92_fourier_N{N}_M{M}.json.

    Parameters
    ----------
    N      : parameter used when running the sampler
    M      : number of residue classes (must match sampler run)
    in_dir : directory containing the sample CSV
    out_dir: directory where the Fourier JSON will be written

    Returns
    -------
    result dict (also written to JSON)
    """
    csv_path = in_dir / f"c92_sample_N{N}_M{M}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Sample CSV not found: {csv_path}\n"
            f"Run c92_sampler.py --N {N} --M {M} --out {in_dir} first."
        )

    # Load sample data
    rows: list[dict] = []
    with open(csv_path) as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append({
                "n": int(row["n"]),
                "stopping_time": int(row["stopping_time"]),
                "drift_obs": float(row["drift_obs"]),
                "odd_residue_mod_M": int(row["odd_residue_mod_M"]),
            })

    # Group by residue
    by_residue: dict[int, list[float]] = defaultdict(list)
    for row in rows:
        by_residue[row["odd_residue_mod_M"]].append(row["drift_obs"])

    # Global mean for centering
    all_obs = [r["drift_obs"] for r in rows]
    global_mean = _mean(all_obs)

    # Mean-centered residue drift vector (length M)
    mean_per_residue = []
    for r in range(M):
        vals = by_residue.get(r, [])
        r_mean = _mean(vals) if vals else global_mean
        mean_per_residue.append(round(r_mean - global_mean, 10))

    # DFT of the centered residue vector
    spectrum = dft(mean_per_residue)

    # Dominant non-DC frequency (skip k=0)
    dominant = (
        max(spectrum[1:], key=lambda x: x["magnitude"])
        if len(spectrum) > 1
        else spectrum[0]
    )

    # Global mean-centered sparsity metrics
    sparsity_metrics = mean_centered_sparsity(all_obs)

    out_dir.mkdir(parents=True, exist_ok=True)
    fourier_path = out_dir / f"c92_fourier_N{N}_M{M}.json"

    result = {
        "N": N,
        "M": M,
        "window": [N, 2 * N],
        "n_samples": len(rows),
        "global_mean_drift": round(global_mean, 10),
        "mean_centered_residue_vector": mean_per_residue,
        "fourier_spectrum": spectrum,
        "dominant_frequency": dominant,
        "sparsity_metrics": sparsity_metrics,
    }

    with open(fourier_path, "w") as fh:
        json.dump(result, fh, indent=2)

    print(f"[C9.2 Fourier] N={N}, M={M} | Fourier analysis complete")
    print(f"[C9.2 Fourier] Dominant freq idx : {dominant['freq_idx']} "
          f"(magnitude={dominant['magnitude']:.8f})")
    print(f"[C9.2 Fourier] Sparsity (mean-centered): "
          f"{sparsity_metrics['sparsity']:.6f}")
    print(f"[C9.2 Fourier] Fourier JSON → {fourier_path}")

    return result


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="C9.2 Fourier Analysis of Collatz Drift — mean-centered sparsity",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--N", type=int, default=10_000,
                        help="Lower bound of dyadic window (must match sampler)")
    parser.add_argument("--M", type=int, default=8,
                        help="Number of odd residue classes (must match sampler)")
    parser.add_argument("--out", type=str, default="outputs",
                        help="Directory containing sample CSV and receiving JSON")
    args = parser.parse_args()

    out_dir = Path(args.out)
    run_fourier_analysis(args.N, args.M, out_dir, out_dir)
