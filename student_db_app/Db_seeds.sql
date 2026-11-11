
USE classesDB;

-- =========================================
-- CLEAR EXISTING DATA
-- =========================================
-- Disable safe update mode
SET SQL_SAFE_UPDATES = 0;

DELETE FROM enrollments;
DELETE FROM students;
DELETE FROM courses;

-- Enable safe update mode again
SET SQL_SAFE_UPDATES = 1;

-- =========================================
-- SEED 15 STUDENTS
-- =========================================

INSERT INTO students
(student_id, student_name, last_name, email, is_active)
VALUES
(1,  'John',    'Sanchez',   'JohnSanchez@gmail.com',   TRUE),
(2,  'Pedro',   'Martin',    'PedroM@gmail.com',         TRUE),
(3,  'Ethan',   'Lennox',    'EthanL@gmail.com',         FALSE),
(4,  'Sal',     'Ami',       'SalAmi@gmail.com',         TRUE),
(5,  'Pan',     'Largo',     'PanL@gmail.com',            TRUE),
(6,  'Maria',   'Rodriguez', 'MariaR@gmail.com',          TRUE),
(7,  'David',   'Johnson',   'DavidJ@gmail.com',          FALSE),
(8,  'Sophia',  'Williams',  'SophiaW@gmail.com',         TRUE),
(9,  'Lucas',   'Garcia',    'LucasG@gmail.com',          TRUE),
(10, 'Emma',    'Brown',     'EmmaB@gmail.com',           TRUE),
(11, 'Daniel',  'Miller',    'DanielM@gmail.com',         TRUE),
(12, 'Olivia',  'Davis',     'OliviaD@gmail.com',         TRUE),
(13, 'Michael', 'Wilson',    'MichaelW@gmail.com',        TRUE),
(14, 'Isabella','Moore',     'IsabellaM@gmail.com',       TRUE),
(15, 'James',   'Taylor',    'JamesT@gmail.com',          TRUE);


-- =========================================
-- SEED 15 COURSES
-- =========================================

INSERT INTO courses
(course_id, course_name, credits)
VALUES
(101, 'Introduction to Programming', 3),
(102, 'Database Management Systems', 4),
(103, 'Web Development',             3),
(104, 'Data Structures',             4),
(105, 'Software Engineering',         3),
(106, 'Computer Networks',            3),
(107, 'Operating Systems',            4),
(108, 'Object-Oriented Programming',  3),
(109, 'Mobile App Development',       3),
(110, 'Cybersecurity Fundamentals',   3),
(111, 'Cloud Computing',              3),
(112, 'Artificial Intelligence',      4),
(113, 'Computer Architecture',        3),
(114, 'Human-Computer Interaction',   3),
(115, 'Algorithms',                   4);


-- =========================================
-- SEED 15 ENROLLMENTS
-- JUNCTION TABLE
-- =========================================

INSERT INTO enrollments
(student_id, course_id, registered)
VALUES
(1,  101, '2026-09-01 09:00:00'),
(1,  102, '2026-09-01 09:15:00'),

(2,  101, '2026-09-01 10:00:00'),
(2,  103, '2026-09-01 10:15:00'),

(3,  104, '2026-09-02 11:00:00'),

(4,  102, '2026-09-02 12:00:00'),
(4,  105, '2026-09-02 12:15:00'),

(5,  106, '2026-09-03 09:00:00'),

(6,  107, '2026-09-03 10:00:00'),
(6,  108, '2026-09-03 10:15:00'),

(7,  103, '2026-09-04 11:00:00'),

(8,  109, '2026-09-04 12:00:00'),

(9,  110, '2026-09-05 09:00:00'),
(9,  111, '2026-09-05 09:15:00'),

(10, 112, '2026-09-05 10:00:00');


-- =========================================
-- VERIFY
-- =========================================

SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM enrollments;


-- =========================================
-- JOIN ALL THREE TABLES
-- =========================================

SELECT
    s.student_id,
    s.student_name,
    s.last_name,
    c.course_id,
    c.course_name,
    c.credits,
    e.registered
FROM enrollments e
JOIN students s
    ON e.student_id = s.student_id
JOIN courses c
    ON e.course_id = c.course_id
ORDER BY s.student_id;
