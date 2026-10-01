from flask import Flask, render_template, request, redirect, url_for, session, Response
from werkzeug.security import check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "attendance-management-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database", "attendance.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
    """
    SELECT * FROM users
    WHERE username = ?
    """,
    (username,)
).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    student_count = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    attendance_count = conn.execute(
        "SELECT COUNT(*) FROM attendance"
    ).fetchone()[0]

    present_count = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE status = 'Present'"
    ).fetchone()[0]

    absent_count = conn.execute(
        "SELECT COUNT(*) FROM attendance WHERE status = 'Absent'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        student_count=student_count,
        attendance_count=attendance_count,
        present_count=present_count,
        absent_count=absent_count
    )

@app.route("/students")
def students():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    search = request.args.get("search", "")

    students = conn.execute(
        """
        SELECT * FROM students
        WHERE roll_no LIKE ?
        OR name LIKE ?
        """,
        (f"%{search}%", f"%{search}%")
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students,
        search=search
    )

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        roll_no = request.form["roll_no"]
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        branch = request.form["branch"]

        conn = get_db()

        existing_student = conn.execute(
            """
            SELECT id
            FROM students
            WHERE roll_no = ?
            """,
            (roll_no,)
        ).fetchone()

        if existing_student:
            conn.close()

            return render_template(
                "add_student.html",
                error="Roll number already exists."
            )

        conn.execute(
            """
            INSERT INTO students
            (roll_no, name, email, course, branch)
            VALUES (?, ?, ?, ?, ?)
            """,
            (roll_no, name, email, course, branch)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    return render_template("add_student.html")

@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    if request.method == "POST":

        roll_no = request.form["roll_no"]
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        branch = request.form["branch"]

        existing_student = conn.execute(
            """
            SELECT id
            FROM students
            WHERE roll_no = ?
            AND id != ?
            """,
            (roll_no, id)
        ).fetchone()

        if existing_student:
            student = conn.execute(
                "SELECT * FROM students WHERE id = ?",
                (id,)
            ).fetchone()

            conn.close()

            return render_template(
                "edit_student.html",
                student=student,
                error="Roll number already exists."
            )

        conn.execute(
            """
            UPDATE students
            SET roll_no = ?, name = ?, email = ?, course = ?, branch = ?
            WHERE id = ?
            """,
            (roll_no, name, email, course, branch, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )

@app.route("/delete_student/<int:id>")
def delete_student(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    conn.execute(
        "DELETE FROM attendance WHERE student_id = ?",
        (id,)
    )

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("students"))

@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students ORDER BY roll_no"
    ).fetchall()

    if request.method == "POST":

        attendance_date = request.form["attendance_date"]

        for student in students:

            status = request.form[
                f"status_{student['id']}"
            ]

            existing_record = conn.execute(
                """
                SELECT id
                FROM attendance
                WHERE student_id = ?
                AND attendance_date = ?
                """,
                (
                    student["id"],
                    attendance_date
                )
            ).fetchone()

            if existing_record:

                conn.execute(
                    """
                    UPDATE attendance
                    SET status = ?
                    WHERE id = ?
                    """,
                    (
                        status,
                        existing_record["id"]
                    )
                )

            else:

                conn.execute(
                    """
                    INSERT INTO attendance
                    (student_id, attendance_date, status)
                    VALUES (?, ?, ?)
                    """,
                    (
                        student["id"],
                        attendance_date,
                        status
                    )
                )

        conn.commit()
        conn.close()

        return redirect(url_for("attendance"))

    conn.close()

    return render_template(
        "attendance.html",
        students=students
    )

@app.route("/attendance_report")
def attendance_report():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    selected_date = request.args.get("date", "")

    if selected_date:

        attendance_records = conn.execute(
            """
            SELECT
                attendance.attendance_date,
                students.roll_no,
                students.name,
                attendance.status
            FROM attendance
            JOIN students
            ON attendance.student_id = students.id
            WHERE attendance.attendance_date = ?
            ORDER BY students.roll_no
            """,
            (selected_date,)
        ).fetchall()

    else:

        attendance_records = conn.execute(
            """
            SELECT
                attendance.attendance_date,
                students.roll_no,
                students.name,
                attendance.status
            FROM attendance
            JOIN students
            ON attendance.student_id = students.id
            ORDER BY attendance.attendance_date DESC
            """
        ).fetchall()

    conn.close()

    return render_template(
        "attendance_report.html",
        attendance_records=attendance_records,
        selected_date=selected_date
    )

@app.route("/export_attendance")
def export_attendance():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    attendance_records = conn.execute(
        """
        SELECT
            attendance.attendance_date,
            students.roll_no,
            students.name,
            attendance.status
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        ORDER BY attendance.attendance_date DESC
        """
    ).fetchall()

    conn.close()

    csv_data = "Date,Roll No,Name,Status\n"

    for record in attendance_records:
        csv_data += (
            f"{record['attendance_date']},"
            f"{record['roll_no']},"
            f"{record['name']},"
            f"{record['status']}\n"
        )

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=attendance_report.csv"
        }
    )

@app.route("/student/<int:id>")
def student_details(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    attendance = conn.execute(
        """
        SELECT status
        FROM attendance
        WHERE student_id = ?
        """,
        (id,)
    ).fetchall()

    conn.close()

    total_classes = len(attendance)

    present_classes = sum(
        1 for record in attendance
        if record["status"] == "Present"
    )

    absent_classes = total_classes - present_classes

    if total_classes > 0:
        attendance_percentage = round(
            (present_classes / total_classes) * 100,
            2
        )
    else:
        attendance_percentage = 0

    return render_template(
        "student_details.html",
        student=student,
        total_classes=total_classes,
        present_classes=present_classes,
        absent_classes=absent_classes,
        attendance_percentage=attendance_percentage
    )

if __name__ == "__main__":
    app.run(debug=True)
    