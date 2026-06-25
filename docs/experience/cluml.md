# ClumL

- 역할: Software Engineer
- 기간: 2025.03 - Present

## 개요

보안 이벤트 분석 제품군에서 탐지 화면·리포트의 데이터 정합성, Rust 서비스 테스트 안정화, issue/spec 작성, PR review를 수행하고 있습니다.

## 주요 업무

- 탐지 목록/상세, time range, port/packet 표시, chart/report 회귀를 수정해 분석 화면과 보고서 신뢰성을 개선했습니다.
- problem, scope, acceptance criteria, test 기준을 포함한 issue로 작업 범위와 검증 기준을 명확화했습니다.
- PR 변경 범위, API/protocol compatibility, test coverage, lint/clippy, regression risk를 검토했습니다.

## 작업 영역

### 분석 UI와 데이터 정합성

보안 분석자가 확인하는 탐지 목록, 상세 화면, time range, port/packet, chart/report 표시를 다뤘습니다. 이 작업은 단순 화면 수정이 아니라 분석 결과와 보고서 산출물이 같은 이벤트 맥락을 보여주도록 맞추는 정합성 작업입니다.

### Rust 서비스 테스트 안정화

Rust 서비스의 설정, 날짜·시간 처리, serialization, 테스트 경계를 검토하며 회귀 위험을 줄이는 방향으로 작업했습니다. dependency, lint/clippy, CI failure, compatibility risk는 PR review에서 별도 확인 항목으로 다룹니다.

### Issue/spec 기반 작업 정의

작업을 시작하기 전에 problem, scope, acceptance criteria, non-goal, test 기준을 issue/spec에 정리합니다. 이 기준은 동료와 자동화 도구가 같은 범위 안에서 구현하고, 리뷰 단계에서 변경 범위와 회귀 위험을 확인하기 위한 계약으로 사용합니다.

### PR review와 품질 관리

issue/spec와 PR diff 사이의 정합성, API/protocol compatibility, test coverage, lint/clippy, regression risk를 검토하며 변경 범위가 합의된 요구사항과 검증 기준 안에 머물도록 확인합니다.

## 기술

Rust, GraphQL, Yew, TypeScript, PostgreSQL, RocksDB
