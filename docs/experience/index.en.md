# Work

## Work Timeline

| Period | Organization | Role | Main Focus |
| --- | --- | --- | --- |
| 2025.03 - 2026.07 | ClumL | Software Engineer | Security event analysis product suite, request-limiting concurrency validation criteria, detection/report display consistency, Rust service compatibility checks, PR review |
| 2021.10 - 2024.11 | TmaxCloud | Software Engineer | Java/TypeScript No-code platform, service/API code-generation validation, data-change history storage/query, entity export/import, SQL/DDL generation |

## Key Outcomes

- [ClumL](cluml.md): reframed a wait symptom observed during customer demo server operation as a request-limiting correctness problem, then organized an over-limit concurrency issue that allowed more than 10x the allowed request volume to pass into handling criteria and regression tests.
- [TmaxCloud service/API code-generation validation](tmaxcloud.md): moved request/response and DB write/read checks for UI-defined service/API code into pre-deployment E2E validation, contributing to reducing the repeated design-validation cycle from roughly 4 weeks to roughly 2 weeks.
- [TmaxCloud data-change history](tmaxcloud.md): designed and implemented source tables, history tables, and insert/update/delete service code that saved previous row data so the platform could query table state at a target point in time.
