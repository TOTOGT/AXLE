"""
AXLE — Topographical Orthogenetics Simulations
simple_to_operator.py

Applies the TOGT operator chain C → K → F → U to the fruit fly
connectome graph and computes the dm³ metric (embodiment threshold τ)
on neuron clusters. Produces before/after visualization.

The operators are implemented as graph transformations:
  C (Compression):   remove low-weight edges, merge near-identical nodes
  K (Curvature):     reweight edges by local clustering coefficient
  F (Fold):          identify and mark fold nodes (high betweenness, rank drop)
  U (Unfold):        select stable attractor subgraph via PageRank

dm³ metric: τ = √(c/κ) where
  c   = mean edge weight after K (Lyapunov rate)
  κ   = noise amplitude = std of weight distribution

G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026
MIT License
"""

import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from connectome_loader import load_connectome, visualize_connectome, connectome_stats

# ── CANONICAL CONSTANTS (from dm3 toy model) ─────────────────────────────────

TAU_CANONICAL   = 2.0        # embodiment threshold
MU_MAX          = -2.0       # maximal transverse Lyapunov exponent
T_STAR          = 2 * math.pi  # limit cycle period
EPS_0           = 1 / 3     # structural stability radius
G6_LAYER_COUNT  = 33        # apex layer count


# ── C: COMPRESSION OPERATOR ──────────────────────────────────────────────────

def operator_C(G: nx.DiGraph, threshold_quantile: float = 0.25) -> nx.DiGraph:
    """
    Compression C: remove edges below the threshold_quantile weight.
    Preserves distinguishability (no two distinct nodes become identical).
    Returns a new graph.
    """
    weights = [d["weight"] for _, _, d in G.edges(data=True)]
    if not weights:
        return G.copy()
    threshold = float(np.quantile(weights, threshold_quantile))

    G_C = nx.DiGraph()
    G_C.add_nodes_from(G.nodes(data=True))
    for u, v, data in G.edges(data=True):
        if data["weight"] >= threshold:
            G_C.add_edge(u, v, **data)

    n_removed = G.number_of_edges() - G_C.number_of_edges()
    print(f"[C] Compression: removed {n_removed} edges "
          f"(threshold={threshold:.3f}, kept "
          f"{G_C.number_of_edges()}/{G.number_of_edges()})")
    return G_C


# ── K: CURVATURE OPERATOR ────────────────────────────────────────────────────

def operator_K(G: nx.DiGraph) -> nx.DiGraph:
    """
    Curvature K: reweight edges by local clustering coefficient.
    Nodes with high local clustering (high curvature) get amplified weights,
    driving trajectories toward the intrinsic threshold κ*.
    """
    G_K = G.copy()
    # clustering on underlying undirected graph
    G_und = G.to_undirected()
    clustering = nx.clustering(G_und)

    for u, v, data in G_K.edges(data=True):
        kappa = (clustering.get(u, 0) + clustering.get(v, 0)) / 2.0
        # K drives weight toward κ* — amplify by (1 + κ)
        G_K[u][v]["weight"] = data["weight"] * (1.0 + kappa)
        G_K[u][v]["curvature"] = kappa

    print(f"[K] Curvature: mean curvature = "
          f"{np.mean(list(clustering.values())):.4f}")
    return G_K


# ── F: FOLD OPERATOR ─────────────────────────────────────────────────────────

def operator_F(G: nx.DiGraph, fold_quantile: float = 0.90) -> nx.DiGraph:
    """
    Fold F: identify fold nodes (high betweenness centrality → rank-1 drop).
    Mark fold nodes; merge their out-edges to a single target (loss of injectivity).
    Returns graph with fold metadata.
    """
    G_F = G.copy()

    # Betweenness centrality identifies high-curvature fold points
    betweenness = nx.betweenness_centrality(G_F)
    threshold = float(np.quantile(list(betweenness.values()), fold_quantile))
    fold_nodes = {n for n, b in betweenness.items() if b >= threshold}

    for n in G_F.nodes():
        G_F.nodes[n]["is_fold"] = n in fold_nodes
        G_F.nodes[n]["betweenness"] = betweenness[n]

    # Fold: for each fold node, collapse all out-edges to highest-weight target
    fold_count = 0
    for n in fold_nodes:
        out_edges = list(G_F.out_edges(n, data=True))
        if len(out_edges) > 1:
            # Keep only the strongest connection (Whitney A₁ local model)
            best = max(out_edges, key=lambda e: e[2].get("weight", 0))
            for u, v, _ in out_edges:
                if v != best[1]:
                    G_F.remove_edge(u, v)
                    fold_count += 1

    print(f"[F] Fold: {len(fold_nodes)} fold nodes identified, "
          f"{fold_count} edges collapsed")
    return G_F


# ── U: UNFOLD OPERATOR ───────────────────────────────────────────────────────

def operator_U(G: nx.DiGraph, top_k_fraction: float = 0.40) -> nx.DiGraph:
    """
    Unfold U: select stable attractor subgraph via PageRank (gradient descent on Φ).
    Retains the top_k_fraction of nodes by PageRank score — the stable branch.
    """
    pagerank = nx.pagerank(G, alpha=0.85, weight="weight")
    n_keep = max(1, int(len(pagerank) * top_k_fraction))
    top_nodes = sorted(pagerank, key=pagerank.get, reverse=True)[:n_keep]
    top_set = set(top_nodes)

    G_U = G.subgraph(top_nodes).copy()
    for n in G_U.nodes():
        G_U.nodes[n]["pagerank"] = pagerank[n]

    print(f"[U] Unfold: retained {G_U.number_of_nodes()} / {G.number_of_nodes()} "
          f"neurons on stable branch")
    return G_U


# ── DM³ METRIC ────────────────────────────────────────────────────────────────

def dm3_metric(G_before: nx.DiGraph, G_after: nx.DiGraph) -> dict:
    """
    Compute the dm³ embodiment threshold τ = √(c/κ) on the graph.

      c   = mean edge weight of G_after  (Lyapunov rate estimate)
      κ   = std of edge weight distribution  (noise amplitude estimate)
      τ   = √(c/κ)

    Also computes:
      μ_max estimate from the spectral gap of the adjacency matrix
      ε₀ estimate from τ and μ_max
    """
    weights_after = [d["weight"] for _, _, d in G_after.edges(data=True)]
    if not weights_after:
        return {"tau": 0, "c": 0, "kappa": 0, "mu_max_est": 0, "eps0_est": 0}

    c     = float(np.mean(weights_after))
    kappa = float(np.std(weights_after)) if np.std(weights_after) > 0 else 1e-6
    tau   = math.sqrt(c / kappa)

    # Spectral gap of largest weakly connected component adjacency
    lcc_nodes = max(nx.weakly_connected_components(G_after), key=len)
    H = G_after.subgraph(lcc_nodes).copy()
    A = nx.to_numpy_array(H, weight="weight")
    eigvals = np.linalg.eigvals(A)
    eigvals_real = np.sort(np.real(eigvals))[::-1]
    mu_max_est = float(eigvals_real[1]) if len(eigvals_real) > 1 else 0.0
    # Normalize to [-2, 0] range for comparison with canonical
    if eigvals_real[0] != 0:
        mu_max_est = mu_max_est / eigvals_real[0] * MU_MAX

    eps0_est = abs(mu_max_est) / (2 * (1 + 2.0))  # Hess V = 2 in toy model

    # Graph embedding distance (dm³ as distance from canonical)
    tau_deviation   = abs(tau - TAU_CANONICAL) / TAU_CANONICAL
    mu_deviation    = abs(mu_max_est - MU_MAX) / abs(MU_MAX)
    dm3_distance    = math.sqrt(tau_deviation**2 + mu_deviation**2)

    return {
        "c":            c,
        "kappa_noise":  kappa,
        "tau":          tau,
        "tau_canonical": TAU_CANONICAL,
        "tau_deviation": tau_deviation,
        "mu_max_est":   mu_max_est,
        "mu_max_canonical": MU_MAX,
        "eps0_est":     eps0_est,
        "eps0_canonical": EPS_0,
        "dm3_distance": dm3_distance,
        "in_arnold_tongue": tau_deviation < EPS_0,
    }


# ── FULL PIPELINE ─────────────────────────────────────────────────────────────

def run_pipeline(G: nx.DiGraph) -> tuple:
    """
    Apply G = U ∘ F ∘ K ∘ C to the connectome graph.
    Returns (G_final, metrics_dict).
    """
    print("\n" + "="*60)
    print("TOGT Operator Chain: C → K → F → U")
    print("="*60)

    G_C = operator_C(G)
    G_K = operator_K(G_C)
    G_F = operator_F(G_K)
    G_U = operator_U(G_F)

    print("\n[dm³] Computing embodiment threshold τ...")
    metrics = dm3_metric(G, G_U)

    print(f"\n[dm³] Results:")
    print(f"  c (Lyapunov rate):          {metrics['c']:.4f}")
    print(f"  κ (noise amplitude):        {metrics['kappa_noise']:.4f}")
    print(f"  τ (embodiment threshold):   {metrics['tau']:.4f}  "
          f"(canonical: {TAU_CANONICAL})")
    print(f"  μ_max estimate:             {metrics['mu_max_est']:.4f}  "
          f"(canonical: {MU_MAX})")
    print(f"  ε₀ estimate:                {metrics['eps0_est']:.4f}  "
          f"(canonical: {EPS_0:.4f})")
    print(f"  dm³ distance from canonical:{metrics['dm3_distance']:.4f}")
    print(f"  In Arnold tongue (< ε₀):    {metrics['in_arnold_tongue']}")

    return G_U, metrics


# ── VISUALIZATION ─────────────────────────────────────────────────────────────

def visualize_before_after(G_before: nx.DiGraph,
                            G_after: nx.DiGraph,
                            metrics: dict,
                            output_path: Path = None):
    """Before/after visualization of the operator chain application."""
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.patch.set_facecolor("#00040F")

    visualize_connectome(G_before,
                         title=f"Before G  —  {G_before.number_of_nodes()} neurons, "
                               f"{G_before.number_of_edges()} synapses",
                         ax=axes[0])
    visualize_connectome(G_after,
                         title=f"After G = U∘F∘K∘C  —  "
                               f"{G_after.number_of_nodes()} neurons, "
                               f"{G_after.number_of_edges()} synapses",
                         ax=axes[1])

    # Metrics annotation
    ann = (
        f"τ = {metrics['tau']:.3f}  (canonical: {TAU_CANONICAL})\n"
        f"μ_max ≈ {metrics['mu_max_est']:.3f}  (canonical: {MU_MAX})\n"
        f"ε₀ ≈ {metrics['eps0_est']:.3f}  (canonical: {EPS_0:.3f})\n"
        f"dm³ distance: {metrics['dm3_distance']:.4f}\n"
        f"Arnold tongue: {'YES ✓' if metrics['in_arnold_tongue'] else 'NO'}"
    )
    fig.text(0.5, 0.02, ann, ha="center", va="bottom",
             color="#C9A84C", fontsize=10,
             bbox=dict(facecolor="#060A12", edgecolor="#0ABAB5",
                       boxstyle="round,pad=0.4"))

    fig.suptitle(
        "AXLE — Fly Connectome under TOGT Operator G = U∘F∘K∘C\n"
        "G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026",
        color="#F5F0E8", fontsize=12, y=1.01
    )

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, facecolor="#00040F",
                    bbox_inches="tight")
        print(f"[AXLE] Saved: {output_path}")
    plt.show()
    plt.close()


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("AXLE — TOGT Operator Chain Simulation")
    print("G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026")
    print("=" * 60)

    G = load_connectome("synthetic")
    G_final, metrics = run_pipeline(G)

    out = Path("outputs")
    out.mkdir(exist_ok=True)
    visualize_before_after(G, G_final, metrics,
                           output_path=out / "connectome_before_after.png")

    # Save metrics as JSON
    import json
    metrics_serializable = {k: float(v) if isinstance(v, (np.floating, float))
                            else v
                            for k, v in metrics.items()}
    with open(out / "dm3_metrics.json", "w") as f:
        json.dump(metrics_serializable, f, indent=2)
    print(f"[AXLE] Metrics saved: outputs/dm3_metrics.json")
    print("\n[AXLE] C → K → F → U → ∞")
