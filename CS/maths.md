# Maths ↔ CS

## ↑ Maths → CS

### Verification provenance: the triple, and three failure classes

**Origin.** Formalising the G⁶ / D₆ operator algebra in Lean 4 required
maintaining a body of machine-checked theorems across a year, several
toolchains, and many sessions of an assistant that does not retain memory
between them. The mathematics is unremarkable. The *bookkeeping* failed in a
way that turned out to be general.

**Finding.** A verification claim names an artifact. Verification is a property
of a triple — *(artifact, toolchain, library)*. Recording only the first
permits three failures indistinguishable to every automated reader:

| | what changed | who erred | correct response |
|---|---|---|---|
| **MISMATCH** | the claim is attached to a different artifact than the one checked | nobody lied | find the sibling; reconcile |
| **STALE** | toolchain or library moved under a true claim | nobody at all | re-run and re-stamp |
| **FAIL** | the check now reports a forbidden result | a real regression | fix the artifact |

Conflating them produces the wrong action every time. Treat a STALE as a FAIL
and you hunt a bug in a clean file; treat a MISMATCH as a FAIL and you repair
the wrong copy while the correct one sits unused in the next directory.

**Evidence.** All three appeared under one header, in one file, within one
month. `SaturnHexagon.lean`, five theorems:

- `angCoupling_not_commute`, `rot_commutes_coupling` — stable throughout.
- `gate_commutes_onsite`, `hex_rotation_invariant` — proved 2026-07-20 under
  `leanprover/lean4:v4.14.0`; admitted under `v4.33.0-rc1` after Mathlib
  stopped supplying `Fintype (Fin 6)` transitively through
  `Mathlib.Data.Real.Basic`. Nobody edited the file. **STALE.**
- `hex_coupling_uniform` — never proved in the copy that claimed it. Its
  `ring` was in a sibling copy written *one minute earlier*, under a header
  reading `<pending>`. **MISMATCH.**

Runs, hashes and timestamps: `~/Desktop/DO NOT DELETE/MANIFEST.md`.

**Instrument.** [`verify-stamp/`](verify-stamp/) — 20 tests, five exit codes,
gating in CI.

**Write-up.** `book6/wp73-the-stamp-and-the-triple.html`

**Limits.** The instrument cannot tell whether the recorded command checks the
right thing. The July CI step was a genuine kernel invocation, correctly
executed, truthfully reporting on six declarations nobody cared about. No
stamp would have helped.

---

## ↓ CS → Maths

*(nothing filled — candidates below are unexamined)*

- **Candidate.** Proof assistants as a working constraint rather than a
  publication step: which of the corpus's stated theorems survive being typed
  at all. Partially probed — nine vacuous theorems of the form
  `: True := trivial` and `x ∈ S → x ∈ S := id` were found and removed. Not
  written up.
- **Candidate.** Complexity claims made in passing (e.g. an assertion that
  protein folding proceeds in polynomial time, since retracted from
  `book6/ch-molbio.html`). A discipline for when a complexity claim may be
  made at all.
- **Candidate.** Search over the corpus for numerical coincidences treated as
  structure — `book6/wp29-numerology-sweep.html` exists; relation to CS
  methods not established.
