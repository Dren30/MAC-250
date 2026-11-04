CREATE DATABASE IF NOT EXISTS classesDB;
use classesDB;
drop table if exists enrollments;
drop table if exists courses;
drop table if exists students;

Create table students (
	student_id int primary key,
	student_name varchar(20) not null,
	last_name varchar(20) not null,
	email varchar(50) unique not null,
	enrolled_since DATE default (CURRENT_DATE),
    is_active Boolean default TRUE
);

create table courses(
	course_id int primary key,
    course_name varchar(60) not null unique,
    credits int not null
);

create table enrollments(
    student_id int,
    course_id int,
    registered datetime not null,
	
    primary key(student_id, course_id),
    foreign key(course_id)  references courses(course_id),
	foreign key(student_id)  references students(student_id)
)