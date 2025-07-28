import sqlite3

def create_database(db_name="art_with_taylor.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT,  -- Date of Birth (ISO: YYYY-MM-DD)
            email TEXT UNIQUE,
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

if __name__ == "__main__":
    create_database()
