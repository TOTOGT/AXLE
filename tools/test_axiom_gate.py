#!/usr/bin/env python3
"""Fixtures for tools/axiom_gate.py. Run: python3 tools/test_axiom_gate.py

The gate decides whether the repository's verification claims stand, so the
gate itself is checked here against reports whose correct verdict is known.
Case 2 is the output of CI run #245, verbatim, including the pretty-printer's
line wrapping -- the shape the previous shell pipeline could not read.
"""

import os
import subprocess
import sys
import tempfile

GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "axiom_gate.py")

CLEAN_12 = """\
'Orthogenesis.NASAGaps.FN_H_101L_isoperimetric' depends on axioms: [propext, Classical.choice, Quot.sound]
'Orthogenesis.NASAGaps.FN_H_102L_phase02_cluster' depends on axioms: [propext, Classical.choice, Quot.sound]
'Orthogenesis.NASAGaps.FN_L_101L_hex_interfaces' depends on axioms: [propext, Classical.choice, Quot.sound]
'Orthogenesis.NASAGaps.FN_L_101L_unique_interface' depends on axioms: [propext]
'Orthogenesis.NASAGaps.FN_T_201L_payload_monotone' does not depend on any axioms
'Orthogenesis.NASAGaps.FN_T_202L_payload_ratio' does not depend on any axioms
'Orthogenesis.NASAGaps.FN_T_201L_stage_gated' depends on axioms: [propext, Classical.choice, Quot.sound]
'Orthogenesis.NASAGaps.FN_U_103L_six_layers' does not depend on any axioms
'Orthogenesis.NASAGaps.FN_U_103L_expand_models_ISRU' depends on axioms: [propext, Classical.choice, Quot.sound]
'Orthogenesis.NASAGaps.FN_A_104L_reachability' depends on axioms: [propext, Classical.choice, Quot.sound]
'Orthogenesis.NASAGaps.FN_C_101L_ring_count' depends on axioms: [propext, Quot.sound]
'Orthogenesis.NASAGaps.nasa_gap_closure_summary' depends on axioms: [propext, Classical.choice, Quot.sound]
"""

# CI run #245, verbatim. Note the wrapped list on the second theorem.
RUN_245 = CLEAN_12.replace(
    "'Orthogenesis.NASAGaps.FN_H_102L_phase02_cluster' depends on axioms:"
    " [propext, Classical.choice, Quot.sound]",
    "'Orthogenesis.NASAGaps.FN_H_102L_phase02_cluster' depends on axioms: [propext,\n"
    " Classical.choice,\n"
    " Quot.sound,\n"
    " Orthogenesis.G6Crystal.colony_depth1_cells._native.native_decide.ax_1_1]")

# Every axiom permitted, but the list is long enough to wrap. The old pipeline
# failed the job on this; it must pass.
WRAPPED_CLEAN = CLEAN_12.replace(
    "'Orthogenesis.NASAGaps.FN_A_104L_reachability' depends on axioms:"
    " [propext, Classical.choice, Quot.sound]",
    "'Orthogenesis.NASAGaps.FN_A_104L_reachability' depends on axioms: [propext,\n"
    " Classical.choice,\n"
    " Quot.sound]")

ADMITTED = CLEAN_12.replace(
    "'Orthogenesis.NASAGaps.FN_C_101L_ring_count' depends on axioms: [propext, Quot.sound]",
    "'Orthogenesis.NASAGaps.FN_C_101L_ring_count' depends on axioms: [propext, sorryAx]")

MALFORMED = CLEAN_12 + \
    "'Orthogenesis.NASAGaps.FN_X_999L_truncated' depends on axioms: [propext\n"

CASES = [
    # name, report, expected_count, want_exit, must_appear_in_output
    ("clean twelve",              CLEAN_12,      12, 0, "OK: 12 theorems"),
    ("run #245 (native_decide)",  RUN_245,       12, 1,
     "FN_H_102L_phase02_cluster depends on Orthogenesis.G6Crystal"
     ".colony_depth1_cells._native.native_decide.ax_1_1"),
    ("clean but wrapped",         WRAPPED_CLEAN, 12, 0, "OK: 12 theorems"),
    ("admitted theorem",          ADMITTED,      12, 1, "sorryAx present"),
    ("unreadable record",         MALFORMED,     13, 1, "did not parse"),
    ("a theorem went missing",    CLEAN_12,      13, 1, "found 12"),
]


def run_case(report, expected):
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(report)
        p = subprocess.run([sys.executable, GATE, path, str(expected)],
                           capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    finally:
        os.unlink(path)


def main():
    failures = 0
    for name, report, expected, want_exit, needle in CASES:
        rc, out = run_case(report, expected)
        ok = (rc == want_exit) and (needle in out)
        print("%-28s %s" % (name, "PASS" if ok else "FAIL"))
        if not ok:
            failures += 1
            print("   wanted exit %d and %r" % (want_exit, needle))
            print("   got exit %d:\n%s" % (rc, "".join("   | " + l + "\n"
                                                       for l in out.splitlines())))
    print("\n%d/%d cases pass" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
