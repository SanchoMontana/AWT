import sqlite3
DB_NAME = "art_with_taylor.db"

def init_db(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT,  -- Date of Birth (ISO: YYYY-MM-DD)
            email TEXT,
            phone, TEXT,
            notes TEXT
        );
    """)

    # Lessons Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Lessons (
            lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,  -- ISO format (YYYY-MM-DD)
            general_notes TEXT
        );
    """)

    # Lesson Attendance Table (per student, per lesson)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS LessonAttendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            directions TEXT,  -- Individual instructions given
            activity_description TEXT,
            photo_path TEXT,  -- File path or URL
            FOREIGN KEY (lesson_id) REFERENCES Lessons(lesson_id),
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        );
    """)

    # Homework Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Homework (
            homework_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assigned_in_lesson_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            homework_description TEXT NOT NULL,
            completed_in_lesson_id INTEGER,  -- Null until completed
            feedback TEXT,  -- Optional notes on completed work
            FOREIGN KEY (assigned_in_lesson_id) REFERENCES Lessons(lesson_id),
            FOREIGN KEY (completed_in_lesson_id) REFERENCES Lessons(lesson_id),
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        );
    """)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created successfully.")


def get_all_students():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT student_id, name FROM Students")
    students = cur.fetchall()
    conn.close()
    return students

def insert_full_lesson_record(date_str, student_ids, homework_text):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Insert lesson
    cur.execute("INSERT INTO lessons (date) VALUES (?)", (date_str,))
    lesson_id = cur.lastrowid

    # Insert lesson-student notes (blank by default)
    for student_id in student_ids:
        cur.execute("""
            INSERT INTO lesson_student_notes (lesson_id, student_id, notes, image_path)
            VALUES (?, ?, ?, ?)""", (lesson_id, student_id, "", None))

    # Insert homework if any
    if homework_text.strip():
        cur.execute("""
            INSERT INTO homework (lesson_id, description)
            VALUES (?, ?)""", (lesson_id, homework_text.strip()))

    conn.commit()
    conn.close()

def insert_new_student(name, dob, email, phone, notes):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Insert lesson
    cur.execute("INSERT INTO Students (name, dob, email, phone, notes) VALUES (?, ?, ?, ?, ?)",
                (name, dob,email, phone, notes))

    conn.commit()
    conn.close()
