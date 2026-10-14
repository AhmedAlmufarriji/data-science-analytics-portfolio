# Social Network Database Simulation

A MySQL schema for user accounts, profiles, posts, follows and likes.

**Stack:** MySQL 8+, SQL

## Design

Uses primary and foreign keys to manage account/profile records, follower relationships, tweets and likes. Includes `createAccount` and `User_Follow` demonstration procedures and test inserts.

**Security caveat:** Password hashing inside a SQL demonstration (including SHA2 where used) is not production password management. Use a modern password hashing mechanism such as Argon2id in the application layer for real systems.

## How to get started

```bash
mysql -u USER -p < sql/social_network.sql
```

Runs with a local test database; inspect tables and routines after execution.
