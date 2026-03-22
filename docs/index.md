# AXLE Documentation

**Formal verification hub for Topographical Orthogenetics (TO) and  
Topographical Orthogonal Generative Theory (TOGT)**

G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026  
MIT License · [github.com/TOTOGT/AXLE](https://github.com/TOTOGT/AXLE)

---

## What AXLE Is

AXLE is the computational and formal verification companion to the
*Principia Orthogona* series. Where the books state theorems and proofs
in mathematical prose, AXLE makes them machine-checkable (Lean 4) and
computationally demonstrable (Python simulations).

The name encodes the structure: AXLE is the axis around which the
operator chain $C \to K \to F \to U$ rotates — the fixed center
that everything else turns on.

The fruit fly 🪰 is the toy machine: small enough to simulate completely,
complex enough to instantiate the full operator chain, and the organism
whose connectome is the best-mapped neural system on Earth.

---

## Repository Structure

```
AXLE/
├── lean/
│   └── Main.lean          — Lean 4 formalization of TOGT core
├── simulations/
│   ├── connectome_loader.py    — Load/generate fly connectome graph
│   └── simple_to_operator.py  — Apply C→K→F→U, compute dm³ metric
├── mappings/
│   └── domain_mappings.md     — C→K→F→U across six domains
├── docs/
│   └── index.md               — This file
├── lakefile.toml              — Lean 4 / Mathlib project file
├── README.md
├── topics.json
└── LICENSE (MIT)
```

---

## The Core Framework

### The Generative Operator

$$\mathcal{G} = U \circ F \circ K \circ C : X \to X$$

Acting on trajectories in a Riemannian manifold $(X, g)$:

| Symbol | Name | Action |
|---|---|---|
| $C$ | Compression | Reduces degrees of freedom, preserves distinguishability |
| $K$ | Curvature | Drives curvature toward intrinsic threshold $\kappa^*$ |
| $F$ | Fold | Triggered at $\|\kappa\| = \kappa^*$; rank-1 Jacobian loss |
| $U$ | Unfold | Selects stable branch via gradient descent on Morse functional |

### The dm³ Canonical Invariants

The explicit toy model on $M = S \times \mathbb{R}$ with contact form $\alpha = dz - r^2 d\theta$ realizes:

$$\iota(\mathfrak{D}) = (T^*, \mu_{\max}, \tau) = (2\pi, -2, 2)$$

| Invariant | Value | Meaning |
|---|---|---|
| $T^*$ | $2\pi$ | Limit cycle period |
| $\mu_{\max}$ | $-2$ | Maximal transverse Lyapunov exponent |
| $\tau$ | $2$ | Embodiment threshold: $\tau = \sqrt{c/\kappa} = \sqrt{4/1}$ |
| $\varepsilon_0$ | $1/3$ | Structural stability radius |

### The g⁶ Crystal

The generative operator applied six times to a structure anchored at
31.5°N (Israel) terminates at the tropopause at layer count $g^6 = 33$.

The 4th Schumann harmonic of the Earth-ionosphere cavity is $f_4 = 33.5$ Hz.

The aspect ratio is $\text{height}/\text{base} = 33{,}000/500 = 66 = g^6 \cdot \tau$.

In TOGT there are no coincidences.

---

## How to Run the Simulations

```bash
# Install dependencies
pip install networkx numpy matplotlib scipy

# Load connectome and visualize
cd simulations
python connectome_loader.py

# Apply operator chain and compute dm³ metric
python simple_to_operator.py
# → outputs/connectome_before_after.png
# → outputs/dm3_metrics.json
```

---

## How to Check the Lean Proofs

```bash
# Install Lean 4 and lake (https://leanprover.github.io/lean4/doc/setup.html)
# Then from repo root:
lake update
lake build
# → Checks Main.lean against Mathlib
```

Key theorems currently formalized:
- `TOGT.noiseTolerance` — $\tau \cdot \varepsilon_0 = 2/3$
- `TOGT.stabilityRadius_eq` — $\varepsilon_0 = 1/3$
- `TOGT.crystal_aspect_ratio` — height/base = 66
- `TOGT.aspect_ratio_encodes_invariants` — $66 = g^6 \cdot \tau$
- `TOGT.crystal_base_perimeter` — base perimeter = 2000 cubits
- `TOGT.g6_equals_schumann` — $g^6 = $ Schumann 4th harmonic integer
- `TOGT.regeneration_unbounded` — hierarchy is unbounded

---

## Related Work

| Item | Link |
|---|---|
| *Applications of GOMC Science* (book) | Zenodo: [10.5281/zenodo.19117400](https://doi.org/10.5281/zenodo.19117400) |
| HAL preprints | hal-05555216, hal-05559997 |
| X threads | [@unitedWeStreamU](https://x.com/unitedWeStreamU) — search "AXLE" |
| FlyWire connectome | [codex.flywire.ai](https://codex.flywire.ai/api/download) |
| Mathlib4 | [leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4) |

---

## Contact

Pablo Nogueira Grossi  
G6 LLC · Newark, NJ · 2026  
pablogrossi@hotmail.com  
ORCID: 0009-0000-6496-2186

$$C \to K \to F \to U \to \infty$$
