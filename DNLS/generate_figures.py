"""
generate_figures.py
===================
Publication-quality figures for:

  "Differential Nonlinear Robustness of Critical States in
   Fibonacci and Tribonacci Substitution Chains"
  Pablo Nogueira Grossi, G6 LLC (2026)
  Zenodo: 10.5281/zenodo.20026943

Figures produced
----------------
  fig1_chain_structure.pdf   — Chain structure diagram (substitution patterns + hoppings)
  fig2_eigenstates.pdf       — Mid-gap eigenstates |ψ_j|² for both chains (linear)
  fig3_ipr_vs_lambda.pdf     — IPR vs λ: differential nonlinear robustness (main result)
  fig4_ipr_ratio.pdf         — Tribonacci/Fibonacci IPR ratio vs λ
  fig5_phase_diagram.pdf     — Schematic phase diagram: localized / critical / delocalized

Usage
-----
  python generate_figures.py

Dependencies: numpy, scipy, matplotlib
"""

import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family':       'serif',
    'font.serif':        ['DejaVu Serif', 'Times New Roman', 'Georgia'],
    'font.size':         11,
    'axes.titlesize':    12,
    'axes.labelsize':    11,
    'xtick.labelsize':   9,
    'ytick.labelsize':   9,
    'legend.fontsize':   9,
    'figure.dpi':        150,
    'savefig.dpi':       300,
    'savefig.bbox':      'tight',
    'savefig.pad_inches':0.05,
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.linewidth':    0.8,
    'lines.linewidth':   1.8,
    'grid.alpha':        0.3,
    'grid.linewidth':    0.5,
})

# Colour palette (PRB-friendly, colour-blind safe)
COL_FIB  = '#2166ac'   # blue   — Fibonacci
COL_TRIB = '#d6604d'   # red    — Tribonacci
COL_GOLD = '#c9a84c'   # gold   — accent / ratio
COL_GREY = '#888888'

ETA = 1.8392867552141612   # tribonacci constant

# ── Import simulation utilities ───────────────────────────────────────────────
import sys
sys.path.insert(0, '/home/claude')
from dnls_nbonacci import (
    fibonacci_word, tribonacci_word,
    build_hamiltonian, mid_gap_state,
    ipr, evolve_dnls
)

# ── Shared simulation parameters ─────────────────────────────────────────────
N      = 500
T_MOD  = 0.5
T_EVO  = 50.0
LAMBDA = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]

print("Building chains …")
word_fib  = fibonacci_word(N + 1)
word_trib = tribonacci_word(N + 1)
H_fib,  hop_fib  = build_hamiltonian(word_fib,  N, T_MOD)
H_trib, hop_trib = build_hamiltonian(word_trib, N, T_MOD)
psi0_fib,  E_fib  = mid_gap_state(H_fib)
psi0_trib, E_trib = mid_gap_state(H_trib)

ipr0_fib  = ipr(psi0_fib)
ipr0_trib = ipr(psi0_trib)
print(f"  Fibonacci  E={E_fib:.4f}  IPR={ipr0_fib:.4f}")
print(f"  Tribonacci E={E_trib:.4f}  IPR={ipr0_trib:.4f}")

print("Running DNLS scans …")
ipr_fib_list  = [ipr0_fib]
ipr_trib_list = [ipr0_trib]
lam_plot = [0.0] + LAMBDA[1:]

for lam in LAMBDA[1:]:
    pf, _ = evolve_dnls(psi0_fib,  hop_fib,  lam, T_EVO)
    pt, _ = evolve_dnls(psi0_trib, hop_trib, lam, T_EVO)
    ipr_fib_list.append(ipr(pf))
    ipr_trib_list.append(ipr(pt))
    print(f"  λ={lam:.1f}  IPR_trib={ipr_trib_list[-1]:.4f}  IPR_fib={ipr_fib_list[-1]:.4f}")

ipr_fib_arr  = np.array(ipr_fib_list)
ipr_trib_arr = np.array(ipr_trib_list)
ratio_arr    = ipr_trib_arr / ipr_fib_arr
lam_arr      = np.array(lam_plot)

# ─────────────────────────────────────────────────────────────────────────────
# Fig 1 — Chain Structure Diagram
# ─────────────────────────────────────────────────────────────────────────────
print("\nFig 1: chain structure …")

def make_chain_diagram(ax, word, hops, n_show=30, label='', col_A='#2166ac', col_B='#d6604d', col_C='#4dac26'):
    hop_map = {0: 1.0, 1: T_MOD, 2: T_MOD**2}
    letter_col = {0: col_A, 1: col_B, 2: col_C}
    letter_sym = {0: 'A', 1: 'B', 2: 'C'}

    site_y = 0.5
    xs = np.linspace(0.04, 0.96, n_show)

    # bonds
    for i in range(n_show - 1):
        t = hop_map.get(word[i], T_MOD)
        lw = 1.0 + 3.5 * t
        ax.plot([xs[i], xs[i+1]], [site_y, site_y],
                color='#444444', lw=lw, solid_capstyle='round', zorder=1)
        # hopping label (every 5th)
        if i % 5 == 2:
            ax.text((xs[i]+xs[i+1])/2, site_y + 0.18,
                    f'{t:.2f}', ha='center', va='bottom',
                    fontsize=7, color='#555555')

    # sites
    for i in range(n_show):
        c = letter_col.get(word[i], col_A)
        ax.scatter(xs[i], site_y, s=120, color=c, zorder=3, linewidths=0.6,
                   edgecolors='white')
        ax.text(xs[i], site_y - 0.22, letter_sym.get(word[i], '?'),
                ha='center', va='top', fontsize=8, color=c, fontweight='bold')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(label, fontsize=11, pad=4)


fig1, axes = plt.subplots(2, 1, figsize=(8.5, 3.2))
fig1.suptitle('Substitution chain structures', fontsize=12, y=1.01)

make_chain_diagram(axes[0], word_fib,  hop_fib,  n_show=32,
                   label='Fibonacci chain  (A→AB, B→A;  $t_A=1.0$, $t_B=0.5$)',
                   col_A=COL_FIB, col_B=COL_TRIB)
make_chain_diagram(axes[1], word_trib, hop_trib, n_show=32,
                   label='Rauzy–Tribonacci chain  (A→AB, B→AC, C→A;  $t_A=1.0$, $t_B=0.5$, $t_C=0.25$)',
                   col_A=COL_FIB, col_B=COL_TRIB, col_C='#4dac26')

# Legend
from matplotlib.lines import Line2D
legend_els = [
    Line2D([0],[0], marker='o', color='w', markerfacecolor=COL_FIB,  markersize=8, label='Letter A  ($t=1.0$)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=COL_TRIB, markersize=8, label='Letter B  ($t=0.5$)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#4dac26',markersize=8, label='Letter C  ($t=0.25$, tribonacci only)'),
    Line2D([0],[0], color='#444', lw=3.5, label='Strong bond ($t=1.0$)'),
    Line2D([0],[0], color='#444', lw=1.5, label='Weak bond ($t=0.5$)'),
]
fig1.legend(handles=legend_els, loc='lower center', ncol=3,
            frameon=True, fontsize=8, bbox_to_anchor=(0.5, -0.18))

fig1.tight_layout()
fig1.savefig('/mnt/user-data/outputs/fig1_chain_structure.pdf')
fig1.savefig('/mnt/user-data/outputs/fig1_chain_structure.png')
print("  saved fig1")

# ─────────────────────────────────────────────────────────────────────────────
# Fig 2 — Mid-gap eigenstates |ψ_j|²
# ─────────────────────────────────────────────────────────────────────────────
print("Fig 2: eigenstates …")

sites = np.arange(N)
prob_fib  = np.abs(psi0_fib)**2
prob_trib = np.abs(psi0_trib)**2

fig2, (ax2a, ax2b) = plt.subplots(2, 1, figsize=(8.5, 5), sharex=True)
fig2.suptitle('Mid-gap critical eigenstates ($\\lambda = 0$)', fontsize=12)

ax2a.fill_between(sites, prob_fib, alpha=0.35, color=COL_FIB)
ax2a.plot(sites, prob_fib, color=COL_FIB, lw=0.8)
ax2a.set_ylabel('$|\\psi_j|^2$')
ax2a.set_title(f'Fibonacci chain   IPR = {ipr0_fib:.4f}', fontsize=10)
ax2a.text(0.97, 0.92, f'$E = {E_fib:.4f}$', transform=ax2a.transAxes,
          ha='right', va='top', fontsize=9, color=COL_GREY)

ax2b.fill_between(sites, prob_trib, alpha=0.35, color=COL_TRIB)
ax2b.plot(sites, prob_trib, color=COL_TRIB, lw=0.8)
ax2b.set_ylabel('$|\\psi_j|^2$')
ax2b.set_xlabel('Site $j$')
ax2b.set_title(f'Rauzy–Tribonacci chain   IPR = {ipr0_trib:.4f}  '
               f'($\\approx {ipr0_trib/ipr0_fib:.1f}\\times$ Fibonacci)', fontsize=10)
ax2b.text(0.97, 0.92, f'$E = {E_trib:.4f}$', transform=ax2b.transAxes,
          ha='right', va='top', fontsize=9, color=COL_GREY)

for ax in (ax2a, ax2b):
    ax.set_xlim(0, N-1)
    ax.grid(True, axis='y')

fig2.tight_layout()
fig2.savefig('/mnt/user-data/outputs/fig2_eigenstates.pdf')
fig2.savefig('/mnt/user-data/outputs/fig2_eigenstates.png')
print("  saved fig2")

# ─────────────────────────────────────────────────────────────────────────────
# Fig 3 — IPR vs λ (main result)
# ─────────────────────────────────────────────────────────────────────────────
print("Fig 3: IPR vs lambda …")

fig3, ax3 = plt.subplots(figsize=(6.5, 4.5))

ax3.plot(lam_arr, ipr_trib_arr, 'o-', color=COL_TRIB, label='Tribonacci ($n=3$)', markersize=5)
ax3.plot(lam_arr, ipr_fib_arr,  's--', color=COL_FIB,  label='Fibonacci ($n=2$)',  markersize=5)

# Annotate λ=1.5 crossover
lam15_idx = lam_arr.tolist().index(1.5)
ax3.annotate('',
    xy=(1.5, ipr_fib_arr[lam15_idx]),
    xytext=(1.5, ipr_trib_arr[lam15_idx]),
    arrowprops=dict(arrowstyle='<->', color=COL_GOLD, lw=1.5))
ax3.text(1.65, (ipr_fib_arr[lam15_idx] + ipr_trib_arr[lam15_idx])/2,
         f'$\\Delta$IPR at\n$\\lambda=1.5$',
         fontsize=8, color=COL_GOLD, va='center')

# Drop annotations
drop_fib  = (ipr_fib_arr[lam15_idx]  - ipr0_fib)  / ipr0_fib * 100
drop_trib = (ipr_trib_arr[lam15_idx] - ipr0_trib) / ipr0_trib * 100
ax3.text(0.97, 0.65,
         f'Fibonacci drop: {drop_fib:.0f}%\nTribonacci drop: {drop_trib:.0f}%\n(at $\\lambda=1.5$)',
         transform=ax3.transAxes, ha='right', va='top',
         fontsize=9, color='#333333',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cccccc', alpha=0.9))

# Linear limit markers
ax3.axhline(ipr0_fib,  color=COL_FIB,  lw=0.7, ls=':', alpha=0.5)
ax3.axhline(ipr0_trib, color=COL_TRIB, lw=0.7, ls=':', alpha=0.5)

ax3.set_xlabel('Nonlinearity strength $\\lambda$')
ax3.set_ylabel('Inverse participation ratio (IPR)')
ax3.set_title('Differential nonlinear robustness\nof mid-gap critical states', fontsize=11)
ax3.legend(loc='upper right', frameon=True)
ax3.set_xlim(-0.2, 10.5)
ax3.set_ylim(0)
ax3.grid(True)

# η annotation
ax3.text(0.03, 0.06,
         f'$\\eta \\approx {ETA:.4f}$  (tribonacci constant)',
         transform=ax3.transAxes, fontsize=8, color=COL_GREY,
         style='italic')

fig3.tight_layout()
fig3.savefig('/mnt/user-data/outputs/fig3_ipr_vs_lambda.pdf')
fig3.savefig('/mnt/user-data/outputs/fig3_ipr_vs_lambda.png')
print("  saved fig3")

# ─────────────────────────────────────────────────────────────────────────────
# Fig 4 — IPR ratio tribonacci/fibonacci vs λ
# ─────────────────────────────────────────────────────────────────────────────
print("Fig 4: IPR ratio …")

fig4, ax4 = plt.subplots(figsize=(6.5, 4))

ax4.plot(lam_arr, ratio_arr, 'D-', color=COL_GOLD, markersize=5, label='IPR ratio trib/fib')
ax4.axhline(ratio_arr[0], color=COL_GREY, lw=0.8, ls='--',
            label=f'Linear limit: {ratio_arr[0]:.2f}')
ax4.axhline(1.0, color='#333333', lw=0.6, ls=':')
ax4.text(10.1, 1.02, '1', fontsize=8, color='#333333')

ax4.fill_between(lam_arr, ratio_arr, 1.0,
                 where=(ratio_arr > 1), alpha=0.12, color=COL_GOLD,
                 label='Tribonacci more localized')

ax4.set_xlabel('Nonlinearity strength $\\lambda$')
ax4.set_ylabel('IPR$_{\\mathrm{trib}}$ / IPR$_{\\mathrm{fib}}$')
ax4.set_title('Localization advantage of tribonacci chain\nunder nonlinear perturbation', fontsize=11)
ax4.legend(frameon=True)
ax4.set_xlim(-0.2, 10.5)
ax4.grid(True)

fig4.tight_layout()
fig4.savefig('/mnt/user-data/outputs/fig4_ipr_ratio.pdf')
fig4.savefig('/mnt/user-data/outputs/fig4_ipr_ratio.png')
print("  saved fig4")

# ─────────────────────────────────────────────────────────────────────────────
# Fig 5 — Schematic substitution tree / fractal diagram
# ─────────────────────────────────────────────────────────────────────────────
print("Fig 5: substitution diagram …")

fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(9, 5))
fig5.suptitle('Substitution rules and spectrum schematic', fontsize=12)

def draw_substitution_tree(ax, rules, letters, colors, title, generations=4):
    """Draw a tree showing the substitution expansion."""
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.05)
    ax.axis('off')
    ax.set_title(title, fontsize=10, pad=6)

    gen_height = 1.0 / generations
    y_positions = [1.0 - (i + 0.5) * gen_height for i in range(generations)]
    ax.text(0.01, y_positions[0] + gen_height*0.3, 'Gen 0', fontsize=8, color=COL_GREY, va='center')

    word = [0]
    prev_positions = {0: [0.5]}

    for g in range(generations):
        y = y_positions[g]
        ax.text(0.01, y + gen_height*0.3, f'Gen {g}', fontsize=7, color=COL_GREY, va='center')

        # Draw current word
        n = len(word)
        xs = np.linspace(0.08, 0.98, n)
        for i, (letter, x) in enumerate(zip(word, xs)):
            col = colors[letter]
            ax.scatter(x, y, s=200/(g+1)**0.5 + 20, color=col,
                       zorder=3, edgecolors='white', linewidths=0.5)
            if g < 3:
                ax.text(x, y, letters[letter], ha='center', va='center',
                        fontsize=max(5, 9-g*1.5), color='white', fontweight='bold')

        # Draw lines to next generation
        if g < generations - 1:
            new_word = [s for c in word for s in rules[c]]
            new_n = len(new_word)
            new_xs = np.linspace(0.08, 0.98, new_n)
            next_y = y_positions[g+1]

            # Map old positions to new
            pos = 0
            for i, (letter, x) in enumerate(zip(word, xs)):
                expanded = rules[letter]
                for j, child in enumerate(expanded):
                    child_x = new_xs[pos]
                    ax.plot([x, child_x], [y - 0.02, next_y + 0.02],
                            color=colors[child], alpha=0.25, lw=0.6)
                    pos += 1
            word = new_word

# Fibonacci
fib_rules  = {0: [0, 1], 1: [0]}
fib_letters = {0: 'A', 1: 'B'}
fib_colors  = {0: COL_FIB, 1: COL_TRIB}
draw_substitution_tree(ax5a, fib_rules, fib_letters, fib_colors,
                       'Fibonacci: A→AB, B→A\n$\\phi$-scaling, $n=2$', generations=5)

# Tribonacci
trib_rules   = {0: [0,1], 1: [0,2], 2: [0]}
trib_letters = {0: 'A', 1: 'B', 2: 'C'}
trib_colors  = {0: COL_FIB, 1: COL_TRIB, 2: '#4dac26'}
draw_substitution_tree(ax5b, trib_rules, trib_letters, trib_colors,
                       f'Rauzy–Tribonacci: A→AB, B→AC, C→A\n$\\eta \\approx {ETA:.4f}$-scaling, $n=3$', generations=5)

# Shared legend
legend_els2 = [
    mpatches.Patch(color=COL_FIB,    label='Letter A'),
    mpatches.Patch(color=COL_TRIB,   label='Letter B'),
    mpatches.Patch(color='#4dac26',  label='Letter C (tribonacci only)'),
]
fig5.legend(handles=legend_els2, loc='lower center', ncol=3,
            frameon=True, fontsize=9, bbox_to_anchor=(0.5, -0.04))

fig5.tight_layout()
fig5.savefig('/mnt/user-data/outputs/fig5_substitution_tree.pdf')
fig5.savefig('/mnt/user-data/outputs/fig5_substitution_tree.png')
print("  saved fig5")

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("All figures saved to /mnt/user-data/outputs/")
print("="*60)
print(f"\nKey numerical results:")
print(f"  Linear IPR ratio (trib/fib): {ratio_arr[0]:.2f}x")
print(f"  Fibonacci IPR drop at λ=1.5: {drop_fib:.0f}%")
print(f"  Tribonacci IPR drop at λ=1.5: {drop_trib:.0f}%")
print(f"  η = {ETA:.9f}")
