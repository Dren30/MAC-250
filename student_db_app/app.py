
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import IntegrityError

app = Flask(__name__)


# Establish a connection to the MySQL database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="...",
        database="classesDB"
    )


# Retrieve and display all students
@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("students.html", students=students)


# Add a new student to the database
@app.route("/insert", methods=["POST"])
def insert_student():
    student_id = request.form["student_id"]
    student_name = request.form["student_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]

    conn = get_connection()
    cursor = conn.cursor()

    # Check if the student ID or email already exists
    check_sql = """
        SELECT student_id, email
        FROM students
        WHERE student_id = %s OR email = %s
    """

    cursor.execute(check_sql, (student_id, email))
    existing_student = cursor.fetchone()

    # If the ID or email already exists
    if existing_student:
        cursor.close()
        conn.close()

        return """
            <script>
                alert("Unable to add student!\\n\\nThe Student ID or email already exists. Please try again.");
                window.location.href = "/";
            </script>
        """

    # Insert the new student
    sql = """
        INSERT INTO students
        (student_id, student_name, last_name, email)
        VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(
            sql,
            (student_id, student_name, last_name, email)
        )

        conn.commit()

    except IntegrityError:
        conn.rollback()

        cursor.close()
        conn.close()

        return """
            <script>
                alert("Something went wrong!\\n\\nThe student could not be added. Please check your information.");
                window.location.href = "/";
            </script>
        """

    cursor.close()
    conn.close()

    return redirect("/")





# Retrieve a student's information for editing
@app.route("/edit/<int:student_id>")
def edit_student(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE student_id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student is None:
        return "Student not found", 404

    return render_template("edit_student.html", student=student)


# Update an existing student's information
@app.route("/update", methods=["POST"])
def update_student():
    student_id = request.form["student_id"]
    student_name = request.form["student_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE students
        SET student_name = %s,
            last_name = %s,
            email = %s
        WHERE student_id = %s
    """

    cursor.execute(
        sql,
        (student_name, last_name, email, student_id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("index"))


# Delete a student from the database
@app.route("/delete", methods=["POST"])
def delete_student():
    student_id = request.form["student_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id = %s",
        (student_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

#----------------------------------------------------------

# Display all courses
@app.route("/courses")
def courses():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM courses"
    cursor.execute(sql)

    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("courses.html", courses=courses)



# Add a new course to the database
@app.route("/insert_course", methods=["POST"])
def insert_course():
    course_id = request.form["course_id"]
    course_name = request.form["course_name"]
    credits = request.form["credits"]

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether the course ID or name already exists
    check_sql = """
        SELECT course_id, course_name
        FROM courses
        WHERE course_id = %s OR course_name = %s
    """
    cursor.execute(check_sql, (course_id, course_name))
    existing_course = cursor.fetchone()

    if existing_course:
        cursor.close()
        conn.close()

        return """
            <script>
                alert("Unable to add course!\\n\\nThe Course ID or course name already exists.");
                window.location.href = "/courses";
            </script>
        """

    sql = """
        INSERT INTO courses (course_id, course_name, credits)
        VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (course_id, course_name, credits))
        conn.commit()

    except IntegrityError:
        conn.rollback()
        cursor.close()
        conn.close()

        return """
            <script>
                alert("The course could not be added. Please check your information.");
                window.location.href = "/courses";
            </script>
        """

    cursor.close()
    conn.close()

    return redirect(url_for("courses"))


# Display the edit course page
@app.route("/edit_course/<int:course_id>")
def edit_course(course_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM courses WHERE course_id = %s"
    cursor.execute(sql, (course_id,))
    course = cursor.fetchone()

    cursor.close()
    conn.close()

    if course is None:
        return redirect(url_for("courses"))

    return render_template("edit_course.html", course=course)


# Update an existing course
@app.route("/update_course", methods=["POST"])
def update_course():
    course_id = request.form["course_id"]
    course_name = request.form["course_name"]
    credits = request.form["credits"]

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether another course already uses this name
    check_sql = """
        SELECT course_id
        FROM courses
        WHERE course_name = %s AND course_id != %s
    """
    cursor.execute(check_sql, (course_name, course_id))
    existing_course = cursor.fetchone()

    if existing_course:
        cursor.close()
        conn.close()

        return f"""
            <script>
                alert("This course name is already being used by another course.");
                window.location.href = "/edit_course/{course_id}";
            </script>
        """

    sql = """
        UPDATE courses
        SET course_name = %s, credits = %s
        WHERE course_id = %s
    """

    try:
        cursor.execute(sql, (course_name, credits, course_id))
        conn.commit()

    except IntegrityError:
        conn.rollback()
        cursor.close()
        conn.close()

        return """
            <script>
                alert("The course could not be updated.");
                window.location.href = "/courses";
            </script>
        """

    cursor.close()
    conn.close()

    return redirect(url_for("courses"))


# Delete a course
@app.route("/delete_course", methods=["POST"])
def delete_course():
    course_id = request.form["course_id"]

    conn = get_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM courses WHERE course_id = %s"

    try:
        cursor.execute(sql, (course_id,))
        conn.commit()

    except IntegrityError:
        conn.rollback()
        cursor.close()
        conn.close()

        return f"""
            <script>
                alert("This course cannot be deleted because students are enrolled in it.");
                window.location.href = "/courses";
            </script>
        """

    cursor.close()
    conn.close()

    return redirect(url_for("courses"))

# -------------------------------------------------------

# Display all enrollments
@app.route("/enrollments")
def enrollments():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all students for the dropdown
    cursor.execute("""
        SELECT student_id, student_name, last_name
        FROM students
        ORDER BY student_id
    """)

    students = cursor.fetchall()

    # Get all courses for the dropdown
    cursor.execute("""
        SELECT course_id, course_name, credits
        FROM courses
        ORDER BY course_id
    """)

    courses = cursor.fetchall()

    # Get all enrollment relationships
    sql = """
        SELECT
            e.student_id,
            s.student_name,
            s.last_name,
            e.course_id,
            c.course_name,
            c.credits,
            e.registered
        FROM enrollments e
        INNER JOIN students s
            ON e.student_id = s.student_id
        INNER JOIN courses c
            ON e.course_id = c.course_id
        ORDER BY e.student_id ASC, e.course_id ASC
    """

    cursor.execute(sql)
    enrollments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "enrollments.html",
        students=students,
        courses=courses,
        enrollments=enrollments
    )


# Add a new enrollment
@app.route("/insert_enrollment", methods=["POST"])
def insert_enrollment():

    student_id = request.form["student_id"]
    course_id = request.form["course_id"]

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether this student is already enrolled in this course
    check_sql = """
        SELECT student_id, course_id
        FROM enrollments
        WHERE student_id = %s AND course_id = %s
    """

    cursor.execute(check_sql, (student_id, course_id))
    existing_enrollment = cursor.fetchone()

    if existing_enrollment:
        cursor.close()
        conn.close()

        return """
            <script>
                alert("This student is already enrolled in this course.");
                window.location.href = "/enrollments";
            </script>
        """

    # Insert the enrollment and record the current date and time
    sql = """
        INSERT INTO enrollments
        (student_id, course_id, registered)
        VALUES (%s, %s, NOW())
    """

    try:
        cursor.execute(sql, (student_id, course_id))
        conn.commit()

    except IntegrityError:
        conn.rollback()

        cursor.close()
        conn.close()

        return """
            <script>
                alert("The enrollment could not be added. Please check your information.");
                window.location.href = "/enrollments";
            </script>
        """

    cursor.close()
    conn.close()

    return redirect(url_for("enrollments"))


# Delete an enrollment
@app.route("/delete_enrollment", methods=["POST"])
def delete_enrollment():

    student_id = request.form["student_id"]
    course_id = request.form["course_id"]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        DELETE FROM enrollments
        WHERE student_id = %s AND course_id = %s
    """

    cursor.execute(sql, (student_id, course_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("enrollments"))

# ______________________________________________________________________________________

# Display all students, courses, and enrollments
@app.route("/show_all")
def show_all():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Retrieve all students
    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY student_id
    """)
    students = cursor.fetchall()

    # Retrieve all courses
    cursor.execute("""
        SELECT *
        FROM courses
        ORDER BY course_id
    """)
    courses = cursor.fetchall()

    # Retrieve all enrollment relationships
    cursor.execute("""
        SELECT
            e.student_id,
            s.student_name,
            s.last_name,
            e.course_id,
            c.course_name,
            c.credits,
            e.registered
        FROM enrollments e
        INNER JOIN students s
            ON e.student_id = s.student_id
        INNER JOIN courses c
            ON e.course_id = c.course_id
        ORDER BY e.student_id, e.course_id
    """)
    enrollments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "show_all.html",
        students=students,
        courses=courses,
        enrollments=enrollments
    )



# Run the Flask development server
if __name__ == "__main__":
    app.run(debug=True)
