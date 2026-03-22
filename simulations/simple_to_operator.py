"""
simple_to_operator.py — C → K → F → U operator chain + dm³ metrics
====================================================================
Applies the four TOGT operators to a connectome graph in sequence and
computes the canonical dm³ triple (ε₀, τ, κ) after each step.

Operator semantics (graph-level implementation)
-----------------------------------------------
C  (Compression)  — remove edges below the 25th-percentile weight
K  (Curvature)    — reweight edges by the local clustering coefficient
F  (Fold)         — collapse high-betweenness "fold nodes" (rank-1 drop)
U  (Unfold)       — PageRank-weighted stable-branch selection

dm³ metric
----------
Given the graph after the U step:
    κ  = mean clustering coefficient
    c  = mean edge weight (proxy for curvature)
    τ  = sqrt(c / κ)          [noise-tolerance coefficient]
    ε₀ = 1/3                  [canonical stability radius]

Arnold-tongue check: |τ - τ_canonical| / τ_canonical < ε₀

Usage
-----
    pip install networkx numpy matplotlib scipy
    cd simulations
    python simple_to_operator.py
    # → outputs/connectome_before_after.png
    # → outputs/dm3_metrics.json
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Tuple

import networkx as nx
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Local import — connectome_loader must be on the path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from connectome_loader import load_connectome

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Canonical invariants (matching lean/Main.lean)
# ---------------------------------------------------------------------------
STABILITY_RADIUS: float = 1.0 / 3.0   # ε₀
NOISE_TOLERANCE_CANONICAL: float = 2.0  # τ_canonical

# ---------------------------------------------------------------------------
# Operator implementations
# ---------------------------------------------------------------------------

def op_compress(G: nx.DiGraph) -> nx.DiGraph:
    """C — Compression: remove edges whose weight is below the 25th percentile.

    Contractive (reduces edge count) and injective (no node merging).
    """
    if G.number_of_edges() == 0:
        return G.copy()
    weights = [d["weight"] for _, _, d in G.edges(data=True)]
    threshold = float(np.percentile(weights, 25))
    H = G.copy()
    to_remove = [(u, v) for u, v, d in H.edges(data=True) if d["weight"] < threshold]
    H.remove_edges_from(to_remove)
    return H


def op_curvature(G: nx.DiGraph) -> nx.DiGraph:
    """K — Curvature: rescale edge weights by the local clustering coefficient.

    Drives the graph toward the critical threshold κ* by amplifying
    edges in highly-clustered neighbourhoods.
    """
    H = G.copy()
    UG = H.to_undirected()
    clust = nx.clustering(UG)
    for u, v in H.edges():
        coeff = (clust.get(u, 0.0) + clust.get(v, 0.0)) / 2.0
        H[u][v]["weight"] *= max(coeff, 1e-6)
    return H


def op_fold(G: nx.DiGraph) -> nx.DiGraph:
    """F — Fold: collapse nodes whose betweenness exceeds the 75th percentile.

    Models a Whitney A₁ singularity: high-betweenness "fold nodes" are
    merged with their highest-weight neighbour, causing a rank-1 drop in
    the incidence structure.
    """
    if G.number_of_nodes() < 2:
        return G.copy()
    betweenness = nx.betweenness_centrality(G)
    values = list(betweenness.values())
    threshold = float(np.percentile(values, 75))
    fold_nodes = [n for n, b in betweenness.items() if b >= threshold]
    H = G.copy()
    for node in fold_nodes:
        if node not in H:
            continue
        neighbours = list(H.successors(node)) + list(H.predecessors(node))
        if not neighbours:
            continue
        # Merge into the neighbour with the highest edge weight
        best = max(
            neighbours,
            key=lambda nb: H[node][nb]["weight"] if H.has_edge(node, nb)
                           else H[nb][node].get("weight", 0.0)
        )
        nx.contracted_nodes(H, best, node, self_loops=False, copy=False)
    return H


def op_unfold(G: nx.DiGraph) -> nx.DiGraph:
    """U — Unfold: select the stable branch via PageRank.

    Retains only edges whose combined endpoint PageRank exceeds the mean,
    landing the system on a fixed-point attractor.
    """
    if G.number_of_edges() == 0:
        return G.copy()
    pagerank = nx.pagerank(G, weight="weight")
    mean_pr = float(np.mean(list(pagerank.values())))
    H = G.copy()
    to_remove = [
        (u, v) for u, v in H.edges()
        if pagerank.get(u, 0.0) + pagerank.get(v, 0.0) < mean_pr
    ]
    H.remove_edges_from(to_remove)
    return H


# ---------------------------------------------------------------------------
# dm³ metric computation
# ---------------------------------------------------------------------------

def dm3_metrics(G: nx.DiGraph) -> dict:
    """Compute the canonical dm³ triple (ε₀, τ, κ) for graph *G*.

    Returns
    -------
    dict with keys:
        epsilon0      — stability radius (always 1/3)
        tau           — computed noise-tolerance coefficient
        kappa         — mean clustering coefficient
        c             — mean edge weight (curvature proxy)
        arnold_ok     — True iff |τ - τ_canonical| / τ_canonical < ε₀
    """
    UG = G.to_undirected()
    kappa = nx.average_clustering(UG) if G.number_of_nodes() > 0 else 0.0
    weights = [d["weight"] for _, _, d in G.edges(data=True)]
    c = float(np.mean(weights)) if weights else 0.0
    tau = float(np.sqrt(c / kappa)) if kappa > 1e-9 else 0.0
    arnold_ok = (
        abs(tau - NOISE_TOLERANCE_CANONICAL) / NOISE_TOLERANCE_CANONICAL
        < STABILITY_RADIUS
    )
    return {
        "epsilon0": STABILITY_RADIUS,
        "tau": tau,
        "kappa": kappa,
        "c": c,
        "arnold_ok": bool(arnold_ok),
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
    }


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(G: nx.DiGraph) -> Tuple[nx.DiGraph, dict]:
    """Apply C → K → F → U in sequence, returning the final graph and metrics."""
    steps = [
        ("C (Compress)", op_compress),
        ("K (Curvature)", op_curvature),
        ("F (Fold)", op_fold),
        ("U (Unfold)", op_unfold),
    ]
    H = G
    for label, op in steps:
        H = op(H)
        print(f"[pipeline] after {label}: "
              f"nodes={H.number_of_nodes()}, edges={H.number_of_edges()}")
    return H, dm3_metrics(H)


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------

def visualise_before_after(G_before: nx.DiGraph, G_after: nx.DiGraph,
                            path: Path) -> None:
    """Side-by-side plot of the connectome before and after the pipeline."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    pos_before = nx.spring_layout(G_before, seed=42, k=0.3)
    pos_after = nx.spring_layout(G_after, seed=42, k=0.3)

    def _draw(ax: plt.Axes, G: nx.DiGraph, pos: dict, title: str) -> None:
        weights = np.array([G[u][v]["weight"] for u, v in G.edges()]) if G.number_of_edges() > 0 else []
        nx.draw_networkx(
            G, pos=pos, ax=ax,
            node_size=20, node_color="steelblue",
            edge_color=weights if len(weights) > 0 else "grey",
            edge_cmap=plt.cm.plasma if len(weights) > 0 else None,
            width=0.5, arrows=False, with_labels=False,
        )
        ax.set_title(title, fontsize=12)
        ax.axis("off")

    _draw(axes[0], G_before, pos_before, "Before (baseline)")
    _draw(axes[1], G_after, pos_after, "After C → K → F → U")
    fig.suptitle("AXLE: C → K → F → U operator chain", fontsize=14)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[simple_to_operator] saved → {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    G = load_connectome()
    G_final, metrics = run_pipeline(G)
    print("[simple_to_operator] dm³ metrics:", json.dumps(metrics, indent=2))

    metrics_path = OUTPUT_DIR / "dm3_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2))
    print(f"[simple_to_operator] saved → {metrics_path}")

    visualise_before_after(G, G_final, OUTPUT_DIR / "connectome_before_after.png")


if __name__ == "__main__":
    main()
