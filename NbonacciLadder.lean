/-!
# NbonacciLadder.lean

The n-bonacci ladder φ → η → Δ → Σ → Ω, and its bound by the embodiment
threshold τ = 2, as one theorem rather than seven.

Companion to `TripleAlphaDm3.lean`, which is the k = 3 case worked concretely.
Mathlib-free: core Lean 4 only.

## What is proved

For **every** k and **every** sequence `a : ℕ → ℕ` satisfying the k-term
recurrence

    a (n + k) = a n + a (n+1) + … + a (n+k−1)

with seeds bounded by `a i ≤ 2^i` for `i < k`:

* `nbonacci_le_two_pow` — `a n ≤ 2 ^ n` for every n.
* `nbonacci_lt_two_pow` — `a (m + k) < 2 ^ (m + k)`: strict once the recurrence
  has fired at least once.

The bound is quantified over sequences, not proved for a construction. That is
what makes it a statement about the ladder rather than about one member of it:
Fibonacci (k = 2), Tribonacci (k = 3), Tetranacci (k = 4), and every k beyond
are instances of the same theorem, and each characteristic root η_k therefore
satisfies η_k < 2 = τ.

The slack is exact and visible in `sumPow_succ`: the k-term window sums to
`2^(m+k) − 2^m`, so the deficit from the threshold is `2^m` — a fixed fraction
`2^{-k}` of the bound. As k grows the fraction shrinks, which is the ordinal form
of η_k increasing toward τ. The ladder approaches the threshold and does not
reach it, at any k.

## What is NOT proved here

* Nothing about the real characteristic root itself. These are bounds on integer
  sequences; that η_k is the root of x^k = x^{k−1} + … + 1, and that η_k → 2, are
  analytic statements this file does not make.
* No claim that any physical system realises the k-term recurrence. That
  identification is made in the chapter prose and is not a theorem.
-/

namespace NbonacciLadder

/-- `sumPrev a n k = a n + a (n+1) + … + a (n+k−1)`, the k-term window. -/
def sumPrev (a : Nat → Nat) (n : Nat) : Nat → Nat
  | 0 => 0
  | (j + 1) => a (n + j) + sumPrev a n j

/-- The window is monotone in the sequence, pointwise over its own span. -/
theorem sumPrev_mono (a b : Nat → Nat) (n : Nat) :
    ∀ k, (∀ i, i < k → a (n + i) ≤ b (n + i)) → sumPrev a n k ≤ sumPrev b n k
  | 0, _ => by simp [sumPrev]
  | (k + 1), h => by
      have hk : sumPrev a n k ≤ sumPrev b n k :=
        sumPrev_mono a b n k (fun i hi => h i (Nat.lt_succ_of_lt hi))
      have hlast : a (n + k) ≤ b (n + k) := h k (Nat.lt_succ_self k)
      simp only [sumPrev]
      omega

/-- The window of the doubling sequence, exactly: `2^n + … + 2^(n+k−1) + 2^n = 2^(n+k)`.
    Stated without subtraction so it holds in `Nat` without side conditions. -/
theorem sumPow_succ (m : Nat) :
    ∀ k, sumPrev (fun i => 2 ^ i) m k + 2 ^ m = 2 ^ (m + k)
  | 0 => by simp [sumPrev]
  | (k + 1) => by
      have ih := sumPow_succ m k
      have e : (2 : Nat) ^ (m + (k + 1)) = 2 ^ (m + k) + 2 ^ (m + k) := by
        rw [show m + (k + 1) = (m + k) + 1 from rfl, Nat.pow_succ]
        omega
      simp only [sumPrev]
      omega

/-- Positivity of the doubling sequence, proved rather than imported: the library
    name for this has moved between Lean versions, and this file depends on no
    library API. -/
theorem two_pow_pos : ∀ m : Nat, 0 < 2 ^ m
  | 0 => by decide
  | (m + 1) => by
      have ih := two_pow_pos m
      rw [Nat.pow_succ]
      omega

/-- The doubling window is strictly below the next power: the deficit is `2^m`. -/
theorem sumPow_lt (m k : Nat) : sumPrev (fun i => 2 ^ i) m k < 2 ^ (m + k) := by
  have h := sumPow_succ m k
  have hp := two_pow_pos m
  omega

/-- Strong induction, self-contained so this file depends on no library API. -/
theorem strong_ind (P : Nat → Prop) (H : ∀ n, (∀ j, j < n → P j) → P n) : ∀ n, P n := by
  have aux : ∀ N n, n < N → P n := by
    intro N
    induction N with
    | zero => intro n hn; exact absurd hn (Nat.not_lt_zero n)
    | succ N ih =>
        intro n hn
        exact H n (fun j hj => ih j (by omega))
  intro n
  exact aux (n + 1) n (Nat.lt_succ_self n)

/-- **The ladder bound.** Every sequence obeying the k-term recurrence with seeds
    under the doubling sequence stays under the doubling sequence forever. This is
    η_k < 2 = τ, for every k at once. -/
theorem nbonacci_le_two_pow
    (k : Nat) (a : Nat → Nat)
    (hseed : ∀ i, i < k → a i ≤ 2 ^ i)
    (hrec : ∀ n, a (n + k) = sumPrev a n k) :
    ∀ n, a n ≤ 2 ^ n := by
  refine strong_ind (fun n => a n ≤ 2 ^ n) ?_
  intro n IH
  by_cases hlt : n < k
  · exact hseed n hlt
  · have hk : k ≤ n := Nat.not_lt.mp hlt
    obtain ⟨m, hm⟩ : ∃ m, n = m + k := ⟨n - k, by omega⟩
    subst hm
    have hprev : ∀ i, i < k → a (m + i) ≤ 2 ^ (m + i) := by
      intro i hi
      exact IH (m + i) (by omega)
    have h1 : sumPrev a m k ≤ sumPrev (fun i => 2 ^ i) m k :=
      sumPrev_mono a (fun i => 2 ^ i) m k hprev
    have h2 := sumPow_lt m k
    rw [hrec m]
    omega

/-- **Strictness.** Once the recurrence has fired, the bound is strict: the ladder
    is below the threshold, not merely at it. -/
theorem nbonacci_lt_two_pow
    (k : Nat) (a : Nat → Nat)
    (hseed : ∀ i, i < k → a i ≤ 2 ^ i)
    (hrec : ∀ n, a (n + k) = sumPrev a n k) :
    ∀ m, a (m + k) < 2 ^ (m + k) := by
  intro m
  have hprev : ∀ i, i < k → a (m + i) ≤ 2 ^ (m + i) := fun i _ =>
    nbonacci_le_two_pow k a hseed hrec (m + i)
  have h1 : sumPrev a m k ≤ sumPrev (fun i => 2 ^ i) m k :=
    sumPrev_mono a (fun i => 2 ^ i) m k hprev
  have h2 := sumPow_lt m k
  rw [hrec m]
  omega

/-- The k = 3 instance: the Tribonacci ladder of the triple-alpha coupling.
    Same theorem, no new proof. -/
theorem tribonacci_lt_two_pow
    (a : Nat → Nat)
    (hseed : ∀ i, i < 3 → a i ≤ 2 ^ i)
    (hrec : ∀ n, a (n + 3) = a n + a (n + 1) + a (n + 2)) :
    ∀ m, a (m + 3) < 2 ^ (m + 3) := by
  refine nbonacci_lt_two_pow 3 a hseed ?_
  intro n
  rw [hrec n]
  simp [sumPrev]
  omega

/-! ## A witness, so the quantifier is not vacuous

A theorem quantified over all sequences says nothing if no sequence satisfies its
hypotheses. `trib3` is a concrete inhabitant: the Tribonacci ladder seeded 1, 2, 4,
which is the doubling sequence on its seeds and strictly under it thereafter.
-/

/-- Tribonacci with doubling seeds. -/
def trib3 : Nat → Nat
  | 0 => 1
  | 1 => 2
  | 2 => 4
  | (n + 3) => trib3 n + trib3 (n + 1) + trib3 (n + 2)

theorem trib3_seed : ∀ i, i < 3 → trib3 i ≤ 2 ^ i := by
  intro i hi
  match i, hi with
  | 0, _ => decide
  | 1, _ => decide
  | 2, _ => decide

theorem trib3_rec (n : Nat) : trib3 (n + 3) = trib3 n + trib3 (n + 1) + trib3 (n + 2) := rfl

/-- The hypotheses are satisfiable, and the general theorem applies to this
    instance with no proof of its own. -/
theorem trib3_lt_two_pow (m : Nat) : trib3 (m + 3) < 2 ^ (m + 3) :=
  tribonacci_lt_two_pow trib3 trib3_seed trib3_rec m

-- 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927 — ratio → η ≈ 1.8393.
#eval (List.range 12).map trib3

/-! ## The hypotheses are load-bearing

`hseed` and `hrec` do not appear in the conclusions above, which is what an
idle-binder scan flags and cannot resolve on its own: a hypothesis in the binder
list may be doing the work, or may be constraining nothing. Here it is settled by
proof. Drop either one and the statement is false.
-/

/-- Without the recurrence, the bound fails: a sequence may satisfy the seed
    condition and still overshoot immediately. -/
theorem hrec_is_necessary :
    ¬ (∀ (k : Nat) (a : Nat → Nat),
        (∀ i, i < k → a i ≤ 2 ^ i) → ∀ n, a n ≤ 2 ^ n) := by
  intro h
  have hs : ∀ i, i < 1 → (fun n => if n = 0 then 1 else 4) i ≤ 2 ^ i := by
    intro i hi
    have : i = 0 := by omega
    subst this
    decide
  have := h 1 (fun n => if n = 0 then 1 else 4) hs 1
  exact absurd this (by decide)

/-- Without the seed bound, the bound fails: the constant sequence 3 obeys the
    one-term recurrence and exceeds 2⁰. -/
theorem hseed_is_necessary :
    ¬ (∀ (k : Nat) (a : Nat → Nat),
        (∀ n, a (n + k) = sumPrev a n k) → ∀ n, a n ≤ 2 ^ n) := by
  intro h
  have hr : ∀ n, (fun _ => 3) (n + 1) = sumPrev (fun _ => 3) n 1 := by
    intro n
    simp [sumPrev]
  have := h 1 (fun _ => 3) hr 0
  exact absurd this (by decide)

-- Kernel gate.
#print axioms strong_ind
#print axioms sumPrev_mono
#print axioms sumPow_succ
#print axioms two_pow_pos
#print axioms sumPow_lt
#print axioms nbonacci_le_two_pow
#print axioms nbonacci_lt_two_pow
#print axioms tribonacci_lt_two_pow
#print axioms trib3_lt_two_pow
#print axioms hrec_is_necessary
#print axioms hseed_is_necessary

end NbonacciLadder
