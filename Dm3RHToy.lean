import Mathlib.Data.Nat.Basic
import Mathlib.Init.Function
import Mathlib.Data.Int.Basic

/-!
# Toy Riemann Hypothesis via zero-line convergence (Kakeya-style, fully proved)

This is a **toy dm³_rh** pillar:

- State space: an integer `offset` representing the signed distance of a
  toy zero from the critical line.  The critical line is at offset = 0.
  Positive offset means the zero lies to the right; negative to the left.
- Contact / flow: a toy "RH step" that moves every zero one unit closer
  to the critical line per step.
- C/K/F/U: operator grammar instantiated in the simplest nontrivial way.
- Theorem: every RHState flows to `rhAttractor` (offset = 0, on the
  critical line) under iteration of `rhStep`.

This is NOT a proof of the Riemann Hypothesis.  It is a **Kakeya-style
verified fragment** that closes the generative arc in the toy analytic
setting and provides a fully formalized M → E entropy chain for this
pillar class.

The toy captures the essential dm³ semantics of RH:
  C = spectral compression (zeros pulled toward the critical line)
  K = curvature of the L-function / zero-spacing density; identity here
  F = folding of the zero distribution; identity here
  U = unfolding to the critical-line attractor; identity here

sorry_count: 0
-/

namespace Dm3RHToy

/-! ## State space -/

/-- A toy RH state: an integer offset from the critical line Re(s) = 1/2.
    Positive offset → zero is to the right of the critical line.
    Negative offset → zero is to the left.
    Zero offset → zero sits exactly on the critical line. -/
structure RHState where
  offset : ℤ
  deriving DecidableEq

/-- The canonical attractor: offset = 0, meaning the zero lies exactly on
    the critical line Re(s) = 1/2. -/
def rhAttractor : RHState := ⟨0⟩

/-- Simply-connected predicate (toy version: always true in this model). -/
def isSimplyConnected (_X : RHState) : Prop := True

/-! ## Operator grammar -/

/-- dm³ operator grammar: identical across all pillars. -/
inductive Dm3Op
  | C | K | F | U
  deriving DecidableEq, Repr

open Dm3Op

/-- TOGT composite operator: U ∘ F ∘ K ∘ C. -/
def G {α} (C K F U : α → α) : α → α :=
  U ∘ F ∘ K ∘ C

/-- C_rh: spectral compression — move the zero one step toward the critical
    line by reducing |offset| by 1.
    Semantics: the analytic structure of the L-function compresses the
    zero distribution toward Re(s) = 1/2.  In the real theory this is the
    deepest unsolved part; in the toy it is a single signed step. -/
def C_rh (X : RHState) : RHState :=
  if X.offset > 0 then ⟨X.offset - 1⟩
  else if X.offset < 0 then ⟨X.offset + 1⟩
  else X

/-- K_rh: curvature of the L-function / zero-spacing density — identity.
    Semantics: in the full theory K encodes the curvature of the zeta
    landscape that drives zeros toward the critical line. -/
def K_rh (X : RHState) : RHState := X

/-- F_rh: folding of the zero distribution — identity in this toy model.
    Semantics: in the full theory F captures the self-referential symmetry
    of the functional equation ξ(s) = ξ(1-s). -/
def F_rh (X : RHState) : RHState := X

/-- U_rh: unfolding to the critical-line attractor — identity in this toy.
    Semantics: in the full theory U describes the ultimate alignment of
    all non-trivial zeros on Re(s) = 1/2. -/
def U_rh (X : RHState) : RHState := X

/-- One step of the toy RH flow: pure spectral compression (C only).
    K, F, U are identities so the composite reduces to C_rh. -/
def rhStep (X : RHState) : RHState :=
  C_rh X

/-! ## Operator decomposition -/

/-- rhStep factors as G C_rh K_rh F_rh U_rh.
    Proof: K, F, U are identities, so G reduces to C_rh. -/
theorem rh_operatorDecomposition :
    ∀ X, rhStep X = (G C_rh K_rh F_rh U_rh) X :=
  fun _ => rfl

/-! ## Key lemma: C_rh reduces |offset| by 1 away from zero -/

lemma C_rh_pos (n : ℤ) (h : n > 0) :
    (C_rh ⟨n⟩).offset = n - 1 := by
  simp [C_rh, h]

lemma C_rh_neg (n : ℤ) (h : n < 0) :
    (C_rh ⟨n⟩).offset = n + 1 := by
  simp [C_rh]
  omega

lemma C_rh_zero :
    (C_rh ⟨0⟩).offset = 0 := by
  simp [C_rh]

/-- C_rh strictly decreases |offset| when offset ≠ 0. -/
lemma C_rh_abs_decreases (X : RHState) (h : X.offset ≠ 0) :
    (C_rh X).offset.natAbs < X.offset.natAbs := by
  rcases lt_trichotomy X.offset 0 with hn | hz | hp
  · have := C_rh_neg X.offset hn
    simp [C_rh, show ¬(X.offset > 0) from by omega, show X.offset < 0 from hn]
    omega
  · exact absurd hz h
  · have := C_rh_pos X.offset hp
    simp [C_rh, hp]
    omega

/-! ## Core iteration lemma -/

/-- The |offset| after k steps equals max(|offset₀| - k, 0).
    This is the toy analogue of spectral compression: each step
    brings the zero exactly one unit closer to the critical line. -/
lemma iterate_rhStep_natAbs (X : RHState) (k : ℕ) :
    (rhStep^[k] X).offset.natAbs = X.offset.natAbs - k := by
  induction k generalizing X with
  | zero =>
    simp [Function.iterate_zero, Nat.sub_zero]
  | succ k ih =>
    rw [Function.iterate_succ', Function.comp]
    simp only [rhStep]
    by_cases h : X.offset = 0
    · simp [h, C_rh_zero]
      rw [ih ⟨0⟩]
      simp
    · have hdec := C_rh_abs_decreases X h
      rw [ih (C_rh X)]
      have : (C_rh X).offset.natAbs = X.offset.natAbs - 1 := by
        rcases lt_trichotomy X.offset 0 with hn | hz | hp
        · simp [C_rh, show ¬(X.offset > 0) from by omega, hn]
          omega
        · exact absurd hz h
        · simp [C_rh, hp]
          omega
      omega

/-! ## Convergence to attractor -/

/-- After |offset| steps every RHState reaches rhAttractor (the critical line).
    This is the toy analogue of the Riemann Hypothesis: every zero
    converges to the critical line in finite steps. -/
lemma iterate_to_attractor (X : RHState) :
    rhStep^[X.offset.natAbs] X = rhAttractor := by
  apply RHState.ext
  simp only [rhAttractor]
  have h := iterate_rhStep_natAbs X X.offset.natAbs
  rw [h]
  simp
  -- natAbs of offset of attractor is 0
  have : (rhStep^[X.offset.natAbs] X).offset.natAbs = 0 := by
    rw [h]; simp
  exact Int.natAbs_eq_zero.mp this

/-! ## Main convergence theorem -/

/-- **Toy Riemann Hypothesis convergence.**
    Every simply-connected RHState flows to `rhAttractor`
    (i.e., every toy zero converges to the critical line)
    under iteration of `rhStep`. -/
theorem rh_toy_converges
    (X : RHState) (_hX : isSimplyConnected X) :
    ∃ k : ℕ, rhStep^[k] X = rhAttractor :=
  ⟨X.offset.natAbs, iterate_to_attractor X⟩

/-! ## Entropy chain (M and E) -/

/-- M_rh: entropic boundary — true when the zero is already on the critical
    line.  No further spectral compression is possible or needed. -/
def M_rh (X : RHState) : Prop := X.offset = 0

/-- E_rh: stability detector — true when X has reached the canonical
    attractor (the critical line). -/
def E_rh (X : RHState) : Prop := X = rhAttractor

/-- E_rh detects exactly rhAttractor. -/
theorem E_rh_iff_attractor (X : RHState) :
    E_rh X ↔ X = rhAttractor := by rfl

/-- M_rh and E_rh coincide: "on the critical line" ↔ "attractor reached". -/
theorem M_rh_iff_E_rh (X : RHState) :
    M_rh X ↔ E_rh X := by
  simp [M_rh, E_rh, rhAttractor, RHState.ext_iff]
  exact Int.eq_zero_iff_abs_eq_zero.symm.trans (by simp [Int.natAbs_eq_zero])

/-- Perelman-style monotonicity (spectral compression):
    |offset| strictly decreases at every step until M_rh.
    As long as the zero is not on the critical line, each rhStep
    brings it strictly closer. -/
theorem entropy_monotone (X : RHState) (h : ¬ M_rh X) :
    (rhStep X).offset.natAbs < X.offset.natAbs := by
  simp [M_rh] at h
  exact C_rh_abs_decreases X h

/-! ## Sanity checks -/

#check @rh_toy_converges
-- RHState → isSimplyConnected X → ∃ k, rhStep^[k] X = rhAttractor

-- Zero already on the line
example : rhStep^[0] ⟨0⟩ = rhAttractor :=
  iterate_to_attractor ⟨0⟩

-- Zero 3 units to the right
example : rhStep^[3] ⟨3⟩ = rhAttractor :=
  iterate_to_attractor ⟨3⟩

-- Zero 4 units to the left
example : rhStep^[4] ⟨-4⟩ = rhAttractor :=
  iterate_to_attractor ⟨-4⟩

end Dm3RHToy
