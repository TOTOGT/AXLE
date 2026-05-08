#!/usr/bin/env python3
"""
generate_all_figures.py
=======================
Generates all 5 figures for:
  "Criticality Thresholds in 1D Multiplying Media with n-Bonacci Modulation"

Fig 1 — Chain structure: substitution word visualized for Fibonacci & Tribonacci
Fig 2 — k_eff vs lambda: Fibonacci generations 4,6,8
Fig 3 — lambda_c(n) vs spectral gap Delta_n with linear fit
Fig 4 — Convergence of k_eff with generation (Fibonacci & Tribonacci)
Fig 5 — Fundamental flux modes: spatial profiles for Fibonacci gen 5 & 8

Author: Pablo Nogueira Grossi | G6 LLC | 2026 | MIT
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.linalg import eig
from scipy.optimize import brentq

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'text.usetex': False,
})

OUT = "/mnt/user-data/outputs"

# -------------------------------------------------------------------------
# Core functions
# -------------------------------------------------------------------------

def nbonacci_word(n, n_gen):
    rules = {}
    for k in range(n):
        if k == 0:   rules[k] = [0, 1] if n > 1 else [0]
        elif k < n-1: rules[k] = [0, k+1]
        else:          rules[k] = [0]
    word = [0]
    for _ in range(n_gen):
        word = [s for c in word for s in rules[c]]
    return word

def build_and_solve(word, lam):
    arr = np.array(word)
    D  = np.ones(len(arr))
    Sr = np.where(arr == 0, 0.5, 2.0)
    Sf = np.where(arr == 0, lam, 0.0).astype(float)
    N  = len(D)
    D_half = np.zeros(N+1)
    D_half[0] = D[0]; D_half[N] = D[N-1]
    for i in range(N-1):
        D_half[i+1] = 2*D[i]*D[i+1]/(D[i]+D[i+1])
    L = np.zeros((N, N))
    for i in range(N):
        L[i,i] = D_half[i] + D_half[i+1] + Sr[i]
        if i > 0:   L[i,i-1] = -D_half[i]
        if i < N-1: L[i,i+1] = -D_half[i+1]
    vals, vecs = eig(np.diag(Sf), L)
    idx = np.argmax(vals.real)
    k   = float(vals[idx].real)
    phi = vecs[:, idx].real
    phi = phi / np.max(np.abs(phi))
    return k, phi

def find_lambda_c(n, g, tol=1e-9):
    word = nbonacci_word(n, g)
    f = lambda lam: build_and_solve(word, lam)[0] - 1.0
    if f(6.0) < 0: return np.nan
    if f(0.3) > 0: return 0.3
    return brentq(f, 0.3, 6.0, xtol=tol)

def spectral_gap(n):
    coeffs = [1] + [-1]*n
    roots  = np.roots(coeffs)
    s = sorted(np.abs(roots), reverse=True)
    return s[0], s[1], s[0]-s[1]

# -------------------------------------------------------------------------
# Figure 1 — Chain structure visualization
# -------------------------------------------------------------------------

def fig1_chain_structure():
    fig, axes = plt.subplots(2, 1, figsize=(12, 3.5))

    COLORS = {0: '#2166ac', 1: '#d6604d', 2: '#4dac26'}
    LABELS = {0: 'A (fissile)', 1: 'B (absorber)', 2: 'C (absorber)'}

    for ax, (n, name, gen) in zip(axes, [(2, 'Fibonacci', 7), (3, 'Tribonacci', 6)]):
        word = nbonacci_word(n, gen)[:80]  # show first 80 sites
        for i, s in enumerate(word):
            ax.add_patch(mpatches.Rectangle(
                (i, 0), 0.9, 1,
                color=COLORS[s], linewidth=0
            ))
        ax.set_xlim(0, len(word))
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xlabel('Site index $i$')
        ax.set_title(f'{name} chain (first {len(word)} sites, gen {gen})')

        # legend
        patches = [mpatches.Patch(color=COLORS[s], label=LABELS[s])
                   for s in sorted(set(word))]
        ax.legend(handles=patches, loc='upper right', framealpha=0.9)

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig1_chain_structure.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Fig 1 saved.")

# -------------------------------------------------------------------------
# Figure 2 — k_eff vs lambda, Fibonacci generations
# -------------------------------------------------------------------------

def fig2_keff_vs_lambda():
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    lam_vals = np.linspace(0.4, 2.5, 100)

    GENS = [4, 6, 8]
    COLORS_FIB = ['#92c5de', '#4393c3', '#2166ac']
    COLORS_TRI = ['#f4a582', '#d6604d', '#b2182b']

    for ax, (n, name, colors) in zip(axes, [
        (2, 'Fibonacci', COLORS_FIB),
        (3, 'Tribonacci', COLORS_TRI)
    ]):
        for g, col in zip(GENS, colors):
            word = nbonacci_word(n, g)
            ks   = [build_and_solve(word, lam)[0] for lam in lam_vals]
            ax.plot(lam_vals, ks, color=col, lw=1.8,
                    label=f'gen {g}  (N={len(word)})')
        ax.axhline(1.0, color='k', lw=0.9, ls='--', label='$k=1$ (critical)')
        ax.set_xlabel(r'$\lambda$ (fission strength)')
        ax.set_ylabel(r'$k_{\rm eff}$')
        ax.set_title(f'{name} chain: $k_{{\\rm eff}}$ vs $\\lambda$')
        ax.legend(); ax.grid(alpha=0.25)
        ax.set_ylim(0.3, 1.6)

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig2_keff_vs_lambda.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Fig 2 saved.")

# -------------------------------------------------------------------------
# Figure 3 — lambda_c(n) vs spectral gap with linear fit
# -------------------------------------------------------------------------

def fig3_lambda_c_vs_gap():
    gen_map = {2: 10, 3: 9, 4: 9, 5: 8}
    ns   = [2, 3, 4, 5]
    gaps, lcs, rhos = [], [], []

    for n in ns:
        r1, r2, gap = spectral_gap(n)
        lc = find_lambda_c(n, gen_map[n])
        rhos.append(r1); gaps.append(gap); lcs.append(lc)

    p    = np.polyfit(gaps, lcs, 1)
    xfit = np.linspace(min(gaps)*0.97, max(gaps)*1.03, 80)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left: lambda_c vs gap
    ax = axes[0]
    sc = ax.scatter(gaps, lcs, c=ns, cmap='viridis', s=120, zorder=5)
    for i, n in enumerate(ns):
        ax.annotate(f'$n={n}$', (gaps[i], lcs[i]),
                    textcoords='offset points', xytext=(8, 4))
    ax.plot(xfit, np.polyval(p, xfit), '--', color='gray', lw=1.4,
            label=f'fit: $\\lambda_c \\approx {p[0]:.3f}\\,\\Delta_n + {p[1]:.3f}$\n'
                  f'$r = {np.corrcoef(gaps,lcs)[0,1]:.4f}$')
    ax.set_xlabel(r'Spectral gap $\Delta_n = \rho_n - |\rho_n^{(2)}|$')
    ax.set_ylabel(r'$\lambda_c(n)$')
    ax.set_title(r'Critical fission strength vs spectral gap')
    ax.legend(); ax.grid(alpha=0.25)

    # Right: lambda_c, Delta_n, rho_n vs n
    ax = axes[1]
    ax.plot(ns, lcs,  'o-', color='steelblue', ms=8, label=r'$\lambda_c(n)$')
    ax.plot(ns, gaps, 's--', color='tomato',   ms=8, label=r'$\Delta_n = \rho_n - |\rho_n^{(2)}|$')
    ax.plot(ns, rhos, '^:',  color='seagreen', ms=8, label=r'$\rho_n$ (n-bonacci const.)')
    ax.axhline(7/6, color='purple', lw=0.8, ls='-.', alpha=0.7, label='$7/6$')
    ax.set_xlabel('$n$ (substitution order)')
    ax.set_ylabel('Value')
    ax.set_title(r'$\lambda_c$, $\Delta_n$, and $\rho_n$ vs $n$')
    ax.set_xticks(ns); ax.legend(); ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig3_lambda_c_gap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Fig 3 saved.")

# -------------------------------------------------------------------------
# Figure 4 — Convergence of k_eff with generation
# -------------------------------------------------------------------------

def fig4_convergence():
    lam_crit = find_lambda_c(2, 10)  # Fibonacci thermodynamic-limit lambda_c

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left: k_eff vs N at fixed lambda = lambda_c(Fibonacci)
    ax = axes[0]
    for n, name, col in [(2,'Fibonacci','steelblue'), (3,'Tribonacci','tomato')]:
        Ns, ks = [], []
        for g in range(3, 11):
            word = nbonacci_word(n, g)
            if len(word) > 500: break
            k, _ = build_and_solve(word, lam_crit)
            Ns.append(len(word)); ks.append(k)
        ax.plot(Ns, ks, 'o-', color=col, label=name, ms=6)
    ax.axhline(1.0, color='k', lw=0.9, ls='--', label='$k=1$')
    ax.set_xlabel('Chain length $N$')
    ax.set_ylabel(r'$k_{\rm eff}$')
    ax.set_title(f'$k_{{\\rm eff}}$ vs $N$ at $\\lambda = \\lambda_c^{{\\rm Fib}} \\approx {lam_crit:.3f}$')
    ax.legend(); ax.grid(alpha=0.25)

    # Right: |lambda_c(g) - lambda_c(g_max)| vs generation (log scale)
    ax = axes[1]
    for n, name, col in [(2,'Fibonacci','steelblue'), (3,'Tribonacci','tomato')]:
        gen_max = 10 if n == 2 else 9
        lc_inf  = find_lambda_c(n, gen_max)
        gens, deltas = [], []
        for g in range(4, gen_max):
            lc = find_lambda_c(n, g)
            delta = abs(lc - lc_inf)
            if delta > 1e-14:
                gens.append(g); deltas.append(delta)
        ax.semilogy(gens, deltas, 'o-', color=col, label=name, ms=6)
    ax.set_xlabel('Generation $g$')
    ax.set_ylabel(r'$|\lambda_c(g) - \lambda_c(\infty)|$')
    ax.set_title('Convergence of $\\lambda_c$ with generation')
    ax.legend(); ax.grid(alpha=0.25, which='both')

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig4_convergence.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Fig 4 saved.")

# -------------------------------------------------------------------------
# Figure 5 — Fundamental flux modes
# -------------------------------------------------------------------------

def fig5_flux_profiles():
    lam_vals_fib = {
        2: find_lambda_c(2, 10),
        3: find_lambda_c(3, 9),
    }

    fig, axes = plt.subplots(2, 2, figsize=(13, 7))

    for row, (n, name) in enumerate([(2, 'Fibonacci'), (3, 'Tribonacci')]):
        lam = lam_vals_fib[n]
        COLORS = {0: '#2166ac', 1: '#d6604d', 2: '#4dac26'}

        for col_idx, g in enumerate([5, 8]):
            ax = axes[row, col_idx]
            word = nbonacci_word(n, g)
            _, phi = build_and_solve(word, lam)
            x = np.arange(len(phi)) / len(phi)

            # Color bars by symbol
            for i, (xi, pi, si) in enumerate(zip(x, phi, word)):
                ax.bar(xi, pi, width=1/len(phi), color=COLORS[si],
                       alpha=0.7, linewidth=0)

            ax.plot(x, phi, color='k', lw=0.8, alpha=0.6)
            ax.set_xlabel('Normalised position $x/L$')
            ax.set_ylabel(r'$\phi$ (norm. flux)')
            ax.set_title(f'{name}, gen {g}, $N={len(word)}$, '
                         f'$\\lambda={lam:.3f}$')
            ax.set_xlim(0, 1); ax.grid(alpha=0.2)

        # Shared legend for symbol colors
        patches = [mpatches.Patch(color=COLORS[s],
                   label=['A (fissile)','B (absorber)','C (absorber)'][s])
                   for s in sorted(set(nbonacci_word(n, 5)))]
        axes[row, 0].legend(handles=patches, loc='upper left', framealpha=0.9)

    plt.tight_layout()
    plt.savefig(f'{OUT}/fig5_flux_profiles.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Fig 5 saved.")

# -------------------------------------------------------------------------
# Run all
# -------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating figures...")
    fig1_chain_structure()
    fig2_keff_vs_lambda()
    fig3_lambda_c_vs_gap()
    fig4_convergence()
    fig5_flux_profiles()
    print("\nAll figures saved to", OUT)
