#!/usr/bin/env python3
"""
extract_names_from_modules.py <compiled_modules.txt> <repo_root>

Unlike extract_names.py (which walks an entire folder and assumes every
.lean file under it is really part of the build -- true for GTCT/GCTC,
NOT true for AXLE, which has ~20+ loose root-level .lean files, many of
them superseded version history like Main_v2.lean..Main_v5.lean that are
never actually imported by anything).

This script instead starts from the REAL, ground-truth list of modules
`lake build` actually compiled (one .olean per compiled module, found by
the caller via `find .lake/build/lib -name '*.olean'`), maps each compiled
module name back to its source file (Foo.Bar -> Foo/Bar.lean), and only
extracts theorem/lemma declarations from files that were genuinely part
of the build. Orphaned/duplicate/dead .lean files that never got compiled
are silently excluded -- which is the correct, honest behaviour.
"""
import os
import re
import sys

DECL_RE = re.compile(
    r'^\s*(?:@\[.*?\]\s*)?(?:private |protected |noncomputable )*(theorem|lemma)\s+'
    r'([^\s:({\[]+)'
)
NAMESPACE_OPEN_RE = re.compile(r'^\s*namespace\s+(\S+)')
NAMESPACE_END_RE = re.compile(r'^\s*end(?:\s+(\S+))?\s*$')
SECTION_OPEN_RE = re.compile(r'^\s*section\b(?:\s+(\S+))?')


def strip_lean_comments(text: str) -> str:
    out = []
    i = 0
    depth = 0
    n = len(text)
    while i < n:
        if text[i:i + 2] == '/-':
            depth += 1
            i += 2
            continue
        if depth > 0:
            if text[i:i + 2] == '-/':
                depth -= 1
                i += 2
                continue
            i += 1
            continue
        out.append(text[i])
        i += 1
    stripped = ''.join(out)
    lines = []
    for line in stripped.split('\n'):
        idx = line.find('--')
        if idx != -1:
            line = line[:idx]
        lines.append(line)
    return '\n'.join(lines)


def extract(text: str):
    stack = []
    results = []
    for line in text.split('\n'):
        m = NAMESPACE_OPEN_RE.match(line)
        if m:
            stack.append(m.group(1))
            continue
        m = SECTION_OPEN_RE.match(line)
        if m and m.group(1):
            stack.append(m.group(1))
            continue
        m = NAMESPACE_END_RE.match(line)
        if m:
            if stack:
                stack.pop()
            continue
        m = DECL_RE.match(line)
        if m:
            kind, name = m.group(1), m.group(2)
            qualified = '.'.join(stack + [name]) if stack else name
            results.append((kind, qualified))
    return results


def main():
    if len(sys.argv) != 3:
        print("usage: extract_names_from_modules.py <compiled_modules.txt> <repo_root>", file=sys.stderr)
        sys.exit(1)
    modules_file, root = sys.argv[1], sys.argv[2]

    with open(modules_file, encoding='utf-8') as f:
        modules = [line.strip() for line in f if line.strip()]

    # Exclude external dependencies (Mathlib, Batteries, Aesop, Qq, Std,
    # ImportGraph, ProofWidgets, Cli, Plausible, LeanSearchClient, Init,
    # Lean, etc.) -- keep only modules that resolve to a real file inside
    # this repo, which is itself proof that they're this project's own
    # declarations and not a transitively-built dependency.
    kept = 0
    skipped_external = 0
    skipped_missing = 0
    for mod in modules:
        rel_path = mod.replace('.', '/') + '.lean'
        full_path = os.path.join(root, rel_path)
        if not os.path.isfile(full_path):
            skipped_missing += 1
            continue
        kept += 1
        with open(full_path, encoding='utf-8', errors='ignore') as f:
            text = f.read()
        stripped = strip_lean_comments(text)
        for kind, name in extract(stripped):
            print(f"{rel_path}\t{kind}\t{name}")

    print(f"# modules considered: {len(modules)}, matched to real files: {kept}, "
          f"no matching file (external dep): {len(modules) - kept}", file=sys.stderr)


if __name__ == '__main__':
    main()
