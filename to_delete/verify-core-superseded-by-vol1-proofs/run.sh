#!/usr/bin/env bash
# The two AXLE files that carry sorry-free content, through the kernel.
#     bash tools/verify-core/run.sh
# AXLE's own Mathlib (v4.14.0) is not built -- there is no Mathlib.olean under
# .lake -- so this borrows the Mathlib that the geometry repository has built.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GEO="${GEOMETRY_ROOT:-$HOME/Desktop/geometry}"
PROBE="$ROOT/tools/verify-core/probe_core.lean"
OUT="$ROOT/tools/verify-core/axioms.txt"
N=99                                   # counted by: grep -c '#print axioms' "$PROBE"
                                       # 62 PrincipiaVol1 + 24 AutophagyDm3 + 13 NbonacciLadder

[ -d "$GEO/.lake/packages/mathlib" ] || {
  echo "No built Mathlib at $GEO."
  echo "Set GEOMETRY_ROOT to a repository that has one, or build AXLE's own."
  exit 127; }

echo "borrowed toolchain : $(cat "$GEO/lean-toolchain")"
echo "AXLE pins          : $(cat "$ROOT/lean-toolchain" 2>/dev/null || echo '(none)')"
echo "  The two differ. Every declaration below elaborates under the borrowed"
echo "  Mathlib; that is the claim being made, not that AXLE's own pin builds."
echo

echo "-- kernel axiom probe --------------------------------------"
( cd "$GEO" && lake env lean "$PROBE" ) > "$OUT" 2>&1
rc=$?
cat "$OUT"
[ "$rc" -ne 0 ] && { echo; echo "PROBE FAILED TO ELABORATE (exit $rc)."; exit 1; }

echo
echo "-- axiom gate ----------------------------------------------"
python3 "$ROOT/tools/axiom_gate.py" "$OUT" "$N"
gate=$?

echo
if [ "$gate" -eq 0 ]; then
  echo "GREEN -- $N declarations, every one kernel-checked, no sorryAx."
else
  echo "RED -- the gate refused. Either a declaration is admitted (sorryAx), an"
  echo "       axiom is outside the allowlist, or the count moved."
fi
exit $gate
