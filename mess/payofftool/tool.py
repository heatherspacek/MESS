import dearpygui.dearpygui as dpg
from platformdirs import user_cache_path

from ..messlib.interfaces.host import Host
from .behaviour import mouseover_plot_react
from .drawing import draw_preview_frame, draw_replay_frame
from .layout import (
    ptool_actions_popup,
    ptool_choose_iso_window,
    ptool_progress_popup,
    ptool_results_window,
    ptool_setup_window,
)
from .solver import PayoffSolver

CACHE_PATH = user_cache_path("mess.payofftool", "Heather Spacek", ensure_exists=True)


def _entrypoint_payofftool():
    dpg.create_context()

    # global theme!
    with dpg.theme() as global_theme:
        # darks
        NORD0 = (46, 52, 64)
        NORD1 = (59, 66, 82)
        NORD2 = (67, 76, 94)
        NORD3 = (76, 86, 106)
        # whites
        NORD4 = (216, 222, 233)
        NORD5 = (229, 233, 240)
        NORD6 = (236, 239, 244)
        # blues
        NORD7 = (143, 188, 187)
        NORD8 = (136, 192, 208)
        NORD9 = (129, 161, 193)
        NORD10 = (94, 129, 172)
        # accents
        NORD11 = (191, 97, 106)  # red
        NORD12 = (208, 135, 112)  # orge
        NORD13 = (235, 203, 139)  # ylw
        NORD14 = (163, 190, 140)  # green
        NORD15 = (180, 142, 173)  # purp

        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 2, 2)
            # dpg.add_theme_style(dpg.mvStyleVar_ItemInnerSpacing, 0, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 3)

            dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 25)

            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, NORD0)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, NORD0)

            dpg.add_theme_color(dpg.mvThemeCol_Button, NORD1)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, NORD1)
            dpg.add_theme_color(dpg.mvThemeCol_Border, NORD4)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, NORD2)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, NORD2)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, NORD3)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, NORD3)
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, NORD10)
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, NORD10)

            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, NORD9)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, NORD9)
            dpg.add_theme_color(dpg.mvThemeCol_Header, NORD10)

            dpg.add_theme_color(dpg.mvThemeCol_Text, NORD6)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, NORD7)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, NORD8)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, NORD9)

            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, NORD1)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, NORD2)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, NORD3)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, NORD8)

            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, NORD10)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, NORD3)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, NORD1)
    dpg.bind_theme(global_theme)

    # Window layouts, including hidden
    ptool_setup_window()
    ptool_results_window()
    ptool_progress_popup()
    ptool_actions_popup()

    # Modal pop-up on first load
    try:
        with open(CACHE_PATH / "last_seen_iso_path", "r") as f:
            last_seen_iso_path = f.read()
    except FileNotFoundError:
        # no last-seen
        dpg.set_value("loaded_iso_path", "")
    else:
        dpg.set_value("loaded_iso_path", last_seen_iso_path)

    if not dpg.get_value("loaded_iso_path"):
        ptool_choose_iso_window()

    # Viewport and final setup
    dpg.create_viewport(title="Payoff Tool", width=700, height=550)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Data objects...
    host = Host(dpg.get_value("loaded_iso_path"))
    static_solver = PayoffSolver(host=host, situation=None)

    dpg.set_item_user_data("host_dummy", host)
    dpg.set_item_user_data("solver_dummy", static_solver)

    while dpg.is_dearpygui_running():
        if dpg.is_item_shown("canvas"):
            mouse_coords = dpg.get_plot_mouse_pos()
            if mouse_coords[0] > 0.0:
                mouseover_plot_react(mouse_coords)
            draw_replay_frame()
            draw_preview_frame()
        else:
            # TODO: this `if` is not right, I don't think this ever gets
            # called.
            draw_preview_frame()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
    dpg.stop_dearpygui()


if __name__ == "__main__":
    _entrypoint_payofftool()
