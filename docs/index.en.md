# Minsik Kim Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I find and fix concurrency and data-correctness problems in platform backends, then verify the result with reproducible tests and real API and database behavior. I have applied this approach across full-time work on a code-generation platform and Rust services, an open-source SQL engine, and a mobile product that I operate directly.

## Representative Work

### [ClumL · Outbound LLM API Rate-Limiting Concurrency Fix](experience/cluml.md)

**Type and period:** Full-time role · Mar 2025 - Jul 2026

**Role:** Rust backend problem analysis, implementation, and regression verification

**Core change:** I fixed a concurrency defect in which LLM API calls read the same pre-reservation state and passed together, pushing the in-flight call count and token reservations beyond their limits.

**Validation:** Under the same concurrency load, I reproduced over-reservation in which the in-flight call count and pending token reservations each reached at least ten times their respective limits, then confirmed that both stayed within their respective limits after the fix.

**Technologies:** `Rust` · `concurrency control` · `regression testing`

### [TmaxCloud · Pre-Deployment API Testing for a Code-Generation Platform](experience/tmaxcloud.md)

**Type and period:** Full-time role · Oct 2021 - Nov 2024

**Role:** Design, implementation, and verification of the React and TypeScript test UI, Java REST API, and database schema

**Core change:** I built a test UI for a platform that generates Java APIs, SQL, and a JAR from UI-defined services, so users can check API responses and database state before deployment.

**Validation:** Invalid service definitions, request/response shapes, and database-write errors could be found without repeating the roughly 20-minute build, deployment, and verification cycle.

**Technologies:** `Java` · `WebSocket` · `Tibero`

### [GlueSQL · Implementing DISTINCT Execution Semantics](opensource/gluesql.md)

**Type and period:** Open-source contribution · Jun 2021 - Present

**Role:** Direct implementation in a Rust SQL engine and contributor code review

**Core change:** I fixed `SELECT DISTINCT` returning duplicate results like a regular `SELECT`, implementing the appropriate deduplication for regular queries and aggregate functions.

**Validation:** Regression tests covered `DISTINCT` over single and multiple columns and aggregate functions including `COUNT`.

**Technologies:** `Rust` · `parser/AST` · `SQL executor`

### [Coupler · Mobile Dating App Engineering Lead](projects/coupler.md)

**Type and period:** Independent product · Jul 2024 - Present

**Role:** Engineering and operations lead across the React Native app, Express API, React admin web, and MySQL database

**Core change:** Made the app and admin web follow access state returned by the API instead of inferring review state independently.

**Validation:** I regression-tested the API response contract, mobile routing, and admin review queue to verify that server-side review state was reflected consistently in the app and admin queue.

**Technologies:** `React Native` · `TypeScript` · `MySQL`

## More

See [Engineering Principles](engineering-principles.md) for the shared approach to problem decomposition, decisions, and verification.

## Contact

- [Email](mailto:meenseek5929@naver.com)
- [GitHub](https://github.com/zmrdltl)
