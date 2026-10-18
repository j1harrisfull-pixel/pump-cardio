#!/usr/bin/env bash
# Build, serve the repo root on :8765 and run the Playwright suites.
#   scripts/test.sh              # all suites
#   scripts/test.sh test_v26     # one suite
# Needs: pip install -r requirements-dev.txt && python -m playwright install chromium
# Optional: CHROME=/usr/bin/google-chrome to use system Chrome. PY=python to choose the interpreter.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}
bash scripts/build.sh
mkdir -p test-output
$PY -m http.server 8765 >/dev/null 2>&1 & SRV=$!
trap 'kill $SRV 2>/dev/null' EXIT
sleep 1
SUITES=${*:-test_app test_wt test_v18 test_v20 test_v24 test_v25 test_v26 test_v28 test_sw}
fail=0
for t in $SUITES; do
  echo "== $t"
  out=$($PY tests/$t.py 2>&1); rc=$?
  echo "$out" | grep -v '^PASS' | tail -15
  if [ $rc -ne 0 ] || echo "$out" | grep -q '^FAIL'; then fail=1; fi
done
[ $fail -eq 0 ] && echo "ALL SUITES PASSED" || { echo "SOME SUITES FAILED"; exit 1; }
