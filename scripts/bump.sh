#!/usr/bin/env bash
# Bump the release marker everywhere: scripts/bump.sh 28   (pc-v27 -> pc-v28)
set -euo pipefail
cd "$(dirname "$0")/.."
NEW="pc-v$1"; OLD=$(grep -o 'pc-v[0-9]*' sw.js | head -1)
sed -i "s/$OLD/$NEW/g" src/top.html sw.js tests/test_sw.py
echo "$OLD -> $NEW"; head -c 22 sw.js; echo
