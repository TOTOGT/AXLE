# Verification tooling in this corpus — read before adding any

The reference implementation is **`TOTOGT/vol1-proofs/tools/`**, not this
directory. It runs five stages — gate self-test, build, probe, axiom gate,
vacuity scan with fixtures that must fire — over 82 declarations
(PrincipiaVol1 58 + AutophagyDm3_v2 24), and it is gated in CI.

`verify-core/` was written here on 2026-08-27 to probe those same two files. It
duplicated `vol1-proofs` and had no vacuity stage, so it has been retired to
`to_delete/verify-core-superseded-by-vol1-proofs/`.

What still belongs here:

- `verify-vol2/` — 19 declarations in `PrincipiaOrthogona_v2/VolumeTwo.lean`,
  which lives in this repo and nowhere else.
- `axiom_gate.py` — shared gate.

The corpus-wide map, the Tier 1 ledger, and the per-repo CI gaps are recorded in
`geometry/CLAUDE.md` under "THE REPO MAP AND THE VERIFICATION LEDGER".
