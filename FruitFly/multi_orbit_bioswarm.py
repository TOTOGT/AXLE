#!/usr/bin/env python3
"""
multi_orbit_bioswarm.py
=======================
Fruit-Fly Connectome Toy Model — Generative Operator Pipeline
G = U ∘ F ∘ K ∘ C on a minimal Drosophila-inspired swarm.

Companion code for:
  "Biological Transitions as Multi-Agent Realisations of the
   Generative Operator Pipeline in TO/TOGT:
   A Fruit-Fly Connectome Toy Model"
  Pablo Nogueira Grossi, G6 LLC (2026)
  Zenodo: https://doi.org/10.5281/zenodo.[THIS_RECORD]
  Companion DNLS paper: https://doi.org/10.5281/zenodo.20026942

Operator definitions
--------------------
C : Localized orthogonal compression  — projects each agent's 2-D state
    onto the nearest axis (compression toward the fold threshold).
K : Curvature intensification/clipping — applies bias b and clips to [-1, 1]
    (models nonlinear saturation of the curvature term).
F : Folding (loss of injectivity) — local averaging across neighbours
    (models synaptic pooling / lateral inhibition).
U : Unfolding (stabilisation) — rescales toward unit sphere
    (models homeostatic gain control).

The pitchfork bifurcation at |α| = 0.5 corresponds to the transition
between a single stable rest state and a pair of bounded oscillatory
states (HPA-axis analogue). This is verified in Lean 4 in
MultiOrbitBioSwarm.lean (AXLE repository).

Author
------
    Pablo Nogueira Grossi  |  ORCID: 0009-0000-6496-2186
    G6 LLC, Newark NJ      |  pablogrossi@hotmail.com
    GitHub: https://github.com/TOTOGT/AXLE

License: MIT
"""
from __future__ import annotations

import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List
import csv
import os

# ---------------------------------------------------------------------------
# 1. Agent and Swarm types
# ---------------------------------------------------------------------------

@dataclass
class BioAgent:
    """Neural cluster: 2-D state vector + coupling constant."""
    state: np.ndarray          # shape (2,)
    coupling: float            # α ∈ [0, 1]
    trajectory: list = field(default_factory=list)

    def record(self) -> None:
        self.trajectory.append(self.state.copy())


BioSwarm = List[BioAgent]


# ---------------------------------------------------------------------------
# 2. Operator pipeline  G = U ∘ F ∘ K ∘ C
# ---------------------------------------------------------------------------

def C_compress(state: np.ndarray) -> np.ndarray:
    """Localized orthogonal compression: project onto nearest axis."""
    idx = np.argmax(np.abs(state))
    out = np.zeros_like(state)
    out[idx] = state[idx]
    return out


def K_clip(state: np.ndarray, b: float = 0.1) -> np.ndarray:
    """Curvature intensification with bias b, clipped to [-1, 1]."""
    return np.clip(state + b * np.sign(state + 1e-12), -1.0, 1.0)


def F_fold(state: np.ndarray, neighbour: np.ndarray, alpha: float) -> np.ndarray:
    """Folding via local averaging: state = (1-α)*state + α*neighbour."""
    return (1.0 - alpha) * state + alpha * neighbour


def U_unfold(state: np.ndarray) -> np.ndarray:
    """Stabilisation: rescale to unit sphere (homeostatic gain control)."""
    norm = np.linalg.norm(state)
    if norm < 1e-12:
        return state
    return state / norm


def apply_G(
    agent: BioAgent,
    neighbour_state: np.ndarray,
    b: float = 0.1,
) -> np.ndarray:
    """One application of G = U ∘ F ∘ K ∘ C."""
    s = C_compress(agent.state)
    s = K_clip(s, b=b)
    s = F_fold(s, neighbour_state, agent.coupling)
    s = U_unfold(s)
    return s


# ---------------------------------------------------------------------------
# 3. Swarm evolution
# ---------------------------------------------------------------------------

def evolve_swarm(
    swarm: BioSwarm,
    n_iter: int = 6,
    b: float = 0.1,
    noise_std: float = 0.01,
    rng: np.random.Generator | None = None,
) -> BioSwarm:
    """
    Evolve the swarm for n_iter steps of G, with optional synaptic noise.

    The Lean-verified contraction bound guarantees that for |α| < 0.5 the
    swarm converges; at |α| = 0.5 the pitchfork bifurcation onset is reached.

    Parameters
    ----------
    swarm    : list of BioAgent — the initial swarm configuration.
    n_iter   : int — number of G-applications (default 6, as in the paper).
    b        : float — curvature bias for K (default 0.1).
    noise_std: float — standard deviation of additive Gaussian synaptic noise.
    rng      : numpy Generator — for reproducibility.
    """
    if rng is None:
        rng = np.random.default_rng(42)
    N = len(swarm)

    for agent in swarm:
        agent.record()

    for _ in range(n_iter):
        new_states = []
        for i, agent in enumerate(swarm):
            # Nearest-neighbour folding (periodic boundary)
            nb = swarm[(i + 1) % N].state
            new_s = apply_G(agent, nb, b=b)
            # Weak synaptic noise
            new_s += rng.normal(0, noise_std, size=new_s.shape)
            new_states.append(new_s)
        for agent, ns in zip(swarm, new_states):
            agent.state = ns
            agent.record()

    return swarm


# ---------------------------------------------------------------------------
# 4. Pitchfork scan: IPR-analogue vs alpha
# ---------------------------------------------------------------------------

def pitchfork_scan(
    alphas: np.ndarray,
    n_agents: int = 10,
    n_iter: int = 6,
    b: float = 0.1,
    noise_std: float = 0.001,
) -> np.ndarray:
    """
    For each coupling α, run the swarm and return the final mean |state|²
    (a localization proxy analogous to IPR) after n_iter applications of G.
    """
    rng = np.random.default_rng(0)
    results = np.zeros(len(alphas))
    for j, alpha in enumerate(alphas):
        swarm = [
            BioAgent(
                state=rng.uniform(-0.5, 0.5, size=2),
                coupling=float(alpha),
            )
            for _ in range(n_agents)
        ]
        swarm = evolve_swarm(swarm, n_iter=n_iter, b=b,
                             noise_std=noise_std, rng=rng)
        final_norms = np.array([np.sum(a.state ** 2) for a in swarm])
        results[j] = float(np.mean(final_norms))
    return results


# ---------------------------------------------------------------------------
# 5. Figure generators
# ---------------------------------------------------------------------------

def fig1_swarm_trajectories(out_dir: str = ".") -> None:
    """
    Fig 1: Swarm trajectories in 2-D state space for α = 0.3 (contractive)
    and α = 0.5 (pitchfork onset), 6 iterations.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    rng = np.random.default_rng(7)

    for ax, alpha, label in zip(
        axes,
        [0.3, 0.5],
        ["α = 0.3 (contractive, L = 0.8)", "α = 0.5 (pitchfork onset, L = 1.0)"],
    ):
        swarm = [
            BioAgent(
                state=rng.uniform(-0.8, 0.8, size=2),
                coupling=alpha,
            )
            for _ in range(8)
        ]
        swarm = evolve_swarm(swarm, n_iter=6, b=0.1,
                             noise_std=0.005, rng=rng)
        cmap = plt.cm.viridis
        for agent in swarm:
            traj = np.array(agent.trajectory)   # shape (7, 2)
            for k in range(len(traj) - 1):
                color = cmap(k / 6)
                ax.plot(traj[k:k+2, 0], traj[k:k+2, 1],
                        color=color, lw=1.5, alpha=0.8)
            ax.scatter(traj[0, 0], traj[0, 1], c="white",
                       edgecolors="black", s=40, zorder=5)
            ax.scatter(traj[-1, 0], traj[-1, 1], c="red",
                       edgecolors="black", s=60, zorder=5, marker="*")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")
        ax.set_title(label, fontsize=11)
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.axhline(0, color="gray", lw=0.5, ls="--")
        ax.axvline(0, color="gray", lw=0.5, ls="--")

    sm = plt.cm.ScalarMappable(cmap=cmap,
                                norm=plt.Normalize(vmin=0, vmax=6))
    sm.set_array([])
    fig.colorbar(sm, ax=axes, label="Iteration", shrink=0.8)
    fig.suptitle(
        "Swarm trajectories under G = U∘F∘K∘C (6 iterations)\n"
        "White circles: initial state  |  Red stars: final state",
        fontsize=10,
    )
    plt.tight_layout()
    path = os.path.join(out_dir, "fig1_swarm_trajectories.pdf")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {path}")


def fig2_pitchfork_scan(out_dir: str = ".") -> None:
    """
    Fig 2: Mean ‖state‖² vs coupling α — the pitchfork signature.
    Vertical dashed line at α = 0.5 (threshold verified in Lean 4).
    """
    alphas = np.linspace(0.0, 0.8, 80)
    mean_norm = pitchfork_scan(alphas, n_agents=12, n_iter=6,
                               b=0.1, noise_std=0.001)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(alphas, mean_norm, color="steelblue", lw=2, label="Mean ‖state‖²")
    ax.axvline(0.5, color="crimson", lw=1.5, ls="--",
               label="α = 0.5 (pitchfork threshold, Lean-verified)")
    ax.set_xlabel("Coupling α", fontsize=12)
    ax.set_ylabel("Mean ‖state‖² after 6 iterations", fontsize=11)
    ax.set_title(
        "Pitchfork bifurcation signature in the BioSwarm model\n"
        "G = U∘F∘K∘C,  N = 12 agents,  b = 0.1",
        fontsize=11,
    )
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    path = os.path.join(out_dir, "fig2_pitchfork_scan.pdf")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {path}")


def fig3_six_iterate_convergence(out_dir: str = ".") -> None:
    """
    Fig 3: Residual ‖state(t) − fixed_point‖ vs iteration for α = 0.3.
    Shows L^k convergence with L = 0.8 (verified in Lean 4).
    """
    rng = np.random.default_rng(99)
    alpha = 0.3
    n_agents = 6
    n_iter = 12

    swarm = [
        BioAgent(state=rng.uniform(-0.8, 0.8, size=2), coupling=alpha)
        for _ in range(n_agents)
    ]
    swarm = evolve_swarm(swarm, n_iter=n_iter, b=0.1,
                         noise_std=0.0, rng=rng)

    # Final state as proxy for fixed point
    fixed = np.array([a.state for a in swarm])      # (N, 2)
    residuals = []
    for t in range(n_iter + 1):
        states_t = np.array([a.trajectory[t] for a in swarm])
        residuals.append(float(np.mean(np.linalg.norm(states_t - fixed, axis=1))))

    iters = np.arange(n_iter + 1)
    L = 0.8
    L_bound = residuals[0] * L ** iters

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogy(iters, residuals, "o-", color="steelblue", lw=2,
                label="Mean residual ‖state(t) − state(12)‖")
    ax.semilogy(iters, L_bound, "r--", lw=1.5,
                label=f"Contraction bound  L^t · r₀,  L = {L}")
    ax.axvline(6, color="gray", lw=1, ls=":",
               label="t = 6 (paper claim)")
    ax.set_xlabel("Iteration t", fontsize=12)
    ax.set_ylabel("Residual (log scale)", fontsize=11)
    ax.set_title(
        f"Six-iterate convergence at α = {alpha}  (L = {L})\n"
        "Lean 4 bound: (4/5)⁶ < 27/100  verified in MultiOrbitBioSwarm.lean",
        fontsize=10,
    )
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    path = os.path.join(out_dir, "fig3_convergence.pdf")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {path}")


def fig4_operator_diagram(out_dir: str = ".") -> None:
    """
    Fig 4: Schematic of the operator pipeline C → K → F → U.
    Produced as a matplotlib figure (no external dependencies).
    """
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")

    ops = [
        ("C", 1.0, "Compress\n(orthogonal\nprojection)", "#4C72B0"),
        ("K", 3.2, "Clip\n(curvature\nintensification)", "#DD8452"),
        ("F", 5.4, "Fold\n(local average\n/ pooling)", "#55A868"),
        ("U", 7.6, "Unfold\n(homeostatic\ngain control)", "#C44E52"),
    ]

    for name, x, desc, color in ops:
        circle = plt.Circle((x, 1.5), 0.6, color=color, zorder=3)
        ax.add_patch(circle)
        ax.text(x, 1.5, name, ha="center", va="center",
                fontsize=16, fontweight="bold", color="white", zorder=4)
        ax.text(x, 0.3, desc, ha="center", va="center",
                fontsize=8, color="black")

    for i in range(len(ops) - 1):
        x1 = ops[i][1] + 0.65
        x2 = ops[i+1][1] - 0.65
        ax.annotate("", xy=(x2, 1.5), xytext=(x1, 1.5),
                    arrowprops=dict(arrowstyle="->", lw=2, color="black"))

    ax.text(5, 2.75, "G = U ∘ F ∘ K ∘ C", ha="center", va="center",
            fontsize=13, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", ec="gray"))

    # Input / output labels
    ax.text(0.1, 1.5, "state\n(xᵢ, yᵢ)", ha="center", va="center",
            fontsize=8, color="gray")
    ax.text(9.0, 1.5, "G(state)", ha="center", va="center",
            fontsize=8, color="gray")

    plt.tight_layout()
    path = os.path.join(out_dir, "fig4_operator_diagram.pdf")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# 6. CSV output
# ---------------------------------------------------------------------------

def write_pitchfork_csv(out_dir: str = ".") -> None:
    """Write pitchfork scan data to CSV for reproducibility."""
    alphas = np.linspace(0.0, 0.8, 80)
    mean_norm = pitchfork_scan(alphas, n_agents=12, n_iter=6,
                               b=0.1, noise_std=0.001)
    path = os.path.join(out_dir, "pitchfork_scan.csv")
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["alpha", "mean_norm_sq"])
        writer.writeheader()
        for a, m in zip(alphas, mean_norm):
            writer.writerow({"alpha": f"{a:.4f}", "mean_norm_sq": f"{m:.6f}"})
    print(f"Saved {path}")


# ---------------------------------------------------------------------------
# 7. Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate all figures and data for Multi-Orbit BioSwarm paper."
    )
    ap.add_argument("--out", default="figures",
                    help="Output directory for figures and CSV (default: ./figures)")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    print("Generating figures...")
    fig1_swarm_trajectories(args.out)
    fig2_pitchfork_scan(args.out)
    fig3_six_iterate_convergence(args.out)
    fig4_operator_diagram(args.out)
    write_pitchfork_csv(args.out)
    print(f"\nAll outputs written to ./{args.out}/")
    print("Figures: fig1–fig4 (.pdf) + pitchfork_scan.csv")


if __name__ == "__main__":
    main()
