import dearpygui.dearpygui as dpg
from db_utils import insert_new_student

ADD_NEW_STUDENT_MODAL_TAG= "add_new_student_modal"
def submit_new_student_callback():
    name = dpg.get_value("student_name")
    dob = dpg.get_value("student_dob")
    email = dpg.get_value("student_email")
    phone = dpg.get_value("student_phone")
    notes = dpg.get_value("student_notes")
    insert_new_student(name, dob, email, phone, notes)
    dpg.delete_item(ADD_NEW_STUDENT_MODAL_TAG)
    return

def open_add_new_student_modal():
    if dpg.does_item_exist(ADD_NEW_STUDENT_MODAL_TAG):
        dpg.delete_item(ADD_NEW_STUDENT_MODAL_TAG)
    with dpg.window(label="Add New User", modal=True, tag=ADD_NEW_STUDENT_MODAL_TAG, width=500, height=500, no_title_bar=False):
        with dpg.group(horizontal=True):
            dpg.add_text("Name:".ljust(15))
            dpg.add_input_text(label=None, tag="student_name", hint="John Doe")
        with dpg.group(horizontal=True):
            dpg.add_text("DoB:".ljust(15))
            dpg.add_input_text(label=None, tag="student_dob", hint="YYYY-MM-DD")
        with dpg.group(horizontal=True):
            dpg.add_text("Email:".ljust(15))
            dpg.add_input_text(label=None, tag="student_email", hint="john.doe@gmail.com")
        with dpg.group(horizontal=True):
            dpg.add_text("Phone Number:".ljust(15))
            dpg.add_input_text(label=None, tag="student_phone", hint="513-555-5555")
        dpg.add_text("Notes:".ljust(15))
        dpg.add_input_text(label=None, tag="student_notes")

        dpg.add_spacer(height=10)
        dpg.add_button(label="Add Student", callback=submit_new_student_callback)
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item(ADD_NEW_STUDENT_MODAL_TAG))

