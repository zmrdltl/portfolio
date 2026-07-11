# Work

## Work Timeline

| Period | Organization | Role | Main Focus |
| --- | --- | --- | --- |
| 2025.03 - 2026.07 | ClumL | Software Engineer | Request-limiting concurrency fix, Rust-service configuration externalization, regression testing |
| 2021.10 - 2024.11 | TmaxCloud | Software Engineer | Java/TypeScript No-code platform, service-code generation validation, data-change history storage/query, entity export/import, SQL/DDL generation |

## Key Outcomes

- [ClumL](cluml.md): moved the request-limiter capacity check and reservation update into one lock scope to fix a race that had allowed requests to pass at more than 10x the effective limit, then externalized a repeated detection setting and reduced one setting-change workflow by more than 30%.
- [TmaxCloud service-code generation validation](tmaxcloud.md): executed services defined from entities and fields in the UI through generated code, then moved API-response and database-write/read checks into pre-deployment E2E validation, contributing to reducing the repeated design-validation cycle from roughly 4 weeks to roughly 2 weeks.
- [TmaxCloud data-change history](tmaxcloud.md): implemented source/history tables and insert/update/delete previous-row storage, then defined the select-SQL rule for reconstructing table state at a target point in time.
