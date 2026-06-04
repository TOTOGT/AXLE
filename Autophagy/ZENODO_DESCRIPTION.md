# Autophagy Chapter — Zenodo Record 20168812 — Deposit Description

## Paste this into the Zenodo description field

---

This deposit contains the complete Chapter A of *Principia Orthogona, Book 3: The Mini-Beast* — "Self-Regulation: Autophagy and the Triple-Alpha Process as dm³ Generative Transitions" — with LaTeX source, Lean 4 formal verification, Python simulation code, and four figures.

The chapter argues that autophagy (cellular self-digestion, Nobel Prize 2016, Ohsumi) and the triple-alpha stellar nucleosynthesis process share the same underlying contact geometry. Both are modelled as instances of the operator pipeline G = U ∘ F ∘ K ∘ C on a contact 3-manifold with contact form α = dz − ρ² dθ.

**Proved without sorry (26 theorems in AutophagyDm3_v2.lean):** contact form non-degeneracy (c(ρ) = −2ρ < 0); all four Whitney A₁ conditions on V(q) = q³ − 3q; double-root factorisation V(q)+2 = (q−1)²(q+2) forcing μ_max = −2; Gronwall stability radius ε₀ = 1/3; basin asymmetry ε₀ < r* ≈ 4/5; stability functional Φ(ρ) = ρ².

**AXLE Issue #14 resolution:** Obligation 1 (contact non-degeneracy) closed — `contactForm_nondeg_scalar` proved. Obligation 2 strengthened — `whitneyFold_conditional` replaces True stub; sorry guards only Mather's theorem. Obligation 3 split — compactness proved (`dm3_basin_compact`, `dm3_basin_nonempty`); Poincaré–Bendixson step remains sorry pending Mathlib.

Two new rows added to the Coherence Bridge parameter table: autophagy (μ_max ≈ −0.41 s⁻¹, β = 1.85) and triple-alpha (μ_max ≈ −0.88 normalised, β = 2.3).

**Files:** autophagy_dm3.pdf (8-page paper), tex/autophagy_dm3.tex (LaTeX source), lean/AutophagyDm3_v2.lean (Lean 4 proofs, 26 theorems), code/autophagy_dm3.py (Python simulation + figures), figures/fig_A1–A4.pdf, figures/coherence_bridge.csv.

**AXLE repository:** https://github.com/TOTOGT/AXLE

---

## Suggested Zenodo metadata

- **Resource type:** Publication / Preprint
- **Keywords:** autophagy; triple-alpha; dm³; contact geometry; Whitney fold; generative operator pipeline; TO/TOGT; Lean 4; mTORC1; stellar nucleosynthesis; Principia Orthogona
- **Programming language:** Python, Lean 4
- **License:** MIT (code, Lean 4); CC BY 4.0 (paper, figures)
- **Related identifiers:**
  - `isPartOf` → 10.5281/zenodo.19117400 (Principia Orthogona series root)
  - `isRelatedTo` → 10.5281/zenodo.20026942 (DNLS companion paper)
  - `isRelatedTo` → 10.5281/zenodo.19210136 (fruit-fly / MultiOrbitBioSwarm paper)
  - `isPartOf` → https://github.com/TOTOGT/AXLE (AXLE repository)
