-- =============================================================
-- ELECTRONIC LIBRARY MANAGEMENT SYSTEM | MySQL 8.0+
-- Project: Requirements, conceptual, logical and physical design
-- Run once in a NEW database using MySQL Workbench or MySQL CLI.
-- =============================================================

-- 1) Create/select database.
CREATE DATABASE IF NOT EXISTS electronic_library_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE electronic_library_db;

-- 2) AUTHORS: one author can write several books.
CREATE TABLE authors (
  author_id INT AUTO_INCREMENT PRIMARY KEY,
  author_name VARCHAR(120) NOT NULL,
  biography TEXT
) ENGINE=InnoDB;

-- 3) MEMBERS: unique membership number and e-mail.
CREATE TABLE members (
  member_id INT AUTO_INCREMENT PRIMARY KEY,
  membership_no VARCHAR(20) NOT NULL UNIQUE,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  phone VARCHAR(20)
) ENGINE=InnoDB;

-- 4) BOOKS: each book has one author.
CREATE TABLE books (
  book_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  publish_year SMALLINT UNSIGNED NOT NULL,
  category VARCHAR(80) NOT NULL,
  author_id INT NOT NULL,
  CONSTRAINT fk_books_authors FOREIGN KEY (author_id)
    REFERENCES authors(author_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT chk_publish_year CHECK (publish_year BETWEEN 1450 AND 2100)
) ENGINE=InnoDB;

-- 5) BORROWINGS: NULL return_date = an active loan.
-- The generated column + UNIQUE constraint forbids two active
-- loans for the same book, even if rows are inserted directly.
CREATE TABLE borrowings (
  borrow_id INT AUTO_INCREMENT PRIMARY KEY,
  book_id INT NOT NULL,
  member_id INT NOT NULL,
  borrow_date DATE NOT NULL,
  due_date DATE NOT NULL,
  return_date DATE DEFAULT NULL,
  active_book_id INT GENERATED ALWAYS AS
    (CASE WHEN return_date IS NULL THEN book_id ELSE NULL END) STORED,
  CONSTRAINT fk_borrowings_books FOREIGN KEY (book_id)
    REFERENCES books(book_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_borrowings_members FOREIGN KEY (member_id)
    REFERENCES members(member_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT uq_one_active_loan_per_book UNIQUE (active_book_id),
  CONSTRAINT chk_due_date CHECK (due_date >= borrow_date),
  CONSTRAINT chk_return_date CHECK
    (return_date IS NULL OR return_date >= borrow_date)
) ENGINE=InnoDB;

-- 6) Search indexes (unique keys already create their own indexes).
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_members_name ON members(full_name);
CREATE INDEX idx_borrowings_member_date ON borrowings(member_id, borrow_date);

-- 7) Book status is derived from loans (no duplicate status to update).
CREATE VIEW v_book_status AS
SELECT b.book_id, b.title, b.category,
  a.author_name,
  CASE WHEN EXISTS (
    SELECT 1 FROM borrowings br
    WHERE br.book_id = b.book_id AND br.return_date IS NULL
  ) THEN 'Borrowed' ELSE 'Available' END AS book_status
FROM books AS b
JOIN authors AS a ON a.author_id = b.author_id;

-- 8) Seed data: authors, members and books.
INSERT INTO authors (author_name, biography) VALUES
  ('Naguib Mahfouz', 'Egyptian novelist and Nobel laureate.'),
  ('Ghazi Al-Gosaibi', 'Saudi poet, writer and diplomat.'),
  ('Agatha Christie', 'British writer of detective fiction.'),
  ('George Orwell', 'English novelist and essayist.'),
  ('Paulo Coelho', 'Brazilian novelist.');

INSERT INTO members (membership_no, full_name, email, phone) VALUES
  ('LIB-001', 'Ahmed Alharbi', 'ahmed.library@example.com', '0500000001'),
  ('LIB-002', 'Nouf Alqahtani', 'nouf.library@example.com', '0500000002'),
  ('LIB-003', 'Sara Alotaibi', 'sara.library@example.com', '0500000003'),
  ('LIB-004', 'Khalid Alshammari', 'khalid.library@example.com', '0500000004'),
  ('LIB-005', 'Lina Alghamdi', 'lina.library@example.com', '0500000005'),
  ('LIB-006', 'Omar Alsubaie', 'omar.library@example.com', '0500000006');

INSERT INTO books (title, publish_year, category, author_id) VALUES
  ('Midaq Alley', 1947, 'Novel', 1),
  ('The Thief and the Dogs', 1961, 'Novel', 1),
  ('An Apartment Called Freedom', 1994, 'Novel', 2),
  ('The Alchemist', 1988, 'Fiction', 5),
  ('Murder on the Orient Express', 1934, 'Mystery', 3),
  ('And Then There Were None', 1939, 'Mystery', 3),
  ('1984', 1949, 'Dystopian', 4),
  ('Animal Farm', 1945, 'Satire', 4),
  ('The Zahir', 2005, 'Fiction', 5),
  ('The Harafish', 1977, 'Novel', 1);

-- 9) Borrowing and returning with a transaction and validation.
-- Use these procedures instead of manually changing loan records.
DELIMITER $$

CREATE PROCEDURE borrow_book(IN p_book_id INT, IN p_member_id INT)
BEGIN
  DECLARE v_locked_book INT DEFAULT NULL;
  DECLARE v_member_count INT DEFAULT 0;
  DECLARE v_active_count INT DEFAULT 0;
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;

  START TRANSACTION;
  SELECT book_id INTO v_locked_book
  FROM books WHERE book_id = p_book_id FOR UPDATE;

  IF v_locked_book IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Book not found';
  END IF;

  SELECT COUNT(*) INTO v_member_count
  FROM members WHERE member_id = p_member_id;
  IF v_member_count = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Member not found';
  END IF;

  SELECT COUNT(*) INTO v_active_count
  FROM borrowings WHERE book_id = p_book_id AND return_date IS NULL;
  IF v_active_count > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Book is currently borrowed';
  END IF;

  INSERT INTO borrowings (book_id, member_id, borrow_date, due_date)
  VALUES (p_book_id, p_member_id, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY));
  COMMIT;
END$$

CREATE PROCEDURE return_book(IN p_borrow_id INT)
BEGIN
  DECLARE v_book_id INT DEFAULT NULL;
  DECLARE v_locked_book INT DEFAULT NULL;
  DECLARE v_return_date DATE DEFAULT NULL;
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;

  START TRANSACTION;
  SELECT book_id INTO v_book_id
  FROM borrowings WHERE borrow_id = p_borrow_id;

  IF v_book_id IS NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Borrowing not found';
  END IF;

  SELECT book_id INTO v_locked_book
  FROM books WHERE book_id = v_book_id FOR UPDATE;
  SELECT return_date INTO v_return_date
  FROM borrowings WHERE borrow_id = p_borrow_id FOR UPDATE;

  IF v_return_date IS NOT NULL THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Book was already returned';
  END IF;

  UPDATE borrowings SET return_date = CURDATE()
  WHERE borrow_id = p_borrow_id;
  COMMIT;
END$$

DELIMITER ;

-- 10) Demonstrate: four borrowings, then return two books.
-- These IDs correspond to the fresh seed data above.
CALL borrow_book(1, 1);
CALL borrow_book(3, 2);
CALL borrow_book(6, 5);
CALL borrow_book(8, 4);
CALL return_book(2);
CALL return_book(4);

-- 11) Display all tables.
SHOW TABLES;
SELECT * FROM authors;
SELECT * FROM members;
SELECT * FROM books;
SELECT * FROM borrowings;

-- 12) Book availability: 2 borrowed and 8 available after the demo.
SELECT * FROM v_book_status ORDER BY book_id;

-- 13) Active loans with member, book and due date.
SELECT br.borrow_id, b.title, m.full_name,
       br.borrow_date, br.due_date
FROM borrowings br
JOIN books b ON b.book_id = br.book_id
JOIN members m ON m.member_id = br.member_id
WHERE br.return_date IS NULL
ORDER BY br.borrow_date, br.borrow_id;

-- 14) Library summary: expected 5 authors, 10 books, 6 members,
-- 4 loan records, with 2 books still borrowed.
SELECT (SELECT COUNT(*) FROM authors) AS total_authors,
       (SELECT COUNT(*) FROM books) AS total_books,
       (SELECT COUNT(*) FROM members) AS total_members,
       (SELECT COUNT(*) FROM borrowings) AS total_borrowings,
       (SELECT COUNT(*) FROM borrowings WHERE return_date IS NULL) AS active_loans;

-- 15) Example of registering another author/member/book later:
-- INSERT INTO authors (author_name, biography) VALUES ('New Author', 'Biography');
-- INSERT INTO members (membership_no, full_name, email)
-- VALUES ('LIB-007', 'New Member', 'new.member@example.com');
-- INSERT INTO books (title, publish_year, category, author_id)
-- VALUES ('New Title', 2023, 'Education', 1);