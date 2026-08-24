# ZENODO_DESCRIPTION_Vol1_V7.md
# Copy this text into the Zenodo description field for the V7 upload.
# Replace {V7_DOI} once Zenodo mints it.

---

## Principia Orthogona, Volume I: The Mathematics of Generative Transitions
### Version 7 — August 2026

**Pablo Nogueira Grossi · G6 LLC, Newark NJ · ORCID: 0009-0000-6496-2186**

Concept DOI (resolves to latest): https://doi.org/10.5281/zenodo.19117399
This deposit: https://doi.org/10.5281/zenodo.19117400
V7 DOI: {V7_DOI}
AXLE: https://github.com/TOTOGT/AXLE · DM3-lab: https://github.com/TOTOGT/DM3-lab

---

### ⚠ Correction notice — read before citing V3–V6

V7 corrects the record on the Lean file shipped with this deposit. Two things
were wrong, and neither was small.

**1. The file did not compile.** V3 through V6 described `PrincipiaVol1.lean`
as *"30+ facts proved, 1 sorry (clearly scoped), 0 axioms beyond Mathlib4."*
That description was never checkable, because the file had never been
elaborated by Lean. The first real build — 24 August 2026, under the
toolchain the deposit itself names — reported **81 errors**. The faults were
mechanical (structure fields separated by `;`, so `Dm3Triple` had exactly one
field and every use of `canonicalTriple.mu_max` was an unknown field; a
`MetricSpace` passed where a `Dist` was expected; `(0 : Fin n)` with no
`[NeZero n]`; four Ordinal lemmas that do not exist under those names; a
carrier type that never unfolded to `ℤ`) — but the consequence was not:
**nothing the earlier versions claimed about that file had been verified by
anything.** The verbatim build log is included in this deposit as
`v6-build-errors.txt`.

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
and its hypotheses.

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
theorems    49
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

Three stages: `lake build`, then `#print axioms` over all 49 theorems, then a
gate that refuses on `sorryAx` or on any axiom outside the allowlist above.
The same file lives in AXLE at
`PrincipiaOrthogona1/PrincipiaVol1.lean`
(https://github.com/TOTOGT/AXLE/blob/main/PrincipiaOrthogona1/PrincipiaVol1.lean).

**What "machine-checked" covers, and what it does not.** The 49 theorems are
arithmetic and structural facts: the Whitney conditions at the fold, the
Gronwall radius, the contact sign, the Lyapunov exponents, the canonical dm³
triple, the separation bound in the form stated below, the club-filter and
regeneration constructions, the crystal aspect ratio, and nine concrete
instances witnessing Theorem 5.3. They do **not** cover the analytic content
of the book — the ODE integration, the variational principle, the Perelman
correspondence. Those are argued in the paper and tracked as open obligations,
not formalised. Provenance lines of the form "*from `X.lean` — 0 sorry*" have
been removed from the Lean file's section banners: those files have not been
built either, and the claim will be restored per file as each goes green.

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
| `separation_sharp_at_33` | at `n = 33` the sixth-power trace equals 33 — the dimension bound is load-bearing, not an unfalsifiable guard |
| `dm3_hypothesis_nonvacuous` | a witness satisfying the hypotheses, so the statement is not vacuously true |
| `v6_separation_statement_is_false` | the refutation of the V3–V6 statement, kept on the record |

The margin is wide: under the hypotheses the sixth-power trace lies in
`[1 − 31/4096, 1 + 31/4096]`. It misses 33 by more than 31. That gap *is* the
dimensional threshold — 33 units of trace require 33 coherent directions, and
below 33 dimensions there are not 33 directions to be had.

---

### Open obligations (5)

| ID | Description | Status in V7 |
|----|-------------|--------------|
| O1 | **Restated.** Spectral reduction `Tr(M⁶) = Σ λᵢ⁶` for a general real `M` (diagonalisability over ℝ, or Jordan form over ℂ). | Open — and *not* the obligation V3–V6 recorded. V7 proves the theorem on the eigenvalue list and on a diagonal matrix, where the reduction has already been performed. This is a boundary of the statement, not a hole in a proof; no `sorry` is taken on its account. |
| O2 | AXLE #14: Mather C∞-stability step; Poincaré–Bendixson | Open — argued in the paper, not formalised |
| O3 | AXLE #15 / T1: full ODE Gronwall integration | Partial — the exponent sign is machine-checked; the integration is not |
| O4 | Discrete dm³ extension to ℤ | Open |
| O5 | Conjecture 15.1: Perelman functor 𝒫 | Open — stated as a conjecture |

---

### Files in this deposit

| File | What it is |
|---|---|
| `PrincipiaVol1.lean` | the Lean, V7 — compiles, 49 theorems, 0 sorry |
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
| **V7** | **August 24, 2026** | **Lean file made to compile (81 errors → 0); separation theorem found false as stated, restated and proved; O1 re-diagnosed; provenance claims that had never been built withdrawn; verifier repository published** |

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
pdflatex principia_vol1_v2_full.tex   # twice, for cross-references
```

---

### Series context

| Role | DOI |
|------|-----|
| Series root / concept DOI | 10.5281/zenodo.19117399 |
| Volume I (this deposit) | 10.5281/zenodo.19117400 |
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
