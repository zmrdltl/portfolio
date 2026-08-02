# Coupler

- Contribution period: Jul 2024 - Present
- Type: Mobile dating app
- Classification: Independent project, started as contracted maintenance

## Role and Responsibilities

I now lead development and operations across the React Native mobile app, Express API, React admin web, and MySQL database.

- Translate product decisions into the app, API, admin web, database schema, and migrations.
- Own QA, code review, merges, releases, deployment, and rollback.
- Keep policy, flows, architecture, database-change verification procedures, and deployment and rollback rules in the [public engineering documentation](https://coupler-developer.github.io/docs/) and tie them to release criteria.

## Using One Server Response for Signup and Review State

**Problem and diagnosis:** The previous signup application asked for about 30 fields at once, creating a large burden before the first review request. The larger consistency risk was that app screens, API result codes, and the admin review queue could independently infer submission, resubmission, approval, rejection, and the next screen, producing different flows.

**Constraints and decision:** The change had to span the existing React Native app, Express API, React admin web, MySQL data, and migrations. Instead of matching client-specific conditionals, I made the API the single source that returns access state and the next action, while the app and admin web interpret only valid server states. Missing or invalid state does not open a screen by inference.

```mermaid
stateDiagram-v2
  state "Submit basic information and required profile" as Submitted
  state "Initial signup review" as InitialReview
  state "Edit and resubmit" as Reapply
  state "Open subsequent reviews" as ReviewOpen
  state "Associate-member review" as AssociateReview
  state "Full-member review" as FullReview

  [*] --> Submitted
  Submitted --> InitialReview: Request review
  InitialReview --> Reapply: Returned
  Reapply --> InitialReview: Resubmit
  InitialReview --> ReviewOpen: Approved
  ReviewOpen --> AssociateReview: Submit
  ReviewOpen --> FullReview: Submit
```

**Implementation:** While moving the existing codebase to version 2.0.0, I reduced the initial application to basic information and the required profile, implemented state transitions that allow associate- and full-member reviews to proceed independently after approval, and reworked the database structure. The [signup response contract](https://coupler-developer.github.io/docs/policy/signup-response-contract/) separates successful responses from screen-routing state, while the [member review policy](https://coupler-developer.github.io/docs/policy/member-review-policy/) aligns submission and resubmission, signup versus settings-change reviews, and admin queue classification.

**Validation and result:** I kept API response-contract, mobile-routing, and admin review-queue regression tests in the same release checklist. Changes go through the [code review policy](https://coupler-developer.github.io/docs/policy/code-review-policy/), QA, and deployment and rollback procedures.

Observed Meta SDK event count upon reaching the initial signup review stage: about 10 before the redesign and about 100 after.

This value counts events recorded when the initial signup review stage was reached.

## Connecting N-to-N Group Meetings as One Operational Lifecycle

**Problem and diagnosis:** A group meeting involving several members and an operator is more than a scheduling screen. Recruitment, application, operator approval, confirmed participation, chat access, completion, and review eligibility change at different times. If each screen and API inferred those states independently, a canceled application could reappear, chat could open before confirmation, or writing could remain available after the meeting ended.

**Constraints and decision:** I had to add the feature within the existing app, API, admin web, and database while aligning operator management of events and participants with member application, reapplication, leaving, chat, and reviews. I separated the event and application lifecycles under server-owned state, initialized group chat only when the event was confirmed for the first time, and derived chat availability and completion from server time.

```mermaid
flowchart TB
  subgraph event["Event lifecycle"]
    draft["DRAFT"]
    open["OPEN"]
    confirmed["CONFIRMED<br/>Initialize chat on first entry"]
    finished["FINISHED<br/>Event start + 24 hours"]
    canceled["CANCELED"]
    deleted["DELETED"]
    draft -->|Publish| open
    open <-->|Confirm / reopen| confirmed
    open --> canceled
    confirmed --> canceled
    draft --> deleted
    open -->|Active event with initialized chat| finished
    confirmed -->|Event start + 24 hours| finished
  end

  subgraph application["Application lifecycle"]
    applied["APPLIED"]
    approved["APPROVED"]
    appCanceled["CANCELED"]
    left["LEFT"]
    applied -->|Approve participation| approved
    approved -->|Operator cancellation| appCanceled
    approved -->|Participant leaves| left
    appCanceled -->|Reapply| applied
  end

  finished ~~~ applied
```

**Implementation:** I implemented meeting, application, participant, chat, and review state in the API and database, then connected admin workflows for creation, publication, approval and cancellation, participants, reviews, and reports. A teammate built parts of the initial mobile list, detail, and chat UI; I connected application state, real-time message merging, read state, notification markers, reapplication, reporting, and reviews to that collaborative mobile flow. Group messages are persisted through REST and received as server-confirmed events over WebSocket.

**Validation and result:** Event publication, confirmation, reopening, and completion, along with application, approval, leaving, reapplication, and review transitions, are release criteria together with API, admin-web, and mobile regressions. Chat opens at 1:00 p.m. on the calendar day before the currently scheduled event start and becomes read-only 24 hours after that start time. I documented the lifecycle in the [group meeting system documentation](https://coupler-developer.github.io/docs/architecture/group-meeting-system/) and released it in the v2.3.0 scope.

## Additional Work

### Three Real-Time Chat Surfaces and One-to-One Gap Recovery

I connected real-time messages and unread-count updates across curator chat, one-to-one matching chat, and N-to-N group chat. All three keep the database and HTTP reads as the durable source while WebSocket distributes confirmed state to connected clients. The idempotent retry and cursor-recovery design below applies specifically to one-to-one matching chat.

**Problem and diagnosis:** On mobile networks, a response can be lost after a message is persisted, an HTTP response can overlap with the sender's WebSocket event, and peer messages can be missed while the connection is down. Treating every retry as a new command would duplicate messages and notifications, while trusting WebSocket delivery alone could leave the screen inconsistent with the database.

**Constraints and decision:** I made message sending an HTTP command that persists to the database first and assigned WebSocket the separate responsibility of distributing server-confirmed real-time state. A client-generated `client_message_id` is stored as a sender-scoped unique key for safe retries, while the database-assigned message ID is the ordering, cursor, and deduplication key.

```mermaid
flowchart TB
  send["Sender App<br/>HTTP POST + client_message_id"]
  api["Express API<br/>HTTP command / cursor query"]
  canonical["MySQL<br/>Message with confirmed database ID"]
  response["Canonical HTTP response"]
  page["before_id cursor page"]
  realtime["WebSocket<br/>Self / peer event"]
  merge["Mobile App<br/>Merge by database ID"]
  recovery["Reconnect<br/>Recover from the latest page"]
  peer["Peer App"]

  send -->|Idempotent persistence| api --> canonical
  canonical --> response --> merge
  canonical --> realtime
  recovery --> api
  canonical --> page --> merge
  realtime --> merge
  realtime --> peer
```

**Implementation and validation:** When the same sender retries the same payload with the same `client_message_id`, the API returns the original message without publishing another WebSocket event or notification. Reusing the key with a different payload is rejected as a conflict. The mobile app merges the HTTP response and sender/peer WebSocket events by the database message ID. After reconnect or screen focus, it walks backward from the latest HTTP page with a `before_id` cursor until it reaches the previous synchronization boundary, merging any missing messages. Regression tests cover persistence, duplicate requests, payload conflicts, cursor pages, and mobile reconnect merging.

**Scaling consideration:** WebSocket fan-out currently uses the connection set of a single API process. To prepare for an event broker and an outbox when moving to multiple instances, the screen-recovery source remains the HTTP API and database.

### An Interruptible Database Migration Runner and Recovery Criteria

**Problem and decision:** An operational database change must prevent several unsafe states together: schema changes without a migration record, partially applied steps, and an older API continuing to write against the new schema. I fixed the target migrations and order in an immutable plan with checksums, then required writer and external-effect fencing, drain, backup, and preconditions before mutation.

**Implementation and validation:** I implemented an interruptible runner that records each migration, its postcondition, and a durable ledger. If interrupted, it keeps the fence in place and resumes or recovers only after confirming the same plan. In development, I confirmed that the related schema change had been applied and its postcondition had succeeded, but the postcheck ledger record was missing; the runner repaired only that ledger gap. The v2.3.0 production migrations predated this runner, so I did not retroactively claim that the new runner executed them; instead, I closed that state by revalidating the live catalog, ledger gaps, postconditions, and schema fingerprint. These rules are maintained in the [database migration policy](https://coupler-developer.github.io/docs/policy/db-migration-gate-policy/).

### Migrating the Admin Web to TypeScript and Preventing JavaScript Reintroduction in CI

**Problem and diagnosis:** Because the admin screens, stores, and locale resources were written in JavaScript and JSX, expected value shapes and response contracts were not visible in types. Loose casts, missing locale keys, and runtime rendering errors therefore had to be addressed together during the migration.

**Constraints and decision:** I migrated the existing admin application incrementally to TypeScript and TSX, then made `allowJs: false` and type checking ongoing constraints rather than treating file conversion as a one-time task.

**Implementation and validation:** I converted the admin web's JavaScript and JSX code to TypeScript and TSX. GitHub Actions CI runs type checks and fails the migration guard if JavaScript or JSX returns under `src` or loose double casts are reintroduced.

## Related Links

- [Google Play](https://play.google.com/store/apps/details?id=com.ritzy.fourhundred&pli=1)
- [App Store](https://apps.apple.com/kr/app/id1645569179)
- [Engineering documentation](https://coupler-developer.github.io/docs/)
