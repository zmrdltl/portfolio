# ClumL

- Period: Mar 2025 - Jul 2026

## Fixing a Concurrency Bug in Outbound LLM API Rate Limiting

**Problem and diagnosis:** When analysis jobs waited a long time on a customer demo server, I examined the logs and the Rust rate limiter. The limiter released its lock between checking capacity and recording a reservation. Concurrent calls could therefore see the same available capacity and all pass the check. Once the in-flight call count and pending token reservations exceeded their limits, subsequent calls calculated their waits against inflated reservations. I treated calls that stayed asleep across a fixed-window boundary as a separate problem with a different cause.

**Constraints and decision:** I put the capacity check and reservation under one lock so another call could not reserve between those steps. Holding the lock while waiting would also block calls that needed to check capacity, so the limiter releases it before waiting.

<figure class="portfolio-diagram" aria-label="ClumL outbound LLM API rate-limiting component diagram" markdown="block">

<div class="portfolio-diagram-flow" markdown="block">

1. A request from the security analysis UI reaches the analysis job through the API.
2. The limiter checks in-flight calls and pending token reservations.
3. When capacity is available, it reserves capacity and calls the external LLM API.

</div>

![A request moves from the security analysis UI through the API and analysis job to the rate limiter, which checks reservation and capacity state before calling the external LLM API.](../assets/diagrams/cluml-rate-limit-components.en.svg)

<figcaption class="portfolio-diagram-link" markdown="span">[Open full-size diagram](../assets/diagrams/cluml-rate-limit-components.en.svg){ aria-label="Open full-size diagram (ClumL outbound LLM API rate-limiting component diagram)" }</figcaption>

</figure>

**Failure flow before the fix:** Both calls counted the same available capacity toward their own reservations.

<figure class="portfolio-diagram" aria-label="ClumL pre-fix rate-limiter race sequence diagram" markdown="block">

<div class="portfolio-diagram-flow" markdown="block">

1. Concurrent calls A and B read the same state before either reserves capacity.
2. Both see available capacity and pass the check.
3. Both then record reservations, which can push calls and pending tokens past their limits.

</div>

![Concurrent calls A and B read the same pre-reservation state, both pass the capacity check, and then record reservations that can exceed the limit.](../assets/diagrams/cluml-rate-limit-race.en.svg)

<figcaption class="portfolio-diagram-link" markdown="span">[Open full-size diagram](../assets/diagrams/cluml-rate-limit-race.en.svg){ aria-label="Open full-size diagram (ClumL pre-fix rate-limiter race sequence diagram)" }</figcaption>

</figure>

**Implementation:** I updated the limiter to reserve an in-flight slot and the estimated tokens immediately after confirming capacity, under the same lock.

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
