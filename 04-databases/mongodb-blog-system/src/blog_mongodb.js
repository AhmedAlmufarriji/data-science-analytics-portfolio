// MongoDB Blog Project
// Run using: mongosh Blog_MongoDB_Project.js
// The database must be empty before the first run.

// 1. Select the blog database.
// MongoDB creates the database when data is first stored.
db = db.getSiblingDB("blog");

// Protect existing data when running the project again.
if (db.getCollectionNames().length > 0) {
  throw new Error("The blog database already contains collections. Use an empty database to run this project.");
}

// 2. Create exactly three collections.
db.createCollection("users");
db.createCollection("posts");
db.createCollection("followers");

// 3. Add the four required users using the command shell.
// MongoDB automatically generates a unique _id for each document.
const usersResult = db.users.insertMany([
  { name: "Sara", age: 20, email: "sara@tst.com", gender: "female" },
  { name: "Noura", age: 20, email: "noura@tst.com", gender: "female" },
  { name: "Ahmed", age: 22, email: "ahmed@tst.com", gender: "male" },
  { name: "Yasser", age: 25, email: "yasser@tst.com", gender: "male" }
]);

// Keep the generated IDs to create references between collections.
const userIds = usersResult.insertedIds;

// 4. Add the four required posts.
// Comments are embedded inside posts because the project allows only three collections.
const postsResult = db.posts.insertMany([
  {
    title: "IOS programming",
    content: "Swift is a powerful and intuitive programming language for macOS, iOS, watchOS, tvOS and beyond",
    userId: userIds[0],  // Sara
    comments: []
  },
  {
    title: "android programming",
    content: "you learn beginning Android programming concepts using the Kotlin programming language, and you build a variety of apps using Android Studio.",
    userId: userIds[1],  // Noura
    comments: []
  },
  {
    title: "machine learning",
    content: "Machine learning is the study of computer algorithms that improve automatically through experience",
    userId: userIds[1],  // Noura
    comments: []
  },
  {
    title: "artificial intelligence",
    content: "Artificial intelligence, is intelligence demonstrated by machines, unlike the natural intelligence displayed by humans and animals",
    userId: userIds[3],  // Yasser
    comments: []
  }
]);

const postIds = postsResult.insertedIds;

// 5. Demonstrate comments by other users, inside the existing posts collection.
db.posts.updateOne(
  { _id: postIds[0] },
  { $push: { comments: { userId: userIds[1], text: "This is a useful post!", createdAt: new Date() } } }
);

db.posts.updateOne(
  { _id: postIds[1] },
  { $push: { comments: { userId: userIds[2], text: "Thanks for sharing!", createdAt: new Date() } } }
);

// 6. Create following relationships (many-to-many).
// followerId: the person who follows; followingId: the person being followed.
db.followers.insertMany([
  { followerId: userIds[0], followingId: userIds[1] }, // Sara follows Noura
  { followerId: userIds[0], followingId: userIds[2] }, // Sara follows Ahmed
  { followerId: userIds[1], followingId: userIds[0] }, // Noura follows Sara
  { followerId: userIds[1], followingId: userIds[3] }, // Noura follows Yasser
  { followerId: userIds[2], followingId: userIds[1] }, // Ahmed follows Noura
  { followerId: userIds[3], followingId: userIds[0] }  // Yasser follows Sara
]);

// 7. Indexes to improve lookup performance and prevent duplicate emails/follows.
db.users.createIndex({ email: 1 }, { unique: true });
db.posts.createIndex({ userId: 1 });
db.followers.createIndex({ followerId: 1, followingId: 1 }, { unique: true });

// 8. Display all inserted collections and their documents.
print("\n=== Collections ===");
printjson(db.getCollectionNames());
print("\n=== Users before age update ===");
db.users.find().forEach(printjson);
print("\n=== Posts before deletion ===");
db.posts.find().forEach(printjson);
print("\n=== Followers ===");
db.followers.find().forEach(printjson);

// 9. Update Sara's age to 22.
db.users.updateOne({ name: "Sara" }, { $set: { age: 22 } });

// 10. Delete the machine learning post (authored by Noura).
db.posts.deleteOne({ title: "machine learning", userId: userIds[1] });

// 11. Verify the final state.
print("\n=== Sara after update ===");
printjson(db.users.findOne({ name: "Sara" }));
print("\n=== Machine learning post after deletion ===");
printjson(db.posts.findOne({ title: "machine learning" }));  // null
print("\n=== All remaining posts ===");
db.posts.find().forEach(printjson);
print("\n=== Final document counts ===");
print("Users: " + db.users.countDocuments({}));          // 4
print("Posts: " + db.posts.countDocuments({}));          // 3
print("Followers: " + db.followers.countDocuments({}));  // 6