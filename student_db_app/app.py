
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

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

    return render_template("index.html", students=students)


# Add a new student to the database
@app.route("/insert", methods=["POST"])
def insert_student():
    student_id = request.form["student_id"]
    student_name = request.form["student_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO students
        (student_id, student_name, last_name, email)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (student_id, student_name, last_name, email)
    )

    conn.commit()

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

    return render_template("edit.html", student=student)


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


# Run the Flask development server
if __name__ == "__main__":
    app.run(debug=True)
