# ClassesDB – Student Management System

## Project Description

ClassesDB is a Student Management System developed using Python, Flask, MySQL, HTML, and CSS.

The application allows users to manage students, courses, and student enrollments through an interactive web interface.

## Features

- **Students:** Add, view, edit, and delete student records.
- **Courses:** Add, view, edit, and delete course records.
- **Enrollments:** Register students for courses and remove enrollment relationships.
- **Show All:** Display all students, courses, and enrollment records in one place.
- **Database Relationships:** Uses primary keys, foreign keys, and a composite primary key to manage relationships between tables.

## Technologies Used

- Python
- Flask
- MySQL
- MySQL Connector/Python
- HTML
- CSS

## Project Structure

```text
student_db_app/
│
├── app.py
├── README.md
├── requirements.txt
│
├── database/
│   ├── tables_creation.sql
│   └── db_seeds.sql
│
└── templates/
    ├── students.html
    ├── edit_student.html
    ├── courses.html
    ├── edit_course.html
    ├── enrollments.html
    └── show_all.html
```

## Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3
- MySQL Server
- MySQL Workbench (or another MySQL client)
- Git

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/Dren30/MAC-250/tree/main/student_db_app
cd student_db_app
```

### 2. Create the MySQL Database

Open MySQL Workbench or another MySQL client and execute the following SQL files in order:

1. `database/tables_creation.sql` – Creates the `classesDB` database and its three tables: students, courses, and enrollments.
2. `database/db_seeds.sql` – Inserts the sample students, courses, and enrollment records.

**Note:** The `tables_creation.sql` script drops and recreates the existing tables. The `db_seeds.sql` script deletes existing records before inserting the sample data. Running these scripts again will reset the database.

### 3. Configure the Database Connection

Open `app.py` and locate the `get_connection()` function.

Update the MySQL connection settings to match your local MySQL configuration:

```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",
        password="your_mysql_password",
        database="classesDB"
    )
```

Replace `your_mysql_username` and `your_mysql_password` with your own MySQL credentials.

**Note:** The database name should remain `classesDB` unless you change it in the SQL scripts as well.

### 4. Install Python Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This installs the Python packages required to run the application.

### 5. Run the Application

After creating the database and configuring the MySQL connection, start the Flask application:

```bash
python app.py
```

Open your web browser and navigate to:

http://127.0.0.1:5000

The ClassesDB Student Management System should now be running.

---

## Database Tables

The project uses three tables:

- **students:** Stores student information, including student ID, name, email, enrollment date, and active status.
- **courses:** Stores available courses, including course ID, course name, and credits.
- **enrollments:** Junction table connecting students and courses through a many-to-many relationship.

The `enrollments` table uses a composite primary key consisting of `student_id` and `course_id` to prevent duplicate student-course enrollments.