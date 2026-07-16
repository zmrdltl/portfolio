# Coupler

- Contribution period: Jul 2024 - Present
- Type: Mobile dating app
- Classification: Independent project, initially outsourced maintenance

## Overview

I now lead development and operations across the React Native mobile app, API, admin web, and database. While moving the existing codebase to version 2.0.0, I implemented signup and review state transitions and reworked the database structure so the app, API, and admin web use the same review states.

## Role and Responsibilities

- Translate product decisions into the app, API, admin web, DB schema, and migrations.
- Own QA, code review, merges, releases, deployment, and rollback.
- Keep policy, flows, architecture, DB-change verification procedures, and deployment and rollback rules in the [public engineering documentation](https://coupler-developer.github.io/docs/) and tie them to release criteria.

## Problem

The previous signup application asked for about 30 fields at once, creating a large burden before the first review request. If the server response, app screens, and admin queue inferred review state independently, submission, resubmission, approval, and rejection behavior could diverge.

## Signup and Review Flow

```mermaid
flowchart LR
  submit["Submit basic information and required profile"] --> initial["Initial signup review"]
  initial -->|Approved| next["Open subsequent reviews"]
  initial -->|Returned| reapply["Edit and resubmit"]
  reapply --> initial
  next --> associate["Associate-member review"]
  next --> full["Full-member review"]
```

The initial application now focuses on basic information and the required profile. After initial signup-review approval, associate and full-member reviews can be submitted in parallel or completed by moving between tabs.

## App / API / Admin Responsibility Boundaries

```mermaid
flowchart LR
  docs["Engineering Docs\nPolicy / Flows / Architecture"]
  api["API\nResponse Contract / Access Rights"]
  app["React Native App\nScreen Routing / Tab Access"]
  admin["Admin Web\nReview Queue / Detail Actions"]
  db["MySQL\nState / Review Rows / Migration"]
  tests["Verification\nContract / Routing / Queue"]
  release["Release\nQA / Deploy / Rollback"]

  docs --> api
  api --> app
  api --> admin
  api --> db
  app --> tests
  admin --> tests
  api --> tests
  db --> tests
  tests --> release
```

The API response contract supplies routing and access rights. The app and admin web apply it to the user flow and review queue, while DB state, migrations, regression tests, and release checks are reviewed within the same change.

## Implementation and Validation

- The [signup response contract](https://coupler-developer.github.io/docs/policy/signup-response-contract/) separates successful API responses from screen-routing state so clients do not infer server state.
- The [member review policy](https://coupler-developer.github.io/docs/policy/member-review-policy/) defines submission and resubmission, separates signup from profile-edit reviews, and standardizes admin queue classification.
- I migrated the admin web from JavaScript to TypeScript and added CI checks for type errors and JavaScript reintroduction.
- API contract, mobile routing, and admin queue regression tests, together with the [code review policy](https://coupler-developer.github.io/docs/policy/code-review-policy/), are part of release checks.
- I used LLMs to support problem decomposition and implementation, while I remained directly responsible for requirements, product and technical judgment, code review, test criteria, merges, and release decisions.

## Observed Result

Meta SDK first signup review event: observed about 10 times before the redesign and about 100 times after.

## Related Links

- [Google Play](https://play.google.com/store/apps/details?id=com.ritzy.fourhundred&pli=1)
- [App Store](https://apps.apple.com/kr/app/id1645569179)
- [Engineering documentation](https://coupler-developer.github.io/docs/)

## Technologies

React Native, TypeScript, Express, MySQL
