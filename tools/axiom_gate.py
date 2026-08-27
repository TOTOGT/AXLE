#!/usr/bin/env python3
"""Decide whether a `#print axioms` report is acceptable.

Usage:  axiom_gate.py REPORT EXPECTED_COUNT [--allow AXIOM ...]

Exit 0 if every theorem in REPORT depends only on permitted axioms and the
number of theorems reported equals EXPECTED_COUNT. Exit 1 otherwise, with one
::error:: line per problem.

WHY THIS IS A FILE AND NOT A SHELL PIPELINE IN THE WORKFLOW
-----------------------------------------------------------
It was a shell pipeline, copied into two workflow steps. Both copies were
line-oriented, and Lean's pretty-printer wraps a long axiom list across
several indented lines:

    'Orthogenesis.NASAGaps.FN_H_102L_phase02_cluster' depends on axioms: [propext,
     Classical.choice,
     Quot.sound,
     Orthogenesis.G6Crystal.colony_depth1_cells._native.native_decide.ax_1_1]

`grep "depends on axioms"` sees only the first of those four lines. The `sed`
that strips the brackets needs a closing `]` on that same line, so it never
matches, and the whole unstripped line falls through the allowlist as though
it were the name of an axiom. CI run #245 is the specimen: it failed for the
right theorem, but the error it printed read

    'FN_H_102L_phase02_cluster' depends on axioms: [propext

naming a permitted axiom as the offender. The same shape means a theorem whose
axiom list is entirely permitted, and merely long enough to wrap, also fails
the job. Right verdict by accident in one direction, wrong verdict in the
other.

A gate is a claim about the artifact it guards, and it is subject to the same
rule as any other claim here: it has to be checked. A pipeline duplicated
across two steps of a YAML file cannot be run on a fixture. This file can --
see tools/test_axiom_gate.py, which includes the run #245 output as a
regression case.

WHAT THE PERMITTED THREE MEAN
-----------------------------
propext, Classical.choice and Quot.sound are the axioms of Lean's standard
classical foundation; Mathlib rests on them throughout. Anything else is a
finding:

  sorryAx           the theorem is admitted, not proved
  Lean.ofReduceBool `native_decide` -- the goal was evaluated in compiled code
                    and the kernel was asked to trust the answer
  <anything else>   an axiom someone declared; read it before allowing it
"""

import re
import sys

DEFAULT_ALLOWED = ("propext", "Classical.choice", "Quot.sound")

RECORD = re.compile(r"^'([^']+)' depends on axioms: \[(.*)\]$")
NO_AXIOMS = "does not depend on any axioms"
HAS_AXIOMS = "depends on axioms"


def parse(text):
    """Return (records, unparsed).

    A record is (theorem_name, [axiom, ...]); a theorem with no axioms yields
    an empty list. `unparsed` holds lines that announce axioms but do not match
    the expected shape -- those are reported as parse failures, never silently
    treated as axiom names.
    """
    # Rejoin the pretty-printer's wrapped continuations. A continuation is any
    # line beginning with whitespace; a record always begins with a quote.
    joined = re.sub(r"\n[ \t]+", " ", text)

    records, unparsed = [], []
    for line in joined.splitlines():
        line = line.strip()
        if NO_AXIOMS in line:
            name = line.split("'")[1] if "'" in line else line
            records.append((name, []))
            continue
        if HAS_AXIOMS not in line:
            continue
        m = RECORD.match(line)
        if not m:
            unparsed.append(line)
            continue
        axioms = [a.strip() for a in m.group(2).split(",") if a.strip()]
        records.append((m.group(1), axioms))
    return records, unparsed


def main(argv):
    if len(argv) < 3:
        sys.stderr.write(__doc__.split("\n\n")[1] + "\n")
        return 2

    path = argv[1]
    try:
        expected = int(argv[2])
    except ValueError:
        sys.stderr.write("EXPECTED_COUNT must be an integer\n")
        return 2

    allowed = set(DEFAULT_ALLOWED)
    if "--allow" in argv:
        allowed.update(argv[argv.index("--allow") + 1:])

    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    records, unparsed = parse(text)
    failed = False

    if "sorryAx" in text:
        print("::error::sorryAx present - a theorem is admitted, not proved")
        failed = True

    for line in unparsed:
        print("::error::axiom report line did not parse; the gate cannot read it:")
        print("::error::  " + line)
        failed = True

    offenders = [(n, [a for a in ax if a not in allowed]) for n, ax in records]
    offenders = [(n, extra) for n, extra in offenders if extra]
    for name, extra in offenders:
        print("::error::%s depends on %s" % (name, ", ".join(extra)))
        failed = True
    if offenders:
        print("::error::permitted axioms are %s." % ", ".join(sorted(allowed)))
        print("::error::native_decide leaves Lean.ofReduceBool and is NOT a"
              " kernel check; sorryAx means the theorem is admitted.")

    if len(records) != expected:
        print("::error::expected %d theorems in this report, found %d"
              " - one was renamed, removed, or failed to elaborate"
              % (expected, len(records)))
        failed = True

    if failed:
        return 1

    print("OK: %d theorems, no sorryAx, no axiom outside the permitted set."
          % len(records))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
