# Kim Minsik Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I am a Platform Software Engineer who connects user-defined services and product changes to working code, SQL, data flows, and test criteria.

In my recent ClumL work, I reframed a request-limiting concurrency issue in a security analysis product and set handling criteria and regression tests so over-limit requests could not enter job execution. At TmaxCloud, I worked on a No-code platform where service/API designs from the UI became executable Java code and SQL, and I made deployed apps store and query data-change history so Studio could show table state at a target point in time. In my personal product Coupler, I aligned the React Native app, API, admin web, and database around the same signup and review rules.

In open source, I have contributed to the Rust SQL engine GlueSQL. I worked on `SELECT DISTINCT`, aggregate `DISTINCT`, SQL parser and AST representation, executor and aggregate handling, Parquet storage, regression tests, and PR review.

## Representative Work

- [Change safety in a security analysis product](experience/cluml.md): reframed a wait symptom observed during customer demo server operation as a rate-limiter concurrency-correctness problem, then set reservation-state criteria and regression tests so over-limit requests could not enter job execution. I handled detection/report display consistency, Rust service configuration changes, and PR review criteria as part of the same change-safety thread.
- [No-code platform service generation and data history](experience/tmaxcloud.md): in TmaxCloud's No-code platform, I turned UI-designed service/API definitions into Java code and SQL, then built a WebSocket test page to verify request/response and DB write/read behavior before deployment. For entities with the data-history option enabled, deployment created the source table and history table together, and insert/update/delete service code saved previous row data so the platform could query table state at a target point in time.
- [Rust SQL engine open-source contribution](opensource/gluesql.md): implemented `SELECT DISTINCT` and aggregate `DISTINCT` across SQL translation, AST representation, executor de-duplication, aggregate handling, AST builder, and regression tests in GlueSQL. This work is visible through 50+ merged PRs in GitHub `is:merged` search for `gluesql/gluesql`.
- [Operating criteria for the personal product Coupler](projects/coupler.md): worked across the React Native app, API, admin web, and database; converted signup/review into staged flows; and connected TypeScript operating criteria, typecheck/migration guards, regression tests, and code review criteria to release criteria.

## Engineering Operating Perspective

I value code that is consistent, extensible, cohesive, loosely coupled, and clear in its separation of responsibilities.

As some repetitive implementation work becomes less of a bottleneck, I consider problem definition, domain policies, responsibility boundaries, test criteria, and review criteria more important. Good engineering documents should become executable guidance that helps teammates and automation tools implement and review from the same perspective.

I describe this in more detail in [Principles](engineering-principles.md).

## Technical Focus Areas

- Engineering workflow: designing change units and validation criteria so docs, type checks, tests, reviews, and release criteria move together
- Service contracts: aligning app/API/admin/database behavior through server response contracts, review policies, permission rules, and routing rules
- Service-generation platforms: connecting UI-defined metadata/schema to Java service code, SQL/DDL, DB verification, data-change history, and entity export/import
- Change safety: separating operational symptoms, configuration changes, and display-consistency issues into reproduction conditions, completion criteria, regression tests, and PR review criteria
- Rust/SQL: Rust SQL engine work, SQL parser/AST, executor/aggregate handling, storage, regression tests, and code review

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
