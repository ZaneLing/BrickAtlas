#!/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PATH="$ROOT/.tools/node-v22.23.2-darwin-arm64/bin:$PATH"
cd "$ROOT"
if ! command -v node >/dev/null 2>&1; then
  printf 'Node.js 22+ is required: https://nodejs.org/\n'
  exit 1
fi
if [ ! -d node_modules ]; then
  npm ci
fi
exec npm run start:local
