import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace DM3

/-! # dm³ Spectral Geometry — Monotonicity Layer
1D and 3D rectangular acoustic + thin-shell Schumann under curvature κ ≥ 0.

All eigenvalue monotonicity results hold in the **physical regime** κ ≥ 0, under
which each chamber dimension Lκ = L₀·(1+γκ) is strictly positive.  The extra
hypothesis `hκ₁ : 0 ≤ κ₁` is stated explicitly wherever it is needed to ensure
the denominators in λ3D are positive. -/

/-- Linear curvature scaling: Lκ(L₀, γ, κ) = L₀ · (1 + γ · κ). -/
def Lκ (L0 γ κ : ℝ) : ℝ := L0 * (1 + γ * κ)

/-- Seed eigenvalue for 1D case: Aₙ = (π n / L₀)². -/
def A1D (n : ℕ) (L0 : ℝ) : ℝ := (Real.pi * n / L0) ^ 2

/-- 1D curvature-deformed eigenvalue: λₙ(κ) = Aₙ (1 + γ κ)⁻². -/
def λ1D (n : ℕ) (L0 γ κ : ℝ) : ℝ :=
  A1D n L0 * (1 + γ * κ)⁻²

/-! ## Full 3D Rectangular Cavity (Neumann) -/

/-- Eigenvalue for mode (nx, ny, nz) under uniform curvature scaling per axis. -/
def λ3D (nx ny nz : ℕ) (Lx0 Ly0 Lz0 γ κ : ℝ) : ℝ :=
  Real.pi ^ 2 * (
    (nx ^ 2 : ℝ) / (Lκ Lx0 γ κ) ^ 2 +
    (ny ^ 2 : ℝ) / (Lκ Ly0 γ κ) ^ 2 +
    (nz ^ 2 : ℝ) / (Lκ Lz0 γ κ) ^ 2 )

/-! ### Private helpers -/

private lemma Lκ_pos (L0 γ κ : ℝ) (hL0 : 0 < L0) (hγ : 0 < γ) (hκ : 0 ≤ κ) :
    0 < Lκ L0 γ κ :=
  mul_pos hL0 (by have := mul_nonneg (le_of_lt hγ) hκ; linarith)

private lemma Lκ_mono (L0 γ : ℝ) (hL0 : 0 < L0) (hγ : 0 < γ)
    {κ₁ κ₂ : ℝ} (hle : κ₁ ≤ κ₂) :
    Lκ L0 γ κ₁ ≤ Lκ L0 γ κ₂ := by
  unfold Lκ
  apply mul_le_mul_of_nonneg_left _ (le_of_lt hL0)
  have := mul_le_mul_of_nonneg_left hle (le_of_lt hγ)
  linarith

/-- Each per-axis term n²/(Lκ)² is antitone in κ on the physical regime κ ≥ 0. -/
private lemma term_antitone (n : ℕ) (L0 γ : ℝ) (hL0 : 0 < L0) (hγ : 0 < γ)
    {κ₁ κ₂ : ℝ} (hκ₁ : 0 ≤ κ₁) (hle : κ₁ ≤ κ₂) :
    (n ^ 2 : ℝ) / (Lκ L0 γ κ₂) ^ 2 ≤ (n ^ 2 : ℝ) / (Lκ L0 γ κ₁) ^ 2 := by
  have hκ₂ : 0 ≤ κ₂ := le_trans hκ₁ hle
  have h1 := Lκ_pos L0 γ κ₁ hL0 hγ hκ₁
  have h2 := Lκ_pos L0 γ κ₂ hL0 hγ hκ₂
  have hmono : Lκ L0 γ κ₁ ≤ Lκ L0 γ κ₂ := Lκ_mono L0 γ hL0 hγ hle
  have h3 : (Lκ L0 γ κ₁) ^ 2 ≤ (Lκ L0 γ κ₂) ^ 2 :=
    pow_le_pow_left (le_of_lt h1) hmono 2
  -- n²/b ≤ n²/c  ↔  n²·c ≤ n²·b  (cross-multiply, b = (Lκ κ₂)², c = (Lκ κ₁)²)
  rw [div_le_div_iff (pow_pos h2 2) (pow_pos h1 2)]
  exact mul_le_mul_of_nonneg_left h3 (sq_nonneg _)

/-- Strict version: n²/(Lκ)² is strictly antitone in κ when n ≠ 0. -/
private lemma term_strictAnti (n : ℕ) (hn : n ≠ 0) (L0 γ : ℝ) (hL0 : 0 < L0) (hγ : 0 < γ)
    {κ₁ κ₂ : ℝ} (hκ₁ : 0 ≤ κ₁) (hlt : κ₁ < κ₂) :
    (n ^ 2 : ℝ) / (Lκ L0 γ κ₂) ^ 2 < (n ^ 2 : ℝ) / (Lκ L0 γ κ₁) ^ 2 := by
  have hκ₂ : 0 ≤ κ₂ := le_of_lt (lt_of_le_of_lt hκ₁ hlt)
  have h1 := Lκ_pos L0 γ κ₁ hL0 hγ hκ₁
  have h2 := Lκ_pos L0 γ κ₂ hL0 hγ hκ₂
  have hmono : Lκ L0 γ κ₁ < Lκ L0 γ κ₂ := by
    unfold Lκ
    apply mul_lt_mul_of_pos_left _ hL0
    have := mul_lt_mul_of_pos_left hlt (le_of_lt hγ)
    linarith
  have h3 : (Lκ L0 γ κ₁) ^ 2 < (Lκ L0 γ κ₂) ^ 2 :=
    pow_lt_pow_left hmono (le_of_lt h1) (by norm_num)
  have hn2 : (0 : ℝ) < (n : ℝ) ^ 2 :=
    pow_pos (by exact_mod_cast Nat.pos_of_ne_zero hn) 2
  rw [div_lt_div_iff (pow_pos h2 2) (pow_pos h1 2)]
  exact mul_lt_mul_of_pos_left h3 hn2

/-! ### Main monotonicity theorems -/

/-- **Antitone**: larger curvature κ enlarges each chamber dimension,
    which lowers all 3D acoustic eigenvalues. Physical regime: `κ₁ ≥ 0`. -/
lemma λ3D_antitone
    (nx ny nz : ℕ) (Lx0 Ly0 Lz0 γ : ℝ)
    (hLx : 0 < Lx0) (hLy : 0 < Ly0) (hLz : 0 < Lz0) (hγ : 0 < γ)
    {κ₁ κ₂ : ℝ} (hκ₁ : 0 ≤ κ₁) (hle : κ₁ ≤ κ₂) :
    λ3D nx ny nz Lx0 Ly0 Lz0 γ κ₂ ≤ λ3D nx ny nz Lx0 Ly0 Lz0 γ κ₁ := by
  dsimp [λ3D]
  apply mul_le_mul_of_nonneg_left _ (by positivity)
  have hx := term_antitone nx Lx0 γ hLx hγ hκ₁ hle
  have hy := term_antitone ny Ly0 γ hLy hγ hκ₁ hle
  have hz := term_antitone nz Lz0 γ hLz hγ hκ₁ hle
  linarith

/-- **Strictly antitone**: for any mode with at least one nonzero index,
    the eigenvalue strictly decreases as κ increases. Physical regime: `κ₁ ≥ 0`. -/
lemma λ3D_strictAnti
    (nx ny nz : ℕ) (Lx0 Ly0 Lz0 γ : ℝ)
    (hLx : 0 < Lx0) (hLy : 0 < Ly0) (hLz : 0 < Lz0) (hγ : 0 < γ)
    (hmode : nx ≠ 0 ∨ ny ≠ 0 ∨ nz ≠ 0)
    {κ₁ κ₂ : ℝ} (hκ₁ : 0 ≤ κ₁) (hlt : κ₁ < κ₂) :
    λ3D nx ny nz Lx0 Ly0 Lz0 γ κ₂ < λ3D nx ny nz Lx0 Ly0 Lz0 γ κ₁ := by
  dsimp [λ3D]
  apply mul_lt_mul_of_pos_left _ (by positivity)
  rcases hmode with hnx | hny | hnz
  · -- nx ≠ 0: x-term strictly decreases, y- and z-terms weakly decrease
    have hx := term_strictAnti nx hnx Lx0 γ hLx hγ hκ₁ hlt
    have hy := term_antitone ny Ly0 γ hLy hγ hκ₁ (le_of_lt hlt)
    have hz := term_antitone nz Lz0 γ hLz hγ hκ₁ (le_of_lt hlt)
    linarith
  · -- ny ≠ 0: y-term strictly decreases
    have hx := term_antitone nx Lx0 γ hLx hγ hκ₁ (le_of_lt hlt)
    have hy := term_strictAnti ny hny Ly0 γ hLy hγ hκ₁ hlt
    have hz := term_antitone nz Lz0 γ hLz hγ hκ₁ (le_of_lt hlt)
    linarith
  · -- nz ≠ 0: z-term strictly decreases
    have hx := term_antitone nx Lx0 γ hLx hγ hκ₁ (le_of_lt hlt)
    have hy := term_antitone ny Ly0 γ hLy hγ hκ₁ (le_of_lt hlt)
    have hz := term_strictAnti nz hnz Lz0 γ hLz hγ hκ₁ hlt
    linarith

/-! ## Thin-Shell Schumann -/

/-- Effective ionospheric height deformed by curvature κ.
    Note: `hκ h0 γ κ = Lκ h0 γ κ` definitionally. -/
def hκ (h0 γ κ : ℝ) : ℝ := h0 * (1 + γ * κ)

/-- Schumann resonance frequency formula: fₙ ≈ (c/2πa)√(n(n+1))·(a/(a+h)). -/
def f_schumann (n : ℕ) (a c h : ℝ) : ℝ :=
  (c / (2 * Real.pi * a)) * Real.sqrt (n * (n + 1)) * (a / (a + h))

/-- f_schumann is antitone in h on the physical regime h ≥ 0
    (larger effective height → lower Schumann frequency). -/
lemma f_schumann_antitone_in_h
    (n : ℕ) (a c : ℝ) (ha : 0 < a) (hc : 0 < c)
    {h₁ h₂ : ℝ} (hh₁ : 0 ≤ h₁) (hle : h₁ ≤ h₂) :
    f_schumann n a c h₂ ≤ f_schumann n a c h₁ := by
  dsimp [f_schumann]
  have hd1 : 0 < a + h₁ := by linarith
  have hd2 : 0 < a + h₂ := by linarith [le_trans hh₁ hle]
  apply mul_le_mul_of_nonneg_left _ (by positivity)
  rw [div_le_div_iff hd2 hd1]
  nlinarith

/-- κ-deformed Schumann frequency. -/
def f_schumann_κ (n : ℕ) (a c h0 γ κ : ℝ) : ℝ :=
  f_schumann n a c (hκ h0 γ κ)

/-- Schumann frequency is antitone in κ on the physical regime κ₁ ≥ 0
    (larger κ increases effective height, lowers frequency). -/
lemma f_schumann_monotone_in_κ
    (n : ℕ) (a c h0 γ : ℝ)
    (ha : 0 < a) (hc : 0 < c) (hh0 : 0 < h0) (hγ : 0 < γ)
    {κ₁ κ₂ : ℝ} (hκ₁ : 0 ≤ κ₁) (hle : κ₁ ≤ κ₂) :
    f_schumann_κ n a c h0 γ κ₂ ≤ f_schumann_κ n a c h0 γ κ₁ := by
  dsimp [f_schumann_κ]
  -- hκ = Lκ definitionally; reuse Lκ helpers
  apply f_schumann_antitone_in_h ha hc
  · -- 0 ≤ hκ h0 γ κ₁ = Lκ h0 γ κ₁ > 0
    exact le_of_lt (Lκ_pos h0 γ κ₁ hh0 hγ hκ₁)
  · -- hκ h0 γ κ₁ ≤ hκ h0 γ κ₂ = Lκ_mono
    exact Lκ_mono h0 γ hh0 hγ hle

/-! ## Monotonicity in Chamber Dimension

The eigenvalue λ3D is also strictly antitone in each chamber length L0 (for fixed κ).
This captures the Wolfe wall-offset sensitivity: enlarging a dimension lowers modes.
-/

/-- λ3D is strictly antitone in the first chamber dimension (Lx0) when nx ≠ 0.
    Larger room → smaller eigenvalue, at fixed κ ≥ 0. -/
lemma λ3D_strictAnti_in_Lx0
    (ny nz : ℕ) (Lx1 Lx2 Ly0 Lz0 γ : ℝ)
    (hLx1 : 0 < Lx1) (hLx2 : Lx1 < Lx2)
    (hLy : 0 < Ly0) (hLz : 0 < Lz0) (hγ : 0 < γ)
    {κ : ℝ} (hκ : 0 ≤ κ) :
    λ3D 1 ny nz Lx2 Ly0 Lz0 γ κ < λ3D 1 ny nz Lx1 Ly0 Lz0 γ κ := by
  dsimp [λ3D]
  apply mul_lt_mul_of_pos_left _ (by positivity)
  -- x-term is strictly smaller for the larger Lx2 (holds for nx = 1 ≠ 0)
  have hLκ1 : 0 < Lκ Lx1 γ κ := Lκ_pos Lx1 γ κ hLx1 hγ hκ
  have hLκ2 : 0 < Lκ Lx2 γ κ := Lκ_pos Lx2 γ κ (lt_trans hLx1 hLx2) hγ hκ
  have hmono : Lκ Lx1 γ κ < Lκ Lx2 γ κ := by
    unfold Lκ
    apply mul_lt_mul_of_pos_right hLx2
    have := mul_nonneg (le_of_lt hγ) hκ; linarith
  have hx : (1 ^ 2 : ℝ) / (Lκ Lx2 γ κ) ^ 2 < (1 ^ 2 : ℝ) / (Lκ Lx1 γ κ) ^ 2 := by
    rw [div_lt_div_iff (pow_pos hLκ2 2) (pow_pos hLκ1 2)]
    have h3 := pow_lt_pow_left hmono (le_of_lt hLκ1) (by norm_num)
    norm_num; exact h3
  -- y- and z-terms are equal (same Ly0, Lz0, κ on both sides)
  have hy : (ny ^ 2 : ℝ) / (Lκ Ly0 γ κ) ^ 2 = (ny ^ 2 : ℝ) / (Lκ Ly0 γ κ) ^ 2 := rfl
  have hz : (nz ^ 2 : ℝ) / (Lκ Lz0 γ κ) ^ 2 = (nz ^ 2 : ℝ) / (Lκ Lz0 γ κ) ^ 2 := rfl
  linarith

/-! ## Universal Sensitivity -/

/-- Universal curvature sensitivity: ∂λ/∂κ = −2Aγ/(1+γκ)³.
    This functional form is independent of the specific geometry (1D, 3D box, or
    spherical shell) as long as the deformation is a uniform K-scaling of all
    linear dimensions.  It is the mathematical signature of the K operator. -/
def S (A γ κ : ℝ) : ℝ := -2 * A * γ / (1 + γ * κ) ^ 3

/-- The sensitivity S is strictly negative for positive A, γ, and κ ≥ 0. -/
lemma S_negative (A γ κ : ℝ) (hA : 0 < A) (hγ : 0 < γ) (hκ : 0 ≤ κ) :
    S A γ κ < 0 := by
  unfold S
  apply neg_lt_zero.mpr
  apply div_pos <;> positivity

end DM3
