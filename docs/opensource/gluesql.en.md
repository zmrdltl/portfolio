# GlueSQL

- Type: Open-source contribution
- Period: Jun 2021 - Present

## Implementing DISTINCT Execution Semantics

**Problem and diagnosis:** `SELECT DISTINCT` syntax information did not reach GlueSQL's Rust SQL engine executor, so the query produced the same result as a regular `SELECT`. Projection and aggregate execution identify duplicates at different state boundaries.

**Constraints and decision:** I had to leave non-`DISTINCT` results unchanged and remove duplicates only at the two state boundaries where final values are produced. Unsupported `DISTINCT ON` returns an explicit error.

Scroll horizontally to inspect the full flow.
{ .diagram-scroll-hint }

![DISTINCT syntax moves through the parser and AST into the query model, then the execution path deduplicates projected rows or aggregate inputs before regression tests verify the behavior.](../assets/diagrams/gluesql-distinct-execution.en.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="GlueSQL DISTINCT execution-semantics flow diagram" }

**Implementation:** I propagated parser/AST output into the query model, then connected row deduplication and aggregate handling in the SQL executor with AST Builder APIs. I also strengthened value equality, hashing, and map-key ordering so duplicate detection remained deterministic.

**Validation and result:** Regression tests covered single and multiple columns, maps, schemaless rows, and aggregate `DISTINCT`, including `COUNT`. The feature and tests preserve the same meaning across SQL input, internal representation, and execution output.

## Implementing the AST Query Interface, Parquet Storage, and CLI

### AST Query Interface

I implemented AST Builder aggregate helpers and `COUNT` argument handling, then updated executor and test paths so aggregate functions could evaluate expression arguments rather than only simple columns.

### Parquet Storage and CLI

I connected Parquet storage to GlueSQL's storage traits and SQL execution, adding file read/write, schema and value conversion, documentation, tests, and a CLI usage path. I later updated the related code to meet `clippy::pedantic` checks.

## Review, Mentoring, and Awards

I authored [50 merged pull requests in `gluesql/gluesql`](https://github.com/gluesql/gluesql/pulls?q=is%3Apr+author%3Azmrdltl+is%3Amerged). I now participate in code review and maintenance as a GlueSQL reviewer, reviewing contributor pull requests for error handling, edge cases, test coverage, and code organization. As an OSSCA mentor in 2023, I guided contributors through Rust project workflows, GlueSQL internals, storage, AST Builder, and function implementation.

| Year | Program | Award |
| --- | --- | --- |
| 2023 | Open Source Contribution Academy | GlueSQL team award while I participated as a mentor: NIPA President Award (Encouragement) |
| 2022 | Open Source Contribution Academy | NIPA President Award (Top Excellence) |
| 2021 | Open Source Contribution Academy | NIPA President Award (Top Excellence) |

- Public award announcement: [2023 Encouragement Award](https://drive.google.com/file/d/1oK3BYXVzaAQec83pAjl00_FUHt9ZZN0b/view?usp=sharing)

## Related Links

- [GlueSQL repository](https://github.com/gluesql/gluesql)
- Representative implementations: [DISTINCT operations](https://github.com/gluesql/gluesql/pull/1710), [Parquet storage read/write](https://github.com/gluesql/gluesql/pull/1269)
- Representative reviews: [REPLACE function](https://github.com/gluesql/gluesql/pull/1266), [GREATEST function](https://github.com/gluesql/gluesql/pull/1312), [SLICE function](https://github.com/gluesql/gluesql/pull/1340)
- External ecosystem contributions: [DataFusion SQL Parser logical XOR](https://github.com/apache/datafusion-sqlparser-rs/pull/357), [BigDecimal `get_scale`](https://github.com/akubera/bigdecimal-rs/pull/116)
- GlueSQL project technical articles: [Breaking the Boundary between SQL and NoSQL Databases](https://gluesql.org/blog/breaking-the-boundary-between-sql-and-nosql), [Revolutionizing Databases by Unifying Query Interfaces](https://gluesql.org/blog/revolutionizing-databases-by-unifying-query-interfaces)
