"""
figures.py — Principia Orthogona Volume Two v2
Fully reproducible figure generation for:
  - dm3 toy model phase portrait (r, theta, z)
  - Contact normal form: transverse eigenvalue lambda(z)
  - Threshold crossing: kappa* vs tau equivalence
  - Bifurcation diagram (mu_max vs gamma)
  - Singularity-bifurcation correspondence (Whitney A1-A3)
  - Coherence Bridge parameter table heatmap
  - Stability radius epsilon_0 derivation

Author: Pablo Nogueira Grossi (G6 LLC, Newark NJ)
ORCID: 0009-0000-6496-2186
Series: Principia Orthogona, Volume Two
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.colors import LinearSegmentedColormap
from scipy.integrate import solve_ivp
from scipy.linalg import eigvals
import warnings
warnings.filterwarnings("ignore")

# ── Aesthetic constants ────────────────────────────────────────────────────────
NAVY   = "#0a1628"
GOLD   = "#c9a84c"
CREAM  = "#f5f0e8"
TEAL   = "#2a7f7f"
ROSE   = "#c0392b"
GRAY   = "#8a9bb0"
WHITE  = "#ffffff"

plt.rcParams.update({
    "figure.facecolor": NAVY,
    "axes.facecolor":   NAVY,
    "axes.edgecolor":   GOLD,
    "axes.labelcolor":  CREAM,
    "text.color":       CREAM,
    "xtick.color":      CREAM,
    "ytick.color":      CREAM,
    "grid.color":       "#1e3050",
    "grid.linewidth":   0.5,
    "font.family":      "DejaVu Serif",
    "font.size":        10,
    "axes.titlesize":   12,
    "axes.titlecolor":  GOLD,
    "lines.linewidth":  1.8,
})

OUT = "/home/claude/principia_v2/figs/"
import os; os.makedirs(OUT, exist_ok=True)

# ── 1. dm3 Toy Model Phase Portrait ───────────────────────────────────────────
def dm3_rhs(t, state, sigma=0.0):
    """
    Equations (4.1)-(4.3):
      r_dot = r(1 - r^2) + 2(r-1)e^{-z}
      theta_dot = 1
      z_dot = r^2 - 2(r-1)^2 e^{-z}
    """
    r, th, z = state
    ez = np.exp(-z)
    r_dot  = r*(1 - r**2) + 2*(r - 1)*ez
    th_dot = 1.0
    z_dot  = r**2 - 2*(r - 1)**2 * ez
    return [r_dot, th_dot, z_dot]

def fig_phase_portrait():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Figure 1 — dm³ Toy Model: Phase Portrait & Contact Variable",
                 color=GOLD, fontsize=13, y=1.01)

    # Left: (r, z) projection
    ax = axes[0]
    ax.set_title("(r, z) projection — Eq. (4.1)/(4.3)")
    ax.set_xlabel("r")
    ax.set_ylabel("z")
    ax.grid(True)

    t_span = (0, 80)
    t_eval = np.linspace(*t_span, 8000)
    initial_conditions = [
        [0.3, 0, 0.01], [0.6, 0, 0.1], [1.5, 0, 0.1],
        [0.1, 0, 0.5],  [2.0, 0, 0.2],
    ]
    colors = [GOLD, TEAL, ROSE, CREAM, GRAY]

    for ic, col in zip(initial_conditions, colors):
        sol = solve_ivp(dm3_rhs, t_span, ic, t_eval=t_eval,
                        method="RK45", rtol=1e-8, atol=1e-10)
        ax.plot(sol.y[0], sol.y[2], color=col, alpha=0.7, lw=1.2)
        ax.plot(ic[0], ic[2], "o", color=col, ms=5)

    # Mark limit cycle Gamma = {r=1}
    ax.axvline(x=1.0, color=GOLD, lw=2.5, ls="--", label=r"$\Gamma$ : $r=1$")
    ax.set_xlim(0, 2.2)
    ax.set_ylim(-0.5, 12)
    ax.legend(loc="upper right", facecolor=NAVY, edgecolor=GOLD)
    ax.text(1.05, 0.3, r"$\Gamma_{12}$", color=GOLD, fontsize=13)

    # Right: transverse eigenvalue lambda(z) — Prop. 4.2
    ax2 = axes[1]
    ax2.set_title(r"Transverse eigenvalue $\lambda(z) = -2(1-e^{-z})$ — Prop. 4.2")
    ax2.set_xlabel("z  (contact variable)")
    ax2.set_ylabel(r"$\lambda(z)$")
    ax2.grid(True)

    z_vals = np.linspace(0, 8, 500)
    lam    = -2*(1 - np.exp(-z_vals))

    ax2.plot(z_vals, lam, color=GOLD, lw=2)
    ax2.axhline(y=0,  color=GRAY,  lw=1, ls="--")
    ax2.axhline(y=-2, color=ROSE,  lw=1.5, ls=":", label=r"$\mu_{\max}=-2$ (full dm³ rate)")
    ax2.axvline(x=0,  color=TEAL,  lw=1.5, ls=":", label=r"$z=0$: embodiment threshold")
    ax2.fill_between(z_vals, lam, 0, where=(z_vals>0), color=TEAL, alpha=0.12,
                     label="attracting region")

    ax2.annotate(r"$\lambda(0)=0$"+"\nneutral (pre-embodiment)",
                 xy=(0,0), xytext=(1.5, 0.3),
                 arrowprops=dict(arrowstyle="->", color=CREAM),
                 color=CREAM, fontsize=9)
    ax2.annotate(r"$\lambda(z)\to -2$"+"\n(post-embodiment)",
                 xy=(7,-1.94), xytext=(4.5,-1.6),
                 arrowprops=dict(arrowstyle="->", color=CREAM),
                 color=CREAM, fontsize=9)

    ax2.legend(loc="lower right", facecolor=NAVY, edgecolor=GOLD, fontsize=8)
    ax2.set_xlim(-0.3, 8)
    ax2.set_ylim(-2.3, 0.5)

    fig.tight_layout()
    path = OUT + "fig1_phase_portrait.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close(fig)
    print(f"  Saved: {path}")

# ── 2. Threshold Equivalence: kappa* ↔ tau ────────────────────────────────────
def fig_threshold_equivalence():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    fig.suptitle(
        r"Figure 2 — Theorem B: $\kappa^* \Leftrightarrow \mu_{\max}<0 \Leftrightarrow \tau\in(0,\infty)$",
        color=GOLD, fontsize=13)

    # (a) kappa accumulation
    ax = axes[0]
    ax.set_title(r"(a) Curvature accumulation $|\kappa|\uparrow\kappa^*$")
    ax.set_xlabel("arc length s")
    ax.set_ylabel(r"$|\kappa(s)|$")
    ax.grid(True)

    s    = np.linspace(0, 10, 500)
    kap  = 1.0 * (1 - np.exp(-0.6*s))  # approaches kappa*=1
    ax.plot(s, kap, color=GOLD, lw=2)
    ax.axhline(y=1.0, color=ROSE, lw=2, ls="--", label=r"$\kappa^*=1$")
    ax.fill_between(s, kap, 1.0, where=(kap<1), alpha=0.15, color=TEAL)
    ax.legend(facecolor=NAVY, edgecolor=GOLD)
    ax.set_ylim(0, 1.3)

    # (b) mu_max sign change
    ax2 = axes[1]
    ax2.set_title(r"(b) Floquet exponent $\mu_{\max}$ vs $\gamma$")
    ax2.set_xlabel(r"dissipation $\gamma$")
    ax2.set_ylabel(r"$\mu_{\max}$")
    ax2.grid(True)

    gamma    = np.linspace(0, 3, 400)
    mu_max   = -0.8*gamma + 0.5   # schematic: crosses 0 at gamma*
    gamma_st = 0.5/0.8
    ax2.plot(gamma, mu_max, color=GOLD, lw=2)
    ax2.axhline(0, color=GRAY, lw=1, ls="--")
    ax2.axvline(gamma_st, color=TEAL, lw=1.5, ls=":", label=rf"$\gamma^*={gamma_st:.2f}$")
    ax2.fill_between(gamma, mu_max, 0, where=(mu_max<0), alpha=0.18, color=ROSE,
                     label=r"$\mu_{\max}<0$: stable")
    ax2.fill_between(gamma, mu_max, 0, where=(mu_max>0), alpha=0.18, color=TEAL,
                     label=r"$\mu_{\max}>0$: unstable")
    ax2.legend(facecolor=NAVY, edgecolor=GOLD, fontsize=8)

    # (c) tau = sqrt(c/kappa_noise)
    ax3 = axes[2]
    ax3.set_title(r"(c) Stochastic threshold $\tau=\sqrt{c/\kappa_{\rm noise}}$")
    ax3.set_xlabel(r"$c$ (contraction rate)")
    ax3.set_ylabel(r"$\tau$")
    ax3.grid(True)

    c_vals   = np.linspace(0.01, 5, 400)
    for kn, col, lab in [(0.25, GOLD, r"$\kappa_{\rm noise}=0.25$"),
                          (1.0,  TEAL, r"$\kappa_{\rm noise}=1$"),
                          (4.0,  ROSE, r"$\kappa_{\rm noise}=4$")]:
        tau = np.sqrt(c_vals / kn)
        ax3.plot(c_vals, tau, color=col, lw=2, label=lab)

    # Mark toy model: c=4, kappa_noise=1, tau=2
    ax3.plot(4, 2, "*", color=WHITE, ms=14, zorder=5,
             label=r"dm³ toy: $\tau=2$")
    ax3.legend(facecolor=NAVY, edgecolor=GOLD, fontsize=8)
    ax3.set_ylim(0, 5)

    fig.tight_layout()
    path = OUT + "fig2_threshold_equivalence.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close(fig)
    print(f"  Saved: {path}")

# ── 3. Bifurcation Diagram ────────────────────────────────────────────────────
def fig_bifurcation():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_title("Figure 3 — dm³ Bifurcation Diagram: Four Bifurcations / Whitney A1–A3",
                 fontsize=12)
    ax.set_xlabel(r"Control parameter $\gamma / e^{z_0}$")
    ax.set_ylabel(r"Orbit radius $r^*$")
    ax.grid(True)

    # Schematic stable branch
    lam = np.linspace(0, 4, 1000)

    # Contact Hopf bifurcation at lam=1
    stable_1   = np.where(lam < 1.0, 1.0, 1.0 + 0.9*np.sqrt(np.maximum(lam-1, 0)))
    unstable_1 = np.where(lam < 1.0, 1.0, 1.0 - 0.9*np.sqrt(np.maximum(lam-1, 0)))

    ax.plot(lam, stable_1,   color=GOLD, lw=2.5, label="stable limit cycle")
    ax.plot(lam, unstable_1, color=ROSE, lw=2, ls="--", label="unstable branch")

    # Saddle-node at lam≈2.5: two branches merge
    sn = 2.5
    sn_idx = np.searchsorted(lam, sn)
    ax.plot([sn, sn], [stable_1[sn_idx], unstable_1[sn_idx]],
            color=TEAL, lw=3, label="saddle-node (A1)")

    # Neimark-Sacker at lam≈1.8: torus birth
    ns = 1.8
    ax.axvline(ns, color=CREAM, lw=1.5, ls=":", alpha=0.7)
    ax.text(ns+0.05, 2.05, "Neimark–Säcker\n(A2 cusp)", color=CREAM, fontsize=8.5)

    # Slow-fast crossover at lam≈3.3
    sf = 3.3
    ax.axvline(sf, color=GRAY, lw=1.5, ls=":", alpha=0.7)
    ax.text(sf+0.05, 0.55, "Slow-fast\ncrossover (A3)", color=GRAY, fontsize=8.5)

    # Contact Hopf annotation
    ax.annotate("Contact Hopf (A1)\n"+r"$\gamma = e^{z_0}$",
                xy=(1.0, 1.0), xytext=(1.3, 0.5),
                arrowprops=dict(arrowstyle="->", color=GOLD),
                color=GOLD, fontsize=9)

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2.5)
    ax.legend(loc="upper left", facecolor=NAVY, edgecolor=GOLD)

    # Whitney table inset
    table_data = [
        ["A1 (fold)",        "0", "Contact Hopf + saddle-node"],
        ["A2 (cusp)",        "1", "Neimark–Säcker"],
        ["A3 (swallowtail)", "2", "Slow-fast crossover"],
    ]
    col_labels = ["Singularity", "Codim", "dm³ bifurcation"]
    table = ax.table(cellText=table_data, colLabels=col_labels,
                     loc="upper right", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    for (r, c), cell in table.get_celld().items():
        cell.set_facecolor("#0f2035" if r > 0 else "#1a3a5c")
        cell.set_edgecolor(GOLD)
        cell.set_text_props(color=CREAM if r > 0 else GOLD)
    table.scale(1, 1.4)

    fig.tight_layout()
    path = OUT + "fig3_bifurcation.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close(fig)
    print(f"  Saved: {path}")

# ── 4. Stability Radius ε₀ = 1/3 ─────────────────────────────────────────────
def fig_stability_radius():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle(r"Figure 4 — Stability Radius $\varepsilon_0 = \frac{|\mu_{\max}|}{2(1+\sup\|\mathrm{Hess}\,V\|)} = \frac{1}{3}$",
                 color=GOLD, fontsize=12)

    # Left: Fokker-Planck stationary measure vs sigma
    ax = axes[0]
    ax.set_title(r"Fokker–Planck measure: $\sigma < \tau$ vs $\sigma > \tau$")
    ax.set_xlabel(r"$\rho = r - 1$ (transverse coord.)")
    ax.set_ylabel("probability density")
    ax.grid(True)

    rho  = np.linspace(-1.5, 1.5, 500)
    tau  = 2.0

    for sigma, col, lab in [(0.5, GOLD,  r"$\sigma=0.5 < \tau=2$ (concentrated)"),
                             (2.0, TEAL,  r"$\sigma=2 = \tau$ (critical)"),
                             (4.0, ROSE,  r"$\sigma=4 > \tau$ (spreading)")]:
        # Gaussian approximation of stationary Fokker-Planck on Gamma
        var = sigma**2 / (4*(1 + (sigma/tau)**2))
        pdf = np.exp(-rho**2 / (2*var)) / np.sqrt(2*np.pi*var)
        ax.plot(rho, pdf, color=col, lw=2, label=lab)

    ax.axvline(0, color=WHITE, lw=1, ls="--", alpha=0.5, label=r"$\Gamma: \rho=0$")
    ax.legend(facecolor=NAVY, edgecolor=GOLD, fontsize=7.5)

    # Right: epsilon_0 as function of mu_max (with Hess norm=2 fixed)
    ax2 = axes[1]
    ax2.set_title(r"$\varepsilon_0$ vs $|\mu_{\max}|$ (Hess$\,V$ norm = 2)")
    ax2.set_xlabel(r"$|\mu_{\max}|$")
    ax2.set_ylabel(r"$\varepsilon_0$")
    ax2.grid(True)

    mu_abs = np.linspace(0.1, 5, 300)
    eps0   = mu_abs / (2*(1 + 2))   # sup Hess = 2

    ax2.plot(mu_abs, eps0, color=GOLD, lw=2.5)
    ax2.plot(2.0, 1/3, "o", color=ROSE, ms=10, zorder=5,
             label=r"dm³ toy: $\varepsilon_0 = 1/3$")
    ax2.axhline(1/3, color=ROSE, lw=1, ls="--", alpha=0.7)
    ax2.axvline(2.0, color=ROSE, lw=1, ls="--", alpha=0.7)
    ax2.legend(facecolor=NAVY, edgecolor=GOLD)
    ax2.set_ylim(0, 0.7)

    fig.tight_layout()
    path = OUT + "fig4_stability_radius.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close(fig)
    print(f"  Saved: {path}")

# ── 5. Coherence Bridge — Parameter Heatmap ───────────────────────────────────
def fig_coherence_bridge():
    domains = [
        "HPA stress",
        "Neural osc.",
        "Circadian",
        "Immune adapt.",
        "Plasma recon.",
        "Market vol.",
    ]
    # (mu_max, omega, beta, kappa_star_mid)
    params = np.array([
        [-0.38,  0.21,    1.9,  0.185],
        [-0.55,  0.45,    2.1,  0.300],
        [-0.29,  7.27e-5, 1.6,  0.100],
        [-0.44,  0.18,    2.0,  0.150],
        [-0.42,  0.015,   1.8,  0.001],
        [-0.67,  0.28,    2.4,  0.150],
    ])
    col_labels = [r"$\mu_{\max}$", r"$\omega$", r"$\beta$", r"$\kappa^*$ (mid)"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title("Figure 5 — Coherence Bridge: dm³ Parameters Across Six Domains",
                 fontsize=12)

    # Normalize each column for color
    norm_params = (params - params.min(0)) / (params.max(0) - params.min(0) + 1e-12)

    # Custom colormap: navy → gold
    cmap = LinearSegmentedColormap.from_list("PO", [NAVY, "#1e5080", TEAL, GOLD])

    im = ax.imshow(norm_params.T, cmap=cmap, aspect="auto", vmin=0, vmax=1)

    ax.set_xticks(range(len(domains)))
    ax.set_xticklabels(domains, rotation=25, ha="right", fontsize=9.5)
    ax.set_yticks(range(len(col_labels)))
    ax.set_yticklabels(col_labels, fontsize=11)

    # Annotate with actual values
    for i, domain in enumerate(domains):
        for j, label in enumerate(col_labels):
            val = params[i, j]
            txt = f"{val:.3f}" if abs(val) > 0.001 else f"{val:.2e}"
            ax.text(i, j, txt, ha="center", va="center",
                    color=NAVY if norm_params[i,j] > 0.5 else CREAM,
                    fontsize=8.5, fontweight="bold")

    # Row separator line
    for j in range(len(col_labels)+1):
        ax.axhline(j-0.5, color=NAVY, lw=1)
    for i in range(len(domains)+1):
        ax.axvline(i-0.5, color=NAVY, lw=1)

    cbar = fig.colorbar(im, ax=ax, orientation="vertical", pad=0.02)
    cbar.set_label("normalized value", color=CREAM)
    cbar.ax.yaxis.set_tick_params(color=CREAM)

    ax.set_xlabel("Domain", labelpad=8)
    fig.text(0.5, -0.04,
             "All six systems share the contact normal form  "
             r"$\dot\rho = \mu_{\max}(1-e^{-\beta z})\rho,\;\dot\theta=\omega$  "
             "— Coherence Bridge Theorem 5.4",
             ha="center", color=GOLD, fontsize=9)

    fig.tight_layout()
    path = OUT + "fig5_coherence_bridge.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close(fig)
    print(f"  Saved: {path}")

# ── 6. Operator Sequence Diagram ──────────────────────────────────────────────
def fig_operator_sequence():
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.axis("off")
    ax.set_title("Figure 6 — Operator Sequence G = U ∘ F ∘ K ∘ C and Contact Extension",
                 fontsize=12)

    ops = [
        ("C", "Compression\n" + r"$X \to X_C$" + "\nreduces DOF",    1.0),
        ("K", "Curvature\n"   + r"$|\kappa|\uparrow\kappa^*$" + "\ndrive",  3.5),
        ("F", "Fold\n"        + r"$\mathrm{rank}(J)\downarrow 1$" + "\nWhitney A1", 6.0),
        ("U", "Unfolding\n"   + r"$\nabla\Phi$-flow" + "\nnew topology",   8.5),
        ("Hdiss", "Contact\ndissipation\n" + r"$H_{\rm diss}=-\gamma V e^{-\beta z}$", 11.0),
    ]
    box_colors = [TEAL, TEAL, ROSE, TEAL, GOLD]

    for (label, desc, x), col in zip(ops, box_colors):
        # Box
        rect = Rectangle((x-0.75, 0.6), 1.5, 1.8,
                          linewidth=2, edgecolor=col,
                          facecolor="#0f2035", zorder=3)
        ax.add_patch(rect)
        ax.text(x, 1.85, label, ha="center", va="center",
                fontsize=16, color=col, fontweight="bold", zorder=4)
        ax.text(x, 1.1, desc, ha="center", va="center",
                fontsize=7.5, color=CREAM, zorder=4, linespacing=1.4)

        # Arrows between boxes
        if x < 11.0:
            next_x = ops[ops.index((label, desc, x))+1][2]
            ax.annotate("", xy=(next_x-0.75, 1.5), xytext=(x+0.75, 1.5),
                        arrowprops=dict(arrowstyle="-|>", color=GOLD,
                                        lw=2, mutation_scale=15))

    # Label under fold: "Vol I → Vol II bridge"
    ax.text(6.0, 0.35, "← Volume One (geometric) | Volume Two (contact) →",
            ha="center", va="center", color=GRAY, fontsize=8.5, style="italic")
    ax.axvline(7.2, color=GRAY, lw=1.5, ls="--", ymin=0.15, ymax=0.85)

    # Bottom note
    ax.text(6.0, 0.05,
            r"$G = U \circ F \circ K \circ C$ (symplectic, Vol. I)  →  "
            r"$H_{\rm diss}$ regularizes $S(\gamma)$ in contact extension $M=X\times\mathbb{R}$  (Prop. 2.1)",
            ha="center", va="bottom", color=GOLD, fontsize=8)

    fig.tight_layout()
    path = OUT + "fig6_operator_sequence.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close(fig)
    print(f"  Saved: {path}")

# ── 7. Contact Normal Form 3D trajectory ──────────────────────────────────────
def fig_contact_3d():
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(8, 7))
    ax  = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(NAVY)
    fig.patch.set_facecolor(NAVY)
    ax.set_title("Figure 7 — dm³ Toy Model: 3D Contact Manifold\n"
                 r"$M = \mathbb{R}^2_{>0}\times\mathbb{R}$, contact form $\alpha = dz - r^2 d\theta$",
                 color=GOLD, fontsize=11)

    t_span = (0, 60)
    t_eval = np.linspace(*t_span, 6000)

    for ic, col, lw in [([0.3, 0, 0.01], GRAY,  1.0),
                         ([0.7, 0, 0.1],  TEAL,  1.2),
                         ([1.5, 0, 0.2],  CREAM, 1.0),
                         ([1.0, 0, 0.0],  GOLD,  2.5)]:   # limit cycle seed
        sol = solve_ivp(dm3_rhs, t_span, ic, t_eval=t_eval,
                        method="RK45", rtol=1e-9, atol=1e-11)
        r, th, z = sol.y
        x_c = r * np.cos(th)
        y_c = r * np.sin(th)
        ax.plot(x_c, y_c, z, color=col, lw=lw, alpha=0.85)

    # Draw Gamma in red
    th_lc = np.linspace(0, 4*np.pi, 200)
    ax.plot(np.cos(th_lc), np.sin(th_lc), np.zeros_like(th_lc)+0.01,
            color=ROSE, lw=3, label=r"$\Gamma_{12}$ ($r=1$)")

    ax.set_xlabel("x", color=CREAM, labelpad=4)
    ax.set_ylabel("y", color=CREAM, labelpad=4)
    ax.set_zlabel("z (contact)", color=CREAM, labelpad=4)
    ax.tick_params(colors=CREAM)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.legend(facecolor=NAVY, edgecolor=GOLD)

    path = OUT + "fig7_contact_3d.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close(fig)
    print(f"  Saved: {path}")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Principia Orthogona Vol. II — Figure Generation")
    print("=" * 50)
    fig_phase_portrait()
    fig_threshold_equivalence()
    fig_bifurcation()
    fig_stability_radius()
    fig_coherence_bridge()
    fig_operator_sequence()
    fig_contact_3d()
    print("=" * 50)
    print(f"All figures written to: {OUT}")
    print("Figures: fig1–fig7")
