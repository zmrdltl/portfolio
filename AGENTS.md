# Portfolio Local Adapter

This repository is the public MkDocs output surface for the technical portfolio.
Keep this file limited to local repository facts and local verification commands.

## External Context

Repository-local inspection may report observations from the current public files,
navigation, wording, and checks without external context.
Before recommending changes to portfolio strategy, case selection, page structure,
public wording, or factual claims, use the external career-writing source configured
for this workspace. If it is unavailable, stop at repository observations and state
the missing verification instead of presenting a recommendation.

Do not recreate portfolio strategy, case selection, writing policy, review lenses, or public content boundary rules in this repository.
Before completing any portfolio modification, use that external source's policy-synchronization gate and report whether the external policy source required an update. Keep the decision criteria in the external source rather than copying them here.

## Local Repository Facts

- Public pages live under `docs/`.
- Navigation is configured in `mkdocs.yml`.
- Korean Markdown is the source language. When Korean public content changes, update the matching `*.en.md` file.
- Use `diagram-design` for new diagrams.

## Public Wording Quality Gate

Use the external career-writing source's public wording and verification contracts.
The checks under `scripts/` and their unit tests are local enforcement adapters, not the source of portfolio writing policy.
When a durable wording rule changes, update its external owner first and then align the local check and regression test.

## Verification

Use these local checks after content or navigation changes:

- `pnpm run ci:local` before pushing `main` changes
- `pnpm run check:actions` after pushing `main` changes
- `pnpm run lint:md`
- `pnpm run check:contract`
- `pnpm run check:public-copy`
- `.venv/bin/python scripts/check_structure.py`
- `.venv/bin/mkdocs build --strict`

When a table, diagram, navigation element, grid, or layout changes, also inspect the rendered result at a narrow mobile viewport and a desktop viewport using the external policy's render acceptance criteria.

When validation behavior changes, also run the matching unit test:

- `pnpm run test:contract`
- `pnpm run test:public-copy`
- `pnpm run test:structure`

For `AGENTS.md`-only changes, Markdown lint is enough unless the change affects publishing, navigation, or validation behavior.

## Publishing

- `main` is the reviewed source branch. GitHub Pages deployment is manual.
- Use `pnpm` as declared by `packageManager`.
- Deploy only when the user explicitly asks to publish the current reviewed public content.
- Configure hooks with `pnpm run setup:githooks` in local clones that publish this repository.
- Before pushing `main`, run `pnpm run ci:local`; the repository pre-push hook runs the same command when hooks are configured.
- After pushing `main`, run `pnpm run check:actions` and verify the GitHub Actions build status. Do not manually dispatch the deploy workflow unless the user asks for deployment. If GitHub cancels before job steps start because a hosted runner was not acquired, rerun the workflow rather than treating that as a content failure.
