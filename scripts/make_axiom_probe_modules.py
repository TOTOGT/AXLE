#!/usr/bin/env python3
"""
make_axiom_probe_modules.py <names_file>

Variant of make_axiom_probe.py for repos (like AXLE) that don't have one
umbrella import root. Instead, it imports every distinct module that the
names actually came from (derived from the relpath column emitted by
extract_names_from_modules.py: "Foo/Bar.lean" -> "import Foo.Bar"),
then emits the same real #print axioms <name> probe lines as before.
"""
import sys

def main():
    if len(sys.argv) != 2:
        print("usage: make_axiom_probe_modules.py <names_file>", file=sys.stderr)
        sys.exit(1)
    names_file = sys.argv[1]

    rows = []
    with open(names_file, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 3:
                continue
            rows.append(parts)

    modules = []
    seen_mod = set()
    for relpath, _kind, _name in rows:
        assert relpath.endswith('.lean')
        mod = relpath[:-len('.lean')].replace('/', '.')
        if mod not in seen_mod:
            seen_mod.add(mod)
            modules.append(mod)

    for mod in modules:
        print(f"import {mod}")
    print()

    seen_name = set()
    for _relpath, _kind, name in rows:
        if name in seen_name:
            continue
        seen_name.add(name)
        print(f"#print axioms {name}")


if __name__ == '__main__':
    main()
