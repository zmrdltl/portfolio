# ClumL

- Period: Mar 2025 - Jul 2026

## Fixing a Concurrency Bug in Outbound LLM API Rate Limiting

**Problem and diagnosis:** While investigating long waits on a customer demo server, I found a race in the AI Security Analysis Engine’s outbound LLM API limiter: concurrent calls could read the same pre-reservation state and push both in-flight calls and pending token reservations past their limits. I distinguished it from waiting at fixed-window boundaries and limited the fix to the over-reservation race.

**Constraints and decision:** The in-flight call count and estimated token reservation had to be checked against one current state, but holding the lock while waiting would block other calls. I kept only the check and reservation in the same lock section and released the lock before waiting.

Scroll horizontally to inspect the full flow.
{ .diagram-scroll-hint }

![A request moves from the security analysis UI through the API and analysis job to the rate limiter, which checks reservation and capacity state before calling the external LLM API.](../assets/diagrams/cluml-rate-limit-components.en.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="ClumL outbound LLM API rate-limiting component diagram" }

**Failure flow before the fix:** Capacity checks and reservation updates ran in separate lock sections, allowing concurrent calls to read the same pre-reservation state.

Scroll horizontally to inspect the full flow.
{ .diagram-scroll-hint }

![Concurrent calls A and B read the same pre-reservation state, both pass the capacity check, and then record reservations that can exceed the limit.](../assets/diagrams/cluml-rate-limit-race.en.svg)
{ .editorial-diagram-scroll role="group" tabindex="0" aria-label="ClumL pre-fix rate-limiter race sequence diagram" }

**Implementation:** I changed the outbound LLM API rate limiter to check one shared state and immediately reserve an in-flight slot and estimated tokens.

**Validation and result:** Before the fix, I reproduced over-reservation in which the in-flight call count and pending token reservations each reached at least ten times their respective limits. After the fix, regression tests confirmed that both values stayed within their respective limits under the same concurrency load.

## Moving a Network-Event Detection Threshold to External Configuration

**Problem and diagnosis:** Even a small threshold adjustment required a code change and a new binary deployment. The recurring cost came from fixing the value adjusted during pcap replay in code, rather than from the detection logic itself.

**Constraints and decision:** The recurring adjustment applied to the occurrence-count threshold. I kept the detection model intact and moved that value outside the code boundary into external configuration.

**Implementation:** I changed the Rust service to read the threshold from external configuration.

- Before: edit code → build → replace binary → restart service → replay pcap and check the database
- After: edit configuration → restart service → replay pcap and check the database

**Validation and result:** I compared the workflow before and after the change using the same pcap replay and DB event check. For one recurring setting change, removing the code edit, build, and binary replacement reduced the operational change time before pcap replay and the database check by at least 30%.

## Additional Work

### Migrating Time Handling from Chrono to Jiff

**Problem and diagnosis:** A successful compile did not prove that timestamp conversion and visible UI output remained unchanged after the dependency migration.

**Constraints and decision:** I first captured the existing Chrono behavior in tests for the timestamp helpers used by the MITRE and clustering views, then separated the Jiff migration from old-dependency cleanup.

**Implementation and validation:** I migrated those timestamp helpers to Jiff and removed the Chrono development dependency and migration-only comparison tests. I completed the migration for those helpers after staged tests, feature and server compatibility checks, and before-and-after comparisons of the affected screens.

### Implementing Report Queries and DHCP Option Views

I implemented dedicated queries for the report’s first-event time and customer list that fetch only the fields needed on screen, and updated the customer list to render incrementally. For DHCP options, I implemented the path from the GraphQL query through formatting to the list and detail views, then verified both displays against the raw event.
