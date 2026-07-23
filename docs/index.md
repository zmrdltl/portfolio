# 김민식 기술 포트폴리오

PLATFORM SOFTWARE ENGINEER

## 요약

코드 생성 플랫폼, Rust 서비스, SQL 엔진, 모바일 제품에서 데이터·상태·동시성 문제를 다뤄 왔습니다. 증상과 원인을 나누고, 선택한 해결책을 구현한 뒤 API·DB·회귀 테스트·릴리스 확인으로 결과를 검증합니다.

## 대표 작업

### [ClumL · 외부 LLM API 호출량 제어 동시성 수정](experience/cluml.md)

**유형·기간:** 정규 경력 · 2025.03 - 2026.07

**역할:** Rust 백엔드 문제 분석·구현 및 회귀 검증

**핵심 변화:** 여러 LLM API 호출이 같은 예약 전 상태를 읽던 확인-예약 경합을 수정했습니다.

**검증:** 같은 동시성 조건에서 실효 동시 호출 한도의 10배 이상까지 LLM API 호출이 통과하던 현상을 재현하고, 수정 후 허용치 이하로 유지됨을 확인했습니다.

**기술:** `Rust` · `동시성 제어` · `회귀 테스트`

### [티맥스클라우드 · 코드 생성 플랫폼의 배포 전 API 테스트 기능](experience/tmaxcloud.md)

**유형·기간:** 정규 경력 · 2021.10 - 2024.11

**역할:** Java·TypeScript 코드 생성 플랫폼 기능 설계·구현 및 검증

**핵심 변화:** UI에서 정의한 서비스가 Java API·SQL과 JAR로 생성되는 플랫폼에, 생성된 API를 배포하지 않고 호출해 응답과 DB 반영을 확인하는 기능을 구현했습니다.

**검증:** 잘못된 서비스 정의·요청·응답 형식과 DB 반영 오류를 한 차례 약 20분의 빌드·배포·확인 절차 없이 발견할 수 있게 했습니다.

**기술:** `Java` · `WebSocket` · `Tibero`

### [GlueSQL · DISTINCT 실행 의미 구현](opensource/gluesql.md)

**유형·기간:** 오픈소스 기여 · 2021.06 - 현재

**역할:** Rust SQL 엔진 기능 직접 구현 및 기여자 코드 리뷰

**핵심 변화:** projection 결과 row 중복 제거와 aggregate state의 중복 값 관리를 분리해 `DISTINCT` 의미를 실행 경로에 연결했습니다.

**검증:** 단일·복수 column, map, schemaless row, aggregate `DISTINCT`를 회귀 테스트로 확인했습니다.

**기술:** `Rust` · `parser/AST` · `SQL executor`

### [Coupler · 모바일 소개팅 앱 개발총괄](projects/coupler.md)

**유형·기간:** 개인 제품 · 2024.07 - 현재

**역할:** React Native 앱·Express API·React 관리자 웹·MySQL DB의 개발 및 운영 총괄

**핵심 변화:** 앱과 관리자 웹이 심사 상태를 각자 추론하지 않고 API가 반환한 접근 상태를 따르도록 통일했습니다.

**검증:** API 응답, 모바일 화면 분기, 관리자 심사 큐의 회귀 테스트를 릴리스 확인 항목으로 운영했습니다.

**기술:** `React Native` · `TypeScript` · `MySQL`

## 더 보기

[개발 원칙](engineering-principles.md)에서 문제 분해, 선택, 검증에 공통으로 적용하는 기준을 확인할 수 있습니다.

## 연락처

- [Email](mailto:meenseek5929@naver.com)
- [GitHub](https://github.com/zmrdltl)
