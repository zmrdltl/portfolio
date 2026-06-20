# Coupler

2024.07 - Present

## 개요

React Native 앱, API, 관리자 웹, 공개 문서로 구성된 개인 제품 개발 프로젝트입니다.
1.0.0 운영 이후 2.0.0 전환 과정에서 TypeScript 전환 기준, 회원가입·심사 흐름 기준, 개발·리뷰 기준을 정리했습니다.

## 역할과 범위

- 개발총괄 / Software Engineer
- 모바일 앱, API, 관리자 웹, 공개 문서의 개발 기준과 릴리스 기준을 정리했습니다.

## 문제와 제약

React Native 제품을 1.0.0 초기 구현 이후 2.0.0까지 전환하면서 모바일 앱, API, 관리자 웹이 같은 상태 모델과 릴리스 기준으로 움직이도록 정리해야 했습니다.

## 설계와 구현

- 관리자 웹 TypeScript 전환과 typecheck CI/migration guard로 유지보수 기준을 고정했습니다.
- 회원가입과 심사 흐름을 use case와 [서버 응답 계약](https://github.com/coupler-developer/docs/blob/main/content/policy/signup-response-contract.md) 중심으로 분리해 화면 분기 기준을 단일화했습니다.
- Admin/Mobile/API가 같은 [회원 심사 정책](https://github.com/coupler-developer/docs/blob/main/content/policy/member-review-policy.md)을 쓰도록 제출/재제출 UX와 심사 목록 기준을 정리했습니다.
- [코드 리뷰 정책](https://github.com/coupler-developer/docs/blob/main/content/policy/code-review-policy.md)에 테스트, 문서 동기화, 회귀 안전성 기준을 남겼습니다.

## 검증과 기준

- typecheck CI와 migration guard로 관리자 웹 TypeScript 전환 기준을 고정했습니다.
- 회원가입 응답 계약과 회원 심사 정책으로 클라이언트 추측 라우팅과 심사 큐 중복 위험을 줄였습니다.

## 결과

2.0.0 전환 범위에서 모바일 앱, API, 관리자 웹의 개발 기준을 정리하고, 회원가입 응답 계약·회원 심사 정책·코드 리뷰 기준을 공개 문서로 남겼습니다.

## 기술

React Native, TypeScript, Express, MySQL
