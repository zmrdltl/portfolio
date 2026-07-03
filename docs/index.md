# 김민식 기술 포트폴리오

PLATFORM SOFTWARE ENGINEER

## 요약

서비스 설계 정보와 도메인 규칙을 SQL/DDL, 서비스 코드, 테스트·리뷰 기준으로 연결해 플랫폼 기능과 변경 안전성을 함께 다루는 Platform Software Engineer입니다.

대표 작업은 세 가지 축으로 정리합니다. 고객사 데모 서버 운영 중 드러난 race condition을 검증 기준으로 닫고 탐지 화면·리포트 표시 일관성을 맞추는 일, metadata-driven platform에서 생성된 서비스와 데이터 이력을 검증 가능하게 만드는 일, Rust SQL engine과 개인 제품에서 service contract와 test/review 기준을 구현하는 일입니다.

## 대표 작업

- [보안 분석 제품의 변경 안전성](experience/cluml.md): 고객사 데모 서버 운영 중 관찰된 대기 증상을 요청 제한 동시성 문제로 재정의하고, 허용치 초과 요청 통과를 막는 불변 조건과 회귀 테스트 기준을 세웠습니다. 탐지 화면·리포트 표시 문제도 query/API contract와 review 기준으로 나누어 검증했습니다.
- [생성 서비스 검증과 변경 이력 기준](experience/tmaxcloud.md): No-code platform에서 generated service의 request/response와 DB write/read 반영을 배포 전 확인하는 E2E test page를 만들고, CAU 변경 이력 table과 row snapshot copy 흐름을 generated CRUD service code에 연결했습니다.
- [Rust SQL engine 오픈소스 기여](opensource/gluesql.md): GlueSQL에서 `SELECT DISTINCT`와 aggregate `DISTINCT`를 SQL translation, AST/query representation, executor de-duplication, aggregate state, AST builder, test-suite 경로로 구현·검증했습니다.
- [개인 제품의 상태 계약과 리뷰 기준](projects/coupler.md): React Native app, API, 관리자 웹의 가입·심사 상태 계약, TypeScript 운영 기준, DB/release guardrail, 코드 리뷰 기준을 제품 운영 기준으로 정리했습니다.

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
- [원칙](engineering-principles.md)
- [GlueSQL](opensource/gluesql.md)
- [Coupler](projects/coupler.md)
- [활동](activities/index.md)
