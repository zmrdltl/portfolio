# Engineering Principles

In product development, I document domain background, operational policies, responsibility boundaries, and verification criteria before implementation, then fix behavior through tests and review. When using automation tools, the goal is not code generation itself, but moving customer and market signals into product changes quickly while keeping the output verifiable under the same criteria.

## Core Principles

- As repetitive implementation becomes easier, problem definition and verification criteria matter more.
- Documentation is not a side artifact. It helps people learn context quickly and keeps judgment criteria stable.
- Clear context, test, and review criteria let people implement and review in the same direction.
- Time saved from repetitive implementation should go into interpreting customer and market signals, domain understanding, and code review.

## Workflow

```text
Domain knowledge and requirements
-> background, operational policies, exception policies
-> context, out-of-scope items, completion criteria
-> implementation plan and test harness
-> implementation
-> review, regression checks, operational cleanup
```

## Context

- Feature background and user flow
- Operational policies and exception policies
- Code boundaries and responsibilities
- Success criteria and out-of-scope items
- Logs, tests, and reproduction steps for failures

Representative work: in [Coupler](projects/coupler.md), I documented signup response contracts and member review policies in public docs; in [ClumL](experience/cluml.md), I narrowed an operational wait symptom into a request-limiting concurrency problem.

## Harness

- Fix core business behavior and exception paths with tests.
- Keep regression-prone paths as sample inputs, reproduction steps, and verification commands.
- Treat data correctness, time handling, serialization, and API compatibility as explicit review points.
- Re-check whether the implementation satisfies the completion criteria.

Representative work: in [TmaxCloud](experience/tmaxcloud.md), I moved generated-service request/response and DB write/read checks into a pre-deployment validation flow; in [GlueSQL](opensource/gluesql.md), I left regression criteria from SQL translation through the test suite.

## Review

- Check whether the change stays within the problem scope.
- Review responsibility boundaries, consistency, extensibility, cohesion, and coupling.
- Check compatibility with existing APIs, configuration, serialization, and user flows.
- Confirm whether tests cover real risk paths.
- Decide whether new complexity is justified by the problem.

Representative work: in [ClumL](experience/cluml.md), I reviewed whether PR changes matched acceptance criteria and regression-test criteria; in [Coupler](projects/coupler.md), I checked state contracts, typechecks, migration guards, and policy-doc synchronization together.

## Domain Learning

In No-code platform work, I transformed design information into SQL, DDL, Java service code, DB verification, and change-history criteria. The same pattern matters when using automation tools: turn customer and market signals, domain knowledge, and requirements into context, tests, and review criteria.

## Anti-patterns

- Merging generated code without tests
- Prompts without success criteria
- Implementation instructions without out-of-scope items
- Large changes without regression-risk explanation
- Emphasizing tool names instead of verification criteria
