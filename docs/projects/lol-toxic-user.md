# LoL 악성 유저 검출

2020.04 - 2020.07

## 개요

Riot Games API를 활용해 게임 로그를 수집하고, 유저의 악성 행위를 점수화하는 웹 서비스를 개발했습니다.

## 역할과 범위

- 팀장으로 프로젝트 기획과 협업을 주도했습니다.
- 데이터 수집, 악성도 계산, 웹 결과 화면 구현에 참여했습니다.

## 문제와 제약

Riot Games API에서 수집한 게임 로그를 기반으로 유저별 악성 행위를 점수화하고 웹에서 확인할 수 있어야 했습니다.

## 설계와 구현

- Python으로 약 1만 명의 유저와 10만 건 이상의 게임 로그를 수집했습니다.
- MySQL RDS에 수집 데이터를 저장했습니다.
- [웹페이지](https://github.com/Find-Troll/Trollgg)에서 게임별 욕설 점수를 실시간으로 표시했습니다.
- 유저별 게임 데이터를 저장해 악성도 계산에 사용했습니다.
- 구현은 [web](https://github.com/Find-Troll/Trollgg), [API](https://github.com/Find-Troll/trollAPI), [crawling](https://github.com/Find-Troll/trollCrawling), [log](https://github.com/Find-Troll/trollLog) 저장소로 분리했습니다.

## 검증과 결과

- OP.GG에서 확인 가능한 티어, 챔피언 선택, 비정상 아이템 구매, 특정 챔피언 편중 승률, 낮은 KDA 등을 기준으로 악성도 점수화 기준을 만들고, 수동 샘플 검증에서 약 95% 수준의 일치율을 확인했습니다.
- 졸업 프로젝트 장려상을 수상했습니다.

## 공개 참고 링크

- [Find-Troll GitHub organization](https://github.com/Find-Troll)

## 기술

React, Node.js, Python, MySQL, Riot Games API
