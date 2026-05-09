# ── Cell 1: imports & global style ──────────────────────────────────────────
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')       # change to 'inline' in Jupyter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif', 'Times New Roman', 'Georgia'],
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'lines.linewidth': 1.8,
    'grid.alpha': 0.3,
    'grid.linewidth': 0.5,
})

# Colour palette (PRB-friendly, colour-blind safe)
COL_FIB  = '#2166ac'   # blue   – Fibonacci
COL_TRIB = '#d6604d'   # red    – Tribonacci
COL_GOLD = '#c9a84c'   # gold   – ratio / accent
COL_GREY = '#888888'

ETA = 1.8392867552141612   # tribonacci constant η (dominant root of x³−x²−x−1)
PHI = 1.6180339887498949   # golden ratio φ
