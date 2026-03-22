"""
connectome_loader.py — Fly connectome graph loader
===================================================
Loads (or synthesises) a fruit-fly connectome graph, computes basic
graph metrics, and writes a visualisation to outputs/connectome_base.png.

Real data can be substituted by replacing `_synthetic_graph()` with a
loader that pulls from codex.flywire.ai (see TODO below).

Usage
-----
    pip install networkx numpy matplotlib scipy
    python connectome_loader.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import networkx as nx
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def _synthetic_graph(n_neurons: int = 200, seed: int = 42) -> nx.DiGraph:
    """Return a synthetic directed graph that mimics connectome statistics.

    Each edge is assigned a random 'weight' in (0, 1].
    TODO: replace with actual FlyWire download once credentials are available.
    """
    rng = np.random.default_rng(seed)
    G: nx.DiGraph = nx.scale_free_graph(n_neurons, seed=seed)
    # Remove self-loops that scale_free_graph may introduce
    G.remove_edges_from(list(nx.selfloop_edges(G)))
    # Assign random weights
    for u, v in G.edges():
        G[u][v]["weight"] = float(rng.uniform(0.01, 1.0))
    return G


def load_connectome(n_neurons: int = 200, seed: int = 42) -> nx.DiGraph:
    """Load the connectome graph.

    Returns a directed weighted graph where nodes are neurons and edge
    weights represent synaptic strength.
    """
    G = _synthetic_graph(n_neurons=n_neurons, seed=seed)
    print(f"[connectome_loader] nodes={G.number_of_nodes()}, "
          f"edges={G.number_of_edges()}")
    return G


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def graph_metrics(G: nx.DiGraph) -> dict:
    """Compute basic graph metrics relevant to TOGT operator analysis."""
    UG = G.to_undirected()
    degrees = [d for _, d in G.degree()]
    weights = [data["weight"] for _, _, data in G.edges(data=True)]
    return {
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "density": nx.density(G),
        "mean_degree": float(np.mean(degrees)),
        "mean_weight": float(np.mean(weights)),
        "clustering_mean": float(nx.average_clustering(UG)),
    }


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------

def visualise(G: nx.DiGraph, path: Path) -> None:
    """Draw the connectome graph and save to *path*."""
    fig, ax = plt.subplots(figsize=(8, 8))
    pos = nx.spring_layout(G, seed=42, k=0.3)
    weights = np.array([G[u][v]["weight"] for u, v in G.edges()])
    nx.draw_networkx(
        G, pos=pos, ax=ax,
        node_size=20, node_color="steelblue",
        edge_color=weights, edge_cmap=plt.cm.plasma,
        width=0.5, arrows=False, with_labels=False,
    )
    ax.set_title("Fly connectome (synthetic baseline)", fontsize=14)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[connectome_loader] saved → {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    G = load_connectome()
    metrics = graph_metrics(G)
    print("[connectome_loader] metrics:", json.dumps(metrics, indent=2))
    visualise(G, OUTPUT_DIR / "connectome_base.png")


if __name__ == "__main__":
    main()
