# ZENODO_DESCRIPTION_Vol1_V7.md
# Copy this text into the Zenodo description field for the V7 upload.

---

## Principia Orthogona, Volume I: The Mathematics of Generative Transitions
### Version 7 — August 2026

**Pablo Nogueira Grossi · G6 LLC, Newark NJ · ORCID: 0009-0000-6496-2186**

**V7 (this version):** https://doi.org/10.5281/zenodo.22084842
**Concept DOI** (resolves to latest): https://doi.org/10.5281/zenodo.19117399
**Prior versions:** V6 10.5281/zenodo.21146416 · V5 10.5281/zenodo.21121980 ·
V4 10.5281/zenodo.20784030 · V1 10.5281/zenodo.19117400
AXLE: https://github.com/TOTOGT/AXLE · DM3-lab: https://github.com/TOTOGT/DM3-lab

---

### What V7 corrects

Two things, one about tooling and one about mathematics.

**1. The Lean file had drifted off its own pin.** V3–V6 described
`PrincipiaVol1.lean` as *"30+ facts proved, 1 sorry (clearly scoped), 0 axioms
beyond Mathlib4."* Built in August 2026 against the Mathlib revision the
repository pins — v4.14.0, December 2024 — it produced 81 errors.

That is drift, not neglect, and the error profile says so.
`Ordinal.sup` and `Ordinal.lt_sup` were deprecated on 2024-08-27;
`Ordinal.IsLimit.add_right` was renamed `isLimit_add` on 2024-10-11;
`Set.finite_insert` is the Mathlib-3-era spelling of `Set.Finite.insert`.
Those are the names the file uses — the names that were current when it was
written and run. What happened afterwards is ordinary and, without CI,
invisible: Mathlib moved, the pin was advanced past the code, some later
hand-edits were never rebuilt, and nothing re-ran the build.

V7 brings the file up to the pin, and ships a runner so the next drift is not
silent. The build log is included as `v6-build-errors.txt`, and the V6 file
unchanged as `PrincipiaVol1-V6-as-deposited.lean.txt`.

**2. The separation theorem was false as stated, not unfinished.** V3–V6
carried it with one `sorry` attributed to a missing Mathlib eigenvalue API
(open obligation O1, AXLE issue #12). In fact the deposited statement

```
IsDm3Stable M  :=  ∀ i ≠ 0, |M i i| ≤ exp (−2)
separation_theorem (n < 33) (M) (IsDm3Stable M) : M.trace ≠ 33
```

is refutable: `IsDm3Stable` constrains only the transverse diagonal and says
nothing about `M 0 0`, so at `n = 1` it holds vacuously and the 1×1 matrix
`(33)` has trace 33. The refutation is now proved in Lean and kept in the
file as `v6_separation_statement_is_false`. No Mathlib API would have closed
that gap — a hypothesis was missing, not a lemma.

The underlying result is real and V7 proves it. Book 2 Theorem 12.2 and both
ancestor files in AXLE (`main_v7.lean` Part H, `AXLE_v6.lean` Part H) state
**Tr(M⁶) ≠ 33** — the sixth power. The exponent was dropped in transcription
into this deposit, leaving a hypothesis about `M` and an argument about `M⁶`
with nothing joining them. At the first power the intended bound is
numerically false (`31·e⁻² ≈ 4.195`, not `< 1`); at the sixth it holds with
room to spare (`31·e⁻¹² ≈ 1.9·10⁻⁴`).

Readers who cited the separation theorem from V3–V6 should cite the V7 form
and its hypotheses. Nothing else in the volume is affected.

---

### What this volume does

This volume develops a unified mathematical framework for generative
transitions: localised geometric events in which a trajectory undergoes
compression, curvature intensification, loss of injectivity, and
stabilisation, governed by the operator sequence G = U ∘ F ∘ K ∘ C.

The framework rests on six minimal assumptions and produces: constructive
operator definitions with explicit formulas; five structural theorems
including existence, non-commutativity, and finite branching; seven analytical
invariants; four normal forms; a singularity classification restricted to the
Whitney A₁–A₃ hierarchy; a free-discontinuity variational principle; and a
symplectic Hamiltonian structure with a distributional generator at the fold.

The second edition added a fifth operator E (Generative Time Circuit) with
ż ≥ 0; a term-by-term structural correspondence with Perelman's proof of the
Poincaré conjecture via Ricci flow with surgery (Conjecture 15.1); and the
dimensional threshold N = 3 as the minimum dimension for non-trivial contact
geometry, connecting it to c = 3 in the Collatz map (Conjecture 16.1).

None of that mathematical content is withdrawn by this correction. What
changed is what can be said about the machine verification of it.

---

### What is machine-checked, exactly

`PrincipiaVol1.lean` in this deposit now compiles and every theorem in it is
kernel-checked.

```
toolchain   leanprover/lean4:v4.14.0
Mathlib     v4.14.0   rev 4bbdccd9c5f862bf90ff12f0a9e2c8be032b9a84
theorems    58
sorry       0
axioms      propext, Classical.choice, Quot.sound  — nothing else
verified    24 August 2026
```

Reproduce it with the small companion repository, which exists so that this
one file can be checked without building all of AXLE:

```
git clone https://github.com/TOTOGT/vol1-proofs
cd vol1-proofs
bash tools/run.sh
```

Three stages: `lake build`, then `#print axioms` over all 58 theorems, then a
gate that refuses on `sorryAx` or on any axiom outside the allowlist above.
CI runs the same script on every push.

**Links in this record are pinned to commits, not to branches.** A branch name
moves; a deposit does not. This is the same rule the build applies to its
dependency — `lake-manifest.json` pins Mathlib by revision
`4bbdccd9c5f862bf90ff12f0a9e2c8be032b9a84`, not by the tag `v4.14.0` — and it
applies here for the same reason.

| what | where |
|---|---|
| the record | `PrincipiaVol1.lean`, attached to this deposit |
| the verifier | `github.com/TOTOGT/vol1-proofs` at commit `b308e1a` |
| the mirror | `github.com/TOTOGT/AXLE` at commit `dd361d5`, path `PrincipiaOrthogona1/PrincipiaVol1.lean` |

The file attached here is the authoritative copy. The repositories are
convenience and reproduction; if any of the three ever disagree, the attached
file and the axiom output above are what this deposit asserts.

**What "machine-checked" covers, and what it does not.** Four things V3–V6
said, or implied, that V7 withdraws:

- **Theorems A–D are structures, not theorems.** `CompressionOp`,
  `CurvatureOp`, `FoldOp`, `UnfoldOp` are Lean *structures* — bundles of
  hypotheses — and `GenerativeOp` is a `def`. Declaring them proves nothing
  about them. What is machine-checked is that they are *inhabited*: twelve
  concrete instances over ℤ. V6's abstract already put this correctly; the
  machine-checked list did not.
- **Two of their fields are weaker than their names, and V7 proves it.**
  `UnfoldOp.stable_branch` is satisfied by `n = 0` for every map on every
  type — it constrains nothing (`unfold_stable_branch_is_vacuous`). So
  "Theorem D (stability)" has no content beyond Φ-decrease.
  `CompressionOp.contractive` says `d(fx,fy) ≤ d(x,y)` — *non-expansive*; the
  identity satisfies it (`compression_permits_identity`). Assumption 3 should
  read "non-expansive".
- **One theorem is withdrawn as an unfalsifiable guard.** V3–V6 counted
  `g6_equals_schumann : g6_layer_count_nat = schumann_4th_harmonic_integer := rfl`,
  where both sides are `def … := 33`. It is `33 = 33` and cannot fail. A
  kernel cannot check a claim about the ionosphere.
- **A physical prediction was reported as machine-checked.** The Factor-of-3
  Prediction (τ_grav < τ_dec/3) carried the words *"this is machine-checked
  (Lean: `basin_asymmetry`: 1/3 < 4/5)"*. `basin_asymmetry` is an inequality
  between two rationals. It says nothing about gravitational decoherence. The
  claim is withdrawn; the prediction stands as physical argument.

The 58 theorems are arithmetic and structural: the Whitney conditions at the
fold, the Gronwall radius, the contact sign, the Lyapunov exponent, the
canonical dm³ triple, the separation bound in the form stated below, the
club-filter and regeneration constructions, the crystal aspect ratio, and the
Theorem 5.3 instances. They do **not** cover the analytic content of the book
— the ODE integration, the variational principle, the symplectic argument, the
Perelman correspondence. Those are argued in the paper and tracked as open
obligations. Provenance lines of the form "*from `X.lean` — 0 sorry*" are
withdrawn from the Lean file's section banners: those files have not been built
either, and each claim returns when its file goes green.

### A new open obligation: the ε₀ instantiation (O7)

ε₀ = 1/3 is the headline constant of this volume, and its instantiation as
printed does not close. §22 (Proof VII) states

> ε₀ = |μ_max| / [2(1 + sup‖Hess V‖)] = 2/(2·3) = 1/3, where sup‖Hess V‖ = |L₂| = 3.

Those three cannot all hold. The formula at H = 3 gives 2/(2·4) = **1/4**
(`epsilon0_of_three`). The printed arithmetic `2/(2·3)` corresponds to
1 + H = 3, i.e. H = 2 — which is also what the Lean line `2/(2*(1+2))` uses.
`epsilon0_of_eq_third_iff` proves the choice is forced: for H ≥ 0, this
formula yields 1/3 for exactly one Hessian bound, H = 2.

So either the formula is right and sup‖Hess V‖ = 2, or the bound is 3 and the
formula should read |μ_max|/(2H) without the 1+. V7 does not choose. It
records that a choice is owed, and proves that one is.

---

### The separation theorem in V7

| theorem | content |
|---|---|
| `exp_neg_two_le` | `e⁻² ≤ 1/4`, from `1 + 1 ≤ e` alone — no interval arithmetic |
| `exp_neg_twelve_le` | `e⁻¹² ≤ (1/4)⁶` — the constant V6 asserted and could not prove |
| `transverse_sum_bound` | `\|Σ_{i≠0} λᵢ⁶\| ≤ 31·(1/4)⁶` — the step V6 admitted with `sorry` |
| `spectral_trace_ne_33` | `λ₀ = 1`, `\|λᵢ\| ≤ e⁻²` for `i ≠ 0`, `n < 33` ⟹ `Σ λᵢ⁶ ≠ 33` |
| `separation_theorem` | the same for a diagonal matrix: `Tr(M⁶) ≠ 33` |
| `separation_trace_first` | first-power form, carrying the normalisation `\|M₀₀\| ≤ 1` that V6 omitted |
| `spectral_trace_ne_33_upto` | the same conclusion to n = 131072 — the dimension bound is sufficient, not necessary |
| `separation_fails_in_high_dimension` | at ~1.7·10⁷ directions the trace does exceed 33 — so it cannot be dropped either |
| `coherent_directions_realise_33` | 33 *coherent* directions realise 33 — a statement about the coherent count, not about n |
| `v6_statement_false_at_dimension_five` | `diag(33,0,0,0,0)` satisfies V6's hypothesis and has trace 33 — not a dimension-1 technicality |
| `dm3_hypothesis_nonvacuous` | a witness satisfying the hypotheses, so the statement is not vacuously true |
| `v6_separation_statement_is_false` | the refutation of the V3–V6 statement, kept on the record |

The margin is wide: under the hypotheses the sixth-power trace lies within
31/4096 of 1, and misses 33 by more than 31.

**One correction inside this correction.** A draft of V7 claimed `n < 33` was
sharp, citing `Σ_{i<33} 1⁶ = 33`. That witness has every λᵢ = 1 and violates
the transverse hypothesis, so it witnesses nothing about n. The hypothesis is
*sufficient and far from necessary* — the same bound carries to n = 131072 —
and it cannot be dropped altogether, since around 1.7·10⁷ contracted
directions do push the trace past 33. 33 is inherited from the dm³ threshold,
not forced by this estimate. What 33 *is* the threshold for is the number of
directions that are **not** contracted.

---

### Open obligations (5)

| ID | Description | Status in V7 |
|----|-------------|--------------|
| O1 | **Restated.** Spectral reduction `Tr(M⁶) = Σ λᵢ⁶` for a general real `M` (diagonalisability over ℝ, or Jordan form over ℂ). | Open — and *not* the obligation V3–V6 recorded. V7 proves the theorem on the eigenvalue list and on a diagonal matrix, where the reduction has already been performed. This is a boundary of the statement, not a hole in a proof; no `sorry` is taken on its account. |
| O2 | AXLE #14: Mather C∞-stability step; Poincaré–Bendixson | Open, and **weaker than V3–V6 recorded**. `AutophagyDm3_v2.lean` builds and is kernel-checked with zero `sorry` for these obligations — but three of the declarations they rest on are `∃ φ : ℝ → ℝ, True`, `True`, and `True`, each proved by `trivial`. They carry no `sorry` because they assert nothing. A kernel check certifies the proof, not the interest of the statement. See `OPEN_QUESTIONS.md`. |
| O3 | AXLE #15 / T1: full ODE Gronwall integration | Partial — the exponent sign is machine-checked; the integration is not |
| O4 | Discrete dm³ extension to ℤ | Open |
| O5 | Conjecture 15.1: Perelman functor 𝒫 | Open — stated as a conjecture |

---

### Files in this deposit

| File | What it is |
|---|---|
| `principia_vol1_v7.pdf` | the paper, V7 (47 pp) — carries the correction notice |
| `principia_vol1_v7.tex` | LaTeX source |
| `PrincipiaVol1.lean` | the Lean, V7 — compiles, 58 theorems, 0 sorry |
| `v6-build-errors.txt` | the verbatim 81-error build log of the V6 file |
| `PrincipiaVol1-V6-as-deposited.lean.txt` | the V6 file, unchanged, for diffing |
| `figures.py` | figure generator (numpy, matplotlib) |
| `fig1`–`fig7` `.pdf` | the seven figures |
| `CHANGES_Vol1.md` | V1 → V7 version history |
| `OPEN_QUESTIONS.md` | open questions with status |

---

### Version history

| Version | Date | Key change |
|---------|------|-----------|
| V1 | March 17, 2026 | Original four-operator framework |
| V2 | May 16, 2026 | Fifth operator E; Perelman correspondence; Collatz threshold |
| V3 | May 2026 | Reproducibility stack: Lean file, figures.py, figure PDFs, changelogs |
| V6 | — | (see repository history) |
| V4 | June 21, 2026 | Seven-proof template on all five theorems | 20784030 |
| V5 | July 2026 | Hand-verified correction pass on §18–22 | 21121980 |
| V6 | July 2026 | Existence, finite branching, two new assumptions, Invariant 7.5 | 21146416 |
| **V7** | **August 24, 2026** · 10.5281/zenodo.22084842 | **Lean file brought up to the pinned Mathlib (81 drift errors → 0), 58 theorems, 0 sorry; separation theorem restated and proved; O1 re-diagnosed; O7 opened on the ε₀ instantiation; verifier repository published** |

---

### Build instructions

**Lean 4** — reproduce the verification exactly:

```
git clone https://github.com/TOTOGT/vol1-proofs
cd vol1-proofs
bash tools/run.sh
```

Pinned to Lean v4.14.0 and Mathlib v4.14.0 (rev 4bbdccd9c5f8). The pin is part
of the claim: "compiles under current Mathlib" is not a checkable statement,
and a floating dependency is how the V3–V6 error went unnoticed.

**Figures:**

```
pip install numpy matplotlib
python figures.py
```

**Paper:**

```
pdflatex principia_vol1_v7.tex   # three times, for TOC and cross-references
```

Builds clean from the V6 source with the deposit's own three figures.

---

### Series context

| Role | DOI |
|------|-----|
| Series root / concept DOI | 10.5281/zenodo.19117399 |
| Volume I — concept DOI | 10.5281/zenodo.19117400 |
| Volume I — V7 (this version) | 10.5281/zenodo.22084842 |
| Volume II (contact geometry) | 10.5281/zenodo.19379473 |
| GCM paper (dm³ toy model) | 10.5281/zenodo.19379385 |
| G6 Crystal (lunar architecture) | 10.5281/zenodo.19162013 |
| Multi-Orbit Identity Theory | 10.5281/zenodo.20230614 |
| Autophagy / Triple-Alpha (Book 3, Ch. A) | 10.5281/zenodo.20168812 |
| Fibonacci / Tribonacci DNLS | 10.5281/zenodo.20026942 |
| AXLE formal verification hub | github.com/TOTOGT/AXLE |
| Volume I verifier | github.com/TOTOGT/vol1-proofs |

**MSC codes:** 37C25, 37G10, 53D10, 57M27, 58K05, 70H05, 47H10

**Keywords:** generative transitions · contact geometry · operator sequence ·
Whitney fold · singularity theory · variational mechanics · symplectic geometry ·
Ricci flow · Perelman conjecture · Lean 4 formal verification · dimensional
threshold · dm³ framework · Gronwall stability · Principia Orthogona · G6 LLC

**License:** CC BY-NC-ND 4.0 (paper) · MIT (code)
**Copyright:** © 2026 Pablo Nogueira Grossi, G6 LLC
**Contact:** g6llc@proton.me
