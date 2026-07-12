# 김민식 기술 포트폴리오

PLATFORM SOFTWARE ENGINEER

## 요약

UI에서 엔티티·필드로 정의한 서비스를 Java 코드와 SQL로 생성하고, API 호출·DB 반영까지 검증하는 Platform Software Engineer입니다.

최근에는 보안 분석 제품의 요청 제한 동시성을 수정하고 Rust 서비스의 반복 운영 설정을 외부화했습니다. No-code platform에서는 생성 코드의 배포 전 검증과 데이터 변경 이력 저장 흐름을, GlueSQL에서는 Rust SQL 엔진의 `DISTINCT`를 구현했습니다.

## 대표 작업

- [보안 분석 제품의 Rust 서비스 개선](experience/cluml.md): 요청 제한 로직의 용량 확인과 제한 상태 갱신을 같은 잠금 구간으로 묶어 허용치 대비 10배 이상 초과 요청이 통과하던 경합을 수정했습니다. 반복 조정하던 탐지 판정값은 외부 설정으로 분리해 설정 변경 1회 작업 시간을 30% 이상 줄였습니다.
- [No-code platform 서비스 생성과 데이터 이력](experience/tmaxcloud.md): TmaxCloud No-code platform에서 UI의 엔티티·필드로 정의한 서비스를 Java 코드와 SQL로 생성했습니다. WebSocket test page에서는 배포 전에 API 응답과 DB 쓰기·읽기를 확인할 수 있게 했습니다. 변경 이력 table과 변경 전 row data 저장 흐름을 구현하고, select SQL로 특정 시점 table 상태를 재구성하는 기준을 정리했습니다.
- [Rust SQL engine 오픈소스 기여](opensource/gluesql.md): GlueSQL에서 `SELECT DISTINCT`와 aggregate `DISTINCT`를 SQL translation, AST 표현, executor 중복 제거, aggregate 처리, AST builder, 회귀 테스트까지 연결해 구현했습니다. `gluesql/gluesql` 기준 GitHub `is:merged` 검색에서 병합 PR 50건을 확인할 수 있습니다.
- [모바일 소개팅 앱 외주 프로젝트 개발총괄](projects/coupler.md): 한 번에 약 30개 항목을 받던 가입 신청을 기본정보와 필수 프로필 중심의 단계형 심사 흐름으로 줄였습니다. 준회원·정회원 심사를 병렬로 제출할 수 있게 앱/API/Admin/DB의 가입·심사 상태 구조를 맞추고, 정책·플로우·아키텍처와 릴리스·배포/롤백 기준은 공개 개발 문서로 남겼습니다. 최초 가입 심사 도달 시 기록되는 Meta SDK CompleteRegistration(등록 완료) 이벤트가 회원가입·심사 흐름 개편 전 약 10건에서 개편 후 약 100건으로 관측됐습니다.

## 기술

- Languages: Java, Rust, TypeScript, SQL
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
