# LoL Toxic User Detection

2020.02 - 2020.07

## Overview

This graduation project collected game logs through the Riot Games API and OP.GG crawling, then scored League of Legends users' toxic behavior and made the results available on the web.

The implementation was split into web, API, crawling, and log repositories. I led project planning and collaboration as team lead.

## Role and scope

- Led project planning and delivery within the project schedule.
- Participated in data collection/storage, toxicity scoring model work, and web result page development.
- Connected Riot Games API, OP.GG crawling, MySQL storage, Python model generation, Node.js API, and React web page.

## Problem and constraints

In-game toxic behavior cannot be checked through one direct metric, so we needed to combine publicly observable match data and OP.GG-visible signals into a user-level toxicity score.

The collected data and scoring criteria were heuristic for an experimental graduation project. This page does not present them as production-service-level validation metrics.

## Design and implementation

- Collected data for approximately 10,000 users and more than 100,000 game logs using Riot Games API and OP.GG crawling.
- Stored collected game records in MySQL RDS.
- Built a clustering-based toxicity scoring model with Python scripts and scikit-learn.
- Used KMeans/Hierarchical Clustering to analyze game-log features.
- Loaded a `.pkl` model to return troll scores for user queries.
- Displayed summoner-name search and per-game toxicity score results on a React web page.
- Split implementation across [web](https://github.com/Find-Troll/Trollgg), [API](https://github.com/Find-Troll/trollAPI), [crawling](https://github.com/Find-Troll/trollCrawling), and [log](https://github.com/Find-Troll/trollLog) repositories.

## Scoring signals

The toxicity score used the following OP.GG-visible signals.

- Tier
- Champion selection
- Abnormal item builds
- One-champion win-rate skew
- Low KDA
- Per-game profanity/toxicity score

## Validation and result

- Built a toxic-user detection system by combining collected data, clustering, and heuristic scoring.
- Observed about 95% agreement in manual sample validation.
- This value comes from manual validation in project documentation, not from a public benchmark or reproducible evaluation dataset. I do not use it as a production-service quality metric.
- Received an encouragement award for the graduation project.

## Public reference

- [Find-Troll GitHub organization](https://github.com/Find-Troll)
- [Find-Troll/Trollgg](https://github.com/Find-Troll/Trollgg)
- [Find-Troll/trollAPI](https://github.com/Find-Troll/trollAPI)
- [Find-Troll/trollCrawling](https://github.com/Find-Troll/trollCrawling)
- [Find-Troll/trollLog](https://github.com/Find-Troll/trollLog)
- [Project overview and demo video](https://youtu.be/DISVpCMBNtE?si=qwhlT71f3LCkxklY)

## Skills

React, Node.js, Python, scikit-learn, KMeans, Hierarchical Clustering, MySQL, AWS EC2, AWS RDS, Riot Games API, OP.GG crawling
