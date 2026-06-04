import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import «dm3-dual-cavity».Monotonicity

open DM3

/-! # dm³ Examples — Matching the Notebooks

Concrete parameter choices that mirror the Python notebooks:
- Hypogeum-like 3D box
- Schumann thin-shell
and simple lemmas showing λ(κ₁) ≥ λ(κ₂) for κ₁ < κ₂. -/

/-! ## Hypogeum-style 3D rectangular cavity -/

namespace HypogeumExample

-- Approximate effective lengths (meters)
def Lx0 : ℝ := 5.2
def Ly0 : ℝ := 4.1
def Lz0 : ℝ := 2.8

-- Curvature scaling parameter (dimensionless)
def γ : ℝ := 0.4

-- Fundamental mode (1,0,0) as a toy example
def λ_fund (κ : ℝ) : ℝ :=
  λ3D 1 0 0 Lx0 Ly0 Lz0 γ κ

/-- λ_fund is antitone in the physical regime: larger κ → lower eigenvalue. -/
lemma λ_fund_antitone {κ₁ κ₂ : ℝ} (hκ₁ : 0 ≤ κ₁) (hle : κ₁ ≤ κ₂) :
    λ_fund κ₂ ≤ λ_fund κ₁ := by
  dsimp [λ_fund]
  exact λ3D_antitone 1 0 0 Lx0 Ly0 Lz0 γ
    (by norm_num [Lx0]) (by norm_num [Ly0]) (by norm_num [Lz0]) (by norm_num [γ])
    hκ₁ hle

/-- Concrete numerical check: κ = 0.4 gives a lower eigenvalue than κ = 0.1. -/
example : λ_fund 0.4 ≤ λ_fund 0.1 :=
  λ_fund_antitone (by norm_num) (by norm_num)

end HypogeumExample

/-! ## Schumann thin-shell example -/

namespace SchumannExample

-- Earth radius and speed of light (SI units)
def a : ℝ := 6_371_000.0
def c : ℝ := 3e8

-- Baseline effective height and curvature scaling
def h0 : ℝ := 85_000.0
def γ : ℝ := 0.3

-- n = 1 Schumann mode with curvature on height
def f1 (κ : ℝ) : ℝ :=
  f_schumann_κ 1 a c h0 γ κ

/-- f1 is antitone in the physical regime: larger κ → lower Schumann frequency. -/
lemma f1_antitone {κ₁ κ₂ : ℝ} (hκ₁ : 0 ≤ κ₁) (hle : κ₁ ≤ κ₂) :
    f1 κ₂ ≤ f1 κ₁ := by
  dsimp [f1]
  exact f_schumann_monotone_in_κ 1 a c h0 γ
    (by norm_num [a]) (by norm_num [c]) (by norm_num [h0]) (by norm_num [γ])
    hκ₁ hle

/-- Concrete numerical check: κ = 0.4 gives a lower Schumann frequency than κ = 0.1. -/
example : f1 0.4 ≤ f1 0.1 :=
  f1_antitone (by norm_num) (by norm_num)

end SchumannExample
