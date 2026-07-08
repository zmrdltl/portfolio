# 김민식 기술 포트폴리오

PLATFORM SOFTWARE ENGINEER

## 요약

제품과 플랫폼의 변경이 빨라질수록 깨지기 쉬운 상태 전이, 데이터 흐름, 서비스 계약을 검증 가능한 기준으로 정리하는 Platform Software Engineer입니다.

최신 경력에서는 운영 중 드러난 요청 제한 동시성 문제를 재현 가능한 불변 조건과 회귀 테스트 기준으로 닫았고, 이전 경력에서는 generated service와 데이터 이력을 배포 전 검증 가능한 구조로 만들었습니다. 제품 개발에서는 앱/API/관리자 웹/DB가 같은 상태 계약과 릴리스 기준을 따르도록 정리했습니다.

AI-assisted development 환경에서도 코드 생성 자체보다 문제 정의, 문서, 타입 검사, 회귀 테스트, 리뷰 기준을 함께 고정해 운영 가능한 변경만 남기는 방식을 사용합니다. 공개 기술 깊이는 Rust SQL engine 오픈소스 기여로 보강합니다. GlueSQL에서는 query semantics, AST/execution path, storage surface, test suite를 PR과 review 기록으로 남겼습니다.

## 대표 작업

- [보안 분석 제품의 변경 안전성](experience/cluml.md): 고객사 데모 서버 운영 중 관찰된 대기 증상을 요청 제한 동시성 정확성 문제로 재정의하고, 허용치 초과 요청 통과를 막는 불변 조건과 회귀 테스트 기준으로 닫았습니다. 탐지 화면·리포트 표시 일관성, Rust 서비스 설정 변경, PR review 기준도 같은 변경 안전성 흐름 안에서 다뤘습니다.
- [생성 플랫폼 검증과 데이터 이력](experience/tmaxcloud.md): No-code platform에서 generated service의 request/response와 DB write/read 반영을 배포 후 확인하던 흐름을 배포 전 E2E 검증 단계로 옮겼습니다. 변경 이력 기능(CAU)의 table과 row snapshot copy 흐름은 generated CRUD service code 안에서 같은 generation boundary로 관리되게 했습니다.
- [Rust SQL engine 오픈소스 기여](opensource/gluesql.md): GlueSQL에서 `SELECT DISTINCT`와 aggregate `DISTINCT`를 SQL translation, AST/query representation, executor de-duplication, aggregate state, AST builder, test-suite 경로로 구현·검증했습니다. `gluesql/gluesql` 기준 merged PR 45개 이상과 review/docs 기록으로 확인할 수 있는 기여입니다.
- [제품 상태 계약과 운영 기준](projects/coupler.md): React Native 앱, API, 관리자 웹, DB가 같은 가입·심사 상태 모델을 따르도록 정리하고, TypeScript 운영 기준, typecheck/migration guard, 회귀 검증, 코드 리뷰 기준을 제품 변경 기준으로 연결했습니다.

## 개발 운영 관점

유지보수를 위한 일관성, 확장성, 응집도와 결합도, 책임 분리가 분명한 코드 작성을 중요하게 봅니다.

반복 구현의 일부 허들이 낮아질수록 문제 정의, 도메인 정책, 책임 범위, 테스트 기준, 리뷰 기준을 흔들리지 않게 남기는 일이 더 중요해진다고 봅니다. 좋은 개발 문서는 동료와 자동화 도구가 같은 기준으로 구현과 리뷰를 이어갈 수 있게 만드는 실행 가능한 기준이어야 한다고 생각합니다.

자세한 기준은 [원칙](engineering-principles.md)에 정리했습니다.

## 주요 기술 영역

- AI-assisted engineering workflow: 문서, 타입 검사, 테스트, 리뷰, 릴리스 기준이 함께 움직이도록 변경 단위와 검증 기준을 설계
- Service contract: 앱/API/관리자 웹/DB가 같은 상태 모델을 따르도록 서버 응답 계약, 심사 정책, 권한·화면 분기 기준을 정리
- Generated platform: 메타데이터와 스키마를 SQL/DDL, generated service code, DB 반영 검증, 변경 이력, 테스트 기준으로 연결
- Change safety: 운영 증상, 설정 변경, 표시 일관성 문제를 재현 조건, 완료 기준, 회귀 테스트, PR review 기준으로 분리
- Rust/SQL: SQL engine internals, parser/AST, storage, Rust 오픈소스 기여, 코드 리뷰

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
