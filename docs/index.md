# 김민식 기술 포트폴리오

PLATFORM SOFTWARE ENGINEER

## 요약

서비스 계약, 데이터 상태, 테스트 기준으로 백엔드/플랫폼 문제를 닫는 Platform Software Engineer입니다. 최신 경력에서는 보안 분석 제품의 요청 제한 동시성 문제를 재정의하고, 이전 경력과 오픈소스에서는 generated service 검증과 Rust SQL engine 변경을 실제 구현·검증 기록으로 남겼습니다.

대표 작업은 네 가지 작업 흐름으로 정리합니다. 최신 경력에서는 보안 분석 제품의 변경 안전성을 다루고, 이전 경력에서는 metadata-driven platform의 생성 서비스와 데이터 이력을 검증 가능하게 만들었으며, 오픈소스에서는 Rust SQL engine의 query semantics와 test suite를 PR과 review 기록으로 남겼습니다. 개인 제품에서는 상태 계약과 릴리스 기준을 제품 운영 기준으로 정리했습니다.

## 대표 작업

- [보안 분석 제품의 변경 안전성](experience/cluml.md): 고객사 데모 서버 운영 중 관찰된 대기 증상을 요청 제한 동시성 문제로 재정의하고, 허용치 초과 요청 통과를 막는 불변 조건과 회귀 테스트 기준을 세웠습니다.
- [생성 서비스 검증과 변경 이력 기준](experience/tmaxcloud.md): No-code platform에서 generated service의 request/response와 DB write/read 반영을 배포 후 확인하던 흐름을 배포 전 E2E 검증 단계로 옮겼습니다. CAU 변경 이력 table과 row snapshot copy 흐름은 generated CRUD service code 안에서 같은 generation boundary로 관리되게 했습니다.
- [Rust SQL engine 오픈소스 기여](opensource/gluesql.md): GlueSQL에서 `SELECT DISTINCT`와 aggregate `DISTINCT`를 SQL translation, AST/query representation, executor de-duplication, aggregate state, AST builder, test-suite 경로로 구현·검증했습니다. `gluesql/gluesql` 기준 merged PR 45개 이상과 review/docs 기록으로 확인할 수 있는 기여입니다.
- [개인 제품의 상태 계약과 리뷰 기준](projects/coupler.md): React Native app, API, 관리자 웹의 가입·심사 상태 계약, TypeScript 운영 기준, DB/release guardrail, 코드 리뷰 기준을 제품 운영 기준으로 정리했습니다. Meta SDK postback 기준 1개월 심사 요청 관련 event count가 약 40개에서 약 1.1k 수준으로 증가한 것을 확인했습니다.

## 개발 관점

유지보수를 위한 일관성, 확장성, 응집도와 결합도, 책임 분리가 분명한 코드 작성을 중요하게 봅니다.

반복 구현의 일부 허들이 낮아질수록 문제 정의, 도메인 정책, 책임 범위, 테스트 기준, 리뷰 기준을 흔들리지 않게 남기는 일이 더 중요해진다고 봅니다. 좋은 개발 문서는 동료와 AI agent가 같은 관점으로 구현과 리뷰를 이어갈 수 있게 만드는 실행 가능한 기준이어야 한다고 생각합니다.

자세한 기준은 [원칙](engineering-principles.md)에 정리했습니다.

## 주요 기술 영역

- Platform: 메타데이터와 스키마를 SQL/DDL, generated service code, DB 반영 검증, 변경 이력, 테스트 기준으로 연결
- Rust/SQL: SQL engine internals, parser/AST, storage, Rust 오픈소스 기여, 코드 리뷰
- Product quality: 보안 이벤트 분석 제품군의 표시 일관성, Rust 서비스 compatibility 확인, React Native 제품 운영, TypeScript 전환, 회원가입/심사 흐름 정리
- Review system: 요구사항 기반 작업 정의, 완료 기준, test coverage, change-safety review, AI-assisted development 검증 기준

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
- [활동](activities/index.md)
