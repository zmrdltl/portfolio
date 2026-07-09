# Kim Minsik Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I am a Platform Software Engineer who turns UI-defined service/API designs into code and SQL, then checks whether product changes are reflected in API responses, database state, tests, and release criteria.

In my recent ClumL work, I reframed a request-limiting concurrency issue in a security analysis product and set handling criteria and regression tests so over-limit requests could not enter job execution. At TmaxCloud's No-code platform, I made UI-designed service/API definitions generate Java code and SQL, then made request/response and DB write/read behavior checkable before deployment. I also made deployed apps store and query data-change history so Studio could show table state at a target point in time. At Coupler, I lead development for a mobile dating app and rebuilt signup/review flows across the React Native app, API, admin web, and database.

In open source, I have contributed to the Rust SQL engine GlueSQL. I contributed `SELECT DISTINCT` and aggregate `DISTINCT` handling, SQL parser and AST representation, executor and aggregate behavior, Parquet storage, regression tests, and PR review.

## Representative Work

- [Request-limiting correctness in a security analysis product](experience/cluml.md): reframed a long-wait symptom observed during customer demo server operation as a rate-limiter concurrency problem. I identified where concurrent requests could read the same pre-reservation state and pass beyond the limit, then set acceptance and regression-test criteria so over-limit requests are stopped before job execution.
- [No-code platform service generation and data history](experience/tmaxcloud.md): in TmaxCloud's No-code platform, I turned UI-designed service/API definitions into Java code and SQL, then built a WebSocket test page to verify request/response and DB write/read behavior before deployment. For entities with the data-history option enabled, deployment created the source table and history table together, and insert/update/delete service code saved previous row data so the platform could query table state at a target point in time.
- [Rust SQL engine open-source contribution](opensource/gluesql.md): implemented `SELECT DISTINCT` and aggregate `DISTINCT` across SQL translation, AST representation, executor de-duplication, aggregate handling, AST builder, and regression tests in GlueSQL. This work is visible through 50+ merged PRs in GitHub `is:merged` search for `gluesql/gluesql`.
- [Development lead for a mobile dating app](projects/coupler.md): reduced a roughly 30-field signup request into a staged review flow centered on basic information and required profile material. I aligned app/API/Admin/database state so associate and full-member reviews could be submitted in parallel, and Meta SDK postback event count showed one-month review-request reach events increasing from roughly 50 to roughly 1.1k.

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
