# verify-stamp

Bind a verification claim to the artifact **and** the environment it was made
about, and fail when they come apart.

## The problem

A verification claim names an artifact. But verification is a property of a
**triple** — *(artifact, toolchain, library)*. Every convention in common use
records the first and drops the other two. That omission permits three
distinct failures which are indistinguishable to every automated reader:

| | what happened | who is at fault |
|---|---|---|
| **MISMATCH** | the claim is attached to a different artifact than the one checked | nobody lied; a copy, a handoff, or a transcription separated them |
| **STALE** | the claim was true; the toolchain or library moved under it | nobody edited anything; the claim expired |
| **FAIL** | re-running now reports a forbidden result | a real regression |

A file header reading `KERNEL-VERIFIED — no sorryAx` looks identical in all
three cases, and in the case where it is simply true.

## Worked example

This tool was written after an audit of `SaturnHexagon.lean` in this
repository, whose header asserted that five theorems were kernel-verified with
no `sorryAx`. Under the toolchain in use a month later, three of the five were
admitted rather than proved. Running the preserved 20 July copy under the
toolchain the header actually named (`leanprover/lean4:v4.14.0`) separated the
causes:

- **T2, T3** — true then, true now.
- **T1, T4** — true then. Mathlib stopped supplying `Fintype (Fin 6)`
  transitively through `Mathlib.Data.Real.Basic` between v4.14.0 and
  v4.33.0-rc1, `fin_cases` lost its instance, and the goals were admitted.
  Nobody touched the file. **STALE.**
- **T5** — never proved in that copy. The `ring` call that closes it was in a
  sibling copy written one minute earlier, under a header that read
  `<pending>`. The claim and the code that justified it were in different
  files. **MISMATCH.**

Specimens and timestamps are in `~/Desktop/DO NOT DELETE/MANIFEST.md`.

## Design

The stamp lives **inside** the artifact, not in a sidecar, because a sidecar
can be separated from what it describes — which is the failure this tool
exists to catch. The content hash covers the file with the stamp block
removed, so the stamp can be rewritten without invalidating itself.

The comment prefix is whatever precedes the `VERIFICATION-STAMP-BEGIN` marker
on its line, so the format works unmodified for `--`, `#`, `//`, `%` and
anything else.

## Usage

Write a stamp (runs the check first, and refuses to stamp a failing check):

```sh
verify-stamp stamp SaturnHexagon.lean \
  --prefix '-- ' \
  --command 'lake env lean SaturnHexagon.lean' \
  --declaration 'gate_commutes_onsite' \
  --declaration 'angCoupling_not_commute' \
  --declaration 'rot_commutes_coupling' \
  --declaration 'hex_rotation_invariant' \
  --declaration 'hex_coupling_uniform' \
  --forbidden 'sorryAx' \
  --env-probe 'toolchain=cat lean-toolchain' \
  --env-probe 'mathlib=git -C .lake/packages/mathlib rev-parse HEAD'
```

Check it (fast — hash and environment only):

```sh
verify-stamp check SaturnHexagon.lean
```

Check it properly (also re-runs the recorded command):

```sh
verify-stamp check --rerun SaturnHexagon.lean
```

## Exit codes

```
 0  OK        hash matches; environment matches; (with --rerun) check passed
10  MISMATCH  content hash differs from the stamp
11  STALE     hash matches, environment differs
12  FAIL      re-ran; forbidden token present or declaration absent
13  ERROR     no stamp, malformed stamp, missing file, probe failed
```

Codes start at 10 on purpose. `1` and `2` are already spoken for by shells,
interpreters and argument parsers. During development a broken invocation
exited 2 and was scored as a genuine MISMATCH by this tool's own test suite —
a checker whose failure is indistinguishable from the failure it reports is
precisely the defect it exists to catch. That bug is why the codes moved.

## Three defects this tool found in itself

Recorded rather than quietly fixed, because a verification tool with an
undisclosed defect history is asking for exactly the trust it exists to
withhold.

1. **Exit code collision.** `MISMATCH` was `2`, the code a Python interpreter
   returns for a file it cannot open. A broken invocation was scored as a
   genuine MISMATCH by the test suite. Codes moved to 10–13.

2. **A stamp describing a file that never existed.** `stamp` hashed the body,
   then reformatted it before writing. The recorded hash described an
   intermediate state. Caught by the self-consistency check at write time.

3. **Self-application deleted the markers.** The source defined
   `BEGIN = "VERIFICATION-STAMP-BEGIN"` literally, so when the tool stamped
   its own source it matched those constant definitions as the stamp block and
   removed them from the body it wrote back. The write reported success. The
   file was then unable to import itself, and its test suite went from 20/20
   to 2/18. The markers are now assembled from parts so they never appear
   literally, and any detected block whose lines do not all look like stamp
   lines is now an `ERROR` rather than a licence to delete them.

The third is the one worth dwelling on: the tool corrupted an artifact while
reporting that it had certified it. That is a worse failure than any it was
built to detect, and it was found only by applying the instrument to itself.

## Security

`--rerun` and the environment probes execute commands taken from the stamp
block inside the artifact. Only use those modes on repositories you would
already be willing to build. `check --no-probe` is a pure hash check and
executes nothing.

## Tests

```sh
./test_verify_stamp.sh
```

24 assertions covering all five exit codes, both MISMATCH routes (edited body,
and a stamp transplanted onto a sibling copy), STALE via a moved environment
probe, FAIL via both a forbidden token and a vanished declaration, refusal to
stamp a failing check, three comment prefixes, self-application (the tool
stamps its own source, still imports, and still checks), and a coincidental
marker in prose being reported as `ERROR` rather than acted on.

## What it does not do

It does not decide whether the recorded command is the right command, or
whether the declarations named are the interesting ones. A stamp that runs a
check of the wrong thing will pass forever. Choosing what to check remains a
human judgement, and no exit code substitutes for someone doubting the
auditor.
