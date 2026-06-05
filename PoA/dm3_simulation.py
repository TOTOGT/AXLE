"""
dm3_simulation.py — TOGT/GTCT contact manifold simulation
G6 LLC · Pablo Nogueira Grossi · 2026
github.com/TOTOGT/AXLE

Simulates the dm³ contact 3-manifold:
    ṙ = r(1 - r²) + 2(r-1)·exp(-r)
    θ̇ = 1
    ż = r² - 2(r-1)²·exp(-r)

Produces:
  1. Phase portrait in (r, z) with limit cycle Γ = {r=1}
  2. Basin hierarchy diagram showing ε₀, 2/3, r*, κ* boundaries
  3. Spiral return: G⁶⁴(x₀) ≠ x₀ — orbit divergence from periodicity
  4. g-series regime plot: consecutive iterate distances vs. n
  5. κ* bifurcation: catastrophe probability vs. κ perturbation
     (biological analogue: anesthetic concentration vs. MT catastrophe rate)
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ── Parameters ──────────────────────────────────────────────
EPS0   = 1/3          # outer basin boundary
R_ATT  = 1.0          # limit cycle radius
KSTAR  = 0.882        # curvature threshold
RSTAR  = 0.773        # inner basin boundary (DOP853, rtol=1e-10)
TSTAR  = 2 * np.pi    # period
MU_MAX = -2.0         # transverse Lyapunov exponent

COLORS = {
    'limit_cycle': '#0ABAB5',
    'basin_outer': '#c8a24a',
    'basin_inner': '#e91e8c',
    'kstar':       '#ff6b35',
    'orbit':       '#9cf3ef',
    'stable':      '#50c878',
    'unstable':    '#c94c4c',
    'bg':          '#06070d',
    'grid':        '#1e2540',
    'text':        '#eef0f7',
}

def dm3_rhs(t, state):
    r, theta, z = state
    r = max(r, 1e-10)
    rdot = r * (1 - r**2) + 2*(r-1)*np.exp(-r)
    tdot = 1.0
    zdot  = r**2 - 2*(r-1)**2 * np.exp(-r)
    return [rdot, tdot, zdot]

def integrate(r0, theta0, z0, t_end, n_points=5000):
    sol = solve_ivp(
        dm3_rhs, [0, t_end],
        [r0, theta0, z0],
        method='DOP853',
        rtol=1e-10, atol=1e-12,
        dense_output=True
    )
    t = np.linspace(0, t_end, n_points)
    return t, sol.sol(t)

# ── Figure setup ─────────────────────────────────────────────
fig = plt.figure(figsize=(18, 14), facecolor=COLORS['bg'])
gs  = GridSpec(3, 3, figure=fig, hspace=0.42, wspace=0.38,
               left=0.07, right=0.97, top=0.94, bottom=0.06)

def style_ax(ax, title=''):
    ax.set_facecolor(COLORS['bg'])
    ax.tick_params(colors=COLORS['text'], labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS['grid'])
    ax.grid(True, color=COLORS['grid'], linewidth=0.4, alpha=0.5)
    ax.xaxis.label.set_color(COLORS['text'])
    ax.yaxis.label.set_color(COLORS['text'])
    if title:
        ax.set_title(title, color=COLORS['text'], fontsize=9, pad=6,
                     fontweight='bold')

# ── Panel 1: Phase portrait (r, ṙ) ──────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1, 'Phase portrait: r vs ṙ')

r_vals = np.linspace(0.01, 2.0, 500)
rdot_vals = r_vals*(1 - r_vals**2) + 2*(r_vals-1)*np.exp(-r_vals)
ax1.plot(r_vals, rdot_vals, color=COLORS['limit_cycle'], lw=1.5, label='ṙ(r)')
ax1.axhline(0, color=COLORS['text'], lw=0.5, alpha=0.4)
ax1.axvline(1.0, color=COLORS['limit_cycle'], lw=1.0, ls='--', alpha=0.6,
            label=f'Γ: r=1')
ax1.axvline(KSTAR, color=COLORS['kstar'], lw=1.0, ls=':', alpha=0.8,
            label=f'κ*≈{KSTAR}')
ax1.axvline(RSTAR, color=COLORS['basin_inner'], lw=1.0, ls=':', alpha=0.7,
            label=f'r*≈{RSTAR}')
ax1.fill_betweenx([-0.6, 0.4], RSTAR, KSTAR,
                  color=COLORS['basin_outer'], alpha=0.08)
ax1.set_xlabel('r'); ax1.set_ylabel('ṙ')
ax1.set_xlim(0, 2); ax1.set_ylim(-0.6, 0.4)
ax1.legend(fontsize=7, facecolor='#0c0f1c', edgecolor=COLORS['grid'],
           labelcolor=COLORS['text'], loc='upper right')

# ── Panel 2: Basin hierarchy ──────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2, 'Basin hierarchy')

y = 0.5
h = 0.25
boundaries = [
    (0,       EPS0,   COLORS['basin_inner'], 'inner basin [0, ε₀]'),
    (EPS0,    2/3,    '#444',                '[ε₀, 2/3]'),
    (2/3,     RSTAR,  '#555',                '[2/3, r*]'),
    (RSTAR,   KSTAR,  COLORS['basin_outer'], '[r*, κ*] admissible'),
    (KSTAR,   1.0,    COLORS['kstar'],       '[κ*, 1] transition'),
    (1.0,     1.0+EPS0, COLORS['limit_cycle'],'Γ + outer ε₀'),
]
for (x0, x1, col, lbl) in boundaries:
    ax2.barh(y, x1-x0, left=x0, height=h, color=col, alpha=0.6,
             edgecolor=COLORS['grid'], linewidth=0.5)

for val, lbl, col in [
    (EPS0,  f'ε₀={EPS0:.3f}', COLORS['text']),
    (2/3,   '2/3',            COLORS['text']),
    (RSTAR, f'r*≈{RSTAR}',   COLORS['basin_inner']),
    (KSTAR, f'κ*≈{KSTAR}',   COLORS['kstar']),
    (1.0,   'Γ',             COLORS['limit_cycle']),
]:
    ax2.axvline(val, color=col, lw=1.0, ls='--', alpha=0.7, ymin=0.1, ymax=0.9)
    ax2.text(val, y + h*0.7, lbl, color=col, fontsize=7,
             ha='center', va='bottom', rotation=45)

ax2.set_xlim(0, 1.4); ax2.set_ylim(0.1, 1.1)
ax2.set_xlabel('r'); ax2.set_yticks([])
ax2.set_title('Basin hierarchy: 0 < ε₀ < 2/3 < r* < κ* < 1',
              color=COLORS['text'], fontsize=8, pad=6)

# ── Panel 3: Limit cycle in (r, z) ───────────────────────────
ax3 = fig.add_subplot(gs[0, 2])
style_ax(ax3, 'Limit cycle Γ in (r, z)')

for r0, col, alpha in [(0.3, COLORS['basin_inner'], 0.7),
                        (0.6, COLORS['basin_outer'], 0.7),
                        (1.5, COLORS['stable'],      0.7),
                        (1.2, COLORS['orbit'],       0.5)]:
    t, Y = integrate(r0, 0, 0, 8*TSTAR, 2000)
    ax3.plot(Y[0], Y[2], color=col, lw=0.8, alpha=alpha)

# Limit cycle
t_lc, Y_lc = integrate(1.0, 0, 0, TSTAR*1.02, 500)
ax3.plot(Y_lc[0], Y_lc[2], color=COLORS['limit_cycle'], lw=2.5,
         label='Γ (limit cycle)')
ax3.set_xlabel('r'); ax3.set_ylabel('z')
ax3.legend(fontsize=7, facecolor='#0c0f1c', edgecolor=COLORS['grid'],
           labelcolor=COLORS['text'])

# ── Panel 4: Spiral return — G⁶⁴(x₀) ≠ x₀ ──────────────────
ax4 = fig.add_subplot(gs[1, 0:2])
style_ax(ax4, 'Spiral return (Theorem T1): G⁶⁴(x₀) ≠ x₀')

# Integrate two initial conditions close together
r0a, r0b = 0.7, 0.72
t_long = 64 * TSTAR
t, Ya = integrate(r0a, 0, 0, t_long, 8000)
t, Yb = integrate(r0b, 0, 0, t_long, 8000)

ax4.plot(t / TSTAR, Ya[0], color=COLORS['orbit'], lw=1.0,
         label=f'r₀={r0a}', alpha=0.9)
ax4.plot(t / TSTAR, Yb[0], color=COLORS['basin_outer'], lw=1.0,
         label=f'r₀={r0b}', alpha=0.9)
ax4.axhline(1.0, color=COLORS['limit_cycle'], lw=1.0, ls='--', alpha=0.6,
            label='Γ: r=1')

# Mark g-regime thresholds
for g, col, lbl in [(1, '#333', 'g¹'), (6, '#555', 'g⁶'),
                     (33, COLORS['kstar'], 'g³³'), (64, COLORS['limit_cycle'], 'g⁶⁴')]:
    ax4.axvline(g, color=col, lw=0.8, ls=':', alpha=0.7)
    ax4.text(g+0.5, 1.55, lbl, color=col, fontsize=7)

ax4.set_xlabel('Cycles (n = t/T*)'); ax4.set_ylabel('r(t)')
ax4.set_xlim(0, 64); ax4.set_ylim(0.2, 1.7)
ax4.legend(fontsize=7, facecolor='#0c0f1c', edgecolor=COLORS['grid'],
           labelcolor=COLORS['text'], loc='upper right')

# ── Panel 5: g-series — consecutive iterate distances ─────────
ax5 = fig.add_subplot(gs[1, 2])
style_ax(ax5, 'g-series: ‖Gⁿx − Gⁿ⁺¹x‖ vs n')

# Simulate discrete iterates by sampling at multiples of T*
r0 = 0.5
t_series, Y_series = integrate(r0, 0, 0, 70*TSTAR, 14000)
# Sample at each full cycle
sample_idx = [np.argmin(np.abs(t_series - n*TSTAR)) for n in range(1, 70)]
r_samples = Y_series[0][sample_idx]
dists = np.abs(np.diff(r_samples))
ns = np.arange(1, len(dists)+1)

ax5.semilogy(ns, dists, color=COLORS['orbit'], lw=1.2, marker='o',
             markersize=2, alpha=0.8)
ax5.axvline(33, color=COLORS['kstar'], lw=1.5, ls='--', alpha=0.8,
            label=f'n=33 (g³³ threshold)')
ax5.axhline(RSTAR, color=COLORS['basin_inner'], lw=1.0, ls=':', alpha=0.7,
            label=f'r*={RSTAR}')
ax5.set_xlabel('Cycle n'); ax5.set_ylabel('‖Gⁿx − Gⁿ⁺¹x‖ (log)')
ax5.legend(fontsize=7, facecolor='#0c0f1c', edgecolor=COLORS['grid'],
           labelcolor=COLORS['text'])

# ── Panel 6: Operator chain — riboswitch analogue ─────────────
ax6 = fig.add_subplot(gs[2, 0])
style_ax(ax6, 'Operator chain: riboswitch mapping')

ops  = ['C\nAptamer\nbinding', 'K\nSD\nsequester', 'F\nStem\nbifurcation',
        'U\nSD\nexposure', 'T\nResistance\ncycle']
cols = ['#4a9eff', '#e05a3a', '#50c878', '#c084fc', COLORS['limit_cycle']]
xs   = [0.12, 0.30, 0.50, 0.68, 0.88]

for i, (op, col, x) in enumerate(zip(ops, cols, xs)):
    circ = plt.Circle((x, 0.5), 0.09, color=col, alpha=0.85, zorder=3)
    ax6.add_patch(circ)
    ax6.text(x, 0.5, op, ha='center', va='center', fontsize=6.5,
             color='white', fontweight='bold', zorder=4)
    if i < len(ops)-1:
        ax6.annotate('', xy=(xs[i+1]-0.09, 0.5), xytext=(x+0.09, 0.5),
                     arrowprops=dict(arrowstyle='->', color=COLORS['text'],
                                     lw=1.2), zorder=5)

# OFF/ON labels
ax6.text(0.12, 0.18, 'OFF state', ha='center', fontsize=7,
         color=COLORS['basin_inner'])
ax6.text(0.88, 0.18, 'ON state', ha='center', fontsize=7,
         color=COLORS['stable'])
ax6.text(0.50, 0.08, 'κ* barrier', ha='center', fontsize=7,
         color=COLORS['kstar'])
ax6.annotate('', xy=(0.50, 0.20), xytext=(0.50, 0.12),
             arrowprops=dict(arrowstyle='->', color=COLORS['kstar'], lw=1.0))

ax6.set_xlim(0, 1); ax6.set_ylim(0, 1); ax6.set_xticks([]); ax6.set_yticks([])

# ── Panel 7: κ* bifurcation — anesthesia analogue ────────────
ax7 = fig.add_subplot(gs[2, 1])
style_ax(ax7, 'κ* shift: anesthetic vs. stabiliser')

# Simple model: catastrophe probability ~ sigmoid of (κ - κ*_eff)
kappa_range = np.linspace(0.5, 1.3, 300)
def catastrophe_prob(kappa, kstar_eff, steepness=15):
    return 1 / (1 + np.exp(-steepness*(kstar_eff - kappa)))

# Baseline (no drug)
p_base = catastrophe_prob(kappa_range, KSTAR)
# Anesthetic: shifts κ* downward by 0.08 (raises catastrophe at lower kappa)
p_anes = catastrophe_prob(kappa_range, KSTAR - 0.08)
# Stabiliser (epothilone): shifts κ* upward by 0.06
p_stab = catastrophe_prob(kappa_range, KSTAR + 0.06)

ax7.plot(kappa_range, p_base, color=COLORS['limit_cycle'], lw=2,
         label='Baseline (no drug)')
ax7.plot(kappa_range, p_anes, color=COLORS['kstar'], lw=2, ls='--',
         label='Anesthetic: κ*↓0.08')
ax7.plot(kappa_range, p_stab, color=COLORS['stable'], lw=2, ls='-.',
         label='Epothilone B: κ*↑0.06')
ax7.axvline(KSTAR, color=COLORS['text'], lw=0.8, ls=':', alpha=0.5)
ax7.text(KSTAR+0.02, 0.5, f'κ*={KSTAR}', color=COLORS['text'], fontsize=7)
ax7.set_xlabel('Local curvature κ')
ax7.set_ylabel('P(catastrophe)')
ax7.legend(fontsize=7, facecolor='#0c0f1c', edgecolor=COLORS['grid'],
           labelcolor=COLORS['text'])
ax7.set_xlim(0.5, 1.3); ax7.set_ylim(-0.05, 1.05)

# ── Panel 8: Cross-domain morphism transfer ───────────────────
ax8 = fig.add_subplot(gs[2, 2])
style_ax(ax8, 'Coherence Bridge: dose-response transfer')

# The TOGT prediction: riboswitch antagonist dose-response (domain 1)
# has the SAME functional form as epothilone dose-response (domain 3)
conc = np.linspace(0, 5, 300)
def switch_prob(c, EC50=2.0, hill=2.0):
    return c**hill / (EC50**hill + c**hill)

p_ribo  = switch_prob(conc, EC50=2.0, hill=1.8)   # riboswitch OFF-lock
p_mt    = switch_prob(conc, EC50=2.3, hill=2.1)   # MT stabilisation
p_ngs   = switch_prob(conc, EC50=1.7, hill=1.5)   # NGS cluster quality

ax8.plot(conc, p_ribo, color='#4a9eff', lw=2,
         label='Riboswitch OFF-lock\n(antagonist conc.)')
ax8.plot(conc, p_mt, color=COLORS['stable'], lw=2, ls='--',
         label='MT stabilisation\n(epothilone B, μg/kg)')
ax8.plot(conc, p_ngs, color=COLORS['basin_outer'], lw=2, ls='-.',
         label='NGS cluster quality\n(primer density, a.u.)')
ax8.set_xlabel('Concentration / dose (a.u.)')
ax8.set_ylabel('Response probability')
ax8.legend(fontsize=6.5, facecolor='#0c0f1c', edgecolor=COLORS['grid'],
           labelcolor=COLORS['text'])
ax8.text(0.05, 0.92, 'Contact morphism f₁₃ predicts\nidentical functional form',
         transform=ax8.transAxes, color=COLORS['kstar'], fontsize=7,
         va='top', style='italic')

# ── Global title ──────────────────────────────────────────────
fig.text(0.5, 0.97,
         'TOGT/GTCT dm³ Contact Manifold — Simulation & Coherence Bridge',
         ha='center', va='top', color=COLORS['text'], fontsize=11,
         fontweight='bold')
fig.text(0.5, 0.955,
         'G6 LLC · Pablo Nogueira Grossi · ORCID 0009-0000-6496-2186 · '
         'github.com/TOTOGT/AXLE · 2026',
         ha='center', va='top', color='#7a8199', fontsize=8)

plt.savefig('/home/claude/dm3_figures.pdf', dpi=150, bbox_inches='tight',
            facecolor=COLORS['bg'])
plt.savefig('/home/claude/dm3_figures.png', dpi=150, bbox_inches='tight',
            facecolor=COLORS['bg'])
print("Saved: dm3_figures.pdf, dm3_figures.png")

# ── Also save individual panels for LaTeX inclusion ───────────
fig2, ax_single = plt.subplots(1, 1, figsize=(6, 4), facecolor=COLORS['bg'])
style_ax(ax_single, 'Phase portrait + basin hierarchy')
ax_single.plot(r_vals, rdot_vals, color=COLORS['limit_cycle'], lw=2)
ax_single.axhline(0, color=COLORS['text'], lw=0.5, alpha=0.4)
for val, col, lbl in [(EPS0, COLORS['basin_outer'], 'ε₀'),
                       (RSTAR, COLORS['basin_inner'], 'r*'),
                       (KSTAR, COLORS['kstar'], 'κ*'),
                       (1.0,  COLORS['limit_cycle'], 'Γ')]:
    ax_single.axvline(val, color=col, lw=1.2, ls='--', alpha=0.8)
    ax_single.text(val+0.01, 0.32, lbl, color=col, fontsize=9)
ax_single.set_xlabel('r'); ax_single.set_ylabel('ṙ = dr/dt')
ax_single.set_xlim(0, 2); ax_single.set_ylim(-0.65, 0.42)
fig2.savefig('/home/claude/fig_phase_portrait.pdf', dpi=150,
             bbox_inches='tight', facecolor=COLORS['bg'])
plt.close('all')
print("Saved: fig_phase_portrait.pdf")
