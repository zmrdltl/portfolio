# Minsik Kim Technical Portfolio

PLATFORM SOFTWARE ENGINEER

## Summary

I am a Platform Software Engineer who verifies generated API responses and database writes and reads before deployment, fixes concurrency bugs in Rust services, and pairs product changes with regression tests and release checks.

## Representative Work

| Representative Work | Core Change | Validation or Result |
| --- | --- | --- |
| [ClumL · Rust Rate Limiting and Detection Thresholds](experience/cluml.md) | Fixed a request-limiting race and moved a network-event detection threshold to external configuration | Before: at least 10x the configured limit passed → after: at or below the limit |
| [TmaxCloud · Generated API Verification](experience/tmaxcloud.md) | Built pre-deployment API verification and data-change history storage | Helped reduce the recurring design-to-verification cycle from about four weeks to about two |
| [GlueSQL · Rust SQL Engine](opensource/gluesql.md) | Connected `DISTINCT` across translation, execution, aggregates, and tests | 50 merged pull requests · current reviewer |
| [Coupler · Mobile App Engineering Lead](projects/coupler.md) | Split signup into review stages and made app screens and the admin review queue follow the review state returned by the API | Meta SDK event recorded upon reaching the initial signup review stage: observed about 10 times before → about 100 times after |

## Technologies by Project

| Project | Technologies |
| --- | --- |
| ClumL | Rust, concurrency control, rate limiting, external configuration for a network-event detection threshold, GraphQL, regression testing, Chrono/Jiff |
| TmaxCloud | Java, TypeScript, React, WebSocket, Monaco Editor, FreeMarker, Tibero, SQL/DDL generation, JUnit, JaCoCo |
| GlueSQL | Rust, SQL engine internals, parser/AST, aggregate functions, Parquet storage, code review |
| Coupler | React Native, React, TypeScript, Express, MySQL, API response design, signup/review state management, GitHub Actions |

## Contact

- [Email](mailto:meenseek5929@naver.com)
- [GitHub](https://github.com/zmrdltl)
