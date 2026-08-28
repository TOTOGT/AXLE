/-!
# TripleAlphaDm3.lean

Chapter A of Principia Orthogona, Book 3: The Mini-Beast —
"Self-Regulation: Autophagy and the Triple-Alpha Process as dm³ Generative
Transitions". Companion to `AutophagyDm3.lean`, which carries the fold-geometry
side (Whitney A₁, Gronwall radius, μ = −2). This file carries the three-body side.

Chapter DOI: 10.5281/zenodo.20221723

Mathlib-free by construction: core Lean 4 only, so it can be checked by
`lean TripleAlphaDm3.lean` with no dependency fetch, and by `#print axioms` with
nothing but the three standard kernel axioms in scope.

## The claim being formalised

The triple-alpha process couples **three** α-particles: two form ⁸Be, and a third
is captured on the resonance before ⁸Be decays. The dm³ reading is that the fold
ladder for a three-body transition is the three-term recurrence

    w(k+3) = w(k+2) + w(k+1) + w(k)

whose characteristic root is the Tribonacci constant η ≈ 1.8393, sitting strictly
between the two-body constant φ ≈ 1.618 and the embodiment threshold τ = 2.

What is proved below is the **discrete, ordinal form of φ < η < τ**:

* `tribo_dominates_fibonacci_step` — each term strictly exceeds the sum of the two
  before it, which is the Fibonacci step. The three-body ladder outgrows the
  two-body one. (η > φ.)
* `tribo_lt_two_pow` — every term after the first is strictly below 2ⁿ. The ladder
  never reaches the doubling rate. (η < τ = 2.)

## What is NOT proved here — read this before citing the file

* Nothing here computes η itself. These are bounds on the integer sequence, not a
  statement about the root of x³ = x² + x + 1. The seven analytic proofs of η live
  in the TOGT deposit; this file does not reproduce or replace them.
* No physics is formalised. The Hoyle resonance energy, the ⁸Be lifetime, the
  reaction rate, and the effective contact form α_QCD appear nowhere below. The
  identification of the triple-alpha process with this recurrence is a modelling
  claim made in the chapter prose, and it is *not* a theorem of this file.
* `tribo` is a definition, not a result. Prose must not call it a theorem.

Bookkeeping note for whoever wires this up: a Lean file that is not a root of some
`[[lean_lib]]` target in `lakefile.toml` is never compiled by `lake build`, and so
is checked by nothing. Add a target before claiming this file is verified.
-/

namespace TripleAlphaDm3

/-- The three-term fold ladder. Seeded `1, 1, 2` so that every term is positive,
    which the bounds below depend on. -/
def tribo : Nat → Nat
  | 0 => 1
  | 1 => 1
  | 2 => 2
  | (n + 3) => tribo (n + 2) + tribo (n + 1) + tribo n

/-- The recurrence itself, definitionally. -/
theorem tribo_rec (n : Nat) :
    tribo (n + 3) = tribo (n + 2) + tribo (n + 1) + tribo n := rfl

/-- Every term is positive. Needed for both bounds; proved, not assumed. -/
theorem tribo_pos : ∀ n, 0 < tribo n
  | 0 => by decide
  | 1 => by decide
  | 2 => by decide
  | (n + 3) => by
      have h := tribo_pos (n + 2)
      rw [tribo_rec]
      omega

/-- **η > φ, in ordinal form.** Each term strictly exceeds the sum of the two
    preceding it — the Fibonacci step — because the three-body recurrence carries
    a third, strictly positive summand. -/
theorem tribo_dominates_fibonacci_step (n : Nat) :
    tribo (n + 2) + tribo (n + 1) < tribo (n + 3) := by
  have h := tribo_pos n
  rw [tribo_rec]
  omega

/-- Every term is bounded by 2ⁿ. -/
theorem tribo_le_two_pow : ∀ n, tribo n ≤ 2 ^ n
  | 0 => by decide
  | 1 => by decide
  | 2 => by decide
  | (n + 3) => by
      have h0 := tribo_le_two_pow n
      have h1 := tribo_le_two_pow (n + 1)
      have h2 := tribo_le_two_pow (n + 2)
      have e : (2 : Nat) ^ (n + 3) = 2 ^ n * 8 := by
        simp [Nat.pow_succ, Nat.mul_assoc]
      have e1 : (2 : Nat) ^ (n + 1) = 2 ^ n * 2 := by
        simp [Nat.pow_succ]
      have e2 : (2 : Nat) ^ (n + 2) = 2 ^ n * 4 := by
        simp [Nat.pow_succ, Nat.mul_assoc]
      rw [tribo_rec, e]
      rw [e1] at h1
      rw [e2] at h2
      omega

/-- **η < τ = 2, in ordinal form.** Past the first term the ladder is strictly
    below the doubling rate: it approaches the embodiment threshold τ = 2 from
    below and never attains it. -/
theorem tribo_lt_two_pow : ∀ n, 0 < n → tribo n < 2 ^ n
  | 0 => by omega
  | 1 => by intro _; decide
  | 2 => by intro _; decide
  | (n + 3) => by
      intro _
      have h0 := tribo_le_two_pow n
      have h1 := tribo_le_two_pow (n + 1)
      have h2 := tribo_le_two_pow (n + 2)
      have hp := tribo_pos n
      have e : (2 : Nat) ^ (n + 3) = 2 ^ n * 8 := by
        simp [Nat.pow_succ, Nat.mul_assoc]
      have e1 : (2 : Nat) ^ (n + 1) = 2 ^ n * 2 := by
        simp [Nat.pow_succ]
      have e2 : (2 : Nat) ^ (n + 2) = 2 ^ n * 4 := by
        simp [Nat.pow_succ, Nat.mul_assoc]
      rw [tribo_rec, e]
      rw [e1] at h1
      rw [e2] at h2
      omega

/-- The two bounds together: the ladder's step ratio is bracketed strictly between
    the Fibonacci step and doubling. This is the discrete content of φ < η < τ. -/
theorem tribo_bracketed (n : Nat) :
    tribo (n + 2) + tribo (n + 1) < tribo (n + 3) ∧ tribo (n + 3) < 2 ^ (n + 3) :=
  ⟨tribo_dominates_fibonacci_step n, tribo_lt_two_pow (n + 3) (by omega)⟩

-- Kernel gate. These must report exactly [propext, Classical.choice, Quot.sound]
-- — and in fact report fewer, since nothing here is classical.
#print axioms tribo_rec
#print axioms tribo_pos
#print axioms tribo_dominates_fibonacci_step
#print axioms tribo_le_two_pow
#print axioms tribo_lt_two_pow
#print axioms tribo_bracketed

end TripleAlphaDm3
