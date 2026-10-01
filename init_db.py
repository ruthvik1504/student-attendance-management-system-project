import sqlite3
import os
from werkzeug.security import generate_password_hash

# Make sure the database folder exists
os.makedirs("database", exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect("database/attendance.db")

cursor = conn.cursor()

# Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    course TEXT,
    branch TEXT
)
""")

# Attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    attendance_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create default admin user
cursor.execute("""
INSERT OR IGNORE INTO users (username, password)
VALUES (?, ?)
""", ("admin", generate_password_hash("admin123")))

# Save changes
conn.commit()

# Close database connection
conn.close()

print("Database created successfully!")