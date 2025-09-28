#!/usr/bin/env bash
set -euo pipefail
IMG="${1:-myapp:dev}"
docker build -t "$IMG" .
echo "[check] user should be non-root"
docker run --rm "$IMG" id -u | grep -qv '^0$'
echo "[ok] non-root"
