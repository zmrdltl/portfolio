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

## Public Wording Quality Gate

Treat public portfolio wording as a reviewed interface, not free-form copy.

- A heading must name the concrete subject and the work performed. Do not use an abstract noun such as `계약`, `경계`, `이관`, `전환`, `검토`, `설정`, `설계`, `개선`, `최적화`, `검증`, `동기화`, or `구현` without naming the API, data, dependency, screen, query, or other affected artifact.
- A core claim must make the contribution relationship readable: who acted, what changed, and how the result was checked. Do not replace these with curator-facing abstractions.
- A technology keyword must be traceable to a sentence on the same project page and to the external career-writing source. Do not add a keyword only to improve search coverage.
- Quantitative wording must retain its comparison condition, contribution boundary, and causal limits.
- Write Korean and English as two natural descriptions of the same fact. Do not preserve Korean word order or abstract nouns when they produce unnatural English.
- When fixing a wording regression, add or update a public-copy test so the rejected wording cannot return silently.

Before completing a public-copy change, inspect every changed heading, table cell, technology item, and quantitative sentence. Ask whether a reader can identify the subject without following another link.

## Verification

Use these local checks after content or navigation changes:

- `pnpm run ci:local` before pushing `main` changes
- `pnpm run check:actions` after pushing `main` changes
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

- `main` is the reviewed source branch. GitHub Pages deployment is manual.
- Use `pnpm` as declared by `packageManager`.
- Deploy only when the user explicitly asks to publish the current reviewed public content.
- Configure hooks with `pnpm run setup:githooks` in local clones that publish this repository.
- Before pushing `main`, run `pnpm run ci:local`; the repository pre-push hook runs the same command when hooks are configured.
- After pushing `main`, run `pnpm run check:actions` and verify the GitHub Actions build status. Do not manually dispatch the deploy workflow unless the user asks for deployment. If GitHub cancels before job steps start because a hosted runner was not acquired, rerun the workflow rather than treating that as a content failure.
