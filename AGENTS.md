# Portfolio Local Adapter

This repository is the public MkDocs output surface for the technical portfolio.
Keep this file limited to local repository facts and local verification commands.

## External Context

Before writing, reviewing, or restructuring portfolio content, use the external career-writing source configured for this workspace.
If that source is unavailable, stop and ask the user for the portfolio writing context.
Do not recreate portfolio strategy, case selection, writing policy, review lenses, or public content boundary rules in this repository.

## Local Repository Facts

- Public pages live under `docs/`.
- Navigation is configured in `mkdocs.yml`.
- Korean Markdown is the source language. When Korean public content changes, update the matching `*.en.md` file.

## Verification

Use these local checks after content or navigation changes:

- `pnpm run lint:md`
- `pnpm run check:contract`
- `pnpm run check:public-copy`
- `.venv/bin/python scripts/check_structure.py`
- `.venv/bin/mkdocs build --strict`

When validation behavior changes, also run the matching unit test:

- `pnpm run test:contract`
- `pnpm run test:public-copy`
- `pnpm run test:structure`

For `AGENTS.md`-only changes, Markdown lint is enough unless the change affects publishing, navigation, or validation behavior.

## Publishing

- `main` is the deployed branch.
- Use `pnpm` as declared by `packageManager`.
- Deploy only reviewed public content.
