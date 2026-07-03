# ClumL

- 역할: Software Engineer
- 기간: 2025.03 - Present

## 개요

보안 이벤트 분석 제품군에서 요청 제한 동시성 문제 정의, 탐지 화면·리포트 표시 일관성, Rust 서비스 compatibility 확인, 요구사항·완료 기준 정리, PR review를 수행하고 있습니다.

현재 경력의 핵심은 고객사 데모 서버 운영 중 드러난 증상을 race condition, API/query contract, compatibility risk처럼 검증 가능한 문제로 나누고, 수정 범위와 완료 기준을 좁혀 변경 안전성을 높이는 일입니다.

## 주요 업무

- 고객사 데모 서버 운영 중 관찰된 장시간 대기 증상을 요청 제한 로직의 확인-예약 경합으로 재정의하고, 허용치 초과 요청 통과를 막는 동시성 불변 조건과 회귀 테스트 기준을 정리했습니다.
- 탐지 목록/상세, time range, port/packet 표시, chart/report 표시 문제에서 원인과 수정 범위를 분리하고, 분석 화면과 보고서가 같은 이벤트 맥락을 유지하는지 검토했습니다.
- 사용자 진입, 중앙 관리, 이벤트 데이터 저장·분배, 탐지·분석 결과 흐름을 역할 기준으로 문서화했습니다.
- 문제, 범위, 완료 기준, 테스트 기준을 정리해 작업 범위와 검증 기준을 명확화했습니다.
- PR 변경 범위, API/protocol compatibility, test coverage, lint/clippy, change-safety risk를 검토했습니다.

## 대표 구조

보안 이벤트 분석 흐름을 역할 기준으로 요약하면 아래와 같습니다.

```mermaid
flowchart LR
  browser["브라우저"]
  web["사용자 진입 웹 화면"]
  management["중앙 관리 서비스"]
  data["이벤트 데이터 저장·분배 서비스"]
  collector["네트워크 이벤트 생성·패킷 추출 서비스"]
  replay["로그·과거 데이터 적재 서비스"]
  detection["탐지 서비스"]
  analysis["분석 서비스"]
  timeseries["시계열 처리 서비스"]
  reference["위협 정보 참고 서비스"]
  extraUi["사용자 주도 추가 분석 화면"]
  extraEngine["추가 분석 엔진"]

  browser --> web
  web --> management
  web --> data
  web --> reference

  management --> detection
  detection --> management

  management --> analysis
  analysis --> management

  management --> collector
  collector --> management

  management --> timeseries
  timeseries --> management

  replay --> data
  collector --> data
  data --> collector
  data --> detection
  data --> analysis
  data --> timeseries
  timeseries --> data

  browser -. 사용자 주도 분석 이동 .-> extraUi
  extraUi --> extraEngine
```

이 구조에서 제가 중점적으로 다루는 부분은 보안 이벤트가 사용자 화면, 중앙 관리 서비스, 이벤트 데이터 저장·분배 서비스, 탐지·분석 서비스, 리포트 표시 기준 사이에서 같은 맥락을 유지하도록 확인하는 흐름입니다.

## 작업 영역

### 요청 제한 동시성 문제와 검증 기준

고객사 데모 서버 운영 중 관찰된 장시간 대기 증상을 단순 지연 문제가 아니라 요청 제한 로직의 확인-예약 경합으로 분리했습니다. 여러 동시 호출자가 같은 예약 전 상태를 보고 허용치 이상으로 요청을 통과시킬 수 있는 문제를 재현 가능한 불변 조건으로 정리했습니다.

수정 방향은 용량 확인과 예약 상태 갱신이 같은 상태를 기준으로 처리되게 하는 것이었고, PR review에서는 이 방향이 회귀 테스트와 함께 적용됐는지 확인했습니다. 이 작업은 성능 수치보다 서버가 허용치 바깥의 요청을 받아들이지 않는 정확성 기준을 세운 사례입니다.

### 분석 UI와 리포트 표시 일관성

보안 분석자가 확인하는 탐지 목록, 상세 화면, time range, port/packet, chart/report 표시를 다뤘습니다. 이 작업은 단순 화면 수정이 아니라 분석 결과와 보고서 산출물이 같은 이벤트 맥락을 보여주도록 맞추는 표시 기준 정리 작업입니다.

문제의 핵심은 같은 보안 이벤트를 목록, 상세, 차트, 리포트가 서로 다른 기준으로 보여줄 때 분석 신뢰성이 깨질 수 있다는 점입니다. 그래서 화면 단위 수정만 보지 않고, 표시 기준과 event context가 일관되게 유지되는지 확인했습니다.

### 제품 구조와 데이터 흐름 정리

사용자 요청 경로, 중앙 관리 서비스의 제어·상태 교환, 이벤트 데이터 저장·분배, 탐지·분석 결과 반환을 역할 기준으로 분리해 정리했습니다.

### Rust 서비스 compatibility 확인

Rust 서비스의 설정, 날짜·시간 처리, serialization, 테스트 경계를 검토하며 기존 동작과의 compatibility risk를 확인하는 방향으로 작업했습니다. dependency, lint/clippy, CI failure, compatibility risk는 PR review에서 별도 확인 항목으로 다룹니다.

### 작업 기준 정리

작업을 시작하기 전에 문제, 범위, 하지 않을 일, 완료 기준, 테스트 기준을 정리합니다. 이 기준은 동료와 AI agent가 같은 범위 안에서 구현하고, 리뷰 단계에서 변경 범위와 변경 안전성을 확인하기 위한 기준으로 사용합니다.

### PR review와 품질 관리

작업 기준과 PR diff 사이의 정합성, API/protocol compatibility, test coverage, lint/clippy, change-safety risk를 검토하며 변경 범위가 합의된 요구사항과 검증 기준 안에 머물도록 확인합니다.

## 결과

요청 제한 동시성 문제, 탐지 화면·리포트 표시 일관성, Rust 서비스 compatibility 확인, 작업 기준 정리와 PR review 기준을 제품 품질과 변경 안전성에 직접 연결되는 작업으로 다루고 있습니다.

## 기술

Rust, GraphQL, Yew, TypeScript, PostgreSQL, RocksDB
