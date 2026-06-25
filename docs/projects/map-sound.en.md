# Map-based Sound Upload Site

2024.10 - 2024.11

## Overview

This was a client delivery project where I implemented location-based sound upload and lookup APIs using Java 17, Spring Boot, MySQL, and Google Maps API.

The service flow allowed authenticated users to upload sounds and images to specific locations, and allowed other users to browse and listen to sounds on a map.

## Role and scope

- Owned backend database design and API implementation across the project.
- Implemented part of the frontend API integration and state management.
- Because this was a client delivery project, the source repository is private. This page links only to a public delivery record.

## Problem and constraints

Location-based sound upload and lookup required user authentication, location storage, file upload, map-coordinate lookup, user profile handling, and listening history to work together.

The client, server, and database also ran on separate hosting environments, so HTTPS/API calls, DB SSL connection, and Google Maps API integration had to be coordinated reliably.

## Architecture and infra

- Frontend: Vercel
- Backend: Render
- Database: Aiven MySQL with SSL connection
- API: Google Maps API
- Backend stack: Java 17, Spring Boot 3+, Maven, MySQL
- Frontend stack: HTML, CSS, vanilla JavaScript

## API scope

| Domain | Endpoint | Purpose |
| --- | --- | --- |
| User | `/api/users/register` | Email/password sign-up |
| User | `/api/users/login` | Login and JWT token issuance |
| User | `/api/users/logout` | JWT-token-based logout |
| User | `/api/users/delete` | Account and user-data deletion |
| User | `/api/users/profile` | User profile lookup |
| User | `/api/users/update-profile` | Name, country, and profile image update |
| User | `/api/users/create-profile` | Default profile creation |
| Sound | `/api/sounds/upload` | Location-based sound, image, and file upload |
| Sound | `/api/sounds/uploads/{userId}` | Sound list uploaded by a specific user |
| Sound | `/api/sounds/explore` | All sounds with location information |
| Location | `/api/locations/allWithSounds` | Sounds and user information by location |
| Location | `/api/locations/get` | Location lookup by latitude/longitude |
| Location | `/api/locations/save` | New location storage |
| User Sound | `/api/user-sound/listen/{soundId}` | Listening-history record for a sound |

## Design and implementation

- Implemented email/password sign-up and login/logout APIs.
- Implemented JWT-based authentication and account deletion flow.
- Implemented user profile lookup, creation, and update APIs.
- Used Google Maps API to look up and store latitude/longitude-based location information.
- Implemented location-based sound/image/file upload APIs.
- Implemented all-sound explore, per-user upload list, and per-location sound list APIs.
- Implemented API support for recording user listening history.
- Added frontend API call code and simple error handling for relevant pages.

## Result

I implemented the backend APIs and frontend API integration for the location-based sound upload and lookup flow according to client requirements. The only public delivery reference linked here is the Kmong portfolio page.

## Public reference

- [Kmong portfolio page](https://kmong.com/portfolio/view/154608)

## Skills

Java 17, Spring Boot, MySQL, Maven, Google Maps API, JWT, DB SSL, HTML, CSS, JavaScript, Vercel, Render, Aiven
