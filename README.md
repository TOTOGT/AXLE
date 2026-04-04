# AXLE – Topographical Orthogenetics Proofs & Extensions
AXLE toy machine fruit fly 🪰

Formal verification hub and extensible repository for **Topographical Orthogenetics (TO)** and **Topographical Orthogonal Generative Theory (TOGT)**.

## Core Focus
- Lean-verified proofs for scaling hierarchies (g⁵/g⁶ → hyper-Mahlo regenerations)
- Operator chain implementations & mappings: **C → K → F → U** across scales
- Nth-degree reconfiguration algorithms & community extensions
- Bridges: plasma instabilities → biological morphogenesis → dm³ systems → Martian colony architecture → toy brain models (fly 🪰 connectome as starting point)

## Current Status
Bootstrapping: MIT licensed, foundations incoming from Principia Orthogona Vol. IV and related threads.

## Planned Structure
- `/lean/`              → Lean 4 proofs (.lean files) for large cardinal hierarchies & regeneration loops
- `/mappings/`          → Docs/notebooks on string-to-bio/plasma mappings
- `/simulations/`       → Python toy models (fly brain connectome + TO operators → dm³ metrics)
- `/scripts/`           → Canonical empirical pipeline scripts (C9.2 Collatz golden runs)
- `/docs/`              → Excerpts, references, book ties

## C9.2 Pipeline (Collatz Empirical Certificates)

The `/scripts/` directory contains the canonical C9.2 pipeline for producing
empirical certificates of the Collatz dm³ structural framework.

| Script | Purpose |
|--------|---------|
| `c92_sampler.py` | Graded drift observable per odd residue, dyadic window \[N, 2N\]. Outputs CSV + `summary.json`. |
| `c92_fourier.py` | DFT of the mean-centered residue-drift vector + mean-centered sparsity metrics. Outputs `fourier.json`. |
| `c92_pipeline.py` | End-to-end runner (test and golden-run modes). |

**Quick start (test run, N=10,000, M=8):**
```bash
cd scripts/
python c92_pipeline.py --test
```

**Golden runs (N=100,000, M=12/14/16) — produce archival certificates:**
```bash
python c92_pipeline.py --golden
```

Artifacts per run written to `outputs/`:
- `c92_sample_N{N}_M{M}.csv`
- `c92_summary_N{N}_M{M}.json`
- `c92_fourier_N{N}_M{M}.json`

## Related Work
- Book: *Applications of Generative Orthogonal Matrix Compression Science* (Vol. IV, Principia Orthogona)
- Zenodo: [add DOI/link after first version]
- X: @unitedWeStreamU (search "AXLE" for threads, e.g., March 2026 foundations)

## Contributing
Want to add files to the community — including from your phone? See [CONTRIBUTING.md](CONTRIBUTING.md) for a step-by-step guide to uploading files via the GitHub mobile app.

Contact: Pablo Grossi | PabloGrossi@hotmail.com | G6 LLC · Newark, NJ · 2026