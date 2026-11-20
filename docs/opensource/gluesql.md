# GlueSQL

- 유형: 오픈소스 기여
- 기간: 2021.06 - 현재

## DISTINCT 실행 의미 구현

**문제와 진단:** GlueSQL의 Rust SQL 엔진에서 `SELECT DISTINCT`가 오류 없이 실행돼도 일반 `SELECT`처럼 중복 행을 반환했습니다. 구문 분석기가 읽은 `DISTINCT` 표시가 내부 쿼리 표현을 거쳐 Rust 실행기로 전달되지 않아, 실행기가 중복을 제거해야 한다는 사실을 알 수 없었습니다.

**제약과 선택:** `SELECT DISTINCT`는 조회 결과에서 같은 행을 한 번만 반환해야 하고, `COUNT(DISTINCT col)`은 집계 함수에 같은 입력값을 한 번만 넣어야 합니다. 중복을 판단할 대상이 달라 조회와 집계의 처리 지점을 나눴습니다. 지원하지 않는 `DISTINCT ON`은 명시적인 오류로 반환했습니다.

`SELECT DISTINCT`에서는 중복 제거 후 `LIMIT`를 적용했습니다. 예를 들어 정렬된 결과가 `A, A, B`라면 `LIMIT 2`를 먼저 적용할 때 `A, A`만 남아 고유 행 `B`가 빠집니다. 중복 제거가 먼저라면 `A, B`가 남습니다. 이 구현은 `LIMIT`가 작아도 중복 제거 전에 조회 결과 전체를 메모리에 모읍니다.

도식을 좌우로 스크롤해 전체 흐름을 확인할 수 있습니다.
{ .diagram-scroll-hint }

![DISTINCT SQL 정보가 parser와 AST를 거쳐 query model에 전달되고, 실행 경로에 따라 projection 결과 행 또는 aggregate 입력 값을 중복 제거한 뒤 회귀 테스트로 확인합니다.](../assets/diagrams/gluesql-distinct-execution.ko.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="GlueSQL DISTINCT 실행 의미 흐름 도식" }

**구현:** parser/AST 결과를 query model에 전달하고, SQL executor의 row 중복 제거와 aggregate 처리, AST Builder API까지 연결했습니다. 중복 제거가 일관되려면 동등한 값은 같은 hash를 가져야 하고, map은 key 입력 순서가 달라도 같은 값으로 판정돼야 했습니다. 이 불변조건을 지키도록 값 비교·hash와 map key 정렬을 함께 보강했습니다.

**검증과 결과:** 단일·복수 열, 맵 값, 스키마가 고정되지 않은 행에서 중복이 제거되는지 회귀 테스트했습니다. `COUNT(DISTINCT col)` 등 중복 제거를 요청한 집계에서는 같은 입력값이 여러 번 들어가도 한 번만 반영되는지 확인했습니다.

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
