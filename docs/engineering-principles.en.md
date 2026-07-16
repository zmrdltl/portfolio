# Engineering Principles

I define the problem and completion criteria before optimizing implementation speed, then keep code, documentation, tests, and review aligned to those criteria.

I use AI tools for problem decomposition and implementation support while retaining direct responsibility for requirements, technical decisions, code review, test criteria, and release decisions.

## Core Principles

### 1. Separate Symptoms from Causes and Set the Scope of the Fix

I do not assume that a slow or failing path has one cause. I inspect concurrency races, maximum waits imposed by fixed windows, API responses, and database changes separately, then state what I will fix and what I will leave unchanged.

### 2. Make Completion Criteria Testable

A successful API response alone is not enough. I test response shapes, database writes and reads, screen routing, and error handling so regressions surface before deployment.

### 3. Verify Existing Behavior before Replacing a Dependency

Before replacing a library or internal implementation, I record existing behavior in tests. After switching to the new implementation, I remove the old dependency and temporary comparison code, then check affected screens, documentation, and deployment steps.

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
| Separating symptoms from causes and setting the scope of the fix | [ClumL](experience/cluml.md) |
| Testable completion criteria | [TmaxCloud](experience/tmaxcloud.md), [GlueSQL](opensource/gluesql.md), [Coupler](projects/coupler.md) |
| Replacing dependencies without changing behavior | [ClumL](experience/cluml.md) |
