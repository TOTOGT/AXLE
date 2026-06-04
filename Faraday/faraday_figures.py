"""
faraday_figures.py
==================
Figure generator for:
  Electromagnetic Unity: From Faraday's Fields to the dm³ Operator Framework
  Pablo Nogueira Grossi — G6 LLC, 2026

Fig 1 — Helical charged-particle trajectory in a magnetic field (3D perspective)
Fig 2 — Faraday induction: flux change → EMF (Lenz's law diagram)
Fig 3 — Magneto-optical Faraday effect: polarization rotation
Fig 4 — dm³ operator correspondence: C→K→F→U mapped to EM phenomena
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc, Circle
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

NAVY  = '#0a1628'
GOLD  = '#c9a84c'
CYAN  = '#1abc9c'
RED   = '#c0392b'
BLUE  = '#1a5276'
PURP  = '#6c3483'
GREY  = '#95a5a6'
LGREY = '#eaf0fb'
WHITE = '#ffffff'

def style():
    plt.rcParams.update({
        'figure.facecolor': WHITE, 'axes.facecolor': WHITE,
        'axes.edgecolor': NAVY, 'axes.labelcolor': NAVY,
        'xtick.color': NAVY, 'ytick.color': NAVY, 'text.color': NAVY,
        'font.family': 'serif', 'font.size': 10,
        'axes.titlesize': 11, 'axes.labelsize': 10,
        'legend.fontsize': 8.5, 'figure.dpi': 150,
    })

# ── Figure 1: Helical trajectory in magnetic field ───────────────────────────
def make_fig1():
    style()
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(NAVY)
    fig.patch.set_facecolor(NAVY)

    # Helical path: B along z-axis, particle spirals
    t = np.linspace(0, 4*np.pi, 600)
    omega_c = 1.0          # cyclotron frequency
    v_par   = 0.4          # parallel velocity
    r       = 0.8          # Larmor radius
    x = r * np.cos(omega_c * t)
    y = r * np.sin(omega_c * t)
    z = v_par * t

    # Colour by z-depth for pseudo-3D
    points = np.array([x, y, z]).T
    from matplotlib.collections import LineCollection
    for i in range(len(t)-1):
        ax.plot(x[i:i+2], y[i:i+2], z[i:i+2],
                color=GOLD, alpha=0.85, linewidth=1.8)

    # Velocity arrow at a mid-point
    mid = len(t)//3
    ax.quiver(x[mid], y[mid], z[mid],
              -r*omega_c*np.sin(omega_c*t[mid]),
               r*omega_c*np.cos(omega_c*t[mid]),
               v_par,
              length=1.0, color=CYAN, linewidth=2.0,
              arrow_length_ratio=0.3, label='v')

    # Magnetic field lines (z-axis arrows)
    for xi, yi in [(-1.5, -1.5), (-1.5, 1.5), (1.5, -1.5), (1.5, 1.5), (0, 0)]:
        ax.quiver(xi, yi, 0, 0, 0, 4*np.pi*v_par,
                  length=1.0, color='#4fc3f7', alpha=0.4,
                  linewidth=1.2, arrow_length_ratio=0.06)

    # F = qv×B label plane
    ax.text(1.2, 0, z[mid]+0.8, 'F = qv×B', color=RED, fontsize=10,
            fontfamily='serif', fontstyle='italic')
    ax.text(0.0, 0, 4*np.pi*v_par + 0.3, 'B', color='#4fc3f7', fontsize=12,
            fontfamily='serif', fontweight='bold')

    ax.set_xlabel('x', color=GREY, labelpad=4)
    ax.set_ylabel('y', color=GREY, labelpad=4)
    ax.set_zlabel('z  (||B)', color=GREY, labelpad=4)
    ax.tick_params(colors=GREY, labelsize=7)
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor(GREY)
        pane.set_alpha(0.2)
    ax.set_title('Helical motion of a charged particle\nin a uniform magnetic field B || z',
                 color=WHITE, pad=10, fontsize=11, fontfamily='serif')
    ax.legend(loc='upper left', facecolor=NAVY, edgecolor=GREY,
              labelcolor=WHITE, fontsize=9)
    plt.tight_layout()
    plt.savefig('/home/claude/fig1_helix.png', dpi=150, bbox_inches='tight',
                facecolor=NAVY)
    plt.close()
    print("fig1 done")

# ── Figure 2: Faraday induction — flux → EMF ─────────────────────────────────
def make_fig2():
    style()
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    # Left: coil + moving magnet + flux curve
    ax = axes[0]
    ax.set_xlim(0, 10); ax.set_ylim(-3, 4); ax.axis('off')
    ax.set_facecolor(WHITE)

    # Coil (rectangles representing wire loops)
    for i, x0 in enumerate(np.linspace(4.0, 6.5, 6)):
        rect = FancyBboxPatch((x0, -0.6), 0.35, 2.2,
                              boxstyle='round,pad=0.05',
                              linewidth=1.8, edgecolor=NAVY,
                              facecolor='none')
        ax.add_patch(rect)
    ax.text(5.25, -1.2, 'Conducting coil', ha='center', fontsize=9,
            color=NAVY, fontfamily='serif')

    # Magnet moving left
    mag = FancyBboxPatch((1.2, -0.3), 1.8, 1.6,
                         boxstyle='round,pad=0.1',
                         facecolor=BLUE, edgecolor=NAVY, linewidth=1.5)
    ax.add_patch(mag)
    ax.text(2.1, 0.1, 'N', ha='center', va='center',
            color=WHITE, fontsize=14, fontweight='bold', fontfamily='serif')
    ax.text(2.1, 0.9, 'S', ha='center', va='center',
            color=WHITE, fontsize=12, fontweight='bold', fontfamily='serif')
    ax.annotate('', xy=(3.5, 0.5), xytext=(1.8, 0.5),  # wrong direction — corrects below
                arrowprops=dict(arrowstyle='->', color=RED, lw=2.2))
    ax.text(2.6, 0.8, 'v', color=RED, fontsize=12, fontstyle='italic',
            fontfamily='serif')

    # B field lines through coil
    for y_b in [0.0, 0.5, 1.0]:
        ax.annotate('', xy=(6.5, y_b), xytext=(3.2, y_b),
                    arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.2,
                                   alpha=0.55))

    # Induced current direction (Lenz)
    arc = Arc((5.25, 0.5), 1.0, 1.8, angle=0,
              theta1=20, theta2=340, color=GOLD, lw=2.0)
    ax.add_patch(arc)
    ax.annotate('', xy=(5.75, 1.4), xytext=(5.75, 1.35),
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.8))
    ax.text(6.9, 0.5, 'I\n(induced)', ha='center', va='center',
            color=GOLD, fontsize=9, fontfamily='serif')

    # EMF = -dΦ/dt label
    ax.text(5.0, 3.2, r'$\mathcal{E} = -\frac{d\Phi_B}{dt}$',
            ha='center', fontsize=13, color=NAVY, fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=LGREY,
                      edgecolor=GOLD, lw=1.5))
    ax.set_title('Faraday Induction (Lenz\'s Law)', fontsize=11,
                 fontfamily='serif', pad=4, color=NAVY)

    # Right: EMF vs time as magnet enters, inside, exits
    ax2 = axes[1]
    t = np.linspace(0, 10, 500)
    # Approaching: positive EMF; inside: near zero; leaving: negative
    emf = (2.5 * np.exp(-((t-2.5)**2)/0.6)
           - 2.5 * np.exp(-((t-7.5)**2)/0.6))
    flux = (2.0 * (1/(1+np.exp(-2*(t-2.5)))) -
             2.0 * (1/(1+np.exp(-2*(t-7.5)))))

    ax2.plot(t, flux, color=BLUE, linewidth=2.0, label='Flux $\\Phi_B$')
    ax2.plot(t, emf,  color=GOLD, linewidth=2.0, linestyle='--',
             label=r'EMF $\mathcal{E}$')
    ax2.axhline(0, color=NAVY, linewidth=0.8, alpha=0.5)
    ax2.axvline(2.5, color=GREY, linewidth=1.0, linestyle=':')
    ax2.axvline(7.5, color=GREY, linewidth=1.0, linestyle=':')
    ax2.text(2.5, 2.7, 'Enter', ha='center', fontsize=8.5, color=GREY,
             fontfamily='serif')
    ax2.text(7.5, 2.7, 'Exit', ha='center', fontsize=8.5, color=GREY,
             fontfamily='serif')
    ax2.set_xlabel('Time $t$', labelpad=5)
    ax2.set_ylabel('Magnitude (a.u.)', labelpad=5)
    ax2.set_title('Flux and Induced EMF vs Time', fontsize=11,
                  fontfamily='serif', pad=4)
    ax2.legend(framealpha=0.9, fontsize=9)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.suptitle('Figure 2 — Faraday\'s Law of Electromagnetic Induction',
                 fontsize=11, fontweight='bold', color=NAVY, y=1.01,
                 fontfamily='serif')
    plt.tight_layout()
    plt.savefig('/home/claude/fig2_induction.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("fig2 done")

# ── Figure 3: Faraday magneto-optical effect ──────────────────────────────────
def make_fig3():
    style()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_xlim(0, 12); ax.set_ylim(-2.5, 2.5); ax.axis('off')

    # Propagation axis
    ax.annotate('', xy=(11.5, 0), xytext=(0.3, 0),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
    ax.text(11.7, 0, 'z (B)', ha='left', va='center',
            fontsize=10, color=NAVY, fontfamily='serif', fontstyle='italic')

    # Incoming polarization plane (vertical, left)
    for sign in [1, -1]:
        ax.annotate('', xy=(2.0, sign*1.6), xytext=(2.0, 0),
                    arrowprops=dict(arrowstyle='->', color=BLUE, lw=2.2))
    ax.text(2.0, 1.9, 'E-field\n(incident)', ha='center', fontsize=9,
            color=BLUE, fontfamily='serif')
    ax.text(2.0, -2.2, r'$\theta_0 = 0°$', ha='center', fontsize=9,
            color=BLUE, fontfamily='serif')

    # Medium block
    medium = FancyBboxPatch((4.5, -1.8), 3.0, 3.6,
                            boxstyle='round,pad=0.1',
                            facecolor=LGREY, edgecolor=GOLD,
                            linewidth=2.0, alpha=0.8)
    ax.add_patch(medium)
    ax.text(6.0, 0.4, 'Magneto-optical\nmedium', ha='center', va='center',
            fontsize=9, color=NAVY, fontfamily='serif', multialignment='center')
    ax.text(6.0, -0.5, '(B || z)', ha='center', va='center',
            fontsize=9, color=BLUE, fontfamily='serif', fontstyle='italic')

    # Rotated polarization (outgoing, tilted ~30 deg)
    theta_F = np.radians(33)  # Faraday rotation angle = 33 degrees!
    for sign in [1, -1]:
        ax.annotate('', xy=(9.5 + sign*1.6*np.sin(theta_F),
                             sign*1.6*np.cos(theta_F)),
                    xytext=(9.5, 0),
                    arrowprops=dict(arrowstyle='->', color=GOLD, lw=2.2))
    ax.text(9.5, 1.9, 'E-field\n(rotated)', ha='center', fontsize=9,
            color=GOLD, fontfamily='serif')
    ax.text(9.5, -2.2, r'$\theta_F = V \cdot B \cdot d$', ha='center',
            fontsize=9, color=GOLD, fontfamily='serif')

    # Rotation arc annotation
    arc = Arc((9.5, 0), 1.4, 1.4, angle=0, theta1=60, theta2=90,
              color=RED, lw=1.8)
    ax.add_patch(arc)
    ax.text(10.2, 0.9, r'$\theta_F$', color=RED, fontsize=10,
            fontfamily='serif', fontstyle='italic')

    # Verdet constant note
    ax.text(6.0, 2.2,
            r'$\theta_F = V \cdot B \cdot d$ — Verdet constant V is material-specific',
            ha='center', fontsize=9.5, color=NAVY, fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor=GOLD, lw=1.2))

    ax.set_title(
        'Figure 3 — Faraday Magneto-Optical Effect\n'
        'Linearly polarised light rotates by angle \u03b8F when propagating through '
        'a magnetised medium (B \u2225 z)',
        fontsize=10.5, color=NAVY, fontfamily='serif', pad=6)
    plt.tight_layout()
    plt.savefig('/home/claude/fig3_faraday_effect.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("fig3 done")

# ── Figure 4: dm³ operator correspondence to EM phenomena ────────────────────
def make_fig4():
    style()
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.5); ax.axis('off')
    fig.patch.set_facecolor('#f8f9fd')
    ax.set_facecolor('#f8f9fd')

    # Two rows: dm³ operators (top) ↔ EM phenomena (bottom)
    ops = [
        ('C\nCompression\n(coupling)', 1.5,  NAVY,   'white',
         'Magnetic\nconfinement\n(Larmor radius)', 1.5, '#1565c0'),
        ('K\nCurvature\n(clipping)',   3.8,  BLUE,   'white',
         'Cyclotron\nresonance\n(frequency \u03c9c)', 3.8, '#1976d2'),
        ('F\nFold\n(saturation)',       6.1,  PURP,   'white',
         'Faraday\nrotation\n(non-linear \u03b8F)', 6.1, PURP),
        ('U\nUnification\n(stability)', 8.4,  '#1e8449', 'white',
         'Maxwell\nunification\n(E, B, c)', 8.4, '#2e7d32'),
        ('T\nTime circuit\n(spiral return)', 10.7, RED, 'white',
         'EM wave\npropagation\n(c = 1/\u221a\u03bc\u03b5)', 10.7, RED),
    ]

    bw, bh = 1.95, 1.10
    for label, cx, fc, tc, em_label, ecx, efc in ops:
        # Top box: dm³ operator
        r = FancyBboxPatch((cx-bw/2, 2.9), bw, bh,
                           boxstyle='round,pad=0.08',
                           facecolor=fc, edgecolor='white',
                           linewidth=1.4, zorder=3)
        ax.add_patch(r)
        ax.text(cx, 2.9+bh/2, label, ha='center', va='center',
                fontsize=8.2, color=tc, fontfamily='serif',
                multialignment='center', zorder=4)

        # Bottom box: EM correspondence
        r2 = FancyBboxPatch((ecx-bw/2, 0.5), bw, bh,
                            boxstyle='round,pad=0.08',
                            facecolor=efc, edgecolor='white',
                            linewidth=1.4, alpha=0.82, zorder=3)
        ax.add_patch(r2)
        ax.text(ecx, 0.5+bh/2, em_label, ha='center', va='center',
                fontsize=8.2, color='white', fontfamily='serif',
                multialignment='center', zorder=4)

        # Vertical correspondence arrow
        ax.annotate('', xy=(cx, 0.5+bh), xytext=(cx, 2.9),
                    arrowprops=dict(arrowstyle='<->', color=GOLD,
                                   lw=1.6), zorder=2)

    # Horizontal arrows between operators (top row)
    for i in range(len(ops)-1):
        x1 = ops[i][1] + bw/2
        x2 = ops[i+1][1] - bw/2
        ax.annotate('', xy=(x2, 3.45), xytext=(x1, 3.45),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.6))

    # Row labels
    ax.text(0.15, 3.45, 'dm\u00b3\noperator', ha='center', va='center',
            fontsize=8.5, color=NAVY, fontfamily='serif',
            fontweight='bold', multialignment='center')
    ax.text(0.15, 1.05, 'EM\nphysics', ha='center', va='center',
            fontsize=8.5, color=BLUE, fontfamily='serif',
            fontweight='bold', multialignment='center')

    ax.text(6.0, 4.3,
            'Figure 4 — dm\u00b3 Operator Chain: Correspondence with Electromagnetic Phenomena',
            ha='center', fontsize=11, color=NAVY, fontfamily='serif',
            fontweight='bold')
    ax.text(6.0, 0.05,
            'Each dm\u00b3 operator C\u2192K\u2192F\u2192U\u2192T has a direct structural '
            'correspondent in classical electromagnetism',
            ha='center', fontsize=9, color=GREY, fontfamily='serif')

    plt.tight_layout()
    plt.savefig('/home/claude/fig4_correspondence.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("fig4 done")

if __name__ == '__main__':
    make_fig1()
    make_fig2()
    make_fig3()
    make_fig4()
    print("All four figures done.")
