from dpg_utils import *
from global_uuids import *
import dearpygui.dearpygui as dpg
from db.db_utils import *
from global_uuids import STUDENT_TAB_NOTES_UUID
from global_uuids import ADD_STUDENT_BUTTON_UUID
from modals import add_new_student, delete_student, modify_student

# --- Global state to track the selected checkbox
student_id_checkbox_map = {"current": None}
headers = get_table_columns(STUDENT_TABLE_NAME)[:-1] # Ignore the notes section for now
students = get_all_students()


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
        dpg.set_value(STUDENT_TAB_NOTES_UUID, cur_student["Notes"])
    else:
        student_id_checkbox_map["current"] = None
        cur_student = None
        dpg.set_value(STUDENT_TAB_NOTES_UUID, "")

    ud_set = {"student": cur_student, "update_fn": create_table, "cols": headers, "rows": students}
    dpg.set_item_user_data(MODIFY_STUDENT_BUTTON_UUID, ud_set)
    dpg.set_item_user_data(DELETE_STUDENT_BUTTON_UUID, ud_set)
    return

def create_table(cols, rows, parent=None):
    global student_id_checkbox_map
    parent=STUDENT_TAB_TABLE_CHILD_WINDOW_UUID
    dpg.set_item_user_data(MODIFY_STUDENT_BUTTON_UUID, {"student": None, "update_fn": create_table})
    dpg.set_item_user_data(DELETE_STUDENT_BUTTON_UUID, {"student": None, "update_fn": create_table})
    if dpg.does_item_exist(parent):
        dpg.delete_item(parent, children_only=True)
    with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp, borders_innerH=True, borders_outerH=True, borders_innerV=True,
                 borders_outerV=True, scrollX=True, scrollY=True, parent=parent) as table:
        dpg.add_table_column(label="")
        for col in cols:
            dpg.add_table_column(label=col)
        student_id_checkbox_map = display_table_data(get_all_students(), table, student_id_checkbox_map, cbcb=on_checkbox_selected)
    if dpg.does_item_exist(STUDENT_TAB_NOTES_CHILD_WINDOW_UUID):
        create_notes_widget() # This is sloppy, but i dont want to do it right.
        dpg.set_value(STUDENT_TAB_NOTES_UUID, "")

def create_notes_widget():
    parent=STUDENT_TAB_NOTES_CHILD_WINDOW_UUID
    if dpg.does_item_exist(parent):
        dpg.delete_item(parent, children_only=True)
    dpg.add_text("Notes:", parent=parent)
    with dpg.child_window(height=100, autosize_x=True, border=True, parent=parent):
        dpg.add_text(tag=STUDENT_TAB_NOTES_UUID)


def students_tab():
    with dpg.tab(label="Students", tag=STUDENT_TAB_UUID):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Add Student", callback=add_new_student.open_modal, tag=ADD_STUDENT_BUTTON_UUID, user_data={"update_fn": create_table, "cols": headers, "rows": students})
            dpg.add_button(label="Modify Student", callback=modify_student.open_modal, tag=MODIFY_STUDENT_BUTTON_UUID, user_data={"student": None, "udpate_fn": create_table})
            dpg.add_button(label="Delete Student", callback=delete_student.open_modal, tag=DELETE_STUDENT_BUTTON_UUID, user_data={"student": None, "udpate_fn": create_table})
        with dpg.child_window(height=300, autosize_x=True, border=False, tag=STUDENT_TAB_TABLE_CHILD_WINDOW_UUID):
            create_table(headers, students, parent=STUDENT_TAB_TABLE_CHILD_WINDOW_UUID)
        with dpg.child_window(height=100, autosize_x=True,border=False, tag=STUDENT_TAB_NOTES_CHILD_WINDOW_UUID):
            create_notes_widget()
