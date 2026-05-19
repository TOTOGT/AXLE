"""
multi_orbit_togt.py
====================
Python simulation & figure generator for:

  Mathematical Foundations of Multi-Orbit Identity Theory
  within the TO/TOGT Operator Framework
  Pablo Nogueira Grossi — Version 2, May 2026
  Zenodo: https://doi.org/10.5281/zenodo.19210058

Produces four figures:
  fig1_identity_orbits.png      — Identity orbits as closed invariant trajectories
  fig2_resonance_amplification.png — R-operator resonance scan
  fig3_operator_stack.png       — Generative stack G = B∘R∘U∘L∘g∘A schematic
  fig4_embodiment_basin.png     — Embodiment criterion: basin stability & perturbation decay
  orbit_resonance_data.csv      — Raw resonance scan data

Usage:
  python multi_orbit_togt.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
import matplotlib.gridspec as gridspec
import csv, os, warnings
warnings.filterwarnings('ignore')

# ── Palette (navy/gold series) ────────────────────────────────────────────────
NAVY  = '#0a1628'
GOLD  = '#c9a84c'
DARK  = '#1a2a4a'
RED   = '#c0392b'
GREEN = '#1e8449'
BLUE  = '#1a5276'
PURP  = '#6c3483'
GREY  = '#7f8c8d'
LGREY = '#ecf0f4'

def base_style():
    plt.rcParams.update({
        'figure.facecolor': 'white', 'axes.facecolor': 'white',
        'axes.edgecolor': NAVY, 'axes.labelcolor': NAVY,
        'xtick.color': NAVY, 'ytick.color': NAVY, 'text.color': NAVY,
        'font.family': 'serif', 'font.size': 10,
        'axes.titlesize': 11, 'axes.labelsize': 10,
        'legend.fontsize': 8.5, 'figure.dpi': 150,
    })

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1 — Identity orbits as closed invariant trajectories in state space
# Models three coexisting orbits O1, O2, O3 under operators A1, A2, A3
# Each orbit is a closed loop; we show their basins and invariant structure.
# ─────────────────────────────────────────────────────────────────────────────
def make_fig1():
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # Left panel: three identity orbits in 2D state space
    ax = axes[0]
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.2, 3.2)
    ax.set_aspect('equal')
    ax.set_facecolor(LGREY)

    # Basin regions (approximate Voronoi-style)
    theta = np.linspace(0, 2*np.pi, 300)

    # Orbit centres
    centres = [(-1.5, 0.8), (1.5, 0.8), (0.0, -1.5)]
    radii   = [0.70, 0.65, 0.75]
    basin_r = [1.35, 1.30, 1.30]
    colors_orb = [BLUE, GREEN, PURP]
    basin_alpha = 0.13
    labels  = [r'$\mathcal{O}_1$', r'$\mathcal{O}_2$', r'$\mathcal{O}_3$']

    for (cx, cy), br, col in zip(centres, basin_r, colors_orb):
        basin = plt.Circle((cx, cy), br, color=col, alpha=basin_alpha, zorder=1)
        ax.add_patch(basin)

    # Draw orbits as closed loops with perturbation noise for realism
    rng = np.random.default_rng(42)
    for (cx, cy), r, col, lbl in zip(centres, radii, colors_orb, labels):
        noise = 0.04 * rng.standard_normal(len(theta))
        ox = cx + (r + noise) * np.cos(theta)
        oy = cy + (r + noise) * np.sin(theta)
        ax.plot(ox, oy, color=col, linewidth=2.3, zorder=4, label=lbl)
        # Arrow on orbit to show direction
        mid = len(theta) // 4
        ax.annotate('', xy=(ox[mid+3], oy[mid+3]), xytext=(ox[mid], oy[mid]),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.8), zorder=5)
        ax.text(cx, cy, lbl, ha='center', va='center', fontsize=11,
                color=col, fontweight='bold', zorder=6)

    # Separator lines between basins (dashed)
    for x in np.linspace(-3.5, 3.5, 200):
        pass  # just decoration via basin circles

    # A few sample trajectories converging to orbits
    for seed, (cx, cy), col in zip([7, 13, 19], centres, colors_orb):
        rng2 = np.random.default_rng(seed)
        for _ in range(3):
            # Start outside basin
            angle = rng2.uniform(0, 2*np.pi)
            dist  = rng2.uniform(1.5, 2.8)
            sx, sy = cx + dist*np.cos(angle), cy + dist*np.sin(angle)
            # Simple spiral-in trajectory
            t_vals = np.linspace(0, 1, 60)
            r_t = dist * (1 - t_vals) + (radii[centres.index((cx,cy))]) * t_vals
            th_t = angle + 3*np.pi*t_vals
            tx = cx + r_t * np.cos(th_t)
            ty = cy + r_t * np.sin(th_t)
            ax.plot(tx, ty, color=col, alpha=0.35, linewidth=0.9, zorder=3,
                    linestyle='--')

    ax.set_xlabel('State space $x_1$', labelpad=5)
    ax.set_ylabel('State space $x_2$', labelpad=5)
    ax.set_title('Three coexisting identity orbits\nwith basin regions', pad=7)
    ax.legend(loc='upper right', framealpha=0.92, fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Right panel: Inv(Oi) as time series — constant invariant per orbit
    ax2 = axes[1]
    t = np.linspace(0, 20, 500)
    inv_vals = [1.00, 1.55, 0.70]
    inv_labels = [r'$\mathrm{Inv}(\mathcal{O}_1) = 1.00$',
                  r'$\mathrm{Inv}(\mathcal{O}_2) = 1.55$',
                  r'$\mathrm{Inv}(\mathcal{O}_3) = 0.70$']
    for iv, col, lbl in zip(inv_vals, colors_orb, inv_labels):
        # Add small perturbation then recovery
        noise = 0.025 * np.sin(5*t) * np.exp(-0.3*t)
        perturb = np.zeros_like(t)
        # Kick at t=8
        kick_idx = np.searchsorted(t, 8)
        perturb[kick_idx:] = 0.18 * np.exp(-1.2*(t[kick_idx:]-8))
        ax2.plot(t, iv + noise + perturb, color=col, linewidth=1.8, label=lbl)
        ax2.axhline(iv, color=col, linewidth=0.8, linestyle=':', alpha=0.6)

    ax2.axvline(8, color=GOLD, linewidth=1.4, linestyle='--',
                label='Perturbation at $t=8$')
    ax2.set_xlabel('Time $t$', labelpad=5)
    ax2.set_ylabel(r'Invariant $\mathrm{Inv}(\mathcal{O}_i)$', labelpad=5)
    ax2.set_title('Orbit invariants: stability under perturbation\n'
                  r'$\|\delta x_t\| \to 0$ (basin stability)', pad=7)
    ax2.legend(loc='upper right', framealpha=0.92, fontsize=8.5)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.suptitle('Figure 1 — Identity Orbits and Invariant Stability',
                 fontsize=11, fontweight='bold', color=NAVY, y=1.01)
    plt.tight_layout()
    plt.savefig('/home/claude/fig1_identity_orbits.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("fig1 done")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2 — R-operator resonance scan
# R1: detection (Inv similarity), R2: amplification (λ > 1), R3: fixed point
# ─────────────────────────────────────────────────────────────────────────────
def make_fig2():
    base_style()
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))

    # Panel A: R1 — Resonance detection: Inv similarity measure vs coupling δ
    ax = axes[0]
    delta = np.linspace(0, 2.0, 300)
    # Similarity = exp(-delta²/2σ²), threshold at δ_thresh
    sigma = 0.4
    thresh = 0.8
    sim = np.exp(-delta**2 / (2*sigma**2))
    detected = sim >= 0.5
    ax.plot(delta, sim, color=BLUE, linewidth=2.2,
            label=r'$\mathrm{Sim}(\mathcal{O}_1,\mathcal{O}_2)$')
    ax.axhline(0.5, color=GOLD, linewidth=1.5, linestyle='--',
               label='Detection threshold')
    ax.fill_between(delta, sim, 0.5, where=detected, color=BLUE, alpha=0.15)
    ax.set_xlabel(r'Invariant distance $|\mathrm{Inv}(\mathcal{O}_1)-\mathrm{Inv}(\mathcal{O}_2)|$')
    ax.set_ylabel(r'$R_1(\mathcal{O}_1,\mathcal{O}_2)$')
    ax.set_title(r'(A) $R_1$: Resonance Detection', fontsize=10)
    ax.legend(fontsize=8, framealpha=0.9)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # Panel B: R2 — Amplification: Inv(G') = λ·Inv(G), λ > 1 across iterations
    ax = axes[1]
    iters = np.arange(0, 12)
    lam = 1.35
    inv_0 = 1.0
    inv_amplified = inv_0 * lam**iters
    inv_capped = np.minimum(inv_amplified, 6.5)  # saturation at boundary
    ax.plot(iters, inv_capped, color=GREEN, linewidth=2.2, marker='o', markersize=5,
            label=r'$\mathrm{Inv}(G_t)$, $\lambda=1.35$')
    ax.plot(iters, inv_0 * np.ones_like(iters), color=GREY, linewidth=1.2,
            linestyle=':', label='Baseline $\mathrm{Inv}(G_0)$')
    # R3 fixed point
    ax.axhline(inv_capped[-1], color=GOLD, linewidth=1.5, linestyle='--',
               label=r'$G_\infty$ (R3 fixed point)')
    ax.set_xlabel('Iteration $t$')
    ax.set_ylabel(r'$\mathrm{Inv}(G_t)$')
    ax.set_title(r'(B) $R_2$: Resonance Amplification', fontsize=10)
    ax.legend(fontsize=8, framealpha=0.9)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # Panel C: R3 — Stabilisation convergence for different initial λ
    ax = axes[2]
    t_vals = np.linspace(0, 8, 200)
    for lam_init, col, lbl in [(2.2, RED, r'$\lambda_0=2.2$'),
                                (1.6, BLUE, r'$\lambda_0=1.6$'),
                                (1.1, GREEN, r'$\lambda_0=1.1$')]:
        # Model: Gt converges to G∞ exponentially
        G_inf = 5.5
        G0    = lam_init * 1.0
        # Saturating approach
        Gt = G_inf - (G_inf - G0) * np.exp(-0.8 * t_vals)
        ax.plot(t_vals, Gt, color=col, linewidth=2.0, label=lbl)
    ax.axhline(G_inf, color=GOLD, linewidth=1.5, linestyle='--',
               label=r'$G_\infty$ (fixed point)')
    ax.set_xlabel('Iteration $t$')
    ax.set_ylabel(r'$\mathrm{Inv}(G_t)$')
    ax.set_title(r'(C) $R_3$: Resonance Stabilisation', fontsize=10)
    ax.legend(fontsize=8, framealpha=0.9)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    plt.suptitle('Figure 2 — R-Operator Family: Resonance Detection, Amplification, Stabilisation',
                 fontsize=11, fontweight='bold', color=NAVY, y=1.02)
    plt.tight_layout()
    plt.savefig('/home/claude/fig2_resonance_amplification.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("fig2 done")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 3 — Generative Stack schematic: G = B ∘ R ∘ U ∘ L ∘ g ∘ A
# with U-operator unification and B-operator boundary detail
# ─────────────────────────────────────────────────────────────────────────────
def make_fig3():
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.0))
    fig.patch.set_facecolor('#f8f9fd')

    # Left: Linear pipeline G = B∘R∘U∘L∘g∘A
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_facecolor('#f8f9fd')

    stages = [
        ('$A$\nOrbit\nGenerator',   1.0,  NAVY,   'white'),
        ('$g$\nLocal\nMap',          2.5,  DARK,   'white'),
        ('$L$\nLift\nOperator',      4.0,  BLUE,   'white'),
        ('$U$\nUnification',         5.5,  PURP,   'white'),
        ('$R$\nResonance',           7.0,  GREEN,  'white'),
        ('$B$\nBoundary',            8.5,  RED,    'white'),
    ]
    bw, bh = 1.25, 1.20
    cy = 2.0

    for label, cx, fc, tc in stages:
        rect = FancyBboxPatch((cx - bw/2, cy - bh/2), bw, bh,
                              boxstyle='round,pad=0.08', linewidth=1.4,
                              edgecolor='white', facecolor=fc, zorder=3)
        ax.add_patch(rect)
        ax.text(cx, cy, label, ha='center', va='center', fontsize=8.2,
                color=tc, zorder=4, multialignment='center', fontfamily='serif')

    # Arrows between stages
    for i in range(len(stages)-1):
        x1 = stages[i][1] + bw/2
        x2 = stages[i+1][1] - bw/2
        ax.annotate('', xy=(x2, cy), xytext=(x1, cy),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.8), zorder=5)

    # Input/Output labels
    ax.text(0.1, cy, r'$\mathcal{O}_t$', ha='center', va='center',
            fontsize=12, color=NAVY, fontfamily='serif')
    ax.annotate('', xy=(stages[0][1]-bw/2, cy), xytext=(0.35, cy),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.8))
    ax.text(9.8, cy, r'$\mathcal{O}_{t+1}$', ha='center', va='center',
            fontsize=12, color=NAVY, fontfamily='serif')
    ax.annotate('', xy=(9.55, cy), xytext=(stages[-1][1]+bw/2, cy),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.8))

    # Formula label below
    ax.text(5.0, 0.55,
            r'$G = B \circ R \circ U \circ L \circ g \circ A$',
            ha='center', va='center', fontsize=12, color=NAVY,
            fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=GOLD, linewidth=1.5))

    ax.text(5.0, 3.65,
            r'Generative Stack — single orbit, one step',
            ha='center', va='center', fontsize=10, color=NAVY, fontfamily='serif')

    # Right: U-operator unification detail — three orbits merging
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 4)
    ax2.axis('off')
    ax2.set_facecolor('#f8f9fd')

    # Input orbits
    orbit_cols = [BLUE, GREEN, PURP]
    orbit_labels = [r'$G_1$', r'$G_2$', r'$G_3$']
    ys_in = [3.2, 2.0, 0.8]
    for oy, col, lbl in zip(ys_in, orbit_cols, orbit_labels):
        ax2.add_patch(FancyBboxPatch((0.3, oy-0.30), 1.1, 0.60,
                                    boxstyle='round,pad=0.06',
                                    facecolor=col, edgecolor='white',
                                    linewidth=1.2, zorder=3))
        ax2.text(0.85, oy, lbl, ha='center', va='center',
                 color='white', fontsize=10, fontfamily='serif', zorder=4)
        # Arrow to U box
        ax2.annotate('', xy=(3.8, 2.0 + (oy-2.0)*0.4), xytext=(1.4, oy),
                     arrowprops=dict(arrowstyle='->', color=col, lw=1.5,
                                     connectionstyle='arc3,rad=0.0'), zorder=2)

    # U1 box
    ax2.add_patch(FancyBboxPatch((3.8, 1.3), 1.5, 1.4,
                                 boxstyle='round,pad=0.1',
                                 facecolor=PURP, edgecolor='white',
                                 linewidth=1.4, zorder=3))
    ax2.text(4.55, 2.0, '$U_1$\nUnify\nIntersect', ha='center', va='center',
             color='white', fontsize=9, fontfamily='serif', zorder=4,
             multialignment='center')

    # Arrow to output
    ax2.annotate('', xy=(7.0, 2.0), xytext=(5.3, 2.0),
                 arrowprops=dict(arrowstyle='->', color=PURP, lw=2.0), zorder=5)

    # Output unified orbit
    ax2.add_patch(FancyBboxPatch((7.0, 1.35), 2.3, 1.30,
                                 boxstyle='round,pad=0.1',
                                 facecolor=GOLD, edgecolor=NAVY,
                                 linewidth=1.5, zorder=3))
    ax2.text(8.15, 2.0,
             r'$G_{\mathrm{unified}}$' '\n'
             r'$\mathrm{Inv} = \mathrm{Inv}_1 \cap \mathrm{Inv}_2 \cap \mathrm{Inv}_3$',
             ha='center', va='center', fontsize=8.2, color=NAVY,
             fontfamily='serif', zorder=4, multialignment='center')

    ax2.text(5.0, 3.7,
             r'$U_1(G_1,G_2,G_3)$ — Invariance-Preserving Unification',
             ha='center', va='center', fontsize=10, color=NAVY, fontfamily='serif')

    plt.suptitle('Figure 3 — Generative Stack and U-Operator Unification',
                 fontsize=11, fontweight='bold', color=NAVY, y=1.01)
    plt.tight_layout()
    plt.savefig('/home/claude/fig3_operator_stack.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("fig3 done")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 4 — Embodiment criterion and B-operator boundary map
# Left: ||δx_t|| decay under perturbation (Theorem 8.1)
# Right: B1/B2/B3 boundary structure in Inv space
# ─────────────────────────────────────────────────────────────────────────────
def make_fig4():
    base_style()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

    # Left: perturbation decay ||δx_t|| → 0 for embodied systems
    ax = axes[0]
    t = np.linspace(0, 15, 400)
    rng = np.random.default_rng(3)

    # Three orbits: different initial perturbation magnitudes
    for mag, col, lbl in [(1.0, BLUE, r'$\mathcal{O}_1$: $\|\delta x_0\|=1.0$'),
                           (0.6, GREEN, r'$\mathcal{O}_2$: $\|\delta x_0\|=0.6$'),
                           (1.4, PURP, r'$\mathcal{O}_3$: $\|\delta x_0\|=1.4$')]:
        noise = 0.03 * rng.standard_normal(len(t))
        decay = mag * np.exp(-0.45 * t) + noise * np.exp(-0.3*t)
        decay = np.maximum(decay, 0)
        ax.plot(t, decay, color=col, linewidth=2.0, label=lbl)

    ax.axhline(0, color=NAVY, linewidth=1.0, linestyle='-', alpha=0.4)
    ax.axhline(0.05, color=GOLD, linewidth=1.3, linestyle='--',
               label=r'Embodiment threshold $\epsilon$')
    ax.set_xlabel('Time $t$', labelpad=5)
    ax.set_ylabel(r'Perturbation norm $\|\delta x_t\|$', labelpad=5)
    ax.set_title('Embodiment Criterion (Theorem 8.1)\n'
                 r'$\|\delta x_t\| \to 0$ under bounded perturbation', pad=7)
    ax.legend(loc='upper right', framealpha=0.92, fontsize=8.5)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    # Right: B-operator boundary structure in Inv space
    ax2 = axes[1]
    ax2.set_xlim(-0.1, 3.5)
    ax2.set_ylim(-0.1, 3.5)
    ax2.set_aspect('equal')

    # Draw Inv space as filled regions
    # B3: collapse region (Inv < ε)
    eps_collapse = 0.3
    collapse_region = plt.Rectangle((0, 0), eps_collapse, 3.5,
                                    color=RED, alpha=0.18, zorder=1)
    ax2.add_patch(collapse_region)
    ax2.text(0.15, 3.2, r'$B_3$: Collapse', ha='center', va='top',
             color=RED, fontsize=8.5, rotation=90, fontfamily='serif')

    # Identity boundaries for three orbits
    orbit_invs = [0.7, 1.5, 2.5]
    orbit_widths = [0.25, 0.28, 0.22]
    for inv_c, w, col, lbl in zip(orbit_invs, orbit_widths, [BLUE, GREEN, PURP],
                                   [r'$\partial\mathcal{O}_1$', r'$\partial\mathcal{O}_2$',
                                    r'$\partial\mathcal{O}_3$']):
        # B1: identity boundary as vertical band
        band = plt.Rectangle((inv_c - w/2, 0), w, 3.5,
                              color=col, alpha=0.22, zorder=2)
        ax2.add_patch(band)
        ax2.axvline(inv_c, color=col, linewidth=2.0, zorder=3, label=lbl + r' ($B_1$)')
        ax2.text(inv_c, 3.35, lbl, ha='center', va='top',
                 color=col, fontsize=8.5, fontfamily='serif')

    # B2: transition arrows between orbits
    tau = 0.5  # max allowed ΔInv for transition
    ax2.annotate('', xy=(orbit_invs[1]-0.02, 1.8), xytext=(orbit_invs[0]+0.15, 1.8),
                 arrowprops=dict(arrowstyle='<->', color=GOLD, lw=2.0))
    ax2.text((orbit_invs[0]+orbit_invs[1])/2, 2.05,
             r'$B_2$: $\Delta\mathrm{Inv}\leq\tau$', ha='center',
             fontsize=8.5, color=GOLD, fontfamily='serif')

    # Restore arrow for B3
    ax2.annotate('', xy=(eps_collapse + 0.05, 1.0), xytext=(eps_collapse + 0.55, 1.0),
                 arrowprops=dict(arrowstyle='<-', color=RED, lw=1.8))
    ax2.text(eps_collapse + 0.30, 1.2, r'$B_3$: Restore', ha='center',
             fontsize=8.0, color=RED, fontfamily='serif')

    ax2.set_xlabel(r'Invariant value $\mathrm{Inv}(\mathcal{O})$', labelpad=5)
    ax2.set_ylabel(r'Secondary invariant', labelpad=5)
    ax2.set_title('B-Operator Boundary Structure\n'
                  r'$B_1$ (identity) · $B_2$ (transition) · $B_3$ (collapse/restore)',
                  pad=7)
    ax2.legend(loc='lower right', framealpha=0.92, fontsize=8.0)
    ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)

    plt.suptitle('Figure 4 — Embodiment Criterion and B-Operator Boundary Map',
                 fontsize=11, fontweight='bold', color=NAVY, y=1.01)
    plt.tight_layout()
    plt.savefig('/home/claude/fig4_embodiment_basin.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("fig4 done")

# ─────────────────────────────────────────────────────────────────────────────
# CSV: resonance scan data (R1 detection, R2 amplification)
# ─────────────────────────────────────────────────────────────────────────────
def make_csv():
    delta = np.linspace(0, 2.0, 100)
    sigma = 0.4
    sim   = np.exp(-delta**2 / (2*sigma**2))
    lam   = 1.35
    iters = np.arange(0, 12)
    inv_t = np.minimum(lam**iters, 6.5)

    with open('/home/claude/orbit_resonance_data.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['# Multi-Orbit Identity Theory — Resonance scan data'])
        w.writerow(['# Pablo Nogueira Grossi, G6LLC, May 2026'])
        w.writerow(['# Zenodo: 10.5281/zenodo.19210058'])
        w.writerow([])
        w.writerow(['## R1 Resonance Detection'])
        w.writerow(['inv_distance_delta', 'similarity_R1'])
        for d, s in zip(delta, sim):
            w.writerow([f'{d:.4f}', f'{s:.6f}'])
        w.writerow([])
        w.writerow(['## R2 Resonance Amplification (lambda=1.35)'])
        w.writerow(['iteration_t', 'Inv_Gt'])
        for i, iv in zip(iters, inv_t):
            w.writerow([int(i), f'{iv:.6f}'])
    print("csv done")

if __name__ == '__main__':
    make_fig1()
    make_fig2()
    make_fig3()
    make_fig4()
    make_csv()
    print("\nAll outputs generated.")
    print("  fig1_identity_orbits.png")
    print("  fig2_resonance_amplification.png")
    print("  fig3_operator_stack.png")
    print("  fig4_embodiment_basin.png")
    print("  orbit_resonance_data.csv")
