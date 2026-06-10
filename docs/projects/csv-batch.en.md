# CSV Batch Pipeline

2024.11

## Overview

Implemented a batch pipeline that loads CSV files larger than 1GB into MySQL using Spring Batch, OpenCSV, MySQL, Prometheus, and Grafana.

## Implementation

- Implemented Reader, Processor, and Writer layers.
- Configured Skip/Retry handling.
- Configured parallel Step, Partitioner, and TaskExecutor processing.
- Added H2 and MySQL tests.
- Used Prometheus and Grafana for monitoring.

## Result

Reduced 1GB data insertion time from approximately 25 minutes to under 5 minutes.

## Skills

Java, Spring Batch, OpenCSV, MySQL, H2, Prometheus, Grafana
