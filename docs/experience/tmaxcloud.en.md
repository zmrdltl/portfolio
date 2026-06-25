# TmaxCloud

- Role: Software Engineer
- Period: 2021.10 - 2024.11

## Overview

I implemented backend/platform features in a Java/TypeScript-based No-code platform, connecting metadata and service design information to DDL, SQL, Java service code, data synchronization, change history, and test tooling.

The work falls into four separate tracks: No-code service generation platform, team test Kubernetes environment, Terraform/k8s external provisioning research, and Redis on Kubernetes research. I keep these tracks separate here because the No-code platform work and the Kubernetes/Redis/Terraform research solved different problems.

## No-code service generation platform

### Problem and constraints

For users to design and deploy applications without writing code directly, metadata, entities, service definitions, and deployment artifacts had to be connected through the same model.

The design information needed to flow into table/entity definitions, service in/out DTOs, context, validation, SQL/DDL, Java service code, and test request formats. Missing mappings or duplicated registration points could turn into debugging cost before and after deployment.

```text
Metadata -> Business Entity -> Service Definition -> Generated Java Service
Entity/Table Definition -> SQL Generator -> DDL/DML
Generated Java Code + SQL -> Application Artifact -> Deployment/Test Flow
```

### Role and scope

- Defined service in/out DTOs, context, and node service structures.
- Implemented entity-to-DTO/context mapping, search/delete/update conditions, and node-service-based Java service code generation flows.
- Implemented Freemarker-template-based Java service generation for Select, Insert, Update, and Delete services.
- Implemented JSON-input-based SQL Generator logic and JUnit tests.
- Implemented React/TypeScript UI and WebSocket-based service test/request-response tooling.

## Code generation

To convert service definitions into Java service code, I organized the inDTO, outDTO, context, node service, SQL type mapping, and template input structures.

- Supported multiple node/block services inside one service flow.
- Mapped entity attributes to inDTO, outDTO, and context values, and passed Update/Delete results into later node inputs.
- Simplified repeated ResultSet SQL-type-to-Java-type mapping through Freemarker macros.
- Designed service flows where each node service could map to a different entity when updating multiple tables.
- Generated request JSON schema from service in/out DTO definitions so test requests and validation criteria could share the same shape.

This was not simple CRUD implementation. It was a generation flow where design-time metadata became executable service code and request/response contracts.

## Representative Generated Service Structure

Internal class and package names are not published; the generated service structure is represented with generic names only.

- `ClientRequest` -> `ServiceDispatcher` -> `GeneratedService`
- `GeneratedService` -> `RequestDTO`/`Context` -> validation -> SQL/CRUD execution
- SQL/CRUD result -> response mapper -> `ClientResponse`

## SQL Generator

I implemented a SQL Generator that accepted JSON requests based on designed entities and generated DDL/DML SQL before application deployment.

- DDL: `CREATE TABLE`, `ALTER TABLE`, `CREATE VIEW`
- DML/query: `SELECT`, `INSERT`, `INSERT ALL`, `UPDATE`, `DELETE`, `EXISTS`
- SQL expression: `CASE`, `AND`, `OR`, `WITH`, `JOIN`, view column mapping
- Key/sequence: primary key, sequence
- Test: verified SQL generated from JSON input with JUnit and configured coverage checks.

Previously, SQL generation requests had to pass through multiple layers and were not available as a library directly imported by the backend. I changed the SQL Generator into a backend-importable library structure, reduced duplicated work, and recorded more than 30% performance optimization in project records from that period.

## Entity export/import

I implemented an export/import MVP for copying and synchronizing entity data between applications through a topic/subscriber model.

- The Export App defined the entities to export and registered topics.
- When an exported entity changed, a publish service emitted messages.
- The Import App stored import metadata and generated DDL and sync services during deployment.
- The Import App subscribed to topics and synchronized data changes.
- DML and metadata schema supported copying only selected attributes.

The implementation required synchronization metadata such as `created_by`, `created_at`, `modified_by`, `modified_at`, and selected attribute lists. Instead of increasing schema complexity with additional tables for selected attributes, I represented the selection data through an array-like field after considering performance and complexity.

Some constraints remained. Redeployment could create PK conflicts with already copied data, and message queue handling during copy or before sync-service subscription was not fully completed within the time limit. This public portfolio includes those boundaries rather than presenting the MVP as a complete synchronization product.

## Change history and table restore

I implemented a flow that generated entity-level change-history tables, stored previous records before CRUD operations, and restored table state for a specific point in time.

- Generated change-history table DDL when entities were created.
- Stored a snapshot of the record matching the PK before Insert/Update/Delete operations.
- Compared before/after states using `UP_TO`, `LAST_MODIFIED_BY`, `DATA_SNAPSHOT`, and a deletion flag.
- Queried the original table and history table together so records no longer present in the current table could still be candidates for restore.
- Used `ROW_NUMBER() OVER (PARTITION BY PK ORDER BY ...)`-style selection to choose snapshots before and after a target time.

This was a data integrity feature for explaining and restoring point-in-time data state of metadata-generated application tables, not just an audit log.

## Tibero JSON and column encryption

I implemented NoSQL-like CRUD features on Tibero RDBMS using JSON types.

- Automatically generated collection/document table DDL.
- Queried and updated complex JSON objects, arrays, and primitive values through JSON Path Expression.
- Provided MongoDB `find`-like APIs and projection to fetch only needed fields.
- Reduced request-data format errors and integrity issues through JSON Schema validation.

I also implemented CRUD service generation logic for metadata-level column encryption. Encrypted columns were encrypted during query binding and decrypted in responses.

- Generated DBMS_CRYPTO-based encryption/decryption SQL.
- Converted different metadata types into string representations to support one encryption/decryption flow.
- Reviewed a structure where keys were not stored directly in the database but managed by a separate server, with key rotation considered.

This public page does not include actual keys, internal function/package/class names, or operational log formats.

## Product UI and service tooling

I implemented React/TypeScript UI and WebSocket tooling for validating and operating metadata and generated services in the No-code platform.

### Entity diagram

I visualized entities and reference relationships with React Flow.

- Displayed selected entities and reference relationships hierarchically.
- Placed parent and child entities in inheritance structures.
- Traversed referenced and referencing entities recursively.
- Supported nodes/edges, zoom, filtering, fit view, automatic layout, and view modes.
- Provided regex search and highlighting.
- Handled parallel connections and self-reference paths separately in custom edges.

Using a proven visualization library reduced the complexity of manually calculating node/edge position and connection state, and improved UI state management and maintainability.

### Metadata history

I implemented a Material UI-based metadata change history page.

- Displayed modified time, metadata name, change type, and before/after values in a table.
- Provided keyword-based filtering and highlighting.
- Supported grouping by modified time and sorting within each group.
- Managed independent sorting state per column.
- Implemented conditional cell highlighting and click/sort interactions.

The page made it easier to find needed items in large change history tables. Independent state management also solved the issue where one column's previous sort state affected another column.

### Request/response flow

I redesigned the WebSocket-based request/response flow.

- Centralized service ID and handler mapping.
- Built reverse mapping between backend service paths and client service IDs.
- Registered message handlers automatically by service group.
- Replaced hard-coded service name strings with service map keys in request senders.
- Used match patterns to catch missing service ID and handler mappings at compile time.
- Standardized server response handling regardless of success or error responses.

Previously, adding a new service required registering the same information in service ID mappers, handler registries, and feature handlers. If one registration was missed, a response could fail to reach the handler. The redesign reduced duplicated registration, reduced service integration time by more than 10% in project records from that period, and replaced debugging sessions that could take at least 30 minutes with compile-time checks.

### Service test page and logger

I implemented a WebSocket-based service test page.

- Reduced invalid connection attempts through WebSocket URL regex validation.
- Fetched service lists after successful connection and displayed them through an Accordion UI.
- Generated JSON request templates per service.
- Let users edit JSON requests in Monaco Editor and send them to real services.
- Supported end-to-end checks of DDL design and generated service behavior through a test deployment mode.

I also organized repeated DAO/service logging through an invocation handler and error logger structure. Project records from that period indicate more than 30% reduction in manual log-writing time, and the error logging flow made SQL error metadata easier to distinguish from ordinary logs.

## Team test Kubernetes environment

I built a 1 master / 3 worker Kubernetes cluster for team development and testing.

- Configured CRI-O runtime and MetalLB load balancing on a CentOS-based cluster.
- The initial kubenet-based setup had average packet loss of 3-5% between worker nodes.
- A compatible network plugin and MetalLB configuration reduced packet loss to below 1%.
- Node downtime decreased from about 5-6 times per month to once or less per month, improving cluster availability.

## Terraform/k8s external provisioning research

I verified whether Terraform commands could be executed remotely from outside a Kubernetes cluster to create and manage EC2 instances.

- Used Kubernetes API Exec and `client-go` to run `terraform init` and `terraform apply` inside a pod.
- Studied the flow for passing commands from outside Kubernetes into a pod and the related gRPC communication pattern.
- The Terraform/k8s provisioning validation recorded an average 5-minute reduction in repeated execution time.

Public learning records:

- [gRPC learning record](https://codecollector.tistory.com/1533)
- [Terraform/k8s experiment record](https://codecollector.tistory.com/1555)

## Redis on Kubernetes research

I researched how to deploy Redis reliably in Kubernetes and reduce redirect issues when external clients connected to a Redis Cluster.

- Used Redis Operator to test standalone/cluster deployment, TLS configuration, and log management.
- Adjusted Redis Operator manifests and custom variables for cluster integration.
- Connected Redis Insight and Prometheus to visualize Redis command execution status and metrics.
- Used Redis Cluster Proxy to resolve external-client redirect issues.
- Compared proxy modules including Predixy, TwemProxy, and Corvus.
- Had 3 related upstream Redis Operator PRs merged during validation: [#265](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/265), [#308](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/308), [#313](https://github.com/OT-CONTAINER-KIT/redis-operator/pull/313).

The validation confirmed a Redis packet delivery success rate above 95% with Redis Operator and proxy-module combinations, and a 30% reduction in issue detection time through Redis Insight and Prometheus-based monitoring.

## Skills

Java, TypeScript, React, Material UI, React Flow, WebSocket, Freemarker, Tibero, SQL generation, JUnit, Kubernetes, CRI-O, MetalLB, Terraform, client-go, Redis Operator, Redis Cluster Proxy, Prometheus
