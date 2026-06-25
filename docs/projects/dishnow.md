# Dishnow

2019.02 - 2019.12

## 개요

Dishnow는 사용자 앱과 사장님 앱으로 구성된 실시간 식당 예약 모바일 앱입니다. 사용자가 주변 식당에 예약 요청을 보내면, 사장님 앱에서 요청을 수락하고 사용자가 최종 예약을 확정하는 흐름을 구현했습니다.

React Native, React, Node.js, MySQL, AWS 기반으로 사용자/사장님 앱, 인증, 예약 상태, push 알림, 리뷰, point system을 개발했습니다.

## 역할과 범위

- 개발자 3인, 기획자 4인, 디자이너 1인 팀으로 진행했습니다.
- 사용자 앱과 사장님 앱의 초기 개발 및 기능 확장에 참여했습니다.
- App 기능 설계, MySQL database 설계, API 연동, 예약 상태 흐름 구현에 참여했습니다.
- 공통 social login, JWT 인증, push notification, review, point system 구현에 참여했습니다.

## 문제와 제약

사용자 앱의 식당 검색/예약 흐름과 사장님 앱의 예약 관리 흐름이 같은 reservation state를 기준으로 동작해야 했습니다.

예약 요청, 사장님 수락, 사용자 확정, SMS 발송, 리뷰 작성이 모두 같은 예약 record의 상태 변화로 이어져야 했고, push notification 누락은 예약 성공률에 직접 영향을 줄 수 있었습니다.

## 설계와 구현

예약 DB table을 중심으로 예약 목록과 상태를 관리하고, 사용자 앱과 사장님 앱을 분리해 구현했습니다.

- 사용자 앱에서 반경 내 식당 검색, 예약 요청, 최종 예약 확정, 리뷰 작성, 계정 관리 기능을 구현했습니다.
- 사장님 앱에서 가게 정보와 예약 요청을 관리하는 기능을 구현했습니다.
- User app에서 예약 정보를 보내면 server가 예약 정보를 저장하고 OneSignal로 host app에 예약 요청 push를 보냈습니다.
- Host app이 예약을 수락하면 server가 예약 상태를 갱신하고 user app에 수락 push를 보냈습니다.
- User app이 최종 예약을 확정하면 server가 상태를 갱신하고 Aligo SMS로 예약 확정 문자를 전송했습니다.
- 예약 종료 후 review와 별점 정보를 저장했습니다.
- ID/password 방식에서 JWT token 인증으로 전환하며 token 기반 session 관리 구조를 적용했습니다.
- AsyncStorage로 app 종료 후 인증 상태를 유지했습니다.
- React/redux 기반 상태 관리를 적용했습니다.

## 검증과 지표

당시 프로젝트 기록 기준으로 아래 결과를 사용합니다. 공개 링크는 대표 code/reference이며, store 배포·download·예약 성공률 지표의 직접 근거는 아닙니다.

- Google Play와 App Store에 배포했습니다.
- App download 100+를 기록했습니다.
- Push notification 적용 전후 예약 상태 data를 비교해 예약 성공률 35% 개선을 확인했습니다.
- 창업 관련 프로그램 수상과 예비창업패키지 지원 이력이 있습니다.

## 남은 제약

JWT token refresh logic은 완전히 구현하지 못한 제약으로 남았습니다. 이 프로젝트는 초기 창업 프로젝트이므로 현재 포트폴리오에서는 제품 흐름, mobile/backend 협업, 예약 상태 관리 경험을 보조 신호로 사용합니다.

## 공개 참고 링크

- [Dishnow GitHub organization](https://github.com/dishnoww)
- [DishnowUser repository](https://github.com/HongikDevelopers/DishnowUser)
- [Dishnow 홍보 영상](https://youtu.be/4_j_0OXUodw?si=eulwjSBBXG1UrEKg)

## 기술

React Native, React, Node.js, Java 8, MySQL, AWS RDS, EC2, S3, JWT, OneSignal Push, Aligo SMS, Kakao, Naver, Facebook, Google Maps API
