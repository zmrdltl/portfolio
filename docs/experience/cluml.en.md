# ClumL

- Period: Mar 2025 - Jul 2026

## Fixing a Request-Limiting Concurrency Bug in an AI Security Analysis Engine

**Problem and diagnosis:** I analyzed requests that remained pending for an extended time on a customer demo server and isolated a check-and-reserve race in which concurrent requests read the same pre-reservation state and exceeded the configured limit. I treated the maximum wait imposed by the fixed window as a separate cause.

```mermaid
flowchart LR
  ui["Security Analysis UI"]
  api["Security Analysis API"]
  limiter["Request Limiter"]
  capacity["Reservation/Capacity State"]
  worker["Analysis Job Execution"]

  ui --> api
  api --> limiter
  limiter --> capacity
  limiter --> worker
```

```mermaid
sequenceDiagram
  participant A as Request A
  participant B as Request B
  participant L as Request Limiter
  participant S as Reservation/Capacity State

  A->>L: Check capacity
  L->>S: Read pre-reservation state
  S-->>L: Capacity available
  B->>L: Check capacity
  L->>S: Read the same state
  S-->>L: Capacity available
  A->>L: Request reservation
  L->>S: Record reservation
  B->>L: Request reservation
  L->>S: Record reservation
  Note over L,S: Requests reading the same state can exceed the limit
```

**Constraints and decision:** The capacity check and reservation update had to be atomic against one current state, but holding the lock while waiting would block other requests. I kept only the check and reservation in the same lock section and released the lock before waiting.

**Implementation:** I changed the request-limiting logic to decide and immediately reserve against one shared state.

**Validation and result:** Before the fix, I reproduced over-reservation that allowed at least ten times as many requests as configured through the limiter. After the fix, regression tests confirmed that the limiter allowed no more requests than configured under the same concurrency load.

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

**Implementation and validation:** I migrated those timestamp helpers to Jiff and removed their Chrono dependency. I compared stage-level tests, affected screens, feature behavior, server compatibility, and before-and-after screenshots.

### Report Query Scope and DHCP Option Display Validation

I separated the report's first-event-time query from customer-list loading, then reviewed a lightweight, report-specific query and incremental rendering for the customer list. For DHCP options, I compared the GraphQL API's `options` field, formatting logic, raw event, detection list, and detail view to confirm that the API change reached the rendered output.
