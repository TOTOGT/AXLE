#!/usr/bin/env python3
"""Export the theorem-registry data (same scan build_theorem_registry.py uses,
no reimplemented logic) as a flat JSON seed for Theorem Alpha 50c."""
import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import build_theorem_registry as R  # running this module also regenerates theorem-registry.html

seed = {
    "closed_kernel_audited": {
        "count": R.kn,
        "names": R.k_names,
        "sources": R.k_sources,
    },
    "open_sorry_core": [{"file": p, "name": n} for p, n, st in R.core if st == 'sorry'],
    "open_sorry_recursive": [{"file": p, "name": n} for p, n, st in R.rec if st == 'sorry'],
}
out = os.path.join(os.path.dirname(__file__), '..', 'theorem_alpha_seed.json')
with open(out, 'w') as f:
    json.dump(seed, f, indent=2)
print(f"kernel-audited (closed): {R.kn}")
print(f"open sorry, core: {len(seed['open_sorry_core'])}")
print(f"open sorry, recursive: {len(seed['open_sorry_recursive'])}")
print(f"wrote {os.path.abspath(out)}")
