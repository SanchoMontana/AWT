from operator import call
import dearpygui.dearpygui as dpg
import sqlite3

from db_utils import DB_NAME, get_table_columns

def display_table_data(rows, table_id, checkbox_ids, cbcb=None):
    try:
        cols = rows[0].keys()
    except IndexError:
        print("No items to display")
        return
    for row in rows:
        with dpg.table_row(parent=table_id):
            cb_id = dpg.generate_uuid()
            checkbox_ids[cb_id] = row["ID"]  # Map checkbox to row index
            dpg.add_checkbox(tag=cb_id, callback=cbcb)
            for col in cols:
                dpg.add_text(str(row[col]))
    return checkbox_ids


def open_error_modal(err_string):
    if dpg.does_item_exist("error_modal"):
        dpg.delete_item("error_modal")
    with dpg.window(label="Error", tag="error_modal", modal=True, width=400, height=300, no_title_bar=False):
        dpg.add_text("ERROR: " + err_string)


class Widget:
    def __init__(self, parent=None, tag=None, user_data=None, callback=None):
        self.parent = parent
        self.user_data = None
        self.callback=callback
        self.db_path = "art_with_taylor.db"
        self.tag = tag if tag else dpg.generate_uuid()
    def set_user_data(self, user_data):
        dpg.set_item_user_data(self.tag, user_data)
    def set_parent(self, parent):
        self.parent = parent

class Table(Widget):
    def __init__(self, table_name, n=0, **kwargs):
        super().__init__(**kwargs)
        self.db_table_name = table_name
        self.cols = []
        self.rows = []
        self.load_cols(exclude=[])
        self.load_rows(n=0)

    def load_cols(self, exclude=[]):
        self.cols = get_table_columns(self.db_path, self.db_table_name)
        for col in exclude:
            self.cols.remove(col)

    def load_rows(self, n=0):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if n != 0:
            query = "SELECT * FROM lessons ORDER BY ID DESC LIMIT ?"
            cur.execute("SELECT * FROM lessons ORDER BY ID DESC LIMIT ?", (n,))
        else: 
            query = "SELECT * FROM lessons ORDER BY ID DESC"
            cur.execute("SELECT * FROM lessons ORDER BY ID DESC")
        self.rows = cur.fetchall()
        conn.close()

    def load_table(self):
        if not self.rows:
            dpg.add_text("No lessons found.")
            return
        with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp, borders_innerH=True, borders_outerH=True, borders_innerV=True,
                 borders_outerV=True, scrollX=True, scrollY=True, parent=self.parent) as table:
            for col in self.cols:
                dpg.add_table_column(label=col)
            for row in self.rows:
                with dpg.table_row():
                    for data in row:
                        dpg.add_selectable(label=str(data))


class Button(Widget):
    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.load()
    
    def load(self):
        dpg.add_button(label=self.label, parent=self.parent, callback=self.callback, user_data=self.user_data)


class DataEntryModal(Widget):
    def __init__(self, title, width=500, height=500, **kwargs):
        super().__init__(**kwargs)
        self.fields = {}
        self.width = width
        self.height = height
        self.buttons = []

    def display_modal(self, text_box_width=200):
        max_field_length = 0
        for field in self.fields.keys():
            max_field_length = max(max_field_length, len(field))
        with dpg.window(label=self.title, modal=True, tag=self.tag, width=self.width, height=self.height, no_title_bar=False):
            for field_name, opts in self.fields:
                with dpg.group(horizontal=True):
                    if "default" in opts:
                        dpg.add_input_text(tag=field_name, default_value=opts["default"], width=text_box_width)
                    elif "hint" in opts:
                        dpg.add_input_text(tag=field_name, hint=opts["hint"], width=text_box_width)
                dpg.add_text(field_name.ljust(max_field_length + 2) + ":", **opts)
            for button_row in self.buttons:
                for button in button_row:
                    with dpg.group(horizontal=True):
                        button.load()


    def add_fields(self, *args):
        for field in args:
            if field not in self.fields.keys():
                self.fields[field] = {"default": None, "hint": None, "tag": dpg.generate_uuid()}
    
    def add_field_with_default(self, field, default):
        self.add_fields(field)
        self.fields[field]["default"]

    def add_field_with_hint(self, field, hint):
        self.add_fields(field)
        self.fields[field]["hint"] = hint

    def add_buttons(self, *args, horizontal=True):
        if horizontal:
            self.buttons.append(args)
        else:
            for arg in args:
                self.buttons.append([arg])


class SearchBar(Widget):
    def __init__(self, label, db_table, db_col, allow_multiple=True, **kwargs):
        super().__init__(**kwargs)
        self.label=label
        self.db_table = db_table
        self.db_col = db_col
        self.allow_multiple = allow_multiple
        self.search_input = None
        self.results_child = None
        self.search_callback = None
        self.selected_items = []
        self.input_text_tag = dpg.generate_uuid()
        self.search_results_group_tag = dpg.generate_uuid()
        self.search_results_tag = dpg.generate_uuid()
        self.locked_in_group_tag = dpg.generate_uuid()

    def load_search_bar(self):
        with dpg.group(tag=self.tag, parent=self.parent):
            with dpg.group():
                dpg.add_text(self.label)
                dpg.add_input_text(
                    tag=self.input_text_tag,
                    callback=self.search_populate_callback,
                    on_enter=False,
                    user_data=self
                )
            with dpg.group(tag=self.search_results_group_tag):
                pass
            with dpg.group(tag=self.locked_in_group_tag, horizontal=True):
                pass

    @staticmethod
    def search_populate_callback(sender, app_data, user_data):

        def set_value(s, a, val):
            dpg.add_text(val, parent=user_data.locked_in_group_tag)
            user_data.selected_items.append(val)
            dpg.set_value(user_data.input_text_tag, "")
            dpg.delete_item(user_data.search_results_tag)
            dpg.focus_item(user_data.input_text_tag)

        def make_window(buttons):
                with dpg.child_window(
                        tag=user_data.search_results_tag,
                        parent=user_data.search_results_group_tag,
                        autosize_x=True,
                        height=len(buttons) * 25 + 20,
                        border=True,
                        ):
                    for button in buttons:
                        dpg.add_button(
                            label=button,
                            parent=user_data.search_results_tag,
                            user_data=button,
                            callback=set_value)

        sql_query_str = f"SELECT {user_data.db_col} FROM {user_data.db_table} WHERE {user_data.db_col} LIKE ?"
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        query = app_data.strip()

        # Clear previous results
        if dpg.does_item_exist(user_data.search_results_tag):
            dpg.delete_item(user_data.search_results_tag)
        buttons = []
        if query:
            cursor.execute(sql_query_str, (f"%{query}%",))
            results = [row[0] for row in cursor.fetchall()]

            for name in results:
                if name not in user_data.selected_items:
                    buttons.append(name)
            make_window(buttons)
