# 경력

## 경력 타임라인

| 기간 | 조직 | 역할 | 주요 내용 |
| --- | --- | --- | --- |
| 2025.03 - 2026.07 | ClumL | Software Engineer | 보안 이벤트 분석 제품군, 요청 제한 동시성 검증 기준, 탐지 화면·리포트 표시 일관성, Rust service compatibility 확인, PR review |
| 2021.10 - 2024.11 | 티맥스클라우드 | Software Engineer | Java/TypeScript No-code 플랫폼, service/API 코드 생성 검증, 데이터 변경 이력 저장·조회, entity export/import, SQL/DDL generation |

## 주요 성과

- [ClumL](cluml.md): 고객사 데모 서버 운영 중 관찰된 대기 증상을 요청 제한 정확성 문제로 재정의하고, 허용치 대비 10배 이상 초과 요청 통과가 발생하던 동시성 문제를 허용치 이하로 제한하는 처리 기준과 회귀 테스트로 정리했습니다.
- [티맥스클라우드 service/API 코드 생성 검증](tmaxcloud.md): No-code platform에서 화면으로 정의한 service/API의 request/response와 DB write/read 확인을 배포 전 E2E 검증 단계로 옮겨, 당시 작업 기준 반복되던 설계-검증 cycle을 약 4주에서 2주 수준으로 줄이는 데 기여했습니다.
- [티맥스클라우드 데이터 변경 이력](tmaxcloud.md): 변경 이력 옵션이 켜진 entity의 원본 table과 변경 이력 table을 생성하고, insert/update/delete 서비스 코드가 변경 전 row data를 저장해 특정 시점 table 상태를 조회할 수 있도록 설계·구현했습니다.

## 엔지니어링 방향

제 핵심 배경은 서비스 설계 정보와 스키마를 코드, SQL, 데이터 흐름, 검증 기준으로 연결하는 백엔드와 플랫폼 엔지니어링입니다.

ClumL에서는 운영 중 드러난 증상을 요청 제한 정확성, 표시 일관성, 설정 변경 안전성 문제로 나누고 재현 조건과 테스트 기준을 세웠습니다.

티맥스클라우드에서는 UI에서 정의한 app, entity, service/API 정보가 Java service code, SQL/DDL, DB 반영 검증, 데이터 변경 이력 저장·조회로 이어지도록 backend/platform 경계를 구현했습니다.

GlueSQL에서는 Rust SQL engine 오픈소스에 기여하며 `SELECT DISTINCT`와 aggregate `DISTINCT`, AST builder, aggregate 처리, Parquet storage, 회귀 테스트, PR review와 mentoring을 경험했습니다.

최근의 개발 과정에서는 구현 품질뿐 아니라 문서화와 검증 기준도 중요하다고 봅니다. 요구사항, 도메인 정책, 책임 범위, 테스트 기준, 리뷰 기준을 명확히 남겨 동료가 같은 기준으로 구현과 리뷰를 진행할 수 있게 하는 방향을 지향합니다.
