# 티맥스클라우드

- 역할: Software Engineer
- 기간: 2021.10 - 2024.11

## 개요

Java/TypeScript 기반 No-code 플랫폼에서 메타데이터와 서비스 설계 정보를 DDL, SQL, Java 서비스 코드, 데이터 동기화, 변경 이력, 테스트 도구로 연결하는 backend/platform 기능을 구현했습니다.

이 페이지의 중심 사례는 No-code service generation platform입니다. team test Kubernetes 환경, Terraform/k8s 외부 provisioning 검증, Redis on Kubernetes 연구는 별도 검증 작업이므로 하단의 보조 사례로 분리합니다.

## 대표 작업로 보는 이유

No-code platform의 핵심 문제는 사용자가 화면에서 정의한 설계 정보가 실제 실행 코드, SQL, 데이터 흐름, 테스트 요청 형식까지 일관되게 이어져야 한다는 점이었습니다.

제가 맡은 범위는 단일 기능 구현보다 넓었습니다. metadata, entity, service definition을 기준으로 code generation, SQL/DDL generation, 데이터 이식성, 변경 이력, request/response tooling을 연결했습니다.

대표 결과는 아래와 같습니다.

- SQL Generator를 backend에서 직접 사용할 수 있는 구조로 바꾸며 당시 프로젝트 기록 기준 30% 이상의 성능 최적화를 확인했습니다.
- 별도 배포 플랫폼과 container 기동을 거친 뒤에야 확인되던 generated service 동작을 WebSocket 기반 E2E test page로 설계·검증 단계에서 확인할 수 있게 했습니다.
- 당시 작업 기준 설계-검증 사이클을 약 4주에서 2주 수준으로 줄이는 데 기여했습니다.
- WebSocket request/response 흐름에서 service mapping 중복 등록을 줄이고, service 통합 시간을 10% 이상 줄였으며, mapping 누락 debugging 문제를 compile-time 확인으로 완화했습니다.
- 반복 logging 구조를 invocation handler와 error logger로 정리해 수작업 log 작성 시간을 30% 이상 줄였습니다.

## No-code 서비스 생성 플랫폼

### 문제와 제약

사용자가 code를 직접 작성하지 않고 app을 설계·배포하려면, metadata, entity, service definition, deployment artifact가 같은 모델을 기준으로 이어져야 했습니다.

설계 정보는 table/entity 정의, service in/out DTO, context, validation, SQL/DDL, Java service code, 테스트 요청 형식까지 연결되어야 했고, 누락된 mapping이나 반복 등록은 배포 전후의 디버깅 비용으로 이어질 수 있었습니다.

```text
Metadata -> Business Entity -> Service Definition -> Generated Java Service
Entity/Table Definition -> SQL Generator -> DDL/DML
Generated Java Code + SQL -> Application Artifact -> Deployment/Test Flow
```

### 역할과 범위

- Service in/out DTO, context, node service 구조를 정의했습니다.
- Entity 속성과 DTO/context mapping, 검색·삭제·갱신 조건절, node service 유형별 Java service code generation 흐름을 구현했습니다.
- Freemarker template로 Select/Insert/Update/Delete 서비스 코드를 생성하는 로직을 작성했습니다.
- JSON input 기반 SQL Generator와 JUnit test를 구현했습니다.
- React/TypeScript 화면과 WebSocket 기반 generated service E2E test page, request/response tooling을 구현했습니다.

## 코드 생성

Service definition을 Java service code로 변환하기 위해 inDTO, outDTO, context, node service, SQL type mapping, template input 구조를 정리했습니다.

- 여러 node/block service를 하나의 service flow 안에서 구성할 수 있게 했습니다.
- Entity 속성과 inDTO, outDTO, context를 mapping하고, Update/Delete 결과를 다음 node의 input으로 넘길 수 있게 했습니다.
- ResultSet의 SQL type을 Java type으로 변환하는 반복 로직을 Freemarker macro로 정리했습니다.
- 여러 table을 갱신하는 service에서 node service별 다른 entity를 mapping하도록 구조를 설계했습니다.
- Service in/out DTO 정의에서 request JSON schema를 생성해 test request와 validation 기준을 맞출 수 있게 했습니다.

이 작업은 단순 CRUD 구현이 아니라, 설계 단계의 metadata가 실행 가능한 service code와 request/response contract로 이어지도록 만드는 생성 흐름이었습니다.

## 대표 생성 서비스 구조

내부 class/package명은 공개하지 않고, 생성 서비스 구조는 generic 이름으로만 표현합니다.

- `ClientRequest` -> `ServiceDispatcher` -> `GeneratedService`
- `GeneratedService` -> `RequestDTO`/`Context` -> validation -> SQL/CRUD execution
- SQL/CRUD result -> response mapper -> `ClientResponse`

## SQL Generator 구현

앱 배포 전 설계된 entity를 기반으로 JSON request를 받아 DDL/DML SQL을 생성하는 SQL Generator를 구현했습니다.

- DDL: `CREATE TABLE`, `ALTER TABLE`, `CREATE VIEW`
- DML/query: `SELECT`, `INSERT`, `INSERT ALL`, `UPDATE`, `DELETE`, `EXISTS`
- SQL expression: `CASE`, `AND`, `OR`, `WITH`, `JOIN`, view column mapping
- Key/sequence: primary key, sequence
- Test: JSON input에서 생성된 SQL을 JUnit으로 검증하고 coverage 확인이 가능하도록 구성했습니다.

기존에는 SQL generation 요청이 여러 계층을 왕복하는 구조였고, backend에서 바로 사용할 수 있는 library 형태가 아니었습니다. SQL Generator를 backend에 직접 import해 사용할 수 있는 구조로 바꾸면서 중복 작업을 줄이고, 당시 프로젝트 기록 기준 30% 이상의 성능 최적화를 확인했습니다.

## 엔티티 내보내기/가져오기

앱 간 entity data를 복사하고 동기화하기 위해 topic/subscriber 기반 export/import MVP를 구현했습니다.

- Export App은 내보낼 entity를 정의하고 topic을 등록합니다.
- Entity 변경이 발생하면 publish service가 message를 발행합니다.
- Import App은 가져올 entity 정보를 저장하고, 배포 시 DDL과 sync service를 생성합니다.
- Import App은 topic을 subscribe해 data 변경 사항을 동기화합니다.
- 선택된 속성만 복사할 수 있도록 DML과 metadata schema를 구성했습니다.

구현 과정에서 `created_by`, `created_at`, `modified_by`, `modified_at`, 선택 속성 목록 같은 동기화 metadata가 필요했고, 속성 선택 정보를 별도 table로 늘리는 대신 성능과 복잡도를 고려해 array-like field로 정리했습니다.

남은 제약도 있었습니다. 재배포 시 이미 복사된 data로 인해 PK 충돌이 생길 수 있고, 복사 중 message queue가 필요한 상황은 시간 제약상 완전히 해결하지 못했습니다. 공개 포트폴리오에서는 이 한계를 포함해 구현 범위를 설명합니다.

## 변경 이력과 테이블 복원

Entity별 변경 이력 설정을 제공하고, CRUD 전에 이전 record를 history table에 저장해 특정 시점의 table 상태를 복원할 수 있는 흐름을 구현했습니다.

- Entity 생성 시 변경 이력 table DDL을 생성했습니다.
- Insert/Update/Delete 전 PK에 해당하는 record snapshot을 history table에 저장했습니다.
- `UP_TO`, `LAST_MODIFIED_BY`, `DATA_SNAPSHOT`, deletion flag를 기준으로 변경 전후 상태를 비교했습니다.
- 원본 table과 변경 이력 table을 함께 조회해 현재 table에 없는 record도 복원 후보로 포함했습니다.
- `ROW_NUMBER() OVER (PARTITION BY PK ORDER BY ...)` 흐름으로 특정 시점 이전/이후 snapshot을 선택했습니다.

이 기능은 단순 audit log가 아니라, metadata 기반으로 생성되는 application table에 대해 시점별 data state를 설명하고 복원할 수 있게 하는 data integrity 기능이었습니다.

## Tibero JSON과 컬럼 암호화

Tibero RDBMS에서 JSON type을 활용해 NoSQL-like CRUD 기능을 구현했습니다.

- Collection/document table DDL을 자동 생성했습니다.
- JSON Path Expression으로 복잡한 JSON object, array, primitive 값을 조회·갱신했습니다.
- MongoDB `find`와 유사한 API와 projection으로 필요한 field만 조회하도록 했습니다.
- JSON Schema validation으로 request data 형식 오류와 무결성 문제를 줄였습니다.

또한 entity metadata column별 암호화 설정을 제공하고, 암호화 대상 column은 query binding 시 암호화하고 response 시 복호화하도록 CRUD service generation logic을 작성했습니다.

- DBMS_CRYPTO 기반 암호화/복호화 SQL을 생성했습니다.
- 다양한 metadata type을 단일 흐름으로 처리하기 위해 값을 string representation으로 변환했습니다.
- Key는 database에 직접 저장하지 않고 별도 server에서 관리하는 구조와 key rotation 가능성을 검토했습니다.

공개 문서에는 실제 key, 내부 function/package/class명, 운영 log format을 남기지 않습니다.

## 제품 UI와 서비스 테스트 도구

No-code platform의 metadata와 generated service를 검증하고 운영하기 위한 React/TypeScript UI와 WebSocket tooling을 구현했습니다.

### 엔티티 다이어그램

React Flow 기반으로 entity와 reference 관계를 시각화했습니다.

- 선택된 entity와 참조 관계를 계층적으로 표시했습니다.
- 상속 구조에서 상위 entity와 자식 entity를 배치했습니다.
- 참조한 entity와 참조된 entity를 재귀적으로 탐색했습니다.
- Node/edge, zoom, filtering, fit view, automatic layout, view mode를 제공했습니다.
- 정규식 검색과 highlight를 제공했습니다.
- Custom edge에서 평행 연결과 self-reference path를 별도로 처리했습니다.

수동으로 node/edge 위치와 연결 상태를 계산하던 복잡도를 줄이고, 검증된 library를 활용해 UI 상태 관리와 유지보수성을 개선했습니다.

### 메타데이터 변경 이력

Material UI 기반 metadata 변경 이력 화면을 구현했습니다.

- 수정 시간, metadata 이름, 수정 유형, 수정 전/후 값을 table로 표시했습니다.
- 검색어 기반 filtering과 highlight를 제공했습니다.
- 수정 시간 기준 grouping과 group 내부 column sorting을 지원했습니다.
- Column별 독립 정렬 상태를 관리했습니다.
- 조건부 cell 강조와 click/sort interaction을 구현했습니다.

변경 이력이 많은 상황에서 필요한 항목을 빠르게 찾을 수 있도록 검색과 highlight를 제공했고, 하나의 정렬 상태가 다른 column 정렬에 남는 문제를 독립 상태 관리로 해결했습니다.

### 요청/응답 흐름

WebSocket 기반 request/response 처리 방식을 개편했습니다.

- Service ID와 handler mapping을 중앙화했습니다.
- Backend service path와 client service ID의 reverse mapping을 구성했습니다.
- Message handler registry를 service group별로 자동 등록하도록 했습니다.
- Hard-coded service name string 대신 service map key를 사용하도록 request sender를 정리했습니다.
- Match pattern으로 service ID와 handler mapping 누락을 compile time에 확인할 수 있게 했습니다.
- Server response format을 success/error 여부와 관계없이 일관되게 처리하도록 정리했습니다.

기존에는 신규 service 추가 시 service ID mapper, handler registry, feature handler에 같은 정보를 여러 번 등록해야 했고, 누락 시 response가 handler까지 도달하지 않는 문제가 있었습니다. 개편 후 신규 service 추가 시 중복 등록을 줄였고, 당시 프로젝트 기록 기준 service 통합 시간을 10% 이상 줄였으며, 누락된 service mapping을 찾는 데 최소 30분 이상 걸리던 debugging 문제를 compile-time 확인으로 완화했습니다.

### 생성 서비스 E2E 테스트 페이지와 로거

No-code platform에서는 사용자가 UI에서 app, entity, service/API field를 정의하면 jar artifact가 생성되고, 이 artifact가 별도 배포 플랫폼으로 넘어가 배포 방식 설정과 container 기동을 거친 뒤에야 실제 동작을 확인할 수 있었습니다. 당시 service/API 수가 200-300개 수준으로 늘면서 잘못된 service definition이나 request/response mapping을 찾기 위해 build/deploy/verify cycle을 반복해야 했고, 한 번의 확인에 작업 기준 약 20분이 걸렸습니다.

이 비용을 줄이기 위해 WebSocket 기반 generated service E2E test page를 구현했습니다.

- WebSocket URL regex validation으로 잘못된 URL 연결 시도를 줄였습니다.
- Connection 성공 시 service 목록을 가져와 Accordion UI로 제공했습니다.
- Service별 JSON request template을 자동 생성했습니다.
- Monaco Editor에서 JSON request를 수정하고 generated service에 전송할 수 있게 했습니다.
- Response와 실제 DB write/read 반영 여부를 함께 확인해 service definition과 request/response mapping 오류를 배포 이후가 아니라 설계·검증 단계에서 찾을 수 있게 했습니다.

이 흐름은 jar 생성, 별도 배포 플랫폼 설정, container 기동 이후에야 확인되던 문제를 앞단으로 당겼고, 당시 작업 기준 설계-검증 사이클을 약 4주에서 2주 수준으로 줄이는 데 기여했습니다.

DAO/service 계층의 반복 logging도 invocation handler와 error logger 구조로 정리했습니다. 당시 프로젝트 기록 기준 수작업 log 작성 시간을 30% 이상 줄였고, SQL error metadata와 일반 log를 구분해 debugging 흐름을 명확히 했습니다.

## 팀 테스트 Kubernetes 환경

팀 개발·테스트 환경을 위해 1 master / 3 worker Kubernetes cluster를 구성했습니다.

- CentOS 기반 cluster에 CRI-O runtime과 MetalLB load balancing을 구성했습니다.
- 초기 kubenet 기반 구성에서 worker node 간 평균 3-5% packet loss가 발생했습니다.
- Compatible network plugin과 MetalLB 구성을 통해 packet loss를 1% 이하로 낮췄습니다.
- Node 중단 빈도를 월 5-6회 수준에서 월 1회 이하로 줄여 cluster availability를 개선했습니다.

## Terraform/k8s 외부 provisioning 검증

Kubernetes cluster 외부에서 Terraform command를 원격 실행해 EC2 instance를 생성·관리할 수 있는지 검증했습니다.

- Kubernetes API Exec과 `client-go`를 사용해 pod 내부에서 `terraform init`, `terraform apply`를 실행했습니다.
- Kubernetes 외부에서 pod 내부 command를 전달하는 구조와 gRPC 통신 흐름을 학습했습니다.
- Terraform/k8s provisioning 검증에서 반복 실행 시간을 평균 5분 줄인 것으로 정리했습니다.

공개 학습 기록:

- [gRPC 학습 기록](https://codecollector.tistory.com/1533)
- [Terraform/k8s 실험 기록](https://codecollector.tistory.com/1555)

## Kubernetes 환경의 Redis 연구

Kubernetes 환경에서 Redis를 안정적으로 배포하고 외부 client가 Redis Cluster에 접근할 때 발생하는 redirect 문제를 줄이기 위한 연구를 수행했습니다.

- Redis Operator로 Redis standalone/cluster 배포, TLS 설정, log 관리 기능을 실험했습니다.
- Redis Operator manifest와 custom variable 설정으로 cluster 연동을 조정했습니다.
- Redis Insight와 Prometheus를 연계해 Redis command 수행 상태와 metric을 시각화했습니다.
- Redis Cluster Proxy로 외부 client의 Redis Cluster redirect 문제를 해결했습니다.
- Predixy, TwemProxy, Corvus 등 proxy module을 비교했습니다.
- Redis Operator 검증 과정에서 관련 upstream PR 3개가 병합되었습니다: [#265](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/265), [#308](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/308), [#313](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/313).

검증 결과 Redis Operator와 proxy module 조합으로 packet 전달 성공률 95% 이상을 확보했고, Redis Insight와 Prometheus 기반 monitoring으로 장애 탐지 시간을 30% 단축했습니다.

## 기술

Java, TypeScript, React, Material UI, React Flow, WebSocket, Freemarker, Tibero, SQL generation, JUnit, Kubernetes, CRI-O, MetalLB, Terraform, client-go, Redis Operator, Redis Cluster Proxy, Prometheus
