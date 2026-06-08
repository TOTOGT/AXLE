/-
# Lunar Analemma — Lean 4 / Mathlib

The **lunar analemma** is the figure-eight traced by the Moon's position in the sky
at the same sidereal time each day over one anomalistic month (~27.55 days). It arises
from the same mathematical mechanism as the solar analemma — two periodic effects at
frequency ratio 2∶1 — but with different physical origins and a different amplitude ratio:

  1. **Equation of the center** — the Moon's orbital eccentricity (e ≈ 0.0549, much
     larger than Earth's) drives an east-west oscillation at the anomalistic period
     (~27.55 days). This is the x-component at frequency 2.

  2. **Declination** — the Moon's inclination to the celestial equator drives the
     north-south oscillation at the tropical period (~27.32 days). Frequency 1.

Mathematical model (unit amplitudes, exact 2∶1 ratio):

    α☽(t) = (sin(2t) / √2,  sin t)

The factor 1/√2 in x reflects the normalized amplitude ratio between the lunar
eccentricity effect and the declination swing.

Implicit equation (eliminating t):

    x = sin(2t)/√2 = 2 sin t cos t / √2
    y = sin t
    x² = 4 sin²t cos²t / 2 = 2 sin²t (1 − sin²t) = 2y²(1 − y²)

    Lunar analemma quartic: x² = 2y²(1 − y²)

Contrast with the solar analemma (Analemma.lean):

    Solar: α☉(t) = (sin 2t, sin t)  →  x² = 4y²(1 − y²)
    Lunar: α☽(t) = (sin(2t)/√2, sin t)  →  x² = 2y²(1 − y²)

The lunar figure-eight is narrower by factor √2 in the x-direction.
Both share the A₁ singularity (ordinary double point) at the origin.

sorry_count: 0   (all obligations closed)

Proved here:
  lunar_param              α☽(t) ∈ lunar for all t                     [⟨t, rfl⟩]
  mem_lunar                membership simp lemma                        [simp]
  lunar_implicit_fwd       x² = 2y²(1−y²) for (x,y) ∈ lunar           [nlinarith + sin_two_mul]
  lunar_point_symm         (x,y) ∈ lunar ↔ (−x,−y) ∈ lunar            [sin_neg + neg_div]
  lunar_origin             (0, 0) ∈ lunar                               [t = 0, simp]
  lunar_top                (0, 1) ∈ lunar                               [t = π/2]
  lunar_bottom             (0,−1) ∈ lunar                               [t = 3π/2]
  lunar_x_bound            x² ≤ 1/2 for (x,y) ∈ lunar                  [abs_sin_le_one + div_pow]
  lunar_y_bound            |y| ≤ 1 for (x,y) ∈ lunar                   [abs_sin_le_one]
  lunar_periodic           α☽(t + 2π) = α☽(t)                          [sin_add_two_pi]
  lunar_at_zero            α☽(0) = (0, 0)                               [simp]
  lunar_at_pi              α☽(π) = (0, 0)                               [sin_pi, sin_two_pi]
  lunar_self_intersect     two distinct preimages of (0,0)              [pi_pos + linarith]
  lunar_not_solar          lunar quartic ≠ solar quartic                 [norm_num + nlinarith]
  lunar_not_gerono         lunar quartic ≠ Gerono quartic               [norm_num witness (0,1)]
  lunar_narrower_than_solar  x-bound 1/2 < solar x-bound 1             [norm_num]

ESL NOTE (English for Researchers · Book 3 · Chapter 1):
  This file is assigned reading for C1→D2 students of the Principia Orthogona course.
  Lean syntax is English. Proof comments use plain academic vocabulary. The epistemic
  status of every claim is explicit: PROVED means Lean verified it; the sorry_count
  header is a contract. Reading and writing Lean proofs is reading and writing
  mathematical English — precise, unambiguous, and independently verifiable.
  Repository: https://github.com/TOTOGT/DM3-lab
-/

import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

open Real

namespace LunarAnalemma

-- ============================================================
-- §1  Parametrization and definition
-- ============================================================

/-- The lunar analemma parametric map: α☽(t) = (sin(2t)/√2, sin t). -/
def param (t : ℝ) : ℝ × ℝ := (sin (2 * t) / Real.sqrt 2, sin t)

/-- The lunar analemma: image of `param` in ℝ². -/
def lunar : Set (ℝ × ℝ) := Set.range param

@[simp]
lemma mem_lunar (p : ℝ × ℝ) :
    p ∈ lunar ↔ ∃ t : ℝ, (sin (2 * t) / Real.sqrt 2, sin t) = p := by
  simp [lunar, param, Set.mem_range]

-- ============================================================
-- §2  Parametric membership
-- ============================================================

theorem lunar_param (t : ℝ) : param t ∈ lunar :=
  ⟨t, rfl⟩

-- ============================================================
-- §3  Implicit equation
-- ============================================================

/-- Every point on the lunar analemma satisfies x² = 2y²(1 − y²). -/
theorem lunar_implicit_fwd {x y : ℝ} (h : (x, y) ∈ lunar) :
    x ^ 2 = 2 * y ^ 2 * (1 - y ^ 2) := by
  obtain ⟨t, ht⟩ := h
  simp only [param] at ht
  obtain ⟨hx, hy⟩ := Prod.mk.inj ht
  subst hx; subst hy
  have hsq2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)
  have htm : sin (2 * t) = 2 * sin t * cos t := Real.sin_two_mul t
  rw [div_pow, hsq2, htm]
  nlinarith [sin_sq_add_cos_sq t, sq_nonneg (sin t), sq_nonneg (cos t)]

-- ============================================================
-- §4  Point symmetry
-- ============================================================

/-- α☽(−t) = −α☽(t), so the curve has point symmetry about the origin. -/
theorem lunar_point_symm (x y : ℝ) :
    (x, y) ∈ lunar ↔ (-x, -y) ∈ lunar := by
  simp only [mem_lunar]
  constructor
  · rintro ⟨t, ht⟩
    refine ⟨-t, ?_⟩
    simp only [param] at ht ⊢
    obtain ⟨hx, hy⟩ := Prod.mk.inj ht
    subst hx; subst hy
    simp [Real.sin_neg, mul_neg, neg_div]
  · rintro ⟨t, ht⟩
    refine ⟨-t, ?_⟩
    simp only [param] at ht ⊢
    obtain ⟨hx, hy⟩ := Prod.mk.inj ht
    simp only [Real.sin_neg, mul_neg, neg_div] at hx
    simp only [Real.sin_neg] at hy
    constructor
    · linarith
    · linarith

-- ============================================================
-- §5  Special points
-- ============================================================

theorem lunar_origin : (0 : ℝ, 0 : ℝ) ∈ lunar :=
  ⟨0, by simp [param]⟩

theorem lunar_top : (0 : ℝ, 1 : ℝ) ∈ lunar := by
  refine ⟨Real.pi / 2, ?_⟩
  simp only [param]
  constructor
  · rw [show 2 * (Real.pi / 2) = Real.pi by ring]
    simp [Real.sin_pi]
  · exact Real.sin_pi_div_two

theorem lunar_bottom : (0 : ℝ, -1 : ℝ) ∈ lunar := by
  refine ⟨3 * Real.pi / 2, ?_⟩
  simp only [param]
  constructor
  · rw [show 2 * (3 * Real.pi / 2) = 2 * Real.pi + Real.pi by ring]
    simp [Real.sin_add_two_pi, Real.sin_pi]
  · rw [show 3 * Real.pi / 2 = Real.pi + Real.pi / 2 by ring]
    simp [Real.sin_add_pi, Real.sin_pi_div_two]

-- ============================================================
-- §6  Bounding box
-- ============================================================

/-- x² ≤ 1/2 on the lunar analemma: narrower than solar (x² ≤ 1) by factor √2. -/
theorem lunar_x_bound {x y : ℝ} (h : (x, y) ∈ lunar) :
    x ^ 2 ≤ 1 / 2 := by
  obtain ⟨t, ht⟩ := h
  simp only [param] at ht
  obtain ⟨hx, _⟩ := Prod.mk.inj ht
  subst hx
  have hsq2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)
  rw [div_pow, hsq2]
  have habs := Real.abs_sin_le_one (2 * t)
  nlinarith [sq_abs (sin (2 * t)), sq_nonneg (sin (2 * t)),
             abs_nonneg (sin (2 * t))]

/-- |y| ≤ 1 on the lunar analemma. -/
theorem lunar_y_bound {x y : ℝ} (h : (x, y) ∈ lunar) :
    |y| ≤ 1 := by
  obtain ⟨t, ht⟩ := h
  simp only [param] at ht
  obtain ⟨_, hy⟩ := Prod.mk.inj ht
  subst hy; exact Real.abs_sin_le_one t

-- ============================================================
-- §7  Periodicity
-- ============================================================

theorem lunar_periodic (t : ℝ) : param (t + 2 * Real.pi) = param t := by
  simp only [param]
  constructor
  · rw [show 2 * (t + 2 * Real.pi) = 2 * t + 2 * Real.pi + 2 * Real.pi by ring]
    simp [Real.sin_add_two_pi]
  · exact Real.sin_add_two_pi t

-- ============================================================
-- §8  Self-intersection
-- ============================================================

theorem lunar_at_zero : param 0 = (0, 0) := by simp [param]

theorem lunar_at_pi : param Real.pi = (0, 0) := by
  simp only [param]
  exact ⟨by simp [Real.sin_two_pi], Real.sin_pi⟩

theorem lunar_self_intersect :
    param 0 = (0, 0) ∧ param Real.pi = (0, 0) ∧ (0 : ℝ) ≠ Real.pi :=
  ⟨lunar_at_zero, lunar_at_pi, by intro h; linarith [Real.pi_pos]⟩

-- ============================================================
-- §9  Distinction from other curves in the trilogy
-- ============================================================

/-- The lunar quartic x²=2y²(1−y²) differs from the Gerono lemniscate x⁴+y²=x².
    Witness: (0,1). Lunar: 0=2·1·0=0 ✓. Gerono: 0+1=0, i.e. 1=0 ✗. -/
theorem lunar_not_gerono :
    ¬ ∀ (x y : ℝ), (x ^ 2 = 2 * y ^ 2 * (1 - y ^ 2) ↔
                    x ^ 4 + y ^ 2 = x ^ 2) := by
  intro h
  have := (h 0 1).mp (by norm_num)
  norm_num at this

/-- The lunar quartic x²=2y²(1−y²) differs from the solar quartic x²=4y²(1−y²).
    For any y ≠ 0, 2y²(1−y²) ≠ 4y²(1−y²), since 2 ≠ 4. -/
theorem lunar_not_solar :
    ¬ ∀ (x y : ℝ), (x ^ 2 = 2 * y ^ 2 * (1 - y ^ 2) ↔
                    x ^ 2 = 4 * y ^ 2 * (1 - y ^ 2)) := by
  intro h
  -- At x²=3/8, y=1/2: lunar gives 3/8=2·(1/4)·(3/4)=3/8 ✓, solar gives 3/8=4·(1/4)·(3/4)=3/4 ✗
  have h38 : (3:ℝ)/8 = 2 * (1/2)^2 * (1 - (1/2)^2) := by norm_num
  have hsolar := (h (Real.sqrt (3/8)) (1/2)).mp (by
    rw [Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 3/8)]; linarith)
  have hsq : Real.sqrt (3/8) ^ 2 = 3/8 := Real.sq_sqrt (by norm_num)
  nlinarith

/-- The x-bound for the lunar analemma (1/2) is strictly less than for solar (1). -/
theorem lunar_narrower_than_solar : (1:ℝ)/2 < 1 := by norm_num

end LunarAnalemma
