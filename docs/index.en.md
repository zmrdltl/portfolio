# Minsik Kim Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I have worked on data, state, and concurrency problems across code-generation platforms, Rust services, a SQL engine, and a mobile product. I separate symptoms from causes, implement the selected solution, and verify the result through APIs, database state, regression tests, and release checks.

## Representative Work

### [ClumL · Outbound LLM API Rate-Limiting Concurrency Fix](experience/cluml.md)

**Type and period:** Full-time role · Mar 2025 - Jul 2026

**Role:** Rust backend problem analysis, implementation, and regression verification

**Core change:** Fixed a check-and-reserve race in which concurrent LLM API calls read the same pre-reservation state.

**Validation:** Under the same concurrency load, reproduced LLM API calls passing at more than ten times the effective concurrency limit, then confirmed the fixed path stayed at or below the limit.

**Technologies:** `Rust` · `concurrency control` · `regression testing`

### [TmaxCloud · Pre-Deployment API Testing for a Code-Generation Platform](experience/tmaxcloud.md)

**Type and period:** Full-time role · Oct 2021 - Nov 2024

**Role:** Feature design, implementation, and verification for a Java and TypeScript code-generation platform

**Core change:** Added a feature to a platform that turns UI-defined services into Java APIs, SQL, and a JAR, allowing those APIs to be called and checked against database state before deployment.

**Validation:** Invalid service definitions, request/response shapes, and database writes could be found without repeating the roughly 20-minute build, deployment, and verification cycle.

**Technologies:** `Java` · `WebSocket` · `Tibero`

### [GlueSQL · Implementing DISTINCT Execution Semantics](opensource/gluesql.md)

**Type and period:** Open-source contribution · Jun 2021 - Present

**Role:** Direct implementation in a Rust SQL engine and contributor code review

**Core change:** Separated projection-row deduplication from unique-value tracking in aggregate state and carried `DISTINCT` semantics into execution.

**Validation:** Covered single and multiple columns, maps, schemaless rows, and aggregate `DISTINCT` with regression tests.

**Technologies:** `Rust` · `parser/AST` · `SQL executor`

### [Coupler · Mobile Dating App Engineering Lead](projects/coupler.md)

**Type and period:** Independent product · Jul 2024 - Present

**Role:** Engineering and operations lead across the React Native app, Express API, React admin web, and MySQL database

**Core change:** Made the app and admin web follow access state returned by the API instead of inferring review state independently.

**Validation:** Kept API response, mobile routing, and admin review-queue regression tests in the release checklist.

**Technologies:** `React Native` · `TypeScript` · `MySQL`

## More

See [Engineering Principles](engineering-principles.md) for the shared approach to problem decomposition, decisions, and verification.

## Contact

- [Email](mailto:meenseek5929@naver.com)
- [GitHub](https://github.com/zmrdltl)
