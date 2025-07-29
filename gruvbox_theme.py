# gruvbox_theme.py
import dearpygui.dearpygui as dpg

def apply_gruvbox_theme():
    with dpg.theme() as gruvbox_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (40, 40, 40), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (40, 40, 40), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (30, 30, 30), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 56, 54), category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Text, (235, 219, 178), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (146, 131, 116), category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 56, 54), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (146, 131, 116), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (214, 93, 14), category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 48, 47), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (146, 131, 116), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (214, 93, 14), category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Tab, (60, 56, 54), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (214, 93, 14), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (214, 93, 14), category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 56, 54), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (146, 131, 116), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (214, 93, 14), category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (40, 40, 40), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (50, 48, 47), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (60, 56, 54), category=dpg.mvThemeCat_Core)

    dpg.bind_theme(gruvbox_theme)

