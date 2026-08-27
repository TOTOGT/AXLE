#!/usr/bin/env bash
# Volume II · the same check CI should run, locally. From anywhere:
#     bash tools/verify-vol2/run.sh
#
# History. PrincipiaOrthogona_v2/VolumeTwo.lean was in no lakefile target until
# 2026-08-26, so nothing had ever elaborated it. Its first build reported eight
# errors, including three in theorems the published Appendix A listed as proved.
# Compilation is not verification and verification is not sufficiency: read
# APPENDIX_A_2026-08-26.md for the three declarations that pass this gate while
# proving less than their names suggest.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1
PROBE="tools/verify-vol2/probe_vol2.lean"
OUT="tools/verify-vol2/axioms.txt"
N=19                                # counted by: grep -c '#print axioms' "$PROBE"
                                    # 14 through V4 + 5 added for V5 (2026-08-26)

command -v lake >/dev/null 2>&1 || { echo "lake not found; install elan first."; exit 127; }

echo "toolchain pinned : $(cat lean-toolchain)"
echo
echo "-- 1/4  gate fixtures (an unchecked gate is not evidence) ----------------"
python3 tools/test_axiom_gate.py || exit 1

echo
echo "-- 2/4  lake build PrincipiaVol2 -----------------------------------------"
lake build PrincipiaVol2 || { echo "BUILD FAILED. Nothing below is meaningful."; exit 1; }

echo
echo "-- 3/4  kernel axiom probe ----------------------------------------------"
lake env lean "$PROBE" > "$OUT" 2>&1
rc=$?
cat "$OUT"
[ "$rc" -ne 0 ] && { echo; echo "PROBE FAILED TO ELABORATE (exit $rc)."; exit 1; }
[ -s "$OUT" ] || { echo "::error:: probe produced no output. Silence is not a pass."; exit 1; }

echo
echo "-- 4/4  axiom gate -------------------------------------------------------"
python3 tools/axiom_gate.py "$OUT" "$N"
gate=$?
echo
if [ "$gate" -eq 0 ]; then
  echo "GREEN - $N declarations, kernel-checked, no sorryAx, axioms within the allowlist."
  echo "        NOT a claim that each proves what its name says. See APPENDIX_A_2026-08-26.md."
else
  echo "RED - the gate refused. Read the report above."
fi
exit $gate
