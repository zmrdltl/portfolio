# LoL Toxic User Detection

2020.04 - 2020.07

## Overview

Developed a web service that collects game logs through the Riot Games API and scores toxic behavior by user.

## Role and Scope

- Led project planning and collaboration as team lead.
- Participated in data collection, toxicity scoring, and web result screen implementation.

## Problem and Constraints

The service needed to score toxic behavior by user based on game logs collected from the Riot Games API and make the result available on the web.

## Design and Implementation

- Collected data for approximately 10,000 users and more than 100,000 game logs using Python.
- Stored collected data in MySQL RDS.
- Displayed toxicity scores by game in real time on the [web page](https://github.com/Find-Troll/Trollgg).
- Stored per-user game data for toxicity scoring.
- Split implementation across [web](https://github.com/Find-Troll/Trollgg), [API](https://github.com/Find-Troll/trollAPI), [crawling](https://github.com/Find-Troll/trollCrawling), and [log](https://github.com/Find-Troll/trollLog) repositories.

## Validation and Result

- Built a toxicity scoring heuristic using OP.GG-visible signals such as tier, champion selection, abnormal item builds, one-champion win-rate skew, and low KDA, and observed about 95% agreement in manual sample validation.
- Received an encouragement award for the graduation project.

## Public Reference

- [Find-Troll GitHub organization](https://github.com/Find-Troll)

## Skills

React, Node.js, Python, MySQL, Riot Games API
