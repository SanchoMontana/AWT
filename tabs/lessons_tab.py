import dearpygui.dearpygui as dpg
from dpg_utils import *
from datetime import datetime

def lessons_tab():
    with dpg.tab(label="Log Lesson") as log_lesson_tab:
        student_selection = SearchBar("Add to lesson attendance:", "Students", "Name")
        student_selection.set_parent(log_lesson_tab)
        student_selection.load_search_bar()
