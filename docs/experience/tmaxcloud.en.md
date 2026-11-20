# TmaxCloud

- Period: Oct 2021 - Nov 2024

## Pre-Deployment API Testing for a Code-Generation Platform

I designed and built a test screen that could call generated APIs and check the data they wrote to the real database before formal deployment.

**Problem and diagnosis:** A customer raised a concern that building and deploying a business application took about four weeks. To find where the time went, I built an app myself on the platform. It generated Java APIs and SQL from entities and services defined in the UI, then packaged them in a JAR. Checking whether service definitions and request and response formats worked required building the JAR, configuring a formal deployment, and starting a container. Each cycle took about 20 minutes, and every correction meant repeating it.

**Constraints and decision:** Mock responses could not show whether the generated code wrote to and read from the actual database correctly. The existing temporary deployment feature could run the generated JAR against that database. I chose to call APIs in that environment from a test screen so users could verify real behavior without repeating the formal deployment cycle.

**Implementation:** I built a React test screen that let users select a service, automatically filled in sample values based on each request field’s type, and let users edit the JSON in Monaco Editor. I implemented WebSocket request and response handling and designed and built the Java REST API and database schema for storing and retrieving actual test data.

Scroll horizontally to inspect the full diagram.
{ .diagram-scroll-hint }

![Conceptual pre-deployment API test UI with service selection, JSON request editing, API responses, and database checks.](../assets/diagrams/tmaxcloud-predeploy-api-test.en.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="TmaxCloud pre-deployment API test UI concept" }

**Validation and result:** I called generated APIs in the temporary deployment environment and checked response formats and actual database writes and reads. Users could find invalid service definitions, missing service mappings, and request and response format errors before formal deployment.

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

Platform UI users can export an entity, import it into another application, and use the imported entity in service definitions. The feature copies data for selected attributes, then synchronizes subsequent changes from connected services through a message broker.

I implemented the export UI so users could select multiple entities at once. I designed selected-attribute metadata and broker-mediated linkage between exported and imported entities, using the existing CQRS middleware. The design stores selected-attribute lists alongside entity information and gives each entity its own publish/subscribe connections. I contributed to the DB schema and APIs for storing exported and imported entity information.

The work spanned the UI, APIs, code generation, and application deployment. When the initial schedule was set at two weeks, I showed the deployment and development screens side by side to explain the progress and why the work would not fit that time frame. The schedule was adjusted to four weeks.

### SQL Generator Logic and Tests

I directly implemented SQL Generator logic that produces DDL from JSON input. I participated in the work to make SQL generation a library imported directly by the backend. I wrote JUnit tests for JSON-input SQL generation and added JaCoCo coverage configuration so the generation logic could be verified independently.

### Standardizing Exception Log Output

I standardized exception log output for messages, error codes, SQL states, and stack traces, and visually distinguished error logs from general terminal output.
