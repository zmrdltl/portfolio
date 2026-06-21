# Repository Guidelines

## Purpose

This repository is a public MkDocs technical portfolio site, not application code.
It contains only curated public-facing career, open-source, project, activity, engineering principles, and evidence documentation.

This site complements a submitted resume. It is not the resume itself; it provides technical context and public evidence that are too detailed for a resume.

## Content Rules

- Keep research notes private/local; publish only reviewed public summaries.
- Do not publish private notes, internal context, private links, credentials, personal identifiers beyond public contact information, non-public implementation details, raw source notes, unapproved Google Drive folders, certificate bundles, academic records, military records, or other administrative proof documents. User-approved, privacy-safe evidence folders may be linked when they directly support a public claim.
- Add no claim unless it is supported by public evidence, reviewed source text, or explicit user confirmation.
- Do not fill blanks, dates, metrics, roles, names, links, outcomes, or rationale by assumption; ask the user when a field would require guessing.
- Use Korean as the source language; update the matching `*.en.md` file when Korean content changes.
- Use the minimum words needed to state scope, role, result, evidence, and skills.

## Writing Rules

- Prefer editing an existing page over adding a new page or section.
- Separate confirmed facts, interpretation, and suggestions.
- Do not use conversation-only labels, temporary wording, or private shorthand from user-agent discussion unless the user explicitly approves it for publication.
- Avoid internal-document expressions and unexplained abbreviations in public pages and commit messages.
- Keep public pages readable without private context.
- Use concise wording, but keep enough context for each page to stand on its own.

## Review Rules

- Apply these review rules and all Review Personas to every review request unless the user explicitly limits the scope.
- Findings come first, ordered by risk.
- Check public-safety issues: private notes, internal links, raw investigation text, credentials, and unsupported personal identifiers.
- Check claim quality: role, scope, metric, date, and evidence must not be stronger than the source supports.
- Check Korean/English parity for changed pages.
- Check navigation links, `pnpm run lint:md`, and `mkdocs build --strict` when content or navigation changes. For AGENTS-only changes, Markdown lint is enough unless the change affects publishing or validation rules.

Review the portfolio as a technical evidence site:

- Do not apply resume-only rules such as 30-60 second scanability, PDF impact sections, or aggressive compression unless the user asks for resume/PDF copy.
- For the homepage, check orientation: a reader should understand the portfolio's technical axes and where to go next.
- For detail pages, check defensibility: claims should be supported by public evidence, reviewed source text, or explicit user confirmation, and private repositories should be represented only through safe public summaries or representative public links.
- Treat private repository limitations as a constraint, not a defect. A representative public docs link is acceptable when code repositories cannot be public.

## Review Personas

Use these personas as review lenses only; they do not override the content rules and must not create new claims.

| Persona | Checks |
| --- | --- |
| Hiring reviewer | Role, scope, result, and evidence are easy to locate and understand without private context |
| Engineering reviewer | Technical ownership, boundaries, testing, review, and documentation standards are concrete but not overstated |
| Evidence reviewer | Public links support the claim; user-confirmed facts are not strengthened; unverifiable fields are marked as needing confirmation |
| Public-safety reviewer | Private information, internal context, unsupported identifiers, and credential archives are absent |
| Maintainer | Section ownership, Korean/English parity, navigation, and commit scope stay consistent |

Evidence review is limited to available public links, reviewed source text, and explicit user confirmation in this work.
If a date, metric, role, link, or outcome cannot be checked from those sources, do not infer it; flag it as needing user confirmation.

## Evaluation Criteria

- Stable: the same reviewed source should produce the same public wording.
- Minimal: remove or shorten before adding new wording.
- Defensible: metrics and achievements must be traceable to public evidence or reviewed source text.
- Consistent: terminology, dates, role names, and page structure must match across Korean and English.

## Structure

Use short navigation labels, but keep directory names explicit.

| Path | Ownership |
| --- | --- |
| `docs/experience/` | Organization work with role, period, and product responsibility |
| `docs/engineering-principles.md` | Public engineering principles and AI-assisted development criteria |
| `docs/opensource/` | Public repository work where code, PRs, review, or technical contribution is the primary signal |
| `docs/projects/` | Personal products, client delivery, student startup, graduation, technical challenge, or selected artifact-centered projects that are not regular employment history |
| `docs/activities/` | Education, mentoring, community, awards, and other supporting activities |
| `docs/evidence/` | Public technical evidence links only, not a credential archive |

If more than one section could apply, choose the section by primary signal: regular employment or organization-owned product responsibility goes to `experience/`, repository contribution to `opensource/`, personal/client/student/artifact-centered work goes to `projects/`, supporting history to `activities/`, and links only to `evidence/`.
Keep awards and certificates as short text in `activities/`; link only public, privacy-safe official pages or explicitly user-approved evidence folders when they add real signal.

Recommended detail-page shape:

```text
Overview
Role and scope
Problem and constraints
Design and implementation
Validation, metrics, or quality criteria
Result
Public evidence or representative public reference
Skills
```

Use this shape as guidance, not as a required template. Omit sections that would force unsupported claims or expose private details.

## Publishing

- `main` is the deployed branch.
- Pull requests should pass Markdown lint and the MkDocs build before merging.
- Use `pnpm` 11.5.2 for Node-based tooling.
- Run `pnpm run lint:md` after editing Markdown files.
- Deploy only reviewed public content.

## Commit Rules

- Stage only related hunks.
- Use Conventional Commits with `docs(scope): summary`.
- Prefer these scopes: `agents`, `structure`, `principles`, `experience`, `opensource`, `projects`, `activities`, `evidence`, `i18n`, `build`.
- Keep the summary concise and specific.
- Use only `What:` and `Why:` body lines when the change affects structure, classification, public-safety rules, or claim strength.
- `What:` must describe only the staged document changes.
- `Why:` must use only confirmed user intent, reviewed source text, or public evidence; do not invent rationale.
- Do not use conversation-only labels, internal-document expressions, or unexplained abbreviations in commit messages.
- Omit the body only for trivial typo, formatting, or link-only fixes.
