# 티맥스클라우드

- 역할: Software Engineer
- 기간: 2021.10 - 2024.11

## 개요

Java/TypeScript 기반 No-code 플랫폼에서 메타데이터, 엔티티, 서비스 설계 정보를 DDL, SQL, Java 서비스 코드, 데이터 동기화, 변경 이력, 테스트 도구로 연결하는 backend/platform 기능을 구현했습니다.

작업 범위는 메타데이터 모델링, SQL 생성, Java 서비스 코드 생성, 엔티티 동기화, 변경 이력, UI/테스트 도구, Kubernetes/Redis 연구를 포함했습니다.

## 메타데이터 기반 생성 흐름

### 문제

서비스 설계 정보가 실제 DDL, SQL, Java 서비스 코드, 배포 산출물, 테스트 흐름으로 이어지기 위해서는 메타데이터 모델과 생성 로직이 일관되어야 했습니다.

### 역할

- Service in/out DTO, context, node service 구조를 정의했습니다.
- Freemarker template 기반 Select/Insert/Update/Delete Java 서비스 코드 생성 로직을 작성했습니다.
- SQL Generator를 백엔드에서 직접 사용하는 라이브러리 구조로 개선했습니다.
- JSON 입력 기반 CREATE/ALTER/VIEW, JOIN, 조건식, DML SQL 생성과 JUnit 테스트를 구현했습니다.

## 데이터 흐름과 변경 이력

- 앱 간 엔티티 export/import 기능을 구현했습니다.
- topic/subscriber 기반 데이터 복사 및 동기화 흐름을 설계했습니다.
- 변경 이력 테이블 생성, CRUD 전 스냅샷 저장, 특정 시점 테이블 복원 SQL을 구현했습니다.

## Tibero와 데이터 기능

- Tibero RDBMS에서 JSON type 기반 NoSQL-like CRUD, JSON Path Expression, JSON Schema validation을 구현했습니다.
- 메타데이터 단위 컬럼 암호화 설정과 DBMS_CRYPTO 기반 암호화/복호화 SQL 및 CRUD 서비스 생성 로직을 설계했습니다.

## 대표 생성 서비스 구조

내부 class/package명은 공개하지 않고, 생성 서비스 구조는 generic 이름으로만 표현합니다.

- `ClientRequest` -> `ServiceDispatcher` -> `GeneratedService`
- `GeneratedService` -> `RequestDTO`/`Context` -> validation -> SQL/CRUD execution
- SQL/CRUD result -> response mapper -> `ClientResponse`

## 테스트와 운영 보조 도구

- React Flow 기반 엔티티 관계 시각화 화면을 구현했습니다.
- Material UI 기반 메타데이터 변경 이력 화면에서 filtering, sorting, grouping, highlighting 기능을 구현했습니다.
- WebSocket 기반 서비스 테스트 화면을 구현했습니다.
- 서비스 ID, 메시지 핸들러, 응답 처리, 로그/오류 처리 구조를 중앙화해 신규 서비스 추가와 디버깅 비용을 줄였습니다.

## Kubernetes와 Redis 연구

- Kubernetes API Exec/client-go 기반 Terraform 원격 실행을 검증했습니다.
- 팀 개발/테스트용 1 master / 3 worker Kubernetes 클러스터를 구성하고 CRI-O, MetalLB 기반 네트워크와 로드밸런싱 환경을 세팅했습니다.
- Redis Operator/Redis Cluster Proxy 기반 Redis 배포, TLS, monitoring, 외부 접근 redirect 문제를 연구했습니다.
- Redis Operator와 proxy 조합으로 Redis cluster 외부 접근과 redirect 동작을 검증하며 패킷 전달 성공률 95% 이상을 확보했고, Redis Insight와 Prometheus 기반 monitoring으로 장애 탐지 시간을 30% 단축했습니다.
- Redis persistence, replication, sharding/failover, Redis Operator CRD/parameter, Redis Cluster Proxy, Redis Insight를 정리해 팀 세미나 자료로 발표했습니다.
- Redis Operator 검증 과정에서 관련 upstream PR 3개가 병합되었습니다: [#265](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/265), [#308](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/308), [#313](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/313).

## 공개 참고 링크

- [Redis & Redis Operator 발표자료](https://docs.google.com/presentation/d/1l67gAgutm97YNqp5bSXZAZbI_zCJUSV-/edit)
- [Redis Proxy 발표자료](https://docs.google.com/presentation/d/12sXamn6Q9la4gSgyEmfi6f00YmS3FHU7/edit)
- [Redis 연구자료](https://drive.google.com/drive/folders/1YMlcGRGy4Yyar5SSkBVY02XzEnUmnrFD)

## 기술

Java, TypeScript, React, Material UI, React Flow, WebSocket, Freemarker, Tibero, SQL generation, JUnit, Kubernetes, Terraform, Redis Operator, Redis Cluster Proxy
