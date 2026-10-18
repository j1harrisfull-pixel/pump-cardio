#!/usr/bin/env bash
# Build the single-file PWA: index.html = src/top.html + src/app.js (run from anywhere)
set -euo pipefail
cd "$(dirname "$0")/.."
cat src/top.html src/app.js > index.html
echo "built index.html ($(wc -c < index.html) bytes) · $(grep -o 'pc-v[0-9]*' src/top.html | head -1) · sw: $(head -c 22 sw.js)"
