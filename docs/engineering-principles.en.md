---
portfolio_role: appendix
---

# Engineering Principles

I define the problem and completion criteria before optimizing implementation speed, then keep code, documentation, tests, and review aligned to those criteria. I use AI tools for problem decomposition and implementation support while retaining direct responsibility for requirements, technical decisions, code review, test criteria, and release decisions.

## Core Principles

### 1. Separate Symptoms from Causes and Set the Scope of the Fix

I do not assume that a slow or failing path has one cause. As in the [ClumL request-limiting fix](experience/cluml.md), which separated a concurrency race from fixed-window waiting, I isolate causes before deciding what to change and what to leave unchanged.

### 2. Make Completion Criteria Testable

A successful API response alone is not enough. I check response shapes, database writes and reads, screen routing, and error handling. The [TmaxCloud pre-deployment API check](experience/tmaxcloud.md), [GlueSQL regression tests](opensource/gluesql.md), and [Coupler release checks](projects/coupler.md) apply this principle.

### 3. Capture Existing Behavior before Replacing an Implementation

Before replacing a library or internal implementation, I record current behavior in tests. In the [Chrono-to-Jiff migration](experience/cluml.md), I captured timestamp behavior before separating the implementation change from dependency cleanup, then checked affected screens and server compatibility.
