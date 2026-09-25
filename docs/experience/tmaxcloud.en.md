# TmaxCloud

- Period: Oct 2021 - Nov 2024

## Pre-Deployment API Testing for a Code-Generation Platform

I designed and built a feature for calling generated APIs before deployment and checking their responses and actual database writes and reads. I implemented the React test UI, Java REST API, and database schema.

Scroll horizontally to inspect the full diagram.
{ .diagram-scroll-hint }

![Conceptual pre-deployment API test UI with service selection, JSON request editing, API responses, and database checks.](../assets/diagrams/tmaxcloud-predeploy-api-test.en.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="TmaxCloud pre-deployment API test UI concept" }

**Problem and diagnosis:** The platform generated Java APIs, SQL, and a JAR from UI-defined entities and services, but real API behavior could only be checked after deployment and container startup. With roughly 200-300 services and APIs to verify, each build, deployment, and verification cycle took about 20 minutes, delaying feedback on invalid definitions and request/response shapes.

**Constraints and decision:** Mock responses could not reveal actual database write/read errors, so I placed a test step before deployment that called APIs through the existing generation and execution path.

**Implementation:** I implemented JSON request editing with Monaco Editor in a React UI, plus WebSocket request/response handling. I also designed and implemented the Java REST API and database schema for listing test targets and storing and reading actual test data.

**Validation and result:** The test flow made generated API responses and actual database writes and reads checkable before deployment. It also made service-definition, mapping, and request/response problems visible before the separate build and deployment cycle.

## Storing Data-Change History and Querying Historical Data

I implemented generated history writes for Create, Update, and Delete services, plus SQL to query row values and the last editor for a requested date.

Scroll horizontally to inspect the full diagram.
{ .diagram-scroll-hint }

![Conceptual data example combining the current table and change history to query row values and the last editor for a requested past date.](../assets/diagrams/tmaxcloud-table-history.en.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="TmaxCloud data-change history and past-date query example" }

**Problem and diagnosis:** Generated CRUD applications kept only current values. Showing values and the last editor from before an update or deletion required saving the prior row, editor, and valid period together.

**Constraints and decision:** Tibero triggers or procedures needed an extra convention to receive the requesting user's identity. I instead generated history writes in CRUD code that already had that identity, using the same entity columns and primary key for storage and queries.

**Implementation:** I implemented FreeMarker templates that generate source/history-table DDL and SQL to store history data for the affected rows when generated Create, Update, and Delete services run. The generated history writes include pre-update and pre-delete values, editor IDs, and deletion state. I also wrote SQL that combines current and historical data to return the valid row for each primary key and its last editor as of a requested date.

**Illustrative example:** The diagram shows a row changing from A to B to C; a January 10 lookup selects historical value B and last editor B while the current source value remains C.

## Additional Work

### Service Code Generation

For Java service-code generation, I wrote the template-input logic and FreeMarker templates for Update and Delete services. I also implemented mapping that passes results into the next step, a shared macro that maps SQL result types to Java types, and the structure that maps different entities to individual steps in multi-table updates.

### Entity Export/Import and Selected-Attribute Synchronization

Platform UI users can export an entity, import it into another generated application, and use the imported entity in service definitions. At import time, the feature copies data for selected attributes; when a connected service later changes data, it synchronizes changes to those attributes through a message broker.

I handled most of this MVP; I did not implement the import-cancellation detail list page or the message-synchronization service, and I did not own the later redeployment migration strategy. I designed selected-attribute metadata and broker-mediated linkage between exported and imported entities. I implemented the export UI. I contributed to the DB schema and API for storing exported and imported entity information.

### SQL Generator Logic and Tests

I directly implemented SQL Generator logic that produces DDL from JSON input. I participated in the work to make SQL generation a library imported directly by the backend. I wrote JUnit tests for JSON-input SQL generation and added JaCoCo coverage configuration so the generation logic could be verified independently.

### Standardizing Exception Log Output

I standardized exception log output for messages, error codes, SQL states, and stack traces, and visually distinguished error logs from general terminal output.
