-- Seeding Students table 

USE classesDB;

-- Disable safe update mode
SET SQL_SAFE_UPDATES = 0;

-- Clear the tables
DELETE FROM enrollments;
DELETE FROM students;
DELETE FROM courses;

-- Enable safe update mode again
SET SQL_SAFE_UPDATES = 1;


INSERT INTO students
(student_id, student_name, last_name, email, is_active)
VALUES
(1, 'John', 'Sanchez', 'JohnSanchez@gmail.com', 1),
(2, 'Pedro', 'Martin', 'PedroM@gmail.com', 1),
(3, 'Ethan', 'Lennox', 'EthanL@gmail.com', 0),
(4, 'Sal', 'Ami', 'SalAmi@gmail.com', 1),
(5, 'Pan', 'Largo', 'PanL@gmail.com', 1),
(6, 'Maria', 'Rodriguez', 'MariaR@gmail.com', 1),
(7, 'David', 'Johnson', 'DavidJ@gmail.com', 0),
(8, 'Sophia', 'Williams', 'SophiaW@gmail.com', 1),
(9, 'Lucas', 'Garcia', 'LucasG@gmail.com', 1),
(10, 'Emma', 'Brown', 'EmmaB@gmail.com', 1);

-- Verify
SELECT * FROM students;