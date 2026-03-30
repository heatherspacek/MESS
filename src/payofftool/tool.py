import dearpygui.dearpygui as dpg
from melee.enums import Stage, Character

from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation
from .solver import PayoffSolver


def ptool_setup_window(settings_struct, settings_callback):

    dpg.create_context()

    with dpg.window(tag="win"):
        stages = [f"{e.name}({e.value})" for e in Stage]
        chars = [f"{c.name}({c.value})" for c in Character]
        dpg.add_combo(items=stages, label="Stage", tag="stg", default_value=stages[2])
        dpg.add_combo(items=chars, label="P1 Char", tag="p1c", default_value=chars[2])
        dpg.add_slider_float(label="P1 Percent", tag="p1p", max_value=300)
        dpg.add_combo(items=chars, label="P2 Char", tag="p2c", default_value=chars[2])
        dpg.add_slider_float(label="P2 Percent", tag="p2p", max_value=300)

        dpg.add_separator()
        dpg.add_text("<Later, there will be fields here to set position (etc)>")

        dpg.add_button(
            label="Close and run sim",
            callback=settings_callback,
            user_data=settings_struct
        )

    dpg.create_viewport(title="Tool1", width=300, height=200)
    dpg.setup_dearpygui()

    dpg.show_viewport()
    dpg.set_primary_window("win", True)

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()


def parse_from_window_settings(settings_dict: dict) -> Situation:

    def bracket_extract(in_str: str):
        leftbracky = in_str.find("(")
        rightbracky = in_str.find(")")
        return in_str[leftbracky+1:rightbracky]

    stg_idx = int(bracket_extract(ptool_user_settings["stg"]))
    p1c_idx = int(bracket_extract(ptool_user_settings["p1c"]))
    p2c_idx = int(bracket_extract(ptool_user_settings["p2c"]))

    return Situation(
        stage=Stage(stg_idx),
        p1_character=Character(p1c_idx),
        p1_percent=ptool_user_settings["p1p"],
        p1_platform=False,
        p1_x_position=5.0,
        p2_character=Character(p2c_idx),
        p2_percent=ptool_user_settings["p2p"],
        p2_platform=False,
        p2_x_position=-10.0,
    )


if __name__ == "__main__":
    ptool_user_settings = {}

    def propagate_settings_cbk(sender, app_data, user_data: dict):
        for key in ["stg", "p1c", "p1p", "p2c", "p2p"]:
            user_data.update({key: dpg.get_value(key)})
        dpg.delete_item(dpg.get_active_window())
        dpg.stop_dearpygui()

    # dpg.create_context()
    # dpg.show_implot_demo()
    ptool_setup_window(ptool_user_settings, propagate_settings_cbk)

    host = Host()
    initial_situation = parse_from_window_settings(ptool_user_settings)
    static_solver = PayoffSolver(host=host, situation=initial_situation)
    static_solver.initial_setup()
    breakpoint()
