"""
interface for building detailed sequences. 

related scratchpad...

"""
import dearpygui.dearpygui as dpg

def clamped_lighten(col_in: tuple[int], by: int):
    return tuple(c + by if c + by <= 255 else 255 for c in col_in)

TICK_PIXELS_W = 15
TICK_PIXELS_H = 25

class Segment:
    def __init__(self, color_idle= (0,150,200), tooltip_contents = "Placeholder.", n_ticks=1):
        self.color_idle = color_idle
        self.color_hover = clamped_lighten(color_idle, 15)
        self.color_active = clamped_lighten(color_idle, 25)
        self.tooltip_contents = tooltip_contents
        self.n_ticks = n_ticks

        with dpg.theme() as new_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.color_idle)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.color_hover)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.color_active)

                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)
        self.theme = new_theme
        self.button_ref = None
        self.button_cb = None

    def add_to_ui(self):
        ref = dpg.add_button(width=TICK_PIXELS_W*self.n_ticks, height=TICK_PIXELS_H, callback=self.button_cb)
        dpg.bind_item_theme(ref, self.theme)
        self.button_ref = ref
        with dpg.tooltip(parent=ref):
            dpg.add_text(self.tooltip_contents)


class SegmentContainer:

    def __init__(self, *args):
        with dpg.theme() as new_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0)
        self.theme = new_theme

        self.segments = []
        for seg in args:
            self.segments.append(seg)
            seg.button_cb = self.parent_cb

        self.infobox_ref = None
        self.focused = None

    def parent_cb(self, *args):
        print(a for a in args)
        dpg.configure_item(self.infobox_ref, show=True)

    def add_to_ui(self):
        with dpg.child_window(width=300, height=150, show=False) as infobox:
            with dpg.group(horizontal=True):
                dpg.add_text("Customizing Action: ")
                dpg.add_text("", tag="info_param_action_name")
            with dpg.group(horizontal=True):
                dpg.add_text("Some quantity: ")
                dpg.add_text("", tag="info_param_frames")
            dpg.add_knob_float(label="Jump Angle")
        with dpg.child_window(width=300, height=55, resizable_x=True, horizontal_scrollbar=True):
            with dpg.group(horizontal=True) as groupref:
                for seg in self.segments:
                    seg.add_to_ui()
            self.groupref = groupref
            dpg.bind_item_theme(groupref, self.theme)
        self.infobox_ref = infobox

    def add(self):
        ...

    def remove(self):
        ...

    def set_focus(self, seg):
        dpg.configure_item(self.infobox_ref, show=True)


def layout():

    s1 = Segment((198, 98, 23), "F1", 5)
    s2 = Segment(n_ticks=12)
    s3 = Segment((100, 225, 44), "action 3", 7)
    scont = SegmentContainer(s1, s2, s3)

    dpg.add_button(label="Add a random action", callback=scont.add)
    dpg.add_button(label="Remove selected action", show=False, callback=scont.remove, tag="btn_remove")

    scont.add_to_ui()


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
