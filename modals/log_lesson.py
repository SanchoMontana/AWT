import dearpygui.dearpygui as dpg
import datetime
from db_utils import get_all_students, insert_full_lesson_record
from modals import add_new_student

# Submit button
def submit_new_lesson_callback():
    date = dpg.get_value("lesson_date")
    homework = dpg.get_value("homework_text")
    attendees = [sid for sid, tag in student_id if dpg.get_value(tag)]

    insert_full_lesson_record(date, attendees, homework)
    dpg.delete_item("log_lesson_modal")


def open_log_lesson_modal():
    if dpg.does_item_exist("log_lesson_modal"):
        dpg.delete_item("log_lesson_modal")

    with dpg.window(label="Log New Lesson", modal=True, tag="log_lesson_modal", width=600, height=600, no_title_bar=False):
        # Date input
        dpg.add_input_text(label="Date (YYYY-MM-DD)", default_value=str(datetime.date.today()), tag="lesson_date")

        # Attendees
        dpg.add_text("Select Attending Students:")
        student_ids = []
        with dpg.child_window(height=120):
            for student in get_all_students():
                sid = f"student_{student[0]}"
                dpg.add_checkbox(label=f"{student[1]} (ID: {student[0]})", tag=sid)
                student_ids.append((student[0], sid))
        dpg.add_spacer(height=10)
        # Homework assigned
        dpg.add_input_text(label="Homework Description", multiline=True, tag="homework_text")

        dpg.add_spacer(height=10)
        dpg.add_button(label="Submit Lesson", callback=submit_new_lesson_callback)
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("log_lesson_modal"))

