# dm³ Lean files — rewrite pass, 2026-07-03

Rewrite of the five uploaded `.lean` files to fix the three failure modes the
audit identified (vacuous tautologies, wrong theorem, invented/mismatched
justifications). Each file now states the *correct* claim and follows one
discipline: prove what is checkable, and mark what is not with a **clearly
labelled `sorry`** and a real proof route — never a fabricated justification.

## Two limits you should know before trusting these

1. **Not machine-checked.** None of these were compiled against Mathlib in this
   session. Lemma/API names (e.g. `ContractingWith.fixedPoint`, `Real.cos_add`,
   `AnalyticOn` vs the renamed `AnalyticOnNhds`) are best-effort and must be
   confirmed by `lake build`.
2. **Rebuilt from the audit, not the hand-proofs.** Where the audit gave the
   actual corrected object (the Bernoulli flow, the centered Gaussian, the
   linearization slip, the Gerono counterexample) the file is rebuilt around the
   real math. Where the deep content lives in a proof not in front of me
   (Invariant 7.5's curvature bound, the full contact normal-form reduction) I
   used an honest `sorry` rather than invent content — because inventing content
   is exactly what the audit caught the originals doing.

## What changed, file by file

**Dm3Arithmetic.lean** — Fix 1: `flow` is now the Bernoulli solution
`r(t)=[1+(r₀⁻²−1)e^(−2t)]^(−1/2)` of `ṙ = r − r³` (fixed point r=1), not a plain
exponential decay. Fix 3: `ρ(x) ∝ exp(−4(x−1)²/σ²)` centered at **r=1** with
coefficient **4** (from drift −4(r−1)), not an `N(0,σ²)` centered at 0. Fix 2:
value `2·exp(z₀)` recorded, with the justification moved to ContactHopf.lean.
Proved: initial-condition algebra target, `flowAux_ode`, equilibrium, all
`μ_hopf` facts, `ρ_peak_at_one`, `ρ_nonneg`. Sorry: `flow_ode` (ṙ=r−r³
derivative), `ρ_normalised`, the Fokker–Planck stationarity (open, no Mathlib SDE).

**ContactHopf.lean** — Deleted the invented "Reeb-direction projection gives a
factor of 2" mechanism. Replaced with the actual linearization algebra
(`−2(1−y·e^(−z₀)) = 2y·e^(−z₀)−2` as a proved `ring` identity) as the honest
locus of the factor of 2. **Reconciliation now RESOLVED** (see
CONTACTHOPF_RECONCILIATION.md): the coefficient on γ in the eigenvalue equation
falls 2→1, and because that coefficient sits in the denominator when solving for
the root, γ* rises `e^(z₀) → 2·e^(z₀)` — both descriptions are the same fix at
two stages, no contradiction. Encoded by two proved root lemmas
(`erroneous_root_is_exp`, `gammaStar_is_root`). Normal-form bifurcation theorem
kept as an honest sorry.

**ExistenceWellPosedness.lean** — Removed the vacuous `∃!y, y=f x` tautologies.
Well-posedness is now "Φ has a unique attracting fixed point." Proved: the
toy-model compression contracts distances by exactly `r*` (`compression_contracts`,
`compression_strict`), and the composite `Φ=R∘K∘F∘C` contracts by `r*` when
F,K,R are non-expansive (`Phi_contracts`). The Banach conclusion
(`Phi_wellPosed`, convergence) is routed to `ContractingWith` via sorry. F/K/R
well-definedness are now substantive named hypotheses (non-expansive, ODE
unique, Morse arg-min), not tautologies.

**Invariant75.lean** — Stopped relabelling a generic Lyapunov contraction as
§7.5. States the real theorem: under a chord-arc/curvature **condition (D)** the
generative curve is injective (`invariant_7_5_injective`, proved from the bound
inside (D)). Necessity of (D) is proved via the **Gerono lemniscate**
`(cos t, sin t·cos t)`, which self-intersects at the origin
(`γ(π/2)=γ(3π/2)=(0,0)`) hence is not injective on `[0,2π]`
(`gerono_not_injOn`, `gerono_fails_conditionD` — both proved). The concrete
"curvature ⇒ chord-arc constant" step is the one external obligation.

**FiniteBranching.lean** — Kept unchanged (only a header note added). The audit
found it already correct in form; it is the reference pattern the other four
were rewritten to match.

## Recommendation echoing the audit

Do not commit any of these as a "proof" until `lake build` passes. The value of
this pass is that the files now state the *right* claims and lie about nothing:
what is proved is proved, what is open is labelled open. That is strictly safer
than the originals, two of which would have put incorrect mathematical content
into the formal record.
