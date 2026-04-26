import dearpygui.dearpygui as dpg
from melee.enums import Stage, Character

from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation
from .solver import PayoffSolver

from mess.animations.vis import lerp_2d
from mess.animations._rs import dump_one_character


def ptool_setup_window():

    with dpg.window(tag="win"):
        dpg.add_spacer(tag="host_dummy")
        dpg.add_spacer(tag="solver_dummy")

        stages = [f"{e.name}({e.value})" for e in Stage]
        chars = [f"{c.name}({c.value})" for c in Character]
        dpg.add_combo(items=stages, label="Stage", tag="stg", default_value=stages[1])
        dpg.add_combo(items=chars, label="P1 Char", tag="p1c", default_value=chars[1])
        dpg.add_slider_float(label="P1 Percent", tag="p1p", max_value=300)
        dpg.add_combo(items=chars, label="P2 Char", tag="p2c", default_value=chars[22])
        dpg.add_slider_float(label="P2 Percent", tag="p2p", max_value=300)

        dpg.add_separator()
        dpg.add_text("<Later, there will be fields here to set position (etc)>..."
                     "")

        dpg.add_button(
            label="Close and run sim",
            callback=go_callback
        )


def parse_from_window_settings() -> Situation:

    def bracket_extract(in_str: str):
        leftbracky = in_str.find("(")
        rightbracky = in_str.find(")")
        return in_str[leftbracky+1:rightbracky]

    stg_idx = int(bracket_extract(dpg.get_value("stg")))
    p1c_idx = int(bracket_extract(dpg.get_value("p1c")))
    p2c_idx = int(bracket_extract(dpg.get_value("p2c")))

    return Situation(
        stage=Stage(stg_idx),
        p1_character=Character(p1c_idx),
        p1_percent=int(dpg.get_value("p1p")),
        p1_platform=False,
        p1_x_position=5.0,
        p2_character=Character(p2c_idx),
        p2_percent=int(dpg.get_value("p2p")),
        p2_platform=False,
        p2_x_position=-10.0,
    )


def ptool_results_window():

    with dpg.window(tag="win_res", show=False):
        dpg.add_text("(Results go here.)", tag="resultsprint")
        with dpg.group(horizontal=True):
            with dpg.drawlist(width=300, height=200, tag="canvas", parent="ttip"):
                dpg.draw_rectangle(pmin=[10, 10], pmax=[290, 190])
            with dpg.plot(no_mouse_pos=True, height=200, width=300, tag="PLT"):
                dpg.add_plot_axis(dpg.mvXAxis, label="fox timing", lock_min=True, lock_max=True)
                with dpg.plot_axis(dpg.mvYAxis, label="falco timing", lock_min=True, lock_max=True):
                    dpg.add_heat_series([1.0, 0.0, 0.4, 0.5], 2, 2)
                    with dpg.tooltip(dpg.last_item(), tag="ttip"):
                        dpg.add_text("Tooltip text.", tag="tooltext")


def go_callback():
    # compose Situation Struct from the window contents:
    slvr: PayoffSolver = dpg.get_item_user_data("solver_dummy")
    slvr.situation = parse_from_window_settings()

    slvr._debug_solve()

    dpg.show_item("win_res")
    dpg.set_value("resultsprint", slvr.results)


if __name__ == "__main__":

    # Window layouts
    dpg.create_context()
    ptool_setup_window()
    ptool_results_window()

    # Viewport and final setup
    dpg.create_viewport(title="Tool1", width=300, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    # dpg.set_primary_window("win", True)

    # Data objects...
    host = Host()
    static_solver = PayoffSolver(host=host, situation=None)

    dpg.set_item_user_data("host_dummy", host)
    dpg.set_item_user_data("solver_dummy", static_solver)

    while dpg.is_dearpygui_running():
        if dpg.is_item_shown("canvas"):
            mouse_coords = dpg.get_plot_mouse_pos()
            res = dpg.get_item_user_data("solver_dummy").results

            # value_under_mouse = res[tuple(mouse_coords)]
            value_under_mouse = mouse_coords
            dpg.set_value("tooltext", str(value_under_mouse))
            dpg.delete_item("canvas", children_only=True)
            dpg.draw_rectangle(pmin=[10, 10], pmax=[290, 190], parent="canvas")
            dpg.draw_circle(
                center=(100 * mouse_coords[0], 200-(100 * mouse_coords[1])),
                radius=10,
                parent="canvas"
            )
            # if mouse_coords[0] > 0.1:
            #     breakpoint()

        dpg.render_dearpygui_frame()
    dpg.destroy_context()
