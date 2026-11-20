# Minsik Kim Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I find and fix concurrency and data-correctness problems in platform backends, then verify the result with reproducible tests and real API and database behavior. I have applied this approach across full-time work on a code-generation platform and Rust services, an open-source SQL engine, and a mobile product for which I led development and operations.

## Representative Work

### [ClumL · Outbound LLM API Rate-Limiting Concurrency Fix](experience/cluml.md)

**Type and period:** Full-time role · Mar 2025 - Jul 2026

**Role:** Rust backend problem analysis, implementation, and regression verification

**Core change:** I fixed a concurrency defect in which LLM API calls read the same pre-reservation state and passed together, pushing the in-flight call count and token reservations beyond their limits.

**Validation:** Under the same concurrency load, I reproduced over-reservation in which the in-flight call count and pending token reservations each reached at least ten times their respective limits, then confirmed that both stayed within their respective limits after the fix.

**Technologies:** `Rust` · `concurrency control` · `regression testing`

### [TmaxCloud · Pre-Deployment API Testing for a Code-Generation Platform](experience/tmaxcloud.md)

**Type and period:** Full-time role · Oct 2021 - Nov 2024

**Role:** Design, implementation, and verification of the React test UI, Java REST API, and database schema

**Core change:** I built a test screen that used the code-generation platform’s temporary deployment environment to check generated API responses and real database changes before formal deployment.

**Validation:** Users could catch invalid service definitions, request and response format errors, and database issues before the build, formal deployment, and verification cycle that took about 20 minutes.

**Technologies:** `Java` · `WebSocket` · `Tibero`

### [GlueSQL · Implementing DISTINCT Execution Semantics](opensource/gluesql.md)

**Type and period:** Open-source contribution · Jun 2021 - Present

**Role:** Direct implementation in a Rust SQL engine and contributor code review

**Core change:** I fixed `SELECT DISTINCT` returning duplicate results. I added deduplication of result rows for `SELECT DISTINCT` and input values for aggregate functions such as `COUNT(DISTINCT col)`.

**Validation:** Regression tests covered `DISTINCT` over single and multiple columns and aggregate functions including `COUNT`.

**Technologies:** `Rust` · `parser/AST` · `SQL executor`

### [Coupler · Mobile Dating App Engineering Lead](projects/coupler.md)

**Type and period:** Independent product · Jul 2024 - Sep 2026

**Role:** Engineering and operations lead across the React Native app, Express API, React admin web, and MySQL database

**Core change:** I reduced the roughly 30-field initial signup form to basic information and the required profile, and made app routing follow server-provided review state. The server classified requests into the appropriate admin review queue.

**Validation:** I regression-tested that the app opened the screen for the server’s review state and that the admin review queue distinguished signup reviews from profile edits.

**Technologies:** `React Native` · `TypeScript` · `MySQL`

## More

See [Engineering Principles](engineering-principles.md) for the shared approach to problem decomposition, decisions, and verification.

## Contact

- [Email](mailto:meenseek5929@naver.com)
- [GitHub](https://github.com/zmrdltl)
