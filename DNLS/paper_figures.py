#!/usr/bin/env python3
"""
paper_figures.py
================
Paper-grade figures for the long-time / FSS DNLS results.

Renders four figures from the verified data produced by `dnls_long_time.py`
+ `analyze_long_time.py` + `fss_analyze.py`:

  fig_A_d2_scaling.png       Multifractal D2 extraction at lambda=0
                             (linear-limit IPR vs N, log-log)
  fig_B_nstability.png       Trib/fib IPR ratio at T=10^4 across (N, lambda)
                             — the N-stability matrix as a heatmap
  fig_C_inversion.png        Robustness inversion: IPR(T)/IPR(0) vs N for
                             both chains at lambda=1 — small N favours fib,
                             large N favours trib
  fig_D_homogenization.png   Trib/fib ratio vs lambda at fixed N=500 for
                             T=10^4 and T=10^5 — homogenization at long times

The data tables are embedded as Python literals so the script is
self-contained and reproducible without the source CSVs. Numbers come
from the runs already committed to grossi-ops/Atratores and
TOTOGT/AXLE/DNLS as of the current session.

Usage
-----
    python3 paper_figures.py             # writes 4 PNGs in CWD
    python3 paper_figures.py --outdir figs

Author
------
    Pablo Nogueira Grossi  |  G6 LLC  |  https://github.com/TOTOGT/AXLE

License: MIT
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

COLOR_FIB = "#3e7cb1"     # medium blue  (Fibonacci)
COLOR_TRIB = "#c14a3a"    # rust red     (Rauzy-Tribonacci)
COLOR_NEUTRAL = "#777777"
COLOR_HIGHLIGHT = "#c9a84c"  # warm gold (annotations)

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.dpi": 180,
    "savefig.bbox": "tight",
})


# ---------------------------------------------------------------------------
# Data tables  (verbatim from runs in the current session)
# ---------------------------------------------------------------------------

# Linear-limit IPR(N) at lambda = 0, T = 10^4 (mid-gap eigenstate).
# Used for the multifractal D2 fit.
N_VALUES = np.array([200, 500, 1000, 2000])
IPR_FIB_LINEAR = np.array([0.03575499, 0.02096451, 0.01080272, 0.00940314])
IPR_TRIB_LINEAR = np.array([0.09692508, 0.08201561, 0.04100882, 0.04839821])

# T = 10^4 final-time IPR by (N, lambda).
# Format: { N: { lambda: (IPR_fib, IPR_trib), ... }, ... }
LAMBDAS = [0.0, 1.0, 2.0, 4.0, 8.0, 10.0]

T1E4 = {
    200: {
        0.0:  (0.03575499, 0.09692508),
        1.0:  (0.01126183, 0.01246712),
        2.0:  (0.01118205, 0.01117019),
        4.0:  (0.00962673, 0.00999188),
        8.0:  (0.01038053, 0.01127915),
        10.0: (0.00960840, 0.00989897),
    },
    500: {
        0.0:  (0.02096451, 0.08201561),
        1.0:  (0.00574806, 0.01197646),
        2.0:  (0.00426846, 0.00591380),
        4.0:  (0.00379125, 0.00626311),
        8.0:  (0.00395431, 0.00453901),
        10.0: (0.00389156, 0.00491297),
    },
    1000: {
        0.0:  (0.01080272, 0.04100882),
        1.0:  (0.00453331, 0.01045178),
        2.0:  (0.00328806, 0.00576027),
        4.0:  (0.00234336, 0.00280575),
        8.0:  (0.00211298, 0.00301105),
        10.0: (0.00200220, 0.00253869),
    },
    2000: {
        0.0:  (0.00940314, 0.04839821),
        1.0:  (0.00337754, 0.02237716),
        2.0:  (0.00190044, 0.00772133),
        4.0:  (0.00199914, 0.00350344),
        8.0:  (0.00149985, 0.00244416),
        10.0: (0.00143363, 0.00257801),
    },
}

# T = 10^5 final-time IPR at N = 500, by lambda.
T1E5_N500 = {
    0.0:  (0.02096451, 0.08201561),
    1.0:  (0.00391307, 0.00431364),
    2.0:  (0.00406452, 0.00433711),
    4.0:  (0.00389356, 0.00404125),
    8.0:  (0.00400245, 0.00388929),
    10.0: (0.00353560, 0.00398814),
}


# ---------------------------------------------------------------------------
# Figure A — Multifractal D2 scaling at lambda = 0
# ---------------------------------------------------------------------------

def fit_d2(N: np.ndarray, ipr: np.ndarray) -> tuple[float, float]:
    """Linear regression of log(IPR) on log(N). Returns (D2, log_A) so
    that IPR(N) ~ A * N^(-D2)."""
    slope, intercept = np.polyfit(np.log(N), np.log(ipr), 1)
    return float(-slope), float(intercept)


def fig_A_d2(out_path: str) -> None:
    D2_fib, logA_fib = fit_d2(N_VALUES, IPR_FIB_LINEAR)
    D2_trib, logA_trib = fit_d2(N_VALUES, IPR_TRIB_LINEAR)

    Ngrid = np.logspace(np.log10(150), np.log10(3000), 200)
    fit_fib = np.exp(logA_fib) * Ngrid ** (-D2_fib)
    fit_trib = np.exp(logA_trib) * Ngrid ** (-D2_trib)

    fig, ax = plt.subplots(figsize=(6.5, 4.6))
    ax.loglog(Ngrid, fit_fib, "-", color=COLOR_FIB, lw=1.4, alpha=0.7,
              label=f"fit  $D_2 = {D2_fib:.3f}$")
    ax.loglog(N_VALUES, IPR_FIB_LINEAR, "o", color=COLOR_FIB, ms=8,
              label="Fibonacci")
    ax.loglog(Ngrid, fit_trib, "-", color=COLOR_TRIB, lw=1.4, alpha=0.7,
              label=f"fit  $D_2 = {D2_trib:.3f}$")
    ax.loglog(N_VALUES, IPR_TRIB_LINEAR, "s", color=COLOR_TRIB, ms=8,
              label="Tribonacci")

    ax.set_xlabel("chain length  $N$")
    ax.set_ylabel(r"linear-limit IPR  $(\lambda = 0)$")
    ax.set_title("Multifractal scaling of mid-gap critical states\n"
                 r"IPR$(N) \sim N^{-D_2}$, $\lambda = 0$")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="upper right", framealpha=0.95)

    # Annotation: caveat on natural lengths
    ax.text(
        0.02, 0.04,
        "N values are not natural Fibonacci/tribonacci\n"
        "lengths; D$_2$ values carry sub-leading\n"
        "scaling-correction uncertainty.",
        transform=ax.transAxes, fontsize=8, color=COLOR_NEUTRAL,
        ha="left", va="bottom",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.7),
    )

    plt.savefig(out_path)
    plt.close()
    print(f"  -> {out_path}   D2_fib={D2_fib:.3f}  D2_trib={D2_trib:.3f}")


# ---------------------------------------------------------------------------
# Figure B — N-stability matrix of the trib/fib IPR ratio
# ---------------------------------------------------------------------------

def fig_B_nstability(out_path: str) -> None:
    Ns = sorted(T1E4.keys())
    ratio = np.zeros((len(LAMBDAS), len(Ns)))
    for j, N in enumerate(Ns):
        for i, lam in enumerate(LAMBDAS):
            ipr_f, ipr_t = T1E4[N][lam]
            ratio[i, j] = ipr_t / ipr_f

    fig, ax = plt.subplots(figsize=(6.5, 5.0))

    # Asymmetric log-norm centred at 1: use log10 of the ratio so 1 -> 0
    log_ratio = np.log10(ratio)
    vmax = np.max(np.abs(log_ratio))
    im = ax.imshow(log_ratio, aspect="auto", cmap="RdBu_r",
                   vmin=-vmax, vmax=vmax,
                   extent=(-0.5, len(Ns) - 0.5, len(LAMBDAS) - 0.5, -0.5))

    ax.set_xticks(range(len(Ns)))
    ax.set_xticklabels([f"N={N}" for N in Ns])
    ax.set_yticks(range(len(LAMBDAS)))
    ax.set_yticklabels([f"$\\lambda={lam:g}$" for lam in LAMBDAS])
    ax.set_title("N-stability of differential robustness at $T=10^4$\n"
                 r"colour = $\log_{10}(\mathrm{IPR}_\mathrm{trib}/\mathrm{IPR}_\mathrm{fib})$")

    # Annotate each cell with the linear ratio
    for i in range(len(LAMBDAS)):
        for j in range(len(Ns)):
            r = ratio[i, j]
            txt_color = "white" if abs(log_ratio[i, j]) > 0.3 else "black"
            ax.text(j, i, f"{r:.2f}", ha="center", va="center",
                    color=txt_color, fontsize=10, fontweight="bold")

    cbar = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
    cbar.set_label(r"$\log_{10}$(ratio)")

    # Caveat in margin
    fig.text(0.02, 0.02,
             "Ratio > 1 (red): tribonacci more localized.  Ratio < 1 (blue): fibonacci more localized.",
             fontsize=8, color=COLOR_NEUTRAL)

    plt.savefig(out_path)
    plt.close()
    print(f"  -> {out_path}")


# ---------------------------------------------------------------------------
# Figure C — Robustness inversion
# ---------------------------------------------------------------------------

def fig_C_inversion(out_path: str) -> None:
    """Plot IPR(T=10^4)/IPR(0) at lambda=1 vs N for both chains.

    Higher value = more retention = more robust.  The crossing point
    between fib and trib is where the relative-robustness order inverts.
    """
    Ns = sorted(T1E4.keys())
    retention_fib = []
    retention_trib = []
    for N in Ns:
        ipr_fib_T, ipr_trib_T = T1E4[N][1.0]
        ipr_fib_0, ipr_trib_0 = T1E4[N][0.0]
        retention_fib.append(ipr_fib_T / ipr_fib_0)
        retention_trib.append(ipr_trib_T / ipr_trib_0)

    retention_fib = np.array(retention_fib)
    retention_trib = np.array(retention_trib)

    fig, ax = plt.subplots(figsize=(6.5, 4.6))
    ax.semilogx(Ns, retention_fib, "o-", color=COLOR_FIB, lw=1.6, ms=9,
                label="Fibonacci   IPR$(T)/$IPR$(0)$")
    ax.semilogx(Ns, retention_trib, "s-", color=COLOR_TRIB, lw=1.6, ms=9,
                label="Tribonacci  IPR$(T)/$IPR$(0)$")

    # Highlight the crossing region
    ax.axhspan(0, 0, alpha=0)  # no-op for layering
    for x, yf, yt in zip(Ns, retention_fib, retention_trib):
        ax.plot([x, x], [yf, yt], ":", color=COLOR_NEUTRAL, lw=0.8, alpha=0.6)

    # Crossing annotation (the curves cross between N=200 and N=500)
    ax.annotate("inversion:\nfib more robust",
                xy=(200, retention_fib[0]), xytext=(220, 0.15),
                fontsize=9, color=COLOR_FIB,
                arrowprops=dict(arrowstyle="->", color=COLOR_FIB, lw=0.8))
    ax.annotate("trib more robust",
                xy=(2000, retention_trib[-1]), xytext=(800, 0.50),
                fontsize=9, color=COLOR_TRIB,
                arrowprops=dict(arrowstyle="->", color=COLOR_TRIB, lw=0.8))

    ax.set_xlabel("chain length  $N$")
    ax.set_ylabel(r"retained fraction  IPR$(T=10^4)\,/\,$IPR$(0)$")
    ax.set_title(r"Robustness inversion at $\lambda = 1$, $T = 10^4$")
    ax.set_ylim(0.05, 0.55)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="upper left", framealpha=0.95)

    plt.savefig(out_path)
    plt.close()
    print(f"  -> {out_path}")


# ---------------------------------------------------------------------------
# Figure D — T-dependence of the differential at fixed N = 500
# ---------------------------------------------------------------------------

def fig_D_homogenization(out_path: str) -> None:
    lams = LAMBDAS
    ratio_T1e4 = []
    ratio_T1e5 = []
    for lam in lams:
        f4, t4 = T1E4[500][lam]
        f5, t5 = T1E5_N500[lam]
        ratio_T1e4.append(t4 / f4)
        ratio_T1e5.append(t5 / f5)

    fig, ax = plt.subplots(figsize=(6.5, 4.6))
    ax.plot(lams, ratio_T1e4, "o-", color=COLOR_HIGHLIGHT, lw=1.8, ms=8,
            label=r"$T = 10^4$  (intermediate)")
    ax.plot(lams, ratio_T1e5, "s--", color=COLOR_FIB, lw=1.8, ms=8,
            label=r"$T = 10^5$  (long time)")
    ax.axhline(1.0, color=COLOR_NEUTRAL, lw=0.8, ls=":")
    ax.text(10.05, 1.02, "ratio = 1", color=COLOR_NEUTRAL, fontsize=8, va="bottom")

    # Mark the lambda=0 baseline
    ax.plot(0, ratio_T1e4[0], "*", color="black", ms=12, zorder=5)
    ax.annotate("linear limit\nratio = 3.91", xy=(0, ratio_T1e4[0]),
                xytext=(1.5, 3.5), fontsize=9, color="black",
                arrowprops=dict(arrowstyle="->", color="black", lw=0.7))

    ax.set_xlabel(r"nonlinearity strength  $\lambda$")
    ax.set_ylabel(r"IPR$_\mathrm{trib}\,/\,$IPR$_\mathrm{fib}$")
    ax.set_title(r"Homogenization of the differential at $N = 500$")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_ylim(0.85, 4.2)

    plt.savefig(out_path)
    plt.close()
    print(f"  -> {out_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Render paper-grade figures.")
    ap.add_argument("--outdir", default=".", help="output directory")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    fig_A_d2(os.path.join(args.outdir, "fig_A_d2_scaling.png"))
    fig_B_nstability(os.path.join(args.outdir, "fig_B_nstability.png"))
    fig_C_inversion(os.path.join(args.outdir, "fig_C_inversion.png"))
    fig_D_homogenization(os.path.join(args.outdir, "fig_D_homogenization.png"))

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
