# Coupler

2024.07 - Present

## Overview

Coupler is a personal product development project spanning a React Native app, API, admin web, and public docs.
From 1.0.0 operation through the 2.0.0 transition, I clarified TypeScript migration criteria, signup/review flow criteria, and development/review criteria.

## Role and Scope

- Development lead / Software Engineer
- Defined development and release criteria across the mobile app, API, admin web, and public docs.

## Problem and Constraints

While moving the React Native product from its 1.0.0 initial implementation through the 2.0.0 transition, I needed the mobile app, API, and admin web to follow the same state model and release criteria.

## Design and Implementation

- Set maintainability criteria by migrating the admin web to TypeScript and adding typecheck CI/migration guards.
- Unified screen branching by separating signup and review flows around use cases and the [server response contract](https://github.com/coupler-developer/docs/blob/main/content/policy/signup-response-contract.md).
- Aligned submission/resubmission UX and review-list criteria so Admin/Mobile/API use the same [member review policy](https://github.com/coupler-developer/docs/blob/main/content/policy/member-review-policy.md).
- Recorded testing, documentation-sync, and regression-safety criteria in the [code review policy](https://github.com/coupler-developer/docs/blob/main/content/policy/code-review-policy.md).

## Validation and Criteria

- Established the admin web TypeScript migration criteria through typecheck CI and migration guards.
- Reduced client-side guesswork and duplicate review-queue risk through the signup response contract and member review policy.

## Result

Within the 2.0.0 transition scope, I clarified development criteria across the mobile app, API, and admin web, and captured the signup response contract, member review policy, and code review criteria in public docs.

## Skills

React Native, TypeScript, Express, MySQL
