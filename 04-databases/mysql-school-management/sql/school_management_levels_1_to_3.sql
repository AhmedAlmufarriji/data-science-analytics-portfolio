-- =====================================================================
-- مشروع مدرسة التميز: مستويات SQL الثلاثة (MySQL 8.0)
-- ملف كامل لإنشاء قاعدة البيانات وتطبيق المستويات 1 ثم 2 ثم 3.
-- شغّل الملف مرة واحدة على قاعدة بيانات غير موجودة سابقًا.
-- =====================================================================

-- مشروع مدرسة التميز: المستوى الأول والمستوى الثاني
-- شغّل هذا الملف على قاعدة MySQL نظيفة لتنفيذ المشروع كاملًا.

-- ================================================================
-- مشروع قواعد البيانات: مدرسة التميز للتعليم الثانوي
-- النظام المستخدم: MySQL
-- المحتوى: إنشاء قاعدة بيانات، إنشاء جداول، إدخال البيانات،
--          عرض البيانات وترتيبها، الأسماء المستعارة، التحديث،
--          وتغيير اسم أحد الجداول.
-- ================================================================

-- 1) إنشاء قاعدة البيانات مع دعم الأحرف العربية.
CREATE DATABASE IF NOT EXISTS al_tamayuz_secondary_school
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 2) اختيار قاعدة البيانات لتنفيذ الأوامر التالية داخلها.
USE al_tamayuz_secondary_school;

-- 3) إنشاء جدول الطلاب والمعلومات الأساسية المطلوبة لكل طالب.
CREATE TABLE students (
    id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('F', 'M') NOT NULL,
    enrollment_date DATE NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    academic_level TINYINT NOT NULL CHECK (academic_level BETWEEN 1 AND 6),
    study_track ENUM('علمي', 'انساني') NOT NULL,
    gpa DECIMAL(5,2) NOT NULL CHECK (gpa BETWEEN 0 AND 100)
);

-- 4) إنشاء جدول المعلمين وتحديد الحقول المطلوبة.
CREATE TABLE teachers (
    id INT PRIMARY KEY,
    teacher_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('F', 'M') NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    office_number INT NOT NULL
);

-- 5) إنشاء جدول المواد الدراسية.
CREATE TABLE subjects (
    id INT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL
);

-- 6) عرض الجداول المتاحة في قاعدة البيانات بعد إنشائها.
SHOW TABLES;

-- 7) إدخال بيانات 30 طالبًا في جدول students.
--    جميع الأسماء والبريد الإلكتروني أمثلة افتراضية لأغراض التدريب.
INSERT INTO students
    (id, student_name, date_of_birth, gender, enrollment_date, email, academic_level, study_track, gpa)
VALUES
    (1,  'أحمد سالم',      '2010-02-14', 'M', '2025-08-24', 'ahmed.salem@student.example.com',       1, 'علمي',   94.50),
    (2,  'محمد خالد',      '2009-07-03', 'M', '2025-08-24', 'mohammed.khalid@student.example.com',   2, 'انساني', 88.25),
    (3,  'عبدالله ناصر',   '2009-11-21', 'M', '2024-08-18', 'abdullah.nasser@student.example.com',   3, 'علمي',   91.75),
    (4,  'عمر فهد',        '2008-04-09', 'M', '2024-08-18', 'omar.fahad@student.example.com',        4, 'علمي',   85.40),
    (5,  'يوسف ماجد',      '2008-12-17', 'M', '2023-08-20', 'yousef.majed@student.example.com',      5, 'انساني', 90.00),
    (6,  'خالد إبراهيم',   '2007-09-06', 'M', '2023-08-20', 'khalid.ibrahim@student.example.com',    6, 'علمي',   96.10),
    (7,  'نورة أحمد',      '2010-05-25', 'F', '2025-08-24', 'noura.ahmed@student.example.com',       1, 'انساني', 93.20),
    (8,  'سارة محمد',      '2009-01-30', 'F', '2025-08-24', 'sarah.mohammed@student.example.com',    2, 'علمي',   97.30),
    (9,  'ريم عبدالله',    '2009-10-12', 'F', '2024-08-18', 'reem.abdullah@student.example.com',     3, 'علمي',   89.90),
    (10, 'هند خالد',       '2008-06-18', 'F', '2024-08-18', 'hind.khalid@student.example.com',       4, 'انساني', 87.50),
    (11, 'ليان فهد',       '2008-03-04', 'F', '2023-08-20', 'layan.fahad@student.example.com',       5, 'علمي',   95.80),
    (12, 'جود علي',        '2007-12-11', 'F', '2023-08-20', 'joud.ali@student.example.com',          6, 'علمي',   98.00),
    (13, 'فيصل تركي',      '2010-08-16', 'M', '2025-08-24', 'faisal.turki@student.example.com',      1, 'علمي',   82.70),
    (14, 'راشد سعيد',      '2009-02-07', 'M', '2025-08-24', 'rashed.saeed@student.example.com',      2, 'انساني', 86.60),
    (15, 'سلطان بدر',      '2009-09-19', 'M', '2024-08-18', 'sultan.badr@student.example.com',       3, 'علمي',   92.45),
    (16, 'تركي عادل',      '2008-07-22', 'M', '2024-08-18', 'turki.adel@student.example.com',        4, 'انساني', 84.30),
    (17, 'بدر حمد',        '2008-10-05', 'M', '2023-08-20', 'badr.hamad@student.example.com',        5, 'علمي',   88.80),
    (18, 'ماجد منصور',     '2007-05-13', 'M', '2023-08-20', 'majed.mansour@student.example.com',     6, 'انساني', 91.15),
    (19, 'العنود سعد',     '2010-03-28', 'F', '2025-08-24', 'alanoud.saad@student.example.com',      1, 'علمي',   96.40),
    (20, 'أروى حسن',       '2009-06-02', 'F', '2025-08-24', 'arwa.hassan@student.example.com',       2, 'انساني', 89.10),
    (21, 'دانة يوسف',      '2009-12-23', 'F', '2024-08-18', 'dana.yousef@student.example.com',       3, 'علمي',   94.90),
    (22, 'لمى ناصر',       '2008-01-15', 'F', '2024-08-18', 'lama.nasser@student.example.com',       4, 'علمي',   90.35),
    (23, 'مها إبراهيم',    '2008-09-08', 'F', '2023-08-20', 'maha.ibrahim@student.example.com',      5, 'انساني', 87.95),
    (24, 'رغد مازن',       '2007-11-27', 'F', '2023-08-20', 'raghad.mazen@student.example.com',      6, 'علمي',   99.00),
    (25, 'عبدالرحمن صالح', '2010-04-20', 'M', '2025-08-24', 'abdulrahman.saleh@student.example.com', 1, 'انساني', 83.55),
    (26, 'زياد حاتم',      '2009-08-31', 'M', '2025-08-24', 'ziyad.hatem@student.example.com',       2, 'علمي',   90.75),
    (27, 'أسامة طارق',     '2009-05-10', 'M', '2024-08-18', 'osama.tariq@student.example.com',       3, 'انساني', 85.85),
    (28, 'شهد سامي',       '2008-02-26', 'F', '2024-08-18', 'shahad.sami@student.example.com',       4, 'علمي',   97.65),
    (29, 'غادة وليد',      '2008-11-14', 'F', '2023-08-20', 'ghada.waleed@student.example.com',      5, 'انساني', 92.20),
    (30, 'مشاعل صالح',     '2007-07-01', 'F', '2023-08-20', 'mashael.saleh@student.example.com',     6, 'علمي',   95.25);

-- 8) إدخال بيانات 10 معلمين في جدول teachers.
INSERT INTO teachers
    (id, teacher_name, date_of_birth, gender, email, office_number)
VALUES
    (1,  'سالم عبدالله',   '1983-03-12', 'M', 'salem.abdullah@teacher.example.com', 101),
    (2,  'خالد منصور',    '1979-08-25', 'M', 'khalid.mansour@teacher.example.com', 102),
    (3,  'أحمد ناصر',     '1986-01-17', 'M', 'ahmed.nasser@teacher.example.com',   103),
    (4,  'فهد محمد',      '1981-11-04', 'M', 'fahad.mohammed@teacher.example.com', 104),
    (5,  'علي إبراهيم',   '1990-05-29', 'M', 'ali.ibrahim@teacher.example.com',   105),
    (6,  'منال صالح',     '1984-07-08', 'F', 'manal.saleh@teacher.example.com',   106),
    (7,  'نورة حسن',      '1988-02-14', 'F', 'noura.hassan@teacher.example.com',  107),
    (8,  'سارة سعيد',     '1982-10-31', 'F', 'sarah.saeed@teacher.example.com',   108),
    (9,  'ريم خالد',      '1991-12-19', 'F', 'reem.khalid@teacher.example.com',   109),
    (10, 'هند ماجد',      '1985-06-22', 'F', 'hind.majed@teacher.example.com',    110);

-- 9) إدخال بيانات 6 مواد دراسية في جدول subjects.
INSERT INTO subjects (id, subject_name)
VALUES
    (1, 'الرياضيات'),
    (2, 'الفيزياء'),
    (3, 'الكيمياء'),
    (4, 'الأحياء'),
    (5, 'اللغة العربية'),
    (6, 'اللغة الإنجليزية');

-- 10) عرض جميع محتويات جدول الطلاب.
SELECT * FROM students;

-- 11) عرض جميع محتويات جدول المعلمين.
SELECT * FROM teachers;

-- 12) عرض جميع محتويات جدول المواد.
SELECT * FROM subjects;

-- 13) عرض بيانات الطلاب مرتبة تصاعديًا وفق اسم الطالب.
SELECT * FROM students
ORDER BY student_name ASC;

-- 14) عرض اسم الطالب باسم مستعار أقصر (الطالب) باستخدام AS.
SELECT id, student_name AS `الطالب`, email, academic_level
FROM students;

-- 15) تحديث البريد الإلكتروني للطالب الذي رقمه التسلسلي 1.
UPDATE students
SET email = 'ahmed.salem.updated@student.example.com'
WHERE id = 1;

-- 16) تحديث رقم المكتب للمعلم الذي رقمه التسلسلي 1.
UPDATE teachers
SET office_number = 201
WHERE id = 1;

-- 17) عرض السجلين للتأكد من نجاح عمليتي التعديل.
SELECT * FROM students WHERE id = 1;
SELECT * FROM teachers WHERE id = 1;

-- 18) تغيير اسم جدول المواد من subjects إلى school_subjects.
ALTER TABLE subjects RENAME TO school_subjects;

-- 19) عرض الجداول مجددًا للتحقق من ظهور الاسم الجديد.
SHOW TABLES;

-- 20) عرض محتويات جدول المواد باسمه الجديد بعد التعديل.
SELECT * FROM school_subjects;

-- 21) التحقق من أعداد السجلات المدخلة: 30 طالبًا، 10 معلمين، 6 مواد.
SELECT COUNT(*) AS student_count FROM students;
SELECT COUNT(*) AS teacher_count FROM teachers;
SELECT COUNT(*) AS subject_count FROM school_subjects;


-- ====================================================================
-- مشروع SQL - المستوى الثاني: مدرسة التميز للتعليم الثانوي
-- استكمال مشروع المستوى الأول (MySQL 8.0)
-- المتطلبات: جداول مشتقة، LIKE، دوال التجميع والأرقام والنصوص،
--            الاستعلامات الشرطية، وتحديث بيانات الطلاب.
-- ====================================================================

-- 1) استخدام قاعدة البيانات المنشأة في مشروع المستوى الأول.
USE al_tamayuz_secondary_school;

-- 2) إضافة أربع سجلات افتراضية إلى طلاب المستوى الأول لتجربة
--    الحالات المطلوبة؛ لأن بيانات المستوى الأول لا تضم معدلات دون 60،
--    أو معدلًا 100، أو أسماء تبدأ بالحرف الإنجليزي A.
--    يصبح إجمالي الطلاب 34 طالبًا، مع الإبقاء على السجلات الأصلية.
INSERT INTO students
    (id, student_name, date_of_birth, gender, enrollment_date,
     email, academic_level, study_track, gpa)
VALUES
    (31, 'Amal', '2010-10-01', 'F', '2025-08-24',
         'amal@student.example.com', 1, 'علمي', 55.00),
    (32, 'Adam', '2007-05-19', 'M', '2023-08-20',
         'adam@student.example.com', 6, 'علمي', 100.00),
    (33, 'Omar', '2009-03-04', 'M', '2025-08-24',
         'omar@student.example.com', 2, 'انساني', 58.00),
    (34, 'سالم', '2010-11-22', 'M', '2025-08-24',
         'salem@student.example.com', 1, 'علمي', 91.00);

-- 3) إنشاء جدول جديد يحتوي على جميع الطلاب الذين معدلاتهم أعلى من 90.
--    الجدول الناتج نسخة من الصفوف المطابقة لحظة تنفيذ الأمر.
CREATE TABLE outstanding_students AS
SELECT *
FROM students
WHERE gpa > 90;

-- 4) إنشاء جدول الطلاب غير المجتازين (معدل أقل من 60).
CREATE TABLE failing_students AS
SELECT *
FROM students
WHERE gpa < 60;

-- 5) عرض بيانات الجدولين الجديدين للتأكد من إنشائهما.
SHOW TABLES;
SELECT * FROM outstanding_students;
SELECT * FROM failing_students;

-- 6) عرض أسماء الطلاب التي تبدأ بحرف A الإنجليزي.
SELECT student_name AS `اسم الطالب`
FROM students
WHERE student_name LIKE 'A%';

-- 7) عرض أسماء الطلاب المؤلفة من أربعة أحرف بالضبط.
--    كل شرطة سفلية (_) في LIKE تمثل حرفًا واحدًا.
SELECT student_name AS `اسم الطالب`
FROM students
WHERE student_name LIKE '____';

-- 8) حساب المتوسط وأعلى معدل وأقل معدل مع أسماء واضحة للنتائج.
SELECT
    ROUND(AVG(gpa), 2) AS `متوسط المعدل التراكمي`,
    MAX(gpa) AS `أعلى معدل تراكمي`,
    MIN(gpa) AS `أقل معدل تراكمي`
FROM students;

-- 9) أسماء المتفوقين في المستوى السادس بمعدل تراكمي يساوي 100.
SELECT student_name AS `اسم الطالب`
FROM students
WHERE academic_level = 6 AND gpa = 100;

-- 10) عرض طلاب المستوى الأول الذين تتراوح أعمارهم بين 15 و16 سنة.
--     TIMESTAMPDIFF تحسب العمر بالسنوات المكتملة وقت تنفيذ الاستعلام.
SELECT
    id,
    student_name AS `اسم الطالب`,
    date_of_birth AS `تاريخ الميلاد`,
    TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) AS `العمر`
FROM students
WHERE academic_level = 1
  AND TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 15 AND 16;

-- 11) حساب عدد الطلاب المسجلين في المستوى الثاني.
SELECT COUNT(*) AS `عدد طلاب المستوى الثاني`
FROM students
WHERE academic_level = 2;

-- 12) عرض المسارات الدراسية دون تكرار باستخدام DISTINCT.
SELECT DISTINCT study_track AS `المسار الدراسي`
FROM students;

-- 13) عرض أسماء المواد باستخدام الدالة UPPER.
--     الأحرف العربية لا يوجد فيها تمييز بين الكبيرة والصغيرة،
--     لذا لن يتغير شكل أسماء المواد المكتوبة بالعربية.
SELECT UPPER(subject_name) AS `اسم المادة بالأحرف الكبيرة`
FROM school_subjects;

-- 14) تقريب المتوسط الحسابي للمعدلات للأسفل باستخدام FLOOR.
SELECT FLOOR(AVG(gpa)) AS `متوسط المعدلات بعد التقريب للأسفل`
FROM students;

-- 15) توسيع نوع عمود الجنس قبل كتابة Female وMale؛
--     لأن تعريفه السابق ENUM('F','M') لا يقبل القيم الجديدة.
ALTER TABLE students
MODIFY COLUMN gender ENUM('F', 'M', 'Female', 'Male') NOT NULL;

-- 16) استبدال F بـ Female وM بـ Male في جميع سجلات الطلاب.
--     REPLACE دالة نصية (String Function) كما هو مطلوب.
UPDATE students
SET gender = REPLACE(REPLACE(gender, 'F', 'Female'), 'M', 'Male')
WHERE gender IN ('F', 'M');

-- 17) عرض الطلاب بعد تغيير قيم عمود الجنس.
SELECT id, student_name, gender
FROM students
ORDER BY id;

-- 18) زيادة المعدل التراكمي خمس درجات للطلاب دون 60 فقط.
UPDATE students
SET gpa = gpa + 5
WHERE gpa < 60;

-- 19) التحقق من قيم المعدلات بعد التحديث للطلاب المحددين.
SELECT id, student_name, gpa AS `المعدل بعد الزيادة`
FROM students
WHERE id IN (31, 33);

-- 20) عرض عدد الطلاب في الجدولين المشتقين.
--     ملاحظة: failing_students يحفظ القيم قبل زيادة المعدلات؛
--     فهو جدول مستقل لا يتحدث تلقائيًا عند تعديل students.
SELECT COUNT(*) AS `عدد الطلاب المتفوقين` FROM outstanding_students;
SELECT COUNT(*) AS `عدد الطلاب غير المجتازين قبل التعديل`
FROM failing_students;


-- =====================================================================
-- بداية المستوى الثالث: العلاقات والإجراءات والـ View والفهارس
-- =====================================================================

-- =====================================================================
-- مدرسة التميز للتعليم الثانوي | SQL المستوى الثالث
-- يكمل مشروعي المستوى الأول والثاني (MySQL 8.0)
-- يشترط تشغيل المستويين السابقين مرة واحدة قبل هذا الملف.
-- =====================================================================

-- 1) اختيار قاعدة البيانات الحالية.
USE al_tamayuz_secondary_school;

-- ---------------------------------------------------------------------
-- العلاقة الأولى: المواد (1) إلى المعلمين (Many)
-- كل معلم يدرّس مادة واحدة، ويمكن للمادة أن يدرّسها عدة معلمين.
-- ---------------------------------------------------------------------

-- 2) إضافة مفتاح المادة إلى جدول المعلمين.
-- نضيفه أولًا وهو يقبل NULL لأن جدول المعلمين يحتوي بيانات مسبقًا.
ALTER TABLE teachers
ADD COLUMN subject_id INT NULL;

-- 3) توزيع المعلمين العشرة السابقين على المواد الست.
UPDATE teachers
SET subject_id = CASE id
    WHEN 1 THEN 1
    WHEN 2 THEN 2
    WHEN 3 THEN 3
    WHEN 4 THEN 4
    WHEN 5 THEN 5
    WHEN 6 THEN 6
    WHEN 7 THEN 1
    WHEN 8 THEN 2
    WHEN 9 THEN 3
    WHEN 10 THEN 4
END
WHERE id BETWEEN 1 AND 10;

-- 4) إضافة معلمين افتراضيين حتى تدرّس كل مادة بواسطة معلمين على الأقل.
INSERT INTO teachers
    (id, teacher_name, date_of_birth, gender, email, office_number, subject_id)
VALUES
    (11, 'عبدالعزيز حمد', '1987-02-15', 'M',
        'abdulaziz.hamad@teacher.example.com', 111, 5),
    (12, 'مريم صالح', '1989-09-18', 'F',
        'maryam.saleh@teacher.example.com', 112, 6);

-- 5) منع إسناد معلم إلى صف دون مادة، ثم ربط المادة بمفتاح أجنبي.
ALTER TABLE teachers
MODIFY COLUMN subject_id INT NOT NULL;

ALTER TABLE teachers
ADD CONSTRAINT fk_teachers_subject
FOREIGN KEY (subject_id) REFERENCES school_subjects(id)
ON UPDATE CASCADE
ON DELETE RESTRICT;

-- 6) عرض المواد مع أسماء المعلمين للتحقق من علاقة واحد إلى متعدد.
SELECT
    sb.id AS subject_id,
    sb.subject_name,
    t.id AS teacher_id,
    t.teacher_name
FROM school_subjects AS sb
JOIN teachers AS t ON t.subject_id = sb.id
ORDER BY sb.id, t.id;

-- ---------------------------------------------------------------------
-- العلاقة الثانية: الطلاب (Many) إلى المواد (Many)
-- ننشئ جدولًا وسيطًا student_subjects بمفتاح أساسي مركب.
-- ---------------------------------------------------------------------

-- 7) إنشاء جدول التحاق الطلاب بالمواد بمفتاحين أجنبيين.
CREATE TABLE student_subjects (
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    PRIMARY KEY (student_id, subject_id),
    CONSTRAINT fk_student_subjects_student
        FOREIGN KEY (student_id) REFERENCES students(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_student_subjects_subject
        FOREIGN KEY (subject_id) REFERENCES school_subjects(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 8) تسجيل كل طالب في ثلاث مواد مختلفة للتطبيق العملي.
-- MOD يوزّع المواد الست بين الطلاب الـ34 دون تكرار للطالب نفسه.
INSERT INTO student_subjects (student_id, subject_id)
SELECT s.id, sb.id
FROM students AS s
JOIN school_subjects AS sb
    ON sb.id IN (
        1 + MOD(s.id - 1, 6),
        1 + MOD(s.id, 6),
        1 + MOD(s.id + 1, 6)
    );

-- 9) عرض أسماء الطلاب والمواد من خلال الجدول الوسيط.
SELECT s.student_name, sb.subject_name
FROM student_subjects AS ss
JOIN students AS s ON ss.student_id = s.id
JOIN school_subjects AS sb ON ss.subject_id = sb.id
ORDER BY s.id, sb.id;

-- ---------------------------------------------------------------------
-- العلاقة الثالثة: المعلمون (Many) إلى الطلاب (Many)
-- ننشئ جدولًا وسيطًا teacher_students بمفتاح أساسي مركب.
-- ---------------------------------------------------------------------

-- 10) إنشاء جدول الربط بين المعلم والطالب بمفتاحين أجنبيين.
CREATE TABLE teacher_students (
    teacher_id INT NOT NULL,
    student_id INT NOT NULL,
    PRIMARY KEY (teacher_id, student_id),
    CONSTRAINT fk_teacher_students_teacher
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_teacher_students_student
        FOREIGN KEY (student_id) REFERENCES students(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- 11) ربط الطالب بمعلمي المواد التي يدرسها فقط.
-- DISTINCT يضمن عدم تكرار علاقة المعلم بالطالب.
INSERT INTO teacher_students (teacher_id, student_id)
SELECT DISTINCT t.id, ss.student_id
FROM student_subjects AS ss
JOIN teachers AS t ON t.subject_id = ss.subject_id;

-- 12) عرض أسماء الطلاب والمعلمين المرتبطين بهم.
SELECT s.student_name, t.teacher_name
FROM teacher_students AS ts
JOIN students AS s ON ts.student_id = s.id
JOIN teachers AS t ON ts.teacher_id = t.id
ORDER BY s.id, t.id;

-- 13) التأكد من أعداد العلاقات والجداول الجديدة.
SHOW TABLES;
SELECT COUNT(*) AS `عدد الطلاب` FROM students;
SELECT COUNT(*) AS `عدد المعلمين` FROM teachers;
SELECT COUNT(*) AS `عدد مواد الطلاب المسجلة` FROM student_subjects;
SELECT COUNT(*) AS `عدد علاقات المعلمين بالطلاب` FROM teacher_students;

-- ---------------------------------------------------------------------
-- الإجراء المخزن Procedure: student_info
-- يعرض جميع أعمدة الطالب، ورقم المادة، واسم المادة التي يدرسها.
-- ---------------------------------------------------------------------

-- 14) إنشاء الإجراء؛ نستخدم DELIMITER حتى لا تنهي ; الأمر مبكرًا.
DELIMITER //
CREATE PROCEDURE student_info()
BEGIN
    SELECT
        s.*,
        sb.id AS subject_id,
        sb.subject_name
    FROM students AS s
    JOIN student_subjects AS ss ON ss.student_id = s.id
    JOIN school_subjects AS sb ON sb.id = ss.subject_id
    ORDER BY s.id, sb.id;
END //
DELIMITER ;

-- 15) استدعاء الإجراء المخزن وعرض نتائجه.
CALL student_info();

-- ---------------------------------------------------------------------
-- العرض الافتراضي View: teacher_info
-- الاسم + رقم المكتب + المادة، ثم عرض الـ View وحذفه.
-- ---------------------------------------------------------------------

-- 16) إنشاء View يجمع المعلمين والمواد التي يدرّسونها.
CREATE VIEW teacher_info AS
SELECT
    t.teacher_name,
    t.office_number,
    sb.subject_name
FROM teachers AS t
JOIN school_subjects AS sb ON t.subject_id = sb.id;

-- 17) عرض الـ View ومحتوياته.
SELECT * FROM teacher_info
ORDER BY teacher_name;

-- 18) حذف الـ View فقط؛ لا تُحذف بيانات الجداول الأصلية.
DROP VIEW teacher_info;

-- ---------------------------------------------------------------------
-- الفهرس Index: ترتيب/بحث أسماء الطلاب أبجديًا.
-- ---------------------------------------------------------------------

-- 19) إنشاء Index على اسم الطالب بترتيب تصاعدي.
CREATE INDEX idx_students_name_alphabetical
ON students (student_name ASC);

-- 20) عرض الفهرس بعد إنشائه.
SHOW INDEX FROM students
WHERE Key_name = 'idx_students_name_alphabetical';

-- 21) عرض الطلاب مرتبين أبجديًا بحسب اسم الطالب.
SELECT id, student_name
FROM students
ORDER BY student_name ASC;

-- 22) حذف الفهرس؛ مع الاحتفاظ بالطلاب وأسمائهم.
DROP INDEX idx_students_name_alphabetical ON students;