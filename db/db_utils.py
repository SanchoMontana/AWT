import sqlite3
DB_NAME = "art_with_taylor.db"
STUDENT_TABLE_NAME = "Students"
LESSON_TABLE_NAME = "Lessons"
LESSON_ATTENDANCE_TABLE_NAME = "LessonAttendance"
HOMEWORK_TABLE_NAME ="Homework"



def init_db(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            DoB TEXT,  -- Date of Birth (ISO: YYYY-MM-DD)
            Email TEXT,
            Phone TEXT,
            Notes TEXT
        );
    """)

    # Lessons Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Lessons (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT NOT NULL,  -- ISO format (YYYY-MM-DD)
            Notes TEXT
        );
    """)

    # Lesson Attendance Table (per student, per lesson)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS LessonAttendance (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Lesson INTEGER NOT NULL,
            Student INTEGER NOT NULL,
            Instructions TEXT,  -- Individual instructions given
            Photo TEXT,  -- File path or URL
            FOREIGN KEY (lesson) REFERENCES Lessons(ID),
            FOREIGN KEY (student) REFERENCES Students(ID)
        );
    """)

    # Homework Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Homework (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date_Assigned INTEGER NOT NULL,
            Student INTEGER NOT NULL,
            Homework_description TEXT NOT NULL,
            Date_Completed INTEGER,  -- Null until completed
            Feedback TEXT,  -- Optional notes on completed work
            FOREIGN KEY (Date_Assigned) REFERENCES Lessons(lesson_id),
            FOREIGN KEY (Date_Completed) REFERENCES Lessons(lesson_id),
            FOREIGN KEY (Student) REFERENCES Students(student_id)
        );
    """)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created successfully.")

def get_all_students():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students ORDER BY ID")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_student_by_id(id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students where ID = ?", (id,))
    row = cur.fetchone()
    conn.close()
    return row

def modify_student(sd):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Students
        SET Name = ?,
        Dob = ?,
        Email = ?,
        Phone = ?,
        Notes = ?
        WHERE id = ?
    """, (sd["Name"], sd["DoB"], sd["Email"], sd["Phone"], sd["Notes"], sd["ID"],))

    conn.commit()
    conn.close()

import sqlite3

def delete_student_by_id(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Students WHERE id = ?", (id,))

    conn.commit()
    conn.close()


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

def get_table_columns(table_name):
    """
    Returns a list of (column_name, column_type) for the given table.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        return [col[1] for col in columns]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []
    finally:
        conn.close()
