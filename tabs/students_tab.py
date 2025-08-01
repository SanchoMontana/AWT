from dpg_utils import *
import dearpygui.dearpygui as dpg
from db.db_utils import *
from modals import add_new_student, delete_student, modify_student

# --- Global state to track the selected checkbox
student_id_checkbox_map = {"current": None}
notes_uuid = "student_tab_notes_footer"
modify_student_button_uuid = "modify_student_button"
delete_student_button_uuid = "delete_student_button"
student_tab_table_uuid = "student_tab_table"

def get_age_given_dob(dob):
    raise NotImplementedError

# Deselect the previously selected checkbox
def on_checkbox_selected(sender, app_data, user_data):
    global student_id_checkbox_map, notes_uuid
    cur = student_id_checkbox_map["current"]
    if cur and cur != sender:
        try:
            dpg.set_value(cur, False)
        except SystemError:
            # This will happen after the table updates due to modified or deleted students
            pass
    # Update the current selected
    if app_data == True:
        student_id_checkbox_map["current"] = sender
        id = student_id_checkbox_map[sender]
        cur_student = get_student_by_id(id)
        dpg.set_value(notes_uuid, cur_student["Notes"])
    else:
        student_id_checkbox_map["current"] = None
        cur_student = None
        dpg.set_value(notes_uuid, "")
    dpg.set_item_user_data(modify_student_button_uuid, {"student": cur_student, "update_fn": update_table})
    dpg.set_item_user_data(delete_student_button_uuid, {"student": cur_student, "update_fn": update_table})
    return


def update_table():
    global student_tab_table_uuid
    global student_id_checkbox_map
    dpg.delete_item(student_tab_table_uuid, children_only=True)
    headers = get_table_columns(STUDENT_TABLE_NAME)[:-1] # Ignore the notes section for now
    dpg.add_table_column(label="", parent=student_tab_table_uuid)
    for header in headers:
        dpg.add_table_column(label=header, parent=student_tab_table_uuid)
    student_id_checkbox_map = display_table_data(get_all_students(), student_tab_table_uuid, student_id_checkbox_map, cbcb=on_checkbox_selected)

def students_tab():
    headers = get_table_columns(STUDENT_TABLE_NAME)[:-1] # Ignore the notes section for now
    students = get_all_students()
    with dpg.tab(label="Students", tag="student_tab_header"):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Add New Student", callback=add_new_student.open_modal, user_data=update_table)
            dpg.add_button(label="Modify Student", callback=modify_student.open_modal, tag=modify_student_button_uuid)
            dpg.add_button(label="Delete Student", callback=delete_student.open_modal, tag=delete_student_button_uuid)
        with dpg.child_window(height=300, border=True, autosize_x=True):
            with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                        borders_innerH=True, borders_outerH=True, borders_innerV=True,
                        borders_outerV=True, scrollX=True, scrollY=True, tag=student_tab_table_uuid):
                update_table()
        dpg.add_text("Notes:")
        with dpg.child_window(border=True, autosize_x=True, autosize_y=False, height=50):
            dpg.add_text("This is a read-only message inside a styled box.", tag=notes_uuid)
