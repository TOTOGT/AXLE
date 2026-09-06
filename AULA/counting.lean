-- Zero Sorries · Session 4 · counting.lean
-- Count the word "sorry" in this file. Write your number down.
-- Then count it again a different way. Then a third way.

-- Claim 1. Adding a number to itself gives an even number.
theorem claim1 (n : Nat) : (n + n) % 2 = 0 := by
  omega

-- Claim 2. Every number is smaller than two raised to that number.
-- We have not proved this one, so it gets a sorry.
theorem claim2 (n : Nat) : n < 2 ^ n := by
  sorry

-- Claim 3. Four is not five.
theorem claim3 : 4 ≠ 5 := by
  decide

/- Claim 4. Two odd numbers added together give an even number.
   Someone proved this on paper last week but nobody typed it in,
   so for now it is a sorry. -/
theorem claim4 (a b : Nat) (ha : a % 2 = 1) (hb : b % 2 = 1) :
    (a + b) % 2 = 0 := by
  sorry

-- Claim 5. Zero is less than one.
theorem claim5 : 0 < 1 := by
  decide

/- Claim 6. Doubling a number and then halving it gives back the number.
   This is the one that took three tries. The first two attempts are in
   the notebook; a sorry holds the place until one of them works. -/
theorem claim6 (n : Nat) : (2 * n) / 2 = n := by
  sorry

-- Claim 7. A number plus zero is that number.
theorem claim7 (n : Nat) : n + 0 = n := by
  rfl

-- Claim 8. Every even number bigger than two is the sum of two primes.
-- Nobody has proved this. Not us, not anyone, since 1742.
-- No sorry will help here: we cannot even write the claim down yet.
-- That is session 8.
