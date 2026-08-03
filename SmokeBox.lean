import Mathlib

/-!
# Atmospheric box model — dilution law and commutation structure

Companion to the July 2026 Canadian-smoke-over-NYC case study.

**Scope discipline.** These are theorems *about a box model*, not claims about the
atmosphere. The July 2026 measurements are consistent with the model; they do not
establish it. Data stays [DATA], the model stays [MODEL], only what follows
necessarily from the definitions below is [VERIFIED].

* **T1** — box dilution: at fixed column burden, surface concentration is
  inversely proportional to mixed-layer depth. This is also what forbids reading
  physics into an empirical log-log slope when the burden is not held fixed.
* **T2** — commutation: the lid commutes exactly with any pointwise loss, but
  NOT with vertical transport. Surface-exposure order-dependence is carried by
  the operator that moves amplitude between layers — never by the lid alone.

T2 is the same structure as `ZeoliteCommutation.lean` in TOTOGT/io, reinstantiated
on a vertical column. That is the point: the algebra is domain-general, the
interpretation is domain-specific.
-/

-- ============================================================
-- T1 · Box dilution law
-- ============================================================

/-- Burden is conserved: concentration times depth returns the column burden. -/
theorem box_invariant (Q h : ℝ) (hh : 0 < h) : (Q / h) * h = Q :=
  div_mul_cancel₀ Q (ne_of_gt hh)

/-- **At fixed burden, a shallower mixed layer means strictly higher surface
concentration.** The exponent here is exactly −1; any empirically fitted slope
differing from −1 reflects a burden that was not held fixed, not new physics. -/
theorem shallower_is_worse (Q h₁ h₂ : ℝ) (hQ : 0 < Q) (h1 : 0 < h₁) (h12 : h₁ < h₂) :
    Q / h₂ < Q / h₁ :=
  div_lt_div_of_pos_left hQ h1 h12

-- ============================================================
-- T2 · Commutation on a 3-layer column
-- layer 0 = surface, 1 = mid, 2 = aloft
-- ============================================================

/-- Vertical mixing: moves amplitude BETWEEN adjacent layers. -/
def transport (v : Fin 3 → ℝ) : Fin 3 → ℝ := ![v 1, v 0 + v 2, v 1]

/-- Pointwise (sitewise) loss — second-order, as in coagulation. -/
def onsite (v : Fin 3 → ℝ) : Fin 3 → ℝ := fun i => (v i) ^ 2

/-- The lid: a 0/1 gate sealing off the layer aloft. -/
def lid (v : Fin 3 → ℝ) : Fin 3 → ℝ := ![v 0, v 1, 0]

/-- A test column with smoke present at all three levels. -/
def plume : Fin 3 → ℝ := ![2, 1, 1]

/-- **The lid commutes exactly with pointwise loss — for every column state.**
So a lid acting on a sitewise process cannot, by itself, produce order-dependence. -/
theorem lid_commutes_onsite (v : Fin 3 → ℝ) : lid (onsite v) = onsite (lid v) := by
  funext i
  fin_cases i <;> simp [lid, onsite]

/-- **Vertical transport does NOT commute with pointwise loss.**
At the mid layer: (2²) + (1²) = 5, but (2+1)² = 9. -/
theorem transport_not_commute : transport (onsite plume) ≠ onsite (transport plume) := by
  intro h
  have h1 := congrFun h 1
  simp [transport, onsite, plume] at h1
  norm_num at h1

/-- **The lid does NOT commute with the full fold `F = transport ∘ onsite`.**
Order-dependence enters only once the fold carries its transport term. -/
theorem lid_fold_not_commute :
    lid (transport (onsite plume)) ≠ transport (onsite (lid plume)) := by
  intro h
  have h2 := congrFun h 2
  simp [lid, transport, onsite, plume] at h2

#print axioms box_invariant
#print axioms shallower_is_worse
#print axioms lid_commutes_onsite
#print axioms transport_not_commute
#print axioms lid_fold_not_commute
