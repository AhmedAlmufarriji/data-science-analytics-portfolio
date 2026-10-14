# MongoDB Blog with Followers

Three MongoDB collections represent users, posts and following relationships.

**Stack:** MongoDB, mongosh, JavaScript

## Model

- `users`: member profiles with demonstration names and email addresses.
- `posts`: articles and embedded comments.
- `followers`: relationships between users.

The script inserts course sample data, edits Sara's age, deletes the machine-learning post and illustrates document queries. This is a local educational example, not a production authentication or content-moderation system.

**Caution:** Execute in a disposable MongoDB database, not an existing production database.

## How to get started

```bash
mongosh < src/blog_mongodb.js
```

Use a local test instance, then inspect `db.users.find()`, `db.posts.find()` and `db.followers.find()`.
