# Work

## Timeline

| Period | Organization | Role | Main Focus |
| --- | --- | --- | --- |
| 2025.03 - 2026.07 | ClumL | Software Engineer | Security event analysis product suite, request-limiting concurrency validation criteria, detection/report display consistency, Rust service compatibility checks, PR review |
| 2021.10 - 2024.11 | TmaxCloud | Software Engineer | Java/TypeScript No-code platform, generated-service E2E validation, change-history feature (CAU), SQL/DDL generation |

## Career Snapshot

- [ClumL](cluml.md): reframed a wait symptom observed during customer demo server operation as a request-limiting correctness problem, then closed an over-limit concurrency issue that had admitted more than 10x the allowed request volume with invariants and regression-test criteria.
- [TmaxCloud generated service](tmaxcloud.md): moved generated-service request/response and DB write/read checks in a No-code platform into pre-deployment E2E validation, contributing to reducing the repeated design-validation cycle from roughly 4 weeks to roughly 2 weeks under the working conditions at the time.
- [TmaxCloud change-history feature (CAU)](tmaxcloud.md): designed and implemented a generation boundary that keeps original tables, change-history tables, generated CRUD service row-snapshot copy flow, and point-in-time select SQL criteria together.

## Direction

My core background is backend/platform engineering that connects service design information and schema to code, SQL, data flows, and verification criteria.

At ClumL, I separated operational symptoms into narrow correctness and change-safety problems, then closed them with reproduction conditions, completion criteria, regression tests, and PR review criteria.

At TmaxCloud, I implemented backend/platform boundaries that connected app, entity, and service/API definitions from the UI to SQL/DDL, generated service code, DB verification, and change-history criteria.

My GlueSQL open-source work is a representative technical-depth signal: SQL engine internals, parser/AST design, Rust-based data processing, storage support, test suites, mentoring, and code review.

In recent development work, I consider documentation and verification criteria as important as implementation quality. I aim to leave requirements, domain policies, responsibility boundaries, test criteria, and review criteria in clear documents so teammates can implement and review using the same standards.
