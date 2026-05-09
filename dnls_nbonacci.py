"""
dnls_nbonacci.py
================
Discrete Nonlinear Schrödinger (DNLS) dynamics on Fibonacci and Tribonacci
substitution chains.

Companion code for:
  "Differential Nonlinear Robustness of Critical States in Fibonacci and
   Tribonacci Substitution Chains"
  Pablo Nogueira Grossi · G6 LLC · 2026
  DOI: 10.5281/zenodo.20075822

Usage
-----
  python dnls_nbonacci.py
  → writes results_table.txt and ipr_vs_lambda.csv

Dependencies: numpy, scipy
"""

import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp


# ── 1. Substitution word generators ─────────────────────────────────────────

def fibonacci_word(length):
    """A→AB, B→A  (encoded 0,1). Returns first `length` symbols."""
    word = [0]
    rules = {0: [0, 1], 1: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]


def tribonacci_word(length):
    """Rauzy: 1→12, 2→13, 3→1  (encoded 0,1,2). Returns first `length` symbols."""
    word = [0]
    rules = {0: [0, 1], 1: [0, 2], 2: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]


# ── 2. Tight-binding Hamiltonian ─────────────────────────────────────────────

def build_hamiltonian(word, N, t_mod=0.5):
    """
    Tridiagonal H on N sites.
    Hopping: letter 0 → 1.0,  letter 1 → t_mod,  letter 2 → t_mod²
    Returns (H, hoppings).
    """
    hop_map  = {0: 1.0, 1: t_mod, 2: t_mod**2}
    hoppings = np.array([hop_map.get(word[j], t_mod) for j in range(N - 1)])
