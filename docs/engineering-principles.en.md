# Engineering Principles

In product development, I document domain background, operational policies, responsibility boundaries, and verification criteria before implementation, then fix behavior through tests and review. In AI-assisted development, the goal is not code generation itself, but making the output verifiable under the same criteria.

## Core Principles

- As repetitive implementation becomes easier, problem definition and verification criteria matter more.
- Documentation is not a side artifact. It helps people learn context quickly and keeps judgment criteria stable.
- Clear context, test, and review criteria let humans and AI agents implement and review in the same direction.
- Time saved from repetitive implementation should go into domain understanding and code review.

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

## Harness

- Fix core business behavior and exception paths with tests.
- Keep regression-prone paths as sample inputs, reproduction steps, and verification commands.
- Treat data correctness, time handling, serialization, and API compatibility as explicit review points.
- Re-check whether the implementation satisfies the completion criteria.

## Review

- Check whether the change stays within the problem scope.
- Review responsibility boundaries, consistency, extensibility, cohesion, and coupling.
- Check compatibility with existing APIs, configuration, serialization, and user flows.
- Confirm whether tests cover real risk paths.
- Decide whether new complexity is justified by the problem.

## Domain Learning

In No-code platform work, I transformed design information into SQL, DDL, Java service code, data synchronization, and change history. In AI-assisted development, the same pattern matters: turn domain knowledge and requirements into context, tests, and review criteria.

## Anti-patterns

- Merging AI-generated code without tests
- Prompts without success criteria
- Implementation instructions without out-of-scope items
- Large changes without regression-risk explanation
- Emphasizing tool names instead of verification criteria
