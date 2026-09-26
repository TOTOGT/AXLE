# Disaster Theory — where the Lean is

**The Lean for Disaster Theory is not in this repository. It is here:**

    geometry/Orthogenesis/Disaster/DisasterTheory.lean
    https://github.com/TOTOGT/geometry/blob/main/Orthogenesis/Disaster/DisasterTheory.lean

Chapter: <https://totogt.github.io/geometry/chDis-disaster.html>
Kernel report: `geometry/tools/verify-audit/2026-09-15/geometry__Orthogenesis__Disaster__DisasterTheory.axioms.txt`

---

## Why this folder exists

From June 2026 until 15 September 2026, `chDis-disaster.html` cited three files
in this repository:

    DisasterTheory.lean
    CatastropheF.lean
    ChaosMu.lean

None of the three has ever existed here — not in the working tree, and not
anywhere in this repository's history. The Lean source existed only inside the
HTML that said it had been checked. `chF-catastrophe.html` and
`chMu-lyapunov.html` cite two of the same names.

This folder is the marker at the address a reader was sent to. It says where the
file actually is, so that following the citation ends in a file rather than in
nothing.

## Why the file is not here

This repository pins `leanprover/lean4:v4.14.0`, has no `.lake`, and has no
`.github/workflows`. Nothing in it has ever been elaborated by anything but a
hand run on one machine. A file deposited here would be as uncheckable as one
that does not exist, and the defect would survive the repair.

`geometry` pins `v4.32.0`, builds, and runs the proofs on every push. The file
is imported by `Orthogenesis.lean`, so it is inside a build target rather than
beside one.

## What the file contains

Nineteen declarations, none admitted, kernel-checked 2026-09-15 against the
`v4.32.0` pin. Among them:

| declaration | what it says |
|---|---|
| `whitney_fold_deriv` | `d/dx (x³ + a·x) = 3x² + a` |
| `published_D2_is_false` | the chapter's D2, `deriv … 0 = 0`, is false — it is `1/3` |
| `fold_at_zero_parameter` | the fold of this unfolding is at `a = 0` |
| `no_critical_point_at_eps0` | at `a = ε₀ = 1/3` the unfolding has no critical point |

The remaining fifteen are the published listing with each docstring reduced to
what its own theorem states. The file's closing block names five obligations the
chapter makes and the file does not discharge, the Disaster Theorem first.

## Reproducing the check

    git clone https://github.com/TOTOGT/geometry && cd geometry
    lake exe cache get
    lake build Orthogenesis.Disaster.DisasterTheory
    lake env lean Orthogenesis/Disaster/DisasterTheory.lean   # then #print axioms

## The rule this folder is an instance of

An address is `(path, sha256, date)`, never a name. A citation that names a file
nobody can open is not a weak verification claim; it is not a verification claim
at all. `geometry/tools/lean_addresses.py` checks the whole corpus against this
rule and reports what still fails it.
