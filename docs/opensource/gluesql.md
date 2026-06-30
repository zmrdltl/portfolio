# GlueSQL

- 유형: 오픈소스 기여
- 기간: 2021.06 - Present

## 개요

GlueSQL은 Rust 기반 SQL database engine입니다. 기여 범위는 SQL engine 기능, parser/AST, aggregate/data function, numeric type 처리, Parquet storage, test suite, 멘토링, 코드 리뷰를 포함합니다.

`gluesql/gluesql`에서 [Merged 45+](https://github.com/gluesql/gluesql/pulls?q=is%3Apr+author%3Azmrdltl+is%3Amerged)을 작성했고, 이력서와 포트폴리오에서는 public GitHub PR, review, docs로 확인 가능한 범위만 사용합니다.

이 페이지는 공개 기술 깊이를 보여주는 자료입니다. 회사 제품의 내부 구현을 공개하지 못하는 제약을 보완하기 위해, SQL engine의 parser, AST, execution path, storage, test suite를 실제 공개 PR과 review로 보여줍니다.

SQL engine 기능은 문법만 추가한다고 끝나지 않습니다. parser가 구문을 받아들이고, AST와 plan/execution path가 같은 의미를 유지하며, storage와 test suite가 예외 조건을 고정해야 합니다. GlueSQL 기여는 이 흐름을 공개적으로 검증 가능한 자료로 남긴 작업입니다.

## 구조 요약

```mermaid
flowchart LR
  syntax["SQL Syntax / Function"]
  parser["Parser"]
  ast["AST / Builder"]
  plan["Plan / Execution"]
  storage["Storage"]
  tests["Test Suite"]
  review["PR Review / Docs"]

  syntax --> parser
  parser --> ast
  ast --> plan
  plan --> storage
  plan --> tests
  tests --> review
```

## CLI Application

GlueSQL은 embedded SQL engine으로 사용할 수 있고, 개발 과정에서 CLI로 SQL 실행 흐름을 확인할 수 있습니다.

![GlueSQL CLI application](attachments/gluesql-cli.png)

## 2021: SQL 함수와 parser 기여

2021.06에 프로그램을 시작해 Rust와 GlueSQL 프로젝트 구조를 파악했고, 2021.08에 첫 공개 PR을 진행했습니다. 2021년에는 OSSCA 멘티로 참여하며 Rust 기반 SQL engine 구조를 학습하고 작은 SQL function부터 parser 연동까지 기여했습니다.

- `REVERSE` SQL function을 추가하고 integration test를 작성했습니다.
- `PartialEq`, `PartialOrd` 관련 test를 작성하고 bug를 수정했습니다.
- GlueSQL에서 logical XOR를 지원하기 위해 upstream parser인 `sqlparser-rs`에 [logical XOR parser PR](https://github.com/apache/datafusion-sqlparser-rs/pull/357)을 병합했습니다.
- GlueSQL Boolean type에 대한 logical XOR 동작을 구현했습니다.
- Aggregation function의 중간 상태를 private enum 기반으로 정리해 값 의미가 모호해지는 문제를 줄였습니다.
- Unary plus/minus unit test를 추가했습니다.

이 시기의 핵심은 SQL 문법, parser, execution path, integration test가 함께 움직이는 구조를 실제 PR로 학습하고 기여한 것입니다.

## 2022: AST Builder, 집계 함수, numeric type

2022년에는 OSSCA 리드 멘티로 활동하며 aggregate/data function과 AST Builder API 개선을 중심으로 기여했습니다.

대표 작업:

- [#635](https://github.com/gluesql/gluesql/pull/635): AST Builder aggregate functions 추가
- [#656](https://github.com/gluesql/gluesql/pull/656): COUNT aggregate function 구현
- [#675](https://github.com/gluesql/gluesql/pull/675): enum Value에 `sqrt` function 추가
- [#684](https://github.com/gluesql/gluesql/pull/684): STDEV aggregate function 추가
- [#698](https://github.com/gluesql/gluesql/pull/698): aggregate function 구조 개선
- [#723](https://github.com/gluesql/gluesql/pull/723): FunctionNode structure 개선
- [#749](https://github.com/gluesql/gluesql/pull/749): aggregate functions가 Expr를 지원하도록 개선
- [#782](https://github.com/gluesql/gluesql/pull/782): test suite refactoring
- [#828](https://github.com/gluesql/gluesql/pull/828): unsigned integer `u8` data type 추가

기술적으로는 AggregateNode, CountArgExprNode, Expr 변환 구조를 다뤘고, numeric type casting, sqrt, variance, standard deviation 같은 SQL/data function 범위를 넓혔습니다. Aggregate expression 지원 과정에서는 async evaluate, storage I/O, lifetime 문제를 함께 다뤘습니다.

Numeric type 판정을 위해 `bigdecimal-rs`에 [`get_scale` PR](https://github.com/akubera/bigdecimal-rs/pull/116)을 병합한 것도 이 범위의 공개 링크로 확인할 수 있는 작업입니다.

## 2023: 멘토링, 리뷰, Parquet storage

2023년에는 OSSCA 멘토로 참여해 contributor mentoring, PR review, issue 안내, Parquet storage 구현에 기여했습니다.

- 17명 대상 1:1 mentoring coffee chat을 4주간 진행했습니다.
- Rust project 기본 명령어, test 작성, GlueSQL 실행 흐름을 설명했습니다.
- GlueSQL의 SQL 실행 흐름을 `parse -> translate -> plan -> execute` 단계로 설명했습니다.
- `REPLACEMENT`, `SORT`, `GREATEST`, `SLICE`, `COALESCE` 등 SQL function PR을 review했습니다.
- `EXPLAIN`, `KEYS`, `SPLICE`, `LEAST`, `TAKE`, `ADD_MONTH` function 구현 방향을 안내했습니다.
- Storage 구조, memory storage transaction, AST builder, alias select node, type별 comparison/scoring 구조를 설명했습니다.

관련 링크:

- [Parquet Storage PR #1269](https://github.com/gluesql/gluesql/pull/1269)
- [REPLACEMENT function review #1266](https://github.com/gluesql/gluesql/pull/1266)
- [SORT function review #1300](https://github.com/gluesql/gluesql/pull/1300)
- [GREATEST function review #1312](https://github.com/gluesql/gluesql/pull/1312)
- [SLICE function review #1340](https://github.com/gluesql/gluesql/pull/1340)
- [COALESCE function review/support #1333](https://github.com/gluesql/gluesql/pull/1333)
- [GlueSQL Parquet storage docs](https://gluesql.org/docs/0.16.0/storages/supported-storages/parquet-storage)

## 유지보수 기여

이후에도 Rust toolchain, clippy, deterministic ordering, `DISTINCT` operation 등 유지보수 PR을 이어갔습니다. 이 범위는 특정 기능 하나보다 project compatibility, lint, deterministic behavior, regression safety를 유지하는 기여로 분류합니다.

## 활동과 수상

OSSCA에서는 2021년 멘티, 2022년 리드 멘티, 2023년 멘토로 활동했습니다. 수상 내역은 [활동](../activities/index.md) 페이지에 따로 정리하고, 이 페이지에서는 code contribution과 review/mentoring의 기술 범위만 설명합니다.

## 링크

- [GlueSQL repository](https://github.com/gluesql/gluesql)
- [`zmrdltl`이 작성한 GlueSQL PR 검색](https://github.com/gluesql/gluesql/pulls?q=is%3Apr+author%3Azmrdltl)
- [GlueSQL 2023년 공식 문서](https://gluesql.org/docs/0.14/)
- [DataFusion SQL Parser logical XOR PR](https://github.com/apache/datafusion-sqlparser-rs/pull/357)
- [BigDecimal `get_scale` PR](https://github.com/akubera/bigdecimal-rs/pull/116)
- [Parquet Storage PR #1269](https://github.com/gluesql/gluesql/pull/1269)

## Articles

- [Breaking the Boundary between SQL and NoSQL Databases](https://gluesql.org/blog/breaking-the-boundary-between-sql-and-nosql)
- [Revolutionizing Databases by Unifying Query Interfaces](https://gluesql.org/blog/revolutionizing-databases-by-unifying-query-interfaces)

## 기술

Rust, SQL engine internals, parser/AST design, aggregate functions, numeric data types, storage, Parquet, test suites, code review, mentoring
