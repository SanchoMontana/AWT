import dearpygui.dearpygui as dpg

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
