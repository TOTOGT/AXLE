"""
AXLE — Topographical Orthogenetics Simulations
connectome_loader.py

Loads the Drosophila connectome (FlyWire or synthetic fallback)
as a directed NetworkX graph, ready for TOGT operator application.

G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026
MIT License
"""

import json
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


# ── CONSTANTS ────────────────────────────────────────────────────────────────

FLYWIRE_API = "https://codex.flywire.ai/api/download"
SYNTHETIC_N_NEURONS   = 200    # nodes in synthetic fallback
SYNTHETIC_N_SYNAPSES  = 800    # edges in synthetic fallback
RANDOM_SEED           = 42


# ── LOADER ───────────────────────────────────────────────────────────────────

def load_connectome(source: str = "synthetic") -> nx.DiGraph:
    """
    Load the fruit fly connectome as a directed graph.

    Parameters
    ----------
    source : str
        "synthetic"  — generate a synthetic scale-free connectome
        "flywire"    — attempt to load from local FlyWire CSV export
                       (download from https://codex.flywire.ai/api/download
                        and place as data/flywire_connections.csv)

    Returns
    -------
    nx.DiGraph with node attribute 'type' and edge attribute 'weight'
    """
    if source == "flywire":
        return _load_flywire()
    else:
        return _synthetic_connectome()


def _load_flywire() -> nx.DiGraph:
    csv_path = Path("data/flywire_connections.csv")
    if not csv_path.exists():
        print(f"[AXLE] FlyWire CSV not found at {csv_path}.")
        print(f"[AXLE] Download from: {FLYWIRE_API}")
        print("[AXLE] Falling back to synthetic connectome.")
        return _synthetic_connectome()

    import csv
    G = nx.DiGraph()
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = int(row.get("pre_root_id", row.get("pre", 0)))
            tgt = int(row.get("post_root_id", row.get("post", 0)))
            w   = float(row.get("syn_count", row.get("weight", 1.0)))
            G.add_edge(src, tgt, weight=w)
    print(f"[AXLE] FlyWire connectome loaded: "
          f"{G.number_of_nodes()} neurons, {G.number_of_edges()} synapses")
    return G


def _synthetic_connectome() -> nx.DiGraph:
    """
    Synthetic scale-free directed graph mimicking fly connectome topology.
    Uses Barabási–Albert model (power-law degree distribution),
    consistent with real connectome statistics.
    """
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    # Undirected BA graph → convert to directed
    G_undirected = nx.barabasi_albert_graph(
        SYNTHETIC_N_NEURONS, m=4, seed=RANDOM_SEED)
    G = nx.DiGraph()

    neuron_types = ["sensory", "interneuron", "motor", "projection"]
    for node in G_undirected.nodes():
        G.add_node(node, type=random.choice(neuron_types),
                   layer=node // (SYNTHETIC_N_NEURONS // 6))  # g-layer assignment

    for u, v in G_undirected.edges():
        weight = float(np.random.exponential(scale=3.0))
        G.add_edge(u, v, weight=weight)
        # ~30% bidirectional (recurrent connections)
        if random.random() < 0.3:
            G.add_edge(v, u, weight=float(np.random.exponential(scale=1.5)))

    print(f"[AXLE] Synthetic connectome: "
          f"{G.number_of_nodes()} neurons, {G.number_of_edges()} synapses")
    print(f"[AXLE] Degree distribution: power-law (BA model, m=4)")
    return G


# ── GRAPH STATISTICS ─────────────────────────────────────────────────────────

def connectome_stats(G: nx.DiGraph) -> dict:
    """Compute basic statistics relevant to TOGT operator application."""
    stats = {
        "n_neurons":     G.number_of_nodes(),
        "n_synapses":    G.number_of_edges(),
        "density":       nx.density(G),
        "is_weakly_connected": nx.is_weakly_connected(G),
        "n_weakly_connected_components":
            nx.number_weakly_connected_components(G),
        "avg_in_degree":  np.mean([d for _, d in G.in_degree()]),
        "avg_out_degree": np.mean([d for _, d in G.out_degree()]),
        "max_in_degree":  max(d for _, d in G.in_degree()),
        "max_out_degree": max(d for _, d in G.out_degree()),
    }
    # Largest weakly connected component size
    lcc = max(nx.weakly_connected_components(G), key=len)
    stats["lcc_size"] = len(lcc)
    stats["lcc_fraction"] = len(lcc) / G.number_of_nodes()
    return stats


# ── VISUALIZATION ─────────────────────────────────────────────────────────────

def visualize_connectome(G: nx.DiGraph,
                         title: str = "Fly Connectome",
                         max_nodes: int = 80,
                         ax=None):
    """
    Draw a subgraph of the connectome.
    Colors nodes by g-layer (operator iterate level).
    """
    # Sample for visibility
    nodes = list(G.nodes())[:max_nodes]
    H = G.subgraph(nodes)

    layer_colors = {
        0: "#0ABAB5",   # g¹ — Tiffany
        1: "#22CFCA",   # g²
        2: "#3DDBD6",   # g³
        3: "#5AE5E0",   # g⁴
        4: "#78EFEB",   # g⁵
        5: "#DFFFFD",   # g⁶ — apex
    }
    node_colors = [
        layer_colors.get(H.nodes[n].get("layer", 0) % 6, "#0ABAB5")
        for n in H.nodes()
    ]

    pos = nx.spring_layout(H, seed=RANDOM_SEED, k=0.6)
    weights = [H[u][v]["weight"] for u, v in H.edges()]
    max_w = max(weights) if weights else 1.0

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor("#00040F")
    ax.set_facecolor("#00040F")

    nx.draw_networkx_nodes(H, pos, node_color=node_colors,
                           node_size=40, alpha=0.9, ax=ax)
    nx.draw_networkx_edges(H, pos,
                           width=[0.5 + 2.0 * w / max_w for w in weights],
                           edge_color="#0ABAB5", alpha=0.35,
                           arrows=True, arrowsize=6, ax=ax)
    ax.set_title(title, color="#F5F0E8", fontsize=13)
    ax.axis("off")
    return ax


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("AXLE — Connectome Loader")
    print("G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026")
    print("=" * 60)
    print()

    G = load_connectome("synthetic")

    stats = connectome_stats(G)
    print("\n[AXLE] Connectome statistics:")
    for k, v in stats.items():
        print(f"  {k:40s} {v}")

    print("\n[AXLE] Rendering connectome visualization...")
    fig, ax = plt.subplots(figsize=(12, 9))
    fig.patch.set_facecolor("#00040F")
    visualize_connectome(G, title="Drosophila Connectome — TOGT Layer Coloring", ax=ax)

    out = Path("outputs")
    out.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(out / "connectome_base.png", dpi=150,
                facecolor="#00040F", bbox_inches="tight")
    print(f"[AXLE] Saved: outputs/connectome_base.png")
    plt.close()
    print("[AXLE] Done. Next: run simple_to_operator.py")
