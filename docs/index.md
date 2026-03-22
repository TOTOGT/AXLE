# AXLE Documentation

**AXLE** is the formal verification and simulation hub for the
**Topographical Orthogonal Generative Theory (TOGT)** developed by
G6 LLC (Pablo Nogueira Grossi, Newark NJ, 2026).

---

## Repository Structure

```
AXLE/
├── lean-toolchain           ← Lean 4 version pin
├── lakefile.toml            ← Lean 4 + Mathlib project file
├── lean/
│   └── Main.lean            ← Core TOGT formalization (proved theorems)
├── simulations/
│   ├── connectome_loader.py ← Fly connectome graph loader
│   └── simple_to_operator.py← C→K→F→U operator chain + dm³ metrics
├── mappings/
│   └── domain_mappings.md   ← C→K→F→U across 6 domains
└── docs/
    └── index.md             ← This file
```

---

## Lean 4 — Building the Proofs

### Prerequisites

- [elan](https://github.com/leanprover/elan) — Lean version manager
- Internet access (Mathlib is downloaded on first build)

### Build

```bash
cd AXLE
# First run: downloads Mathlib cache (~1–5 min)
lake update
lake build
```

`lake build` typecheck-passes with zero `sorry`s.

### Types defined in `lean/Main.lean`

| Type | Description |
|------|-------------|
| `Operator α` | Endofunction wrapper |
| `Chain α` | Ordered list of operators |
| `CompressionOp α` | C — contractive injective map |
| `CurvatureOp α` | K — drives Φ toward threshold κ* |
| `FoldOp α` | F — Whitney A₁–A₃ singularity |
| `UnfoldOp α` | U — fixed-point attractor selection |
| `GenerativeOp` | G = U ∘ F ∘ K ∘ C (four-step chain) |
| `RegenerationLevel` | Level index + layer count in regeneration hierarchy |

### Theorems

| Theorem | Statement |
|---------|-----------|
| `noiseTolerance_times_stabilityRadius` | τ · ε₀ = 2/3 |
| `crystal_aspect_ratio` | 66 = 2 × g⁶ |
| `g6_equals_schumann` | g⁶ = 33 |
| `crystal_base_perimeter` | 4 × 500 = 2000 cubits |
| `chain_concat_wellformed` | WellFormed preserved under concatenation |
| `chain_concat_apply` | Composition identity for Chain |
| `generativeOp_wellformed` | GenerativeOp is always well-formed |
| `regeneration_unbounded` | ∀ n, ∃ RegenerationLevel with idx ≥ n |

---

## Python Simulations — Running the Operator Chain

### Prerequisites

```bash
pip install networkx numpy matplotlib scipy
```

### Run

```bash
cd simulations

# 1. Generate baseline connectome visualisation
python connectome_loader.py
#   → outputs/connectome_base.png

# 2. Apply C → K → F → U and compute dm³ metrics
python simple_to_operator.py
#   → outputs/connectome_before_after.png
#   → outputs/dm3_metrics.json
```

### dm³ Metric Interpretation

After the U step the script reports:

```json
{
  "epsilon0": 0.3333,
  "tau": <computed>,
  "kappa": <mean clustering>,
  "c": <mean edge weight>,
  "arnold_ok": true/false
}
```

`arnold_ok = true` means the graph is within the Arnold tongue:
`|τ − τ_canonical| / τ_canonical < ε₀`.

---

## Domain Mappings

See [`mappings/domain_mappings.md`](../mappings/domain_mappings.md) for a
table of how C → K → F → U instantiates across:

1. Plasma physics
2. Biological morphogenesis
3. Fruit-fly connectome
4. Abstract dm³ metric space
5. Martian colony architecture
6. Large-cardinal hierarchy (Lean)

---

## Canonical Invariants

| Symbol | Value | Source |
|--------|-------|--------|
| ε₀ | 1/3 | Stability radius |
| τ | 2 | Noise-tolerance coefficient |
| g⁶ | 33 | Schumann 4th harmonic integer |
| τ · ε₀ | 2/3 | Arnold-tongue half-width |

---

## Roadmap

- **Issue #2**: Replace `axiom regeneration_step` with a full Lean proof
  using Mathlib's ordinal / large-cardinal hierarchy.
- **Issue #3**: Load the real FlyWire connectome from codex.flywire.ai.
- **Issue #4**: Martian colony dm³ mapping (closed-loop life support).

---

*C → K → F → U → ∞*  
G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026
