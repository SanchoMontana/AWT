import dearpygui.dearpygui as dpg
from global_uuids import DELETE_STUDENT_MODAL_UUID 
from db_utils import delete_student_by_id, get_student_by_id
from dpg_utils import *

def submit_delete_student_callback(sender, app_data, user_data):
    student = {"ID": user_data["student"]["ID"]}
    student["Name"] = dpg.get_value("student_name")
    student["DoB"] = dpg.get_value("student_dob")
    student["Email"] = dpg.get_value("student_email")
    student["Phone"] = dpg.get_value("student_phone")
    student["Notes"] = dpg.get_value("student_notes")
    delete_student_by_id(student["ID"])
    dpg.delete_item(DELETE_STUDENT_MODAL_UUID)
    user_data["update_fn"](user_data["cols"], user_data["rows"])
    return

def open_modal(sender, app_data, user_data):
    student = user_data["student"]
    if student == None:
        open_error_modal("Unable to delete... No Student selected")
        return

    if dpg.does_item_exist(DELETE_STUDENT_MODAL_UUID):
        dpg.delete_item(DELETE_STUDENT_MODAL_UUID)
    with dpg.window(label="Delete User", modal=True, tag=DELETE_STUDENT_MODAL_UUID, width=500, height=500, no_title_bar=False):
        dpg.add_text(f"Permanantly delete {student["Name"]}?")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Delete Student", callback=submit_delete_student_callback, user_data=user_data)
            dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item(DELETE_STUDENT_MODAL_UUID))

