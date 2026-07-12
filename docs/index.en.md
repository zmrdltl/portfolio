# Kim Minsik Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I turn services defined from entities and fields in a UI into Java code and SQL, then verify API calls and database effects as one platform workflow.

Most recently, I fixed request-limiting concurrency and externalized a repeated operational setting in Rust services for a security analysis product. I also implemented pre-deployment generated-code validation and data-history storage in a No-code platform, plus `DISTINCT` in the Rust SQL engine GlueSQL.

## Representative Work

- [Rust service improvements in a security analysis product](experience/cluml.md): moved the request-limiter capacity check and state update into one lock scope, fixing a race that had allowed requests to pass at more than 10x the effective limit. I also externalized a repeatedly adjusted detection setting, reducing the work for one setting change by more than 30%.
- [No-code platform service generation and data history](experience/tmaxcloud.md): in TmaxCloud's No-code platform, I generated Java code and SQL from services defined through UI entities and fields. A WebSocket test page made API responses and database writes/reads verifiable before deployment. I implemented history-table and previous-row storage flows, then defined the select-SQL rule for reconstructing table state at a target point in time.
- [Rust SQL engine open-source contribution](opensource/gluesql.md): implemented `SELECT DISTINCT` and aggregate `DISTINCT` across SQL translation, AST representation, executor de-duplication, aggregate handling, AST builder, and regression tests in GlueSQL. This work is visible through 50 merged PRs under GitHub `is:merged` search for `gluesql/gluesql`.
- [Development lead for a contracted mobile dating app project](projects/coupler.md): reduced a roughly 30-field signup request into a staged review flow centered on basic information and required profile material. I aligned the app, API, Admin, and database around a shared signup/review state contract so associate and full-member reviews could be submitted in parallel, then documented policy, flow, architecture, release, deployment, and rollback criteria in public development docs. The Meta SDK CompleteRegistration event, recorded when a person reached the first signup review, was observed at roughly 10 events before the signup/review-flow redesign and roughly 100 afterward.

## Skills

- Languages: Java, Rust, TypeScript, SQL
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
