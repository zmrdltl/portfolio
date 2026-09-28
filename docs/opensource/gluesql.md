# GlueSQL

- 유형: 오픈소스 기여
- 기간: 2021.06 - 현재

## DISTINCT 실행 의미 구현

**문제와 진단:** `SELECT DISTINCT` 구문 정보가 GlueSQL의 Rust SQL 엔진 실행기(executor)까지 전달되지 않아 일반 `SELECT`와 같은 결과를 만들었습니다. 중복의 의미는 projection과 aggregate에서 서로 다른 상태를 기준으로 했습니다.

**제약과 선택:** `DISTINCT`가 아닌 기존 실행 결과는 유지하면서, `SELECT DISTINCT`는 projection 결과 행을, aggregate `DISTINCT`는 집계 함수의 입력 값을 중복 제거하도록 나눴습니다. 지원하지 않는 `DISTINCT ON`은 명시적 오류로 처리했습니다.

도식을 좌우로 스크롤해 전체 흐름을 확인할 수 있습니다.
{ .diagram-scroll-hint }

![DISTINCT SQL 정보가 parser와 AST를 거쳐 query model에 전달되고, 실행 경로에 따라 projection 결과 행 또는 aggregate 입력 값을 중복 제거한 뒤 회귀 테스트로 확인합니다.](../assets/diagrams/gluesql-distinct-execution.ko.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="GlueSQL DISTINCT 실행 의미 흐름 도식" }

**구현:** parser/AST 결과를 query model에 전달하고, SQL executor의 row 중복 제거와 aggregate 처리, AST Builder API까지 연결했습니다. 중복 제거가 일관되려면 동등한 값은 같은 hash를 가져야 하고, map은 key 입력 순서가 달라도 같은 값으로 판정돼야 했습니다. 이 불변조건을 지키도록 값 비교·hash와 map key 정렬을 함께 보강했습니다.

**검증과 결과:** 단일·복수 column, map과 schemaless row, `COUNT`를 포함한 aggregate `DISTINCT`를 회귀 테스트로 확인했습니다. SQL 입력, 내부 표현, 실행 결과가 같은 의미를 유지하도록 기능과 테스트를 함께 반영했습니다.

## 추가 작업

- **파서 의존성 비교 평가:** 자체 파서 교체안을 공개 AST와 Query Builder의 호환성 비용까지 검토했습니다. 같은 core 복사본에서 `sqlparser/serde`만 끄고 다시 켜 비교한 `sqlparser` 검사 시간은 2.6초와 8.0초였고, 기존 구성과 기능 제거 구성에서 core 테스트는 각각 593개 통과했습니다. AST 변환에 필요한 `bigdecimal`은 유지하고 내부에서 사용하지 않는 `serde`만 제거하는 [PR #2042](https://github.com/gluesql/gluesql/pull/2042)를 선택했습니다. 공개 AST 직렬화 소비자는 해당 기능을 직접 켜야 할 수 있습니다.
- **AST Query Interface:** AST Builder의 aggregate helper와 `COUNT` argument를 구현하고, aggregate 함수가 expression argument를 평가하도록 executor와 테스트를 수정했습니다.
- **Parquet Storage·CLI:** storage trait와 SQL 실행 경로에 Parquet을 연결하고 file read/write, schema·value 변환, 문서, 테스트, CLI 사용 흐름을 추가했습니다. 이후 `clippy::pedantic` 기준에 맞춰 코드를 정리했습니다.

## 리뷰와 멘토링

2026년 7월 10일 기준 [`gluesql/gluesql` 병합 PR 50건](https://github.com/gluesql/gluesql/pulls?q=is%3Apr+author%3Azmrdltl+is%3Amerged)을 작성했습니다. 현재 GlueSQL 리뷰어로 코드 리뷰와 유지보수에 참여하며, 기여자 PR의 오류 처리, edge case, 테스트 커버리지, 코드 구조를 검토합니다. 2023년에는 OSSCA 멘토로 Rust 프로젝트 기본 흐름, GlueSQL 구조, storage와 AST Builder, 함수 구현 방향을 안내했습니다.

제가 참여한 GlueSQL 팀은 2021·2022년 오픈소스 컨트리뷰션 아카데미 최우수상(정보통신산업진흥원장상)을 받았습니다. 2023년에는 제가 멘토로 참여한 GlueSQL 팀이 정보통신산업진흥원 장려상을 받았습니다.

## 관련 링크

- [GlueSQL repository](https://github.com/gluesql/gluesql)
- 대표 구현: [DISTINCT operations](https://github.com/gluesql/gluesql/pull/1710), [Parquet storage read/write](https://github.com/gluesql/gluesql/pull/1269)
- 대표 리뷰: [REPLACE 함수](https://github.com/gluesql/gluesql/pull/1266), [GREATEST 함수](https://github.com/gluesql/gluesql/pull/1312), [SLICE 함수](https://github.com/gluesql/gluesql/pull/1340)
- 외부 생태계 기여: [DataFusion SQL Parser logical XOR](https://github.com/apache/datafusion-sqlparser-rs/pull/357), [BigDecimal `get_scale`](https://github.com/akubera/bigdecimal-rs/pull/116)
- GlueSQL 프로젝트 기술 글: [Breaking the Boundary between SQL and NoSQL Databases](https://gluesql.org/blog/breaking-the-boundary-between-sql-and-nosql), [Revolutionizing Databases by Unifying Query Interfaces](https://gluesql.org/blog/revolutionizing-databases-by-unifying-query-interfaces)
