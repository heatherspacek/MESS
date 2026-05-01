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


def ptool_setup_window():

    with dpg.font_registry():
        dpg.add_font("res/NotoSans-Regular.ttf", 16 * 2, tag="default_font")
        dpg.add_font("res/NotoSans-Bold.ttf", 16 * 2, tag="bold_font")
        dpg.bind_font("default_font")
        dpg.set_global_font_scale(0.5)

    with dpg.window(tag="win_setup", pos=(0, 0)):
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
        with dpg.drawlist(tag="setup_dlist", width=250, height=200):
            dpg.draw_rectangle(pmin=(5, 5), pmax=(245, 195))

        dpg.add_button(label="Close and run sim", callback=go_callback)

def ptool_progress_popup():
    with dpg.window(modal=True, show=False, pos=(200, 200), tag="win_progress"):
        dpg.add_text("", tag="progress_text")
        dpg.add_progress_bar(tag="progress_bar")

def parse_from_window_settings() -> Situation:

    def bracket_extract(in_str: str):
        leftbracky = in_str.find("(")
        rightbracky = in_str.find(")")
        return in_str[leftbracky + 1 : rightbracky]

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
    slvr.situation = parse_from_window_settings()
    slvr._debug_solve()

    # dpg.set_value("resultsprint", slvr.results)
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
    print(frame_loop_i)
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

    animations_list_ch1, _, _ = retrieve_character_data(
        "/home/heather/Documents/Disk Images/Super Smash Bros. Melee (v1.02).iso",
        1,
    )
    animations_list_ch2, _, _ = retrieve_character_data(
        "/home/heather/Documents/Disk Images/Super Smash Bros. Melee (v1.02).iso",
        22,
    )

    hurts1, hits1 = retrieve_move_data(
        "/home/heather/Documents/Disk Images/Super Smash Bros. Melee (v1.02).iso",
        1,
        animations_list_ch1.index(
            LIBMELEE_TO_DEMANGLED[repl_frame_to_draw.p1_game_action]
        ),
    )
    hurts2, hits2 = retrieve_move_data(
        "/home/heather/Documents/Disk Images/Super Smash Bros. Melee (v1.02).iso",
        22,
        animations_list_ch2.index(
            LIBMELEE_TO_DEMANGLED[repl_frame_to_draw.p2_game_action]
        ),
    )

    hurts1_thisframe: list[HurtBoxProcessed] = hurts1[
        (repl_frame_to_draw.p1_game_action_frame + 1) % len(hurts1)
    ]
    hurts2_thisframe: list[HurtBoxProcessed] = hurts2[
        (repl_frame_to_draw.p2_game_action_frame + 1) % len(hurts2)
    ]
    hits1_thisframe = [
        h for h in hits1 if h.frame_i == repl_frame_to_draw.p1_game_action_frame + 1
    ]
    hits2_thisframe = [
        h for h in hits2 if h.frame_i == repl_frame_to_draw.p2_game_action_frame + 1
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
    # Window layouts
    dpg.create_context()
    ptool_setup_window()
    ptool_results_window()
    ptool_progress_popup()

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
