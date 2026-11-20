# TmaxCloud

- Period: Oct 2021 - Nov 2024

## Pre-Deployment API Testing for a Code-Generation Platform

I designed and built a test screen that could call generated APIs and check the data they wrote to the real database before formal deployment.

**Problem and diagnosis:** The team routinely told customers to allow about four weeks to build and deploy a business app, based on similar projects. I questioned whether the full four weeks were necessary. To find where the time went and which steps we could shorten, I built an app myself on the platform, following the same steps as a customer administrator.

The platform generated Java APIs and SQL from entities and services defined in the UI and packaged them in a JAR. While building the app, I found that checking a service definition or its request and response formats required building the JAR, configuring a formal deployment, and starting a container. Each cycle took about 20 minutes. When I found an error, I had to fix the definition and repeat the cycle.

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

I implemented SQL to record changes and the ID of the user who called the write API. I also wrote SQL to look up each row’s value on a given date and the API caller who requested its most recent change as of that date.

<figure class="portfolio-diagram" aria-label="TmaxCloud data-change history and past-date query example" markdown="block">

<div class="portfolio-diagram-flow" markdown="block">

1. The current table stores the latest value `C`. The history records previous values and API caller IDs.
2. A query for January 10 selects the row that was valid on that date.
3. The query returns the historical value `B` and the API caller who requested the last change. The current value remains `C`.

</div>

![Example of querying a past row value and the API caller who requested its last change using the current table and the change history.](../assets/diagrams/tmaxcloud-table-history.en.svg?v=2)

<figcaption class="portfolio-diagram-link" markdown="span">[Open full-size diagram](../assets/diagrams/tmaxcloud-table-history.en.svg?v=2){ aria-label="Open full-size diagram (TmaxCloud data-change history and past-date query example)" }</figcaption>

</figure>

**Problem and diagnosis:** Generated CRUD applications kept only current values. Looking up a row’s past value and who requested its last change required recording the previous value, change timestamp, and API caller ID.

**Constraints and decision:** Tibero triggers or procedures would need a convention for passing the API caller ID from the request to the database. The generated Create, Update, and Delete API code already had that ID, so I put the history writes in that code and used the same entity columns and primary key for storage and queries.

**Implementation:** I wrote FreeMarker templates for source and history table DDL and for the SQL that records changes when a Create, Update, or Delete API runs. The history records pre-update and pre-delete row values, change timestamps, the user ID from the API request, and deletion status. My query combines current and historical data using those timestamps. For each primary key, it returns the row as of the given date and the API caller who requested its latest change by then.

**Illustrative example:** On January 8, user B called the update API to set the row’s value to B. The value changed to C on January 15. A January 10 lookup returns value B and user B, who requested the last change as of that date. The current row still holds C.

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
