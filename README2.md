# TOGT / AXLE — Principia Orthogona

**Topographical Orthogonal Generative Theory**  
*A structural framework for generative emergence across domains*

---

## Overview

This repository contains diagrams, papers, and formal materials for the **TOGT (Topographical Orthogonal Generative Theory)** / **GTCT (Generative Contact Theory)** framework developed in *Principia Orthogona* (Volumes I–VI, G6 LLC).

The core claim: a single operator algebra `G = U ∘ F ∘ K ∘ C` — Unfolding, Folding, Curvature, Compression — generates the contact geometry underlying stable structures across physical, biological, economic, and mathematical domains. Not as analogy, but as exact morphisms in the category **dm³**.

---

## Diagrams

| File | Description |
|------|-------------|
| `diagrams/01_operator_sequence.svg` | The four-operator sequence G = U∘F∘K∘C with domain instantiations |
| `diagrams/02_saturn_hexagon.svg` | Saturn's north polar hexagon as canonical dm³ instantiation |
| `diagrams/03_coherence_bridge.svg` | Coherence Bridge Theorem — functors across 6 domains |
| `diagrams/04_collatz_dm3.svg` | Collatz conjecture as dm³ system (AXLE Target 5) |
| `diagrams/05_domain_map.svg` | Full application domain survey (20+ fields) |

---

## The Operator Algebra

```
C (Compression):   Lipschitz map onto lower-dimensional submanifold. κ = Lip(C) < 1
K (Curvature):     Riemannian curvature drives orbit toward critical threshold κ*
F (Folding):       Whitney A₁ singularity fires at κ*. det(Df) → 0. Geometry locks.
U (Unfolding):     Gradient descent on Lyapunov Φ selects stable attractor. ∇Φ = 0
```

**Convergence:** Banach fixed point on compact orbit closure K. Contraction constant κ ≤ √(7/9) ≈ 0.882 from ε* = 1/3.

*Structural Hypothesis (SH): mutual orthogonality of perpendicular components — assumed, formal verification deferred to Volume VI.*

---

## Priority Domains

### Saturn's Hexagon (Best Instantiation)
Saturn's north polar hexagon maps cleanly onto the dm³ sequence: the 3D atmosphere compresses to a quasi-2D jet layer (C), Rossby wave curvature drives toward κ* selecting wavenumber n=6 — not 5, not 7 — (K), the Whitney fold locks the six sharp corners (F), and gradient descent on Φ yields the persistent 40+ year fixed point observed from Voyager through Cassini (U).

**Open question:** Are the parameters μ_max, ω, β, κ* derived independently from atmospheric data, or fitted post-hoc?

### Collatz Conjecture (AXLE Target 5)
The Collatz map T(n) = n/2 (even) or 3n+1 (odd) is proposed as a dm³ system with orbit {4→2→1} as unique attractor.

**Structural observation (publishable independently):** Mean step ratio with c=3 gives 3/4 < 1 (mean contraction). With c=5: 5/4 > 1 (divergent). The value c=3 is the minimal odd constant producing mean contraction.

**Status:** Framework proposed. Axioms 7–8 (no divergent orbits, unique attractor) are open — these *are* the conjecture. Formal verification target: Lean 4 (AXLE Target 5).

**Zenodo paper:** *"The Collatz Conjecture as a Canonical dm³-System: A Structural Framework for Decidability"* — does not claim proof; claims structural visibility prior to axiomatization.

---

## TOGT Pedagogical Levels (CEFR Alignment)

| Level | Task | Saturn Example |
|-------|------|----------------|
| A2 | Observe | "The jet bends six times" — label the corners |
| B1 | Explain | "Rossby waves select n=6 by rotation + Coriolis" |
| B2 | Derive | "κ* selects the fold mode via Whitney A₁" |
| C1 | Unify | "Saturn = HPA = market: exact morphisms in dm³-Cat" |

---

## Epistemic Status

This framework is philosophy-of-mathematics / structural mathematics. Claims range from:

- **Empirically supported:** c=3 fingerprint; Saturn Rossby n=6 selection; TDA in markets
- **Conjectured / open:** Structural Hypothesis SH; Collatz Axioms 7–8; ZFC translation
- **Proposed / philosophical:** GUT-level unification; Templar/mythic instantiations; string theory mapping

The honest contribution: *a new structural language for identifying generative invariants across domains, with the Collatz conjecture as the sharpest test case.*

---

## Repository Structure

```
togt-axle/
├── diagrams/           # SVG diagrams for GitHub
│   ├── 01_operator_sequence.svg
│   ├── 02_saturn_hexagon.svg
│   ├── 03_coherence_bridge.svg
│   ├── 04_collatz_dm3.svg
│   └── 05_domain_map.svg
├── docs/               # Papers and formal materials
└── README.md
```

---

## Publications

- **Principia Orthogona, Vol. III** — The Mini-Beast / Nested Infinities (Book 3, G6 LLC)
- **GTCT Audit Draft** — Vol. IV, IMPA format
- **Zenodo:** *Collatz as dm³-System* — DOI pending

---

*"The proof is not a line. It is a crystal."*  
— Principia Orthogona, Chapter 10

---

**Contact:** Pablo / G6 LLC  
**License:** All rights reserved, G6 LLC
