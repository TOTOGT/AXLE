## Session 2026-08-25

### Changes made
- preemie-manual.html: WHO percentiles suppressed before corrected age zero; Fenton 2013 referral added per row; dead code block removed; age-5 scope noted; book6 link added
- wp-preemie-dm3.html: new working paper, dm3 mapping of prematurity across four bio domains; anchor is AutophagyDm3_v2.lean (24 theorems, no sorry, no True conclusions)
- AutophagyDm3_v2.lean: updated, two Lean obligations open: surfactant network CRNT deficiency, thymic selection topology
- to_delete/ policy established: errors are evidence, nothing deleted directly
- chapter-gal-galois merged to main, fast-forward, clean

### House rules added
- Nothing deleted directly — items move to to_delete/ first
- lake-manifest.json has unstaged changes — do not sweep

## Session 2026-08-30 — corpus-wide Lean verification-claim audit

### What was scanned
All 206 `.lean` files under geometry, AXLE, GTCT, 3M (158 unique by content
hash). Each file's prose claim about its own status was compared against its
comment-stripped body. Cheap, no compute — it only asks whether a file's claim
matches its own content.

### Result
79 files make a verification claim in their prose. 21 of those contain a
`sorry`, a `native_decide`, or a bare `axiom`. **Most of those 21 are honest** —
files like `Dm3Arithmetic.lean`, `ContactHopf.lean`, `FiniteBranching.lean` and
`G6Conjecture.lean` say plainly "**Not machine-checked**", and
`MagneticLattice`/`SeismicLattice` scope the claim ("sorry-free *where the
mathematics is elementary*"). Those are the pattern to keep.

### The one that was not honest: CatGT/axle_togt_canonical.lean
Header said: *"theorem = proved in AXLE (Lean 4, zero sorry, zero axioms beyond
Mathlib)"*. All three parts were false.

1. **It does not compile.** Zero `import` lines, so `Matrix` and `Float.pi` are
   unknown identifiers. 5 errors against Lean 4.32.0 / Mathlib v4.32.0. Nothing
   in it has ever been machine-checked.
2. **It declares nine axioms**, not zero.
3. **Three of those axioms are false as stated**, which makes the file
   logically inconsistent — `False` is derivable, so every theorem in it
   follows regardless of its proof. Machine-checked refutation: at α = Bool,
   x = true, all operators `fun _ => false`, `regeneration_loop_invariant`
   gives `false = true`. `#print axioms` on the derived `False` names the
   axiom as its only non-standard dependency.
4. Four more axioms have body `True` — they assume nothing and prove nothing.

**A false axiom is strictly worse than a `sorry`.** A `sorry` fails loudly and
shows up in `#print axioms` as `sorryAx`. A false axiom compiles silently and
proves everything downstream.

**The corpus already knew.** `Main_v6.lean` carries the note *"Without this
hypothesis the original theorem is FALSE"* against `dm3_volume_invariant` and
adds the hypothesis. That repair never reached the canonical file. Applied now
to all three, with the counterexamples recorded at each site. The corrected
forms were checked to be *theorems of plain Mathlib* — the hypothesis does all
the work — so they assume nothing and cannot reintroduce inconsistency.

### On the registry
`theorem-registry.html` marks this file's 17 theorems ✓. That is not a
fabrication: the page states its own method — *"Not a kernel check… a
text/regex scan… cannot certify that a file compiles"* — and the file sits in
the **extended** tier, which the page labels as holding duplicates and orphans.
The disclosure is real and it should stay. But it covers *"we did not run
Lean"*, not *"this file cannot be run"* and not *"this file's axioms are
refutable"*. A text scan is structurally blind to both.

**Proposed, not yet done:** give the registry builder two more columns it can
compute without running Lean — `imports = 0` (a file that cannot compile) and
`axiom count > 0` — and refuse the ✓ glyph to any file with either. That
converts a caveat the reader must scroll to into a mark they cannot misread.

### House rules this adds
- **An `axiom` is an assumption, and an assumption can be false.** Before
  writing or trusting one, instantiate it at a two-element type with constant
  maps. If it survives that, it is at least not trivially inconsistent.
- **A universally quantified statement over arbitrary functions is almost
  always false.** If a claim is about operators *built to satisfy* a property,
  that property is a hypothesis, not a theorem.
- **Count the imports.** A Lean file with zero imports that mentions `Matrix`
  has never been compiled by anyone.
