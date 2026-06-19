#!/usr/bin/env bash
set -euo pipefail

NODE_BIN="${NODE_BIN:-node}"

"$NODE_BIN" --check docs/script.js
echo "JavaScript syntax check passed."
