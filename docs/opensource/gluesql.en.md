# GlueSQL

- Type: Open-source contribution
- Period: Jun 2021 - Present

## Implementing DISTINCT Execution Semantics

**Problem and diagnosis:** GlueSQL's Rust SQL engine could accept `SELECT DISTINCT` without an error and still return duplicate rows like a regular `SELECT`. The parser recognized `DISTINCT`, but the flag did not reach the Rust executor through the internal query model, leaving the executor to run a regular query.

**Constraints and decision:** `SELECT DISTINCT` has to return each distinct result row once, whereas `COUNT(DISTINCT col)` has to pass each distinct input value to the aggregate once. Because the two operations deduplicate different things, I handled them at different points in execution. Unsupported `DISTINCT ON` returns an explicit error.

For `SELECT DISTINCT`, I applied `LIMIT` after deduplication. For example, applying `LIMIT 2` to the sorted results `A, A, B` first would leave `A, A` and lose the unique row `B`. Deduplicating first produces `A, B`. This implementation collects all result rows in memory before deduplicating, even when the limit is small.

<figure class="portfolio-diagram" aria-label="GlueSQL DISTINCT execution-semantics flow diagram" markdown="block">

<div class="portfolio-diagram-flow" markdown="block">

1. Pass the parsed `DISTINCT` flag through the query model to the executor.
2. Deduplicate result rows for `SELECT DISTINCT` and input values for aggregate `DISTINCT`.
3. Verify the outputs for both execution paths with regression tests.

</div>

![DISTINCT syntax moves through the parser and AST into the query model, then the execution path deduplicates projected rows or aggregate inputs before regression tests verify the behavior.](../assets/diagrams/gluesql-distinct-execution.en.svg)

<figcaption class="portfolio-diagram-link" markdown="span">[Open full-size diagram](../assets/diagrams/gluesql-distinct-execution.en.svg){ aria-label="Open full-size diagram (GlueSQL DISTINCT execution-semantics flow diagram)" }</figcaption>

</figure>

**Implementation:** I propagated parser/AST output into the query model, then connected row deduplication and aggregate handling in the SQL executor with AST Builder APIs. Consistent deduplication required equal values to produce the same hash and equivalent maps to compare equally regardless of key insertion order. I updated value comparison, hashing, and map-key ordering together to preserve those invariants.

**Validation and result:** Regression tests checked deduplication across single and multiple columns, map values, and schemaless rows. I also checked that aggregates such as `COUNT(DISTINCT col)` use a repeated input value only once.

## Additional Work

- **Parser dependency evaluation:** I assessed an in-house parser against the compatibility cost of the public AST and Query Builder. In the same copy of core, the `sqlparser` check took 2.6 seconds with only `sqlparser/serde` disabled and 8.0 seconds after re-enabling it; the baseline and feature-disabled configurations each passed 593 core tests. I kept `bigdecimal` because the AST conversion depends on it and chose [PR #2042](https://github.com/gluesql/gluesql/pull/2042) to remove only unused `serde`. Consumers serializing the public AST may need to enable the feature directly.
- **AST Query Interface:** I implemented AST Builder aggregate helpers and `COUNT` argument handling, then updated the executor and tests to evaluate expression arguments.
- **Parquet Storage and CLI:** I connected Parquet to the storage traits and SQL execution, adding file read/write, schema and value conversion, documentation, tests, and a CLI usage path. I later updated the code to meet `clippy::pedantic` checks.

## Review and Mentoring

As of July 10, 2026, I had authored [50 merged pull requests in `gluesql/gluesql`](https://github.com/gluesql/gluesql/pulls?q=is%3Apr+author%3Azmrdltl+is%3Amerged). I now participate in code review and maintenance as a GlueSQL reviewer, reviewing contributor pull requests for error handling, edge cases, test coverage, and code organization. As an OSSCA mentor in 2023, I guided contributors through Rust project workflows, GlueSQL internals, storage, AST Builder, and function implementation.

The GlueSQL team I joined received the Open Source Contribution Academy's NIPA President Award (Top Excellence) in 2021 and 2022. The GlueSQL team I mentored received a NIPA Encouragement Award in 2023.

## Related Links

- [GlueSQL repository](https://github.com/gluesql/gluesql)
- Representative implementations: [DISTINCT operations](https://github.com/gluesql/gluesql/pull/1710), [Parquet storage read/write](https://github.com/gluesql/gluesql/pull/1269)
- Representative reviews: [REPLACE function](https://github.com/gluesql/gluesql/pull/1266), [GREATEST function](https://github.com/gluesql/gluesql/pull/1312), [SLICE function](https://github.com/gluesql/gluesql/pull/1340)
- External ecosystem contributions: [DataFusion SQL Parser logical XOR](https://github.com/apache/datafusion-sqlparser-rs/pull/357), [BigDecimal `get_scale`](https://github.com/akubera/bigdecimal-rs/pull/116)
- GlueSQL project technical articles: [Breaking the Boundary between SQL and NoSQL Databases](https://gluesql.org/blog/breaking-the-boundary-between-sql-and-nosql), [Revolutionizing Databases by Unifying Query Interfaces](https://gluesql.org/blog/revolutionizing-databases-by-unifying-query-interfaces)
