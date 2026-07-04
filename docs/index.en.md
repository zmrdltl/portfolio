# Kim Minsik Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I am a Platform Software Engineer who closes backend/platform problems through service contracts, data-state criteria, and tests. At ClumL, I organize request-limiting concurrency and display-consistency issues in a security analysis product into validation criteria. At TmaxCloud, I implemented flows that connect UI metadata to generated service code and DB change history. In GlueSQL, I left Rust SQL engine parser/AST/executor/test-suite changes in 45+ merged PRs and review records. In Coupler, I turned state contracts and release criteria across a React Native app, API, and admin web into product operating standards.

I organize representative work around four work streams. In my current role, I work on change safety in a security analysis product. In my previous role, I made generated services and data history verifiable in a metadata-driven platform. In open source, I left Rust SQL engine query semantics and test-suite work in PR and review records. In personal product work, I turned state contracts and release criteria into product operating standards.

## Representative Work

- [Change safety in a security analysis product](experience/cluml.md): reframed a wait symptom observed during customer demo server operation as a rate-limiter concurrency problem, then defined invariants and regression-test criteria that prevent over-limit request admission. I also split detection/report display issues into query/API contracts, event context, and review criteria.
- [Generated-service validation and change-history criteria](experience/tmaxcloud.md): moved generated-service request/response and DB write/read checks from post-deployment verification into pre-deployment E2E validation. I kept CAU change-history tables and row-snapshot copy flow inside the same generation boundary as generated CRUD service code.
- [Rust SQL engine open-source contribution](opensource/gluesql.md): implemented and validated `SELECT DISTINCT` and aggregate `DISTINCT` across SQL translation, AST/query representation, executor de-duplication, aggregate state, AST builder, and test-suite paths in GlueSQL. This work is visible through 45+ merged PRs plus review/docs records in `gluesql/gluesql`.
- [State contracts and review criteria for a personal product](projects/coupler.md): organized signup/review state contracts, TypeScript operating criteria, DB/release guardrails, and code review criteria across a React Native app, API, and admin web. Using Meta SDK postback data, I confirmed that review-request-related events over one month increased from roughly 40 to roughly 1.1k; I use this only as event-count evidence, not as a user-count or conversion-rate claim.

## Engineering Perspective

I value code that is consistent, extensible, cohesive, loosely coupled, and clear in its separation of responsibilities.

As some repetitive implementation work becomes less of a bottleneck, I consider problem definition, domain policies, responsibility boundaries, test criteria, and review criteria more important. Good engineering documents should become executable guidance that helps teammates and AI agents implement and review from the same perspective.

I describe this in more detail in [Principles](engineering-principles.md).

## Technical Focus Areas

- Platform: connecting metadata and schema information to SQL/DDL, generated service code, DB verification, change history, and test criteria
- Rust/SQL: SQL engine internals, parser/AST, storage, Rust open-source contribution, and code review
- Product quality: display consistency in security event analysis products, Rust service compatibility checks, React Native product operation, TypeScript migration, and signup/review flow cleanup
- Review system: requirements-based work definition, completion criteria, test coverage, change-safety review, and verification criteria for AI-assisted development

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
