-- 01 | Database and user accounts
-- Twitter Simulation | MySQL 8.0+
-- Educational project: resets ONLY the twitter_simulation demo database.
-- All serial IDs are generated using AUTO_INCREMENT.
SET NAMES utf8mb4;
DROP DATABASE IF EXISTS twitter_simulation;
CREATE DATABASE twitter_simulation
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE twitter_simulation;

-- Account login data; store a SHA-256 hash, never plain passwords.
CREATE TABLE users (
    user_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash BINARY(64) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- One user has at most one profile. Username is unique.
CREATE TABLE profiles (
    profile_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL UNIQUE,
    username VARCHAR(30) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    bio VARCHAR(280),
    location VARCHAR(100),
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_profiles_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 02 | Follow, tweet and like tables
-- Each user can follow many users and be followed by many users.
-- A UNIQUE pair prevents following the same person twice.
CREATE TABLE follows (
    follow_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    follower_user_id BIGINT UNSIGNED NOT NULL,
    followed_user_id BIGINT UNSIGNED NOT NULL,
    followed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_follow_pair UNIQUE (follower_user_id, followed_user_id),
    CONSTRAINT fk_follows_follower FOREIGN KEY (follower_user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_follows_followed FOREIGN KEY (followed_user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT chk_not_self_follow CHECK (follower_user_id <> followed_user_id)
) ENGINE=InnoDB;

-- One user may publish multiple tweets (up to 280 characters).
CREATE TABLE tweets (
    tweet_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    content VARCHAR(280) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tweets_author FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT chk_tweet_content CHECK (CHAR_LENGTH(content) > 0)
) ENGINE=InnoDB;

-- One tweet may be liked by many users; each user likes it once.
CREATE TABLE likes (
    like_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    tweet_id BIGINT UNSIGNED NOT NULL,
    liked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_tweet_like UNIQUE (user_id, tweet_id),
    CONSTRAINT fk_likes_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_likes_tweet FOREIGN KEY (tweet_id)
        REFERENCES tweets(tweet_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 03 | Stored procedure: createAccount
-- Adds login data and profile atomically in one transaction.
-- SHA2(password, 256) returns 64 hexadecimal characters for BINARY(64).
DELIMITER $$
CREATE PROCEDURE createAccount(
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_username VARCHAR(30),
    IN p_display_name VARCHAR(100),
    IN p_bio VARCHAR(280),
    IN p_location VARCHAR(100)
)
BEGIN
    DECLARE v_user_id BIGINT UNSIGNED;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
    INSERT INTO users (email, password_hash)
    VALUES (p_email, CAST(SHA2(p_password, 256) AS BINARY(64)));
    SET v_user_id = LAST_INSERT_ID();

    INSERT INTO profiles
        (user_id, username, display_name, bio, location)
    VALUES
        (v_user_id, p_username, p_display_name, p_bio, p_location);
    COMMIT;
END$$
DELIMITER ;

-- 04 | Stored procedure: User_Follow
-- Follows another user by USERNAME (without entering numeric IDs).
-- Rejects missing usernames, self-following and duplicate follows.
DELIMITER $$
CREATE PROCEDURE User_Follow(
    IN p_follower_username VARCHAR(30),
    IN p_target_username VARCHAR(30)
)
BEGIN
    DECLARE v_follower_id BIGINT UNSIGNED DEFAULT NULL;
    DECLARE v_target_id BIGINT UNSIGNED DEFAULT NULL;

    SELECT user_id INTO v_follower_id
    FROM profiles WHERE username = p_follower_username;

    SELECT user_id INTO v_target_id
    FROM profiles WHERE username = p_target_username;

    IF v_follower_id IS NULL OR v_target_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'One or both usernames do not exist';
    END IF;

    IF v_follower_id = v_target_id THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A user cannot follow themselves';
    END IF;

    INSERT INTO follows (follower_user_id, followed_user_id)
    VALUES (v_follower_id, v_target_id);
END$$
DELIMITER ;

-- 05 | Insert account and profile examples
-- Sample accounts. User IDs, profile IDs and created_at are automatic.
-- Emails below use example.com and are fictional.
CALL createAccount('ahmed@example.com', 'DemoPass#A1',
    'ahmed_ds', 'Ahmed', 'Data science and AI learner', 'Makkah');
CALL createAccount('noura@example.com', 'DemoPass#N2',
    'noura_codes', 'Noura', 'Building apps with SQL', 'Riyadh');
CALL createAccount('khalid@example.com', 'DemoPass#K3',
    'khalid_tech', 'Khalid', 'Technology and innovation', 'Jeddah');
CALL createAccount('sara@example.com', 'DemoPass#S4',
    'sara_analytics', 'Sara', 'Analytics and visualization', 'Dammam');
CALL createAccount('faisal@example.com', 'DemoPass#F5',
    'faisal_travels', 'Faisal', 'Travel notes and photography', 'Taif');
CALL createAccount('lina@example.com', 'DemoPass#L6',
    'lina_reads', 'Lina', 'Books and learning', 'Medina');

-- Follow relationships are created by usernames, not IDs.
CALL User_Follow('ahmed_ds', 'noura_codes');
CALL User_Follow('ahmed_ds', 'sara_analytics');
CALL User_Follow('ahmed_ds', 'lina_reads');
CALL User_Follow('noura_codes', 'ahmed_ds');
CALL User_Follow('noura_codes', 'khalid_tech');
CALL User_Follow('khalid_tech', 'ahmed_ds');
CALL User_Follow('khalid_tech', 'noura_codes');
CALL User_Follow('sara_analytics', 'ahmed_ds');
CALL User_Follow('sara_analytics', 'lina_reads');
CALL User_Follow('faisal_travels', 'ahmed_ds');
CALL User_Follow('lina_reads', 'sara_analytics');
CALL User_Follow('lina_reads', 'noura_codes');

-- 06 | Insert tweets and likes
-- Find tweet authors by username so no serial ID is hard-coded.
INSERT INTO tweets (user_id, content)
SELECT user_id, 'Started learning MySQL today.'
FROM profiles WHERE username = 'ahmed_ds';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'ER diagrams make database design clearer.'
FROM profiles WHERE username = 'ahmed_ds';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'Foreign keys maintain relationships.'
FROM profiles WHERE username = 'ahmed_ds';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'A new project is coming soon!'
FROM profiles WHERE username = 'noura_codes';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'Stored procedures are useful for repeatable tasks.'
FROM profiles WHERE username = 'noura_codes';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'Technology can connect people worldwide.'
FROM profiles WHERE username = 'khalid_tech';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'Today I built my first dashboard.'
FROM profiles WHERE username = 'sara_analytics';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'Data tells a story when visualized well.'
FROM profiles WHERE username = 'sara_analytics';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'Exploring new destinations this weekend.'
FROM profiles WHERE username = 'faisal_travels';
INSERT INTO tweets (user_id, content)
SELECT user_id, 'Reading a great book about databases.'
FROM profiles WHERE username = 'lina_reads';

-- Like a tweet by matching its content and the liker username.
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'noura_codes'
  AND t.content = 'Started learning MySQL today.';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'sara_analytics'
  AND t.content = 'Started learning MySQL today.';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'ahmed_ds'
  AND t.content = 'A new project is coming soon!';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'khalid_tech'
  AND t.content = 'ER diagrams make database design clearer.';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'lina_reads'
  AND t.content = 'Today I built my first dashboard.';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'faisal_travels'
  AND t.content = 'Technology can connect people worldwide.';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'noura_codes'
  AND t.content = 'Stored procedures are useful for repeatable tasks.';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'ahmed_ds'
  AND t.content = 'Data tells a story when visualized well.';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'sara_analytics'
  AND t.content = 'Reading a great book about databases.';
INSERT INTO likes (user_id, tweet_id)
SELECT p.user_id, t.tweet_id FROM profiles AS p CROSS JOIN tweets AS t
WHERE p.username = 'lina_reads'
  AND t.content = 'Foreign keys maintain relationships.';

-- 07 | Display data and required tweet count
-- List all available tables.
SHOW TABLES;

-- Display every table. Hashes shown here are NOT plain passwords.
SELECT user_id, email,
       CAST(password_hash AS CHAR(64)) AS password_sha256,
       created_at
FROM users;
SELECT * FROM profiles;
SELECT * FROM follows;
SELECT * FROM tweets;
SELECT * FROM likes;

-- Display who follows whom, using usernames.
SELECT a.username AS follower, b.username AS followed,
       f.followed_at
FROM follows AS f
JOIN profiles AS a ON a.user_id = f.follower_user_id
JOIN profiles AS b ON b.user_id = f.followed_user_id
ORDER BY follower, followed;

-- Show who liked each tweet.
SELECT p.username AS liked_by, t.content AS tweet_content,
       l.liked_at
FROM likes AS l
JOIN profiles AS p ON p.user_id = l.user_id
JOIN tweets AS t ON t.tweet_id = l.tweet_id
ORDER BY t.tweet_id, liked_by;

-- REQUIRED: number of tweets for ONLY ONE USER (ahmed_ds).
SELECT p.username, COUNT(t.tweet_id) AS tweet_count
FROM profiles AS p
LEFT JOIN tweets AS t ON t.user_id = p.user_id
WHERE p.username = 'ahmed_ds'
GROUP BY p.user_id, p.username;

-- Extra: profile-style summary (followers, following, tweets, likes).
SELECT p.username, p.display_name, u.created_at,
       (SELECT COUNT(*) FROM follows AS f
        WHERE f.followed_user_id = p.user_id) AS followers_count,
       (SELECT COUNT(*) FROM follows AS f
        WHERE f.follower_user_id = p.user_id) AS following_count,
       (SELECT COUNT(*) FROM tweets AS t
        WHERE t.user_id = p.user_id) AS tweets_count,
       (SELECT COUNT(*) FROM likes AS l
        WHERE l.user_id = p.user_id) AS likes_given_count
FROM profiles AS p
JOIN users AS u ON u.user_id = p.user_id
ORDER BY p.username;