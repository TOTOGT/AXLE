/-
  TribonacciRatioConvergence.lean

  Formalization target for the Tribonacci jet-ratio claim (F.1, dm³/TOGT paper):
      ⟨n_k⟩ / ⟨n_{k+1}⟩ → η ≈ 1.8393...   (η = real root of X³ - X² - X - 1)

  This file is a SPEC, not a finished proof: every `sorry` marks either (a) routine
  algebra/tactic work that should close directly, or (b) one piece of genuinely new
  mathematical content not reducible to existing Mathlib lemmas, or (c) a hypothesis
  that depends on the paper's actual initial data (w(0), w(1), w(2)) and can't be
  discharged in the abstract.

  Every Mathlib identifier below has been checked against live mathlib4 docs during
  this session (not recalled from training data). Where a name is used but was NOT
  independently re-verified in this exact file, it is flagged inline with "UNVERIFIED".

  Dependency order: read top to bottom. Later sections depend on earlier ones.
-/

import Mathlib.Algebra.LinearRecurrence
import Mathlib.Algebra.QuadraticDiscriminant
import Mathlib.Algebra.Polynomial.Degree.Definitions
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Matrix.Notation
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Complex.Abs
import Mathlib.Data.Complex.Module

-- NOTE (build fix, this session): `Mathlib.LinearAlgebra.Matrix.Irreducible.Defs` and
-- `Mathlib.Analysis.SpecificLimits.Fibonacci` were removed from the import list above.
-- Confirmed by direct `find` against the actual checked-out mathlib commit (the real
-- pinned `v4.14.0` tag, not the stray newer master snapshot that caused the earlier
-- toolchain mismatch): NEITHER file exists at this pin. `Mathlib.Data.Matrix.Mul` and
-- `Mathlib.Data.Fin.VecNotation` are added explicitly in their place since `TriboM`
-- below needs `Matrix` and `.mulVec` regardless — both of those modules are confirmed
-- present (they built successfully in the last full run). NOTE: the 2-D `!![a, b; c, d]`
-- matrix-literal notation is NOT provided by `Fin.VecNotation` (that only gives the
-- 1-D `![...]` vector notation) — it lives in `Mathlib.Data.Matrix.Notation`, added
-- explicitly below after a genuine parse failure (`unexpected token ';'`) confirmed
-- this was the missing piece. `Mathlib.Data.Complex.Module` is added for the
-- `Algebra ℝ ℂ` instance (`instAlgebraOfReal`, line 95 of that file) needed by
-- `algebraMap ℝ ℂ` in Section 7.

open Polynomial Matrix

/-! ## 0. Setup: the recurrence, its characteristic polynomial, and the substitution matrix -/

-- w(n+3) = w(n+2) + w(n+1) + w(n)
noncomputable def tribRec : LinearRecurrence ℝ where
  order := 3
  coeffs := ![1, 1, 1]

-- Complex-valued companion recurrence, defined DIRECTLY (same integer coefficients,
-- just living in ℂ) rather than via a `tribRec.map (algebraMap ℝ ℂ)`-style construction:
-- `LinearRecurrence.map` does not exist anywhere in Mathlib (confirmed by grep against
-- the actual pinned commit), so this sidesteps that gap entirely instead of assuming it.
noncomputable def tribRecC : LinearRecurrence ℂ where
  order := 3
  coeffs := ![1, 1, 1]

noncomputable def tribCharPoly : Polynomial ℝ := X ^ 3 - X ^ 2 - X - 1

-- sanity link to the LinearRecurrence API (`charPoly`, `charPoly_monic`,
-- `charPoly_degree_eq_order` are confirmed-existing names in `Mathlib.Algebra.LinearRecurrence`)
theorem tribRec_charPoly_eq : tribRec.charPoly = tribCharPoly := by
  sorry -- unfolds `LinearRecurrence.charPoly` against `tribRec.coeffs`; routine

-- Tribonacci substitution matrix (1→12, 2→13, 3→1) — independent framing via
-- Perron–Frobenius / primitive matrices; same characteristic polynomial as tribRec.
noncomputable def TriboM : Matrix (Fin 3) (Fin 3) ℝ :=
  !![1, 1, 1;
     1, 0, 0;
     0, 1, 0]

/-! ## 1. η: the real root, and its defining algebraic relation -/

noncomputable def η : ℝ := sorry -- IVT witness: tribCharPoly.eval 1 = -2 < 0 < 1 = tribCharPoly.eval 2

theorem eta_mem_Ioo : 1 < η ∧ η < 2 := by
  sorry -- IVT + strict monotonicity of tribCharPoly on (1, ∞)
        -- (derivative 3X²-2X-1 = (3X+1)(X-1) > 0 for X > 1)

theorem eta_cubic : η ^ 3 = η ^ 2 + η + 1 := by
  sorry -- from tribCharPoly.eval η = 0, i.e. η³-η²-η-1 = 0; `linarith` after unfolding

theorem eta_pos : 0 < η := (eta_mem_Ioo).1.trans_le' (by norm_num) |>.le.lt_of_ne (by
  sorry) -- or just: `lt_trans one_pos eta_mem_Ioo.1` style; η > 1 > 0

theorem eta_ne_zero : η ≠ 0 := by
  intro h
  have h3 := eta_cubic
  rw [h] at h3
  norm_num at h3
  -- h : η = 0, substituted into eta_cubic gives 0^3 = 0^2+0+1, i.e. 0 = 1, false

/-! ## 2. Root separation: the other two roots are a non-real conjugate pair, modulus 1/√η

   Route: factor out (X - η), get a REAL quadratic quotient, and use Mathlib's
   EXISTING (confirmed) quadratic discriminant machinery — no cubic-discriminant
   theory needed. This replaced an earlier, wrong attempt to invent a
   `Polynomial.discrim` for cubics, which does not exist in Mathlib.
-/

theorem eta_inv_eq : (1 : ℝ) / η = η ^ 2 - η - 1 := by
  rw [div_eq_iff eta_ne_zero]
  linear_combination -eta_cubic
  -- goal: 1 = (η²-η-1)*η, i.e. 1-η³+η²+η = 0 = -(eta_cubic rearranged); needs coefficient -1

-- CONFIRMED against docs: `tribCharPoly_factor` needs no new discriminant theory,
-- just this polynomial identity, which holds BECAUSE η satisfies eta_cubic
-- (it is not a free-variable ring identity — `ring` alone cannot close it).
theorem tribCharPoly_factor :
    tribCharPoly = (X - C η) * (X ^ 2 + C (η - 1) * X + C (1 / η)) := by
  sorry
  -- BUILD-FIX NOTE (this session): the original attempt (`simp only [...]; ring_nf;
  -- linarith [eta_cubic]`) doesn't typecheck as written — `linarith` operates on ordered
  -- fields, not on `Polynomial ℝ` values, and this goal lives in `Polynomial ℝ` even
  -- after expanding both sides. The genuine proof needs a coefficient-by-coefficient
  -- comparison (e.g. `Polynomial.ext` + `Polynomial.coeff_X_pow` / `coeff_C` lemmas)
  -- reducing to the SAME scalar identity `eta_cubic` supplies, but that reduction is
  -- itself real work, not a one-line tactic swap — left as `sorry` per this file's own
  -- stated convention (header: sorries mark either routine gaps or genuinely new content).

-- CONFIRMED against docs: `discrim` (Mathlib.Algebra.QuadraticDiscriminant, quadratics only)
-- and `discrim_eq_sq_of_quadratic_eq_zero` both exist with the expected signatures.
theorem trib_quotient_discrim_eq :
    discrim 1 (η - 1) (1 / η) = (η - 1) ^ 2 - 4 / η := by
  unfold discrim
  ring

theorem trib_quotient_discrim_neg : discrim 1 (η - 1) (1 / η) < 0 := by
  rw [trib_quotient_discrim_eq, sub_neg, lt_div_iff₀ eta_pos]
  -- reduces to (η-1)²*η < 4; substitute η³=η²+η+1 ⟹ reduces to (η-1)²+2 > 0, unconditional
  nlinarith [sq_nonneg (η - 1), eta_cubic]

-- CONFIRMED: `discrim_eq_sq_of_quadratic_eq_zero` + `sq_nonneg` + `linarith` closes this
-- directly — no need for `quadratic_ne_zero_of_discrim_ne_sq` as a separate black box.
theorem trib_quotient_no_real_root :
    ¬ ∃ x : ℝ, x ^ 2 + (η - 1) * x + 1 / η = 0 := by
  rintro ⟨x, hx⟩
  -- BUILD-FIX NOTE: `discrim_eq_sq_of_quadratic_eq_zero` (Mathlib.Algebra.QuadraticDiscriminant,
  -- checked directly against source) actually has signature
  -- `(h : a * (x * x) + b * x + c = 0) : discrim a b c = (2*a*x+b)^2` — it pattern-matches
  -- on `x * x`, NOT `x ^ 2`. `hx`'s shape (`x ^ 2 + ...`) never matched at all (the earlier
  -- "leading coefficient" diagnosis was wrong; the real gap is `^2` vs `x*x`). Restating
  -- in the exact required shape fixes it.
  have hx' : (1 : ℝ) * (x * x) + (η - 1) * x + 1 / η = 0 := by
    rw [one_mul, ← pow_two]; exact hx
  have hsq := discrim_eq_sq_of_quadratic_eq_zero hx' -- discrim = (2x+(η-1))²
  linarith [sq_nonneg (2 * x + (η - 1)), trib_quotient_discrim_neg, hsq]

-- α, β: the non-real conjugate pair, existence packaged abstractly
noncomputable def α : ℂ := sorry -- root of X²+(η-1)X+1/η over ℂ, Im ≠ 0 (from trib_quotient_no_real_root)
noncomputable def β : ℂ := starRingEnd ℂ α -- conjugate

theorem alpha_beta_ne_real : α.im ≠ 0 := by
  sorry -- from trib_quotient_no_real_root: no REAL root of the quotient ⟹ its complex
        -- roots are non-real, hence come as a conjugate pair (β := conj α)

theorem alpha_ne_beta : α ≠ β := by
  sorry -- α = conj α would force α.im = 0, contradicting `alpha_beta_ne_real`

theorem eta_ne_alpha : (η : ℂ) ≠ α := by
  sorry -- η real, α non-real
theorem eta_ne_beta : (η : ℂ) ≠ β := by
  sorry -- η real, β non-real

-- modulus via Vieta: η·α·β = 1 (product of roots of tribCharPoly), αβ = |α|² since β = conj α
theorem alpha_modulus_eq : Complex.abs α = 1 / Real.sqrt η := by
  sorry -- η·(α * conj α) = 1  ⟹  η·|α|² = 1  ⟹  |α| = 1/√η

theorem alpha_modulus_lt_one : Complex.abs α < 1 := by
  sorry -- 1/√η < 1 since η > 1 (from eta_mem_Ioo)

/-! ## 3. Perron–Frobenius framing (independent cross-check via the substitution matrix)

   NOTE (build fix, this session): `TriboM.IsPrimitive`
   (Mathlib.LinearAlgebra.Matrix.Irreducible.Defs) and `Matrix.perronRoot` (open,
   unmerged Mathlib PR chain #39917–#39922, mkaratarakis/or4nge19) are confirmed
   ABSENT at the pinned mathlib rev (v4.14.0) — checked directly against the actual
   checked-out commit via `find`, not assumed. The two theorems that depended on them,
   `triboM_isPrimitive` and `triboM_perronRoot_eq_eta`, have been dropped. Everything
   else in this section (`triboM_eigen_eq`, `triboM_eigenvector_pos`) is plain matrix
   algebra and doesn't need either missing module — kept as-is.
-/

theorem triboM_eigen_eq :
    TriboM.mulVec ![η ^ 2, η, 1] = η • ![η ^ 2, η, 1] := by
  sorry -- reduces to η² = η + 1 + 1/η, i.e. eta_cubic after clearing denominators

theorem triboM_eigenvector_pos : ∀ i, 0 < (![η ^ 2, η, 1] : Fin 3 → ℝ) i := by
  sorry -- from eta_pos

/-! ## 4. Binet-type closed form -/

theorem geom_eta_isSol :
    tribRecC.IsSolution (fun n => (η : ℂ) ^ n) := by
  sorry -- geom_sol_iff_root_charPoly, η is a root of tribCharPoly (tribRecC.charPoly = tribCharPoly.map (algebraMap ℝ ℂ))

theorem geom_alpha_isSol :
    tribRecC.IsSolution (fun n => α ^ n) := by
  sorry -- geom_sol_iff_root_charPoly, α is a root of tribCharPoly

theorem geom_beta_isSol :
    tribRecC.IsSolution (fun n => β ^ n) := by
  sorry -- geom_sol_iff_root_charPoly, β is a root of tribCharPoly

theorem trib_geom_basis :
    LinearIndependent ℂ ![fun n => (η : ℂ) ^ n, fun n => α ^ n, fun n => β ^ n] := by
  sorry -- Vandermonde, nonsingular from {eta_ne_alpha, eta_ne_beta, alpha_ne_beta}

-- w : the actual sequence from the paper (⟨n_k⟩), assumed to satisfy tribRec
variable (w : ℕ → ℝ) (hw : tribRec.IsSolution w)

theorem exists_binet_coeffs :
    ∃! c : Fin 3 → ℂ, ∀ n : ℕ, (w n : ℂ) = c 0 * (η : ℂ) ^ n + c 1 * α ^ n + c 2 * β ^ n := by
  sorry -- trib_geom_basis spans (dimension count via `LinearRecurrence.solSpace_rank`)
        -- + injectivity of `LinearRecurrence.toInit`

theorem binet_coeffs_conj_symmetric (c : Fin 3 → ℂ)
    (hc : ∀ n, (w n : ℂ) = c 0 * (η : ℂ) ^ n + c 1 * α ^ n + c 2 * β ^ n) :
    (starRingEnd ℂ) (c 0) = c 0 ∧ (starRingEnd ℂ) (c 1) = c 2 := by
  sorry -- conjugate `hc`; conj η=η, conj α=β, conj β=α; match against `exists_binet_coeffs`

theorem trib_closed_form (c1 : ℝ) (c2 : ℂ)
    (hc : ∀ n : ℕ, (w n : ℂ) = (c1 : ℂ) * (η : ℂ) ^ n + c2 * α ^ n + (starRingEnd ℂ) c2 * β ^ n) :
    ∀ n : ℕ, w n = c1 * η ^ n + 2 * (c2 * α ^ n).re := by
  sorry -- c2·α^n + conj(c2)·β^n = c2·α^n + conj(c2·α^n) = 2 Re(c2·α^n)

/-! ## 5. The target theorem -/

theorem tendsto_trib_succ_div_trib_atTop (c1 : ℝ) (hc1 : c1 ≠ 0) :
    Filter.Tendsto (fun n => w (n + 1) / w n) Filter.atTop (nhds η) := by
  sorry
  -- w(n)/η^n = c1 + 2 Re(c2·(α/η)^n); |α/η| = |α|/η = η^(-3/2) < 1 (alpha_modulus_eq, eta_mem_Ioo)
  -- so (α/η)^n → 0, hence w(n)/η^n → c1 ≠ 0, and w(n+1)/w(n) = η · (w(n+1)/η^(n+1)) / (w(n)/η^n) → η

/-! ## 6. NOT YET DONE — data-dependent hypothesis

   `hc1 : c1 ≠ 0` above must be checked against the paper's ACTUAL initial values
   (w(0), w(1), w(2) for the F.1 observable). True for essentially every seed
   (it excludes only the measure-zero {α,β}-eigenspace), but not free — pull the
   real numbers from the .tex source before treating this as closed.
-/

/-! ## 7. The general lift (proposed Mathlib contribution, fills a confirmed gap:
   Loogle query `LinearRecurrence, Filter.Tendsto` returns 0 results as of this session) -/

theorem LinearRecurrence.tendsto_succ_div_of_dominant_simple_root
    (E : LinearRecurrence ℝ) (r : Fin E.order → ℂ)
    (hroots : ∀ i, (E.charPoly.map (algebraMap ℝ ℂ)).IsRoot (r i))
    (hdistinct : Function.Injective r)
    (hsplit : Fintype.card (Fin E.order) = E.charPoly.natDegree)
    (i₀ : Fin E.order) (hreal : (r i₀).im = 0)
    (hdom : ∀ j ≠ i₀, Complex.abs (r j) < Complex.abs (r i₀))
    (w : ℕ → ℝ) (hw : E.IsSolution w)
    (c : Fin E.order → ℂ) (hc : ∀ n, (w n : ℂ) = ∑ i, c i * (r i) ^ n)
    (hc0 : c i₀ ≠ 0) :
    Filter.Tendsto (fun n => w (n + 1) / w n) Filter.atTop (nhds (r i₀).re) := by
  sorry
  -- w(n)/r_{i₀}^n = c_{i₀} + ∑_{j≠i₀} c_j (r_j/r_{i₀})^n → c_{i₀} (each term → 0 via hdom)
  -- Fibonacci (order 2) and this file's Tribonacci (order 3) result both become
  -- corollaries of this one theorem once it exists.
