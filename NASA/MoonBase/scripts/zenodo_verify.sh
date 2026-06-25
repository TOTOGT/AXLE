#!/usr/bin/env bash
# zenodo_verify.sh — verify the 14 Zenodo DOIs in RFI §13 (Notice ID 80JSC026MoonBase_RFI).
#
# Usage:
#   ./zenodo_verify.sh > zenodo_doi_verification.log 2>&1
#
# Exits non-zero on any DOI that does not resolve or whose title does not
# contain the expected fragment.  Prints a per-DOI status line.

set -u

DOIS=(
  "19117399:Series root"
  "20320693:Operator algebra"
  "20159456:Contact geometry"
  "20239928:GTCT"
  "19162012:G6 Crystal"
  "20168812:Autophagy"
  "20230612:Biological transitions"
  "20128568:connectome"
  "20075822:DNLS"
  "20077205:n-Bonacci"
  "20230633:Polylaminin"
  "20230614:Multi-Orbit"
  "19431918:Wavenumber"
  "19379385:dm"
)

failed=0
for entry in "${DOIS[@]}"; do
  id="${entry%%:*}"
  expected_fragment="${entry#*:}"
  echo "—— Checking 10.5281/zenodo.$id ——"
  if ! json=$(curl -fsSL --max-time 30 "https://zenodo.org/api/records/$id" 2>/dev/null); then
    echo "  ✗ FETCH FAILED (curl exit non-zero)"
    failed=$((failed+1))
    continue
  fi
  title=$(printf '%s' "$json" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('metadata',{}).get('title','<no title>'))" 2>/dev/null) || {
    echo "  ✗ JSON PARSE FAILED"
    failed=$((failed+1))
    continue
  }
  echo "  title:    $title"
  echo "  expected: contains '$expected_fragment'"
  # case-insensitive substring match
  if printf '%s' "$title" | grep -qi -- "$expected_fragment"; then
    echo "  ✓ OK"
  else
    echo "  ⚠ TITLE FRAGMENT NOT FOUND — review manually"
    failed=$((failed+1))
  fi
done

echo
echo "—— Checking SSRN 10.2139/ssrn.6439626 ——"
if curl -fsSL --max-time 30 -o /dev/null -w "  HTTP %{http_code}\n" "https://doi.org/10.2139/ssrn.6439626" 2>/dev/null; then
  echo "  (manually inspect the resolved landing page)"
else
  echo "  ✗ FETCH FAILED"
  failed=$((failed+1))
fi

echo
if [ "$failed" -eq 0 ]; then
  echo "All deposits verified."
  exit 0
else
  echo "$failed deposit(s) failed verification. See lines marked ✗ or ⚠ above."
  exit 1
fi
