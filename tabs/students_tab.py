import dearpygui.dearpygui as dpg
import sqlite3

DB_PATH = "art_with_taylor.db"

def get_recent_students(limit=10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM Students ORDER BY student_id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def draw_students_tab():
    with dpg.tab(label="Students"):
        rows = get_recent_students()
        if not rows:
            dpg.add_text("No students found.")
            return

        headers = rows[0].keys()

        # Table for student list
        with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp):
            for h in headers:
                dpg.add_table_column(label=h)

            for row in rows:
                with dpg.table_row():
                    for val in row:
                        # Use selectable so we can detect clicks
                        dpg.add_selectable(label=str(val), callback=lambda s, a, u=row: show_student_details(u))

        # Details section below
        with dpg.child_window(height=150, border=True):
            dpg.add_text("Select a student to see details here", tag="student_details_text")

def show_student_details(student_row):
    # Clear previous details
    dpg.delete_item("student_details_text", children_only=True)
    # Update details
    details = "\n".join(f"{k}: {v}" for k, v in student_row.items())
    dpg.set_value("student_details_text", details)

