# 김민식 기술 포트폴리오

PLATFORM SOFTWARE ENGINEER

## 요약

화면에서 정의한 service/API를 코드와 SQL로 만들고, 제품 변경이 API 응답, DB 상태, 테스트, 릴리스 기준까지 반영되는지 확인하는 Platform Software Engineer입니다.

최신 경력인 ClumL에서는 보안 분석 제품의 요청 제한 동시성 문제를 재정의하고, 허용치 초과 요청이 작업 실행 단계로 넘어가지 않도록 처리 기준과 회귀 테스트를 세웠습니다. TmaxCloud No-code platform에서는 화면에서 설계한 service/API를 Java 코드와 SQL로 생성하고, 배포 전 request/response와 DB write/read를 확인할 수 있게 했습니다. 배포된 앱의 데이터 변경 이력은 저장·조회해 특정 시점의 table 상태를 보여줄 수 있게 했습니다. Coupler에서는 모바일 소개팅 앱 개발총괄로 React Native 앱, API, 관리자 웹, DB의 가입·심사 흐름을 재구성하고, 정책·플로우·아키텍처와 릴리스·배포/롤백 기준을 공개 개발 문서로 정리했습니다.

오픈소스에서는 Rust SQL engine GlueSQL에 기여했습니다. `SELECT DISTINCT`와 aggregate `DISTINCT` 구현, SQL parser와 AST 표현, executor와 aggregate 처리, Parquet storage, 회귀 테스트, PR review에 참여했습니다.

## 대표 작업

- [보안 분석 엔진 요청 제한 정확성](experience/cluml.md): 고객사 데모 서버 운영 중 관찰된 장시간 대기 증상을 요청 제한 로직의 동시성 문제로 재정의했습니다. 여러 요청이 같은 예약 전 상태를 보고 허용치보다 많이 통과할 수 있는 지점을 확인하고, 작업 실행 전에 제한 기준을 지키도록 수용 기준과 회귀 테스트 기준을 세웠습니다.
- [No-code platform 서비스 생성과 데이터 이력](experience/tmaxcloud.md): TmaxCloud No-code platform에서 화면으로 설계한 service/API를 Java 코드와 SQL로 생성하고, 배포 전 WebSocket test page로 request/response와 DB write/read를 확인할 수 있게 했습니다. 변경 이력 옵션이 켜진 entity는 배포 시 원본 table과 변경 이력 table을 생성하고, insert/update/delete 서비스 코드가 변경 전 row data를 이력 table에 저장해 특정 시점 table 상태를 조회할 수 있도록 했습니다.
- [Rust SQL engine 오픈소스 기여](opensource/gluesql.md): GlueSQL에서 `SELECT DISTINCT`와 aggregate `DISTINCT`를 SQL translation, AST 표현, executor 중복 제거, aggregate 처리, AST builder, 회귀 테스트까지 연결해 구현했습니다. `gluesql/gluesql` 기준 GitHub `is:merged` 검색에서 병합 PR 44건을 확인할 수 있습니다.
- [모바일 소개팅 앱 개발총괄](projects/coupler.md): 한 번에 약 30개 항목을 받던 가입 신청을 기본정보와 필수 프로필 중심의 단계형 심사 흐름으로 줄였습니다. 준회원·정회원 심사를 병렬로 제출할 수 있게 앱/API/Admin/DB 상태를 맞추고, 정책·플로우·아키텍처와 릴리스·배포/롤백 기준은 공개 개발 문서로 남겼습니다. Meta SDK postback event count 기준 1개월 심사 요청 도달 event가 약 50건에서 약 1.1k 수준으로 증가한 것을 확인했습니다.

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
