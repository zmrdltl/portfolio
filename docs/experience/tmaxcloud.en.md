# TmaxCloud

- Role: Software Engineer
- Period: 2021.10 - 2024.11

## Overview

I implemented backend/platform features in a Java/TypeScript-based No-code platform, connecting metadata, entity, and service design information to DDL, SQL, Java service code, data synchronization, change history, and test tooling.

The scope included metadata modeling, SQL generation, Java service code generation, entity synchronization, change history, UI/test tooling, and Kubernetes/Redis research.

## Metadata-driven Generation Flow

### Problem

The platform needed a consistent metadata model and generation flow so service design information could become DDL, SQL, Java service code, deployment artifacts, and test flows.

### Role

- Defined service in/out DTOs, context, and node service structures.
- Implemented Freemarker-template-based Java service code generation for Select, Insert, Update, and Delete services.
- Improved the SQL Generator into a library used directly by the backend.
- Implemented JSON-input-based SQL generation for CREATE, ALTER, VIEW, JOIN, conditional expressions, and DML statements, with JUnit tests.

## Data Flow and Change History

- Implemented entity export/import features between applications.
- Designed topic/subscriber-based data copy and synchronization flows.
- Implemented change history table generation, snapshot storage before CRUD operations, and SQL for restoring table state at a specific point in time.

## Tibero and Data Features

- Implemented NoSQL-like CRUD features on Tibero RDBMS using JSON types, JSON Path Expression, and JSON Schema validation.
- Designed metadata-level column encryption settings and DBMS_CRYPTO-based encryption/decryption SQL and CRUD service generation logic.

## Test and Operational Tooling

- Implemented React Flow-based entity relationship visualization.
- Implemented a Material UI-based metadata change history page with filtering, sorting, grouping, and highlighting.
- Implemented a WebSocket-based service test page.
- Centralized service ID mapping, message handler mapping, response handling, and log/error handling to reduce duplicated work and debugging cost when adding services.

## Kubernetes and Redis Research

- Verified Terraform remote execution through Kubernetes API Exec and client-go.
- Built a team development/test Kubernetes cluster with 1 master node and 3 worker nodes.
- Researched Redis deployment, TLS, monitoring, and external access redirect behavior using Redis Operator and Redis Cluster Proxy.
- Verified an average 5-minute saving in Terraform/k8s provisioning, a Redis packet delivery success rate above 95%, and a 30% reduction in issue detection time.
- Had 3 related upstream Redis Operator PRs merged during validation: [#265](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/265), [#308](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/308), [#313](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/313).

## Skills

Java, TypeScript, React, Material UI, React Flow, WebSocket, Freemarker, Tibero, SQL generation, JUnit, Kubernetes, Terraform, Redis Operator, Redis Cluster Proxy
