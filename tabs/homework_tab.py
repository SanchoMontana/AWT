import dearpygui.dearpygui as dpg
import sqlite3

DB_PATH = "art_with_taylor.db"

def get_recent_homework(limit=10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM homework ORDER BY homework_id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def draw_homework_tab():
    with dpg.tab(label="Homework"):
        rows = get_recent_homework()
        if not rows:
            dpg.add_text("No homework entries found.")
            return

        headers = rows[0].keys()

        with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp):
            for h in headers:
                dpg.add_table_column(label=h)

            for row in rows:
                with dpg.table_row():
                    for val in row:
                        dpg.add_selectable(label=str(val), callback=lambda s, a, u=row: show_homework_details(u))

        with dpg.child_window(height=150, border=True):
            dpg.add_text("Select homework to see details here", tag="homework_details_text")

def show_homework_details(hw_row):
    dpg.delete_item("homework_details_text", children_only=True)
    details = "\n".join(f"{k}: {v}" for k, v in hw_row.items())
    dpg.set_value("homework_details_text", details)

