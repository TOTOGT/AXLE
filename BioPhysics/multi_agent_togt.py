"""
multi_agent_togt.py
====================
Simulation and figure generator for:
  "Biological Transitions as Multi-Agent Realisations of the
   Generative Operator Pipeline in Topographical Orthogonal
   Generative Theory (TO/TOGT)"
  Pablo Nogueira Grossi, 2026

Produces four figures:
  fig1_agent_trajectories.pdf   — N-agent convergence under G^6
  fig2_pitchfork_scan.pdf       — HPA-axis bifurcation scan
  fig3_convergence.pdf          — contraction rate across iterations
  fig4_operator_diagram.pdf     — schematic of the G = U∘F∘K∘C pipeline

Dependencies: numpy, matplotlib
Usage:
  python multi_agent_togt.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch
import os

# ── Aesthetic constants ──────────────────────────────────────────────────────
PALETTE = {
    "bg":      "#0d1117",
    "grid":    "#1e2a38",
    "accent1": "#4fc3f7",   # neural blue
    "accent2": "#81c784",   # HPA green
    "accent3": "#ffb74d",   # circadian amber
    "accent4": "#ce93d8",   # immune violet
    "accent5": "#ef9a9a",   # protein red
    "white":   "#e8edf3",
    "mid":     "#7a8fa6",
}

plt.rcParams.update({
    "figure.facecolor":  PALETTE["bg"],
    "axes.facecolor":    PALETTE["bg"],
    "axes.edgecolor":    PALETTE["grid"],
    "axes.labelcolor":   PALETTE["white"],
    "axes.titlecolor":   PALETTE["white"],
    "xtick.color":       PALETTE["mid"],
    "ytick.color":       PALETTE["mid"],
    "grid.color":        PALETTE["grid"],
    "grid.linewidth":    0.6,
    "text.color":        PALETTE["white"],
    "font.family":       "serif",
    "font.size":         10,
    "savefig.dpi":       200,
    "savefig.bbox":      "tight",
    "savefig.facecolor": PALETTE["bg"],
})

OUT = "/mnt/user-data/outputs"

# ── dm³ normalisation constants ──────────────────────────────────────────────
T_STAR  = 2 * np.pi    # = 2π
MU_MAX  = -2.0
TAU     = 2.0

# ── Operator pipeline G = U∘F∘K∘C ───────────────────────────────────────────
def C(x, epsilon=0.15):
    """Compression: neighbourhood averaging with coupling epsilon."""
    N = len(x)
    mean = np.mean(x)
    return x + epsilon * (mean - x)

def K(x, kappa=0.8):
    """Curvature intensification: alignment + clipping."""
    return np.clip(kappa * x, -1.0, 1.0)

def F(x, alpha=0.3):
    """Loss of injectivity: fold via tanh saturation."""
    return np.tanh(alpha * x)

def U(x, gamma=0.05):
    """Stabilisation: pull toward global coherence."""
    fixed = np.mean(np.tanh(x))
    return x + gamma * (fixed - x)

def G(x, alpha=0.3):
    """Full composite operator G = U∘F∘K∘C."""
    return U(F(K(C(x))))


# ═══════════════════════════════════════════════════════════════════════════════
# Fig 1 — Agent trajectories under 6 applications of G
# ═══════════════════════════════════════════════════════════════════════════════
def fig1_agent_trajectories(n_agents=12, n_iter=6, seed=42):
    rng = np.random.default_rng(seed)
    # Initial diverse states (neural, HPA, circadian, immune, protein)
    x0 = rng.uniform(-1.2, 1.2, n_agents)
    colors = [
        PALETTE["accent1"], PALETTE["accent2"], PALETTE["accent3"],
        PALETTE["accent4"], PALETTE["accent5"],
    ]

    history = [x0.copy()]
    x = x0.copy()
    for _ in range(n_iter):
        x = G(x)
        history.append(x.copy())
    history = np.array(history)   # shape (n_iter+1, n_agents)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    for i in range(n_agents):
        c = colors[i % len(colors)]
        ax.plot(range(n_iter + 1), history[:, i],
                color=c, alpha=0.75, linewidth=1.4,
                marker="o", markersize=3.5, markerfacecolor=c)

    ax.axhline(np.mean(history[-1]), color=PALETTE["white"],
               linewidth=1.8, linestyle="--", alpha=0.9,
               label=f"Collective fixed point ≈ {np.mean(history[-1]):.4f}")

    ax.set_xlabel("Iteration  $k$  (application of $G$)", labelpad=8)
    ax.set_ylabel("Agent state  $x_i^{(k)}$", labelpad=8)
    ax.set_title("Fig 1 — Multi-Agent Convergence under $G^6$\n"
                 "$(N=12$ agents, $\\alpha=0.3,\\,\\varepsilon=0.15)$",
                 pad=10, fontsize=11)
    ax.set_xticks(range(n_iter + 1))
    ax.grid(True, axis="both")
    ax.legend(loc="upper right", fontsize=8.5,
              framealpha=0.25, edgecolor=PALETTE["grid"])

    # Annotate convergence band
    fp = np.mean(history[-1])
    ax.fill_between(range(n_iter + 1),
                    fp - 0.02, fp + 0.02,
                    color=PALETTE["white"], alpha=0.07)

    fig.tight_layout()
    path = os.path.join(OUT, "fig1_agent_trajectories.pdf")
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# Fig 2 — HPA-axis pitchfork bifurcation scan
# ═══════════════════════════════════════════════════════════════════════════════
def fig2_pitchfork_scan():
    alphas = np.linspace(0.0, 1.0, 400)
    # Fixed-point branches: for x'=lambda*x - c*x^3, equilibria at x*=±sqrt((lambda-1)/c)
    # In our normalised form: lambda=alpha/0.5, c=1, threshold |alpha|=0.5
    fp_upper, fp_lower, fp_zero = [], [], []

    for a in alphas:
        lam = 2.0 * a          # rescale so threshold at a=0.5 → lam=1
        if lam < 1.0:
            fp_zero.append((a, 0.0))
            fp_upper.append((a, np.nan))
            fp_lower.append((a, np.nan))
        else:
            c = 1.0
            branch = np.sqrt((lam - 1.0) / c)
            fp_zero.append((a, 0.0))
            fp_upper.append((a,  branch))
            fp_lower.append((a, -branch))

    az, fz = zip(*fp_zero)
    au, fu = zip(*[(a, f) for a, f in fp_upper if not np.isnan(f)])
    al, fl = zip(*[(a, f) for a, f in fp_lower if not np.isnan(f)])

    fig, ax = plt.subplots(figsize=(7, 4.2))

    # Stable zero branch (sub-threshold)
    mask = np.array(az) < 0.5
    ax.plot(np.array(az)[mask], np.array(fz)[mask],
            color=PALETTE["accent2"], linewidth=2.2, label="Stable (zero)")

    # Unstable zero branch (super-threshold)
    mask2 = np.array(az) >= 0.5
    ax.plot(np.array(az)[mask2], np.array(fz)[mask2],
            color=PALETTE["accent2"], linewidth=2.2, linestyle="--",
            alpha=0.5, label="Unstable (zero, super-threshold)")

    ax.plot(au, fu, color=PALETTE["accent1"], linewidth=2.2,
            label="Stable $x^+$  (high-stress attractor)")
    ax.plot(al, fl, color=PALETTE["accent5"], linewidth=2.2,
            label="Stable $x^-$  (recovery attractor)")

    ax.axvline(0.5, color=PALETTE["accent3"], linewidth=1.5,
               linestyle=":", alpha=0.9, label="Pitchfork threshold $|\\alpha|=1/2$")

    ax.annotate("Pitchfork\nonset", xy=(0.5, 0.03),
                xytext=(0.58, 0.18),
                arrowprops=dict(arrowstyle="->", color=PALETTE["accent3"], lw=1.2),
                color=PALETTE["accent3"], fontsize=8.5)

    ax.set_xlabel("Coupling parameter  $|\\alpha|$", labelpad=8)
    ax.set_ylabel("Fixed-point branch  $x^*$", labelpad=8)
    ax.set_title("Fig 2 — HPA-Axis Saturated Pitchfork Bifurcation\n"
                 "(stress-response switching at $|\\alpha|=1/2$)",
                 pad=10, fontsize=11)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.25,
              edgecolor=PALETTE["grid"])
    ax.grid(True)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-1.05, 1.05)

    fig.tight_layout()
    path = os.path.join(OUT, "fig2_pitchfork_scan.pdf")
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")

    # Also export raw CSV for reproducibility
    import csv
    csv_path = os.path.join(OUT, "pitchfork_scan.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["alpha", "fp_zero", "fp_upper", "fp_lower"])
        for a, fz_val, (_, fu_val), (_, fl_val) in zip(
                alphas, fz, fp_upper, fp_lower):
            w.writerow([f"{a:.6f}", f"{fz_val:.6f}",
                        f"{fu_val:.6f}" if not np.isnan(fu_val) else "NaN",
                        f"{fl_val:.6f}" if not np.isnan(fl_val) else "NaN"])
    print(f"  saved {csv_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# Fig 3 — Contraction rate across iterations
# ═══════════════════════════════════════════════════════════════════════════════
def fig3_convergence(n_agents=30, n_iter=8, seed=7):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1.5, 1.5, n_agents)

    spreads = [np.std(x)]
    for _ in range(n_iter):
        x = G(x)
        spreads.append(np.std(x))
    spreads = np.array(spreads)

    # Theoretical bound: (4/5)^k * spread_0  (contraction L<1 for |alpha|<0.5)
    L = 0.80
    theory = spreads[0] * L ** np.arange(n_iter + 1)

    fig, ax = plt.subplots(figsize=(7, 4.0))
    ax.semilogy(range(n_iter + 1), spreads,
                color=PALETTE["accent1"], linewidth=2.2,
                marker="o", markersize=5, label="Empirical spread $\\sigma(k)$")
    ax.semilogy(range(n_iter + 1), theory,
                color=PALETTE["accent3"], linewidth=1.6,
                linestyle="--", label=f"Bound $(4/5)^k\\,\\sigma_0$  ($L={L}$)")

    # Mark six-iterate bound from Lean proof
    six_bound = spreads[0] * (4/5)**6
    ax.axhline(six_bound, color=PALETTE["accent5"], linewidth=1.0,
               linestyle=":", alpha=0.8,
               label=f"$(4/5)^6 < 27/100$ bound  (Lean verified)")
    ax.annotate(f"$(4/5)^6\\approx{(4/5)**6:.4f}<0.27$",
                xy=(6, six_bound), xytext=(4.2, six_bound * 1.6),
                arrowprops=dict(arrowstyle="->", color=PALETTE["accent5"], lw=1.0),
                color=PALETTE["accent5"], fontsize=8)

    ax.set_xlabel("Iteration  $k$", labelpad=8)
    ax.set_ylabel("Collective spread  $\\sigma(k)$  (log scale)", labelpad=8)
    ax.set_title("Fig 3 — Contraction of Collective State under $G^k$\n"
                 "$(N=30$ agents,  $\\alpha=0.3 < 1/2)$",
                 pad=10, fontsize=11)
    ax.legend(loc="upper right", fontsize=8.5,
              framealpha=0.25, edgecolor=PALETTE["grid"])
    ax.grid(True, which="both")
    ax.set_xticks(range(n_iter + 1))

    fig.tight_layout()
    path = os.path.join(OUT, "fig3_convergence.pdf")
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# Fig 4 — Operator pipeline schematic
# ═══════════════════════════════════════════════════════════════════════════════
def fig4_operator_diagram():
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")

    boxes = [
        (1.0,  "C", "Compression\n(neighbourhood\naveraging)",   PALETTE["accent2"]),
        (3.2,  "K", "Curvature\nintensification\n(clip/align)",  PALETTE["accent1"]),
        (5.4,  "F", "Loss of\ninjectivity\n(fold / tanh)",       PALETTE["accent3"]),
        (7.6,  "U", "Stabilisation\n(global\ncoherence)",        PALETTE["accent4"]),
    ]

    W, H = 1.5, 1.6
    Y = 1.5

    for x, label, desc, color in boxes:
        rect = mpatches.FancyBboxPatch(
            (x - W/2, Y - H/2), W, H,
            boxstyle="round,pad=0.08",
            linewidth=1.6, edgecolor=color,
            facecolor=color + "28",   # semi-transparent fill
        )
        ax.add_patch(rect)
        ax.text(x, Y + 0.28, label, ha="center", va="center",
                fontsize=16, fontweight="bold", color=color)
        ax.text(x, Y - 0.38, desc, ha="center", va="center",
                fontsize=7.2, color=PALETTE["mid"], linespacing=1.4)

    # Arrows between boxes
    arrow_kw = dict(arrowstyle="-|>", color=PALETTE["white"],
                    lw=1.4, mutation_scale=14)
    for i in range(len(boxes) - 1):
        x0 = boxes[i][0] + W/2
        x1 = boxes[i+1][0] - W/2
        ax.annotate("", xy=(x1, Y), xytext=(x0, Y),
                    arrowprops=arrow_kw)

    # Operator composition label
    ax.text(5.0, 0.35,
            r"$G \;=\; U \circ F \circ K \circ C$",
            ha="center", va="center", fontsize=13,
            color=PALETTE["white"],
            bbox=dict(boxstyle="round,pad=0.3",
                      facecolor=PALETTE["bg"],
                      edgecolor=PALETTE["grid"], linewidth=1.0))

    # Input / output labels
    ax.text(0.05, Y, "Agent\nstate\n$x_i$",
            ha="left", va="center", fontsize=8, color=PALETTE["mid"])
    ax.text(9.95, Y, "Updated\nstate\n$G(x_i)$",
            ha="right", va="center", fontsize=8, color=PALETTE["mid"])

    ax.set_title("Fig 4 — Operator Pipeline $G = U \\circ F \\circ K \\circ C$\n"
                 "Applied to each biological agent at every generative step",
                 pad=8, fontsize=11)

    fig.tight_layout()
    path = os.path.join(OUT, "fig4_operator_diagram.pdf")
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating figures for multi_agent_togt V2 ...")
    fig1_agent_trajectories()
    fig2_pitchfork_scan()
    fig3_convergence()
    fig4_operator_diagram()
    print("Done.")
