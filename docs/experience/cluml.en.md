# ClumL

- Role: Software Engineer
- Period: 2025.03 - Present

## Overview

I work on change-safety criteria in a security event analysis product suite. The core of my current role is not to describe the whole system, but to narrow operational symptoms into concrete technical problems and close them with verifiable criteria.

The representative work here is request-limiting concurrency and detection/report display consistency. Rust service compatibility checks, requirements/completion criteria, and PR review support those changes by keeping them inside the agreed problem scope and compatible with existing behavior.

## Representative Work

### Aimer RateLimiter Over-Limit Request Admission

I reframed a long-wait symptom observed during customer demo server operation as a check-and-reserve race in request limiting, not as a generic latency problem.

#### Problem Context

```mermaid
flowchart LR
  ui["Analysis UI"]
  api["Aimer API"]
  limiter["RateLimiter"]
  bucket["Reservation / Capacity State"]
  worker["Aimer Work Execution"]

  ui --> api
  api --> limiter
  limiter --> bucket
  limiter --> worker
```

#### Failure Flow

```mermaid
sequenceDiagram
  participant A as Request A
  participant B as Request B
  participant L as RateLimiter
  participant S as Reservation / Capacity State

  A->>L: Check capacity
  L->>S: Read pre-reservation state
  S-->>L: Can pass
  B->>L: Check capacity
  L->>S: Read the same pre-reservation state
  S-->>L: Can pass
  A->>S: Record reservation
  B->>S: Record reservation
  Note over L,S: Multiple requests passing from the same state can admit over-limit requests
```

What I did:

- Separated the long-wait symptom into a check-and-reserve race in `RateLimiter`.
- Defined the validation criterion that capacity checks and reservation updates must operate against the same state.
- Reviewed whether the PR change matched the acceptance criteria and regression-test criteria.

Validation/result:

- Captured the condition where requests could pass more than 10x beyond the allowed limit as a reproducible correctness problem.
- Framed the result as a correctness criterion that prevents over-limit request admission, not as a latency-metric claim.

### Detection Screen and Report Display Consistency

If detection lists, detail screens, charts, and reports show the same security event through different criteria, analyst trust can break. This work is not a list of screen fixes; it is about checking whether event context stays consistent through the display path.

```mermaid
flowchart LR
  event["Security Event"]
  list["Detection List"]
  detail["Detail Screen"]
  chart["Chart"]
  report["Report"]
  context["Shared Event Context"]

  event --> list
  event --> detail
  event --> chart
  event --> report
  list --> context
  detail --> context
  chart --> context
  report --> context
```

What I did:

- Separated causes and change scope for detection list/detail views, time ranges, port/packet display, and chart/report behavior.
- Reviewed whether analysis screens and reports stayed aligned to the same event context, rather than checking only screen-level fixes.
- Included API/query contracts and display-rule drift in review criteria.

Validation/result:

- Organized detection/report display issues around whether the same event context was preserved.
- Connected those checks to change-safety criteria so product changes would not weaken trust in analysis results and report outputs.

## Supporting Work Criteria

```mermaid
flowchart LR
  issue["Problem Definition"]
  scope["Scope / Non-goals"]
  criteria["Completion Criteria"]
  tests["Test Criteria"]
  review["PR Review"]
  safety["Change-Safety Check"]

  issue --> scope
  scope --> criteria
  criteria --> tests
  tests --> review
  review --> safety
```

- Reviewed configuration, date/time handling, serialization, and test boundaries in Rust services to check compatibility risk against existing behavior.
- Clarified the problem, scope, non-goals, completion criteria, and test expectations before implementation so implementation and review used the same criteria.
- Reviewed PR scope, API/protocol compatibility, test coverage, lint/clippy results, and change-safety risk so changes did not drift beyond the agreed problem scope.

## Skills

Rust, GraphQL, Yew, TypeScript, PostgreSQL, RocksDB
