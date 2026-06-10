# Repository Guidelines

## Purpose

This repository is a public MkDocs portfolio site.
It contains curated, public-facing career and project documentation only.

## Content Rules

- Do not add private notes, investigation logs, draft reasoning, or internal-only context.
- Do not include private company links, private issue or PR links, credentials, personal identifiers beyond public contact information, or non-public implementation details.
- Keep detailed research notes in a private or local workspace, then copy only reviewed public summaries into this repository.
- Prefer concise career and project summaries with public evidence links.
- Use Korean as the primary source language for public portfolio pages.
- Keep English translations in matching `*.en.md` files and update them when the Korean source changes.
- Do not publish raw source notes from Notion, PDFs, or local draft files.
- Add the minimum words needed to state scope, role, result, evidence, and skills.

## Writing Rules

- Prefer editing an existing page over adding a new page or section.
- Separate confirmed facts, interpretation, and suggestions.
- Do not add a claim unless it is supported by public evidence or the reviewed Korean source text.
- Keep public pages readable without private context.
- When changing Korean source pages, update the matching English `*.en.md` page in the same change.

## Review Rules

- Findings come first, ordered by risk.
- Check public-safety issues: private notes, internal links, raw investigation text, credentials, and unsupported personal identifiers.
- Check claim quality: role, scope, metric, date, and evidence must not be stronger than the source supports.
- Check Korean/English parity for changed pages.
- Check navigation links, `pnpm run lint:md`, and `mkdocs build --strict`.

## Evaluation Criteria

- Stable: the same reviewed source should produce the same public wording.
- Minimal: remove or shorten before adding new wording.
- Defensible: metrics and achievements must be traceable to public evidence or reviewed source text.
- Consistent: terminology, dates, role names, and page structure must match across Korean and English.

## Structure

- `docs/experience/`: company experience pages
- `docs/projects/`: selected project pages
- `docs/opensource/`: open-source work
- `docs/evidence/`: public links and references only

## Publishing

- `main` is the deployed branch.
- Pull requests should pass Markdown lint and the MkDocs build before merging.
- Use `pnpm` 11.5.2 for Node-based tooling.
- Run `pnpm run lint:md` after editing Markdown files.
- Deploy only reviewed public content.
