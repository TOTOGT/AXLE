#!/usr/bin/env python3
"""
analyze_long_time.py
====================
Analysis companion for `dnls_long_time.py`.

Reads `ipr_vs_time.csv` (long-format: time, lambda, chain, IPR, norm) and
produces:

  1. A sanity report (text) covering:
       - lambda = 0 flatness check  (linear-limit baseline)
       - norm-conservation summary  (DOP853 drift per run)
       - t = 0 IPR values           (tie-back to Table 1 of the paper)
  2. fig_long_ipr_vs_t.png         - IPR(t) on log-log, both chains, all lambdas
  3. fig_long_lambda0_check.png    - flatness of the linear-limit run
  4. fig_long_alpha_fit.png        - late-time fits of IPR(t) ~ t^(-alpha)
  5. spreading_exponents.csv       - fitted alpha per (chain, lambda)

Companion to:
  "Differential Nonlinear Robustness of Critical States in Fibonacci and
   Tribonacci Substitution Chains"
  Pablo Nogueira Grossi, G6 LLC (2026)
  DOI: 10.5281/zenodo.20026943

Usage
-----
    python3 analyze_long_time.py                          # uses ipr_vs_time.csv
    python3 analyze_long_time.py --csv long_run.csv       # custom input

Author
------
    Pablo Nogueira Grossi  |  ORCID: 0009-0000-6496-2186
    G6 LLC, Newark NJ  |  GitHub: https://github.com/TOTOGT/AXLE

License: MIT
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# 1. CSV loader
# ---------------------------------------------------------------------------

def load_csv(path: str) -> dict[tuple[str, float], dict[str, np.ndarray]]:
    """
    Load the long-format CSV into a {(chain, lambda): {time, IPR, norm}} dict.
    """
    rows_by_key: dict[tuple[str, float], list[tuple[float, float, float]]] = (
        defaultdict(list)
    )
    with open(path, "r", newline="") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            key = (r["chain"], float(r["lambda"]))
            rows_by_key[key].append(
                (float(r["time"]), float(r["IPR"]), float(r["norm"]))
            )

    out: dict[tuple[str, float], dict[str, np.ndarray]] = {}
    for key, rows in rows_by_key.items():
        rows.sort(key=lambda x: x[0])
        t = np.array([r[0] for r in rows])
        ipr = np.array([r[1] for r in rows])
        norm = np.array([r[2] for r in rows])
        out[key] = {"time": t, "IPR": ipr, "norm": norm}
    return out


# ---------------------------------------------------------------------------
# 2. Sanity report
# ---------------------------------------------------------------------------

def sanity_report(data: dict[tuple[str, float], dict[str, np.ndarray]]) -> dict:
    """
    Print and return a structured sanity report.

    Hard checks:
      - lambda=0 IPR must be flat to ~5 sig figs (linear-limit eigenstate)
      - norm drift max should be << 1e-3 for any reasonable run
    """
    lambdas = sorted({lam for _, lam in data.keys()})
    chains = sorted({ch for ch, _ in data.keys()})

    print("=" * 72)
    print("SANITY REPORT")
    print("=" * 72)

    # --- lambda=0 flatness check ---
    print("\n[1] Linear-limit (lambda=0) flatness check")
    print("    IPR(t) at lambda=0 should be constant -- the t=0 eigenstate")
    print("    evolves only in phase under linear dynamics.")
    print()
    print(f"    {'chain':>12} {'IPR(t=0)':>14} {'IPR(t=T)':>14} "
          f"{'max|dIPR|':>14} {'rel.var.':>12}")
    print("    " + "-" * 68)
    flatness = {}
    for ch in chains:
        key = (ch, 0.0)
        if key not in data:
            print(f"    {ch:>12}  no lambda=0 row -- linear-limit check skipped")
            continue
        ipr = data[key]["IPR"]
        ipr0 = float(ipr[0])
        iprT = float(ipr[-1])
        max_dev = float(np.max(np.abs(ipr - ipr0)))
        rel = max_dev / abs(ipr0) if ipr0 != 0 else float("inf")
        flatness[ch] = (ipr0, iprT, max_dev, rel)
        print(f"    {ch:>12} {ipr0:>14.8f} {iprT:>14.8f} "
              f"{max_dev:>14.2e} {rel:>12.2e}")

    # --- t=0 IPR (tie-back to Table 1) ---
    print("\n[2] t = 0 IPR values  (tie-back to Table 1 of the paper)")
    print("    These should match the lambda=0 column of Table 1 exactly.")
    print()
    print(f"    {'chain':>12} {'IPR(0)':>14}")
    print("    " + "-" * 28)
    for ch in chains:
        # any lambda will do; t=0 is identical (mid-gap eigenstate)
        for lam in lambdas:
            key = (ch, lam)
            if key in data:
                print(f"    {ch:>12} {float(data[key]['IPR'][0]):>14.8f}")
                break

    # --- norm-conservation summary ---
    print("\n[3] Norm conservation across all runs")
    print("    DOP853 at rtol=1e-8 should keep |norm-1| << 1e-5 over T=10^3.")
    print()
    print(f"    {'chain':>12} {'lambda':>8} {'max|norm-1|':>14}")
    print("    " + "-" * 36)
    norm_summary = []
    worst_drift = 0.0
    for ch in chains:
        for lam in lambdas:
            key = (ch, lam)
            if key not in data:
                continue
            drift = float(np.max(np.abs(data[key]["norm"] - 1.0)))
            worst_drift = max(worst_drift, drift)
            tag = "" if drift < 1e-5 else "  <-- check"
            print(f"    {ch:>12} {lam:>8.2f} {drift:>14.2e}{tag}")
            norm_summary.append((ch, lam, drift))

    # --- final IPR vs lambda summary (compact table) ---
    print("\n[4] Final-time IPR(T) by chain and lambda  (the long-time headline)")
    print()
    header = "    " + f"{'lambda':>8}"
    for ch in chains:
        header += f" {('IPR_' + ch[:4]):>14}"
    if "fibonacci" in chains and "tribonacci" in chains:
        header += f" {'ratio_t/f':>12}"
    print(header)
    print("    " + "-" * (len(header) - 4))

    for lam in lambdas:
        line = f"    {lam:>8.2f}"
        ipr_by_chain = {}
        for ch in chains:
            key = (ch, lam)
            if key in data:
                v = float(data[key]["IPR"][-1])
                ipr_by_chain[ch] = v
                line += f" {v:>14.8f}"
            else:
                line += f" {'-':>14}"
        if "fibonacci" in ipr_by_chain and "tribonacci" in ipr_by_chain:
            line += f" {ipr_by_chain['tribonacci']/ipr_by_chain['fibonacci']:>12.4f}"
        print(line)

    print()
    print("=" * 72)
    return {
        "flatness": flatness,
        "norm_summary": norm_summary,
        "worst_drift": worst_drift,
    }


# ---------------------------------------------------------------------------
# 3. Plots
# ---------------------------------------------------------------------------

def plot_ipr_vs_t(
    data: dict[tuple[str, float], dict[str, np.ndarray]],
    out_path: str = "fig_long_ipr_vs_t.png",
) -> None:
    """
    Log-log IPR(t) for both chains, all lambdas. Solid = tribonacci, dashed = fibonacci.
    """
    chains = sorted({ch for ch, _ in data.keys()})
    lambdas = sorted({lam for _, lam in data.keys()})

    fig, ax = plt.subplots(figsize=(8, 6), dpi=140)
    cmap = plt.cm.viridis(np.linspace(0.05, 0.95, len(lambdas)))
    style = {"fibonacci": "--", "tribonacci": "-"}
    width = {"fibonacci": 1.3, "tribonacci": 1.8}

    for ch in chains:
        for i, lam in enumerate(lambdas):
            key = (ch, lam)
            if key not in data:
                continue
            t = data[key]["time"]
            ipr = data[key]["IPR"]
            mask = t > 0
            ax.loglog(
                t[mask],
                ipr[mask],
                style.get(ch, "-"),
                color=cmap[i],
                lw=width.get(ch, 1.5),
                label=f"{ch[:4]}  lambda={lam:.1f}",
            )

    ax.set_xlabel("time  t")
    ax.set_ylabel("IPR(t)")
    ax.set_title("Long-time IPR on Fibonacci (dashed) and Tribonacci (solid) chains")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(ncol=2, fontsize=8, loc="best")
    plt.tight_layout()
    plt.savefig(out_path, dpi=140)
    plt.close()
    print(f"  -> {out_path}")


def plot_lambda0_check(
    data: dict[tuple[str, float], dict[str, np.ndarray]],
    out_path: str = "fig_long_lambda0_check.png",
) -> None:
    """
    Linear-limit sanity plot: IPR(t) at lambda=0 should be visually flat.
    """
    chains = sorted({ch for ch, _ in data.keys()})
    fig, ax = plt.subplots(figsize=(8, 5), dpi=140)
    for ch in chains:
        key = (ch, 0.0)
        if key not in data:
            continue
        t = data[key]["time"]
        ipr = data[key]["IPR"]
        ax.semilogx(t[t > 0], ipr[t > 0], lw=1.6, label=f"{ch}  IPR(0)={ipr[0]:.5f}")
    ax.set_xlabel("time  t")
    ax.set_ylabel("IPR(t)  at lambda = 0")
    ax.set_title("Linear-limit sanity check (IPR should be flat)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    plt.tight_layout()
    plt.savefig(out_path, dpi=140)
    plt.close()
    print(f"  -> {out_path}")


# ---------------------------------------------------------------------------
# 4. Spreading-exponent fit  (open question 3)
# ---------------------------------------------------------------------------

def fit_alpha(t: np.ndarray, ipr: np.ndarray, late_frac: float = 0.3
              ) -> tuple[float, float, int]:
    """
    Fit IPR(t) ~ A * t^(-alpha) on the late-time tail.

    Strategy: take the last `late_frac` of points by log(t), do a linear
    regression of log(IPR) on log(t). Returns (alpha, log_A, n_points).

    A positive alpha means the participation length L_eff ~ 1 / IPR is
    spreading; alpha = 1 is ballistic / fully extended; alpha < 1 is
    sub-diffusive; alpha approx 0 is self-trapping.
    """
    mask = (t > 0) & (ipr > 0)
    t = t[mask]
    ipr = ipr[mask]
    if len(t) < 6:
        return float("nan"), float("nan"), 0

    log_t = np.log(t)
    log_ipr = np.log(ipr)
    cutoff = log_t[0] + (1.0 - late_frac) * (log_t[-1] - log_t[0])
    sel = log_t >= cutoff
    if sel.sum() < 4:
        return float("nan"), float("nan"), int(sel.sum())

    slope, intercept = np.polyfit(log_t[sel], log_ipr[sel], 1)
    return float(-slope), float(intercept), int(sel.sum())


def alpha_table_and_plot(
    data: dict[tuple[str, float], dict[str, np.ndarray]],
    csv_out: str = "spreading_exponents.csv",
    fig_out: str = "fig_long_alpha_fit.png",
) -> None:
    """
    Fit alpha for each (chain, lambda) with lambda > 0; write CSV; plot
    fits overlaid on the IPR(t) curves for visual inspection.
    """
    chains = sorted({ch for ch, _ in data.keys()})
    lambdas = sorted({lam for _, lam in data.keys() if lam > 0.0})

    rows: list[tuple[str, float, float, float, int]] = []
    for ch in chains:
        for lam in lambdas:
            key = (ch, lam)
            if key not in data:
                continue
            t = data[key]["time"]
            ipr = data[key]["IPR"]
            alpha, log_A, n = fit_alpha(t, ipr)
            rows.append((ch, lam, alpha, log_A, n))

    with open(csv_out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["chain", "lambda", "alpha", "log_A", "n_points"])
        for r in rows:
            w.writerow([r[0], f"{r[1]:.4f}", f"{r[2]:.6f}", f"{r[3]:.6f}", r[4]])
    print(f"  -> {csv_out}")

    print("\n[5] Spreading-exponent fits  IPR(t) ~ t^(-alpha) on late tail")
    print(f"    {'chain':>12} {'lambda':>8} {'alpha':>10} {'pts':>6}")
    print("    " + "-" * 38)
    for ch, lam, alpha, _, n in rows:
        print(f"    {ch:>12} {lam:>8.2f} {alpha:>10.4f} {n:>6d}")

    # Visual: log-log curves with the fitted slope drawn over the late tail.
    fig, axes = plt.subplots(1, len(chains), figsize=(6 * len(chains), 5), dpi=140,
                             squeeze=False)
    cmap = plt.cm.plasma(np.linspace(0.05, 0.95, max(len(lambdas), 1)))
    for ax, ch in zip(axes[0], chains):
        for i, lam in enumerate(lambdas):
            key = (ch, lam)
            if key not in data:
                continue
            t = data[key]["time"]
            ipr = data[key]["IPR"]
            mask = (t > 0) & (ipr > 0)
            ax.loglog(t[mask], ipr[mask], color=cmap[i], lw=1.4,
                      label=f"lambda={lam:.1f}")
            alpha, log_A, n = fit_alpha(t, ipr)
            if np.isfinite(alpha) and n >= 4:
                t_tail = t[mask][-n:]
                fit_line = np.exp(log_A) * t_tail ** (-alpha)
                ax.loglog(t_tail, fit_line, ":", color=cmap[i], lw=2.2)
        ax.set_xlabel("time  t")
        ax.set_ylabel("IPR(t)")
        ax.set_title(f"{ch}  (dotted = late-time t^(-alpha) fit)")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=8, loc="best")
    plt.tight_layout()
    plt.savefig(fig_out, dpi=140)
    plt.close()
    print(f"  -> {fig_out}")


# ---------------------------------------------------------------------------
# 5. Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Analyze long-time DNLS output (ipr_vs_time.csv)."
    )
    ap.add_argument("--csv", default="ipr_vs_time.csv",
                    help="input CSV path (default: ipr_vs_time.csv)")
    ap.add_argument("--no-plots", action="store_true",
                    help="skip plotting (sanity report + alpha CSV only)")
    args = ap.parse_args()

    data = load_csv(args.csv)
    if not data:
        print(f"ERROR: no rows loaded from {args.csv}", file=sys.stderr)
        return 1

    sanity_report(data)

    if not args.no_plots:
        print("\nGenerating figures ...")
        plot_ipr_vs_t(data)
        plot_lambda0_check(data)

    alpha_table_and_plot(data)
    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
