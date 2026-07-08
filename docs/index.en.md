# Kim Minsik Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I am a Platform Software Engineer who turns fragile state transitions, data flows, and service contracts in changing products and platforms into verifiable criteria.

In my current role, I closed a request-limiting concurrency issue with reproducible invariants and regression-test criteria. In prior platform work, I made generated services and data history verifiable before deployment. In product development, I align app, API, admin, and database behavior around shared state contracts and release criteria.

In AI-assisted development, I focus less on code generation itself and more on keeping problem definitions, docs, type checks, regression tests, and review criteria aligned so only operable changes remain. I support this with public Rust SQL engine work. In GlueSQL, I left query semantics, AST/execution-path, storage-surface, and test-suite work in PR and review records.

## Representative Work

- [Change safety in a security analysis product](experience/cluml.md): reframed a wait symptom observed during customer demo server operation as a rate-limiter concurrency-correctness problem, then closed it with invariants and regression-test criteria that prevent over-limit request admission. I handled detection/report display consistency, Rust service configuration changes, and PR review criteria as part of the same change-safety thread.
- [Generated-platform validation and data history](experience/tmaxcloud.md): moved generated-service request/response and DB write/read checks from post-deployment verification into pre-deployment E2E validation. I kept change-history feature (CAU) tables and row-snapshot copy flow inside the same generation boundary as generated CRUD service code.
- [Rust SQL engine open-source contribution](opensource/gluesql.md): implemented and validated `SELECT DISTINCT` and aggregate `DISTINCT` across SQL translation, AST/query representation, executor de-duplication, aggregate state, AST builder, and test-suite paths in GlueSQL. This work is visible through 45+ merged PRs plus review/docs records in `gluesql/gluesql`.
- [Product state contracts and operating criteria](projects/coupler.md): aligned signup/review state models across a React Native app, API, admin web, and database, then connected TypeScript operating criteria, typecheck/migration guards, regression validation, and code review criteria into product-change standards.

## Engineering Operating Perspective

I value code that is consistent, extensible, cohesive, loosely coupled, and clear in its separation of responsibilities.

As some repetitive implementation work becomes less of a bottleneck, I consider problem definition, domain policies, responsibility boundaries, test criteria, and review criteria more important. Good engineering documents should become executable guidance that helps teammates and automation tools implement and review from the same perspective.

I describe this in more detail in [Principles](engineering-principles.md).

## Technical Focus Areas

- AI-assisted engineering workflow: designing change units and validation criteria so docs, type checks, tests, reviews, and release criteria move together
- Service contract: aligning app/API/admin/database behavior through server response contracts, review policies, permission criteria, and routing criteria
- Generated platform: connecting metadata and schema information to SQL/DDL, generated service code, DB verification, change history, and test criteria
- Change safety: separating operational symptoms, configuration changes, and display-consistency issues into reproduction conditions, completion criteria, regression tests, and PR review criteria
- Rust/SQL: SQL engine internals, parser/AST, storage, Rust open-source contribution, and code review

## Skills

- Languages: Rust, Java, TypeScript, SQL
- Backend/Data: SQL/DDL Generator, GraphQL, WebSocket, PostgreSQL, MySQL, Tibero
- Frontend: React, React Native, Material UI, React Flow
- Infra/Tools: Kubernetes, Terraform, GitHub Actions, AWS

## Links

- [Email](mailto:meenseek5929@naver.com)
- [GitHub](https://github.com/zmrdltl)

## Navigation

- [Work](experience/index.md)
- [ClumL](experience/cluml.md)
- [TmaxCloud](experience/tmaxcloud.md)
- [GlueSQL](opensource/gluesql.md)
- [Coupler](projects/coupler.md)
- [Principles](engineering-principles.md)
- [Activities](activities/index.md)
