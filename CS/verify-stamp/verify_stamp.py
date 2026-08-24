#!/usr/bin/env python3
"""
verify-stamp — bind a verification claim to the artifact and environment it
was made about, and fail when they come apart.

WHY THIS EXISTS
---------------
A verification claim names an artifact. But verification is a property of a
TRIPLE: (artifact, toolchain, library). Conventional practice records the
first and drops the other two, which permits three distinct failures that are
indistinguishable to every automated reader:

  MISMATCH  the claim is attached to a different artifact than the one checked
            (a transcription or handoff error: the fix lives in one copy, the
            claim in another)
  STALE     the claim was true, and the toolchain or library has moved under
            it (nobody edited anything; the claim simply expired)
  FAIL      re-running the check now reports a forbidden result

The stamp is embedded IN the artifact, not in a sidecar, because a sidecar can
be separated from what it describes — which is the failure this tool exists to
catch. The content hash covers the file with the stamp block removed, so the
stamp can be rewritten without invalidating itself.

SECURITY NOTE
-------------
`--rerun` and the environment probes execute commands taken from the stamp
block inside the artifact. Only run those modes on repositories you would
already be willing to build. `check` without `--rerun` still runs the probe
commands; use `--no-probe` for a pure hash check on untrusted input.

EXIT CODES
----------
   0  OK        hash matches; environment matches; (with --rerun) check passed
  10  MISMATCH  content hash differs from the stamp
  11  STALE     hash matches, environment differs
  12  FAIL      re-ran and the check reported a forbidden token, or a required
                declaration was absent
  13  ERROR     no stamp, malformed stamp, missing file, probe failed

Codes start at 10 deliberately. 1 and 2 are already spoken for by shells,
interpreters and argument parsers; during development of this tool a broken
invocation exited 2 and was scored as a genuine MISMATCH by its own test
suite. A checker whose failure is indistinguishable from the failure it
reports is the defect it exists to catch.
"""

import argparse
import datetime
import hashlib
import os
import re
import subprocess
import sys

VERSION = "1"

# Assembled from parts on purpose. If the full marker strings appeared
# literally here, this file would contain its own delimiters, and stamping it
# would match these lines as the stamp block and strip them from the artifact.
# That is not hypothetical: it happened on the first self-application, the
# write reported success, and the file was left unable to import itself.
_MARK = "VERIFICATION" + "-STAMP"
BEGIN = _MARK + "-BEGIN"
END = _MARK + "-END"

OK, MISMATCH, STALE, FAIL, ERROR = 0, 10, 11, 12, 13
NAME = {OK: "OK", MISMATCH: "MISMATCH", STALE: "STALE", FAIL: "FAIL", ERROR: "ERROR"}

# --------------------------------------------------------------------------
# stamp parsing
# --------------------------------------------------------------------------

def split_stamp(text):
    """Return (before, stamp_lines, after, comment_prefix).

    stamp_lines is None when the file carries no stamp.
    The comment prefix is whatever text precedes the BEGIN marker on its line,
    which is what makes this work for --, #, //, % and friends.
    """
    lines = text.splitlines(keepends=True)
    b = e = None
    prefix = ""
    for i, line in enumerate(lines):
        if BEGIN in line and b is None:
            b = i
            prefix = line[:line.index(BEGIN)]
        elif END in line and b is not None:
            e = i
            break
    if b is None or e is None:
        return text, None, "", ""
    return "".join(lines[:b]), lines[b:e + 1], "".join(lines[e + 1:]), prefix


def block_is_wellformed(stamp_lines, prefix):
    """Every line between the markers must look like a stamp line.

    Without this, any file that merely mentions a marker -- documentation, a
    test fixture, this tool's own source -- can have arbitrary lines treated as
    stamp content and removed. Deleting lines from an artifact while claiming
    to certify it is the worst failure available to this program.
    """
    for line in stamp_lines:
        s = line
        if prefix and s.startswith(prefix):
            s = s[len(prefix):]
        elif prefix:
            return False
        s = s.strip()
        if BEGIN in s or END in s or not s:
            continue
        if ":" not in s:
            return False
    return True


def content_hash(text):
    before, stamp, after, _ = split_stamp(text)
    if stamp is None:
        body = text
    else:
        body = before + after
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def parse_fields(stamp_lines, prefix):
    """Parse `key: value` lines, allowing repeats (returns list per key)."""
    fields = {}
    for line in stamp_lines:
        s = line
        if prefix and s.startswith(prefix):
            s = s[len(prefix):]
        s = s.strip()
        if BEGIN in s or END in s or not s:
            continue
        if ":" not in s:
            continue
        k, v = s.split(":", 1)
        fields.setdefault(k.strip(), []).append(v.strip())
    return fields


def one(fields, key, default=None):
    v = fields.get(key)
    if not v:
        return default
    return v[0]


# --------------------------------------------------------------------------
# probes
# --------------------------------------------------------------------------

def run(cmd, cwd, timeout=900):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                       text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def probe_env(fields, cwd, enabled=True):
    """Evaluate every `env-probe: NAME = command` entry.

    Returns (dict NAME->value, error_or_None).
    """
    got = {}
    if not enabled:
        return got, None
    for entry in fields.get("env-probe", []):
        if "=" not in entry:
            return got, "malformed env-probe: %r" % entry
        name, cmd = entry.split("=", 1)
        rc, out = run(cmd.strip(), cwd)
        if rc != 0:
            return got, "env-probe %r failed (exit %d): %s" % (
                name.strip(), rc, out.strip()[:200])
        got[name.strip()] = out.strip()
    return got, None


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_check(args):
    path = args.file
    if not os.path.isfile(path):
        return report(ERROR, path, "no such file")
    text = open(path, encoding="utf-8").read()
    before, stamp, after, prefix = split_stamp(text)
    if stamp is None:
        return report(ERROR, path, "no %s block found" % BEGIN)

    if not block_is_wellformed(stamp, prefix):
        return report(ERROR, path,
                      "a %s marker was found but the block is not well formed;\n"
                      "  refusing to interpret it (a coincidental marker in prose"
                      " or code will do this)" % BEGIN)

    f = parse_fields(stamp, prefix)
    cwd = args.cwd or os.path.dirname(os.path.abspath(path)) or "."

    recorded = one(f, "content-sha256")
    if not recorded:
        return report(ERROR, path, "stamp has no content-sha256")

    actual = content_hash(text)
    if actual != recorded:
        return report(MISMATCH, path,
                      "stamp describes a different artifact\n"
                      "  stamp content-sha256: %s\n"
                      "  actual content-sha256: %s\n"
                      "  the claim and the file it is attached to have come apart"
                      % (recorded, actual))

    got, err = probe_env(f, cwd, enabled=not args.no_probe)
    if err:
        return report(ERROR, path, err)

    drift = []
    for entry in f.get("env", []):
        if "=" not in entry:
            return report(ERROR, path, "malformed env: %r" % entry)
        name, recorded_val = entry.split("=", 1)
        name, recorded_val = name.strip(), recorded_val.strip()
        if name in got and got[name] != recorded_val:
            drift.append((name, recorded_val, got[name]))

    if drift:
        msg = ["environment has moved since the stamp was written"]
        for name, was, now in drift:
            msg.append("  %s\n    stamped: %s\n    current: %s" % (name, was, now))
        msg.append("  the claim was true of the stamped environment and is"
                   " unsupported until re-run")
        return report(STALE, path, "\n".join(msg))

    if not args.rerun:
        return report(OK, path, "hash and environment match (not re-run;"
                                " pass --rerun to execute the check)")

    command = one(f, "command")
    if not command:
        return report(ERROR, path, "stamp has no command: cannot re-run")
    rc, out = run(command, cwd)

    problems = []
    for tok in f.get("forbidden", []):
        if tok in out:
            problems.append("forbidden token present in output: %s" % tok)
    for decl in f.get("declaration", []):
        if decl not in out:
            problems.append("declaration absent from output: %s" % decl)
    expect_rc = one(f, "expect-exit")
    if expect_rc is not None and str(rc) != expect_rc.strip():
        problems.append("exit code %d, stamp expects %s" % (rc, expect_rc.strip()))

    if problems:
        return report(FAIL, path, "re-run disagrees with the stamp:\n  " +
                      "\n  ".join(problems) + "\n--- output ---\n" + out.strip())
    return report(OK, path, "hash, environment and re-run all agree")


def cmd_stamp(args):
    path = args.file
    if not os.path.isfile(path):
        return report(ERROR, path, "no such file")
    text = open(path, encoding="utf-8").read()
    before, stamp, after, prefix = split_stamp(text)
    if stamp is not None and not block_is_wellformed(stamp, prefix):
        sys.stderr.write(
            "refusing to stamp: a %s marker was found but the block is not well\n"
            "formed. Rewriting would delete the lines between the markers.\n" % BEGIN)
        return ERROR
    prefix = args.prefix if args.prefix is not None else (prefix or "-- ")
    cwd = args.cwd or os.path.dirname(os.path.abspath(path)) or "."

    rc, out = run(args.command, cwd)
    for tok in args.forbidden:
        if tok in out:
            sys.stderr.write(
                "refusing to stamp: forbidden token %r present in output\n"
                "--- output ---\n%s\n" % (tok, out.strip()))
            return FAIL
    missing = [d for d in args.declaration if d not in out]
    if missing:
        sys.stderr.write(
            "refusing to stamp: declarations absent from output: %s\n"
            "--- output ---\n%s\n" % (", ".join(missing), out.strip()))
        return FAIL

    env_pairs = []
    for entry in args.env_probe:
        name, cmd = entry.split("=", 1)
        prc, pout = run(cmd.strip(), cwd)
        if prc != 0:
            sys.stderr.write("env-probe %r failed: %s\n" % (name.strip(), pout))
            return ERROR
        env_pairs.append((name.strip(), cmd.strip(), pout.strip()))

    body = before + after if stamp is not None else text

    # Normalise the body FIRST, then hash the normalised form, then write it
    # verbatim. Hashing a body you are about to reformat is how a stamp ends
    # up describing a file that never existed.
    if args.at == "top":
        body = body
    else:
        body = body.rstrip("\n") + "\n\n"
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

    L = []
    L.append("%s%s v%s" % (prefix, BEGIN, VERSION))
    L.append("%sartifact: %s" % (prefix, os.path.basename(path)))
    L.append("%scontent-sha256: %s" % (prefix, body_hash))
    L.append("%schecked-at: %s" % (prefix, datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    L.append("%scommand: %s" % (prefix, args.command))
    if args.expect_exit is not None:
        L.append("%sexpect-exit: %d" % (prefix, args.expect_exit))
    else:
        L.append("%sexpect-exit: %d" % (prefix, rc))
    for name, cmd, val in env_pairs:
        L.append("%senv-probe: %s = %s" % (prefix, name, cmd))
        L.append("%senv: %s = %s" % (prefix, name, val))
    for d in args.declaration:
        L.append("%sdeclaration: %s" % (prefix, d))
    for t in args.forbidden:
        L.append("%sforbidden: %s" % (prefix, t))
    L.append("%s%s" % (prefix, END))
    block = "\n".join(L) + "\n"

    new = block + body if args.at == "top" else body + block

    # the hash must describe the body, not the stamped file; re-derive to prove it
    open(path, "w", encoding="utf-8").write(new)
    check = content_hash(open(path, encoding="utf-8").read())
    if check != body_hash:
        sys.stderr.write("internal error: stamp is not self-consistent\n")
        return ERROR
    print("stamped %s\n  content-sha256 %s\n  exit %d" % (path, body_hash, rc))
    return OK


def report(code, path, msg):
    print("[%s] %s" % (NAME[code], path))
    for line in msg.splitlines():
        print("  " + line if line else "")
    return code


def main():
    ap = argparse.ArgumentParser(prog="verify-stamp", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="verify an existing stamp")
    c.add_argument("file")
    c.add_argument("--rerun", action="store_true",
                   help="also execute the recorded command and check its output")
    c.add_argument("--no-probe", action="store_true",
                   help="skip environment probes (pure hash check)")
    c.add_argument("--cwd", default=None)
    c.set_defaults(func=cmd_check)

    s = sub.add_parser("stamp", help="run the check and write a stamp")
    s.add_argument("file")
    s.add_argument("--command", required=True)
    s.add_argument("--declaration", action="append", default=[],
                   help="string that must appear in the output (repeatable)")
    s.add_argument("--forbidden", action="append", default=[],
                   help="string that must NOT appear (repeatable)")
    s.add_argument("--env-probe", action="append", default=[],
                   help="NAME=command whose stdout pins part of the environment")
    s.add_argument("--expect-exit", type=int, default=None)
    s.add_argument("--prefix", default=None, help="comment prefix, e.g. '-- '")
    s.add_argument("--at", choices=["top", "bottom"], default="bottom")
    s.add_argument("--cwd", default=None)
    s.set_defaults(func=cmd_stamp)

    args = ap.parse_args()
    try:
        sys.exit(args.func(args))
    except subprocess.TimeoutExpired:
        sys.exit(report(ERROR, args.file, "command timed out"))


if __name__ == "__main__":
    main()

# VERIFICATION-STAMP-BEGIN v1
# artifact: verify_stamp.py
# content-sha256: aa1dcf38f536af176a10dfd8dec399112c84bd68a91c9e33b395962f019594d6
# checked-at: 2026-08-21T13:42:44Z
# command: ./test_verify_stamp.sh
# expect-exit: 0
# env-probe: python3 = python3 --version
# env: python3 = Python 3.10.12
# declaration: passed 24, failed 0
# forbidden:   FAIL 
# VERIFICATION-STAMP-END
