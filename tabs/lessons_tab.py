import dearpygui.dearpygui as dpg
import sqlite3

DB_PATH = "art_with_taylor.db"

def get_recent_lessons(limit=10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM lessons ORDER BY lesson_id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def lessons_tab():
    with dpg.tab(label="Lessons"):
        rows = get_recent_lessons()
        if not rows:
            dpg.add_text("No lessons found.")
            return

        headers = rows[0].keys()

        with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp):
            for h in headers:
                dpg.add_table_column(label=h)

            for row in rows:
                with dpg.table_row():
                    for val in row:
                        dpg.add_selectable(label=str(val), callback=lambda s, a, u=row: show_lesson_details(u))

        with dpg.child_window(height=150, border=True):
            dpg.add_text("Select a lesson to see details here", tag="lesson_details_text")

def show_lesson_details(lesson_row):
    dpg.delete_item("lesson_details_text", children_only=True)
    details = "\n".join(f"{k}: {v}" for k, v in lesson_row.items())
    dpg.set_value("lesson_details_text", details)

