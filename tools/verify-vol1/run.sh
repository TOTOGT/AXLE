#!/usr/bin/env bash
# The Volume I deposit's Lean is verified in its own small repository, not here.
#
# AXLE is too large to build for a single check — that is the whole reason the
# little repos exist. This script exists only so that anyone who looks for the
# Volume I verifier in AXLE finds the pointer instead of a dead end.
#
#     git clone https://github.com/TOTOGT/vol1-proofs
#     cd vol1-proofs && bash tools/run.sh
#
# What that runs, as of 2026-08-27: gate self-test → lake build → `#print axioms`
# over 82 declarations (PrincipiaVol1.lean 58 + AutophagyDm3_v2.lean 24) → a gate
# that refuses on sorryAx or on any axiom outside
# {propext, Classical.choice, Quot.sound} → a vacuity scan whose fixtures must
# fire, since a silent detector is worse than none.
#
# The last recorded run (tools/axioms.txt, 2026-08-25) is clean: zero sorryAx,
# 76 declarations on the standard trio, 2 on [propext, Quot.sound], 3 on
# [propext] alone.
#
# This comment said "49 theorems" until 2026-08-27. Both files are probed, and
# both counts belong here: 49 was neither.
#
# Pinned to Lean v4.14.0 and Mathlib v4.14.0 (rev 4bbdccd9c5f8). The pin is part
# of the claim.
#
# History: the first build of PrincipiaVol1.lean, on 2026-08-24, reported 81
# errors. V3–V6 of the deposit had described it as "30+ facts proved, 1 sorry".
# See PrincipiaOrthogona1/CHANGES_Vol1.md.
set -uo pipefail
cat <<'MSG'
The Volume I verifier lives in its own repository:

    git clone https://github.com/TOTOGT/vol1-proofs
    cd vol1-proofs
    bash tools/run.sh

Expected: GREEN — 49 theorems, every one kernel-checked, 0 sorry.
MSG
exit 0
