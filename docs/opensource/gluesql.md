# GlueSQL

- 유형: 오픈소스 기여
- 기간: 2021.08 - Present

## 개요

GlueSQL은 Rust 기반 SQL database engine입니다.
기여 범위는 SQL engine 기능, parser/AST, numeric type 처리, Parquet storage, test suite, 멘토링, 코드 리뷰를 포함합니다.

## 기여

- `gluesql/gluesql`에서 [PR 50개 이상](https://github.com/gluesql/gluesql/pulls?q=is%3Apr+author%3Azmrdltl)을 작성했습니다.
- SQL function, aggregate function, AST Builder API, numeric data type, Parquet storage, test suite 개선에 기여했습니다.
- GlueSQL 사용을 위해 `apache/datafusion-sqlparser-rs`에 [logical XOR PR](https://github.com/apache/datafusion-sqlparser-rs/pull/357)을 병합했습니다.
- numeric type 판정을 위해 `akubera/bigdecimal-rs`에 [`get_scale` PR](https://github.com/akubera/bigdecimal-rs/pull/116)을 병합했습니다.
- 2025년에도 Rust toolchain, clippy, deterministic ordering, `DISTINCT` operation 등 유지보수 PR을 이어갔습니다.

## 리뷰와 멘토링

- 오픈소스 멘토링 활동에서 contributor mentoring, PR review, issue 안내를 수행했습니다.
- 2021년 멘티, 2022년 리드 멘티, 2023년 멘토로 활동했습니다.
- 오픈소스 컨트리뷰션 아카데미에서 GlueSQL 활동으로 2021년 정보통신산업진흥원장상 최우수상, 2022년 정보통신산업진흥원장상 최우수상, 2023년 정보통신산업진흥원장상 장려상을 수상했습니다.

## 공개 증빙

- [GlueSQL repository](https://github.com/gluesql/gluesql)
- [오픈소스 컨트리뷰션 아카데미 수상 증빙 폴더](https://drive.google.com/drive/folders/1Kp0WQnuLxfCKPfvxvYLO27yjkDyE2Wda)
- [2022 GlueSQL 발표자료](https://docs.google.com/presentation/d/14jt84NOFgBZlR41AIjbc6N2LNWzkgYNjIRbhk2sGWdc/edit#slide=id.g1421bd87c53_2_22)
- [2023 GlueSQL 발표자료](https://docs.google.com/presentation/d/1Rx6Vgbxsth6xA_681xyWXOhD_BFjDyM79m921FOr31E/edit)

## 기술

Rust, SQL engine internals, parser/AST design, data types, storage, test suites, code review, mentoring
