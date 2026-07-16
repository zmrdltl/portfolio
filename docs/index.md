# 김민식 기술 포트폴리오

PLATFORM SOFTWARE ENGINEER

## 요약

생성된 API의 응답과 DB 쓰기·읽기를 배포 전에 검증하고, Rust 동시성 문제를 수정하며, 제품 변경을 회귀 테스트와 릴리스 기준에 연결해 온 Platform Software Engineer입니다.

## 대표 작업

| 대표 작업 | 핵심 변경 | 검증·결과 |
| --- | --- | --- |
| [ClumL · Rust 서비스 정확성](experience/cluml.md) | 요청 제한 경합 수정, 반복 운영 설정 외부화 | 수정 전 허용치의 10배 이상 통과 재현 → 수정 후 허용치 이하 |
| [티맥스클라우드 · 생성 API 검증](experience/tmaxcloud.md) | API 배포 전 검증, 데이터 변경 이력 구현 | 당시 반복 설계·검증 주기 약 4주 → 2주 수준 단축에 기여 |
| [GlueSQL · Rust SQL 엔진](opensource/gluesql.md) | `DISTINCT`를 SQL 변환·실행·집계·테스트에 연결 | 병합 PR 50건 · 현재 리뷰어 |
| [Coupler · 모바일 앱 개발총괄](projects/coupler.md) | 가입 신청을 단계형 심사와 서버 응답 기반 심사 상태 계약 중심으로 개편 | Meta SDK 최초 가입 심사 도달 이벤트: 개편 전 약 10건 → 개편 후 약 100건 관측 |

## 작업별 기술

| 작업 | 기술 |
| --- | --- |
| ClumL | Rust, 동시성 제어, 요청 제한, 설정 관리, GraphQL, 회귀 테스트, Chrono/Jiff |
| 티맥스클라우드 | Java, TypeScript, React, WebSocket, Monaco Editor, FreeMarker, Tibero, SQL·DDL 생성, JUnit, JaCoCo |
| GlueSQL | Rust, SQL 엔진 내부 구조, parser/AST, 집계 함수, Parquet storage, 코드 리뷰 |
| Coupler | React Native, React, TypeScript, Express, MySQL, API 계약, 상태 전이 설계, GitHub Actions |

## 연락처

- [Email](mailto:meenseek5929@naver.com)
- [GitHub](https://github.com/zmrdltl)
