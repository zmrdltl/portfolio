# TmaxCloud

- Period: Oct 2021 - Nov 2024

## Pre-Deployment API Testing for a Code-Generation Platform

**Problem and diagnosis:** Users defined entities and service logic in the UI, and the platform generated Java APIs, SQL, and a JAR. The generated APIs could only be checked against real responses and database writes and reads after a separate deployment and container startup. With roughly 200–300 services and APIs to verify, one build, deploy, and verification cycle took about 20 minutes, and each invalid definition or request/response shape restarted the same delayed feedback loop.

**Constraints and decision:** Verification had to cover real JSON requests, responses, and database state rather than mocks. I placed those checks in a React, TypeScript, and WebSocket test UI that runs before deployment.

Scroll horizontally to inspect the full flow.
{ .diagram-scroll-hint }

![App, entity, and service definitions generate Java, SQL, and DDL artifacts, which the pre-deployment test UI exercises with JSON and WebSocket calls before checking API responses and database writes and reads.](../assets/diagrams/tmaxcloud-predeploy-api-test.en.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="TmaxCloud generated-API pre-deployment test flow diagram" }

**Implementation:** I built a React and TypeScript test UI where users selected a service, edited its JSON request in Monaco Editor, and called the generated API. The UI sent calls over WebSocket, while a supporting Java REST API and database schema connected the response to real database writes and reads.

**Validation and result:** I found invalid request/response shapes and missing definition-to-code links without a separate deployment, while still checking actual database writes and reads. Each such check no longer required repeating the roughly 20-minute build, deployment, and verification cycle.

## Data-Change History and Historical Table Reconstruction

**Problem and diagnosis:** Generated CRUD applications kept only current values. Showing earlier values and the last editor after an update or deletion required storing the prior row, editor, and valid period under one consistent definition.

**Constraints and decision:** A Tibero database trigger or procedure could see the changed row but did not naturally receive the requesting user's identity. I chose to generate the history write in CRUD code, which already carried that identity, and made the history-table DDL and point-in-time read use the same entity columns and primary key.

Scroll horizontally to inspect the full flow.
{ .diagram-scroll-hint }

![One entity definition drives source and history table DDL plus CRUD history writes, and the resulting history reconstructs row values and the last editor for a requested date.](../assets/diagrams/tmaxcloud-table-history.en.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="TmaxCloud data-change history and requested-date reconstruction diagram" }

**Implementation:** I encoded the source/history-table DDL and the SQL that stores a row before an update or deletion in FreeMarker templates. I also wrote a query that combines current and historical data to reconstruct each row as of a requested date and return its last editor.

**Validation and result:** Using example data, I confirmed that the history table captured values before updates and deletions together with the editor and deletion state. I also confirmed that, for a requested date, the query selected the valid history row for each primary key and returned the table state and last editor as of that date.

## Additional Work

### Entity Export/Import and Selected-Attribute Synchronization

Studio users can export an entity, import it into another generated application, and use the imported entity in service definitions. At import time, the feature copies data for selected attributes; when a connected service later changes data, it synchronizes changes to those attributes through a message broker.

I contributed to the DB schema and API for storing exported and imported entity information. I designed selected-attribute metadata and broker-mediated linkage between exported and imported entities. I implemented the export UI. The message-synchronization service and the redeployment migration strategy for later schema changes were separate areas of work.

### SQL Generation Library

I helped separate SQL generation into a library imported directly by the backend. I wrote JUnit tests for JSON-input SQL generation and added JaCoCo coverage configuration so the generation logic could be verified independently.

### Standardizing Exception Log Output

I standardized exception log output for messages, error codes, SQL states, and stack traces, and visually distinguished error logs from general terminal output.
