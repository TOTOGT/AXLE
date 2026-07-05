/-
AXLE — Principia Orthogona Formal Verification Engine
G6 LLC · Pablo Nogueira Grossi · Newark NJ · 2026
MIT License

This is the barrel file for the AXLE library.
It imports every module that Lake should compile as part of
the AXLE build target.

Structure:
· Verified geometric fragment — finite.lean (Kakeya)
· Verified toy pillars — Dm3*Toy.lean (pillars; PoincareToy removed, see below)
· Verified ordinal hierarchy — AXLE_v5_1.lean (Mahlo)
· Real conjectural pillars — dm3Collatz.lean, Dm3Comp.lean

sorry count across verified modules: 0
sorry count across conjectural modules: see individual files

NOTE (fixed — real bugs found via the first real `lake build` ever run
against this repo):
· import Finite -> import finite: the real file on disk is lowercase
  finite.lean. Case-sensitive on Linux CI runners; invisible on
  case-insensitive macOS filesystems, so this went undetected until now.
· import Dm3PoincareToy removed: Dm3PoincareToy.lean does not exist
  anywhere in this repository (confirmed via repo-wide file search).
  The "Topological pillar" it was meant to cover has no source file yet.
-/

-- ============================================================
-- VERIFIED: Geometric fragment (Kakeya)
-- ============================================================
-- Proves: finite-directions Kakeya with thickened segments.
-- namespace AXLE.Kakeya.Finite
-- sorry count: 0
import finite

-- ============================================================
-- VERIFIED: Toy pillars (zero sorry each)
-- ============================================================

-- Topological pillar (discrete Ricci flow -> sphereComplex): REMOVED.
-- Dm3PoincareToy.lean does not exist in this repository — there is
-- nothing to import here. Restore this import if/when that file is
-- actually added to the repo.

-- Additive-arithmetic pillar: compression toward prime-pair base
-- namespace Dm3GoldbachToy
import Dm3GoldbachToy

-- PDE/flow pillar: energy dissipation → rest state
-- namespace Dm3NSToy
import Dm3NSToy

-- Analytic pillar: zeros pulled to critical line
-- namespace Dm3RHToy
import Dm3RHToy

-- ============================================================
-- VERIFIED: Ordinal hierarchy (Mahlo levels)
-- ============================================================
-- Proves: closurePoints_stationary for regular uncountable α.
-- Volume IV master theorem: regeneration_hierarchy_mahlo.
-- namespace TOGT
-- sorry count: 0
import AXLE_v5_1

-- ============================================================
-- CONJECTURAL: Real pillars (formally stated, sorry present)
-- ============================================================

-- Collatz/Syracuse: real C/K/F/U grammar, convergence axiomatic
-- namespace Dm3Collatz
import dm3Collatz

-- P vs NP: computational dm³ pillar
-- namespace Dm3Comp
import Dm3Comp
