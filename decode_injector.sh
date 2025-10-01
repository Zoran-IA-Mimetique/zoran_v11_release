#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <injector_base64_file>"
  exit 2
fi
IN="$1"
OUT_GZ="/tmp/injector_decoded.gz"
OUT_YML="/tmp/injector_decoded.yml"
base64 -d "$IN" > "$OUT_GZ"
gunzip -c "$OUT_GZ" > "$OUT_YML"
echo "Decoded YAML written to: $OUT_YML"
echo "Verify SHA256: sha256sum $OUT_YML"
