# Zenodo DOI Verification — RFI §13

**Date:** June 25, 2026
**Verification method attempted:** Programmatic fetch of each Zenodo record landing page
via `https://doi.org/<doi>` and `https://zenodo.org/records/<id>`.
**Outcome:** **Blocked** — the verification sandbox could not reach
zenodo.org or doi.org during this session (network timeouts on every fetch,
including a control fetch to example.com).
**Recommended action:** Re-run from a machine with normal internet access
using the script at the bottom of this file.

## The 14 DOIs to verify (RFI §13)

| # | DOI | Title claimed in RFI §13 | Verified? |
|---|-----|--------------------------|-----------|
| 1 | 10.5281/zenodo.19117399 | Series root (concept DOI, all versions) | ⬜ pending |
| 2 | 10.5281/zenodo.20320693 | Vol. I v3 — Operator algebra | ⬜ pending |
| 3 | 10.5281/zenodo.20159456 | Vol. II v2a — Contact geometry | ⬜ pending |
| 4 | 10.5281/zenodo.20239928 | GTCT Ring 5 v3 — Fifth operator T | ⬜ pending |
| 5 | 10.5281/zenodo.19162012 | G6 Crystal concept DOI — NASA Moon Base | ⬜ pending |
| 6 | 10.5281/zenodo.20168812 | Autophagy / Triple-Alpha Ch. A | ⬜ pending |
| 7 | 10.5281/zenodo.20230612 | Biological transitions v2 (7 systems) | ⬜ pending |
| 8 | 10.5281/zenodo.20128568 | Fruit-fly connectome v2 | ⬜ pending |
| 9 | 10.5281/zenodo.20075822 | DNLS / Tribonacci v4 | ⬜ pending |
| 10 | 10.5281/zenodo.20077205 | n-Bonacci criticality thresholds | ⬜ pending |
| 11 | 10.5281/zenodo.20230633 | Polylaminin / k-nacci spine | ⬜ pending |
| 12 | 10.5281/zenodo.20230614 | Multi-Orbit Identity Theory v2 | ⬜ pending |
| 13 | 10.5281/zenodo.19431918 | Wavenumber 6 / Nested Infinities | ⬜ pending |
| 14 | 10.5281/zenodo.19379385 | dm³ Operator Toy Model (GCM) | ⬜ pending |
| — | SSRN 10.2139/ssrn.6439626 | Full series on SSRN | ⬜ pending |

## Verification script

Run this from a machine with internet access. It exits non-zero on
any failure and prints a per-DOI status line.

```bash
#!/usr/bin/env bash
# zenodo_verify.sh — verify the 14 Zenodo DOIs in RFI §13.
set -u
DOIS=(
  "19117399:Series root (concept DOI, all versions)"
  "20320693:Vol. I v3 — Operator algebra"
  "20159456:Vol. II v2a — Contact geometry"
  "20239928:GTCT Ring 5 v3 — Fifth operator T"
  "19162012:G6 Crystal concept DOI — NASA Moon Base"
  "20168812:Autophagy / Triple-Alpha Ch. A"
  "20230612:Biological transitions v2 (7 systems)"
  "20128568:Fruit-fly connectome v2"
  "20075822:DNLS / Tribonacci v4"
  "20077205:n-Bonacci criticality thresholds"
  "20230633:Polylaminin / k-nacci spine"
  "20230614:Multi-Orbit Identity Theory v2"
  "19431918:Wavenumber 6 / Nested Infinities"
  "19379385:dm³ Operator Toy Model (GCM)"
)

failed=0
for entry in "${DOIS[@]}"; do
  id="${entry%%:*}"
  expected_title="${entry#*:}"
  echo "—— Checking 10.5281/zenodo.$id ——"
  json=$(curl -fsSL "https://zenodo.org/api/records/$id") || {
    echo "  ✗ FETCH FAILED"
    failed=$((failed+1))
    continue
  }
  title=$(echo "$json" | python3 -c "import json,sys; print(json.load(sys.stdin)['metadata']['title'])")
  echo "  title:    $title"
  echo "  expected: $expected_title"
  if echo "$title" | grep -qi "$(echo "$expected_title" | cut -d'—' -f1 | tr -d ' ')"; then
    echo "  ✓ OK"
  else
    echo "  ⚠ TITLE MISMATCH — review manually"
    failed=$((failed+1))
  fi
done
echo
if [ "$failed" -eq 0 ]; then
  echo "All 14 DOIs verified."
else
  echo "$failed DOI(s) failed verification. See above."
  exit 1
fi
```

Save as `~/Desktop/AXLE/NASA/MoonBase/scripts/zenodo_verify.sh`, then:

```
chmod +x ~/Desktop/AXLE/NASA/MoonBase/scripts/zenodo_verify.sh
~/Desktop/AXLE/NASA/MoonBase/scripts/zenodo_verify.sh \
  > ~/Desktop/AXLE/NASA/MoonBase/zenodo_doi_verification.log 2>&1
```

Update the table above (`⬜ pending` → `✓` or `✗ <issue>`) after running.

## SSRN deposit

The SSRN deposit DOI `10.2139/ssrn.6439626` is verified the same way:
visit `https://doi.org/10.2139/ssrn.6439626`; the landing page should
resolve to the SSRN paper page. If the landing page returns 404 or
"abstract submitted but not posted," update the RFI accordingly.

## What happens if a DOI fails

1. **Wrong title** — the deposit is real but the title in RFI §13 is
   outdated; update the RFI internal record (no NASA-side correction needed
   unless NASA asks specifically).
2. **404 / unresolved** — the deposit is missing or unpublished; this is a
   credibility risk if NASA checks. Either re-publish the deposit or
   strike it from §13.
3. **Wrong version** — the DOI resolves but to a different version than
   claimed (e.g. RFI says "Vol. I v3" but DOI resolves to v2). Either
   update the RFI to cite the correct concept DOI or re-publish v3.

## Status of this file

This file is a deliverable scaffolding. The actual verification needs to be
run from a machine with internet access. Until that is done, the §13
DOI table cannot be marked as verified.
