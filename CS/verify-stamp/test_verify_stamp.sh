#!/usr/bin/env bash
# Test suite for verify-stamp. A checker that is not itself checked is a joke.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
VS="python3 $HERE/verify_stamp.py"
T=$(mktemp -d); cd "$T"
pass=0; fail=0
expect() { # expect <code> <label> <command...>
  local want=$1 label=$2; shift 2
  "$@" > out.txt 2>&1; local got=$?
  if [ "$got" -eq "$want" ]; then pass=$((pass+1)); printf "  ok   %-46s (exit %d)\n" "$label" "$got"
  else fail=$((fail+1)); printf "  FAIL %-46s want %d got %d\n" "$label" "$want" "$got"; sed 's/^/       /' out.txt; fi
}

# a toy "artifact" in a language with # comments, and a toy "checker"
cat > widget.py <<'PY'
def add(a, b):
    return a + b
PY
cat > runcheck.sh <<'SH'
#!/usr/bin/env bash
python3 - <<'P'
import widget
assert widget.add(2,2) == 4
print("declaration: add")
print("status: clean")
P
SH
chmod +x runcheck.sh
echo "v1.2.3" > toolversion.txt

echo "== 1. stamping =="
expect 0 "stamp writes a stamp" \
  $VS stamp widget.py --prefix "# " \
      --command "./runcheck.sh" \
      --declaration "declaration: add" \
      --forbidden "TRACEBACK" \
      --env-probe "toolchain=cat toolversion.txt"

echo "== 2. clean check =="
expect 0 "check (hash+env)"        $VS check widget.py
expect 0 "check --rerun"           $VS check widget.py --rerun

echo "== 3. MISMATCH: artifact edited after stamping =="
cp widget.py widget.bak
printf 'def sub(a, b):\n    return a - b\n' >> widget.py
expect 10 "edited body -> MISMATCH"  $VS check widget.py
cp widget.bak widget.py
expect 0 "restored -> OK"           $VS check widget.py

echo "== 3b. MISMATCH: stamp moved onto a different artifact =="
# the exact SaturnHexagon failure: claim transplanted to a sibling copy
python3 - <<'P'
src = open('widget.py').read()
stamp = src[src.index('# VERIFICATION-STAMP-BEGIN'):]
open('widget_sibling.py','w').write("def add(a, b):\n    return a * b\n\n" + stamp)
P
expect 10 "stamp on sibling copy -> MISMATCH" $VS check widget_sibling.py

echo "== 4. STALE: environment moved, file untouched =="
echo "v2.0.0" > toolversion.txt
expect 11 "toolchain moved -> STALE"  $VS check widget.py
expect 0 "--no-probe ignores env"    $VS check widget.py --no-probe
echo "v1.2.3" > toolversion.txt
expect 0 "toolchain restored -> OK"  $VS check widget.py

echo "== 5. FAIL: re-run now reports a forbidden token =="
cat > runcheck.sh <<'SH'
#!/usr/bin/env bash
echo "declaration: add"
echo "TRACEBACK: something broke"
SH
chmod +x runcheck.sh
expect 12 "forbidden token -> FAIL"   $VS check widget.py --rerun
expect 0 "check without --rerun still OK" $VS check widget.py

echo "== 5b. FAIL: declaration disappeared =="
cat > runcheck.sh <<'SH'
#!/usr/bin/env bash
echo "status: clean"
SH
chmod +x runcheck.sh
expect 12 "missing declaration -> FAIL" $VS check widget.py --rerun

echo "== 6. ERROR cases =="
printf 'x = 1\n' > plain.py
expect 13 "unstamped file -> ERROR"   $VS check plain.py
expect 13 "missing file -> ERROR"     $VS check nope.py

echo "== 7. stamp refuses to certify a failing check =="
cat > widget2.py <<'PY'
x = 1
PY
cat > badcheck.sh <<'SH'
#!/usr/bin/env bash
echo "TRACEBACK: nope"
SH
chmod +x badcheck.sh
expect 12 "stamp refuses on forbidden token" \
  $VS stamp widget2.py --prefix "# " --command "./badcheck.sh" --forbidden "TRACEBACK"
[ -f widget2.py ] && grep -q "VERIFICATION-STAMP" widget2.py && { echo "  FAIL wrote a stamp anyway"; fail=$((fail+1)); } || { echo "  ok   no stamp written"; pass=$((pass+1)); }

echo "== 8. language-agnostic prefixes =="
printf -- '-- lean-ish artifact\ndef f := 1\n' > a.lean
expect 0 "-- prefix"  $VS stamp a.lean --prefix "-- " --command "echo declaration: f" --declaration "declaration: f"
expect 0 "-- check"   $VS check a.lean
printf '// c-ish artifact\nint f(){return 1;}\n' > a.c
expect 0 "// prefix"  $VS stamp a.c --prefix "// " --command "echo declaration: f" --declaration "declaration: f"
expect 0 "// check"   $VS check a.c

echo "== 9. self-application: the tool must survive stamping itself =="
cp "$HERE/verify_stamp.py" ./vs_copy.py
cp "$HERE/test_verify_stamp.sh" ./ts_copy.sh 2>/dev/null || true
expect 0 "stamps its own source" \
  python3 ./vs_copy.py stamp ./vs_copy.py --prefix "# " --command "echo declaration: ok" --declaration "declaration: ok"
expect 0 "still imports after stamping"  python3 -c "import importlib.util,sys; sp=importlib.util.spec_from_file_location('vs','./vs_copy.py'); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); sys.exit(0 if m.BEGIN.endswith('-BEGIN') else 1)"
expect 0 "checks its own stamp"          python3 ./vs_copy.py check ./vs_copy.py
python3 - <<'P'
a=[l for l in open('vs_copy.py') if 'VERIFICATION' in l and 'MARK' in l]
print("  ok   marker definition survived" if a else "  FAIL marker definition deleted")
P

echo "== 10. a coincidental marker in prose is ERROR, not a licence to delete =="
printf '# notes\n# VERIFICATION-STAMP-BEGIN appears in this sentence\nimportant_code = 1\n# VERIFICATION-STAMP-END too\n' > prose.py
expect 13 "malformed block -> ERROR"      $VS check prose.py

echo
echo "passed $pass, failed $fail"
[ "$fail" -eq 0 ] || exit 1
