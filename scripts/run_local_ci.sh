#!/usr/bin/env bash
set -euo pipefail

echo "Removing macOS Finder metadata from docs..."
find docs -type f -name '.DS_Store' -delete

pnpm install --frozen-lockfile
pnpm run lint:md

python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

pnpm run test:structure
pnpm run test:contract
pnpm run test:public-copy
pnpm run test:built-site
pnpm run check:structure
pnpm run check:contract
pnpm run check:public-copy
.venv/bin/mkdocs build --strict
pnpm run check:built-site
