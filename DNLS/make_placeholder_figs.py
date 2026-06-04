"""
Create lightweight placeholder PDFs for fig1-fig5 so paper_v3.tex compiles.
The user should replace these with the actual fig1-fig5 from the original
generate_figures.py output (they already exist alongside the v2 paper).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIGS = [
    ("fig1_chain_structure",   "Substitution chain structure (Fibonacci & Tribonacci)"),
    ("fig2_eigenstates",       "Mid-gap critical eigenstates |psi_j|^2"),
    ("fig3_ipr_vs_lambda",     "IPR at T=50 vs lambda"),
    ("fig4_ipr_ratio",         "IPR ratio trib/fib at T=50 vs lambda"),
    ("fig5_substitution_tree", "Substitution trees (Fibonacci & Tribonacci)"),
]

for name, title in FIGS:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.55, title, ha="center", va="center",
            fontsize=14, color="#444", family="serif")
    ax.text(0.5, 0.35,
            "(placeholder — regenerate from generate_figures.py in v2 toolchain)",
            ha="center", va="center", fontsize=9, color="#888",
            style="italic", family="serif")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("#cccccc")
        spine.set_linewidth(0.5)
    fig.savefig(f"figures/{name}.pdf", bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    print(f"saved figures/{name}.pdf (placeholder)")
