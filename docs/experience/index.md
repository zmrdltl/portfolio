# 경력

## 경력 타임라인

| 기간 | 조직 | 역할 | 주요 내용 |
| --- | --- | --- | --- |
| 2025.03 - 2026.07 | ClumL | Software Engineer | 요청 제한 동시성 수정, Rust 서비스 설정 외부화, 회귀 테스트 |
| 2021.10 - 2024.11 | 티맥스클라우드 | Software Engineer | Java/TypeScript No-code 플랫폼, 서비스 코드 생성 검증, 데이터 변경 이력 저장·조회, entity export/import, SQL/DDL generation |

## 주요 성과

- [ClumL](cluml.md): 요청 제한 로직의 용량 확인과 예약 갱신을 같은 잠금 구간으로 묶어 허용치 대비 10배 이상 초과 요청이 통과하던 경합을 수정하고, 반복 조정하던 탐지 판정값은 외부 설정으로 분리해 설정 변경 1회 작업 시간을 30% 이상 줄였습니다.
- [티맥스클라우드 서비스 코드 생성 검증](tmaxcloud.md): UI의 엔티티·필드로 정의한 서비스를 생성 코드로 실행하고 API 응답과 DB 쓰기·읽기를 배포 전 E2E 검증 단계에서 확인해, 당시 반복되던 설계-검증 cycle을 약 4주에서 2주 수준으로 줄이는 데 기여했습니다.
- [티맥스클라우드 데이터 변경 이력](tmaxcloud.md): 원본·변경 이력 table과 insert/update/delete 서비스 코드의 변경 전 row data 저장 흐름을 구현하고, select SQL로 특정 시점 table 상태를 재구성하는 기준을 정리했습니다.
