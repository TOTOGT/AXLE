-- ============================================================================
/-
  AXLE — Algebraic eXpression Language for Evaluation
  Principia Orthogona · G⁵ · Complete Completeness
  Version 8.1 — All type errors fixed; 6 honest admits remain (kernel-checked)

  Foundational volumes (Principia Orthogona series):
  1. 10.5281/zenodo.19117399
  2. 10.5281/zenodo.19379472
  3. 10.5281/zenodo.19122167
  4. 10.5281/zenodo.19162012
  5. 10.5281/zenodo.19208014
  6. 10.5281/zenodo.19210136
  7. 10.5281/zenodo.19208283
  8. 10.5281/zenodo.19210057
  9. 10.5281/zenodo.19378741
  10. 10.5281/zenodo.19379384
-/
-- ============================================================================

-- Runnable copy of `main/axle_v8.1`, which is Lean source carrying a version number
-- where its extension should be: `lake` cannot build it, no census counts it, and a
-- citation to "AXLE_v8.1.lean" resolves to nothing.
--
-- VERIFIED 2026-08-28.  Elaborates with zero errors under Lean 4.32.0 against the
-- Mathlib built in the geometry repository.  Six `sorry` warnings, six declarations,
-- six `sorryAx`.  Reproduce with:
--     cd ~/Desktop/geometry && lake env lean ~/Desktop/AXLE/main/AXLE_v8_1.lean
--
-- Before that run the file did not elaborate at all: twelve errors of Mathlib API
-- drift from the v4.14 it was written against.  Statements, not just proofs, were
-- affected -- `closurePoints_stationary_regular` had `hreg : sorry` as its hypothesis
-- because `Ordinal.IsLimit` no longer resolved, so its `sorryAx` was reporting a
-- broken statement rather than an honest admit.  Fixed:
--     Ordinal.sup          -> iSup            Ordinal.omega -> Ordinal.omega0
--     Ordinal.IsLimit      -> Order.IsSuccLimit  (4 sites)
--     (n % 12).toReal      -> ((n % 12 : Nat) : Real)
--     `lambda` as a binder name -> beta   (a parse error, and never legal)
--     weight / applyG / simpleEmbedding / G6Ordinal marked noncomputable
-- Nothing in the mathematical content was changed: six admits before, six after.
--
-- The nine original imports were pinned to Mathlib v4.14.0 and do not all resolve
-- under the v4.32.0 that geometry has built.  Each was checked against the Mathlib
-- actually on disk at geometry/.lake/packages/mathlib rather than assumed:
--     Mathlib.Order.Ordinal.Basic          -> Mathlib.SetTheory.Ordinal.Basic
--     Mathlib.GroupTheory.DihedralGroup    -> Mathlib.GroupTheory.SpecificGroups.Dihedral
--     Mathlib.SetTheory.ClubFilter.Basic   -> absent, and not needed: this file defines
--     Mathlib.SetTheory.StationarySet.Basic   IsClubBelow / IsStationaryBelow itself
--     Mathlib.MeasureTheory.Measure.MeasureSpace -> dropped, unreferenced
--     Mathlib.Topology.MetricSpace.Basic         -> dropped, unreferenced
--
-- A bare `import Mathlib` was tried first and is version-independent, but it pulls the
-- whole library: minutes of cold load and several GB, which reads as a hang.  A narrow
-- import that is short a name fails in seconds with an unknown identifier, which is the
-- better failure.
import Mathlib.SetTheory.Ordinal.Basic
import Mathlib.Order.Cofinal
import Mathlib.SetTheory.Cardinal.Arithmetic
import Mathlib.SetTheory.Ordinal.FixedPoint
import Mathlib.Data.Matrix.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.GroupTheory.SpecificGroups.Dihedral

namespace TOGT

open Ordinal Cardinal Set

-- ============================================================================
-- PART A: CLUB FILTER AND STATIONARY SETS
-- ============================================================================

def IsUnboundedBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ β < α, ∃ γ < α, γ ∈ S ∧ β < γ

def IsOmegaClosedBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ c : ℕ → Ordinal,
    (∀ n, c n ∈ S) → (∀ n, c n < α) → StrictMono c →
    (⨆ n, c n) ∈ S

def IsClubBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  IsUnboundedBelow S α ∧ IsOmegaClosedBelow S α

def IsStationaryBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ C : Set Ordinal, IsClubBelow C α → ∃ β ∈ C, β ∈ S

def closurePointsBelow (α : Ordinal) : Set Ordinal :=
  { β | β < α ∧ Order.IsSuccLimit β }

theorem closurePoints_stationary_regular
    (α : Ordinal) (hreg : Order.IsSuccLimit α ∧ α.card.ord = α) :
    IsStationaryBelow (closurePointsBelow α) α := by
  intro C hC
  classical
  sorry  -- honest admit #5

-- ============================================================================
-- PART B–F: dm³ OPERATOR CHAIN & dm³ STRATA
-- ============================================================================

def η : ℝ := 1.839286755214161
noncomputable def weight (k : ℕ) : ℝ := (η : ℝ)⁻¹ ^ k

def PhaseVector := Fin 12 → ℝ

def P : Matrix (Fin 12) (Fin 12) ℝ :=
  Matrix.of (λ i j => if j = i + 1 then 1 else 0)

def orthogonalStepping (v : PhaseVector) : Prop :=
  ∀ i : Fin 12, v i * (Matrix.mulVec P v i) = 0

noncomputable def Z_even : ℝ :=
  ∑ k : Fin 6, weight (2 * k.val)

noncomputable def hexagonalEigenmode : PhaseVector :=
  fun i => if i.val % 2 = 0 then 1 / Real.sqrt Z_even else 0

def isCrystalSaturated (v : PhaseVector) : Prop :=
  Matrix.mulVec (P ^ 36) v = v ∧
  orthogonalStepping v ∧
  ∑ i, v i ^ 2 * weight i = 1

noncomputable def applyG (v : PhaseVector) : PhaseVector :=
  λ i => weight (i + 1) * (if i % 2 = 0 then v (i / 2) else 3 * v i + 1)

theorem crystal_lockin (v : PhaseVector) :
  ∃ m ≤ 33, isCrystalSaturated (applyG^[m] v) := by
  sorry

def D6 := DihedralGroup 6

def isEigenmodeLocked (v : PhaseVector) : Prop :=
  isCrystalSaturated v ∧ v = hexagonalEigenmode

theorem d6_lockin (v : PhaseVector) :
  ∃ m ≤ 33, isEigenmodeLocked (applyG^[m] v) := by
  sorry

def IsRegular (α : Ordinal) : Prop :=
  Order.IsSuccLimit α ∧ α.card.ord = α

def IsClub (C : Set Ordinal) (α : Ordinal) : Prop :=
  IsUnboundedBelow C α ∧ IsOmegaClosedBelow C α

def IsStationary (S : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ C : Set Ordinal, IsClub C α → ∃ β < α, β ∈ C ∧ β ∈ S

def closurePoints (α : Ordinal) : Set Ordinal :=
  {β | β < α ∧ Order.IsSuccLimit β}

noncomputable def G6Ordinal : Ordinal := Ordinal.omega0 ^ Ordinal.omega0

theorem g6_unconditional_closure (v : PhaseVector) :
  ∃ m ≤ 33, isCrystalSaturated (applyG^[m] v) ∧
    isEigenmodeLocked (applyG^[m] v) := by
  sorry

-- ============================================================================
-- PART G: COLlatZ BRIDGE
-- ============================================================================

def dm3Orbit (n : ℕ) (m : ℕ) : ℕ := Nat.iterate (fun k => if k % 2 = 0 then k / 2 else 3 * k + 1) m n

noncomputable def simpleEmbedding (n : ℕ) : PhaseVector :=
  fun i => if i.val % 2 = 0 then ((n % 12 : ℕ) : ℝ) / 12 else 0

theorem embedding_intertwining (n : ℕ) :
  ∃ m, applyG^[m] (simpleEmbedding n) = simpleEmbedding (dm3Orbit n m) := by
  sorry

theorem collatz_conjecture_via_dm3_gqm :
  ∀ n : ℕ, ∃ m : ℕ, dm3Orbit n m = 1 := by
  intro n
  sorry

-- ============================================================================
-- PART I: PRIORITY DOMAINS & NORMALIZATION FIX
-- ============================================================================

/-
Normalization fix for the hexagonal eigenmode
The earlier P^36 correction was valid: for a 12-cycle, the phase-advance matrix satisfies (P^{12} = I), hence (P^{36} = I), and the first condition in isCrystalSaturated,

(P ^ 36) v = v

is trivially satisfiable for any phase vector. That specific falsity is resolved.

However, d6_lockin and g6_unconditional_closure remained false for a different reason: the normalization condition in isCrystalSaturated failed for the original hexagonalEigenmode.
isCrystalSaturated requires:
∑_i v_i² · weight(i) = 1.
For

hexagonalEigenmode := fun i => if i % 2 = 0 then 1 else 0

the sum runs over even indices only:
∑_{k=0}^{5} 1² · η^{-2k} ≈ 1 + 0.296 + 0.088 + 0.026 + 0.008 + 0.002 ≈ 1.42 ≠ 1.
So isCrystalSaturated hexagonalEigenmode is false. Since

isEigenmodeLocked w := isCrystalSaturated w ∧ w = hexagonalEigenmode

no vector can satisfy it, and both d6_lockin and g6_unconditional_closure were false theorems.

The precise fix is to normalize the eigenmode on its even-index support:

noncomputable def Z_even : ℝ :=
  ∑ k : Fin 6, weight (2 * k.val)

noncomputable def hexagonalEigenmode : PhaseVector :=
  fun i => if i.val % 2 = 0 then 1 / Real.sqrt Z_even else 0

With this definition, the normalization condition
∑_i hexagonalEigenmode_i² · weight(i) = 1
holds by construction. The orthogonalStepping condition also holds: (P) shifts indices by 1, the eigenmode alternates nonzero/zero on even/odd indices, and thus (v_i · (Pv)_i = 0) for all i.
After this fix:

crystal_lockin — open (genuine dynamics question)
d6_lockin — open (no longer blocked by normalization)
g6_unconditional_closure — open
closurePoints_stationary_regular — open (standard ordinal argument)
collatz_conjecture_via_dm3_gqm — open (equivalent to Collatz)

embedding_intertwining — open (carries a sorry; omitted from the list above until 2026-08-28)

There are six honest open admits, none provably false. That is the correct and transparent
state for a public release. The count was five here until the kernel probe at the foot of
this file was run: it reports sorryAx on all six declarations, and embedding_intertwining
was the one this list did not name.
-/

end TOGT

/-
  KERNEL AUDIT. Compiling is not proving: `sorry` is a warning, not an error, so this
  file compiles whether or not anything in it is proved. These six lines ask the kernel
  what each theorem actually rests on.

  EXPECTED HERE: `sorryAx` on all six. That is not a failure — it is the file's own
  disclosure, confirmed. The header block claimed "five honest open admits" and named
  five; the sixth, `embedding_intertwining`, carries a `sorry` as well. Six is the
  number the kernel reports, and the header and the list above were corrected to six
  on 2026-08-28. Left here as the record of what the probe caught.

  Nothing in this file is a proved theorem. `η` is a `def` — a literal, not a result.

  ONE ASYMMETRY WORTH READING.  Five of the six report
      [propext, sorryAx, Classical.choice, Quot.sound]
  and `collatz_conjecture_via_dm3_gqm` reports `[sorryAx]` alone.  The other three
  axioms enter through the mathematical structure a statement actually touches --
  ordinals, reals, quotients.  A statement that reaches none of it, and whose proof
  is `sorry`, leaves the kernel nothing else to name.  That is what the bare
  `[sorryAx]` is telling you, and it is a stronger signal than the sorry itself.

  Run from the geometry repository root, which already has Mathlib built:
      cd ~/Desktop/geometry && lake env lean ~/Desktop/AXLE/main/AXLE_v8_1.lean
-/
#print axioms TOGT.closurePoints_stationary_regular
#print axioms TOGT.crystal_lockin
#print axioms TOGT.d6_lockin
#print axioms TOGT.g6_unconditional_closure
#print axioms TOGT.embedding_intertwining
#print axioms TOGT.collatz_conjecture_via_dm3_gqm
