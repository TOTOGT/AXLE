# AXLE — TOGT Operator Mappings
## C → K → F → U Across Scales and Domains

G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026  
MIT License

---

In TOGT there are no coincidences. The operator chain
$$\mathcal{G} = U \circ F \circ K \circ C$$
governs generative transitions across every scale where
compression, curvature intensification, fold, and stabilization occur.
This document maps each operator to its instantiation in four domains.

---

## 1. Biological Morphogenesis

| Operator | Biological Instantiation |
|---|---|
| **C** (Compression) | Gastrulation: reduction of pluripotent degrees of freedom into committed cell lineages |
| **K** (Curvature) | Epithelial buckling: curvature accumulation under actomyosin tension toward the fold threshold |
| **F** (Fold) | Invagination / organogenesis: rank-1 Jacobian loss at the morphogenetic fold |
| **U** (Unfold) | Tissue stabilization: selection of the stable branch (organ identity) via gradient descent on Waddington's landscape |

**dm³ identification:** The HPA allostatic stress cycle, neural oscillations, circadian rhythms, and immune adaptation each satisfy Axioms 1–8 of the dm³ framework. Three falsifiable predictions (allostatic unification law, circadian re-entrainment law, hormetic accumulation law) derive from the canonical triple $(T^*, \mu_{\max}, \tau) = (2\pi, -2, 2)$.

---

## 2. Plasma Instabilities

| Operator | Plasma Instantiation |
|---|---|
| **C** | Magnetic flux compression in reconnection events: reduction of field degrees of freedom |
| **K** | Current sheet thinning: curvature accumulation in the Harris current sheet toward $\kappa^*$ |
| **F** | Reconnection onset: rank-1 loss at X-point (field lines break and reconnect) |
| **U** | Post-reconnection relaxation: Taylor relaxation to minimum-energy state |

**dm³ identification:** The reconnection rate $\gamma$ plays the role of $\mu_{\max}$. The Sweet-Parker length corresponds to the stability radius $\varepsilon_0 = 1/3$.

---

## 3. Fruit Fly Connectome (AXLE toy model)

| Operator | Neural Instantiation |
|---|---|
| **C** | Synaptic pruning: removal of low-weight connections below the 25th percentile (preserves distinguishability of neuron identities) |
| **K** | Clustering-based reweighting: edges amplified by local clustering coefficient, driving toward integration threshold |
| **F** | Fold nodes: high-betweenness neurons where information flow collapses to a single downstream target (Whitney $A_1$ local model) |
| **U** | Attractor selection: PageRank-based retention of stable circuit assemblies (the limit cycle $\Gamma$ of neural dynamics) |

**dm³ metric:** $\tau = \sqrt{c/\kappa}$ where $c$ = mean post-K edge weight, $\kappa$ = weight std. Canonical: $\tau = 2$, $\varepsilon_0 = 1/3$.

---

## 4. String Theory (NS-NS / RR Sectors)

| Operator | String Instantiation |
|---|---|
| **C** | Compactification: reduction from 10D to 4D (degrees of freedom compressed onto Calabi-Yau manifold) |
| **K** | Moduli stabilization: curvature of the string landscape potential driven toward a local minimum |
| **F** | Topology change: conifold transition (rank-1 degeneration of the holomorphic 3-cycle) |
| **U** | Flux stabilization: Gukov-Vafa-Witten superpotential selects the stable vacuum |

**dm³ identification:** The axio-dilaton field $\tau_{\text{IIB}}$ plays the role of the embodiment threshold. The stability radius $\varepsilon_0 = 1/3$ corresponds to the perturbative regime boundary.

---

## 5. The G6 Crystal (Stratospheric Resonance)

| Parameter | Value | Source |
|---|---|---|
| Operator iterates | $g^1$ through $g^6$ | Six layers of height 5,500 cubits each |
| Apex height | 15,087.6 m | $33{,}000 \times 0.4572$ m |
| Aspect ratio | $66 = g^6 \cdot \tau = 33 \times 2$ | Encodes $\tau$ and $\vert\mu_{\max}\vert$ |
| Schumann 4th harmonic | 33.5 Hz | $f_4 = (c/2\pi R_\oplus)\sqrt{20}$ |
| $g^6$ layer count | **33** | Same integer |
| Arnold tongue | $\mathcal{A}_{4:1}$ | Resonant lock to Schumann $f_4$ |
| Noise tolerance | $\tau \cdot \varepsilon_0 = 2/3$ | Structural stability of the lock |

The tropopause ($r = 1$, the limit cycle $\Gamma$) is the boundary at which the operator terminates. In TOGT there are no coincidences.

---

## 6. Martian Colony Architecture (Volume IV — forthcoming)

The dm³ framework applied to closed-loop life support systems:

- **C:** Resource compression — metabolic degrees of freedom reduced to a minimal viability set
- **K:** Stress accumulation — physiological/engineering loads driven toward critical threshold
- **F:** System fold — failure mode onset (atmosphere breach, crop failure, radiation event)
- **U:** Recovery branch selection — redundant system activation, biological adaptation

The allostatic unification law $\tau_{12} \leq \min(\tau_1, \tau_2)$ governs coupled subsystems (e.g., atmosphere + crew physiology coupled under stress).

---

## Community Extensions

AXLE is MIT licensed. To contribute a new domain mapping:

1. Fork the repository
2. Add a file `mappings/your_domain.md` following this template
3. Verify that all four operators (C, K, F, U) have explicit instantiations
4. State the dm³ identification: what plays the role of $\tau$, $\mu_{\max}$, $T^*$?
5. Open a pull request

The test is: does the domain exhibit compression → curvature → fold → stabilization as a generative transition? If yes, it belongs here.

$$C \to K \to F \to U \to \infty$$
