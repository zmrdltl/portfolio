# TmaxCloud

- Period: Oct 2021 - Nov 2024

## Pre-Deployment API Testing for a Code-Generation Platform

**Problem and diagnosis:** Users defined entities and service logic in the UI, and the platform generated Java APIs, SQL, and a JAR. The generated APIs could only be checked against real responses and database writes and reads after a separate deployment and container startup. With roughly 200–300 services and APIs to verify, one build, deploy, and verification cycle took about 20 minutes, and each invalid definition or request/response shape restarted the same delayed feedback loop.

**Constraints and decision:** Verification had to cover real JSON requests, responses, and database state rather than mocks. I placed those checks in a React, TypeScript, and WebSocket test UI that runs before deployment.

```mermaid
flowchart TD
  definition["UI Definition\nApp / Entity / Service"]
  artifacts["Generated Artifacts\nJava / SQL / DDL"]
  tester["Pre-Deployment Test UI\nJSON Editing / WebSocket Call"]
  validation["Result Check\nAPI Response / DB Write and Read"]

  definition --> artifacts
  artifacts --> tester
  tester --> validation
```

**Implementation:** I built a React and TypeScript test UI where users selected a service, edited its JSON request in Monaco Editor, and called the generated API. The UI sent calls over WebSocket, while a supporting Java REST API and database schema connected the response to real database writes and reads.

**Validation and result:** I found invalid request/response shapes and missing definition-to-code links without a separate deployment, while still checking actual database writes and reads. Each such check no longer required repeating the roughly 20-minute build, deployment, and verification cycle.

## Data-Change History and Historical Table Reconstruction

**Problem and diagnosis:** Generated CRUD applications kept only current values. Showing earlier values and the last editor after an update or deletion required storing the prior row, editor, and valid period under one consistent definition.

**Constraints and decision:** A Tibero database trigger or procedure could see the changed row but did not naturally receive the requesting user's identity. I chose to generate the history write in CRUD code, which already carried that identity, and made the history-table DDL and point-in-time read use the same entity columns and primary key.

```mermaid
flowchart TD
  entity["Entity Definition\nColumns / Primary Key / History Enabled"]
  ddl["DDL Generation\nSource + History Tables"]
  crud["CRUD Code Generation\nStore Row Before Update/Delete"]
  history["History\nPrimary Key / Editor / Valid Period / Row Data"]
  restore["Requested-Date Reconstruction\nRow Value / Last Editor"]

  entity --> ddl
  entity --> crud
  ddl --> history
  crud --> history
  history --> restore
```

**Implementation:** I encoded the source/history-table DDL and the SQL that stores a row before an update or deletion in FreeMarker templates. I also wrote a query that combines current and historical data to reconstruct each row as of a requested date and return its last editor.

**Result:** The CRUD code produced by the platform stores the prior row, editor, and deletion state in the history table. Given a date, the query selects the row version valid on that date and returns the historical table state and last editor.

## Additional Work

### Entity Export/Import and Selected-Attribute Synchronization

Studio users can export an entity, import it into another generated application, and use the imported entity in service definitions. At import time, the feature copies data for selected attributes; when a connected service later changes data, it synchronizes changes to those attributes through a message broker.

I contributed to the DB schema and API for storing exported and imported entity information. I designed selected-attribute metadata and broker-mediated linkage between exported and imported entities. I implemented the export UI. The message-synchronization service and the redeployment migration strategy for later schema changes were separate areas of work.

### SQL Generation Library

I helped separate SQL generation into a library imported directly by the backend. I wrote JUnit tests for JSON-input SQL generation and added JaCoCo coverage configuration so the generation logic could be verified independently.

### Standardizing Exception Log Output

I standardized exception log output for messages, error codes, SQL states, and stack traces, and visually distinguished error logs from general terminal output.
