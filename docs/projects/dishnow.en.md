# Dishnow

2019.02 - 2019.12

## Overview

Dishnow was a real-time restaurant reservation mobile app with separate customer and store-owner apps. A user sent a reservation request to nearby restaurants, the store-owner app accepted the request, and the user finalized the reservation.

Using React Native, React, Node.js, MySQL, and AWS, I worked on customer/store-owner apps, authentication, reservation state, push notifications, reviews, and a point system.

## Role and scope

- Worked with a team of 3 developers, 4 planners, and 1 designer.
- Participated in early development and feature expansion for both the customer app and store-owner app.
- Participated in app feature design, MySQL database design, API integration, and reservation-state flow implementation.
- Worked on shared social login, JWT authentication, push notifications, reviews, and a point system.

## Problem and constraints

The customer app's restaurant search/reservation flow and the store-owner app's reservation management flow needed to operate on the same reservation state.

Reservation request, store-owner acceptance, user confirmation, SMS delivery, and review writing all had to map to state changes on the same reservation record. Missing push notifications could directly affect reservation success.

## Design and implementation

I used the reservation DB table as the source for reservation lists and status, and implemented separate customer and store-owner apps.

- Implemented customer app features for nearby restaurant search, reservation requests, final confirmation, review writing, and account management.
- Implemented store-owner app features for managing store information and reservation requests.
- When the user app sent reservation information, the server stored it and sent a reservation-request push to the host app through OneSignal.
- When the host app accepted a reservation, the server updated reservation state and sent an acceptance push to the user app.
- When the user finalized a reservation, the server updated the state and sent a confirmation SMS through Aligo.
- Stored review and rating information after a completed reservation.
- Migrated from ID/password handling to JWT-token-based authentication and session management.
- Used AsyncStorage to keep authentication state after app termination.
- Applied React/redux-based state management.

## Validation and metrics

The following results come from project records from that period. The public links are representative code/reference links, not direct support for store release, download count, or reservation-success metrics.

- Released the apps on Google Play and the App Store.
- Recorded 100+ app downloads.
- Compared reservation status data before and after push notification rollout and confirmed a 35% reservation-success improvement.
- Had startup-program awards and preliminary startup package support history.

## Remaining constraint

JWT token refresh logic was not fully completed. Since this was an early startup project, this portfolio uses it as a supporting signal for product flow, mobile/backend collaboration, and reservation-state management experience.

## Public reference

- [Dishnow GitHub organization](https://github.com/dishnoww)
- [DishnowUser repository](https://github.com/HongikDevelopers/DishnowUser)
- [Dishnow promotional video](https://youtu.be/4_j_0OXUodw?si=eulwjSBBXG1UrEKg)

## Skills

React Native, React, Node.js, Java 8, MySQL, AWS RDS, EC2, S3, JWT, OneSignal Push, Aligo SMS, Kakao, Naver, Facebook, Google Maps API
