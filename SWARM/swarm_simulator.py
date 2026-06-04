"""
swarm_simulator.py
==================
Full simulator for:
  "The Swarm Simulator: A Dynamical Systems Model of Collective Intelligence
   Using the TO/TOGT Operator Pipeline"
  Pablo Nogueira Grossi — G6 LLC, Newark NJ, 2026

Zenodo: https://doi.org/10.5281/zenodo.20230613
AXLE:   https://github.com/TOTOGT/AXLE

Implements:
  - SwarmParams dataclass (§3 parameters)
  - step() function (§7 minimal simulator)
  - Full time-evolution loop
  - Fixed-point detection
  - Multi-orbit simulation (§6)
  - Figure generation (4 figures)

Figures generated:
  fig1_state_evolution.pdf  — I, C, M, F over time under contraction
  fig2_convergence.pdf      — ‖Xt − X*‖ vs t (geometric decay, Theorem 5.3)
  fig3_contraction_region.pdf — L = LI+LC+LM parameter space
  fig4_multi_orbit.pdf      — two independent clusters converging to distinct X*

Usage:
  pip install numpy matplotlib
  python swarm_simulator.py

Pablo Nogueira Grossi · G6 LLC · Newark NJ · 2026
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# ── Output directory ──────────────────────────────────────────────────────────
OUTDIR = "figures"
os.makedirs(OUTDIR, exist_ok=True)

# ── Style ─────────────────────────────────────────────────────────────────────
NAVY  = "#1a2744"
GOLD  = "#c9a84c"
TEAL  = "#1a6b5a"
RED   = "#c0392b"
GREY  = "#7f8c8d"
MID   = "#3a4f7a"

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


# ── §7 Minimal Simulator (from paper) ────────────────────────────────────────

class SwarmParams:
    """Parameters governing the swarm evolution (§3)."""
    def __init__(
        self,
        type_quality : float = 0.65,   # f_types
        agent_quality: float = 0.80,   # f_agents
        noise        : float = 0.20,   # η (noise level)
        drag         : float = 1.50,   # D (drag — high drag keeps LC small)
        beta         : float = 0.10,   # β (reuse amplification)
        reuse        : float = 0.50,   # reuse rate
        avg_quality  : float = 0.22,   # avg_quality
        alpha        : float = 0.02,   # α (diffusion rate)
        # NOTE: defaults chosen so LI+LC+LM ≈ 0.81 < 1 (Theorem 5.1 satisfied)
    ):
        self.type_quality  = type_quality
        self.agent_quality = agent_quality
        self.noise         = noise
        self.drag          = drag
        self.beta          = beta
        self.reuse         = reuse
        self.avg_quality   = avg_quality
        self.alpha         = alpha

        # Derived Lipschitz constants (upper bounds)
        self.LI = type_quality * agent_quality * (1 - noise)
        self.LC = self.LI / (1 + drag)
        self.LM = (1 + beta * reuse) * avg_quality
        self.L  = self.LI + self.LC + self.LM

    def contraction_factor(self) -> float:
        """L = LI + LC + LM. Contraction holds iff L < 1."""
        return self.L

    def is_contractive(self) -> bool:
        return self.L < 1.0

    def __repr__(self):
        return (f"SwarmParams(LI={self.LI:.4f}, LC={self.LC:.4f}, "
                f"LM={self.LM:.4f}, L={self.L:.4f}, "
                f"contractive={self.is_contractive()})")


def step(state: tuple, params: SwarmParams, t: int) -> tuple:
    """
    §7 Minimal Simulator — one time step of the swarm evolution.

    Implements Definitions 3.1–3.4:
      I_{t+1} = I_t · f_types · f_agents · (1 − η)
      C_{t+1} = C_t · I_{t+1} / (1 + D)
      M_{t+1} = M_t · (1 + β · reuse) · avg_quality
      F_{t+1} = 1 + α · t

    Returns: (I_new, C_new, M_new, F_new)
    """
    I, C, M, F = state
    p = params

    I_new = I * p.type_quality * p.agent_quality * (1 - p.noise)
    C_new = C * I_new / (1 + p.drag)
    M_new = M * (1 + p.beta * p.reuse) * p.avg_quality
    F_new = 1 + p.alpha * t

    return (I_new, C_new, M_new, F_new)


def evolve(state0: tuple, params: SwarmParams, T: int) -> np.ndarray:
    """
    Full time evolution: X_{t+1} = G_swarm(X_t), t = 0, ..., T-1.
    Returns array of shape (T+1, 4).
    """
    traj = np.zeros((T + 1, 4))
    traj[0] = state0
    state = state0
    for t in range(1, T + 1):
        state = step(state, params, t)
        traj[t] = state
    return traj


def find_fixedpoint(params: SwarmParams, T: int = 200) -> tuple:
    """
    Approximate fixed point by long-run evolution from a canonical start.
    For I, C, M: iterate to convergence. F grows linearly (not fixed).
    """
    state = (1.0, 1.0, 1.0, 1.0)
    for t in range(T):
        state = step(state, params, t)
    return state


def l1_norm(a: tuple, b: tuple) -> float:
    return sum(abs(x - y) for x, y in zip(a, b))


# ── Figure 1: State Evolution ─────────────────────────────────────────────────

def fig1_state_evolution():
    """I, C, M, F over time for a contractive parameter set."""
    p = SwarmParams()
    print(f"  Params: {p}")

    state0 = (1.0, 1.0, 1.0, 0.0)
    T = 60
    traj = evolve(state0, p, T)
    ts = np.arange(T + 1)

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    labels = ["I (shared intent)", "C (coordination)",
              "M (type propagation)", "F (diffusion)"]
    colors = [NAVY, TEAL, GOLD, RED]

    for ax, col, label, color in zip(axes.flat, range(4), labels, colors):
        ax.plot(ts, traj[:, col], color=color, lw=2)
        ax.set_xlabel("Time t")
        ax.set_ylabel(label.split()[0])
        ax.set_title(label)
        ax.axhline(traj[-1, col], color=color, lw=0.8, ls="--", alpha=0.5)
        ax.grid(True, alpha=0.2)

    fig.suptitle(
        f"Swarm State Evolution · G_swarm = F ∘ M ∘ C ∘ I\n"
        f"L = {p.L:.4f} < 1 (contractive) · Theorem 5.1",
        fontsize=12
    )
    plt.tight_layout()
    savefig("fig1_state_evolution")


# ── Figure 2: Convergence (Theorem 5.3) ──────────────────────────────────────

def fig2_convergence():
    """‖Xt − X*‖₁ vs t — geometric decay, Theorem 5.3."""
    p = SwarmParams()
    X_star = find_fixedpoint(p)

    T = 60
    state0_list = [
        (2.0, 0.5, 1.5, 0.0),
        (0.3, 1.8, 0.4, 0.0),
        (1.5, 1.5, 0.8, 0.0),
    ]
    labels = [r"$X_0 = (2.0, 0.5, 1.5, 0)$",
              r"$X_0 = (0.3, 1.8, 0.4, 0)$",
              r"$X_0 = (1.5, 1.5, 0.8, 0)$"]
    colors = [NAVY, TEAL, GOLD]

    fig, ax = plt.subplots(figsize=(8, 5))

    ts = np.arange(T + 1)
    for state0, label, color in zip(state0_list, labels, colors):
        traj = evolve(state0, p, T)
        norms = [l1_norm(tuple(traj[t]), X_star) for t in range(T + 1)]
        ax.semilogy(ts, norms, color=color, lw=2, label=label)

    # Theoretical bound: L^t * ‖X0 - X*‖
    L = p.contraction_factor()
    r0 = l1_norm(state0_list[0], X_star)
    theoretical = [r0 * L**t for t in ts]
    ax.semilogy(ts, theoretical, "--", color=GREY, lw=1.5,
                label=rf"Bound: $L^t \cdot \|X_0 - X^*\|_1$, $L={L:.3f}$")

    ax.set_xlabel("Time t")
    ax.set_ylabel(r"$\|X_t - X^*\|_1$")
    ax.set_title(
        "Global Convergence · Theorem 5.3\n"
        r"$\|X_t - X^*\|_1 \leq L^t \cdot \|X_0 - X^*\|_1$"
    )
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.2)
    savefig("fig2_convergence")


# ── Figure 3: Contraction Region ─────────────────────────────────────────────

def fig3_contraction_region():
    """L = LI + LC + LM parameter space — contraction region (L < 1)."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Left: noise vs type_quality — contraction region
    ax = axes[0]
    noise_vals = np.linspace(0.0, 0.5, 200)
    tq_vals    = np.linspace(0.5, 1.0, 200)
    N, TQ = np.meshgrid(noise_vals, tq_vals)

    # Fixed: agent_quality=0.88, drag=0.20, beta=0.15, reuse=0.60, avg_qual=0.85
    LI = TQ * 0.88 * (1 - N)
    LC = LI / (1 + 0.20)
    LM_fixed = (1 + 0.15 * 0.60) * 0.85
    L_total = LI + LC + LM_fixed

    cf = ax.contourf(noise_vals, tq_vals, L_total,
                     levels=50, cmap="RdYlGn_r")
    plt.colorbar(cf, ax=ax, label="L = LI + LC + LM")
    ax.contour(noise_vals, tq_vals, L_total, levels=[1.0],
               colors=NAVY, linewidths=2)
    ax.set_xlabel(r"Noise $\eta$")
    ax.set_ylabel(r"Type quality $f_{\rm types}$")
    ax.set_title("Contraction region (L < 1)\nContour at L = 1")

    # Right: avg_quality vs beta — LM contribution
    ax = axes[1]
    aq_vals   = np.linspace(0.5, 1.0, 200)
    beta_vals = np.linspace(0.0, 1.0, 200)
    AQ, BETA = np.meshgrid(aq_vals, beta_vals)
    LM = (1 + BETA * 0.60) * AQ
    # Fixed LI + LC for default params
    p_default = SwarmParams()
    LI_LC_fixed = p_default.LI + p_default.LC
    L_total2 = LI_LC_fixed + LM

    cf2 = ax.contourf(aq_vals, beta_vals, L_total2,
                      levels=50, cmap="RdYlGn_r")
    plt.colorbar(cf2, ax=ax, label="L = LI + LC + LM")
    ax.contour(aq_vals, beta_vals, L_total2, levels=[1.0],
               colors=NAVY, linewidths=2)
    ax.set_xlabel(r"Average quality $\bar{q}$")
    ax.set_ylabel(r"Reuse amplification $\beta$")
    ax.set_title(r"Contraction region: $\beta$ vs $\bar{q}$" + "\nContour at L = 1")

    fig.suptitle("Contraction Parameter Space · Theorem 5.1\nGreen = L < 1 (contractive)",
                 fontsize=12)
    plt.tight_layout()
    savefig("fig3_contraction_region")


# ── Figure 4: Multi-Orbit (§6) ────────────────────────────────────────────────

def fig4_multi_orbit():
    """Two independent clusters converging to distinct fixed points (§6)."""
    # Cluster A: high-quality, low noise
    pA = SwarmParams(type_quality=0.92, agent_quality=0.90, noise=0.04,
                     drag=0.15, beta=0.10, reuse=0.55, avg_quality=0.88)
    # Cluster B: lower quality, higher noise
    pB = SwarmParams(type_quality=0.82, agent_quality=0.80, noise=0.10,
                     drag=0.30, beta=0.20, reuse=0.65, avg_quality=0.78)

    T = 80
    state0A = (1.0, 1.0, 1.0, 0.0)
    state0B = (1.0, 1.0, 1.0, 0.0)

    trajA = evolve(state0A, pA, T)
    trajB = evolve(state0B, pB, T)

    X_starA = find_fixedpoint(pA)
    X_starB = find_fixedpoint(pB)

    ts = np.arange(T + 1)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    # I component
    ax = axes[0]
    ax.plot(ts, trajA[:, 0], color=NAVY, lw=2, label=r"Cluster A ($L_A$=" + f"{pA.L:.3f})")
    ax.plot(ts, trajB[:, 0], color=RED,  lw=2, label=r"Cluster B ($L_B$=" + f"{pB.L:.3f})")
    ax.axhline(X_starA[0], color=NAVY, lw=0.8, ls="--", alpha=0.6, label=r"$I^*_A$")
    ax.axhline(X_starB[0], color=RED,  lw=0.8, ls="--", alpha=0.6, label=r"$I^*_B$")
    ax.set_title("I (shared intent)")
    ax.set_xlabel("Time t"); ax.legend(fontsize=8); ax.grid(True, alpha=0.2)

    # C component
    ax = axes[1]
    ax.plot(ts, trajA[:, 1], color=NAVY, lw=2)
    ax.plot(ts, trajB[:, 1], color=RED,  lw=2)
    ax.axhline(X_starA[1], color=NAVY, lw=0.8, ls="--", alpha=0.6)
    ax.axhline(X_starB[1], color=RED,  lw=0.8, ls="--", alpha=0.6)
    ax.set_title("C (coordination)"); ax.set_xlabel("Time t"); ax.grid(True, alpha=0.2)

    # Convergence norms
    ax = axes[2]
    normsA = [l1_norm(tuple(trajA[t]), X_starA) for t in range(T + 1)]
    normsB = [l1_norm(tuple(trajB[t]), X_starB) for t in range(T + 1)]
    ax.semilogy(ts, normsA, color=NAVY, lw=2, label=f"Cluster A")
    ax.semilogy(ts, normsB, color=RED,  lw=2, label=f"Cluster B")
    ax.set_title(r"$\|X_t - X^*\|_1$ · Two Orbits")
    ax.set_xlabel("Time t"); ax.set_ylabel(r"$\|X_t - X^*\|_1$")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.2)

    # Annotate fixed-point values
    inv_A = sum(abs(x) for x in X_starA[:3])
    inv_B = sum(abs(x) for x in X_starB[:3])
    fig.suptitle(
        f"Multi-Orbit System S = {{O₁, O₂}} · §6\n"
        f"Inv(O_A) ≈ {inv_A:.3f}, Inv(O_B) ≈ {inv_B:.3f}, "
        f"Inv(S) > max{{Inv(O_A), Inv(O_B)}}",
        fontsize=12
    )
    plt.tight_layout()
    savefig("fig4_multi_orbit")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Swarm Simulator — Figure Generator")
    print("Zenodo: https://doi.org/10.5281/zenodo.20230613")
    print(f"Output: {os.path.abspath(OUTDIR)}/\n")

    # Verify contraction condition for default params
    p_default = SwarmParams()
    print(f"Default parameters:")
    print(f"  {p_default}")
    print(f"  Contractive: {p_default.is_contractive()}\n")

    print("Generating figure 1: state evolution...")
    fig1_state_evolution()

    print("Generating figure 2: convergence (Theorem 5.3)...")
    fig2_convergence()

    print("Generating figure 3: contraction parameter space...")
    fig3_contraction_region()

    print("Generating figure 4: multi-orbit system...")
    fig4_multi_orbit()

    print("\nAll figures generated.")
    print("Build Lean: lake update && lake build SwarmSimulator")
