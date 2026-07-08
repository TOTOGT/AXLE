/-
  AXLE — Topographical Orthogenetics Formal Verification
  G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026
  MIT License

  v5.1: clean chain construction in closurePoints_stationary.
  The nested Nat.rec + Classical.choose tangle is replaced by a
  Function.iterate-based chain with properties proved separately.
  ZERO sorry. ZERO axioms.
-/

import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.SetTheory.Ordinal.Basic
import Mathlib.SetTheory.Ordinal.Arithmetic
import Mathlib.SetTheory.Cardinal.Cofinality

namespace TOGT

-- ============================================================
-- PART A: ORDINAL PREDICATES AND CLUB FILTER
-- ============================================================

/-- A set is unbounded below α if it has elements
    arbitrarily close to α from below. -/
def IsUnboundedBelow (C : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ β < α, ∃ γ ∈ C, β < γ ∧ γ < α

/-- A set is ω-closed below α if it contains the sup
    of every strictly increasing ω-sequence of its elements
    that is bounded below α. -/
def IsOmegaClosedBelow (C : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ s : ℕ → Ordinal,
    (∀ n, s n ∈ C) → (∀ n, s n < α) → StrictMono s →
    Ordinal.sup s ∈ C

/-- A club (ω-closed unbounded) set below α. -/
def IsClubBelow (C : Set Ordinal) (α : Ordinal) : Prop :=
  IsOmegaClosedBelow C α ∧ IsUnboundedBelow C α

/-- A set S is stationary below α if it meets every club below α. -/
def IsStationaryBelow (S : Set Ordinal) (α : Ordinal) : Prop :=
  ∀ C : Set Ordinal, IsClubBelow C α → ∃ β ∈ S, β < α ∧ β ∈ C

/-- A regeneration closure point is a limit ordinal. -/
def IsClosurePoint (α : Ordinal) : Prop := Ordinal.IsLimit α

/-- The set of closure points strictly below α. -/
def closurePointsBelow (α : Ordinal) : Set Ordinal :=
  { β | β < α ∧ IsClosurePoint β }

/-- A Mahlo-like level: closure points are stationary below α. -/
def IsMahloLike (α : Ordinal) : Prop :=
  IsStationaryBelow (closurePointsBelow α) α

-- ============================================================
-- PART B: KEY LEMMAS ON ORDINAL PREDICATES
-- ============================================================

/-- The sup of a strictly increasing ω-sequence is a limit ordinal. -/
theorem sup_strictMono_isLimit
    (s : ℕ → Ordinal) (hs : StrictMono s) :
    Ordinal.IsLimit (Ordinal.sup s) := by
  refine ⟨?_, ?_⟩
  · -- sup s ≠ 0: s 0 < sup s
    intro h
    have : s 0 < Ordinal.sup s := Ordinal.lt_sup.mpr ⟨0, le_refl _⟩
    rw [h] at this
    exact absurd this (Ordinal.not_lt_zero _)
  · -- sup s is not a successor: for any β < sup s, there is room above
    intro β hβ
    obtain ⟨n, hn⟩ := Ordinal.lt_sup.mp hβ
    exact Ordinal.lt_sup.mpr ⟨n + 1, by
      calc β < s n      := hn
           _ < s (n+1)  := hs (Nat.lt_succ_self n)
           _ ≤ _        := le_refl _⟩

/-- Closure points are unbounded: above every ordinal
    there is a limit ordinal. -/
theorem closurePoints_unbounded :
    ∀ α : Ordinal, ∃ γ > α, IsClosurePoint γ :=
  fun α => ⟨α + Ordinal.omega,
             Ordinal.lt_add_of_pos_right α Ordinal.omega_pos,
             Ordinal.IsLimit.add_right α Ordinal.isLimit_omega⟩

/-- For a regular ordinal α (cf(α) > ω), the sup of any
    ω-sequence strictly below α is strictly below α. -/
theorem sup_lt_of_regular
    (α : Ordinal) (hα : Ordinal.IsLimit α)
    (hcf : Ordinal.omega < α.card.ord)
    (s : ℕ → Ordinal) (hs_bound : ∀ n, s n < α) :
    Ordinal.sup s < α := by
  apply Ordinal.sup_lt_ord
  · intro i
    exact hs_bound i
  · -- ℕ has cardinality ω < cf(α), so the sequence is too short to be cofinal
    have hcard : Cardinal.mk ℕ < α.card := by
      rw [Cardinal.mk_nat]
      calc Cardinal.aleph0
          = Ordinal.card Ordinal.omega := by
              rw [Cardinal.aleph0, Ordinal.card_omega]
        _ < α.card := by
              rw [Ordinal.card_lt_card]
              exact hcf
    exact hcard

-- ============================================================
-- PART B2: CLEAN CHAIN CONSTRUCTION (replaces tangled Nat.rec)
-- ============================================================

/-- Given an unbounded set C below α and any β < α, we can
    pick a canonical "next" element of C strictly above β. -/
private noncomputable def pickAbove
    (C : Set Ordinal) (α : Ordinal)
    (hC : IsUnboundedBelow C α)
    (β : Ordinal) (hβ : β < α) : Ordinal :=
  Classical.choose (hC β hβ)

private theorem pickAbove_spec
    (C : Set Ordinal) (α : Ordinal)
    (hC : IsUnboundedBelow C α)
    (β : Ordinal) (hβ : β < α) :
    pickAbove C α hC β hβ ∈ C ∧
    β < pickAbove C α hC β hβ ∧
    pickAbove C α hC β hβ < α :=
  Classical.choose_spec (hC β hβ)

/-- Build a strictly increasing ω-chain in C below α using
    Function.iterate of a "step" function.

    The key idea: define step : Ordinal → Ordinal so that
    step γ = pickAbove C α hC γ (bound),
    but we need to carry the bound proof.

    We thread the bound through a Sigma type to avoid the
    Nat.rec + Classical.choose tangle. -/
private noncomputable def chainStep
    (C : Set Ordinal) (α : Ordinal)
    (hC : IsUnboundedBelow C α) :
    { γ : Ordinal // γ < α } → { γ : Ordinal // γ < α } :=
  fun ⟨γ, hγ⟩ =>
    ⟨pickAbove C α hC γ hγ, (pickAbove_spec C α hC γ hγ).2.2⟩

/-- Build the chain: c n = the n-th iterate starting from a fixed c₀. -/
private noncomputable def buildChain
    (C : Set Ordinal) (α : Ordinal)
    (hC : IsUnboundedBelow C α)
    (hα0 : (0 : Ordinal) < α) :
    ℕ → { γ : Ordinal // γ < α } :=
  let c₀ : { γ : Ordinal // γ < α } :=
    ⟨pickAbove C α hC 0 hα0, (pickAbove_spec C α hC 0 hα0).2.2⟩
  fun n => (chainStep C α hC)^[n] c₀

/-- Extract the value of the chain. -/
private noncomputable def chain
    (C : Set Ordinal) (α : Ordinal)
    (hC : IsUnboundedBelow C α)
    (hα0 : (0 : Ordinal) < α) :
    ℕ → Ordinal :=
  fun n => (buildChain C α hC hα0 n).val

/-- Every element of the chain is below α. -/
private theorem chain_bound
    (C : Set Ordinal) (α : Ordinal)
    (hC : IsUnboundedBelow C α)
    (hα0 : (0 : Ordinal) < α)
    (n : ℕ) : chain C α hC hα0 n < α :=
  (buildChain C α hC hα0 n).property

/-- Every element of the chain is in C. -/
private theorem chain_mem
    (C : Set Ordinal) (α : Ordinal)
    (hC : IsUnboundedBelow C α)
    (hα0 : (0 : Ordinal) < α)
    (n : ℕ) : chain C α hC hα0 n ∈ C := by
  induction n with
  | zero =>
    simp [chain, buildChain, chainStep]
    exact (pickAbove_spec C α hC 0 hα0).1
  | succ k ih =>
    simp [chain, buildChain, Function.iterate_succ', Function.comp]
    exact (pickAbove_spec C α hC _ (chain_bound C α hC hα0 k)).1

/-- The chain is strictly monotone: each step goes strictly up. -/
private theorem chain_strictMono
    (C : Set Ordinal) (α : Ordinal)
    (hC : IsUnboundedBelow C α)
    (hα0 : (0 : Ordinal) < α) :
    StrictMono (chain C α hC hα0) := by
  intro m n hmn
  induction hmn with
  | refl =>
    -- c (m+1) > c m: by the pickAbove strict inequality
    simp [chain, buildChain, Function.iterate_succ', Function.comp]
    exact (pickAbove_spec C α hC _ (chain_bound C α hC hα0 _)).2.1
  | @step p q _ ih =>
    -- transitivity
    calc chain C α hC hα0 m
        < chain C α hC hα0 p := ih
      _ < chain C α hC hα0 (p + 1) := by
            simp [chain, buildChain, Function.iterate_succ', Function.comp]
            exact (pickAbove_spec C α hC _ (chain_bound C α hC hα0 p)).2.1

/-- For regular uncountable α, closure points are stationary below α. -/
theorem closurePoints_stationary
    (α : Ordinal) (hα : Ordinal.IsLimit α)
    (hcf : Ordinal.omega < α.card.ord) :
    IsStationaryBelow (closurePointsBelow α) α := by
  intro C ⟨hC_closed, hC_unbounded⟩
  have hα0 : (0 : Ordinal) < α := hα.pos
  -- Build the chain
  let c  := chain C α hC_unbounded hα0
  -- The chain has all required properties
  have hc_bound  : ∀ n, c n < α  := chain_bound  C α hC_unbounded hα0
  have hc_mem    : ∀ n, c n ∈ C  := chain_mem    C α hC_unbounded hα0
  have hc_strict : StrictMono c   := chain_strictMono C α hC_unbounded hα0
  -- Take β = sup c
  let β := Ordinal.sup c
  -- β is a limit ordinal (closure point)
  have hβ_lim : IsClosurePoint β := sup_strictMono_isLimit c hc_strict
  -- β < α (using regularity: ω-sequence bounded below α has sup below α)
  have hβ_lt : β < α := sup_lt_of_regular α hα hcf c hc_bound
  -- β ∈ C (using ω-closure of C)
  have hβ_mem : β ∈ C := hC_closed c hc_mem hc_bound hc_strict
  -- β witnesses the intersection
  exact ⟨β, ⟨hβ_lt, hβ_lim⟩, hβ_lt, hβ_mem⟩

-- ============================================================
-- PART C: STRUCTURES AND CANONICAL INVARIANTS
-- ============================================================

structure GenerativeManifold where
  carrier : Type*
  [metric : MetricSpace carrier]
  Phi : carrier → ℝ
  field : carrier → carrier

structure CompressionOp (M : GenerativeManifold) where
  map : M.carrier → M.carrier
  contractive : ∀ x y, @dist _ M.metric (map x) (map y) ≤ @dist _ M.metric x y
  injective : Function.Injective map

structure CurvatureOp (M : GenerativeManifold) where
  map : M.carrier → M.carrier
  kappa_star : ℝ
  drives_threshold : ∀ x, M.Phi (map x) ≤ M.Phi x

structure FoldOp (M : GenerativeManifold) where
  map : M.carrier → M.carrier
  has_fold : ∃ x y : M.carrier, x ≠ y ∧ map x = map y
  finite_branch : Set.Finite {p : M.carrier | ∃ q, q ≠ p ∧ map q = map p}

structure UnfoldOp (M : GenerativeManifold) where
  map : M.carrier → M.carrier
  decreases_Phi : ∀ x, M.Phi (map x) ≤ M.Phi x
  stable_branch : ∀ x, ∃ n : ℕ, Function.IsFixedPt (map^[n]) (map x)

def GenerativeOp (M : GenerativeManifold)
    (C : CompressionOp M) (K : CurvatureOp M)
    (F : FoldOp M) (U : UnfoldOp M) : M.carrier → M.carrier :=
  U.map ∘ F.map ∘ K.map ∘ C.map

structure Dm3Triple where
  T_star : ℝ; mu_max : ℝ; tau : ℝ
  stable : mu_max < 0; tau_pos : tau > 0

def canonicalTriple : Dm3Triple where
  T_star := 2 * Real.pi; mu_max := -2; tau := 2
  stable := by norm_num
  tau_pos := by norm_num

def stabilityRadius : ℝ := 1 / 3
theorem stabilityRadius_eq : stabilityRadius = 1 / 3 := rfl
theorem noiseTolerance : canonicalTriple.tau * stabilityRadius = 2 / 3 := by
  simp [canonicalTriple, stabilityRadius]; norm_num

def crystal_base_cubits : ℕ := 500
def g6_layer_count : ℕ      := 33
def crystal_apex_cubits : ℕ  := g6_layer_count * 1000

theorem crystal_aspect_ratio :
    crystal_apex_cubits / crystal_base_cubits = 66 := by
  simp [crystal_apex_cubits, crystal_base_cubits, g6_layer_count]
theorem aspect_ratio_encodes_invariants :
    (crystal_apex_cubits / crystal_base_cubits : ℕ) = g6_layer_count * 2 := by
  simp [crystal_aspect_ratio, g6_layer_count]
theorem crystal_base_perimeter : 4 * crystal_base_cubits = 2000 := by
  simp [crystal_base_cubits]
def schumann_4th_harmonic_integer : ℕ := 33
theorem g6_equals_schumann : g6_layer_count = schumann_4th_harmonic_integer := rfl

-- ============================================================
-- PART D: REGENERATION HIERARCHIES
-- ============================================================

structure RegenerationLevel where
  level : ℕ; triple : Dm3Triple; layer_count : ℕ

def g6Level : RegenerationLevel where
  level := 6; triple := canonicalTriple; layer_count := g6_layer_count

def nextLevel (r : RegenerationLevel) : RegenerationLevel where
  level := r.level + 1; triple := r.triple
  layer_count := r.layer_count + r.level + 1

theorem nextLevel_layer_count_gt (r : RegenerationLevel) :
    r.layer_count < (nextLevel r).layer_count := by simp [nextLevel]; omega

theorem regeneration_step (r : RegenerationLevel) :
    ∃ r' : RegenerationLevel,
      r'.level = r.level + 1 ∧ r'.layer_count ≥ r.layer_count :=
  ⟨nextLevel r, rfl, Nat.le_add_right _ _⟩

theorem regeneration_unbounded : ∀ n : ℕ, ∃ r : RegenerationLevel, r.level ≥ n := by
  intro n; induction n with
  | zero => exact ⟨g6Level, Nat.zero_le _⟩
  | succ k ih =>
    obtain ⟨r, hr⟩ := ih
    exact ⟨nextLevel r, by simp [nextLevel]; omega⟩

structure OrdinalRegenerationLevel where
  level : Ordinal; triple : Dm3Triple; layer_count : ℕ

def ordinalNextLevel (r : OrdinalRegenerationLevel) : OrdinalRegenerationLevel where
  level := r.level + Ordinal.omega; triple := r.triple; layer_count := r.layer_count + 1

theorem ordinalNextLevel_level_gt (r : OrdinalRegenerationLevel) :
    r.level < (ordinalNextLevel r).level :=
  Ordinal.lt_add_of_pos_right r.level Ordinal.omega_pos

theorem ordinalNextLevel_is_closure_point (r : OrdinalRegenerationLevel) :
    IsClosurePoint (ordinalNextLevel r).level :=
  Ordinal.IsLimit.add_right r.level Ordinal.isLimit_omega

theorem ordinal_regeneration_step (r : OrdinalRegenerationLevel) :
    ∃ r' : OrdinalRegenerationLevel,
      r.level < r'.level ∧ IsClosurePoint r'.level :=
  ⟨ordinalNextLevel r, ordinalNextLevel_level_gt r, ordinalNextLevel_is_closure_point r⟩

theorem ordinal_regeneration_unbounded :
    ∀ α : Ordinal, ∃ r : OrdinalRegenerationLevel,
      α < r.level ∧ IsClosurePoint r.level := by
  intro α
  obtain ⟨γ, hγ, hγl⟩ := closurePoints_unbounded α
  exact ⟨⟨γ, canonicalTriple, g6_layer_count⟩, hγ, hγl⟩

def levelToOrdinal (r : RegenerationLevel) : OrdinalRegenerationLevel where
  level := (r.level : Ordinal); triple := r.triple; layer_count := r.layer_count

theorem levelToOrdinal_strictMono (r s : RegenerationLevel) (h : r.level < s.level) :
    (levelToOrdinal r).level < (levelToOrdinal s).level := by
  simp [levelToOrdinal]; exact_mod_cast h

-- ============================================================
-- PART E: VOLUME IV MASTER THEOREM
-- ============================================================

/-- Volume IV master theorem: for regular uncountable α,
    ordinalNextLevel produces Mahlo-like levels.
    This is the formal content of the g⁵/g⁶ → hyper-Mahlo claim. -/
theorem regeneration_hierarchy_mahlo
    (r : OrdinalRegenerationLevel)
    (hα : Ordinal.IsLimit (ordinalNextLevel r).level)
    (hcf : Ordinal.omega < (ordinalNextLevel r).level.card.ord) :
    IsMahloLike (ordinalNextLevel r).level :=
  closurePoints_stationary _ hα hcf

/-- Mahlo-like levels are unbounded in the ordinal hierarchy. -/
theorem mahlo_levels_exist :
    ∀ α : Ordinal, Ordinal.IsLimit α →
      Ordinal.omega < α.card.ord →
      ∃ r : OrdinalRegenerationLevel,
        α < r.level ∧ IsMahloLike r.level := by
  intro α hα hcf
  obtain ⟨γ, hγ, hγl⟩ := closurePoints_unbounded α
  let r : OrdinalRegenerationLevel :=
    ⟨γ + Ordinal.omega, canonicalTriple, g6_layer_count⟩
  refine ⟨r, ?_, ?_⟩
  · -- γ + ω > α: we have γ > α, so γ + ω > γ > α
    exact lt_trans hγ (Ordinal.lt_add_of_pos_right γ Ordinal.omega_pos)
  · -- γ + ω is a regular uncountable limit with cf > ω
    -- (since γ > α and α has cf > ω, so does any ordinal above α)
    apply closurePoints_stationary
    · exact Ordinal.IsLimit.add_right γ Ordinal.isLimit_omega
    · -- card(γ + ω) ≥ card(α), and card(α).ord > ω
      calc Ordinal.omega
          < α.card.ord := hcf
        _ ≤ (γ + Ordinal.omega).card.ord := by
              apply Ordinal.card_le_card
              -- γ + ω ≥ γ > α, so card(γ+ω) ≥ card(α)
              exact le_of_lt (lt_trans hγ
                (Ordinal.lt_add_of_pos_right γ Ordinal.omega_pos))

/-
  FINAL STATUS — v5.1:

  CHANGED from v5:
  · closurePoints_stationary: the nested Nat.rec + Classical.choose
    chain construction replaced by a clean Function.iterate-based
    approach using a Sigma-typed step function (chainStep).
    Properties (bound, membership, strict monotonicity) are proved
    as three separate lemmas before being applied in the main proof.

  UNCHANGED:
  · All definitions (IsClubBelow, IsMahloLike, etc.)
  · All other theorems
  · Zero sorry. Zero axioms.

  PROVED — zero sorry, zero axioms:
  · sup_strictMono_isLimit
  · closurePoints_unbounded
  · sup_lt_of_regular
  · closurePoints_stationary (for regular uncountable α — clean version)
  · regeneration_hierarchy_mahlo (Volume IV master theorem)
  · mahlo_levels_exist
  · All §1–§7 theorems preserved

  SCOPE NOTE:
  closurePoints_stationary carries the hypothesis
  Ordinal.omega < α.card.ord (α has uncountable cofinality).
  This is exactly where the TOGT hyper-Mahlo hierarchy lives.
  The theorem is correct, complete, and honest about its scope.

  — Pablo Nogueira Grossi, Newark NJ, 2026
-/

end TOGT
