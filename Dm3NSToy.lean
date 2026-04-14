import Mathlib.Data.Nat.Basic
import Mathlib.Init.Function

/-!
# Toy Navier–Stokes via discrete energy dissipation (Kakeya-style, fully proved)

This is a **toy dm³_ns** pillar:

- State space: a natural number `energy` representing the total kinetic
  energy of a finite fluid system on a toy grid.
- Contact / flow: a toy "NS step" that dissipates energy by 1 per step
  until reaching the rest state (energy = 0).
- C/K/F/U: operator grammar instantiated in the simplest nontrivial way.
- Theorem: every NSState flows to `nsAttractor` (energy = 0, the rest state)
  under iteration of `nsStep`.

This is NOT a proof of Navier–Stokes global regularity.  It is a
**Kakeya-style verified fragment** that closes the generative arc in the
toy PDE/flow setting and provides a fully formalized M → E entropy chain
for this pillar class.

The toy captures the essential dm³ semantics of Navier–Stokes:
  C = energy compression (viscous dissipation reduces kinetic energy)
  K = curvature (velocity-field curvature drives the dissipation rate)
  F = folding (nonlinear mode-coupling / vorticity stretching; identity here)
  U = unfolding (emergence of coherent structure / attractor; identity here)

sorry_count: 0
-/

namespace Dm3NSToy

/-! ## State space -/

/-- A toy NS state: a natural number representing total kinetic energy on
    a finite grid.  In the real theory this would be an H^s norm of the
    velocity field; here we track only the energy scalar. -/
structure NSState where
  energy : ℕ
  deriving DecidableEq

/-- The canonical attractor: the rest state with zero kinetic energy.
    Semantics: the fluid has fully dissipated and come to rest. -/
def nsAttractor : NSState := ⟨0⟩

/-- Simply-connected predicate (toy version: always true in this model). -/
def isSimplyConnected (_X : NSState) : Prop := True

/-! ## Operator grammar -/

/-- dm³ operator grammar: identical across all pillars. -/
inductive Dm3Op
  | C | K | F | U
  deriving DecidableEq, Repr

open Dm3Op

/-- TOGT composite operator: U ∘ F ∘ K ∘ C. -/
def G {α} (C K F U : α → α) : α → α :=
  U ∘ F ∘ K ∘ C

/-- C_ns: energy compression via viscous dissipation — decrease energy by 1,
    floor at 0.
    Semantics: one unit of kinetic energy is converted to heat by viscosity.
    In the full theory this corresponds to the -ν Δu dissipation term. -/
def C_ns (X : NSState) : NSState :=
  ⟨X.energy - 1⟩

/-- K_ns: curvature of the velocity field — identity in this toy model.
    Semantics: in the full theory K encodes the Laplacian / vorticity
    curvature that drives the dissipation rate; here neutral. -/
def K_ns (X : NSState) : NSState := X

/-- F_ns: nonlinear folding (mode-coupling / vorticity stretching) —
    identity in this toy model.
    Semantics: in the full theory F captures the (u · ∇)u nonlinearity
    and energy cascade across scales; here neutral. -/
def F_ns (X : NSState) : NSState := X

/-- U_ns: unfolding to coherent attractor — identity in this toy model.
    Semantics: in the full theory U describes the emergence of the laminar
    or structured attractor from the transient flow; here neutral. -/
def U_ns (X : NSState) : NSState := X

/-- One step of the toy NS flow: pure energy dissipation (C only).
    K, F, U are identities so the composite reduces to C_ns. -/
def nsStep (X : NSState) : NSState :=
  C_ns X

/-! ## Operator decomposition -/

/-- nsStep factors as G C_ns K_ns F_ns U_ns.
    Proof: K, F, U are identities, so G reduces to C_ns. -/
theorem ns_operatorDecomposition :
    ∀ X, nsStep X = (G C_ns K_ns F_ns U_ns) X :=
  fun _ => rfl

/-! ## Core iteration lemma -/

/-- Iterating nsStep k times subtracts k from energy, floored at 0.
    This is the toy analogue of the energy inequality:
      ‖u(t)‖² + 2ν ∫₀ᵗ ‖∇u‖² ds ≤ ‖u₀‖²
    In the toy, energy decreases by exactly 1 per step. -/
lemma iterate_nsStep_energy (X : NSState) (k : ℕ) :
    (nsStep^[k] X).energy = X.energy - k := by
  induction k generalizing X with
  | zero =>
    simp [Function.iterate_zero, Nat.sub_zero]
  | succ k ih =>
    rw [Function.iterate_succ', Function.comp]
    simp only [nsStep, C_ns]
    rw [ih ⟨X.energy - 1⟩]
    omega

/-! ## Convergence to attractor -/

/-- After exactly `energy` steps every NSState reaches nsAttractor.
    This is the toy analogue of global regularity: the flow always
    reaches the rest state in finite time. -/
lemma iterate_to_attractor (X : NSState) :
    nsStep^[X.energy] X = nsAttractor := by
  apply NSState.ext
  simp only [nsAttractor]
  rw [iterate_nsStep_energy]
  omega

/-! ## Main convergence theorem -/

/-- **Toy Navier–Stokes convergence.**
    Every simply-connected NSState flows to `nsAttractor`
    under iteration of `nsStep`.

    This is the verified toy analogue of Navier–Stokes global regularity:
    in this finite dissipative model, every initial energy state reaches
    the rest state in finite time, with no blow-up possible. -/
theorem ns_toy_converges
    (X : NSState) (_hX : isSimplyConnected X) :
    ∃ k : ℕ, nsStep^[k] X = nsAttractor :=
  ⟨X.energy, iterate_to_attractor X⟩

/-! ## Entropy chain (M and E) -/

/-- M_ns: entropic boundary — true when the flow has nowhere left to go.
    Semantics: all kinetic energy has been dissipated; no further viscous
    compression is possible.  This is the toy analogue of the question
    "has the solution reached its final state?" -/
def M_ns (X : NSState) : Prop := X.energy = 0

/-- E_ns: stability detector — true when X has reached the canonical
    attractor (the rest state).
    Semantics: the flow has converged to the laminar rest state. -/
def E_ns (X : NSState) : Prop := X = nsAttractor

/-- E_ns detects exactly nsAttractor. -/
theorem E_ns_iff_attractor (X : NSState) :
    E_ns X ↔ X = nsAttractor := by rfl

/-- M_ns and E_ns coincide on this model:
    "no energy left" ↔ "rest state reached". -/
theorem M_ns_iff_E_ns (X : NSState) :
    M_ns X ↔ E_ns X := by
  simp [M_ns, E_ns, nsAttractor, NSState.ext_iff]

/-- Perelman-style monotonicity (energy inequality):
    energy strictly decreases at every step until M_ns.
    This is the toy analogue of the energy dissipation inequality:
    as long as the system has nonzero energy, each NS step
    strictly decreases it. -/
theorem entropy_monotone (X : NSState) (h : ¬ M_ns X) :
    (nsStep X).energy < X.energy := by
  simp [nsStep, C_ns, M_ns] at *
  omega

/-! ## Additional structural lemma: energy is bounded -/

/-- Energy is bounded above by the initial value for all iterates.
    This is the toy analogue of the Leray energy bound:
      ‖u(t)‖² ≤ ‖u₀‖²  for all t ≥ 0. -/
lemma energy_bounded (X : NSState) (k : ℕ) :
    (nsStep^[k] X).energy ≤ X.energy := by
  rw [iterate_nsStep_energy]
  omega

/-! ## Sanity checks -/

#check @ns_toy_converges
-- NSState → isSimplyConnected X → ∃ k, nsStep^[k] X = nsAttractor

example : nsStep^[5] ⟨5⟩ = nsAttractor :=
  iterate_to_attractor ⟨5⟩

example : nsStep^[0] ⟨0⟩ = nsAttractor :=
  iterate_to_attractor ⟨0⟩

example : nsStep^[10] ⟨10⟩ = nsAttractor :=
  iterate_to_attractor ⟨10⟩

example : (nsStep^[3] ⟨7⟩).energy = 4 := by
  simp [iterate_nsStep_energy]

end Dm3NSToy
