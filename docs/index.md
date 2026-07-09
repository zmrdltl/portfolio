# 김민식 기술 포트폴리오

PLATFORM SOFTWARE ENGINEER

## 요약

사용자가 정의한 서비스와 제품 변경이 실제 코드, SQL, 데이터 흐름, 테스트 기준까지 이어지도록 정리하는 Platform Software Engineer입니다.

최신 경력인 ClumL에서는 보안 분석 제품의 요청 제한 동시성 문제를 재정의하고, 허용치 초과 요청이 작업 실행 단계로 넘어가지 않도록 처리 기준과 회귀 테스트를 세웠습니다. TmaxCloud No-code platform에서는 화면에서 설계한 service/API가 Java 코드와 SQL로 생성되어 실행되도록 만들고, 배포된 앱에서 발생한 데이터 변경 이력을 저장·조회해 특정 시점의 table 상태를 보여줄 수 있게 했습니다. 개인 제품 Coupler에서는 React Native 앱, API, 관리자 웹, DB가 같은 가입·심사 기준을 따르도록 제품 흐름과 운영 기준을 정리했습니다.

오픈소스에서는 Rust SQL engine GlueSQL에 기여했습니다. `SELECT DISTINCT`와 aggregate `DISTINCT`, SQL parser와 AST 표현, executor와 aggregate 처리, Parquet storage, 회귀 테스트, PR review를 다뤘습니다.

## 대표 작업

- [보안 분석 제품의 변경 안전성](experience/cluml.md): 고객사 데모 서버 운영 중 관찰된 대기 증상을 요청 제한 동시성 정확성 문제로 재정의하고, 허용치 초과 요청이 작업 실행 단계로 들어가지 않도록 예약 상태 갱신 기준과 회귀 테스트를 세웠습니다. 탐지 화면·리포트 표시 일관성, Rust 서비스 설정 변경, PR review 기준도 같은 변경 안전성 흐름 안에서 다뤘습니다.
- [No-code platform 서비스 생성과 데이터 이력](experience/tmaxcloud.md): TmaxCloud No-code platform에서 화면으로 설계한 service/API를 Java 코드와 SQL로 생성하고, 배포 전 WebSocket test page로 request/response와 DB write/read를 확인할 수 있게 했습니다. 변경 이력 옵션이 켜진 entity는 배포 시 원본 table과 변경 이력 table을 생성하고, insert/update/delete 서비스 코드가 변경 전 row data를 이력 table에 저장해 특정 시점 table 상태를 조회할 수 있도록 했습니다.
- [Rust SQL engine 오픈소스 기여](opensource/gluesql.md): GlueSQL에서 `SELECT DISTINCT`와 aggregate `DISTINCT`를 SQL translation, AST 표현, executor 중복 제거, aggregate 처리, AST builder, 회귀 테스트까지 연결해 구현했습니다. `gluesql/gluesql` 기준 GitHub `is:merged` 검색에서 병합 PR 50건 이상을 확인할 수 있습니다.
- [개인 제품 Coupler 운영 기준](projects/coupler.md): React Native 앱, API, 관리자 웹, DB를 함께 다루며 가입·심사 흐름을 단계형으로 바꾸고, TypeScript 운영 기준, typecheck/migration guard, 회귀 테스트, 코드 리뷰 기준을 릴리스 기준과 연결했습니다.

## 개발 운영 관점

유지보수를 위한 일관성, 확장성, 응집도와 결합도, 책임 분리가 분명한 코드 작성을 중요하게 봅니다.

반복 구현의 일부 허들이 낮아질수록 문제 정의, 도메인 정책, 책임 범위, 테스트 기준, 리뷰 기준을 흔들리지 않게 남기는 일이 더 중요해진다고 봅니다. 좋은 개발 문서는 동료와 자동화 도구가 같은 기준으로 구현과 리뷰를 이어갈 수 있게 만드는 실행 가능한 기준이어야 한다고 생각합니다.

자세한 기준은 [원칙](engineering-principles.md)에 정리했습니다.

## 주요 기술 영역

- 개발 운영: 문서, 타입 검사, 테스트, 리뷰, 릴리스 기준이 함께 움직이도록 변경 단위와 검증 기준을 설계
- 서비스 계약: 앱/API/관리자 웹/DB가 같은 상태 모델을 따르도록 서버 응답 계약, 심사 정책, 권한·화면 분기 기준을 정리
- 서비스 생성 플랫폼: 화면에서 정의한 metadata/schema를 Java service code, SQL/DDL, DB 검증, 데이터 변경 이력, entity export/import로 연결
- 변경 안전성: 운영 증상, 설정 변경, 표시 일관성 문제를 재현 조건, 완료 기준, 회귀 테스트, PR review 기준으로 분리
- Rust/SQL: Rust SQL engine, SQL parser/AST, executor/aggregate 처리, storage, 회귀 테스트, 코드 리뷰

## 기술

- Languages: Rust, Java, TypeScript, SQL
- Backend/Data: SQL/DDL Generator, GraphQL, WebSocket, PostgreSQL, MySQL, Tibero
- Frontend: React, React Native, Material UI, React Flow
- Infra/Tools: Kubernetes, Terraform, GitHub Actions, AWS

## 링크

- [Email](mailto:meenseek5929@naver.com)
- [GitHub](https://github.com/zmrdltl)

## 둘러보기

- [경력](experience/index.md)
- [ClumL](experience/cluml.md)
- [티맥스클라우드](experience/tmaxcloud.md)
- [GlueSQL](opensource/gluesql.md)
- [Coupler](projects/coupler.md)
- [원칙](engineering-principles.md)
