# Secondary School Management — SQL Levels 1–3

An integrated relational database exercise covering table design, data modification, analytical queries and relationships.

**Stack:** MySQL 8+, SQL

## Contents

Students, teachers, subjects, many-to-many junction tables, sample records, conditional queries, aggregate functions, views, stored procedures, and indexes.

**Caution:** This script creates and modifies a course sample database; check for `DROP` or table-renaming commands before executing. Use MySQL Workbench against a disposable local database.

Student and teacher names are fictional demonstration records.

## How to get started

```bash
mysql -u USER -p < sql/school_management_levels_1_to_3.sql
```

Replace USER with your local MySQL username. Avoid executing against any existing school production system.
