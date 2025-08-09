#!/usr/bin/python3

import dearpygui.dearpygui as dpg

dpg.create_context()

# from fonts.font_init import *
from gruvbox_theme import apply_gruvbox_theme
from db_utils import init_db
from tabs.students_tab import students_tab
from tabs.lessons_tab import lessons_tab
from modals.log_lesson import open_log_lesson_modal
from modals import add_new_student

# Initialize DB (only needed once at app start)
init_db()

apply_gruvbox_theme()

dpg.create_viewport(title="🎨 Art Lesson Manager", width=1200, height=800)
dpg.setup_dearpygui()

with dpg.window(label="Main", width=1200, height=800):
    with dpg.tab_bar():
        pass
        # students_tab()
        lessons_tab()
        #homework_tab()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
