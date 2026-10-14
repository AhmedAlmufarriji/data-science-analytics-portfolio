# Electronic Library Management Database

Relational schema for authors, books, members and lending/return transactions.

**Stack:** MySQL 8+, SQL

## Database design

Requirements analysis, conceptual ER model, logical primary/foreign keys and physical indexes. Demonstrates book availability and SQL operations for borrowing and returning books.

**Caution:** The stored procedures and sample data are for a learning exercise; production circulation systems require authentication, recovery, concurrency validation and richer audit trails.

## How to get started

```bash
mysql -u USER -p < sql/library_management.sql
```

Use an isolated local MySQL database for demonstration and review.
