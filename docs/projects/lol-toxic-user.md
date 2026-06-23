# LoL 악성 유저 검출

2020.02 - 2020.07

## 개요

Riot Games API와 OP.GG crawling으로 게임 로그를 수집하고, League of Legends 유저의 악성 행위를 점수화해 웹에서 조회할 수 있게 만든 졸업 프로젝트입니다.

구현은 web, API, crawling, log repository로 분리했고, 팀장으로 프로젝트 기획과 협업을 주도했습니다.

## 역할과 범위

- 팀장으로 프로젝트 기획과 일정 내 개발을 주도했습니다.
- Data 수집·저장, 악성도 계산 model, web result page 개발에 참여했습니다.
- Riot Games API, OP.GG crawling, MySQL 저장, Python model 생성, Node.js API, React web page를 연결했습니다.

## 문제와 제약

게임 내 악성 행위는 단일 지표로 직접 확인하기 어렵기 때문에, 공개적으로 확인 가능한 match data와 OP.GG-visible signal을 조합해 user-level toxicity score를 만들어야 했습니다.

수집 data와 scoring 기준은 실험 프로젝트 수준의 heuristic이므로, public page에서는 운영 서비스 수준의 검증 지표처럼 표현하지 않습니다.

## 설계와 구현

- Riot Games API와 OP.GG crawling으로 약 1만 명의 유저와 10만 건 이상의 game log를 수집했습니다.
- MySQL RDS에 수집한 game record를 저장했습니다.
- Python script와 scikit-learn으로 clustering 기반 악성도 계산 model을 만들었습니다.
- KMeans/Hierarchical Clustering을 활용해 game log feature를 분석했습니다.
- `.pkl` model을 load해 user query에 대한 troll score를 반환했습니다.
- React web page에서 summoner name 검색과 game별 욕설 점수 결과를 표시했습니다.
- 구현은 [web](https://github.com/Find-Troll/Trollgg), [API](https://github.com/Find-Troll/trollAPI), [crawling](https://github.com/Find-Troll/trollCrawling), [log](https://github.com/Find-Troll/trollLog) 저장소로 분리했습니다.

## 점수화 기준

악성도 점수화에는 OP.GG에서 확인 가능한 아래 signal을 사용했습니다.

- Tier
- Champion selection
- 비정상 item build
- 특정 champion 편중 win rate
- 낮은 KDA
- Game별 욕설 score

## 검증과 결과

- 수집 data, clustering, heuristic scoring을 결합해 악성 유저 판별 system을 구현했습니다.
- 수동 sample 검증에서 약 95% 수준의 일치율을 관찰했습니다.
- 이 수치는 public benchmark나 재현 가능한 평가 dataset이 아니라 프로젝트 문서 기준의 수동 검증 결과이므로, 운영 서비스 품질 지표처럼 사용하지 않습니다.
- 졸업 프로젝트 장려상을 수상했습니다.

## 공개 참고 링크

- [Find-Troll GitHub organization](https://github.com/Find-Troll)
- [Find-Troll/Trollgg](https://github.com/Find-Troll/Trollgg)
- [Find-Troll/trollAPI](https://github.com/Find-Troll/trollAPI)
- [Find-Troll/trollCrawling](https://github.com/Find-Troll/trollCrawling)
- [Find-Troll/trollLog](https://github.com/Find-Troll/trollLog)
- [프로젝트 설명 및 동작 영상](https://youtu.be/DISVpCMBNtE?si=qwhlT71f3LCkxklY)

## 기술

React, Node.js, Python, scikit-learn, KMeans, Hierarchical Clustering, MySQL, AWS EC2, AWS RDS, Riot Games API, OP.GG crawling
