# ── §2: Tight-binding Hamiltonian & mid-gap eigenstate ───────────────────────
#
# H is tridiagonal, H[j,j+1] = H[j+1,j] = t_{word[j]}, diagonal = 0.
# Hopping map:  letter 0 → t_A = 1.0
#               letter 1 → t_B = t_mod       (default 0.5)
#               letter 2 → t_C = t_mod²
#
# t_mod = 0.5 is the generic incommensurate point used throughout the paper.
# The mid-gap eigenstate is the one whose eigenvalue is closest to E = 0.

T_MOD = 0.5   # hopping modulation (paper default)

def build_hamiltonian(word, N, t_mod=T_MOD):
    """
    Build N×N tridiagonal tight-binding Hamiltonian.
    Returns (H, hoppings) where hoppings is the (N-1,) bond array.
    """
    hop_map = {0: 1.0, 1: t_mod, 2: t_mod**2}
    hoppings = np.array([hop_map.get(word[j], t_mod) for j in range(N - 1)])
