# Portfolio diagram-design style guide

## Scope

This file owns only the portfolio's project-local visual tokens and SVG embedding implementation.

- For diagram type selection, layout, connector construction, complexity limits, and the taste gate, follow the installed `diagram-design` skill's `SKILL.md` and the selected `references/type-*.md`.
- For shared semantic token behavior, typography roles, and export procedure, follow `diagram-design/references/style-guide.md` and `diagram-design/references/export.md`.
- For portfolio structure, public wording, claims, review, and verification policy, follow the external source routed by this repository's `AGENTS.md`.
- Do not copy those external rules into this file.

## Local source anchors

The selected values and embedding behavior below are grounded in these repository files:

- `mkdocs.yml` configures the light `default` scheme with `blue grey` as the primary palette and `indigo` as the accent palette.
- `docs/assets/stylesheets/extra.css` supplies the `#fafafa` editorial wrapper background and owns its border, radius, responsive width, and narrow-screen scrolling behavior.
- `docs/assets/diagrams/coupler-application-lifecycle.ko.svg` and `docs/assets/diagrams/coupler-application-lifecycle.en.svg` provide the current semantic colors, font stacks, node treatments, and marker treatments.
- `docs/assets/diagrams/coupler-event-lifecycle.ko.svg` and `docs/assets/diagrams/coupler-event-lifecycle.en.svg` repeat the same visual system and confirm that it is shared across the existing editorial SVGs.

## Selected visual tokens

Use this table as the project-local source of selected token values. `rule` is derived from the locally observed `ink` value at 12% opacity, and `soft` is an accessibility-adjusted selection based on the existing soft token; the other values are normalized from the source files above.

| Role | Light value | Local basis |
| --- | --- | --- |
| `paper` | `#f5f5f5` | Existing lifecycle SVGs |
| `paper-2` | `#fafafa` | `docs/assets/stylesheets/extra.css` |
| `surface` | `#ffffff` | Existing lifecycle SVG node fill |
| `ink` | `#2d3142` | Existing lifecycle SVGs |
| `muted` | `#4f5d75` | Existing lifecycle SVGs |
| `soft` | `#667085` | Darkened from the existing soft token to 4.56:1 contrast on paper |
| `rule` | `rgba(45, 49, 66, 0.12)` | `ink` derived at 12% opacity |
| `accent` | `#4051b5` | Existing lifecycle SVGs and the MkDocs indigo accent direction |
| `accent-tint` | `rgba(64, 81, 181, 0.08)` | Existing lifecycle SVGs |
| `terminal-tint` | `rgba(45, 49, 66, 0.05)` | Existing lifecycle SVG terminal-state fill |
| `link` | `#2e5aa8` | Existing lifecycle SVGs |

Keep small required labels on `muted`; use `soft` only for nonessential secondary labels.

Only the light skin is defined because `mkdocs.yml` currently configures only the light `default` scheme. Add a dark skin only after its tokens and rendered contrast have been selected and verified separately.

## Typography tokens

The existing lifecycle SVGs import these three families and apply Geist to readable state names and Geist Mono to technical state and transition labels.

| Role | Family |
| --- | --- |
| `title`, `callout` | `Instrument Serif`, serif |
| `node-name` | `Geist`, `-apple-system`, `BlinkMacSystemFont`, `Apple SD Gothic Neo`, `Noto Sans KR`, `Segoe UI`, sans-serif |
| `sublabel`, `eyebrow`, `arrow-label` | `Geist Mono`, `ui-monospace`, `SFMono-Regular`, `Menlo`, `Consolas`, monospace |

Use the sizes, weights, tracking, and role restrictions defined by the shared `diagram-design` style guide.

## Portfolio SVG embedding

1. Build the diagram with `diagram-design`, then export the diagram-only SVG for portfolio embedding.
2. Store the deliverable under `docs/assets/diagrams/` as locale-paired files: `<slug>.ko.svg` and `<slug>.en.svg`.
3. Keep both locale files structurally equivalent. Localize visible labels, `<title>`, and `<desc>` without changing the represented states, relationships, or emphasis.
4. Make each SVG self-contained: inline its token declarations, font stacks, marker definitions, and component styles. Do not depend on CSS inheritance through the embedding page.
5. Set the root SVG to `role="img"` with `aria-labelledby="title desc"`, and provide localized `<title id="title">` and `<desc id="desc">` elements.
6. Embed the asset with an `<img>` inside `.editorial-diagram-scroll`. Give the focusable scroll wrapper `role="group"`, `tabindex="0"`, and a concise localized `aria-label`; supply concise page-local `alt` text, using an empty `alt` only when adjacent prose fully duplicates the diagram.
7. Leave responsive width, narrow-screen scrolling, outer background, border, radius, and padding to `.editorial-diagram-scroll`; do not reproduce that container chrome inside the SVG.
8. Keep all project colors referenced through the semantic roles above. Diagram-specific SVG files may inline their resolved values but must not introduce a competing palette.
