import dearpygui.dearpygui as dpg

from gruvbox_theme import apply_gruvbox_theme
from db_utils import init_db
from tabs.students_tab import draw_students_tab
from tabs.lessons_tab import draw_lessons_tab
from tabs.homework_tab import draw_homework_tab
from modals.log_lesson import open_log_lesson_modal
from modals.add_new_student import open_add_new_student_modal

# Initialize DB (only needed once at app start)
init_db()

dpg.create_context()
apply_gruvbox_theme()

dpg.create_viewport(title="🎨 Art Lesson Manager", width=1200, height=800)
dpg.setup_dearpygui()

with dpg.window(label="Main", width=1200, height=800):
    # Add log button
    with dpg.group(horizontal=True):
        dpg.add_button(label="Log Lesson", callback=open_log_lesson_modal)
        dpg.add_button(label="Add New Student", callback=open_add_new_student_modal)
    dpg.add_separator()

    # Tabbed views
    with dpg.tab_bar():
        draw_students_tab()
        draw_lessons_tab()
        draw_homework_tab()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
