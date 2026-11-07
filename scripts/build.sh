#!/usr/bin/env bash
# Build the single-file PWA: index.html = src/top.html + src/app.js (run from anywhere)
set -euo pipefail
cd "$(dirname "$0")/.."
# weeks/*.json are inlined as WEEKS_BUILTIN (each file must be valid JSON; the app validates the content)
{ cat src/top.html; echo "<script>var WEEKS_BUILTIN=["; first=1
  for f in weeks/*.json; do [ -e "$f" ] || continue; python3 -m json.tool "$f" >/dev/null || { echo "bad JSON: $f" >&2; exit 1; }
    [ $first = 1 ] || echo ","; first=0; cat "$f"; done
  echo "];</script>"; cat src/app.js; } > index.html
echo "built index.html ($(wc -c < index.html) bytes) · $(grep -o 'pc-v[0-9]*' src/top.html | head -1) · sw: $(head -c 22 sw.js)"
