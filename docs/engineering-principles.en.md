# Engineering Principles

I define the problem and completion criteria before optimizing implementation speed, then keep code, documentation, tests, and review aligned to those criteria.

## Core Principles

### 1. Define the Problem and Boundaries First

I examine why a feature is needed, the user flow, and operational policy before separating the problem from non-goals. Clear success criteria and ownership boundaries keep implementation and review focused on the same outcome, with problem definition before tool selection.

### 2. Make Completion Verifiable

I fix core behavior and exceptional paths in tests, then check high-risk areas such as API contracts, data shapes, and compatibility separately. Incorrect changes should surface in automated checks or a documented reproduction path.

### 3. Review and Deliver the Whole Change

I review documentation, state contracts, migrations, user flows, deployment, and rollback criteria along with the code diff. I release only after checking that any new complexity is necessary for the problem.

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
| Problem and boundaries | [ClumL](experience/cluml.md) |
| Verifiable completion | [TmaxCloud](experience/tmaxcloud.md), [GlueSQL](opensource/gluesql.md) |
| Review and delivery | [Coupler](projects/coupler.md) |
