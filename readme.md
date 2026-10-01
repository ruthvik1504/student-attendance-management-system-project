# Student Attendance Management System

A web-based Student Attendance Management System built using Python, Flask, SQLite, HTML, CSS, and JavaScript.

## Features

- Secure admin login
- Password hashing
- Session-based authentication
- Student management
  - Add students
  - Edit students
  - Delete students
  - Search students by roll number or name
  - View student details
- Attendance management
  - Mark students Present/Absent
  - Prevent duplicate attendance for the same student and date
  - Update existing attendance records
- Attendance reports
- Filter attendance reports by date
- Export attendance records to CSV
- Individual student attendance percentage
- Dashboard statistics
  - Total students
  - Total attendance records
  - Present records
  - Absent records
- Form validation and error handling
- Responsive layout for smaller screens
- Delete confirmation
- Basic JavaScript interactions

## Tech Stack

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

### Security
- Werkzeug password hashing
- Session-based authentication
- Parameterized SQL queries

## Project Structure

```text
project-1/
│
├── app.py
├── init_db.py
├── requirements.txt
├── README.md
│
├── database/
│   └── attendance.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── templates/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── students.html
    ├── add_student.html
    ├── edit_student.html
    ├── attendance.html
    ├── attendance_report.html
    └── student_details.html

Installation
1. Clone the project
git clone <repository-url>
cd project-1
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment

Windows:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Initialize the database
python init_db.py
6. Run the application
python app.py

The application will run locally at:

http://127.0.0.1:5000
Default Login
Username: admin
Password: admin123

Change the default credentials before deploying the application publicly.

Database

The application uses SQLite for storing:

User accounts
Student information
Attendance records

The database file is located at:

database/attendance.db
Future Improvements

Possible future improvements include:

Multiple user roles
Teacher accounts
Admin panel
Course/subject-wise attendance
Monthly attendance reports
PDF report generation
Improved dashboard charts
Email notifications
Cloud database
Production deployment
REST API
Advanced authentication
Author

Built as a college software project.

License

This project is intended for educational and learning purposes.    