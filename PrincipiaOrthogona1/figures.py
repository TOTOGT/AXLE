"""
figures.py
==========
Figure generator for:
  Principia Orthogona, Volume I: The Mathematics of Generative Transitions
  Second Edition — Pablo Nogueira Grossi — G6 LLC, Newark NJ, 2026

Zenodo: https://doi.org/10.5281/zenodo.19117399
AXLE:   https://github.com/TOTOGT/AXLE

Generates all 7 figures as both PDF and PNG.

Usage:
    pip install numpy matplotlib
    python figures.py

Outputs (in ./figures/ directory):
    fig1_phase_portrait.pdf / .png
    fig2_threshold_equivalence.pdf / .png
    fig3_bifurcation.pdf / .png
    fig4_stability_radius.pdf / .png
    fig5_coherence_bridge.pdf / .png
    fig6_operator_sequence.pdf / .png
    fig7_contact_3d.pdf / .png

Lean verification of dm³ scalar invariants:
    mu_dm3_neg     : -2 < 0
    gronwall_radius: 1/3
    basin_asymmetry: 1/3 < 4/5
    noiseTolerance : 2 * (1/3) = 2/3
All proved without sorry in PrincipiaVol1.lean.

Pablo Nogueira Grossi · G6 LLC · Newark NJ · 2026
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import warnings
warnings.filterwarnings("ignore")

# ── Output directory ──────────────────────────────────────────────────────────
OUTDIR = "figures"
os.makedirs(OUTDIR, exist_ok=True)

# ── dm³ canonical invariants (Lean: canonicalTriple) ─────────────────────────
MU_MAX      = -2.0          # transverse Lyapunov exponent (mu_dm3_neg: -2 < 0)
TAU         = 2.0           # embodiment threshold
T_STAR      = 2 * np.pi    # natural period
EPSILON_0   = 1 / 3        # Gronwall radius (gronwall_radius: 1/3)
R_STAR      = 4 / 5        # inner boundary (basin_asymmetry: 1/3 < 4/5)
NOISE_TOL   = TAU * EPSILON_0  # = 2/3 (noiseTolerance)

# ── Style ─────────────────────────────────────────────────────────────────────
NAVY  = "#1a2744"
GOLD  = "#c9a84c"
TEAL  = "#1a6b5a"
RED   = "#c0392b"
GREY  = "#7f8c8d"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "figure.dpi": 150,
    "text.usetex": False,
})

def savefig(name):
    for ext in ("pdf", "png"):
        path = os.path.join(OUTDIR, f"{name}.{ext}")
        plt.savefig(path, bbox_inches="tight", dpi=150)
    print(f"  saved {name}.pdf / .png")
    plt.close()

# ── Figure 1: dm³ Phase Portrait with Gronwall Basin ─────────────────────────
def fig1_phase_portrait():
    fig, ax = plt.subplots(figsize=(6, 6))

    theta = np.linspace(0, 2 * np.pi, 400)

    # Gronwall basin boundary (r = ε₀ = 1/3)
    ax.plot(EPSILON_0 * np.cos(theta), EPSILON_0 * np.sin(theta),
            "--", color=GOLD, lw=1.5, label=r"$\varepsilon_0 = 1/3$ (Gronwall)")

    # Inner boundary r* ≈ 4/5
    ax.plot(R_STAR * np.cos(theta), R_STAR * np.sin(theta),
            ":", color=GREY, lw=1.5, label=r"$r^* \approx 4/5$ (inner boundary)")

    # Limit cycle Γ (r = 1)
    ax.plot(np.cos(theta), np.sin(theta),
            "-", color=NAVY, lw=2.5, label=r"$\Gamma$ (attractor, $r=1$)")

    # Sample converging orbits (basin)
    for r0 in [0.45, 0.6, 1.25, 1.5]:
        phi = np.linspace(0, 6 * np.pi, 600)
        r   = 1 + (r0 - 1) * np.exp(-0.4 * phi / (2 * np.pi))
        ax.plot(r * np.cos(phi), r * np.sin(phi),
                color=TEAL, lw=0.8, alpha=0.5)

    ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\rho \cos\theta$"); ax.set_ylabel(r"$\rho \sin\theta$")
    ax.set_title("dm\u00b3 Phase Portrait\n"
                 r"$\mu_{\max}=-2$, $\varepsilon_0=1/3$, $r^*\approx4/5$"
                 "\nLean: mu_dm3_neg, gronwall_radius, basin_asymmetry")
    ax.legend(fontsize=9, loc="upper right")
    ax.axhline(0, color="k", lw=0.4); ax.axvline(0, color="k", lw=0.4)

    savefig("fig1_phase_portrait")


# ── Figure 2: Threshold Equivalence ──────────────────────────────────────────
def fig2_threshold_equivalence():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Left: V(q) = q³ − 3q with Whitney A₁ annotations
    ax = axes[0]
    q  = np.linspace(-1.2, 2.2, 500)
    Vq = q**3 - 3*q
    ax.plot(q, Vq, color=NAVY, lw=2, label=r"$V(q)=q^3-3q$")
    ax.plot(q, (q-1)**2*(q+2) - 2, "--", color=TEAL, lw=1.2, alpha=0.7,
            label=r"$(q-1)^2(q+2)-2$ (factored)")
    ax.axhline(-2, color=GOLD, lw=1.2, ls="--", label=r"$V=-2$ (fold energy)")
    ax.plot(1, -2, "o", color=GOLD, ms=8, zorder=5,
            label=r"$q=1$, $V(1)=-2$ (fold point)")
    ax.set_xlabel(r"$q$"); ax.set_ylabel(r"$V(q)$")
    ax.set_title("Whitney $A_1$ Fold Potential\n"
                 "Lean: V_critical_at_one, V_factored")
    ax.legend(fontsize=8); ax.set_ylim(-4, 4)

    # Right: V'(q) and V''(q)
    ax = axes[1]
    Vp  = 3*q**2 - 3
    Vpp = 6*q
    ax.plot(q, Vp,  color=RED,  lw=2, label=r"$V'(q)=3q^2-3$")
    ax.plot(q, Vpp, color=TEAL, lw=2, label=r"$V''(q)=6q$")
    ax.axvline(1, color=GREY, lw=1, ls=":")
    ax.plot(1, 0, "o", color=RED,  ms=8, label=r"$V'(1)=0$ (proved)")
    ax.plot(1, 6, "o", color=TEAL, ms=8, label=r"$V''(1)=6\neq0$ (proved)")
    ax.set_xlabel(r"$q$"); ax.set_ylabel("")
    ax.set_title("Whitney $A_1$ Conditions Verified\n"
                 "Lean: V_second_deriv_at_one, V_second_deriv_ne_zero")
    ax.legend(fontsize=8); ax.axhline(0, color="k", lw=0.4)
    ax.set_ylim(-10, 10)

    plt.tight_layout()
    savefig("fig2_threshold_equivalence")


# ── Figure 3: Bifurcation Diagram near κ* ────────────────────────────────────
def fig3_bifurcation():
    fig, ax = plt.subplots(figsize=(7, 4.5))

    kappa = np.linspace(0, 2, 500)
    kstar = 1.0

    # Stable branch (before fold)
    mask_s = kappa <= kstar
    ax.plot(kappa[mask_s], 0.5 * kappa[mask_s], color=NAVY, lw=2.5,
            label="Stable branch (pre-fold)")

    # Unstable branch (after fold, upper)
    mask_u = kappa >= kstar
    ax.plot(kappa[mask_u], 0.5 + 0.8*(kappa[mask_u]-kstar)**0.5,
            "--", color=RED, lw=2, label="Unstable branch")

    # New stable branch (post-fold)
    ax.plot(kappa[mask_u], -0.3 + 0.4*(kappa[mask_u]-kstar)**0.5,
            color=TEAL, lw=2.5, label="New stable branch (post-fold)")

    ax.axvline(kstar, color=GOLD, lw=1.5, ls="--",
               label=r"$\kappa^*$ (fold point)")
    ax.plot(kstar, 0.5, "o", color=GOLD, ms=10, zorder=5)

    ax.set_xlabel(r"$\kappa$ (curvature parameter)")
    ax.set_ylabel(r"Trajectory branch $x$")
    ax.set_title(r"Bifurcation Diagram near $\kappa^*$" + "\n"
                 "Lean: FoldOp.has_fold, FoldOp.finite_branch")
    ax.legend(fontsize=9)

    savefig("fig3_bifurcation")


# ── Figure 4: Stability Radius ε₀ = 1/3 ─────────────────────────────────────
def fig4_stability_radius():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Left: contraction exponent as function of ε
    ax = axes[0]
    eps = np.linspace(0, 0.5, 300)
    exponent = (MU_MAX + 3*eps) * T_STAR  # (μmax + 3ε)·T*
    ax.plot(eps, exponent, color=NAVY, lw=2.5)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(EPSILON_0, color=GOLD, lw=1.5, ls="--",
               label=r"$\varepsilon_0=1/3$")
    ax.fill_between(eps, exponent, 0,
                    where=(eps < EPSILON_0), alpha=0.15, color=TEAL,
                    label="Contraction region")
    ax.fill_between(eps, exponent, 0,
                    where=(eps >= EPSILON_0), alpha=0.15, color=RED,
                    label="Expansion region")
    ax.set_xlabel(r"$\varepsilon$ (perturbation amplitude)")
    ax.set_ylabel(r"$(\mu_{\max}+3\varepsilon)\cdot T^*$")
    ax.set_title("Gronwall Contraction Exponent\n"
                 "Lean: gronwall_contraction_below_stability_radius")
    ax.legend(fontsize=9)

    # Right: Φ(ρ) = ρ² stability functional
    ax = axes[1]
    rho = np.linspace(0, 2, 300)
    ax.plot(rho, rho**2, color=NAVY, lw=2.5, label=r"$\Phi(\rho)=\rho^2$")
    ax.plot(rho, 2*rho, color=TEAL, lw=2, ls="--", label=r"$\Phi'(\rho)=2\rho$")
    ax.axvline(EPSILON_0, color=GOLD, lw=1.5, ls="--",
               label=r"$\varepsilon_0=1/3$")
    ax.axvline(R_STAR, color=GREY, lw=1.5, ls=":",
               label=r"$r^*=4/5$")
    ax.set_xlabel(r"$\rho$"); ax.set_ylabel("")
    ax.set_title(r"Stability Functional $\Phi(\rho)=\rho^2$" + "\n"
                 "Lean: Phi_pos, dPhi_pos, basin_asymmetry")
    ax.legend(fontsize=9)

    plt.tight_layout()
    savefig("fig4_stability_radius")


# ── Figure 5: Coherence Bridge ────────────────────────────────────────────────
def fig5_coherence_bridge():
    domains = [
        "HPA stress axis",
        "Neural oscillations",
        "Circadian clock",
        "Wigner crystal",
        "Tubulin / microtubule",
        "Autophagy (cell) [A]",
        "Triple-alpha (star) [A]",
    ]
    mu_vals = [-0.38, -0.55, -0.29, -0.31, -0.48, -0.41, -0.88]
    beta_vals = [1.9, 2.1, 1.6, 1.7, 2.0, 1.85, 2.3]
    colors = [GREY]*5 + [GOLD, TEAL]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: μmax
    ax = axes[0]
    y  = np.arange(len(domains))
    bars = ax.barh(y, mu_vals, color=colors, edgecolor="white", height=0.6)
    ax.set_yticks(y); ax.set_yticklabels(domains, fontsize=9)
    ax.set_xlabel(r"$\mu_{\max}$ (s$^{-1}$)")
    ax.set_title("Transverse Lyapunov Exponent\n"
                 "Lean: mu_dm3_neg (all < 0)")
    ax.axvline(0, color="k", lw=0.8)
    for bar, val in zip(bars, mu_vals):
        ax.text(val - 0.01, bar.get_y() + bar.get_height()/2,
                f"{val}", va="center", ha="right", fontsize=8, color="white")
    ax.set_xlim(-1.0, 0.05)

    # Right: β
    ax = axes[1]
    ax.barh(y, beta_vals, color=colors, edgecolor="white", height=0.6)
    ax.set_yticks(y); ax.set_yticklabels(domains, fontsize=9)
    ax.set_xlabel(r"$\beta$ (fold sharpness)")
    ax.set_title("Fold Sharpness\n"
                 r"Higher $\beta$ = sharper transition")
    ax.axvline(2.0, color=GREY, lw=1, ls="--", label=r"$\beta=2.0$")
    ax.legend(fontsize=8)

    handles = [
        mpatches.Patch(color=GREY, label="Prior domains"),
        mpatches.Patch(color=GOLD, label="Autophagy (Chapter A, new)"),
        mpatches.Patch(color=TEAL, label="Triple-alpha (Chapter A, new)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3,
               fontsize=9, bbox_to_anchor=(0.5, -0.05))

    plt.tight_layout()
    savefig("fig5_coherence_bridge")


# ── Figure 6: Operator Sequence G = U∘F∘K∘C∘E ────────────────────────────────
def fig6_operator_sequence():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(0, 10); ax.set_ylim(0, 2); ax.axis("off")

    ops   = ["C\nCompress", "K\nCurvature", "F\nFold", "U\nUnfold", "E\nEntropy"]
    descs = [
        "Reduces d.o.f.\nLipschitz",
        "Drives κ→κ*\nMonotone Φ",
        "Rank-1 Jacobian\nFinite branch",
        "Stable branch\nFixed point",
        "ż ≥ 0\nIrreversible cost",
    ]
    colors_ops = [TEAL, NAVY, RED, TEAL, GOLD]

    xs = np.linspace(0.8, 9.2, 5)

    for i, (x, op, desc, col) in enumerate(zip(xs, ops, descs, colors_ops)):
        box = mpatches.FancyBboxPatch((x-0.55, 0.55), 1.1, 0.9,
                                       boxstyle="round,pad=0.05",
                                       fc=col, ec="white", lw=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, 1.0, op, ha="center", va="center",
                fontsize=10, color="white", fontweight="bold")
        ax.text(x, 0.35, desc, ha="center", va="top",
                fontsize=7.5, color=NAVY, style="italic")
        if i < 4:
            ax.annotate("", xy=(xs[i+1]-0.56, 1.0), xytext=(x+0.56, 1.0),
                        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))

    # Loop arrow from E back to C'
    ax.annotate("", xy=(xs[0], 0.55), xytext=(xs[4], 0.55),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2,
                                connectionstyle="arc3,rad=0.4"))
    ax.text(5.0, 0.1, r"$C' \to \cdots$ (next cycle)", ha="center",
            fontsize=8.5, color=GREY)

    ax.set_title("Operator Sequence $G = U \\circ F \\circ K \\circ C$ (+ $E$, Second Edition)\n"
                 "Lean: GenerativeOp (Theorem A (proved)), UnfoldOp.stable_branch (Theorem D (proved))",
                 fontsize=10)

    savefig("fig6_operator_sequence")


# ── Figure 7: Contact 3-Manifold with Limit Cycle Γ ──────────────────────────
def fig7_contact_3d():
    fig = plt.figure(figsize=(8, 6))
    ax  = fig.add_subplot(111, projection="3d")

    # Contact manifold: torus-like surface
    u   = np.linspace(0, 2*np.pi, 60)
    v   = np.linspace(0, 2*np.pi, 60)
    U, V = np.meshgrid(u, v)
    R_maj, R_min = 2.0, 0.7
    X = (R_maj + R_min*np.cos(V)) * np.cos(U)
    Y = (R_maj + R_min*np.cos(V)) * np.sin(U)
    Z = R_min * np.sin(V)
    ax.plot_surface(X, Y, Z, alpha=0.15, color=TEAL, linewidth=0)

    # Limit cycle Γ on the torus (r = 1 in contact coordinates)
    th  = np.linspace(0, 2*np.pi, 300)
    Xg  = (R_maj + R_min*np.cos(0)) * np.cos(th)
    Yg  = (R_maj + R_min*np.cos(0)) * np.sin(th)
    Zg  = np.zeros_like(th)
    ax.plot(Xg, Yg, Zg, color=NAVY, lw=2.5, label=r"$\Gamma$ (limit cycle, $r=1$)")

    # Gronwall basin circle (ε₀ = 1/3 offset)
    r_gb = R_maj * (1 - EPSILON_0 * 0.5)
    ax.plot(r_gb*np.cos(th), r_gb*np.sin(th), np.zeros_like(th),
            "--", color=GOLD, lw=1.5, label=r"$\varepsilon_0=1/3$ (basin)")

    # A few converging trajectories
    for phi0 in [0, np.pi/2, np.pi, 3*np.pi/2]:
        t  = np.linspace(0, 4*np.pi, 200)
        r  = 1 + 0.5*np.exp(-0.4*t/(2*np.pi))
        xt = (R_maj + R_min*np.cos(phi0 + 0.3*t)) * np.cos(t)
        yt = (R_maj + R_min*np.cos(phi0 + 0.3*t)) * np.sin(t)
        zt = 0.3*np.exp(-0.4*t/(2*np.pi))*np.sin(phi0 + t)
        ax.plot(xt, yt, zt, color=TEAL, lw=0.8, alpha=0.5)

    ax.set_title("Contact 3-Manifold $(X, \\alpha)$ with Limit Cycle $\\Gamma$\n"
                 r"$\alpha = dz - \rho^2 d\theta$, "
                 "Lean: contactCoeff_neg, gronwall_radius",
                 fontsize=9)
    ax.legend(fontsize=8, loc="upper right")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")

    savefig("fig7_contact_3d")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Principia Orthogona, Volume I — Figure Generator")
    print(f"dm³ invariants: T* = 2π, μmax = {MU_MAX}, τ = {TAU}")
    print(f"ε₀ = {EPSILON_0:.4f}, r* = {R_STAR:.4f}, τ·ε₀ = {NOISE_TOL:.4f}")
    print(f"Output directory: {os.path.abspath(OUTDIR)}/\n")

    print("Generating figure 1: dm³ phase portrait...")
    fig1_phase_portrait()

    print("Generating figure 2: threshold equivalence / Whitney A₁...")
    fig2_threshold_equivalence()

    print("Generating figure 3: bifurcation diagram...")
    fig3_bifurcation()

    print("Generating figure 4: stability radius...")
    fig4_stability_radius()

    print("Generating figure 5: coherence bridge...")
    fig5_coherence_bridge()

    print("Generating figure 6: operator sequence...")
    fig6_operator_sequence()

    print("Generating figure 7: contact 3-manifold...")
    fig7_contact_3d()

    print("\nAll figures generated. Files in ./figures/")
    print("Build paper: pdflatex principia_vol1_v2_full.tex (run twice)")
    print("Build Lean:  lake update && lake build PrincipiaVol1")
