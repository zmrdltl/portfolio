# 경력

## Timeline

| 기간 | 조직 | 역할 | 주요 내용 |
| --- | --- | --- | --- |
| 2025.03 - 2026.07 | ClumL | Software Engineer | 보안 이벤트 분석 제품군, 요청 제한 동시성 검증 기준, 탐지 화면·리포트 표시 일관성, Rust service compatibility 확인, PR review |
| 2021.10 - 2024.11 | 티맥스클라우드 | Software Engineer | Java/TypeScript No-code 플랫폼, generated service E2E 검증, 변경 이력 기능(CAU), SQL/DDL generation |

## 경력 스냅샷

- [ClumL](cluml.md): 고객사 데모 서버 운영 중 관찰된 대기 증상을 요청 제한 정확성 문제로 재정의하고, 허용치 대비 10배 이상 초과 요청 통과가 발생하던 동시성 문제를 허용치 이하로 제한하는 불변 조건과 회귀 테스트 기준으로 닫았습니다.
- [티맥스클라우드 generated service](tmaxcloud.md): No-code platform에서 generated service의 request/response와 DB write/read 확인을 배포 전 E2E 검증 단계로 옮겨, 당시 작업 기준 반복되던 설계-검증 cycle을 약 4주에서 2주 수준으로 줄이는 데 기여했습니다.
- [티맥스클라우드 변경 이력 기능(CAU)](tmaxcloud.md): 원본 table, 변경 이력 table, generated CRUD service code의 row snapshot copy 흐름, 특정 시점 select SQL 기준을 같은 generation boundary 안에서 관리하도록 설계·구현했습니다.

## 방향

제 핵심 배경은 서비스 설계 정보와 스키마를 코드, SQL, 데이터 흐름, 검증 기준으로 연결하는 백엔드와 플랫폼 엔지니어링입니다.

ClumL에서는 운영 중 드러난 증상을 좁은 정확성·변경 안전성 문제로 분리하고, 재현 조건, 완료 기준, 회귀 테스트, PR review 기준으로 닫는 역할을 맡았습니다.

티맥스클라우드에서는 UI에서 정의한 app, entity, service/API 정보가 SQL/DDL, generated service code, DB 반영 검증, 변경 이력 기준으로 이어지도록 backend/platform 경계를 구현했습니다.

GlueSQL 오픈소스 활동은 기술 깊이를 보여주는 대표 경험입니다. SQL engine 내부 구조, parser와 AST, Rust 기반 데이터 처리, storage 지원, test suite, 멘토링, 코드 리뷰 경험을 이어왔습니다.

최근의 개발 과정에서는 구현 품질뿐 아니라 문서화와 검증 기준도 중요하다고 봅니다. 요구사항, 도메인 정책, 책임 범위, 테스트 기준, 리뷰 기준을 명확히 남겨 동료가 같은 기준으로 구현과 리뷰를 진행할 수 있게 하는 방향을 지향합니다.
