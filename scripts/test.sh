#!/usr/bin/env bash
# Build, serve the repo root on :8765 and run the Playwright suites in parallel.
#   scripts/test.sh              # full run: every suite, JOBS workers (default 3), test_sw last on its own
#   scripts/test.sh --fast       # fast tier: this week's audit + the suites that change most (about 3 min)
#   scripts/test.sh test_v26     # one or more named suites
# Needs: pip install -r requirements-dev.txt && python -m playwright install chromium
# Optional: CHROME=/usr/bin/google-chrome to use system Chrome · PY=python · JOBS=4 · WEEK=current (audit only this week)
# Per-suite output lands in test-output/<suite>.log; the summary below prints each suite's non-PASS lines.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}; JOBS=${JOBS:-3}
FULL="test_audit test_v25 test_app test_wt test_v18 test_v20 test_v24 test_v26 test_v28 test_v29 test_v30 test_v31 test_v32 test_v33 test_v34 test_v35 test_v37 test_v39 test_v40 test_v41 test_v42 test_v43 test_v44 test_v46 test_v47 test_v48 test_v49 test_v50 test_v51 test_v52 test_v53 test_v54 test_v55 test_v56 test_sw"
FAST="test_audit test_app test_v31 test_v34 test_v35 test_v37 test_v39 test_v40 test_v41 test_v42 test_v43 test_v44 test_v46 test_v47 test_v48 test_v49 test_v50 test_v51 test_v52 test_v53 test_v54 test_v55 test_v56"
if [ "${1:-}" = "--fast" ]; then SUITES=$FAST; export WEEK=${WEEK:-current}; else SUITES=${*:-$FULL}; fi
bash scripts/build.sh
mkdir -p test-output; rm -f test-output/*.rc
$PY -m http.server 8765 >/dev/null 2>&1 & SRV=$!
trap 'kill $SRV 2>/dev/null' EXIT
sleep 1
run1(){ local t=$1 out rc; out=$($PY "tests/$t.py" 2>&1); rc=$?
  { echo "== $t"; echo "$out" | grep -v '^PASS' | tail -15; } > "test-output/$t.log"
  if [ $rc -ne 0 ] || echo "$out" | grep -q '^FAIL'; then echo FAIL > "test-output/$t.rc"; else echo OK > "test-output/$t.rc"; fi; }
export -f run1; export PY
PAR=$(printf '%s\n' $SUITES | grep -v '^test_sw$' || true)
[ -n "$PAR" ] && printf '%s\n' $PAR | xargs -P "$JOBS" -I{} bash -c 'run1 {}'
# test_sw rewrites sw.js for a moment, so it never runs beside the others
printf '%s\n' $SUITES | grep -q '^test_sw$' && run1 test_sw
fail=0
for t in $SUITES; do cat "test-output/$t.log"; [ "$(cat "test-output/$t.rc" 2>/dev/null)" = OK ] || fail=1; done
[ $fail -eq 0 ] && echo "ALL SUITES PASSED" || { echo "SOME SUITES FAILED"; exit 1; }
