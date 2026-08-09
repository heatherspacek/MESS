import tkinter as tk
from tkinter import filedialog

import dearpygui.dearpygui as dpg
from melee.enums import Character, Stage
from mess.animations.data import retrieve_move_data
from platformdirs import user_cache_path

from ..messlib.interfaces.host import Host
from .behaviour import (
    go_callback,
    hide_actions_and_lock_variations,
    select_action,
    varybox_ticked,
)

CACHE_PATH = user_cache_path("mess.payofftool", "Heather Spacek", ensure_exists=True)


def tkinter_file_chooser() -> tuple[bool, str]:
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askopenfilename(
        title="Choose location of SSBM backup image...",
        initialdir=".",
        filetypes=[("GameCube Disk Image Backup", "*.iso")],
    )
    if folder_selected is not None:
        try:
            _ = retrieve_move_data(folder_selected, 1, 55)
        except Exception:
            return (False, "Issue reading selected file.")
        else:
            with open(CACHE_PATH / "last_seen_iso_path", "w") as f:
                f.write(folder_selected)
            return (True, folder_selected)


def ptool_choose_iso_window():

    def first_time_choose_iso():
        success, path = tkinter_file_chooser()
        if success:
            dpg.set_value("loaded_iso_path", path)
            dpg.hide_item("win_iso_browse")
            host: Host = dpg.get_item_user_data("host_dummy")
            host.console_setup()
        else:
            dpg.set_value("iso_browse_result_text", path)

    if dpg.does_item_exist("win_iso_browse"):
        dpg.show_item("win_iso_browse")
    else:
        with dpg.window(modal=True, tag="win_iso_browse"):
            dpg.add_button(
                label="Browse for SSBM backup image...",
                height=55,
                callback=first_time_choose_iso,
            )
            dpg.add_text("", tag="iso_browse_result_text")


def ptool_setup_window():

    with dpg.font_registry():
        dpg.add_font("res/NotoSans-Regular.ttf", 16 * 2, tag="default_font")
        dpg.add_font("res/NotoSans-Regular.ttf", 24 * 2, tag="header_font")
        dpg.add_font("res/NotoSans-Bold.ttf", 16 * 2, tag="bold_font")
        dpg.bind_font("default_font")
        dpg.set_global_font_scale(0.5)

    # TODO: get pretty :]
    with dpg.theme(tag="default_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBg, (255, 140, 23), category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
            )

    # dpg.bind_theme("default_theme")
    # dpg.show_style_editor()

    with dpg.window(tag="win_setup", pos=(0, 0), width=690, height=-1, no_close=True):
        with dpg.group(horizontal=True):
            dpg.add_text("SSBM Backup Path: ")
            dpg.add_text(tag="loaded_iso_path")
            dpg.add_button(
                label="(Click to change)", small=True, callback=ptool_choose_iso_window
            )

        with dpg.group(horizontal=True):
            with dpg.group(width=230):
                dpg.add_spacer(tag="host_dummy")
                dpg.add_spacer(tag="solver_dummy")
                dpg.add_text("Situation setup")
                dpg.bind_item_font(dpg.last_item(), "header_font")
                stages = [f"{e.name}({e.value})" for e in Stage]
                chars = [f"{c.name}({c.value})" for c in Character]
                dpg.add_combo(
                    items=stages,
                    label="Stage",
                    tag="stg",
                    default_value=stages[1],
                    callback=lambda a, b, x: print(b),
                )
                dpg.add_combo(
                    items=chars, label="P1 Char", tag="p1c", default_value=chars[1]
                )
                dpg.add_slider_int(label="P1 Percent", tag="p1p", max_value=200)
                dpg.add_combo(
                    items=chars, label="P2 Char", tag="p2c", default_value=chars[22]
                )
                dpg.add_slider_int(label="P2 Percent", tag="p2p", max_value=200)
                dpg.add_slider_float(
                    label="p1 x pos",
                    min_value=-75,
                    max_value=75,
                    default_value=-15,
                    tag="p1x",
                )
                dpg.add_checkbox(label="p1 plat?", tag="p1plat")
                dpg.add_checkbox(label="p1 face left?", tag="p1facing")
                dpg.add_slider_float(
                    label="p2 x pos",
                    min_value=-75,
                    max_value=75,
                    default_value=15,
                    tag="p2x",
                )
                dpg.add_checkbox(label="p2 plat?", tag="p2plat")
                dpg.add_checkbox(label="p2 face left?", tag="p2facing")
            # --------------------- horizontal split
            with dpg.group():
                with dpg.drawlist(tag="preview_canvas", width=370, height=200):
                    dpg.draw_rectangle(pmin=(5, 5), pmax=(365, 195))
                dpg.add_text("Current Actions:")
                dpg.bind_item_font(dpg.last_item(), "bold_font")
                with dpg.group(horizontal=True):
                    dpg.add_text("P1: ")
                    dpg.add_text("...", tag="p1_set_action_name")
                    dpg.add_text("(")
                    dpg.add_text("1", tag="p1_set_action_vary_count")
                    dpg.add_text(" variations)")
                with dpg.group(horizontal=True):
                    dpg.add_text("P2: ")
                    dpg.add_text("...", tag="p2_set_action_name")
                    dpg.add_text("(")
                    dpg.add_text("1", tag="p2_set_action_vary_count")
                    dpg.add_text(" variations)")
                dpg.add_button(
                    label="CLICK TO EDIT ACTIONS\n& PARAMETERS",
                    callback=lambda x: dpg.show_item("win_actions"),
                    width=-1,
                )
                dpg.add_button(label=" RUN ", callback=go_callback, height=45, width=-1)
                dpg.bind_item_font(dpg.last_item(), "header_font")


def ptool_progress_popup():
    with dpg.window(modal=True, show=False, pos=(50, 50), tag="win_progress"):
        dpg.add_text("", tag="progress_text")
        dpg.add_progress_bar(tag="progress_bar")


def ptool_results_window():
    with dpg.window(tag="win_res", pos=(400, 0), show=False):
        dpg.add_text("(Results go here.)", tag="resultsprint")
        with dpg.group(horizontal=True):
            with dpg.drawlist(width=300, height=200, tag="canvas"):
                dpg.draw_rectangle(pmin=[10, 10], pmax=[290, 190])
            with dpg.plot(no_mouse_pos=True, height=200, width=300, tag="PLT"):
                dpg.add_plot_axis(
                    dpg.mvXAxis,
                    label="[x axis]",
                    lock_min=True,
                    lock_max=True,
                    tag="plt_xaxis",
                )
                with dpg.plot_axis(
                    dpg.mvYAxis,
                    label="[y axis]",
                    lock_min=True,
                    lock_max=True,
                    tag="plt_yaxis",
                ):
                    dpg.add_heat_series([0.0], 1, 1, tag="plt_series", col_major=True)
                    dpg.add_spacer(width=0, height=0, tag="plt_xdata_container")
                    dpg.add_spacer(width=0, height=0, tag="paramaxis_x")
                    dpg.add_spacer(width=0, height=0, tag="paramaxis_y")
                    dpg.add_spacer(width=0, height=0, tag="paramaxis_rem")
                    with dpg.tooltip(dpg.last_item(), tag="ttip"):
                        dpg.add_text("", tag="tooltext")
        #
        with dpg.group(tag="sliders_dyngroup"):
            pass


def ptool_actions_popup():
    """The window for the user to define the actions each player should
    do, and the parameterization for each."""

    # Get predefined actions list from messlib.
    from ..messlib.data_structures.move_definitions import Actions

    actions_list = Actions.all_actions()

    with dpg.window(tag="win_actions", show=False, width=550, height=350, pos=(200, 0)):
        dpg.add_combo(
            actions_list,
            label="P1 Base Action",
            default_value="sh_back_air",
            callback=select_action,
            user_data="p1",
            tag="p1_base_action_choice",
        )
        dpg.add_group(tag="p1act_dynamicgroup", indent=25)
        select_action(None, "sh_back_air", "p1")
        dpg.add_combo(
            actions_list,
            label="P2 Base Action",
            default_value="jump_cancelled_upsmash",
            callback=select_action,
            user_data="p2",
            tag="p2_base_action_choice",
        )
        dpg.add_group(tag="p2act_dynamicgroup", indent=25)
        select_action(None, "jump_cancelled_upsmash", "p2")
        dpg.add_button(
            label="OK", callback=hide_actions_and_lock_variations, height=35, width=-1
        )
        dpg.bind_item_font(dpg.last_item(), "header_font")
        # some default parameters for a sweep:
        for chbox in [
            "p1_checkbox_slack_frames",
            "p1_checkbox_ff_frame",
            "p2_checkbox_frames_dashing",
        ]:
            dpg.set_value(chbox, True)
            varybox_ticked(chbox, None, None)
        dpg.set_value("p1_varyrange_slack_frames", (1, 5, 0, 0))
        dpg.set_value("p1_varyrange_ff_frame", (2, 3, 0, 0))
        dpg.set_value("p2_varyrange_frames_dashing", (2, 6, 0, 0))
        hide_actions_and_lock_variations()
