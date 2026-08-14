"""
interface for building detailed sequences. 
we'll see what we can do with DPG, and if it's too restrictive, investigate smth else.
"""
import dearpygui.dearpygui as dpg

def clamped_lighten(col_in: tuple[int], by: int):
    return tuple(c + by if c + by <= 255 else 255 for c in col_in)

class Segment:
    def __init__(self, color_idle= (0,150,200), tooltip_contents = "Placeholder.", width=25):
        self.color_idle = color_idle
        self.color_hover = clamped_lighten(color_idle, 15)
        self.color_active = clamped_lighten(color_idle, 25)
        self.tooltip_contents = tooltip_contents
        self.width = width

        with dpg.theme() as new_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.color_idle)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.color_hover)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.color_active)

                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0)
        self.theme = new_theme

    def add_to_ui(self):
        self._button_ref = dpg.add_button(width=self.width, height=25)
        dpg.bind_item_theme(dpg.last_item(), self.theme)
        with dpg.tooltip(self._button_ref):
            dpg.add_text(self.tooltip_contents)


def layout():
    s1 = Segment((198, 98, 23), "F1", 75)
    s2 = Segment()
    s3 = Segment()
    with dpg.group(horizontal=True):
        s1.add_to_ui()
        s2.add_to_ui()
        s3.add_to_ui()


if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()
    dpg.show_viewport()

    with dpg.window():
        layout()
    dpg.start_dearpygui()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
    dpg.stop_dearpygui()
