#!/usr/bin/env bash
# Restore PNG references from text sidecars (GitHub push path is text-only for this bot).
set -euo pipefail
cd "$(dirname "$0")"
for f in light-week.png light-session.png light-emom.png; do
  base64 -d "${f}.b64" > "$f"
  echo "restored $f ($(wc -c < "$f") bytes)"
done
