# ── §1: Substitution chain generation ───────────────────────────────────────
#
# Fibonacci substitution:   A→AB,  B→A          (letters encoded 0, 1)
# Tribonacci (Rauzy) sub.:  1→12,  2→13,  3→1   (letters encoded 0, 1, 2)
#
# Letter frequencies converge to the left Perron–Frobenius eigenvector of the
# companion matrix.  For tribonacci:
#   M = [[1,1,1],[1,0,0],[0,1,0]],  ρ(M) = η
#   (f_1, f_2, f_3) ≈ (0.5437, 0.2956, 0.1607)

def fibonacci_word(length):
    """
    Iterate A→AB, B→A until len ≥ length, then truncate.
    Returns list of ints: 0=A, 1=B.
    """
    word = [0]
    rules = {0: [0, 1], 1: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]

def tribonacci_word(length):
    """
    Rauzy substitution: 1→12, 2→13, 3→1.
    Returns list of ints: 0='1', 1='2', 2='3'.
    det(companion) = 1  →  T₃ ∈ SL(3,ℤ).
    """
    word = [0]
    rules = {0: [0, 1], 1: [0, 2], 2: [0]}
    while len(word) < length:
        word = [s for c in word for s in rules[c]]
    return word[:length]

# Quick sanity check
w_fib  = fibonacci_word(20)
w_trib = tribonacci_word(20)
print("Fibonacci (20)  :", w_fib)
print("Tribonacci (20) :", w_trib)

# Verify tribonacci letter frequencies approach PF eigenvector
N_long = 10000
wt = tribonacci_word(N_long)
f1 = wt.count(0)/N_long
f2 = wt.count(1)/N_long
f3 = wt.count(2)/N_long
print(f"\nTribonacci letter freqs (N={N_long}): "
      f"f1={f1:.4f} f2={f2:.4f} f3={f3:.4f}")
print(f"Expected (PF):  f1≈0.5437, f2≈0.2956, f3≈0.1607")
