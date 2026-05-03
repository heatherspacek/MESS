import tkinter as tk
from tkinter import filedialog

import dearpygui.dearpygui as dpg
from melee.enums import Stage, Character

from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation
from ..messlib.data_structures.classes import FacingDirection
from .solver import PayoffSolver

from mess.animations.vis import lerp_2d
from mess.animations.data import retrieve_move_data, HurtBoxProcessed
from .structures import PayoffReplayFrame

import numpy as np

from platformdirs import user_cache_path

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
    return (False, "No file selected.")


def ptool_choose_iso_window():

    def first_time_choose_iso():
        success, path = tkinter_file_chooser()
        if success:
            dpg.set_value("loaded_iso_path", path)
            dpg.hide_item("win_iso_browse")
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
            with dpg.group(width=200):
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
                    label="p1 x pos", min_value=-75, max_value=75, default_value=0
                )
                dpg.add_checkbox(label="p1 plat?")
                dpg.add_slider_float(
                    label="p2 x pos", min_value=-75, max_value=75, default_value=0
                )
                dpg.add_checkbox(label="p2 plat?")
                dpg.add_text("Current Actions:")
                dpg.add_text("P1: bair | P2: dash, usmash")
                dpg.add_button(
                    label="CLICK TO EDIT ACTIONS \n& PARAMETERS",
                    callback=lambda x: dpg.show_item("win_actions"),
                )
            #
            with dpg.drawlist(tag="setup_dlist", width=370, height=300):
                dpg.draw_rectangle(pmin=(5, 5), pmax=(365, 295))
        #
        dpg.add_separator()
        with dpg.group(horizontal=True):
            dpg.add_button(label=" RUN ", callback=go_callback, height=65, width=-1)
            dpg.bind_item_font(dpg.last_item(), "large_font")


def ptool_progress_popup():
    with dpg.window(modal=True, show=False, pos=(50, 50), tag="win_progress"):
        dpg.add_text("", tag="progress_text")
        dpg.add_progress_bar(tag="progress_bar")


def ptool_actions_popup():
    """The window for the user to define the actions each player should
    do, and the parameterization for each."""

    with dpg.window(tag="win_actions", show=False):
        dpg.add_combo(
            ["floop"],
            label="P1 Base Action",
            callback=lambda x: dpg.add_checkbox(
                label="bweh", parent="p1act_dynamicgroup"
            ),
        )
        dpg.add_group(tag="p1act_dynamicgroup")
        dpg.add_combo(
            ["gloop"],
            label="P2 Base Action",
            callback=lambda x: dpg.add_checkbox(
                label="bweh", parent="p2act_dynamicgroup"
            ),
        )
        dpg.add_group(tag="p2act_dynamicgroup")


def bracket_extract(in_str: str):
    leftbracky = in_str.find("(")
    rightbracky = in_str.find(")")
    return in_str[leftbracky + 1 : rightbracky]


def parse_from_window_settings() -> Situation:

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
        p2_x_position=-19.0,
    )


def ptool_results_window():
    with dpg.window(tag="win_res", pos=(400, 0), show=False):
        dpg.add_text("(Results go here.)", tag="resultsprint")
        with dpg.group(horizontal=True):
            with dpg.drawlist(width=300, height=200, tag="canvas"):
                dpg.draw_rectangle(pmin=[10, 10], pmax=[290, 190])
            with dpg.plot(no_mouse_pos=True, height=200, width=300, tag="PLT"):
                dpg.add_plot_axis(
                    dpg.mvXAxis,
                    label="fox timing",
                    lock_min=True,
                    lock_max=True,
                    tag="plt_xaxis",
                )
                with dpg.plot_axis(
                    dpg.mvYAxis,
                    label="falco timing",
                    lock_min=True,
                    lock_max=True,
                    tag="plt_yaxis",
                ):
                    dpg.add_heat_series([0.0], 1, 1, tag="plt_series", col_major=True)
                    with dpg.tooltip(dpg.last_item(), tag="ttip"):
                        dpg.add_text("", tag="tooltext")


def go_callback():
    # compose Situation Struct from the window contents:
    slvr: PayoffSolver = dpg.get_item_user_data("solver_dummy")
    sitch = parse_from_window_settings()
    slvr.host.situation_setup(sitch)
    slvr.host.save_savestate()
    # ^ surely this can go in situation_setup someday.

    input_sets = slvr.compose_sims(range(1, 8), range(1, 8))
    dpg.show_item("win_progress")
    slvr.results = slvr.run_sims(
        input_sets,
        lambda x: dpg.set_value("progress_text", x),
        lambda x: dpg.set_value("progress_bar", x),
    )
    slvr.host.console.stop()
    dpg.hide_item("win_progress")
    dpg.configure_item("win_setup", collapsed=True)
    dpg.show_item("win_res")
    display_results(slvr.results)


def display_results(solver_results):
    """Configure the results window, the plot series, the replay view,
    etc etc. The structure of solver_results is {k: v} where k is the
    tuple of (x,y) to plot, and v is (outcome, [frames_list])"""
    OUTCOME_MAPPING = {"Falco win": 0.0, "Fox win": 1.0, "Whiff": 0.4, "Trade": 0.6}
    outcomes_numeric = [OUTCOME_MAPPING[v[0]] for v in solver_results.values()]
    outcomes_x = set([k[0] for k in solver_results.keys()])
    outcomes_y = set([k[1] for k in solver_results.keys()])
    dpg.configure_item(
        "plt_series",
        cols=len(outcomes_x),
        rows=len(outcomes_y),
        x=outcomes_numeric,
    )
    dpg.set_item_user_data("plt_series", outcomes_numeric)
    autoticks_x = np.arange(0, 1, 0.5 / (len(outcomes_x)))[1::2]
    tickmap_x = tuple((str(k), v) for k, v in zip(sorted(outcomes_x), autoticks_x))
    dpg.set_axis_ticks("plt_xaxis", label_pairs=tickmap_x)
    dpg.set_item_user_data("plt_xaxis", tickmap_x)
    autoticks_y = np.arange(0, 1, 0.5 / (len(outcomes_y)))[1::2]
    tickmap_y = tuple((str(k), v) for k, v in zip(sorted(outcomes_y), autoticks_y))
    dpg.set_axis_ticks("plt_yaxis", label_pairs=tickmap_y)
    dpg.set_item_user_data("plt_yaxis", tickmap_y)


def mouseover_plot_react(mouse_coords):
    plt_val = dpg.get_item_user_data("plt_series")
    plt_x = np.array([xi[1] for xi in dpg.get_item_user_data("plt_xaxis")])
    bound_x = plt_x - plt_x[0]
    plt_y = np.array([yi[1] for yi in dpg.get_item_user_data("plt_yaxis")])
    bound_y = plt_y - plt_y[0]
    shaped = np.reshape(plt_val, (len(plt_x), len(plt_y)))
    sel_x = np.argmax(bound_x > mouse_coords[0]) - 1
    sel_y = np.argmax(bound_y > mouse_coords[1]) - 1
    shaped[sel_x, -sel_y - 1] = 0.27
    dpg.configure_item("plt_series", x=shaped.flatten().tolist())

    res = dpg.get_item_user_data("solver_dummy").results
    # Sentinel value... TODO fixup
    hover_key = list(res.keys())[np.argmax(shaped == 0.27)]
    dpg.set_value("tooltext", res[hover_key][0])
    dpg.set_value("resultsprint", hover_key)
    # just in case its casting to string implicitly:
    dpg.set_item_user_data("resultsprint", hover_key)


def dpg_draw_capsule(y1, z1, y2, z2, size, color=(255, 255, 255, 255)):
    for t in [a / 9 for a in range(10)]:
        x, y = lerp_2d((y1, z1), (y2, z2), t)
        dpg.draw_circle([x, y], size, parent="canvas", color=color)


def draw_replay_frame():
    res = dpg.get_item_user_data("solver_dummy").results
    if res is None:
        return  # no results yet.

    results_index_tuple = dpg.get_item_user_data("resultsprint")
    if results_index_tuple is None:
        results_index_tuple = list(res.keys())[0]

    replay = res[results_index_tuple][1]
    indices_loop = list(range(len(replay)))
    for _ in range(7):
        indices_loop.append(indices_loop[-1])

    frame_loop_i = indices_loop[(dpg.get_frame_count() // 2) % len(indices_loop)]
    repl_frame_to_draw: PayoffReplayFrame = replay[frame_loop_i]

    p1x = repl_frame_to_draw.p1_pos.x
    p1y = repl_frame_to_draw.p1_pos.y
    p1f = repl_frame_to_draw.p1_facing
    p2x = repl_frame_to_draw.p2_pos.x
    p2y = repl_frame_to_draw.p2_pos.y
    p2f = repl_frame_to_draw.p2_facing

    from ..messlib.data_structures.translations import LIBMELEE_TO_DEMANGLED

    p1color = (200, 200, 255, 255)
    p2color = (200, 255, 200, 255)
    if "DAMAGE" in repl_frame_to_draw.p1_game_action.name:
        p1color = (200, 200 / 1.3, 255 / 1.3, 255)
    if "DAMAGE" in repl_frame_to_draw.p2_game_action.name:
        p2color = (200, 255 / 1.3, 200 / 1.3, 255)

    from mess.animations.data import retrieve_character_data

    isopath = dpg.get_value("loaded_iso_path")

    animations_list_ch1, _, _ = retrieve_character_data(
        isopath,
        int(bracket_extract(dpg.get_value("p1c"))),
    )
    animations_list_ch2, _, _ = retrieve_character_data(
        isopath,
        int(bracket_extract(dpg.get_value("p2c"))),
    )

    hurts1, hits1 = retrieve_move_data(
        isopath,
        int(bracket_extract(dpg.get_value("p1c"))),
        animations_list_ch1.index(
            LIBMELEE_TO_DEMANGLED[repl_frame_to_draw.p1_game_action]
        ),
    )
    hurts2, hits2 = retrieve_move_data(
        isopath,
        int(bracket_extract(dpg.get_value("p2c"))),
        animations_list_ch2.index(
            LIBMELEE_TO_DEMANGLED[repl_frame_to_draw.p2_game_action]
        ),
    )

    hurts1_thisframe: list[HurtBoxProcessed] = hurts1[
        (repl_frame_to_draw.p1_game_action_frame) % len(hurts1)
    ]
    hurts2_thisframe: list[HurtBoxProcessed] = hurts2[
        (repl_frame_to_draw.p2_game_action_frame) % len(hurts2)
    ]
    hits1_thisframe = [
        h for h in hits1 if h.frame_i == repl_frame_to_draw.p1_game_action_frame
    ]
    hits2_thisframe = [
        h for h in hits2 if h.frame_i == repl_frame_to_draw.p2_game_action_frame
    ]

    dpg.delete_item("canvas", children_only=True)
    dpg.draw_rectangle(pmin=[10, 10], pmax=[290, 190], parent="canvas")

    DRAW_SCALE = 4
    X_DRAW_OFFSET = 35
    Y_DRAW_OFFSET = 30

    def x_tform(x, world_x, facing: FacingDirection):
        x_faced = -x if facing == "LEFT" else x
        return DRAW_SCALE * (X_DRAW_OFFSET + world_x + x_faced)

    def y_tform(y, world_y):
        return DRAW_SCALE * (Y_DRAW_OFFSET - (world_y + y))

    for hx in hurts1_thisframe:
        x1, y1, z1 = hx.pos_a
        x2, y2, z2 = hx.pos_b
        scale = hx.size
        dpg_draw_capsule(
            x_tform(z1, p1x, p1f),
            y_tform(y1, p1y),
            x_tform(z2, p1x, p1f),
            y_tform(y2, p1y),
            scale * DRAW_SCALE,
            color=p1color,
        )
    for hx in hurts2_thisframe:
        x1, y1, z1 = hx.pos_a
        x2, y2, z2 = hx.pos_b
        scale = hx.size
        dpg_draw_capsule(
            x_tform(z1, p2x, p2f),
            y_tform(y1, p2y),
            x_tform(z2, p2x, p2f),
            y_tform(y2, p2y),
            scale * DRAW_SCALE,
            color=p2color,
        )
    for htx in hits1_thisframe:
        _, y, z = htx.pos
        dpg.draw_circle(
            (
                x_tform(z, p1x, p1f),
                y_tform(y, p1y),
            ),
            htx.size * DRAW_SCALE,
            parent="canvas",
            color=(255, 0, 0, 255),
        )
    for htx in hits2_thisframe:
        _, y, z = htx.pos
        dpg.draw_circle(
            (
                x_tform(z, p2x, p2f),
                y_tform(y, p2y),
            ),
            htx.size * DRAW_SCALE,
            parent="canvas",
            color=(255, 0, 0, 255),
        )


if __name__ == "__main__":
    dpg.create_context()

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
    host = Host()
    static_solver = PayoffSolver(host=host, situation=None)

    dpg.set_item_user_data("host_dummy", host)
    dpg.set_item_user_data("solver_dummy", static_solver)

    while dpg.is_dearpygui_running():
        if dpg.is_item_shown("canvas"):
            mouse_coords = dpg.get_plot_mouse_pos()
            if mouse_coords[0] > 0.0:
                mouseover_plot_react(mouse_coords)
            draw_replay_frame()

        dpg.render_dearpygui_frame()
    dpg.destroy_context()
