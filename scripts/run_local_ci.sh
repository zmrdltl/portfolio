#!/usr/bin/env bash
set -euo pipefail

pnpm install --frozen-lockfile
pnpm run lint:md

python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

pnpm run test:structure
pnpm run test:contract
pnpm run test:public-copy
pnpm run check:structure
pnpm run check:contract
pnpm run check:public-copy
.venv/bin/mkdocs build --strict
