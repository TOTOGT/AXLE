# Architecture ↔ CS

## ↑ Architecture → CS

### A fourth class: VACUOUS — the check passes and means nothing

**Origin.** `Orthogenesis/Architecture/` formalises lattice claims for acoustic,
magnetic, seismic and crystal structures. Measured 2026-08-21:

| file | lines | theorems | defs | `sorry` |
|---|---|---|---|---|
| `AcousticLattice.lean` | 192 | 11 | 5 | 3 |
| `DM3Bridge.lean` | 224 | 14 | 6 | 0 |
| `G6Crystal.lean` | 364 | 29 | 20 | 11 |
| `MagneticLattice.lean` | 283 | 20 | 9 | 8 |
| `SeismicLattice.lean` | 225 | 17 | 5 | 6 |
| **total** | **1288** | **91** | **45** | **28** |

Six of those 91 are live placeholders of the form `: True := trivial`:

```
AcousticLattice.lean:166   full_diffraction_spectrum_placeholder
AcousticLattice.lean:171   intentionality_placeholder
AcousticLattice.lean:175   quetzal_match_placeholder
MagneticLattice.lean:259   neutron_selection_rule_placeholder
SeismicLattice.lean:187    hexagrid_collapse_superior_placeholder
SeismicLattice.lean:194    crack_tortuosity_placeholder
```

**Finding.** These are a *fourth* failure class, and the instrument built for
the first three cannot see it.

MISMATCH, STALE and FAIL all concern whether a **proof** still supports a
statement. VACUOUS concerns whether the **statement says anything**. A theorem
`: True := trivial` compiles cleanly, depends on no axioms beyond the standard
three, contains no `sorry`, and reports exactly what a real theorem reports.
`#print axioms` is the wrong instrument by construction: it asks what a proof
rests on, and a trivially true statement rests on nothing. The check passes,
truthfully, and certifies nothing.

| | question asked | detects |
|---|---|---|
| MISMATCH | is this the artifact that was checked? | hash |
| STALE | is this the environment it was checked in? | probe |
| FAIL | does the check still pass? | re-run |
| **VACUOUS** | **does the statement have content?** | **nothing yet** |

**Why it survives here.** The Architecture library *is* in a build target —
`lean_lib Orthogenesis`, imported by `Orthogenesis.lean` — so `lake build`
compiles all 91 theorems on every push. But the CI axiom probe names only the
five `SaturnHexagon` theorems. None of the 91 is axiom-checked, and even if all
91 were, the six placeholders would pass.

So the corpus contains two distinct blind spots stacked: theorems outside the
probe, and theorems the probe cannot judge even when aimed at them.

**Detection sketch, not built.** A statement-level check: reject a `theorem`
whose type is `True`, or whose type is an implication from a hypothesis to
itself, or which quantifies over nothing and asserts a decidable closed
proposition already reducible by `decide`. Textual grep finds the obvious
shapes — that is how these six were found — but a real check has to work on the
*elaborated type*, not the source text, or it will miss anything written
indirectly and flag anything mentioned in a comment.

**Open.** The six placeholders are unresolved. Each should become a real
statement or be deleted; leaving them is the corpus asserting 91 theorems while
85 are load-bearing. Deleting them is not a decision this file can make.

---

## ↓ CS → Architecture

*(nothing filled)*

- **Candidate, unexamined.** `SeismicLattice.lean` and `G6Crystal.lean` make
  comparative claims about hexagonal grids under collapse. Whether any is in a
  state where a machine check would mean something has not been assessed — and
  the two `hexagrid_collapse` placeholders suggest the comparative claim is
  currently asserted rather than proved.
- **Candidate, unexamined.** `AcousticLattice.lean` carries an
  `intentionality_placeholder`. Whatever it is meant to state, a claim about
  intentionality is not the kind of thing a lattice formalisation can settle,
  and it should be looked at before it acquires a proof-shaped wrapper.
