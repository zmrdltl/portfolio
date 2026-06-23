# 지도 기반 소리 업로드/조회 사이트

2024.10 - 2024.11

## 개요

Java 17, Spring Boot, MySQL, Google Maps API 기반으로 위치별 소리 업로드·조회 API를 구현한 고객 납품 프로젝트입니다.

로그인한 사용자가 특정 위치에 소리와 이미지를 업로드하고, 다른 사용자가 지도 기반으로 소리를 조회·청취할 수 있는 흐름을 구현했습니다.

## 역할과 범위

- Backend 전반의 DB 설계와 API 구현을 담당했습니다.
- Frontend에서는 page별 API 연동과 상태 관리 일부를 구현했습니다.
- 고객 납품 프로젝트 특성상 source repository는 공개하지 않고, 공개 가능한 납품 이력 링크만 제공합니다.

## 문제와 제약

위치 기반 소리 업로드/조회 기능은 사용자 인증, 위치 정보 저장, file upload, 지도 좌표 조회, 사용자 profile, 청취 기록이 함께 맞물려야 했습니다.

또한 client, server, database가 각각 다른 hosting 환경에서 동작했기 때문에 HTTPS/API 호출, DB SSL connection, Google Maps API 연동을 안정적으로 맞춰야 했습니다.

## 구조와 인프라

- Frontend: Vercel
- Backend: Render
- Database: Aiven MySQL with SSL connection
- API: Google Maps API
- Backend stack: Java 17, Spring Boot 3+, Maven, MySQL
- Frontend stack: HTML, CSS, vanilla JavaScript

## API 범위

| Domain | Endpoint | Purpose |
| --- | --- | --- |
| User | `/api/users/register` | email/password 기반 회원가입 |
| User | `/api/users/login` | login 후 JWT token 발급 |
| User | `/api/users/logout` | JWT token 기반 logout |
| User | `/api/users/delete` | 회원 탈퇴 및 사용자 data 삭제 |
| User | `/api/users/profile` | 사용자 profile 조회 |
| User | `/api/users/update-profile` | 이름, 국가, profile image 등 profile 수정 |
| User | `/api/users/create-profile` | 기본 profile 생성 |
| Sound | `/api/sounds/upload` | 위치 기반 sound, image, file upload |
| Sound | `/api/sounds/uploads/{userId}` | 특정 사용자가 올린 sound 목록 조회 |
| Sound | `/api/sounds/explore` | 전체 sound를 위치 정보와 함께 조회 |
| Location | `/api/locations/allWithSounds` | 위치별 sound와 사용자 정보 조회 |
| Location | `/api/locations/get` | 위도/경도 기반 위치 정보 조회 |
| Location | `/api/locations/save` | 새 위치 정보 저장 |
| User Sound | `/api/user-sound/listen/{soundId}` | 특정 sound 청취 기록 추가 |

## 설계와 구현

- Email/password 기반 회원가입과 login/logout API를 구현했습니다.
- JWT 기반 인증과 사용자 삭제 흐름을 구현했습니다.
- 사용자 profile 조회, 생성, 수정 API를 구현했습니다.
- Google Maps API를 활용해 위도/경도 기반 위치 정보를 조회하고 저장했습니다.
- 위치 기반 sound/image/file upload API를 구현했습니다.
- 전체 sound explore, 사용자별 upload 목록, 위치별 sound 목록을 조회하는 API를 구현했습니다.
- 사용자의 sound 청취 기록을 저장하는 API를 구현했습니다.
- Frontend page별 API 호출 코드와 간단한 error handling을 추가했습니다.

## 결과

고객 요구사항에 맞춰 위치 기반 소리 업로드·조회 backend API와 frontend API 연동을 구현했고, 공개 가능한 납품 이력은 Kmong portfolio page로만 연결합니다.

## 공개 참고 링크

- [Kmong portfolio page](https://kmong.com/portfolio/view/154608)

## 기술

Java 17, Spring Boot, MySQL, Maven, Google Maps API, JWT, DB SSL, HTML, CSS, JavaScript, Vercel, Render, Aiven
