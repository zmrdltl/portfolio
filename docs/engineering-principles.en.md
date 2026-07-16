# Engineering Principles

I define the problem and completion criteria before optimizing implementation speed, then keep code, documentation, tests, and review aligned to those criteria.

I use AI tools for problem decomposition and implementation support while retaining direct responsibility for requirements, technical decisions, code review, test criteria, and release decisions.

## Core Principles

### 1. Separate Symptoms into Failure Modes and Ownership Boundaries

I do not reduce a slow or failing path to one assumed cause. I separate concurrency races, fixed-window waits, API contracts, and database changes into distinct failure modes, then define direct ownership and non-goals before implementation.

### 2. Turn Completion Criteria into Executable Contracts

A successful response is not enough. I lock down API response shapes, database writes and reads, state transitions, and exceptional paths with tests and reproduction procedures so incorrect changes surface before deployment.

### 3. Split Migrations into Baseline, Transition, and Cleanup

I first capture existing behavior in baseline tests, transition to the new implementation, and then remove old dependencies and temporary comparison code. I review documentation, state contracts, migrations, user flows, deployment, and rollback criteria as part of the same change.

## Workflow

```text
Understand the domain and requirements
-> Define the problem, non-goals, and completion criteria
-> Write an implementation and verification plan
-> Implement in small units
-> Test, review, and synchronize documentation
-> Release and check for regressions
```

## Principles and Related Work

| Principle | Work Examples |
| --- | --- |
| Failure modes and ownership boundaries | [ClumL](experience/cluml.md) |
| Executable completion contracts | [TmaxCloud](experience/tmaxcloud.md), [GlueSQL](opensource/gluesql.md), [Coupler](projects/coupler.md) |
| Baseline-driven migrations | [ClumL](experience/cluml.md) |
