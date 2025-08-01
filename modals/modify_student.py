import dearpygui.dearpygui as dpg
from db.db_utils import modify_student, get_student_by_id
from dpg_utils import *

MODIFY_STUDENT_MODAL_TAG= "modify_student_modal"
def submit_modify_student_callback(sender, app_data, user_data):
    student = {"ID": user_data["student"]["ID"]}
    student["Name"] = dpg.get_value("student_name")
    student["DoB"] = dpg.get_value("student_dob")
    student["Email"] = dpg.get_value("student_email")
    student["Phone"] = dpg.get_value("student_phone")
    student["Notes"] = dpg.get_value("student_notes")
    modify_student(student)
    dpg.delete_item(MODIFY_STUDENT_MODAL_TAG)
    user_data["update_fn"](user_data["cols"], user_data["rows"])
    return

def open_modal(sender, app_data, user_data):
    student = user_data["student"]
    if student == None:
        open_error_modal("Unable to modify... No Student selected")
        return

    if dpg.does_item_exist(MODIFY_STUDENT_MODAL_TAG):
        dpg.delete_item(MODIFY_STUDENT_MODAL_TAG)
    with dpg.window(label="Modify User", modal=True, tag=MODIFY_STUDENT_MODAL_TAG, width=500, height=500, no_title_bar=False):
        with dpg.group(horizontal=True):
            dpg.add_text("Name:".ljust(15))
            dpg.add_input_text(default_value=student["Name"], tag="student_name")
        with dpg.group(horizontal=True):
            dpg.add_text("DoB:".ljust(15))
            dpg.add_input_text(default_value=student["DoB"], tag="student_dob")
        with dpg.group(horizontal=True):
            dpg.add_text("Email:".ljust(15))
            dpg.add_input_text(default_value=student["Email"], tag="student_email")
        with dpg.group(horizontal=True):
            dpg.add_text("Phone Number:".ljust(15))
            dpg.add_input_text(default_value=student["Phone"], tag="student_phone")
        dpg.add_text("Notes:".ljust(15))
        dpg.add_input_text(default_value=student["Notes"], tag="student_notes")

        dpg.add_spacer(height=10)
        dpg.add_button(label="Modify Student", callback=submit_modify_student_callback, user_data=user_data)
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item(MODIFY_STUDENT_MODAL_TAG))

