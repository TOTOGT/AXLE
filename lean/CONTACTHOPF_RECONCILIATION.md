# ContactHopf.lean — γ* reconciliation (RESOLVED)

**Date:** 2026-07-03 · **Status:** resolved, independently re-derived both ways.

## The apparent conflict

Two descriptions of the same V3→V4 fix seemed to point in opposite directions:

- **Raw algebra (audit):** the erroneous linearization
  `−2·(1 − γ·e^(−z₀)) = 2·γ·e^(−z₀) − 2` carries coefficient **2** on
  `γ·e^(−z₀)`; the correct linearization `γ·e^(−z₀) − 2` carries coefficient
  **1**. Going wrong→correct, the coefficient **decreases** 2→1.
- **Vol II V4 changelog:** `γ*` is corrected `e^(z₀) → 2·e^(z₀)` — an
  **increase**.

Decrease vs. increase looked like a contradiction. It is not.

## Resolution

The two statements describe **different quantities at different stages** of the
same derivation.

`γ*` is not the coefficient; it is the **root** of the eigenvalue (zero-crossing)
equation, i.e. the value of γ that makes the linearized term vanish. Solving each
equation for its root moves the coefficient into the **denominator**:

### Erroneous equation
```
2·γ·e^(−z₀) − 2 = 0
2·γ·e^(−z₀) = 2
γ = 1 / e^(−z₀) = e^(z₀)
```
Root: **γ* = e^(z₀)**.

### Correct equation
```
γ·e^(−z₀) − 2 = 0
γ·e^(−z₀) = 2
γ = 2 / e^(−z₀) = 2·e^(z₀)
```
Root: **γ* = 2·e^(z₀)**.

## Why both directions are correct simultaneously

| Quantity | Erroneous | Correct | Direction |
|---|---|---|---|
| Coefficient on γ in the eigenvalue equation | 2 | 1 | **down** (÷2) |
| Root γ* (= 2 / coefficient · … , coefficient in denominator) | e^(z₀) | 2·e^(z₀) | **up** (×2) |

The coefficient falls 2→1; because it sits in the denominator when solving for
the root, γ* rises by the reciprocal factor, e^(z₀) → 2·e^(z₀). Same fix, two
vantage points. **No contradiction.**

## Lean witnesses (proved in ContactHopf.lean)

- `erroneous_root_is_exp` : `2·(e^(z₀)·e^(−z₀)) − 2 = 0` — confirms e^(z₀) is
  the erroneous root.
- `gammaStar_is_root` : `linearizedHopfTerm z₀ (gammaStar z₀) = 0`, i.e.
  `(2·e^(z₀))·e^(−z₀) − 2 = 0` — confirms 2·e^(z₀) is the correct root.
- `linearization_erroneous_expansion`, `linearization_discrepancy` — the
  coefficient step (2→1) as `ring` identities.

Both root lemmas reduce to `e^(z₀)·e^(−z₀) = 1` (`Real.exp_add` + `neg_add`),
so they are elementary and hold with no sorry.

## Action taken

ContactHopf.lean's header "⚠ open reconciliation" warning has been replaced with
this resolution, and the two root lemmas above were added to encode it in Lean.
The changelog value (γ* = 2·e^(z₀)) and the corrected algebra are consistent.
