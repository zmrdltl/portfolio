# TmaxCloud

- Period: Oct 2021 - Nov 2024

## Pre-Deployment API Testing for a Code-Generation Platform

I designed and built a test screen that could call generated APIs and check the data they wrote to the real database before formal deployment.

**Problem and diagnosis:** A customer raised a concern that building and deploying a business application took about four weeks. To find where the time went, I built an app myself on the platform. It generated Java APIs and SQL from entities and services defined in the UI, then packaged them in a JAR. Checking whether service definitions and request and response formats worked required building the JAR, configuring a formal deployment, and starting a container. Each cycle took about 20 minutes, and every correction meant repeating it.

**Constraints and decision:** Mock responses could not show whether the generated code wrote to and read from the actual database correctly. The existing temporary deployment feature could run the generated JAR against that database. I chose to call APIs in that environment from a test screen so users could verify real behavior without repeating the formal deployment cycle.

**Implementation:** I built a React test screen that let users select a service, automatically filled in sample values based on each request field’s type, and let users edit the JSON in Monaco Editor. I implemented WebSocket request and response handling and designed and built the Java REST API and database schema for storing and retrieving actual test data.

<figure class="portfolio-diagram" aria-label="TmaxCloud pre-deployment API test UI concept" markdown="block">

<div class="portfolio-diagram-flow" markdown="block">

1. Select a generated API in the temporary deployment environment.
2. Prepare a JSON request and call the API over WebSocket.
3. Check the API response and the actual database writes and reads.

</div>

![Conceptual pre-deployment API test UI with service selection, JSON request editing, API responses, and database checks.](../assets/diagrams/tmaxcloud-predeploy-api-test.en.svg)

<figcaption class="portfolio-diagram-link" markdown="span">[Open full-size diagram](../assets/diagrams/tmaxcloud-predeploy-api-test.en.svg){ aria-label="Open full-size diagram (TmaxCloud pre-deployment API test UI concept)" }</figcaption>

</figure>

**Validation and result:** I called generated APIs in the temporary deployment environment and checked response formats and actual database writes and reads. Users could find invalid service definitions, missing service mappings, and request and response format errors before formal deployment.

**Post-change feedback:** I separately asked internal users how long it took to build and deploy an app after the changes. The median reported time from the start of entity definition to JAR deployment was about two weeks.

## Storing Data-Change History and Querying Historical Data

I implemented generated history writes for Create, Update, and Delete services, plus SQL to query row values and the last editor for a requested date.

<figure class="portfolio-diagram" aria-label="TmaxCloud data-change history and past-date query example" markdown="block">

<div class="portfolio-diagram-flow" markdown="block">

1. The current table stores the latest value `C`. The history stores prior values and their editors.
2. A query for January 10 selects the row that was valid on that date.
3. It returns the historical value `B` and the last editor while preserving the current value `C`.

</div>

![Conceptual data example combining the current table and change history to query row values and the last editor for a requested past date.](../assets/diagrams/tmaxcloud-table-history.en.svg)

<figcaption class="portfolio-diagram-link" markdown="span">[Open full-size diagram](../assets/diagrams/tmaxcloud-table-history.en.svg){ aria-label="Open full-size diagram (TmaxCloud data-change history and past-date query example)" }</figcaption>

</figure>

**Problem and diagnosis:** Generated CRUD applications kept only current values. To look up a row’s value and last editor as of a past date, I needed to record the previous value, the time of the change, and who made it.

**Constraints and decision:** Tibero triggers or procedures needed an extra convention to receive the requesting user's identity. I instead generated history writes in CRUD code that already had that identity, using the same entity columns and primary key for storage and queries.

**Implementation:** I implemented FreeMarker templates that generate source and history table DDL, plus SQL to store history for rows affected by Create, Update, and Delete services. The history includes pre-update and pre-delete values, change timestamps, editor IDs, and deletion state. I wrote SQL that uses change timestamps to combine current and historical data and return the valid row and its last editor for each primary key as of a requested date.

**Illustrative example:** On January 8, editor B changed the row to value B. The value changed to C on January 15. A January 10 lookup returns B and the editor who set it, while the current row still holds C.

**Follow-up verification:** In a reproduction of the generated Update service, concurrent requests repeatedly targeted a small set of rows. The history showed a continuous chain of before-and-after values and consecutive revision numbers. The last recorded value for each row matched its current value. When a failure was injected before commit, the row update and its history entry rolled back together.

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
