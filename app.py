from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("students.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL,
                year INTEGER NOT NULL,
                phone TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    with get_db() as conn:
        if search:
            students = conn.execute("""
                SELECT * FROM students
                WHERE name LIKE ? OR email LIKE ? OR course LIKE ?
                ORDER BY id DESC
            """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
        else:
            students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
        total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        courses = conn.execute("SELECT COUNT(DISTINCT course) FROM students").fetchone()[0]
    return render_template("index.html", students=students, total=total, courses=courses, q=search)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        data = (
            request.form.get("name", "").strip(),
            request.form.get("email", "").strip().lower(),
            request.form.get("course", "").strip(),
            request.form.get("year", "").strip(),
            request.form.get("phone", "").strip()
        )
        if not all(data[:4]):
            flash("Please fill in all required fields.", "error")
            return render_template("form.html", student=None)
        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO students (name, email, course, year, phone) VALUES (?, ?, ?, ?, ?)",
                    (data[0], data[1], data[2], int(data[3]), data[4])
                )
            flash("Student added successfully.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("This email address is already registered.", "error")
        except ValueError:
            flash("Year must be a valid number.", "error")
    return render_template("form.html", student=None)

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with get_db() as conn:
        student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if student is None:
        flash("Student not found.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        course = request.form.get("course", "").strip()
        year = request.form.get("year", "").strip()
        phone = request.form.get("phone", "").strip()
        if not all([name, email, course, year]):
            flash("Please fill in all required fields.", "error")
            return render_template("form.html", student=student)
        try:
            with get_db() as conn:
                conn.execute("""
                    UPDATE students SET name=?, email=?, course=?, year=?, phone=?
                    WHERE id=?
                """, (name, email, course, int(year), phone, student_id))
            flash("Student details updated.", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("That email is already used by another student.", "error")
        except ValueError:
            flash("Year must be a valid number.", "error")
    return render_template("form.html", student=student)

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db() as conn:
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    flash("Student deleted.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
