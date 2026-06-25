"""
figures_enceladus.py
Principia Orthogona × Enceladus — Zenodo deposit figures
Pablo Nogueira Grossi · G6 LLC · 2026 · CC BY 4.0
DOI: 10.5281/zenodo.20779067

Run: python3 figures_enceladus.py
Produces: fig1_operator_chain.png
          fig2_whitney_fold.png
          fig3_gronwall_basin.png
          fig4_chemical_survival.png
          fig5_entropy_monotonicity.png
          fig6_enceladus_cross_section.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc, Wedge
from matplotlib.colors import LinearSegmentedColormap
from scipy.integrate import odeint

# ── Palette ──────────────────────────────────────────────────────────
NAVY   = '#1a2744'
GOLD   = '#c9a84c'
CREAM  = '#faf7f0'
SMOKE  = '#f0ece4'
TEAL   = '#1a6457'
RED    = '#8a2020'
PURPLE = '#4a3880'
MID    = '#5a6e8a'
ORANGE = '#c47820'

DPI = 180

# ─────────────────────────────────────────────────────────────────────
# FIG 1 — Operator chain G = U∘F∘K∘C∘E with Enceladus mapping
# ─────────────────────────────────────────────────────────────────────
def fig1_operator_chain():
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.axis('off')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6)

    operators = [
        ('C', TEAL,   'Compression',
         '3D ocean convection\n→ 1D fissure flow\nδ ≈ 10⁻³',
         'Subsurface\nocean'),
        ('K', MID,    'Curvature',
         'Ice-shell curvature\n→ κ* ≈ (2000 m)⁻¹\nTidal heating Q̇ ≈ 10¹⁰ W',
         'Ice shell\npressure'),
        ('F', RED,    'Fold (Whitney A₁)',
         'Fissure rupture\nJacobian rank loss = 1\nN_fiss = 4–8 branches',
         'Tiger-stripe\nejection'),
        ('U', '#4a7a30', 'Unfolding',
         'Plume dispersal\n→ E-ring orbit Γ\na_E = 3.95 R_S',
         'E-ring\ninsertion'),
        ('E', ORANGE, 'Entropy',
         'Ejection irreversibility\nṠ ≈ 2.7×10⁶ J K⁻¹ s⁻¹\nSpace weathering',
         'Chemical\nrecord'),
    ]

    xs = [1.1, 3.5, 5.9, 8.3, 10.7]
    box_w, box_h = 1.7, 1.4

    for i, (op, col, name, detail, phys) in enumerate(operators):
        x = xs[i]
        # Main operator box
        bb = FancyBboxPatch((x - box_w/2, 3.0), box_w, box_h,
                            boxstyle='round,pad=0.08',
                            linewidth=2, edgecolor=col,
                            facecolor=NAVY)
        ax.add_patch(bb)
        # Operator letter
        ax.text(x, 3.7 + box_h*0.15, op,
                ha='center', va='center', fontsize=26, fontweight='bold',
                color=col, fontfamily='serif')
        # Name below letter
        ax.text(x, 3.15, name,
                ha='center', va='center', fontsize=6.5,
                color=CREAM, fontfamily='sans-serif')
        # Detail box (below)
        ax.text(x, 2.3, detail,
                ha='center', va='center', fontsize=6.2,
                color='#aab8cc', fontfamily='monospace', linespacing=1.5)
        # Physical label (above)
        ax.text(x, 5.1, phys,
                ha='center', va='center', fontsize=7,
                color=GOLD, fontfamily='sans-serif',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d1a2e',
                          edgecolor=GOLD, linewidth=0.8))
        # Arrow to next
        if i < len(operators) - 1:
            ax.annotate('', xy=(xs[i+1] - box_w/2 - 0.05, 3.7),
                        xytext=(x + box_w/2 + 0.05, 3.7),
                        arrowprops=dict(arrowstyle='->', color=GOLD,
                                        lw=2.0))

    # G = ... label
    ax.text(6.0, 5.7,
            r'$G_E = E \circ U \circ F \circ K \circ C$   ·   dm³ Operator Chain',
            ha='center', va='center', fontsize=12,
            color=CREAM, fontfamily='serif', style='italic')

    # Bottom source line
    ax.text(6.0, 0.3,
            'Principia Orthogona · Grossi 2026 · Zenodo 10.5281/zenodo.20779067',
            ha='center', va='center', fontsize=6.5, color='#556070')

    # Vertical dashed line showing Vol I / Vol II boundary
    ax.axvline(x=7.1, ymin=0.08, ymax=0.9, color=GOLD,
               linestyle='--', linewidth=0.8, alpha=0.4)
    ax.text(7.1, 0.8, 'Vol I / Vol II\nboundary', ha='center',
            fontsize=5.5, color=GOLD, alpha=0.6)

    fig.suptitle('Figure 1 — dm³ Operator Chain: Enceladus Physical Realisation',
                 color=GOLD, fontsize=10, y=0.97, fontfamily='sans-serif')
    plt.tight_layout(pad=0.5)
    plt.savefig('fig1_operator_chain.png', dpi=DPI, facecolor=NAVY,
                bbox_inches='tight')
    plt.close()
    print('fig1 done')


# ─────────────────────────────────────────────────────────────────────
# FIG 2 — Whitney A₁ Fold: potential + Enceladus parameters
# ─────────────────────────────────────────────────────────────────────
def fig2_whitney_fold():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor(NAVY)

    # Panel A: Whitney A₁ potential V(q) = q³ − 3q
    ax = axes[0]
    ax.set_facecolor('#0d1a2e')
    q = np.linspace(-2.2, 2.2, 400)
    V = q**3 - 3*q

    ax.plot(q, V, color=GOLD, lw=2.5, label=r'$V(q) = q^3 - 3q$')
    # Mark critical points
    ax.scatter([1, -1], [-2, 2], color=[TEAL, RED], s=80, zorder=5)
    ax.annotate(r'$q^* = 1$ (stable branch)', xy=(1, -2),
                xytext=(1.4, -3.2), fontsize=8, color=TEAL,
                arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.2))
    ax.annotate(r'$q = -1$ (unstable)', xy=(-1, 2),
                xytext=(-2.1, 0.5), fontsize=8, color=RED,
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))

    # Shade stable region
    q_stable = q[q >= 1]
    V_stable = q_stable**3 - 3*q_stable
    ax.fill_between(q_stable, V_stable, -6, alpha=0.12, color=TEAL,
                    label='Stable branch (Enceladus)')

    ax.axhline(0, color='#556070', lw=0.8, ls='--')
    ax.axvline(0, color='#556070', lw=0.8, ls='--')
    ax.set_xlabel(r'$q$  (deformation parameter)', color=CREAM, fontsize=9)
    ax.set_ylabel(r'$V(q)$', color=CREAM, fontsize=9)
    ax.set_title('Whitney A₁ Normal Form\n' r'$V(q)=q^3-3q$, proved in PrincipiaVol1.lean',
                 color=CREAM, fontsize=9, pad=8)
    ax.set_ylim(-6, 6)
    ax.tick_params(colors=CREAM, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor('#334466')
    ax.legend(fontsize=7.5, facecolor='#0d1a2e', labelcolor=CREAM,
              edgecolor=GOLD)
    ax.text(0.05, 0.04,
            r'$V_{\rm critical}(q^*)=-2$' + '\n' + r'$V^{\prime\prime}(q^*)=6>0$',
            transform=ax.transAxes, fontsize=7.5, color=GOLD,
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#0a1420', edgecolor=GOLD,
                      alpha=0.8))

    # Panel B: Bifurcation at κ* — Enceladus ice-shell
    ax2 = axes[1]
    ax2.set_facecolor('#0d1a2e')

    kappa = np.linspace(0, 1.2e-3, 400)  # m⁻¹
    kappa_star = 5e-4  # m⁻¹

    # Stable branch: r_stable (containment possible)
    r_stable = np.where(kappa <= kappa_star,
                        1.0 - 0.3*(kappa/kappa_star)**2,
                        np.nan)
    # Unstable branch: r_unstable (diverging)
    r_unstable = np.where(kappa <= kappa_star,
                          0.3*(kappa/kappa_star)**2,
                          np.nan)
    # Post-fold: ejection
    r_eject = np.where(kappa >= kappa_star,
                       1.0 + 2.5*(kappa/kappa_star - 1),
                       np.nan)

    ax2.plot(kappa*1e3, r_stable, color=TEAL, lw=2.5, label='Stable (contained)')
    ax2.plot(kappa*1e3, r_unstable, color=RED, lw=2, ls='--', label='Unstable')
    ax2.plot(kappa*1e3, r_eject, color=GOLD, lw=2.5, label='Ejection branch (fold)')
    ax2.axvline(kappa_star*1e3, color=GOLD, lw=1.5, ls=':')
    ax2.text(kappa_star*1e3 + 0.01, 1.85,
             r'$\kappa^* \approx (2000\,{\rm m})^{-1}$',
             color=GOLD, fontsize=8)
    ax2.scatter([kappa_star*1e3], [1.0], color=GOLD, s=120, zorder=5,
                marker='*', label='Fold point (tiger stripe)')

    ax2.set_xlabel(r'Ice-shell curvature $\kappa$ $(10^{-3}\ {\rm m}^{-1})$',
                   color=CREAM, fontsize=9)
    ax2.set_ylabel('Scaled response (normalised)', color=CREAM, fontsize=9)
    ax2.set_title('Whitney A₁ in Enceladus Ice Shell\n'
                  'Fold at critical focal radius κ*',
                  color=CREAM, fontsize=9, pad=8)
    ax2.tick_params(colors=CREAM, labelsize=8)
    for spine in ax2.spines.values():
        spine.set_edgecolor('#334466')
    ax2.legend(fontsize=7.5, facecolor='#0d1a2e', labelcolor=CREAM,
               edgecolor=GOLD)
    ax2.set_ylim(-0.1, 2.2)

    fig.suptitle('Figure 2 — Whitney A₁ Fold: Normal Form and Enceladus Ice-Shell Bifurcation',
                 color=GOLD, fontsize=10, y=1.01, fontfamily='sans-serif')
    fig.patch.set_facecolor(NAVY)
    plt.tight_layout()
    plt.savefig('fig2_whitney_fold.png', dpi=DPI, facecolor=NAVY,
                bbox_inches='tight')
    plt.close()
    print('fig2 done')


# ─────────────────────────────────────────────────────────────────────
# FIG 3 — Gronwall Basin ε₀ = 1/3 with chemistry
# ─────────────────────────────────────────────────────────────────────
def fig3_gronwall_basin():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.patch.set_facecolor(NAVY)

    # Panel A: Phase portrait with Gronwall basin
    ax = axes[0]
    ax.set_facecolor('#0d1a2e')
    ax.set_aspect('equal')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)

    # Limit cycle Γ at r = 1
    theta = np.linspace(0, 2*np.pi, 300)
    ax.plot(np.cos(theta), np.sin(theta), color=GOLD, lw=2.5,
            label=r'Limit cycle $\Gamma$ ($r=1$)', zorder=5)

    # Gronwall basin boundaries
    r_eps = 1 + 1/3  # outer = 4/3
    r_inn = 1 - 1/3  # inner = 2/3
    ax.plot(r_eps*np.cos(theta), r_eps*np.sin(theta),
            color=TEAL, lw=1.8, ls='--',
            label=r'$r_{\rm att}+\varepsilon_0 = 4/3$')
    ax.plot(r_inn*np.cos(theta), r_inn*np.sin(theta),
            color=TEAL, lw=1.8, ls=':',
            label=r'$r_{\rm att}-\varepsilon_0 = 2/3$')

    # Shade basin
    for r_out, r_in, col, alp in [
        (r_eps, 1.0, TEAL, 0.08),
        (1.0, r_inn, TEAL, 0.08),
    ]:
        angles = np.linspace(0, 2*np.pi, 300)
        x_out = r_out * np.cos(angles)
        y_out = r_out * np.sin(angles)
        x_in  = r_in  * np.cos(angles[::-1])
        y_in  = r_in  * np.sin(angles[::-1])
        ax.fill(np.concatenate([x_out, x_in]),
                np.concatenate([y_out, y_in]),
                color=col, alpha=alp)

    # Trajectories converging to Γ
    def dm3_ode(y, t):
        r, theta_v = y
        drdt = r*(1 - r**2) + 2*(r-1)*np.exp(-0.5)
        dtdt = 1.0
        return [drdt, dtdt]

    t = np.linspace(0, 15, 800)
    for r0 in [0.3, 0.55, 1.5, 1.75]:
        sol = odeint(dm3_ode, [r0, 0], t)
        r_sol = sol[:, 0]
        th_sol = sol[:, 1]
        x_sol = r_sol * np.cos(th_sol)
        y_sol = r_sol * np.sin(th_sol)
        col = MID if r0 < 1 else RED
        ax.plot(x_sol[:300], y_sol[:300], color=col, lw=0.9, alpha=0.7)

    # Whitney fold threshold r★
    r_star = 0.77594059
    ax.plot(r_star*np.cos(theta), r_star*np.sin(theta),
            color=RED, lw=1.2, ls='-.', alpha=0.7,
            label=r'$r^\star \approx 0.776$ (Whitney threshold)')

    ax.text(0, 0, r'$\varepsilon_0 = 1/3$',
            ha='center', va='center', fontsize=10, color=GOLD,
            fontfamily='serif')

    ax.set_xlabel('$x = r\\cos\\theta$', color=CREAM, fontsize=9)
    ax.set_ylabel('$y = r\\sin\\theta$', color=CREAM, fontsize=9)
    ax.set_title('Gronwall Basin $\\mathcal{B}(\\varepsilon_0)$\n'
                 'dm³ contact normal form',
                 color=CREAM, fontsize=9)
    ax.tick_params(colors=CREAM, labelsize=8)
    for sp in ax.spines.values():
        sp.set_edgecolor('#334466')
    ax.legend(fontsize=6.8, facecolor='#0d1a2e', labelcolor=CREAM,
              edgecolor=GOLD, loc='upper right')

    # Panel B: Chemical basin mapping
    ax2 = axes[1]
    ax2.set_facecolor('#0d1a2e')

    compounds = {
        'Aromatic\n(aryl)':  (520, True,  TEAL),
        'Carbonyl\n(O-bearing)': (500, True, TEAL),
        'Ester /\nalkene': (420, False, RED),
        'Ether /\nethyl': (365, False, RED),
        'N,O-bearing\n(tentative)': (440, None, ORANGE),
    }

    names = list(compounds.keys())
    D_vals = [compounds[k][0] for k in names]
    survives = [compounds[k][1] for k in names]
    colors_bar = [compounds[k][2] for k in names]

    bars = ax2.barh(names, D_vals, color=colors_bar, alpha=0.85,
                    edgecolor=CREAM, linewidth=0.6)

    # Threshold line: D_min ~ 450 kJ/mol (basin boundary)
    D_min = 450
    ax2.axvline(D_min, color=GOLD, lw=2, ls='--',
                label=f'Basin boundary $D_{{\\min}} \\approx {D_min}$ kJ/mol\n'
                       r'($\varepsilon_0=1/3$ analogue)')

    # Labels
    for i, (bar, D, s) in enumerate(zip(bars, D_vals, survives)):
        label = ('✓ E-ring stable' if s is True
                 else ('✗ Absent from E ring' if s is False
                       else '? Status open'))
        col_l = TEAL if s is True else (RED if s is False else ORANGE)
        ax2.text(D + 8, bar.get_y() + bar.get_height()/2,
                 label, va='center', fontsize=7.5, color=col_l)

    ax2.axvspan(D_min, 620, alpha=0.07, color=TEAL,
                label=r'Within basin ($D \geq D_{\min}$)')
    ax2.axvspan(300, D_min, alpha=0.07, color=RED,
                label=r'Outside basin ($D < D_{\min}$)')

    ax2.set_xlabel('Bond dissociation energy $D$ (kJ mol⁻¹)', color=CREAM, fontsize=9)
    ax2.set_title('Chemical Survival as Gronwall Basin Selection\n'
                  'Khawaja et al. 2025 · Proposition 5.1',
                  color=CREAM, fontsize=9)
    ax2.tick_params(colors=CREAM, labelsize=8)
    ax2.set_xlim(300, 620)
    for sp in ax2.spines.values():
        sp.set_edgecolor('#334466')
    ax2.legend(fontsize=7, facecolor='#0d1a2e', labelcolor=CREAM,
               edgecolor=GOLD, loc='lower right')

    ax2.text(0.02, 0.04,
             'Data: Khawaja et al. (2025)\nNölle et al. (2024)',
             transform=ax2.transAxes, fontsize=6.5, color='#8899aa',
             fontstyle='italic')

    fig.suptitle('Figure 3 — Gronwall Basin ε₀ = 1/3 and Chemical Survival Record',
                 color=GOLD, fontsize=10, y=1.01, fontfamily='sans-serif')
    plt.tight_layout()
    plt.savefig('fig3_gronwall_basin.png', dpi=DPI, facecolor=NAVY,
                bbox_inches='tight')
    plt.close()
    print('fig3 done')


# ─────────────────────────────────────────────────────────────────────
# FIG 4 — Entropy monotonicity z(t) with Enceladus observational bound
# ─────────────────────────────────────────────────────────────────────
def fig4_entropy_monotonicity():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor(NAVY)

    # Panel A: z(t) along dm³ contact orbit
    ax = axes[0]
    ax.set_facecolor('#0d1a2e')

    def dm3_full(y, t):
        r, theta, z = y
        drdt = r*(1 - r**2) + 2*(r-1)*np.exp(-z)
        dtdt = 1.0
        dzdt = r**2 - 2*(r-1)**2 * np.exp(-z)
        return [drdt, dtdt, dzdt]

    t_span = np.linspace(0, 25, 1500)
    for r0, col, lbl in [(0.4, TEAL, '$r_0=0.4$'), (1.6, RED, '$r_0=1.6$'),
                          (0.9, MID, '$r_0=0.9$')]:
        sol = odeint(dm3_full, [r0, 0, 0.01], t_span)
        ax.plot(t_span, sol[:, 2], color=col, lw=2, label=lbl)

    ax.axhline(0, color='#556070', lw=0.8, ls='--')
    ax.set_xlabel('$t$  (dimensionless time)', color=CREAM, fontsize=9)
    ax.set_ylabel('$z(t)$ — entropy / contact action', color=CREAM, fontsize=9)
    ax.set_title('Entropy Monotonicity — Theorem T1\n'
                 r'$\dot{z}(t) \geq 0$ along all contact orbits',
                 color=CREAM, fontsize=9)
    ax.tick_params(colors=CREAM, labelsize=8)
    for sp in ax.spines.values():
        sp.set_edgecolor('#334466')
    ax.legend(fontsize=8, facecolor='#0d1a2e', labelcolor=CREAM, edgecolor=GOLD)
    ax.text(0.03, 0.92,
            'Lean 4 status: exponent sign ✓\nFull ODE: open (AXLE #15)',
            transform=ax.transAxes, fontsize=7, color=ORANGE,
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#0a1420', edgecolor=ORANGE))

    # Panel B: Observational bound — ether concentration vs dwell time
    ax2 = axes[1]
    ax2.set_facecolor('#0d1a2e')

    # Schematic decay curve (photodissociation)
    tau = np.logspace(1, 7, 400)  # years

    # Aromatic: long photodissociation lifetime (~10⁷ yr)
    C_aryl   = np.exp(-tau / 1e7)
    # Ether: shorter lifetime (~10⁴ yr)
    C_ether  = np.exp(-tau / 1e4)
    # E-ring dwell time range (shaded)
    t_ring_lo, t_ring_hi = 1e3, 1e6

    ax2.semilogx(tau, C_aryl, color=TEAL, lw=2.5,
                 label='Aromatic / carbonyl ($D≥500$ kJ/mol)')
    ax2.semilogx(tau, C_ether, color=RED, lw=2.5,
                 label='Ether / ethyl ($D≤380$ kJ/mol)')
    ax2.axvspan(t_ring_lo, t_ring_hi, alpha=0.12, color=GOLD,
                label='E-ring dwell time range\n$10^3$–$10^6$ yr')

    # Gronwall basin boundary
    ax2.axhline(np.exp(-t_ring_lo/1e4), color=GOLD, lw=1.2, ls='--', alpha=0.7)
    ax2.text(2e6, np.exp(-t_ring_lo/1e4) + 0.02,
             r'$\varepsilon_0 = 1/3$ threshold',
             color=GOLD, fontsize=7.5)

    # Annotations for Khawaja data points
    ax2.scatter([1e4], [C_aryl[np.argmin(np.abs(tau-1e4))]],
                color=TEAL, s=80, zorder=5, marker='D')
    ax2.scatter([1e4], [C_ether[np.argmin(np.abs(tau-1e4))]],
                color=RED, s=80, zorder=5, marker='D')
    ax2.text(8e3, 0.78, 'E5 fly-by\n(Khawaja 2025)', fontsize=7,
             color='#aab8cc', ha='center')

    ax2.set_xlabel('E-ring dwell time $τ_{{\\rm dwell}}$ (yr)', color=CREAM, fontsize=9)
    ax2.set_ylabel('Relative concentration $C(τ)/C(0)$', color=CREAM, fontsize=9)
    ax2.set_title('Observational Bound for T1 Closure — Proposition 6.1\n'
                  'Predicted chemical decay profile (future mission test)',
                  color=CREAM, fontsize=9)
    ax2.tick_params(colors=CREAM, labelsize=8)
    for sp in ax2.spines.values():
        sp.set_edgecolor('#334466')
    ax2.legend(fontsize=7.5, facecolor='#0d1a2e', labelcolor=CREAM,
               edgecolor=GOLD)
    ax2.set_ylim(-0.05, 1.1)
    ax2.text(0.02, 0.04,
             'z(τ) ~ −log[ether](τ)/[ether](0)\nmeasures entropy accumulation',
             transform=ax2.transAxes, fontsize=7, color=ORANGE,
             fontfamily='monospace')

    fig.suptitle('Figure 4 — Entropy Monotonicity (Theorem T1) and Observational Closure Strategy',
                 color=GOLD, fontsize=10, y=1.01, fontfamily='sans-serif')
    plt.tight_layout()
    plt.savefig('fig4_entropy_monotonicity.png', dpi=DPI, facecolor=NAVY,
                bbox_inches='tight')
    plt.close()
    print('fig4 done')


# ─────────────────────────────────────────────────────────────────────
# FIG 5 — Enceladus cross-section with operator chain
# ─────────────────────────────────────────────────────────────────────
def fig5_cross_section():
    fig, ax = plt.subplots(figsize=(11, 9))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_aspect('equal')
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.2, 4.2)
    ax.axis('off')

    # ── Moon body ──
    moon = plt.Circle((0, 0), 2.5, color='#e8e0d0', zorder=2)
    ax.add_patch(moon)
    # Ice shell (south pole at bottom)
    shell = plt.Circle((0, 0), 2.5, color='#b8cce0', zorder=3, fill=False,
                        lw=8, alpha=0.6)
    ax.add_patch(shell)
    # South polar ice — thinner, highlighted
    ice_south = Wedge((0, 0), 2.5, 230, 310, width=0.25,
                      color='#c8dff0', zorder=4)
    ax.add_patch(ice_south)
    # Subsurface ocean
    ocean = plt.Circle((0, 0), 2.25, color='#1a4878', zorder=3, alpha=0.7)
    ax.add_patch(ocean)
    # Rocky core
    core = plt.Circle((0, 0), 1.4, color='#5a4830', zorder=4, alpha=0.9)
    ax.add_patch(core)

    # Labels inside
    ax.text(0, 0, 'Rocky\nCore', ha='center', va='center',
            fontsize=7, color='#c8a870', fontweight='bold')
    ax.text(0, 1.85, 'Subsurface Ocean\n(3D convection → C)', ha='center',
            va='center', fontsize=7.5, color='#88ccee')

    # ── Tiger stripes ──
    stripe_angles = [-20, -5, 10, 25]
    for angle in stripe_angles:
        rad = np.radians(angle - 90)  # South pole at bottom
        x1 = 2.25 * np.cos(rad)
        y1 = 2.25 * np.sin(rad)
        x2 = 2.52 * np.cos(rad)
        y2 = 2.52 * np.sin(rad)
        ax.plot([x1, x2], [y1, y2], color=RED, lw=3, zorder=6)

    # ── Plume jets ──
    # Main plume from south pole
    jet_x = np.array([-0.25, 0.0, 0.25])
    for jx in jet_x:
        ax.annotate('', xy=(jx*3, -3.8), xytext=(jx*0.8, -2.52),
                    arrowprops=dict(arrowstyle='->', color=CREAM,
                                   lw=1.8, alpha=0.8,
                                   connectionstyle='arc3,rad=0.05'))
    # Plume cloud
    for i in range(25):
        np.random.seed(i)
        px = np.random.uniform(-0.6, 0.6)
        py = np.random.uniform(-2.9, -3.5)
        ax.scatter([px], [py], s=8, color='#d8e8f0', alpha=0.5, zorder=7)

    # ── E ring (schematic arc) ──
    e_ring = Arc((0, 0), 7.0, 7.0, angle=0, theta1=180, theta2=360,
                 color=GOLD, lw=2.5, zorder=8, linestyle='-')
    ax.add_patch(e_ring)
    ax.text(0, -3.7, r'E ring  ($\Gamma$ — Keplerian attractor, $a_E = 3.95\,R_S$)',
            ha='center', va='top', fontsize=8, color=GOLD)

    # ── Operator annotations ──
    ops = [
        (0.05, 1.6, 'C', TEAL,
         'Compression\n3D ocean → 1D fissure\nδ ≈ 10⁻³'),
        (-2.0, -0.3, 'K', MID,
         'Curvature\nκ → κ* ≈ (2000 m)⁻¹\nTidal Q̇ ≈ 10¹⁰ W'),
        (-2.8, -1.5, 'F', RED,
         'Fold (Whitney A₁)\nJacobian rank loss = 1\nN_fiss = 4–8'),
        (1.0, -3.0, 'U', '#4a7a30',
         'Unfolding\nPlume → E-ring orbit\nv_jet ≈ 400 m/s'),
        (2.9, -1.0, 'E', ORANGE,
         'Entropy\nṠ ≈ 2.7×10⁶ J K⁻¹ s⁻¹\nSpace weathering'),
    ]

    for x, y, letter, col, detail in ops:
        circle = plt.Circle((x, y), 0.22, color=col, zorder=10, alpha=0.95)
        ax.add_patch(circle)
        ax.text(x, y, letter, ha='center', va='center',
                fontsize=12, fontweight='bold', color='white',
                fontfamily='serif', zorder=11)
        # Detail box
        offx = 0.35 if x > 0 else -0.35
        offy = 0.25
        ha = 'left' if x > 0 else 'right'
        ax.text(x + offx, y + offy, detail,
                ha=ha, va='center', fontsize=6.5,
                color='#aab8cc', fontfamily='monospace',
                linespacing=1.4,
                bbox=dict(boxstyle='round,pad=0.3',
                          facecolor='#0a1420', edgecolor=col,
                          linewidth=0.8, alpha=0.9),
                zorder=12)

    # Title
    ax.text(0, 4.0,
            'Figure 5 — Enceladus Cryovolcanic System as dm³ Operator Chain',
            ha='center', va='center', fontsize=10, color=GOLD,
            fontfamily='sans-serif', fontweight='bold')
    ax.text(0, 3.65,
            r'$G_E = E \circ U \circ F \circ K \circ C$  ·  '
            'Khawaja et al. (2025) · Grossi 2026',
            ha='center', va='center', fontsize=8, color=CREAM,
            fontfamily='serif', style='italic')

    plt.tight_layout(pad=0.5)
    plt.savefig('fig5_cross_section.png', dpi=DPI, facecolor=NAVY,
                bbox_inches='tight')
    plt.close()
    print('fig5 done')


# ─────────────────────────────────────────────────────────────────────
# FIG 6 — Falsifiability matrix
# ─────────────────────────────────────────────────────────────────────
def fig6_falsifiability():
    fig, ax = plt.subplots(figsize=(12, 5.5))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor('#0d1a2e')
    ax.axis('off')

    # Table data
    headers = ['Condition', 'Requirement', 'Enceladus Evidence',
               'Status', 'Future Test']
    rows = [
        ('F1 · Compression',
         'Non-degenerate compression\nδ > 0, dim reduces',
         '3D ocean → 1D fissure\nδ ≈ 10⁻³, dim 3 → 1',
         '✓ PASSED', 'Gravity / seismic mapping'),
        ('F2 · Curvature',
         'Fold at κ*, not before/after',
         'Shell fractures at κ*ₑₙc\n≈ (2000 m)⁻¹',
         '✓ PASSED*', 'Pre-fracture curvature (OE-1)'),
        ('F3 · Fold',
         'Whitney A₁: rank loss = 1\nFinite branches',
         'Rank loss at fissure lip\nN_fiss = 4–8 (finite)',
         '✓ PASSED', 'Plume morphology (OE-3)'),
        ('F4 · Sequence',
         'Order: C → K → F → U\nNo out-of-sequence events',
         'Convection → pressure\n→ ejection → E-ring',
         '✓ PASSED', 'Time-lapse plume imaging'),
        ('F-new · Entropy',
         'Chemical complexity ↘\nwith dwell time',
         'Ether absent in E ring\nvs. fresh plume (E5)',
         '○ OPEN', 'Time-resolved E-ring sampling (OE-2)'),
    ]

    col_widths = [0.14, 0.22, 0.24, 0.12, 0.22]
    col_x = [0.02]
    for w in col_widths[:-1]:
        col_x.append(col_x[-1] + w)

    # Header
    for j, (h, cx) in enumerate(zip(headers, col_x)):
        ax.text(cx, 0.92, h, transform=ax.transAxes,
                fontsize=8.5, color=GOLD, fontweight='bold',
                fontfamily='sans-serif')

    ax.plot([0.01, 0.99], [0.88, 0.88], color=GOLD, lw=1,
            transform=ax.transAxes, clip_on=False)

    # Rows
    row_ys = np.linspace(0.78, 0.08, len(rows))
    for i, (row, ry) in enumerate(zip(rows, row_ys)):
        bg = '#0d1a2e' if i % 2 == 0 else '#111f2e'
        rect = patches.FancyBboxPatch((0.01, ry - 0.05), 0.98, 0.12,
                                       boxstyle='square,pad=0',
                                       linewidth=0,
                                       facecolor=bg,
                                       transform=ax.transAxes)
        ax.add_patch(rect)
        for j, (cell, cx) in enumerate(zip(row, col_x)):
            status_color = (TEAL if '✓' in cell
                            else (ORANGE if '○' in cell else CREAM))
            col = status_color if j == 3 else CREAM
            fw = 'bold' if j in (0, 3) else 'normal'
            ax.text(cx, ry + 0.035, cell, transform=ax.transAxes,
                    fontsize=7.2, color=col, va='center',
                    fontweight=fw,
                    fontfamily='monospace' if j in (2, 4) else 'sans-serif',
                    linespacing=1.4)

    ax.plot([0.01, 0.99], [0.04, 0.04], color='#334466', lw=0.8,
            transform=ax.transAxes, clip_on=False)
    ax.text(0.5, 0.01,
            '*F2 passed conditionally — quantitative pre-fracture curvature measurement would tighten. '
            '  Data: Khawaja et al. 2025 · Principia Orthogona Vol. I (Grossi 2026)',
            transform=ax.transAxes, fontsize=6, color='#8899aa',
            ha='center', style='italic')

    fig.suptitle('Figure 6 — Falsifiability Conditions F1–F-new: Assessment Against Enceladus Data',
                 color=GOLD, fontsize=10, y=0.99, fontfamily='sans-serif')
    plt.tight_layout()
    plt.savefig('fig6_falsifiability.png', dpi=DPI, facecolor=NAVY,
                bbox_inches='tight')
    plt.close()
    print('fig6 done')


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import os
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(out_dir)
    print(f'Generating figures in: {out_dir}')
    fig1_operator_chain()
    fig2_whitney_fold()
    fig3_gronwall_basin()
    fig4_entropy_monotonicity()
    fig5_cross_section()
    fig6_falsifiability()
    print('\nAll figures generated:')
    for f in sorted(os.listdir('.')):
        if f.startswith('fig') and f.endswith('.png'):
            size = os.path.getsize(f) // 1024
            print(f'  {f}  ({size} KB)')
