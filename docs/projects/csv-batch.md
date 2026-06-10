# 1GB 이상 CSV 데이터 처리

2024.11

## 개요

Spring Batch, OpenCSV, MySQL, Prometheus/Grafana를 활용해 1GB 이상 CSV 데이터를 MySQL에 적재하는 batch pipeline을 구현했습니다.

## 구현

- Reader/Processor/Writer 계층을 구현했습니다.
- Skip/Retry 처리를 구성했습니다.
- 병렬 Step, Partitioner, TaskExecutor 처리를 구성했습니다.
- H2/MySQL 테스트를 작성했습니다.
- Prometheus와 Grafana로 모니터링을 구성했습니다.

## 결과

1GB 데이터 삽입 시간을 평균 25분에서 5분 이내로 단축했습니다.

## 기술

Java, Spring Batch, OpenCSV, MySQL, H2, Prometheus, Grafana
