# Kim Minsik Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I am a Platform Software Engineer who connects service design information and domain rules to SQL/DDL, service code, test criteria, and review criteria so platform features and change safety move together.

I organize representative work around three problem areas and four representative cases: using validation criteria to close a race condition found during customer demo server operation while keeping detection and report displays consistent, making generated services and data history verifiable in metadata-driven platforms, and implementing service contracts plus test/review criteria in a Rust SQL engine and product operation work.

## Representative Work

- [Change safety in a security analysis product](experience/cluml.md): reframed a wait symptom observed during customer demo server operation as a rate-limiter concurrency problem and set invariant and regression-test criteria to prevent over-limit request admission. I also split detection/report display issues into query/API contract and review-validation scopes.
- [Generated-service validation and change-history criteria](experience/tmaxcloud.md): built an E2E test page to verify generated-service request/response and DB write/read behavior before deployment, and connected CAU change-history tables with row-snapshot copy flow in generated CRUD service code.
- [Rust SQL engine open-source contribution](opensource/gluesql.md): implemented and validated `SELECT DISTINCT` and aggregate `DISTINCT` across SQL translation, AST/query representation, executor de-duplication, aggregate state, AST builder, and test-suite paths in GlueSQL.
- [State contracts and review criteria for a personal product](projects/coupler.md): organized signup/review state contracts, TypeScript operating criteria, DB/release guardrails, and code review criteria across a React Native app, API, and admin web.

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
- [Principles](engineering-principles.md)
- [GlueSQL](opensource/gluesql.md)
- [Coupler](projects/coupler.md)
- [Activities](activities/index.md)
